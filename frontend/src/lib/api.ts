/**
 * SARAS ATLAS — API Client.
 * Connects Next.js directly to the FastAPI REST backend.
 */

import {
  SystemHealth,
  DigitalTwinTopology,
  InventorySummaryResponse,
  ActiveRisksResponse,
  SimulationRequest,
  SimulationResponse,
  ScenarioComparisonResponse,
  OptimizationRequest,
  OptimizationResult,
  ApprovalRequest,
  ApprovalResponse,
  AuditTrailResponse,
  BatchScenarioItem,
  BatchRunResponse,
  SensitivitySweepResponse,
  PolicyDefinition,
  PolicyOptimizationResponse,
  SupplierSourcingResponse,
  IngestionEntity,
  IngestionPreviewResponse,
  IngestionCommitResponse,
  RollbackResponse,
  DataQualityReport,
} from "./types";

const API_BASE = "http://127.0.0.1:8000/api/v1";

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      ...(options?.headers || {}),
    },
  });

  if (!res.ok) {
    const errorBody = await res.text();
    let detail = res.statusText;
    try {
      const parsed = JSON.parse(errorBody);
      detail = parsed.detail || detail;
    } catch {
      detail = errorBody || detail;
    }
    throw new Error(`API Error [${res.status}]: ${detail}`);
  }

  return res.json() as Promise<T>;
}

export async function getSystemHealth(): Promise<SystemHealth> {
  return fetchJson<SystemHealth>(`${API_BASE}/health`);
}

export async function getDigitalTwinTopology(): Promise<DigitalTwinTopology> {
  return fetchJson<DigitalTwinTopology>(`${API_BASE}/twin/topology`);
}

export async function getInventorySummary(): Promise<InventorySummaryResponse> {
  return fetchJson<InventorySummaryResponse>(`${API_BASE}/twin/inventory-summary`);
}

export async function getActiveRisks(): Promise<ActiveRisksResponse> {
  return fetchJson<ActiveRisksResponse>(`${API_BASE}/risks/active`);
}

export async function runSimulation(req: SimulationRequest): Promise<SimulationResponse> {
  return fetchJson<SimulationResponse>(`${API_BASE}/scenarios/simulate`, {
    method: "POST",
    body: JSON.stringify(req),
  });
}

export async function compareScenarios(
  baselineRequest: SimulationRequest,
  mitigatedRequest: SimulationRequest
): Promise<ScenarioComparisonResponse> {
  return fetchJson<ScenarioComparisonResponse>(`${API_BASE}/scenarios/compare`, {
    method: "POST",
    body: JSON.stringify({
      baseline_request: baselineRequest,
      mitigated_request: mitigatedRequest,
    }),
  });
}

export async function solveOptimization(req: OptimizationRequest): Promise<OptimizationResult> {
  return fetchJson<OptimizationResult>(`${API_BASE}/optimization/solve`, {
    method: "POST",
    body: JSON.stringify(req),
  });
}

export async function submitApproval(req: ApprovalRequest): Promise<ApprovalResponse> {
  return fetchJson<ApprovalResponse>(`${API_BASE}/governance/approve`, {
    method: "POST",
    body: JSON.stringify(req),
  });
}

export async function getAuditTrail(): Promise<AuditTrailResponse> {
  return fetchJson<AuditTrailResponse>(`${API_BASE}/governance/audit-trail`);
}

// ---------------------------------------------------------------------------
// Phase 3 Endpoints: Batch, Policy, & Ingestion
// ---------------------------------------------------------------------------

export async function fetchBenchmarkScenarios(count: number = 10): Promise<BatchScenarioItem[]> {
  return fetchJson<BatchScenarioItem[]>(`${API_BASE}/batch/generate-benchmark?count=${count}`);
}

export async function runBatchSimulation(
  scenarios: BatchScenarioItem[],
  batchName: string = "Standard Stress Test",
  parallel: boolean = true
): Promise<BatchRunResponse> {
  return fetchJson<BatchRunResponse>(`${API_BASE}/batch/run`, {
    method: "POST",
    body: JSON.stringify({
      batch_name: batchName,
      scenarios,
      parallel,
      max_workers: 4,
      persist_results: true,
      random_seed: 42,
    }),
  });
}

export async function runSensitivitySweep(
  parameter: "supplier_delay" | "freight_surcharge" | "demand_surge",
  minValue: number,
  maxValue: number,
  steps: number = 10
): Promise<SensitivitySweepResponse> {
  return fetchJson<SensitivitySweepResponse>(`${API_BASE}/batch/sensitivity`, {
    method: "POST",
    body: JSON.stringify({
      parameter,
      min_value: minValue,
      max_value: maxValue,
      steps,
    }),
  });
}

export async function fetchStandardPolicies(): Promise<PolicyDefinition[]> {
  return fetchJson<PolicyDefinition[]>(`${API_BASE}/policy/standard-suite`);
}

export async function evaluateMitigationPolicies(
  policies?: PolicyDefinition[],
  draws: number = 25
): Promise<PolicyOptimizationResponse> {
  return fetchJson<PolicyOptimizationResponse>(`${API_BASE}/policy/evaluate`, {
    method: "POST",
    body: JSON.stringify({
      policies,
      num_stochastic_draws: draws,
      random_seed: 42,
    }),
  });
}

export async function optimizeSupplierSourcing(params?: {
  annualDemand?: number;
  shenzhenDisruptionProb?: number;
  saigonDisruptionProb?: number;
}): Promise<SupplierSourcingResponse> {
  return fetchJson<SupplierSourcingResponse>(`${API_BASE}/policy/sourcing`, {
    method: "POST",
    body: JSON.stringify({
      annual_demand_units: params?.annualDemand ?? 150000,
      shenzhen_disruption_probability: params?.shenzhenDisruptionProb ?? 0.25,
      saigon_disruption_probability: params?.saigonDisruptionProb ?? 0.08,
    }),
  });
}

export async function previewUploadFile(
  file: File,
  targetEntity: IngestionEntity
): Promise<IngestionPreviewResponse> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("target_entity", targetEntity);

  const res = await fetch(`${API_BASE}/ingestion/preview`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`Upload preview failed: ${errText}`);
  }
  return res.json();
}

export async function commitIngestionDataset(
  fileId: string,
  targetEntity: IngestionEntity,
  columnMapping: Record<string, string>,
  deduplicationStrategy: string = "REPLACE_EXISTING",
  imputeMissing: boolean = true
): Promise<IngestionCommitResponse> {
  return fetchJson<IngestionCommitResponse>(`${API_BASE}/ingestion/commit`, {
    method: "POST",
    body: JSON.stringify({
      file_id: fileId,
      target_entity: targetEntity,
      column_mapping: columnMapping,
      deduplication_strategy: deduplicationStrategy,
      impute_missing: imputeMissing,
    }),
  });
}

export async function rollbackIngestion(rollbackToken: string): Promise<RollbackResponse> {
  return fetchJson<RollbackResponse>(`${API_BASE}/ingestion/rollback`, {
    method: "POST",
    body: JSON.stringify({
      rollback_token: rollbackToken,
    }),
  });
}

export async function fetchDataQualityReport(): Promise<DataQualityReport> {
  return fetchJson<DataQualityReport>(`${API_BASE}/ingestion/quality`);
}

