from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_recommendation import get_recommendation

app = FastAPI()

class RecommendationRequest(BaseModel):
    livestock: dict
    feed_plans: list
    health_records: list

@app.post("/recommendation")
async def get_ai_recommendation(request: RecommendationRequest):
    try:
        recommendation = get_recommendation(
            livestock_data=request.livestock,
            feed_plans=request.feed_plans,
            health_records=request.health_records
        )
        return recommendation
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")