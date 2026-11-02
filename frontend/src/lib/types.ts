/**
 * SARAS ATLAS — TypeScript Data Types & Interfaces.
 * Strictly mirrors FastAPI backend schemas and models.
 */

export interface SystemHealth {
  status: string;
  service: string;
  version: string;
  database: string;
  optimizer: string;
  memory: {
    system_total_phys_gb: number;
    system_avail_phys_gb: number;
    process_working_set_mb: number;
  };
  architecture: string;
}

export interface TopologyNode {
  id: string;
  type: "SUPPLIER" | "WAREHOUSE" | "RETAIL_CHANNEL" | string;
  name: string;
  code: string;
  lat: number;
  lng: number;
  status: "NORMAL" | "WARNING" | "CRITICAL_STOCKOUT_RISK" | string;
}

export interface TopologyEdge {
  from_node: string;
  to_node: string;
  key: string;
  mode: "OCEAN" | "AIR" | "GROUND_LTL" | "PARCEL" | string;
  delay_days: number;
  status: string;
}

export interface DigitalTwinTopology {
  organization: {
    id: string;
    name: string;
    slug: string;
  };
  organization_id: string;
  total_nodes: number;
  total_edges: number;
  nodes: TopologyNode[];
  edges: TopologyEdge[];
}

export interface SkuInventoryItem {
  sku_id: string;
  sku_code: string;
  product_name: string;
  retail_price: number;
  total_on_hand: number;
  total_reserved: number;
  total_available: number;
  total_in_transit: number;
  min_days_of_coverage: number;
  status: "HEALTHY" | "AT_RISK" | "CRITICAL_STOCKOUT";
}

export interface InventorySummaryResponse {
  total_skus: number;
  total_on_hand_units: number;
  total_available_units: number;
  total_in_transit_units: number;
  items: SkuInventoryItem[];
}

export interface ActiveRisk {
  risk_id: string;
  category?: "SUPPLY_CHAIN_INBOUND" | "LOGISTICS_SURCHARGE" | "INVENTORY_STOCKOUT" | string;
  risk_type?: string;
  severity: "CRITICAL" | "HIGH" | "WARNING" | "INFO" | string;
  title: string;
  description?: string;
  summary?: string;
  financial_exposure_estimate?: number;
  estimated_revenue_exposure?: number;
  estimated_monthly_freight_inflation?: number;
  cost_delta_per_unit?: number;
  margin_erosion_pts?: number;
  impacted_entities?: string[];
  entity_id?: string;
  destination_warehouse?: string;
  affected_warehouse?: string;
  delay_days?: number;
  affected_units?: number;
  affected_cogs_value?: number;
  vulnerable_skus?: Array<{
    sku_code?: string;
    available_stock?: number;
    days_of_coverage?: number;
    projected_stockout_day?: number;
    unmet_gap_days?: number;
  }>;
  recommended_action?: string;
}

export interface ActiveRisksResponse {
  status: string;
  total_active_risks: number;
  critical_count: number;
  warning_count: number;
  risks: ActiveRisk[];
}

export interface SupplierDelayShock {
  po_number: string;
  delay_days: number;
}

export interface FreightSurchargeShock {
  lane_id: string;
  surcharge_percentage: number;
}

export interface DemandSurgeShock {
  sku_code: string;
  demand_multiplier: number;
  duration_days: number;
}

export interface ShocksConfig {
  supplier_delays?: SupplierDelayShock[];
  freight_surcharges?: FreightSurchargeShock[];
  demand_elasticities?: DemandSurgeShock[];
}

export interface MitigationsConfig {
  emergency_air_freight_units?: number;
  inter_warehouse_transfer_units?: number;
  ad_spend_throttle_percentage?: number;
}

export interface SimulationRequest {
  scenario_name: string;
  horizon_days: number;
  shocks: ShocksConfig;
  mitigations: MitigationsConfig;
}

export interface SummaryScorecard {
  gross_revenue: number;
  net_revenue: number;
  cogs_total: number;
  freight_total: number;
  allocated_ad_spend: number;
  net_contribution_margin: number;
  contribution_margin_pct: number;
  total_orders_fulfilled: number;
  unfulfilled_lost_orders: number;
  stockout_days: number;
  working_capital_required: number;
}

export interface ComparisonScorecard {
  delta_revenue: number;
  delta_contribution_margin: number;
  margin_percentage_shift: number;
  avoided_cross_zone_freight_penalty: number;
  stockout_days_avoided: number;
}

export interface DailyTimeseries {
  revenue: number[];
  contribution_margin: number[];
  cash_balance: number[];
}

