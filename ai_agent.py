import os
import json
import logging
from typing import Any
from google import genai
from google.genai import types
from google.genai.errors import APIError

from calculations import calculate_transport_emissions, calculate_electricity_emissions

# Configure standard enterprise logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_MODEL: str = 'gemini-2.5-flash'
DEFAULT_TEMPERATURE: float = 0.2


def get_client() -> genai.Client:
    """
    Initialize and securely return the Gemini client.
    
    Returns:
        genai.Client: Configured client instance.
        
    Raises:
        ValueError: If GEMINI_API_KEY is not found in environment or Streamlit secrets.
    """
    api_key: str | None = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("GEMINI_API_KEY")
        except ImportError:
            logger.warning("Streamlit not installed or secrets unavailable.")
            
    if not api_key:
        logger.error("Failed to initialize Gemini client: API Key missing.")
        raise ValueError("GEMINI_API_KEY not found in environment or secrets.")
        
    return genai.Client(api_key=api_key)


def process_user_input(user_text: str) -> dict[str, Any]:
    """
    Parses unstructured user text, identifies carbon-emitting activities, 
    and returns computed footprints alongside AI-generated advice.
    
    Args:
        user_text (str): The natural language input from the user.
        
    Returns:
        dict[str, Any]: A structured dictionary containing:
            - success (bool): True if parsing was successful, False otherwise.
            - activities (list[dict]): Processed activities with emission values.
            - total_emission_kg (float): Total footprint for the parsed text.
            - advice (str): Actionable recommendation.
            - error (str, optional): Error message if success is False.
    """
    try:
        client: genai.Client = get_client()
    except ValueError as e:
        return {"success": False, "error": str(e)}

    system_prompt: str = """
    You are a Principal Carbon Footprint AI Assistant.
    Analyze the user's daily activities from the text.
    Extract carbon-emitting activities related to 'transport' (distance in km and mode like 'petrol car', 'ev', 'bus') 
    or 'electricity' (hours and appliance like 'ac', 'heater', 'laptop').
    
    Also, generate a brief, highly contextual, and actionable recommendation to reduce their specific emissions 
    in a cyber-forensic, data-driven tone.
    
    Return the output STRICTLY as a JSON object with this schema:
    {
        "activities": [
            {
                "category": "transport" | "electricity",
                "item": "petrol car" | "ac" | etc,
                "amount": numeric_value
            }
        ],
        "advice": "Your actionable advice here in short."
    }
    """
    
    try:
        logger.info("Sending request to Gemini API.")
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=user_text,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                temperature=DEFAULT_TEMPERATURE
            )
        )
        
        # Guard against empty response
        if not response.text:
            logger.warning("Received empty text from Gemini API.")
            raise ValueError("Empty response from AI model.")

        result_json: dict[str, Any] = json.loads(response.text)
        
        # Calculate total footprint
        total_footprint: float = 0.0
        processed_activities: list[dict[str, Any]] = []
        
        activities: list[dict[str, Any]] = result_json.get("activities", [])
        
        if not activities:
            logger.info("No actionable carbon activities identified in user input.")
            # Treat this as a valid, but empty parsing (irrelevant input)
            return {
                "success": True,
                "activities": [],
                "total_emission_kg": 0.0,
                "advice": result_json.get("advice", "No carbon-related activities detected. Try logging a commute or appliance usage.")
            }
            
        for act in activities:
            cat: str = act.get("category", "")
            item: str = act.get("item", "")
            amount: float = float(act.get("amount", 0.0))
            
            emission: float = 0.0
            if cat == "transport":
                emission = calculate_transport_emissions(amount, item)
            elif cat == "electricity":
                emission = calculate_electricity_emissions(amount, item)
            else:
                logger.warning(f"Unknown category '{cat}' received from AI.")
                continue
                
            total_footprint += emission
            processed_activities.append({
                "category": cat,
                "item": item,
                "amount": amount,
                "emission_kg": emission
            })
            
        logger.info(f"Successfully processed user input. Total footprint: {total_footprint} kg.")
        
        return {
            "success": True,
            "activities": processed_activities,
            "total_emission_kg": round(total_footprint, 2),
            "advice": result_json.get("advice", "No advice generated.")
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response from Gemini: {e}")
        return {"success": False, "error": "AI returned malformed JSON."}
    except APIError as e:
        logger.error(f"Gemini API Error occurred: {e}")
        return {"success": False, "error": "AI Service Timeout or API Error. Please try again later."}
    except Exception as e:
        logger.exception("Unexpected error during process_user_input.")
        return {"success": False, "error": f"An unexpected error occurred: {str(e)}"}
