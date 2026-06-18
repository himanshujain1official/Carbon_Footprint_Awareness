import json
import pytest
from unittest.mock import patch, MagicMock
from google.genai.errors import APIError

from ai_agent import process_user_input

# --- FIXTURES ---

@pytest.fixture
def mock_gemini_client():
    """
    Fixture to mock the genai.Client globally so real API calls are never made during tests.
    """
    with patch('ai_agent.get_client') as mock_get_client:
        mock_client_instance = MagicMock()
        mock_get_client.return_value = mock_client_instance
        yield mock_client_instance


# --- TESTS ---

class TestAIAgent:

    def test_process_user_input_happy_path(self, mock_gemini_client):
        """
        Scenario 1: The Happy Path. 
        Mock a successful API response with correctly formatted JSON data.
        """
        # Prepare the mocked JSON response text that Gemini would return
        mock_response_text = json.dumps({
            "activities": [
                {
                    "category": "transport",
                    "item": "petrol car",
                    "amount": 20.0
                }
            ],
            "advice": "Consider carpooling to reduce your transport footprint."
        })
        
        # Configure the mock to return an object with a .text attribute
        mock_response_obj = MagicMock()
        mock_response_obj.text = mock_response_text
        mock_gemini_client.models.generate_content.return_value = mock_response_obj
        
        user_text = "I drove 20km in my petrol car today."
        result = process_user_input(user_text)
        
        # Assertions
        assert result["success"] is True
        assert len(result["activities"]) == 1
        assert result["activities"][0]["category"] == "transport"
        assert result["activities"][0]["amount"] == 20.0
        # 20km * 0.19 (petrol car factor) = 3.8
        assert result["total_emission_kg"] == 3.8
        assert "Consider carpooling" in result["advice"]
        
        # Ensure the mock was actually called
        mock_gemini_client.models.generate_content.assert_called_once()

    def test_process_user_input_api_error(self, mock_gemini_client):
        """
        Scenario 2: API Timeout/Error.
        Mock the genai.Client raising an exception to test the try-except fallback.
        """
        # Configure the mock to explicitly raise an APIError
        mock_gemini_client.models.generate_content.side_effect = APIError("Timeout connecting to Gemini API.")
        
        user_text = "I left the AC on for 5 hours."
        result = process_user_input(user_text)
        
        # Assertions
        assert result["success"] is False
        assert "API Error" in result["error"] or "Timeout" in result["error"]
        
    def test_process_user_input_irrelevant_input(self, mock_gemini_client):
        """
        Scenario 3: Irrelevant/Ambiguous Input.
        Mock a scenario where the AI returns an empty activities list.
        """
        mock_response_text = json.dumps({
            "activities": [],
            "advice": "I don't see any carbon-related activities in your message."
        })
        
        mock_response_obj = MagicMock()
        mock_response_obj.text = mock_response_text
        mock_gemini_client.models.generate_content.return_value = mock_response_obj
        
        user_text = "What is the capital of France?"
        result = process_user_input(user_text)
        
        # Assertions
        assert result["success"] is True
        assert len(result["activities"]) == 0
        assert result["total_emission_kg"] == 0.0
        assert "carbon-related activities" in result["advice"]
