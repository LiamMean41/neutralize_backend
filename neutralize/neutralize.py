from fastapi import FastAPI, HTTPException
from fastapi import APIRouter
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

from schemas import BiasRequest, TextRequest

neu = APIRouter()

@neu.post("/gpt_analyze/")
async def analyze_bias_endpoint(request: BiasRequest):
    try:
        explanation = analyze_bias(request.text, request.bias_level)
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
MODEL_NAME = "bucketresearch/politicalBiasBERT"
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

@neu.post("/analyze/")
async def analyze_bias(request: TextRequest):
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