"""
SARAS ATLAS — AI Decision Intelligence Models
Defines query contracts, fact citations, intent classification, and structured response schemas.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class QueryTopic(str, Enum):
    INVENTORY = "INVENTORY"
    DISRUPTIONS = "DISRUPTIONS"
    WAREHOUSES = "WAREHOUSES"
    SUPPLIERS = "SUPPLIERS"
    DEMAND = "DEMAND"
    MARGINS = "MARGINS"
    EXPOSURE = "EXPOSURE"
    SIMULATION = "SIMULATION"
    OPTIMIZATION = "OPTIMIZATION"
    GENERAL = "GENERAL"


class GroundedCitation(BaseModel):
    source_entity: str = Field(..., description="Entity name e.g. InventorySnapshot, OperationalRiskSentinel")
    record_key: str = Field(..., description="Key identifier e.g. SKU-001@WH-WEST, PO-9012")
    metric_name: str = Field(..., description="Specific metric name e.g. days_of_coverage, unit_contribution_margin")
    verified_value: str = Field(..., description="Verified value as string or formatted currency")
    audit_timestamp: str = Field(..., description="Timestamp when metric was retrieved")


class QuestionRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500, description="Natural language question from business leader")
    entity_focus: Optional[str] = Field(None, description="Optional entity focus (e.g. WH-WEST, SKU-001)")


class IntelligenceResponse(BaseModel):
    query: str
    intent_topic: QueryTopic
    confidence_score: float
    answer_markdown: str
    grounded_metrics: Dict[str, Any]
    citations: List[GroundedCitation]
    suggested_actions: List[str]
    data_freshness: str = "VERIFIED_LIVE_TWIN_DATA"
