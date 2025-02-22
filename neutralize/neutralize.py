from fastapi import Depends
from service.oauth import get_current_user
from schemas import User, BiasRequest, TextRequest
from fastapi import HTTPException
from neutralize.GPT import GPT_ana
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from fastapi import APIRouter

neu = APIRouter()

@neu.post("/gpt_analyze/")
async def analyze_bias_endpoint(request: BiasRequest, current_user: User = Depends(get_current_user)):
    try:
        explanation = GPT_ana(request.text, request.bias_level)
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@neu.post("/analyze/")
async def analyze_bias(request: TextRequest, current_user: User = Depends(get_current_user)):
    try:
        inputs = tokenizer(request.text, return_tensors="pt")
        with torch.no_grad():
            logits = model(**inputs).logits
            probabilities = logits.softmax(dim=-1)[0].tolist()

        categories = ["Left", "Center", "Right"]
        bias_result = {categories[i]: probabilities[i] for i in range(len(categories))}

        return {"bias_analysis": bias_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@neu.post("/analyze_mult/")
async def analyze_bias(request: TextRequest, current_user: User = Depends(get_current_user)):
    try:
        # Analyze bias using PoliticalBiasBERT
        inputs = tokenizer(request.text, return_tensors="pt")
        with torch.no_grad():
            logits = model(**inputs).logits
            probabilities = logits.softmax(dim=-1)[0].tolist()
        categories = ["Left", "Middle", "Right"]
        bias_result = {categories[i]: probabilities[i] for i in range(len(categories))}

        # Analyze text bias using GPT
        explanation = GPT_ana(request.text, bias_result)
        return {"bias_analysis": bias_result, "explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))