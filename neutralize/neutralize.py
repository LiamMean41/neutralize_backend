from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from neutralize.GPT.work import analyze_bias

from schemas import BiasRequest

neu = APIRouter()

@neu.post("/analyze_bias")
def analyze_bias_endpoint(request: BiasRequest):
    try:
        explanation = analyze_bias(request.text, request.bias_level)
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))