export interface SimulationResponse {
  scenario_name: string;
  execution_duration_ms: number;
  horizon_days: number;
  summary_scorecard: SummaryScorecard;
  comparison_vs_baseline: ComparisonScorecard;
  executive_narrative: string;
  daily_timeseries: DailyTimeseries;
}

export interface ScenarioComparisonResponse {
  baseline_result: SimulationResponse;
  mitigated_result: SimulationResponse;
  net_margin_delta: number;
  revenue_saved: number;
  stockout_days_saved: number;
  executive_verdict: string;
}

export interface OptimizationRequest {
  capital_budget_ceiling: number;
  min_service_fill_rate: number;
  max_ad_throttle_pct: number;
  target_sku: string;
  objective: "MAXIMIZE_CONTRIBUTION_MARGIN" | "MINIMIZE_WORKING_CAPITAL" | "MAXIMIZE_FILL_RATE";
}

export interface OptimizationResult {
  status: string;
  solve_time_ms: number;
  recommended_air_freight_units: number;
  recommended_transfer_units: number;
  recommended_ad_throttle_pct: number;
  capital_required: number;
  projected_net_contribution_margin: number;
  projected_contribution_margin_pct: number;
  projected_stockout_days: number;
  projected_fill_rate: number;
  objective_value: number;
  rationale: string;
}

export interface ApprovalRequest {
  recommendation_id?: string;
  approver_primary_id: string;
  approver_primary_name: string;
  approver_secondary_id: string;
  approver_secondary_name: string;
  decision: "APPROVED" | "REJECTED" | "MODIFIED";
  notes?: string;
  approved_capital_outlay: number;
}

export interface ApprovalResponse {
  id: string;
  decision: string;
  approved_capital_outlay: number;
  approver_primary: string;
  approver_secondary: string;
  digital_signature_sha256: string;
  created_at: string;
  status: string;
  two_man_rule_satisfied: boolean;
}

export interface AuditTrailItem {
  id: string;
  approver: string;
  role: string;
  decision: string;
  comments: string;
  digital_signature_hash: string;
  created_at: string;
}

export interface AuditTrailResponse {
  total_simulations_recorded: number;
  total_approvals_recorded: number;
  recent_approvals: AuditTrailItem[];
  recent_simulations: any[];
}

// ---------------------------------------------------------------------------
// Phase 3: Batch Scenario Engine, Dynamic Policy, & Enterprise Ingestion
// ---------------------------------------------------------------------------

export interface BatchScenarioItem {
  scenario_id: string;
  scenario_name: string;
  description?: string;
  shocks: ShocksConfig;
  mitigations: MitigationsConfig;
  weight: number;
  tags: string[];
}

export interface BatchScenarioResult {
  scenario_id: string;
  scenario_name: string;
  shocks_summary: Record<string, any>;
  mitigations_summary: Record<string, any>;
  scorecard: SummaryScorecard;
  comparison_vs_baseline?: ComparisonScorecard;
  rank: number;
  composite_score: number;
  execution_ms: number;
  status: string;
}

export interface BatchRunSummary {
  mean_net_revenue: number;
  mean_contribution_margin: number;
  min_contribution_margin: number;
  max_contribution_margin: number;
  mean_fill_rate: number;
  min_fill_rate: number;
  max_fill_rate: number;
  mean_stockout_days: number;
  max_stockout_days: number;
  mean_working_capital: number;
}

export interface BatchRunResponse {
  batch_id: string;
  batch_name: string;
  total_scenarios: number;
  completed_scenarios: number;
  failed_scenarios: number;
  total_execution_ms: number;
  mean_execution_ms_per_scenario: number;
  scenarios_per_second: number;
  best_case: BatchScenarioResult;
  worst_case: BatchScenarioResult;
  baseline: BatchScenarioResult;
  summary_stats: BatchRunSummary;
  ranked_results: BatchScenarioResult[];
}

export interface SensitivityPoint {
  param_value: number;
  param_label: string;
  net_revenue: number;
  contribution_margin: number;
  contribution_margin_pct: number;
  fill_rate: number;
  stockout_days: number;
  working_capital: number;
}

export interface SensitivitySweepResponse {
  parameter: string;
  steps_evaluated: number;
  points: SensitivityPoint[];
  elasticity_score: number;
  executive_insight: string;
}

export interface PolicyDefinition {
  policy_id: string;
  name: string;
  description: string;
  air_freight_units: number;
  transfer_units: number;
  ad_throttle_pct: number;
  supplier_allocation: Record<string, number>;
  mitigation_budget: number;
}

