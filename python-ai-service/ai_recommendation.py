import requests
import json
from fastapi import HTTPException

XAI_API_URL = "https://api.x.ai/v1/recommendations"
XAI_API_KEY = "your-xai-api-key"  # Replace with actual API key from xAI

def get_recommendation(livestock_data, feed_plans, health_records):
    # Prepare data for xAI API
    input_data = {
        "livestock": {
            "type": livestock_data["type"],
            "animalId": livestock_data["animalId"],
            "age": livestock_data["age"],
            "weight": livestock_data["weight"]
        },
        "feed_plans": feed_plans,
        "health_records": health_records
    }

    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(XAI_API_URL, headers=headers, json=input_data, timeout=10)
        response.raise_for_status()
        result = response.json()

        # Validate and structure the response
        if not all(key in result for key in ["type", "recommendation", "confidence"]):
            raise ValueError("Invalid response from xAI API")

        return {
            "type": result["type"],
            "recommendation": result["recommendation"],
            "confidence": float(result["confidence"])
        }
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"xAI API request failed: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Invalid xAI API response: {str(e)}")