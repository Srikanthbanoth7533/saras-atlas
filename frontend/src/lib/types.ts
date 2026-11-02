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
  category: "SUPPLY_CHAIN_INBOUND" | "LOGISTICS_SURCHARGE" | "INVENTORY_STOCKOUT" | string;
  severity: "CRITICAL" | "WARNING" | "INFO";
  title: string;
  description: string;
  financial_exposure_estimate: number;
  impacted_entities: string[];
  recommended_action: string;
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
