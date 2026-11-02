# REST API & OPENAPI SPECIFICATION

**Document ID:** API-ATLAS-001  
**Version:** 1.0.0  
**Phase:** Phase 0 Baseline  
**Author:** Senior Backend Architect & API Designer  

---

## 1. API Architecture & Design Standards

The SARAS ATLAS Application Programming Interface is built according to modern RESTful principles, strictly validated via **Pydantic v2**, and documented automatically via OpenAPI 3.1.0 (Swagger UI at `/docs`).

Core design standards:
1. **Base URL:** `http://127.0.0.1:8000/api/v1`
2. **Data Format:** All requests and responses use UTF-8 encoded `application/json`.
3. **Idempotency & Safety:** All `GET` requests are side-effect free. State mutations use explicit `POST` or `PUT` verbs with UUID-based idempotency keys.
4. **Latency Target:** Sub-50ms response times for operational queries; sub-200ms for 90-day multi-echelon scenario simulations.
5. **Model Context Protocol (MCP) Integration:** Exposes standardized tool endpoints formatted to Anthropic's MCP specification, enabling AI assistants (like Claude or Saras iQ) to query twin state and run simulations safely.

---

## 2. Comprehensive Endpoint Catalog

```
+-----------------------------------------------------------------------------------------+
|                               API ENDPOINT TAXONOMY                                     |
+-------------------+---------------------------------------------+-----------------------+
| Subsystem         | Path                                        | Method & Purpose      |
+-------------------+---------------------------------------------+-----------------------+
| System Health     | /api/v1/health                              | GET: Host & Engine OK |
| Digital Twin      | /api/v1/twin/topology                       | GET: Network Nodes    |
|                   | /api/v1/twin/inventory-summary              | GET: Stock & DoC      |
| Risk Sentinels    | /api/v1/risks/active                        | GET: Flagged Shocks   |
| Simulation        | /api/v1/scenarios/simulate                  | POST: Run Shock Sim   |
|                   | /api/v1/scenarios/compare                   | GET: Compare Scenarios|
| Optimization      | /api/v1/optimization/solve                  | POST: OR-Tools Solver |
| Governance        | /api/v1/governance/approve                  | POST: 2-Man Sign-Off  |
|                   | /api/v1/governance/audit-trail              | GET: Immutable Log    |
| MCP Gateway       | /api/v1/mcp/tools                           | GET: List MCP Tools   |
|                   | /api/v1/mcp/tools/call                      | POST: Execute MCP Tool|
+-------------------+---------------------------------------------+-----------------------+
```

---

## 3. Detailed Endpoint Specifications

### 3.1 System Health & Diagnostics
#### `GET /api/v1/health`
Returns host environment vitals, database connection status, and solver readiness.

- **Response `200 OK`:**
```json
{
  "status": "HEALTHY",
  "version": "1.0.0",
  "timestamp": "2026-11-02T20:30:00Z",
  "environment": {
    "os": "Windows 11 Home",
    "python_version": "3.12.10",
    "ram_allocated_mb": 184.5,
    "ram_free_mb": 1720.0
  },
  "storage": {
    "oltp_database": "SQLite 3.45 (WAL Mode)",
    "olap_database": "DuckDB 1.1 Embedded",
    "status": "CONNECTED"
  },
  "solvers": {
    "google_ortools_milp": "READY"
  }
}
```

---

### 3.2 Digital Twin State Endpoints

#### `GET /api/v1/twin/topology`
Retrieves the active multi-echelon network graph (Suppliers, Ports, Warehouses, Customer Zones) with geographical coordinates, transit lead times, and current stock status.

- **Response `200 OK`:**
```json
{
  "organization_id": "org_vanguard_01",
  "nodes": [
    {
      "id": "node_supp_shenzhen",
      "type": "SUPPLIER",
      "name": "Apex Factory 01 (Shenzhen)",
      "country": "CHN",
      "lat": 22.5431,
      "lng": 114.0579,
      "status": "OPERATIONAL"
    },
    {
      "id": "node_wh_reno",
      "type": "WAREHOUSE_3PL",
      "name": "West Coast 3PL (Reno, NV)",
      "country": "USA",
      "lat": 39.5296,
      "lng": -119.8138,
      "status": "CRITICAL_STOCKOUT_RISK"
    },
    {
      "id": "node_wh_allentown",
      "type": "WAREHOUSE_3PL",
      "name": "East Coast 3PL (Allentown, PA)",
      "country": "USA",
      "lat": 40.6084,
      "lng": -75.4902,
      "status": "OPERATIONAL"
    }
  ],
  "edges": [
    {
      "from_node": "node_supp_shenzhen",
      "to_node": "node_wh_reno",
      "mode": "OCEAN",
      "lead_time_days": 45,
      "base_freight_unit_cost": 6.00,
      "active_po_count": 1
    },
    {
      "from_node": "node_wh_reno",
      "to_node": "zone_pacific_us",
      "mode": "PARCEL_GROUND",
      "lead_time_days": 2,
      "base_freight_unit_cost": 8.50,
      "status": "NORMAL"
    }
  ]
}
```

---

### 3.3 Scenario Simulation Endpoints

#### `POST /api/v1/scenarios/simulate`
Executes an in-memory counterfactual simulation, applying user-specified disruption levers and computing forward-looking financial statements and stockout timelines.

