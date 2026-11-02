"""
SARAS ATLAS — AI Decision Intelligence Routes
"""

from typing import List
from fastapi import APIRouter, Depends
from src.domain.intelligence.models import QuestionRequest, IntelligenceResponse
from src.domain.intelligence.engine import DecisionIntelligenceEngine
from src.security.models import User
from src.security.auth import get_current_user

router = APIRouter(prefix="/intelligence", tags=["AI Decision Intelligence"])


@router.post("/query", response_model=IntelligenceResponse)
def query_intelligence(request: QuestionRequest, user: User = Depends(get_current_user)):
    engine = DecisionIntelligenceEngine()
    return engine.answer_question(request)


@router.get("/sample-queries", response_model=List[str])
def get_sample_queries():
    return [
        "What is our stockout risk and days of coverage across warehouses?",
        "How is the PO-9012 Shenzhen delay impacting our GAAP contribution margin?",
        "What actions does the OR-Tools solver recommend to protect EBITDA?",
        "How does cross-zone fulfillment from WH-EAST bleed our margin?",
        "What is the optimal dual-sourcing split between Shenzhen and Saigon?",
    ]
