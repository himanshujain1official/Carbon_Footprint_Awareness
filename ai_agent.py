import os
import json
from google import genai
from google.genai import types
from calculations import calculate_transport_emissions, calculate_electricity_emissions

# Initialize the Gemini client securely
# Streamlit secrets or os.environ will be used to pass the key
def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            pass
            
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment or secrets.")
    return genai.Client(api_key=api_key)

def process_user_input(user_text: str) -> dict:
    """
    Parses unstructured text, identifies activities, and returns computed footprint and advice.
    Uses gemini-2.5-flash for high speed and efficiency.
    """
    client = get_client()
    
    # Prompt engineering to strictly extract structured data and personalized advice
    system_prompt = """
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
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                temperature=0.2
            )
        )
        
        result_json = json.loads(response.text)
        
        # Calculate total footprint using our validated math functions
        total_footprint = 0.0
        processed_activities = []
        
        for act in result_json.get("activities", []):
            cat = act.get("category")
            item = act.get("item", "")
            amount = float(act.get("amount", 0))
            
            emission = 0.0
            if cat == "transport":
                emission = calculate_transport_emissions(amount, item)
            elif cat == "electricity":
                emission = calculate_electricity_emissions(amount, item)
                
            total_footprint += emission
            processed_activities.append({
                "category": cat,
                "item": item,
                "amount": amount,
                "emission_kg": emission
            })
            
        return {
            "success": True,
            "activities": processed_activities,
            "total_emission_kg": round(total_footprint, 2),
            "advice": result_json.get("advice", "No advice generated.")
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