export interface PolicyEvaluationMetric {
  policy_id: string;
  name: string;
  description: string;
  mean_cm: number;
  p10_cm: number;
  p90_cm: number;
  cm_std_dev: number;
  mean_fill_rate: number;
  mean_stockout_days: number;
  mitigation_cost: number;
  cvar_90: number;
  robustness_score: number;
  composite_score: number;
  rank: number;
  is_pareto_efficient: boolean;
  explainable_rationale: string;
}

export interface ParetoPoint {
  policy_id: string;
  policy_name: string;
  mitigation_cost: number;
  service_level: number;
  net_cm: number;
  is_pareto_optimal: boolean;
}

export interface PolicyOptimizationResponse {
  evaluated_policies: PolicyEvaluationMetric[];
  pareto_frontier: ParetoPoint[];
  recommended_policy_id: string;
  recommended_policy_name: string;
  stochastic_draws: number;
  executive_verdict: string;
}

export interface SupplierSourcingResponse {
  optimal_shenzhen_share: number;
  optimal_saigon_share: number;
  expected_landed_cogs: number;
  expected_risk_hedged_stockout_cost: number;
  single_source_stockout_cost: number;
  net_portfolio_savings: number;
  optimal_service_level: number;
  explainability: string;
}

export type IngestionEntity = "INVENTORY_SNAPSHOT" | "PURCHASE_ORDER" | "SKU_CATALOG" | "SALES_ORDER";

export interface CanonicalSchemaField {
  field_name: string;
  data_type: string;
  required: boolean;
  description: string;
  aliases: string[];
}

export interface ValidationIssue {
  row_index: number;
  column: string;
  severity: "ERROR" | "WARNING" | "INFO";
  message: string;
  value?: any;
}

export interface IngestionPreviewResponse {
  file_id: string;
  filename: string;
  file_format: string;
  file_size_bytes: number;
  target_entity: IngestionEntity;
  total_rows: number;
  preview_rows: Record<string, any>[];
  detected_columns: string[];
  suggested_mapping: Record<string, string>;
  canonical_fields: CanonicalSchemaField[];
  total_errors: number;
  total_warnings: number;
  issues_sample: ValidationIssue[];
  missing_value_summary: Record<string, number>;
  duplicate_rows_count: number;
  can_commit: boolean;
}

export interface IngestionCommitResponse {
  rollback_token: string;
  status: string;
  target_entity: IngestionEntity;
  rows_processed: number;
  rows_inserted: number;
  rows_updated: number;
  rows_rejected: number;
  execution_duration_ms: number;
  sha256_checksum: string;
  timestamp: string;
  lineage_record_id: string;
  message: string;
}

export interface RollbackResponse {
  rollback_token: string;
  status: string;
  restored_entity: string;
  message: string;
  timestamp: string;
}

export interface DatasetHealthMetric {
  entity_name: string;
  total_records: number;
  completeness_pct: number;
  validity_pct: number;
  uniqueness_pct: number;
  timeliness_score: number;
  health_grade: string;
}

export interface DataQualityReport {
  overall_health_score: number;
  overall_grade: string;
  evaluated_records: number;
  metrics_by_dataset: DatasetHealthMetric[];
  system_recommendations: string[];
  last_audit_timestamp: string;
}

// =========================================================================
// PHASE 4: ENTERPRISE INTELLIGENCE, RCA, FORECASTING & CONNECTORS
// =========================================================================

export interface GroundedCitation {
  source_entity: string;
  record_key: string;
  metric_name: string;
  verified_value: string;
  audit_timestamp: string;
}

export interface IntelligenceResponse {
  query: string;
  intent_topic: string;
  confidence_score: number;
  answer_markdown: string;
  grounded_metrics: Record<string, any>;
  citations: GroundedCitation[];
  suggested_actions: string[];
  data_freshness: string;
}

export interface CausalNode {
  node_id: string;
  label: string;
  layer: "UPSTREAM_SUPPLIER" | "LOGISTICS_CORRIDOR" | "FULFILLMENT_NODE" | "CUSTOMER_DELIVERY" | "FINANCIAL_EBITDA";
  metric_label: string;
  metric_value: string;
  severity: "CRITICAL" | "WARNING" | "NORMAL";
  causal_parent_id?: string;
  impact_weight: number;
  description: string;
}

export interface FinancialAttributionSegment {
  segment_name: string;
  dollar_impact: number;
  percentage_of_total: number;
  accounting_category: string;
  evidence_citation: string;
}

