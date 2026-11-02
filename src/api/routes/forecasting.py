"""
SARAS ATLAS — Advanced Forecasting Routes
"""

from fastapi import APIRouter, Depends, Query
from src.domain.forecasting.models import (
    ForecastSeriesType,
    ForecastingEvaluationResponse,
)
from src.domain.forecasting.engine import AdvancedForecaster
from src.security.models import User
from src.security.auth import get_current_user

router = APIRouter(prefix="/forecasting", tags=["Advanced Forecasting"])


@router.get("/evaluate", response_model=ForecastingEvaluationResponse)
def evaluate_forecasting(
    series_type: ForecastSeriesType = Query(ForecastSeriesType.DAILY_DEMAND, description="Target time-series"),
    horizon_days: int = Query(30, ge=7, le=60, description="Future forecast horizon"),
    user: User = Depends(get_current_user),
):
    forecaster = AdvancedForecaster()
    return forecaster.evaluate_forecast(series_type=series_type, horizon_days=horizon_days)
