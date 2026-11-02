"""
SARAS ATLAS — Dynamic Policy Optimization Pydantic Schemas.
Defines schemas for multi-policy evaluation, robustness risk distributions,
Pareto cost/service-level frontiers, and multi-supplier sourcing allocation.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class PolicyDefinition(BaseModel):
    """Operational mitigation policy specification."""
    policy_id: str = Field(..., description="Unique policy identifier (e.g. POL-HYBRID-OR)")
    name: str = Field(..., description="Human-readable policy name")
    description: str = Field(default="", description="Operating strategy summary")
    air_freight_units: int = Field(default=0, ge=0)
    transfer_units: int = Field(default=0, ge=0)
    ad_throttle_pct: float = Field(default=0.0, ge=0.0, le=0.50)
    supplier_allocation: Dict[str, float] = Field(
        default_factory=lambda: {"Shenzhen Primary": 1.0, "Saigon Secondary": 0.0}
    )
    mitigation_budget: float = Field(default=0.0, ge=0.0)


class PolicyEvaluationMetric(BaseModel):
    """Statistical outcome and risk metrics for an evaluated policy."""
    policy_id: str
    name: str
    description: str
    mean_cm: float = Field(..., description="Expected 90-day Net Contribution Margin ($)")
    p10_cm: float = Field(..., description="10th percentile worst-case Net CM ($)")
    p90_cm: float = Field(..., description="90th percentile upside Net CM ($)")
    cm_std_dev: float = Field(..., description="Standard deviation of CM across stochastic draws ($)")
    mean_fill_rate: float = Field(..., description="Expected customer order fill rate [0..1]")
    mean_stockout_days: float = Field(..., description="Expected days in stockout condition")
    mitigation_cost: float = Field(..., description="Direct operational cost of executing policy ($)")
    cvar_90: float = Field(..., description="Conditional Value-at-Risk below 10th percentile ($)")
    robustness_score: float = Field(..., description="Tail-risk resilience index [0..100]")
    composite_score: float = Field(..., description="Weighted multi-criteria score [0..100]")
    rank: int = Field(..., description="Ordinal policy ranking (1 = optimal)")
    is_pareto_efficient: bool = Field(default=False)
    explainable_rationale: str = Field(..., description="Transparent mathematical justification")


class ParetoPoint(BaseModel):
    """Point on the Cost vs Service-Level Pareto Trade-Off Frontier."""
    policy_id: str
    policy_name: str
    mitigation_cost: float
    service_level: float = Field(..., description="Fill rate percentage [0..100]")
    net_cm: float
    is_pareto_optimal: bool


class PolicyOptimizationRequest(BaseModel):
    """Request to evaluate and rank candidate mitigation policies."""
    policies: Optional[List[PolicyDefinition]] = None
    num_stochastic_draws: int = Field(default=25, ge=10, le=100)
    random_seed: int = Field(default=42)
    budget_ceiling: float = Field(default=40000.00)
    service_level_floor: float = Field(default=0.90)


class PolicyOptimizationResponse(BaseModel):
    """Complete dynamic policy evaluation response."""
    evaluated_policies: List[PolicyEvaluationMetric]
    pareto_frontier: List[ParetoPoint]
    recommended_policy_id: str
    recommended_policy_name: str
    stochastic_draws: int
    executive_verdict: str


class SupplierSourcingRequest(BaseModel):
    """Request for multi-supplier portfolio allocation optimization."""
    annual_demand_units: int = Field(default=150000, description="Annual production volume")
    holding_cost_annual_rate: float = Field(default=0.20, description="Inventory carrying cost rate [0..1]")
    stockout_penalty_per_unit: float = Field(default=75.00, description="Margin loss per unfulfilled unit ($)")
    # Primary Supplier (Shenzhen)
    shenzhen_unit_cogs: float = Field(default=45.15)
    shenzhen_lead_time_days: int = Field(default=35)
    shenzhen_disruption_probability: float = Field(default=0.25, ge=0.0, le=1.0)
    # Secondary Supplier (Saigon)
    saigon_unit_cogs: float = Field(default=49.50)
    saigon_lead_time_days: int = Field(default=18)
    saigon_disruption_probability: float = Field(default=0.08, ge=0.0, le=1.0)


class SupplierSourcingResponse(BaseModel):
    """Optimal risk-hedged supplier allocation decision."""
    optimal_shenzhen_share: float = Field(..., description="Optimal allocation percentage to Shenzhen [0..1]")
    optimal_saigon_share: float = Field(..., description="Optimal allocation percentage to Saigon [0..1]")
    expected_landed_cogs: float = Field(..., description="Expected blended procurement cost ($)")
    expected_risk_hedged_stockout_cost: float = Field(..., description="Expected stockout cost under dual sourcing ($)")
    single_source_stockout_cost: float = Field(..., description="Expected stockout cost if 100% Shenzhen ($)")
    net_portfolio_savings: float = Field(..., description="Net financial benefit of dual sourcing ($)")
    optimal_service_level: float = Field(..., description="Projected service level under optimal allocation")
    explainability: str = Field(..., description="Optimization rationale and sensitivity notes")

