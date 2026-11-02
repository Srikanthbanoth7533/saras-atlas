# SARAS ATLAS — PRODUCT REQUIREMENTS DOCUMENT (PRD)

**Document ID:** PRD-ATLAS-001  
**Version:** 1.0.0  
**Phase:** Phase 0 Baseline  
**Author:** Principal Product Strategist & Enterprise Architect  
**Reviewers:** Technical Program Manager, Autonomous CTO, Cybersecurity Architect  

---

## 1. Product Overview & Strategic Intent

### 1.1 Objective
SARAS ATLAS is an operational digital twin and counterfactual decision simulation platform designed for omnichannel e-commerce and retail businesses. The primary objective is to empower executive and operational leaders to simulate the multi-echelon physical and financial consequences of supply chain shocks (supplier delays, freight cost inflation, demand surges) and execute mathematically optimal, constraint-aware mitigation decisions.

### 1.2 Target Audience & Personas
1. **Chief Operating Officer (COO) / VP of Supply Chain:** Needs visibility into warehouse stockout horizons, carrier lane performance, and transfer logistics; seeks to eliminate stockouts without bloating inventory carrying costs.
2. **Chief Financial Officer (CFO) / VP of Finance:** Focuses on Contribution Margin (CM), working capital liquidity, cash burn rates, inventory holding costs, and mitigating unexpected logistics surcharges.
3. **Head of Growth / VP of Marketing:** Balances paid advertising acquisition spend (CAC/ROAS) against physical inventory availability; requires alerts to prevent spending ad dollars on inventory heading into stockouts.
4. **Founder / CEO:** Requires unified executive situational awareness, clear alternative comparisons ("Option A vs Option B vs Option C"), and transparent evidence before authorizing capital-intensive actions.
5. **Forward Deployed Engineer (FDE):** Technical operator who customizes, provisions, and embeds the platform into client data stacks to deliver continuous operational ROI.

---

## 2. User Journeys & Core Workflows

### Journey 1: Disruption Detection & Impact Propagation (The "Morning Routine")
1. **Trigger:** The system ingests daily operational snapshots (inventory balances, inbound ASN / purchase order tracking updates, carrier freight invoices, and sales velocity).
2. **Detection:** The Risk Detection Engine flags a critical vulnerability: *Purchase Order #PO-8821 (10,000 units of SKU-APPAREL-01) has suffered a 21-day port congestion delay in Long Beach, CA.*
3. **Propagation:** The Digital Twin propagates this delay forward across the multi-echelon network:
   - Primary West Coast 3PL will stock out in 9 days.
   - East Coast 3PL will attempt to fulfill national orders, increasing average fulfillment cost from $6.20 to $11.80 per unit due to cross-country Zone 7/8 shipping.
   - East Coast 3PL will completely exhaust stock 12 days later.
   - 30-day projected revenue loss: $142,500; projected margin collapse: -22.4 percentage points.
4. **Alert:** The Executive Situation Room highlights the SKU with an amber "Critical Stockout & Margin Erosion Warning."

### Journey 2: Counterfactual Scenario Simulation Studio
1. **Action:** The COO opens the Scenario Simulation Studio to model alternatives.
2. **Hypothesis Creation:**
   - *Scenario 1 (Status Quo):* Take no corrective action. Let stock run out and resume when PO-8821 arrives.
   - *Scenario 2 (Expedited Air Freight):* Issue an emergency purchase order for 3,000 units to a backup factory in Vietnam with 7-day air delivery at $14.50/unit freight.
   - *Scenario 3 (Inventory Reallocation & Ad Throttling):* Transfer 1,500 units from the European distribution center via priority air, reallocate stock between US warehouses, and throttle Google/Meta ad spend by 25% on SKU-APPAREL-01 to reduce burn velocity.
3. **Execution:** The user clicks "Run Simulation". The engine calculates multi-period balance equations, fulfillment routing matrices, and cash requirements in < 150 ms.
4. **Comparison:** A multi-dimensional scorecard renders: Net Revenue, Contribution Margin $, CM %, Working Capital Required, Customer Fill Rate, and Stockout Days.

