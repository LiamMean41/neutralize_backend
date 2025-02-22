from fastapi import FastAPI, HTTPException
from fastapi import APIRouter
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from neutralize.GPT.work import GPT_ana
from neutralize.NLP.nlp_model import NLP_ana

from schemas import BiasRequest, TextRequest

neu = APIRouter()

@neu.post("/gpt_analyze/")
async def analyze_bias_endpoint(request: BiasRequest):
    try:
        explanation = GPT_ana(request.text, request.bias_level)
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@neu.post("/analyze/")
async def analyze_bias(request: TextRequest):
    try:
        bias_result = NLP_ana(request.text)
        return {"bias_analysis": bias_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Integrated API
# NLP + GPT
# Endpoint: /analyze_mult/
@neu.post("/analyze_mult/")
async def analyze_bias(request: TextRequest):
    try:
        # Analyze bias using NLP_ana
        bias_result = NLP_ana(request.text)

        # Analyze text bias using GPT
        explanation = GPT_ana(request.text, bias_result)
        return {"bias_analysis": bias_result, "explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))