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
