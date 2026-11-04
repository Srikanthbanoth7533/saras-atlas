# SARAS ATLAS — API Architecture Specification

## 1. Overview
The SARAS ATLAS REST API is built on FastAPI and Pydantic v2, exposing high-performance, asynchronous endpoints for digital twin monitoring, deterministic simulation, prescriptive optimization, root cause analysis, governance, and executive reporting.

Base URL: `/api/v1`

---

## 2. API Endpoints Catalog

### 2.1 System Vitals & Health
- **`GET /api/v1/health`**
  - **Purpose**: Verifies database connectivity, optimizer readiness, and process memory RSS footprint.
  - **Sample Response**:
    ```json
    {
      "status": "HEALTHY",
      "service": "SARAS ATLAS — Commerce Resilience & Decision Simulation Platform",
      "version": "1.0.0-phase1",
      "database": "ONLINE (SQLite WAL)",
      "optimizer": "READY (OR-Tools SCIP)",
      "memory": {
        "system_total_phys_gb": 7.75,
        "system_avail_phys_gb": 1.02,
        "process_working_set_mb": 218.95
      },
      "architecture": "In-Process Modular Monolith (< 350 MB Target RSS)"
    }
    ```

### 2.2 Digital Twin & Inventory Monitoring
- **`GET /api/v1/twin/topology`**
  - **Purpose**: Returns complete network topology (warehouses, suppliers, transport corridors).
- **`GET /api/v1/inventory/summary`**
  - **Purpose**: Returns network-wide inventory levels, safety stock thresholds, and stockout runout dates.
- **`GET /api/v1/risks/active`**
  - **Purpose**: Returns operational risk sentinel alerts with severity ratings and revenue exposure.

### 2.3 Simulation & Scenario Comparison
- **`POST /api/v1/simulation/run`**
  - **Payload**:
    ```json
    {
      "scenario_name": "Status Quo Unmitigated Disruption",
      "horizon_days": 90,
      "shocks": {
        "supplier_delays": [{ "po_number": "PO-9012", "delay_days": 21 }],
        "freight_surcharges": [{ "lane_id": "lane_east_coast_parcel", "surcharge_percentage": 0.28 }],
        "demand_elasticities": [{ "sku_code": "APEX-JKT", "demand_multiplier": 1.45, "duration_days": 30 }]
      },
      "mitigations": {}
    }
    ```
  - **Returns**: 90-day daily timeseries trajectory, summary scorecards, lost sales, and executive narrative.
- **`POST /api/v1/simulation/compare`**
  - **Payload**: Baseline request and comparison request.
  - **Returns**: Before-vs-after delta matrix across revenue, COGS, freight, and net CM.

### 2.4 Prescriptive Optimization (Google OR-Tools SCIP)
- **`POST /api/v1/optimization/solve`**
  - **Payload**:
    ```json
    {
      "capital_budget_ceiling": 40000.0,
      "min_service_fill_rate": 0.95,
      "max_ad_throttle_pct": 0.35,
      "target_sku": "APEX-JKT",
      "objective": "MAXIMIZE_CONTRIBUTION_MARGIN"
    }
    ```
  - **Returns**:
    ```json
    {
      "status": "OPTIMAL",
      "solve_time_ms": 54,
      "recommended_air_freight_units": 2995,
      "recommended_transfer_units": 800,
      "recommended_ad_throttle_pct": 0.0,
      "capital_required": 39997.50,
      "projected_contribution_margin_pct": 0.396,
      "rationale": "Global optimum reached. Maxed 800 units ground transfer @ $3.20/unit ($2,560.00), remaining $37,440.00 deployed into 2,995 air units ($37,437.50)."
    }
    ```

### 2.5 Multi-Scenario Batch & Sensitivity
- **`POST /api/v1/batch/run`**: Executes concurrent multi-parameter simulation runs across delay and demand grids.
- **`POST /api/v1/batch/sensitivity`**: Generates sensitivity elasticities and partial derivatives.

### 2.6 Dynamic Policy Optimization & Ingestion
- **`GET /api/v1/policy/list`**: Returns active sourcing and allocation policies.
- **`POST /api/v1/policy/evaluate`**: Evaluates policy switches against historical benchmarks.
- **`POST /api/v1/ingestion/preview`**: Ingests and validates CSV/Parquet uploads with strict schema checking.
- **`POST /api/v1/ingestion/commit`**: Merges staged datasets into SQLite master.
- **`POST /api/v1/ingestion/rollback`**: Reverts staging transactions atomically.

### 2.7 AI Copilot, Root Cause & Forecasting
- **`POST /api/v1/intelligence/query`**: Answers natural language supply chain resilience questions grounded in digital twin state.
- **`GET /api/v1/rca/trace`**: Traces the 5-tiered disruption cascade and loss decomposition for incident PO-9012 ($224,500.00 gross vs $129,844.32 net).
- **`GET /api/v1/forecasting/predict`**: Returns statistical demand forecasts with 80% and 95% confidence bands.

### 2.8 Governance & Two-Man Rule
- **`POST /api/v1/governance/approve`**: Submits executive approval (enforces Two-Man Rule when capital exceeds $25,000.00).
- **`GET /api/v1/governance/audit-trail`**: Retrieves immutable SHA-256 cryptographic audit ledger.

### 2.9 Executive Reporting Dossiers
- **`GET /api/v1/reports/summary`**: Returns JSON summary of executive dossier.
- **`GET /api/v1/reports/export/pdf`**: Generates and downloads 3-page boardroom PDF briefing.
- **`GET /api/v1/reports/export/csv`**: Generates and downloads RFC-4180 audit spreadsheet with 100% data parity.
