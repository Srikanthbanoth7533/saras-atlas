"""
SARAS ATLAS — Prescriptive Explainability Routes
"""

from fastapi import APIRouter, Depends, Query
from src.domain.explainability.recommendations import (
    PrescriptiveDossierResponse,
    ExplainableRecommendationBuilder,
)
from src.security.models import User
from src.security.auth import get_current_user

router = APIRouter(prefix="/explainability", tags=["Explainable Recommendations"])


@router.get("/recommendations", response_model=PrescriptiveDossierResponse)
def get_explainable_recommendations(
    scenario_id: str = Query("SCN-CURRENT-DISRUPTION", description="Scenario identifier"),
    user: User = Depends(get_current_user),
):
    return ExplainableRecommendationBuilder.build_standard_dossier(scenario_id=scenario_id)