- **Request Body (`SimulationRequest`):**
```json
{
  "scenario_name": "Tri-Disruption: Delayed PO + Freight Spike + Viral Surge",
  "horizon_days": 90,
  "shocks": {
    "supplier_delays": [
      {
        "po_number": "PO-9012",
        "delay_days": 21
      }
    ],
    "freight_surcharges": [
      {
        "lane_id": "lane_east_coast_parcel",
        "surcharge_percentage": 0.28
      }
    ],
    "demand_elasticities": [
      {
        "sku_code": "APEX-JKT-BLK",
        "demand_multiplier": 1.45,
        "duration_days": 30
      }
    ]
  },
  "mitigations": {
    "emergency_air_freight_units": 1500,
    "inter_warehouse_transfer_units": 600,
    "ad_spend_throttle_percentage": 0.18
  }
}
```

- **Response `200 OK` (`SimulationResponse`):**
```json
{
  "simulation_id": "sim_run_99812",
  "execution_duration_ms": 112,
  "horizon_days": 90,
  "summary_scorecard": {
    "gross_revenue": 1425600.00,
    "net_revenue": 1382400.00,
    "cogs_total": 412500.00,
    "freight_total": 182400.00,
    "allocated_ad_spend": 284200.00,
    "net_contribution_margin": 461800.00,
    "contribution_margin_pct": 0.3341,
    "stockout_days_avoided": 11,
    "working_capital_required": 22400.00
  },
  "comparison_vs_baseline": {
    "delta_revenue": 351000.00,
    "delta_contribution_margin": 241800.00,
    "margin_percentage_shift": -0.0469,
    "avoided_cross_zone_freight_penalty": 38400.00
  },
  "executive_narrative": "Applying a 1,500-unit emergency air shipment combined with an 18% marketing ad throttle eliminates the 11-day stockout window completely, preserving $351,000 in net sales and protecting $241,800 in Contribution Margin with an outlay of $22,400 in self-funding capital."
}
```

---

### 3.4 Optimization Engine Endpoints

#### `POST /api/v1/optimization/solve`
Invokes the Google OR-Tools Mixed-Integer Linear Programming (MILP) solver to compute the mathematically optimal mitigation plan given budget and service constraints.

- **Request Body (`OptimizationRequest`):**
```json
{
  "scenario_id": "sim_run_99812",
  "objective": "MAXIMIZE_CONTRIBUTION_MARGIN",
  "constraints": {
    "max_capital_outlay_dollars": 40000.00,
    "min_order_fill_rate": 0.90,
    "max_ad_throttle_pct": 0.30,
    "max_solver_seconds": 3.0
  }
}
```

- **Response `200 OK` (`OptimizationResponse`):**
```json
{
  "solver_status": "OPTIMAL",
  "solve_time_ms": 348,
  "optimality_gap": 0.00,
  "optimal_decision_vector": {
    "air_freight_allocation": [
      {
        "sku_code": "APEX-JKT-BLK-M",
        "units": 850,
        "vendor": "VEND-VIETNAM-02",
        "freight_cost": 10625.00
      },
      {
        "sku_code": "APEX-JKT-BLK-L",
        "units": 650,
        "vendor": "VEND-VIETNAM-02",
        "freight_cost": 8125.00
      }
    ],
    "inter_warehouse_transfers": [
      {
        "sku_code": "APEX-JKT-BLK-S",
        "units": 600,
        "from_warehouse": "WH-EAST-ALLENTOWN",
        "to_warehouse": "WH-WEST-RENO",
        "transfer_cost": 1920.00
      }
    ],
    "ad_spend_adjustment": {
      "sku_code": "APEX-JKT-BLK",
      "throttle_percentage": 0.18,
      "daily_savings": 810.00
    }
  },
  "projected_outcome": {
    "total_capital_outlay": 20670.00,
    "net_contribution_margin_saved": 248900.00,
    "roi_on_mitigation": 12.04
  }
}
```

---

### 3.5 Governance & Human Approval Endpoints

#### `POST /api/v1/governance/approve`
Executes an authenticated multi-signature approval for a proposed optimization recommendation.

- **Request Body (`ApprovalRequest`):**
```json
{
  "recommendation_id": "rec_opt_90114",
  "approver_id": "usr_coo_sarah",
  "role": "COO",
  "decision": "APPROVED",
  "comments": "Approved air freight split and stock transfer. Verified with Allentown warehouse manager."
}
```

- **Response `200 OK`:**
```json
{
  "approval_id": "appr_77182",
  "status": "APPROVED",
  "digital_signature_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "timestamp": "2026-11-02T20:35:10Z",
  "actionable_dispatch_ready": true
}
```

---

### 3.6 Model Context Protocol (MCP) Endpoints

#### `GET /api/v1/mcp/tools`
Returns the tool registration schema compliant with Anthropic's Model Context Protocol.

- **Response `200 OK`:**
```json
{
  "tools": [
    {
      "name": "saras_atlas_simulate_shock",
      "description": "Simulates multi-echelon supply chain disruptions and returns projected Contribution Margin and stockout horizons.",
      "input_schema": {
        "type": "object",
        "properties": {
          "po_delay_days": { "type": "integer", "description": "Delay in purchase order arrival" },
          "freight_surcharge_pct": { "type": "number", "description": "Percentage freight surcharge" },
          "demand_surge_pct": { "type": "number", "description": "Demand surge multiplier" }
        },
        "required": ["po_delay_days"]
      }
    },
    {
      "name": "saras_atlas_optimize_decision",
      "description": "Invokes the Google OR-Tools MILP solver to find optimal split air-freight and stock transfer mitigations under cash constraints.",
      "input_schema": {
        "type": "object",
        "properties": {
          "max_budget": { "type": "number", "description": "Maximum cash outlay permitted" }
        },
        "required": ["max_budget"]
      }
    }
  ]
}
```
