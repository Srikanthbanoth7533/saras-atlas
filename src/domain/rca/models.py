"""
SARAS ATLAS — Root Cause Analysis (RCA) Models
Defines causal propagation nodes, financial impact attribution, and sensitivity variable schemas.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class CausalLayer(str, Enum):
    UPSTREAM_SUPPLIER = "UPSTREAM_SUPPLIER"
    LOGISTICS_CORRIDOR = "LOGISTICS_CORRIDOR"
    FULFILLMENT_NODE = "FULFILLMENT_NODE"
    CUSTOMER_DELIVERY = "CUSTOMER_DELIVERY"
    FINANCIAL_EBITDA = "FINANCIAL_EBITDA"


class CausalNode(BaseModel):
    node_id: str
    label: str
    layer: CausalLayer
    metric_label: str
    metric_value: str
    severity: str  # CRITICAL, WARNING, NORMAL
    causal_parent_id: Optional[str] = None
    impact_weight: float = Field(..., ge=0.0, le=1.0)
    description: str


class FinancialAttributionSegment(BaseModel):
    segment_name: str
    dollar_impact: float
    percentage_of_total: float
    accounting_category: str
    evidence_citation: str


class InfluentialVariable(BaseModel):
    variable_name: str
    elasticity_rank: int
    sensitivity_score: float  # |d(CM)/d(Variable)| normalized
    observed_value: str
    baseline_value: str
    unit_of_measure: str
    explanation: str


class RootCauseTraceResponse(BaseModel):
    disruption_id: str
    primary_root_cause: str
    root_cause_narrative: str
    causal_chain: List[CausalNode]
    financial_attribution: List[FinancialAttributionSegment]
    total_financial_impact: float
    top_influential_variables: List[InfluentialVariable]
    evidence_telemetry: List[str]
    generated_at: str

