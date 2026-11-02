"""
SARAS ATLAS — Advanced Statistical & ML Forecasting Models
Defines contracts for train/test split evaluation, prediction intervals, model comparisons, and drift detection.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ForecastSeriesType(str, Enum):
    DAILY_DEMAND = "DAILY_DEMAND"
    LEAD_TIME_DAYS = "LEAD_TIME_DAYS"


class ModelEvaluationScore(BaseModel):
    model_config = {"protected_namespaces": ()}
    model_name: str
    mae: float
    rmse: float
    mape: float  # Percentage e.g. 8.4%
    wape: float  # Weighted absolute percentage error
    test_samples_count: int
    is_best_model: bool = False
    fit_duration_ms: float


class DriftAnalysis(BaseModel):
    drift_detected: bool
    drift_severity: str  # NONE, MILD_VOLATILITY, STRUCTURAL_REGIME_SHIFT
    z_score_shift: float
    ks_statistic: float
    p_value: float
    message: str
    recommended_retraining_cadence: str


class ForecastDataPoint(BaseModel):
    period: int
    date: str
    actual: Optional[float] = None
    predicted: float
    lower_80: float
    upper_80: float
    lower_95: float
    upper_95: float
    is_forecast_horizon: bool = False


class ForecastingEvaluationResponse(BaseModel):
    series_type: ForecastSeriesType
    target_entity: str  # e.g. "Vanguard Apparel Omnichannel Demand" or "Shenzhen Port Lead Time"
    train_periods: int
    test_periods: int
    forecast_horizon: int
    models_evaluated: List[ModelEvaluationScore]
    best_model_name: str
    forecast_trajectory: List[ForecastDataPoint]
    drift_analysis: DriftAnalysis
    validation_methodology: str
    generated_at: str