### Journey 3: Mixed-Integer Linear Optimization & Recommendation
1. **Action:** The user requests an algorithmic solution: "Generate Optimal Mitigation Plan".
2. **Constraint Definition:**
   - Maximum additional cash outlay: $40,000.
   - Minimum acceptable customer order fill rate: 88%.
   - Minimum acceptable SKU Contribution Margin: 18.0%.
3. **Solver Execution:** The OR-Tools MILP solver processes integer decision variables (units transferred, units air-freighted, ad spend reduction factor, carrier lane selection).
4. **Output:** A mathematically provable optimal decision is recommended, complete with sensitivity analysis and a step-by-step action plan.
5. **Governance & Approval:** The COO and CFO electronically sign off on the plan within the platform, generating an immutable audit record and exportable operational instructions.

---

## 3. Functional Requirements (FR)

### Module 1: Canonical Commerce Digital Twin (FR-01 to FR-04)
- **FR-01 (Multi-Echelon Network Graph):** The system MUST represent the physical supply chain as a directed multigraph $G = (V, E)$, where vertices $V$ represent Suppliers, Ports, Consolidation Hubs, 3PL Fulfillment Centers, and Customer Zones, and edges $E$ represent transport lanes characterized by lead-time distributions, transport modes (Ocean, Air, Parcel), and cost matrices.
- **FR-02 (SKU & Unit Economics Mapping):** The system MUST maintain detailed unit economics for each SKU, including base Bill of Materials / Supplier COGS, inbound freight tariffs, customs duties, storage holding costs per day, pick/pack fees, channel referral fees, and outbound parcel rate cards by carrier zone (Zones 1 through 8).
- **FR-03 (Inventory State Tracking):** The system MUST track multi-echelon inventory states across discrete buckets: On-Hand (Available to Promise), Reserved (Committed to Open Orders), In-Transit (Shipped POs on water/air), and Backordered.
- **FR-04 (Multi-Location Inventory Balancing):** The system MUST compute daily balance equations for every SKU across every node over a forward-looking 90-day planning horizon.

### Module 2: Disruption Detection & Impact Propagation (FR-05 to FR-07)
- **FR-05 (Automated Vulnerability Detection):** The system MUST continuously calculate the "Days of Inventory Coverage" (DoC) and "Stockout Probability" for every SKU-node pair, raising alerts when coverage drops below cumulative replenishment lead times.
- **FR-06 (Cascading Propagation Engine):** When an upstream shock occurs (lead-time extension, node closure, shipping rate spike), the engine MUST automatically recalculate downstream order fulfillment routes, identifying secondary warehouse split-shipments, stock transfers, and carrier surcharge impacts.
- **FR-07 (Financial Shock Mapping):** The engine MUST project the daily financial impact of disruptions across four core financial metrics:
  1. Gross Revenue Exposure ($)
  2. Net Realized Revenue ($)
  3. Net Contribution Margin ($ and %)
  4. Working Capital & Cash Burn ($)

### Module 3: Scenario Simulation Studio (FR-08 to FR-11)
- **FR-08 (Zero-Risk Branching Sandbox):** The system MUST allow users to clone the production digital twin state into isolated, ephemeral simulation branches without modifying baseline operational data.
- **FR-09 (Parametric Shock Levers):** The simulation interface MUST provide interactive parameter controls for:
  - Supplier lead-time shifts ($\Delta L \in [-30, +60]$ days)
  - Demand elasticity multipliers ($\alpha \in [0.5, 3.0]$)
  - Carrier freight cost multipliers ($\beta \in [0.8, 2.5]$)
  - Ad spend scaling factors ($\gamma \in [0.0, 2.0]$)
- **FR-10 (Sub-Second Batch Evaluation):** The simulation engine MUST evaluate a 90-day multi-echelon scenario across 100 SKUs and 5 warehouses in under 200 milliseconds on the host hardware.
- **FR-11 (Side-by-Side Scenario Scorecards):** The UI MUST render clear comparative delta tables displaying baseline vs alternative scenarios with explicit percentage and dollar differences.

### Module 4: Prescriptive Optimization Engine (FR-12 to FR-14)
- **FR-12 (Mixed-Integer Linear Programming Formulation):** The system MUST formulate decision trade-offs as a constrained MILP model solvable via Google OR-Tools.
- **FR-13 (Configurable Objective Functions):** The solver MUST support dual primary objective functions selectable by the user:
  - *Objective A:* Maximize Cumulative Net Contribution Margin ($) subject to service level and cash constraints.
  - *Objective B:* Minimize Operational Cost & Stockout Penalties subject to working capital ceiling.
