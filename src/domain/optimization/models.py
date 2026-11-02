"""
SARAS ATLAS — Prescriptive Optimization Models.
Defines schemas for Google OR-Tools MILP decision engine.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class ObjectiveType(str, Enum):
    MAXIMIZE_CONTRIBUTION_MARGIN = "MAXIMIZE_CONTRIBUTION_MARGIN"
    MINIMIZE_WORKING_CAPITAL = "MINIMIZE_WORKING_CAPITAL"
    MAXIMIZE_FILL_RATE = "MAXIMIZE_FILL_RATE"


class SupplierCandidate(BaseModel):
    supplier_id: str
    supplier_name: str
    mode: str = "AIR_EXPEDITED"
    unit_cost_air: float = Field(default=12.50, description="Freight expediting premium per unit")
    lead_time_days: int = Field(default=8, description="Days to arrive at Reno 3PL")
    moq: int = Field(default=500, description="Minimum order quantity")
    max_capacity: int = Field(default=3000, description="Maximum available factory production")


class TransferCandidate(BaseModel):
    origin_warehouse_id: str
    destination_warehouse_id: str
    transfer_cost_per_unit: float = Field(default=3.20, description="Inter-node LTL freight cost")
    transit_days: int = Field(default=4, description="Days in transit between nodes")
    max_transfer_units: int = Field(default=800, description="Max safe transfer without starving origin")


class OptimizationRequest(BaseModel):
    capital_budget_ceiling: float = Field(default=40000.00, description="Max cash outlay for mitigations ($)")
    min_service_fill_rate: float = Field(default=0.90, description="Minimum acceptable fill rate [0..1]")
    max_ad_throttle_pct: float = Field(default=0.35, description="Maximum allowed ad reduction [0..0.35]")
    target_sku: str = Field(default="APEX-JKT", description="Target SKU experiencing disruption")
    objective: ObjectiveType = Field(default=ObjectiveType.MAXIMIZE_CONTRIBUTION_MARGIN)
    supplier_candidate: Optional[SupplierCandidate] = None
    transfer_candidate: Optional[TransferCandidate] = None


class OptimizationResult(BaseModel):
    status: str = Field(..., description="Solver status: OPTIMAL, FEASIBLE, or INFEASIBLE")
    solve_time_ms: int = Field(..., description="Solver execution time in milliseconds")
    recommended_air_freight_units: int = Field(..., description="Units to air-freight from backup factory")
    recommended_transfer_units: int = Field(..., description="Units to transfer between warehouses")
    recommended_ad_throttle_pct: float = Field(..., description="Percentage to throttle ad spend [0..1]")
    capital_required: float = Field(..., description="Total cash required for air + transfer ($)")
    projected_net_contribution_margin: float = Field(..., description="Projected CM ($) over 90-day horizon")
    projected_contribution_margin_pct: float = Field(..., description="Projected CM %")
    projected_stockout_days: int = Field(..., description="Projected stockout days under recommendation")
    projected_fill_rate: float = Field(..., description="Projected customer order fill rate [0..1]")
    objective_value: float = Field(..., description="Value of objective function achieved")
    rationale: str = Field(..., description="Explainable mathematical rationale for recommendation")
