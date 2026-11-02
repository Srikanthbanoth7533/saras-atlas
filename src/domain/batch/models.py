"""
SARAS ATLAS — Multi-Scenario Batch Engine Pydantic Schemas.
Defines schemas for batch scenario generation, parallel execution, sensitivity sweeping,
ranking, and persistence.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from src.domain.simulation.models import (
    ShocksConfig,
    MitigationsConfig,
    SummaryScorecard,
    ComparisonScorecard,
)


class BatchScenarioItem(BaseModel):
    """A single scenario configuration within a batch."""
    scenario_id: str = Field(..., description="Unique scenario identifier (e.g. SCN-001)")
    scenario_name: str = Field(..., description="Human-readable scenario title")
    description: Optional[str] = Field(default="", description="Detailed scenario rationale")
    shocks: ShocksConfig = Field(default_factory=ShocksConfig)
    mitigations: MitigationsConfig = Field(default_factory=MitigationsConfig)
    weight: float = Field(default=1.0, ge=0.0, description="Probability or business weight")
    tags: List[str] = Field(default_factory=list, description="Categorization tags")


class BatchScenarioResult(BaseModel):
    """Simulation output and comparative ranking for a single scenario."""
    scenario_id: str
    scenario_name: str
    shocks_summary: Dict[str, Any]
    mitigations_summary: Dict[str, Any]
    scorecard: SummaryScorecard
    comparison_vs_baseline: Optional[ComparisonScorecard] = None
    rank: int = Field(default=1, description="Relative ranking based on composite score")
    composite_score: float = Field(default=0.0, description="Normalized multi-criteria score [0..100]")
    execution_ms: float
    status: str = "COMPLETED"


class BatchRunRequest(BaseModel):
    """Request to execute a batch of scenarios."""
    batch_name: str = Field(default="Standard Resilience Stress Test")
    scenarios: List[BatchScenarioItem] = Field(..., min_length=1)
    parallel: bool = Field(default=True, description="Enable thread-pooled execution")
    max_workers: int = Field(default=4, ge=1, le=8, description="Max parallel worker threads")
    persist_results: bool = Field(default=True, description="Persist run to SQLite/DuckDB")
    random_seed: Optional[int] = Field(default=42, description="Deterministic seed for reproducibility")


class BatchRunSummary(BaseModel):
    """Aggregate statistical summary across all executed scenarios in a batch."""
    mean_net_revenue: float
    mean_contribution_margin: float
    min_contribution_margin: float
    max_contribution_margin: float
    mean_fill_rate: float
    min_fill_rate: float
    max_fill_rate: float
    mean_stockout_days: float
    max_stockout_days: int
    mean_working_capital: float


class BatchRunResponse(BaseModel):
    """Complete batch execution evaluation response."""
    batch_id: str
    batch_name: str
    total_scenarios: int
    completed_scenarios: int
    failed_scenarios: int
    total_execution_ms: float
    mean_execution_ms_per_scenario: float
    scenarios_per_second: float
    best_case: BatchScenarioResult
    worst_case: BatchScenarioResult
    baseline: BatchScenarioResult
    summary_stats: BatchRunSummary
    ranked_results: List[BatchScenarioResult]


class SensitivitySweepRequest(BaseModel):
    """Request for single-parameter sensitivity sweep."""
    parameter: str = Field(..., description="Parameter to sweep: 'supplier_delay' | 'freight_surcharge' | 'demand_surge'")
    min_value: float = Field(..., description="Starting value for sweep")
    max_value: float = Field(..., description="Ending value for sweep")
    steps: int = Field(default=10, ge=3, le=50, description="Number of discrete evaluation steps")
    baseline_delay_days: int = Field(default=21)
    baseline_freight_surcharge: float = Field(default=0.28)
    baseline_demand_multiplier: float = Field(default=1.45)
    mitigations: MitigationsConfig = Field(default_factory=MitigationsConfig)


class SensitivityPoint(BaseModel):
    """Individual data point in a sensitivity analysis curve."""
    param_value: float
    param_label: str
    net_revenue: float
    contribution_margin: float
    contribution_margin_pct: float
    fill_rate: float
    stockout_days: int
    working_capital: float


class SensitivitySweepResponse(BaseModel):
    """Response containing parametric sensitivity trajectory."""
    parameter: str
    steps_evaluated: int
    points: List[SensitivityPoint]
    elasticity_score: float = Field(..., description="Relative sensitivity gradient (% CM change / % param change)")
    executive_insight: str