- **FR-14 (Hard & Soft Constraints):** The optimization solver MUST enforce hard operational constraints (warehouse physical capacity, supplier minimum order quantities, maximum budget ceilings, lead-time physics) and soft penalties (customer stockout dissatisfaction).

### Module 5: Governance, Audit & Explainability (FR-15 to FR-18)
- **FR-15 (Deterministic Narrative Synthesis):** The system MUST generate comprehensive, publication-quality executive briefings explaining disruption causes, financial impact breakdowns, and recommendation rationales using deterministic variance decomposition without requiring an external paid LLM API.
- **FR-16 (Immutable Decision Log & Audit Trail):** Every simulated scenario, parameter adjustment, user comment, and formal approval MUST be logged with cryptographic timestamping and user attribution.
- **FR-17 (Two-Man Rule Approval Workflows):** Decisions involving capital outlays exceeding a configurable threshold (e.g. > $25,000) MUST require electronic multi-stakeholder sign-off (e.g. COO + CFO) before generating operational dispatch orders.
- **FR-18 (Model Context Protocol / External API Readiness):** The simulation engine MUST expose authenticated OpenAPI REST endpoints and clean tool schemas compliant with the Anthropic Model Context Protocol (MCP) to allow external conversational agents (such as Saras iQ or Claude) to invoke simulations safely.

---

## 4. Non-Functional Requirements (NFR)

### 4.1 Performance & Latency
- **NFR-01 (Simulation Latency):** 90-day simulation execution for the standard enterprise baseline MUST complete in $\le 250$ milliseconds.
- **NFR-02 (Optimization Solve Time):** OR-Tools MILP optimization solve time MUST be strictly bounded by a 5.0-second timeout ceiling, returning the best feasible integer solution found.
- **NFR-03 (UI Responsiveness):** Dashboard and scenario comparison tables MUST achieve First Contentful Paint (FCP) $\le 1.0$ second and cumulative layout shift (CLS) $\le 0.05$.

### 4.2 Resource & Hardware Boundedness (8 GB RAM Host Target)
- **NFR-04 (Memory Footprint):** The backend Python runtime MUST consume $\le 350$ MB resident memory (RSS) during active multi-scenario simulation.
- **NFR-05 (Frontend Memory):** Next.js client-side execution in the browser MUST consume $\le 150$ MB RAM.
- **NFR-06 (Zero Background Daemon Overhead):** The application MUST NOT require background services or daemons running when the application is terminated.

### 4.3 Cost & Third-Party Dependencies
- **NFR-07 (Zero Spending Compliance):** The platform MUST operate at exactly ₹0 cost. No external paid cloud subscription, API token, or proprietary database license is required for any core feature.
- **NFR-08 (Permissive Open-Source Licensing):** All software libraries MUST be licensed under MIT, Apache 2.0, or BSD licenses. No AGPL or commercial proprietary code.

### 4.4 Security & Data Privacy
- **NFR-09 (Zero Irreversible Autonomous Actions):** The platform MUST NOT trigger autonomous financial wire transfers, live supplier purchase orders, or irreversible database deletes without explicit human authentication and confirmation.
- **NFR-10 (Data Isolation & Integrity):** SQLite database MUST operate with Write-Ahead Logging (WAL) and strict foreign key integrity enabled.

---

## 5. Success Metrics & Validation KPIs

| KPI Code | Metric Name | Phase 0 Target | Phase 1-4 Production Target |
| :--- | :--- | :--- | :--- |
| **KPI-01** | Simulation Engine Speed | $\le 250$ ms per scenario | $\le 100$ ms per scenario |
| **KPI-02** | Optimization Optimality Gap | Feasible within 5.0s | Gap $\le 2.0\%$ within 3.0s |
| **KPI-03** | Financial Calculation Precision | Exact GAAP alignment | Zero floating-point drift |
| **KPI-04** | Host Memory Usage | $\le 500$ MB combined | $\le 450$ MB combined |
| **KPI-05** | Total Financial Spend | ₹0.00 | ₹0.00 |