export interface InfluentialVariable {
  variable_name: string;
  elasticity_rank: number;
  sensitivity_score: number;
  observed_value: string;
  baseline_value: string;
  unit_of_measure: string;
  explanation: string;
}

export interface RootCauseTraceResponse {
  disruption_id: string;
  primary_root_cause: string;
  root_cause_narrative: string;
  causal_chain: CausalNode[];
  financial_attribution: FinancialAttributionSegment[];
  total_financial_impact: number;
  top_influential_variables: InfluentialVariable[];
  evidence_telemetry: string[];
  generated_at: string;
}

export interface ExplainableRecommendationItem {
  recommendation_id: string;
  action_type: string;
  title: string;
  what_action: string;
  why_recommended: string;
  expected_financial_benefits: string;
  benefit_dollar_amount: number;
  required_capital: string;
  capital_dollar_amount: number;
  operational_tradeoffs: string;
  risks_and_assumptions: string;
  alternative_actions: string[];
  consequences_of_no_action: string;
  governance_requirement: string;
  priority_rank: number;
}

export interface PrescriptiveDossierResponse {
  scenario_id: string;
  solver_status: string;
  total_required_capital: number;
  total_expected_financial_benefit: number;
  net_roi_multiple: number;
  recommendations: ExplainableRecommendationItem[];
  governance_mandate: string;
  generated_at: string;
}

export interface ModelEvaluationScore {
  model_name: string;
  mae: number;
  rmse: number;
  mape: number;
  wape: number;
  test_samples_count: number;
  is_best_model: boolean;
  fit_duration_ms: number;
}

export interface DriftAnalysis {
  drift_detected: boolean;
  drift_severity: "NONE" | "MILD_VOLATILITY" | "STRUCTURAL_REGIME_SHIFT";
  z_score_shift: number;
  ks_statistic: number;
  p_value: number;
  message: string;
  recommended_retraining_cadence: string;
}

export interface ForecastDataPoint {
  period: number;
  date: string;
  actual?: number | null;
  predicted: number;
  lower_80: number;
  upper_80: number;
  lower_95: number;
  upper_95: number;
  is_forecast_horizon: boolean;
}

export interface ForecastingEvaluationResponse {
  series_type: "DAILY_DEMAND" | "LEAD_TIME_DAYS";
  target_entity: string;
  train_periods: number;
  test_periods: number;
  forecast_horizon: number;
  models_evaluated: ModelEvaluationScore[];
  best_model_name: string;
  forecast_trajectory: ForecastDataPoint[];
  drift_analysis: DriftAnalysis;
  validation_methodology: string;
  generated_at: string;
}

export interface ConnectorConfig {
  connector_id: string;
  name: string;
  connector_type: "BIGQUERY" | "SNOWFLAKE" | "AMAZON_REDSHIFT" | "REST_WEBHOOK" | "CSV_EXCEL";
  is_enabled: boolean;
  host?: string;
  database?: string;
  warehouse_or_dataset?: string;
  auth_mode: string;
  is_sandbox_mode: boolean;
  description: string;
}

export interface ConnectionTestResult {
  connector_id: string;
  connector_type: string;
  success: boolean;
  latency_ms: number;
  status: string;
  message: string;
  discovered_tables_count: number;
  discovered_tables: string[];
  sample_rows_previewed: number;
  security_posture: string;
}

export interface SchemaDiscoveryResponse {
  connector_id: string;
  connector_type: string;
  dialect: string;
  database: string;
  schema_name: string;
  tables: Record<string, Array<{ column: string; type: string }>>;
  recommended_sync_mode: string;
  generated_at: string;
}

export interface AuditLogEntry {
  timestamp: string;
  event_id: string;
  user_id: string;
  username: string;
  role: string;
  action: string;
  resource: string;
  status: string;
  client_ip?: string;
  details?: Record<string, any>;
}

export interface ExecutiveReportData {
  title: string;
  subtitle: string;
  enterprise: string;
  generated_at: string;
  executive_summary: string;
  kpi_posture: string[][];
  active_disruptions: Array<{
    id: string;
    title: string;
    severity: string;
    node: string;
    exposure: string;
  }>;
  root_cause_analysis: {
    primary_cause: string;
    narrative: string;
    attributions: string[][];
  };
  recommendations: Array<{
    rank: number;
    title: string;
    action: string;
    financial_benefit: string;
    capital: string;
    tradeoffs: string;
    consequences_inaction: string;
  }>;
  assumptions_and_limitations: string[];
  governance: {
    mandate: string;
    approver_1: string;
    approver_2: string;
    digital_seal: string;
  };
}

