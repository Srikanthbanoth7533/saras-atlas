"""
SARAS ATLAS — Pydantic Schemas for Simulation Requests & Responses.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class SupplierDelayShock(BaseModel):
    """Shock: Inbound purchase order arrival delay."""
    po_number: str = Field(..., description="Purchase order identifier (e.g. PO-9012)")
    delay_days: int = Field(..., ge=-30, le=90, description="Additional days delayed at port/transit")


class FreightSurchargeShock(BaseModel):
    """Shock: Outbound parcel carrier freight surcharge."""
    lane_id: str = Field(..., description="Carrier lane (e.g. lane_east_coast_parcel)")
    surcharge_percentage: float = Field(..., ge=-0.50, le=3.00, description="Percentage carrier rate increase (e.g. 0.28 for +28%)")


class DemandSurgeShock(BaseModel):
    """Shock: Downstream customer demand multiplier."""
    sku_code: str = Field(..., description="Target SKU or prefix (e.g. APEX-JKT)")
    demand_multiplier: float = Field(..., ge=0.10, le=5.00, description="Demand expansion factor (e.g. 1.45 for +45%)")
    duration_days: int = Field(default=30, ge=1, le=90, description="Duration of promotional surge in days")


class ShocksConfig(BaseModel):
    """Collection of exogenous disruption shocks."""
    supplier_delays: List[SupplierDelayShock] = Field(default_factory=list)
    freight_surcharges: List[FreightSurchargeShock] = Field(default_factory=list)
    demand_elasticities: List[DemandSurgeShock] = Field(default_factory=list)


class MitigationsConfig(BaseModel):
    """Collection of candidate operational mitigation decisions."""
    emergency_air_freight_units: int = Field(default=0, ge=0, description="Units ordered via expedited air freight from Vietnam backup")
    inter_warehouse_transfer_units: int = Field(default=0, ge=0, description="Units transferred ground East-to-West")
    ad_spend_throttle_percentage: float = Field(default=0.0, ge=0.0, le=0.50, description="Percentage marketing ad throttle (0.0 to 0.50)")


class SimulationRequest(BaseModel):
    """Inbound request to run a counterfactual multi-echelon simulation."""
    scenario_name: str = Field(..., description="Human-readable scenario name")
    horizon_days: int = Field(default=90, ge=14, le=180, description="Forward planning horizon in days")
    shocks: ShocksConfig = Field(default_factory=ShocksConfig)
    mitigations: MitigationsConfig = Field(default_factory=MitigationsConfig)


class SummaryScorecard(BaseModel):
    """Executive financial and operational metrics summary."""
    gross_revenue: float
    net_revenue: float
    cogs_total: float
    freight_total: float
    allocated_ad_spend: float
    net_contribution_margin: float
    contribution_margin_pct: float
    total_orders_fulfilled: int
    unfulfilled_lost_orders: int
    stockout_days: int
    working_capital_required: float


class ComparisonScorecard(BaseModel):
    """Variance deltas compared to baseline."""
    delta_revenue: float
    delta_contribution_margin: float
    margin_percentage_shift: float
    avoided_cross_zone_freight_penalty: float
    stockout_days_avoided: int


class SimulationResponse(BaseModel):
    """Complete simulation evaluation response."""
    scenario_name: str
    execution_duration_ms: int
    horizon_days: int
    summary_scorecard: SummaryScorecard
    comparison_vs_baseline: Optional[ComparisonScorecard] = None
    executive_narrative: str
    daily_timeseries: Optional[Dict[str, List[float]]] = None
