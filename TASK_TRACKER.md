# SARAS ATLAS — TASK TRACKER

**Project:** SARAS ATLAS (Commerce Resilience & Decision Simulation Platform)  
**Program Status:** Phase 0 Complete — Phase 1 Ready  
**Date:** November 2, 2026  

---

## Phase 0 Work Breakdown Structure (WBS) & Tracking

| Task ID | Task Category | Description | Owner | Status | Validation Artifact |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T0.1.1** | System Inspection | Hardware discovery: CPU, RAM, Disk, GPU via WMI | DevOps | **DONE** | CIM query logs, `docs/technology_and_dependency_register.md` |
| **T0.1.2** | Toolchain Audit | Discover Git, Node, npm, Python versions, package managers | DevOps | **DONE** | CLI validation output |
| **T0.1.3** | RAM Audit & Sizing | Evaluate 8GB physical memory constraint & RAM budgeting | Arch | **DONE** | `IMPLEMENTATION_LOG.md` (Entry 001) |
| **T0.1.4** | Workspace Setup | Initialize `saras-atlas` directory, git repo, `.gitignore` | DevOps | **DONE** | `.gitignore`, Git init log |
| **T0.1.5** | Python Isolation | Provision isolated Python 3.12.10 virtual environment (`.venv`) | DevOps | **DONE** | `.venv/Scripts/python.exe` verified |
| **T0.1.6** | Storage Strategy | Formulate SQLite (OLTP) + DuckDB (OLAP) zero-overhead ADR | Arch | **DONE** | ADR-001 |
| **T0.2.1** | Saras Research | Audit Daton, Pulse, Saras iQ, iQ MCP, FDE offerings | Strategist | **DONE** | `docs/saras_product_capability_audit.md` |
| **T0.2.2** | Customer Validation | Analyze published Saras case studies (Faherty, BPN, Lansinoh) | Strategist | **DONE** | Case study synthesis & attribution |
| **T0.2.3** | Overlap Analysis | Map Saras descriptive capabilities vs ATLAS simulation gap | Strategist | **DONE** | `docs/opportunity_and_differentiation_analysis.md` |
| **T0.3.1** | Competitor Audit | Research Triple Whale, Polar, Northbeam, Daasity, Peel, Glew | Market Intel| **DONE** | `docs/competitor_landscape.md` |
| **T0.3.2** | Enterprise Audit | Benchmark Kinaxis, Coupa, Blue Yonder, ToolsGroup, Aera | Market Intel| **DONE** | `docs/competitor_landscape.md` |
| **T0.3.3** | Source Register | Assemble verified URLs, citation dates, and evidence tiers | Market Intel| **DONE** | `docs/source_register.md` |
| **T0.4.1** | Opportunity Matrix | Score 4 candidate product concepts on value, risk, & cost | PM / CTO | **DONE** | `docs/opportunity_and_differentiation_analysis.md` |
| **T0.4.2** | Flagship Use Case | Formalize trans-pacific supplier delay + freight spike + surge | PM | **DONE** | `docs/customer_problem_and_business_case.md` |
| **T0.5.1** | Scope Evaluation | Audit 11 candidate modules; carve out rigorous MVP scope | PM | **DONE** | `docs/final_product_scope.md` |
| **T0.6.1** | System Architecture | Design Modular Monolith, Component Diagram, Data Flows | Arch | **DONE** | `docs/system_architecture.md` |
| **T0.6.2** | API Specification | Design REST API contracts for Digital Twin, Scenarios, & Solver | Arch | **DONE** | `docs/api_design.md` |
| **T0.7.1** | Data Modeling | Define canonical relational schemas, foreign keys, indexes | Data Eng | **DONE** | `docs/database_and_data_model.md` |
| **T0.7.2** | Synthetic Strategy | Design realistic multi-echelon disruption dataset generator | Data Eng | **DONE** | `docs/synthetic_data_strategy.md` |
| **T0.8.1** | Calculation Formulas | Specify exact inventory coverage, stockout risk, CM, working cap | AI/ML Eng | **DONE** | `docs/simulation_methodology.md` |
| **T0.8.2** | Forecasting Design | Formulate baseline statistical models, backtesting, uncertainty | AI/ML Eng | **DONE** | `docs/forecasting_and_ml_strategy.md` |
| **T0.8.3** | Optimization Model | Formulate MILP decision solver (OR-Tools) with constraints | AI/ML Eng | **DONE** | `docs/optimization_methodology.md` |
| **T0.8.4** | Agent & Explain | Design Explainability narrative engine and agent workflow | AI/ML Eng | **DONE** | `docs/ai_agent_architecture.md` |
| **T0.9.1** | Security Modeling | Develop STRIDE threat model, RBAC, human approval gates | Security | **DONE** | `docs/security_threat_model.md` |
| **T0.10.1** | Document Assembly | Author all 22 Phase 0 documentation manuals in `docs/` | Program Mgr| **DONE** | `docs/*.md` |
| **T0.11.1** | Phase 0 Gate Check | Conduct end-of-phase verification and go/no-go audit | CTO | **DONE** | `TEST_RESULTS.md`, Final Report |

---

## Phase 1 Preview (Pending User Authorization)

| Task ID | Target Phase | Proposed Title | Dependencies |
| :--- | :--- | :--- | :--- |
| **T1.1.1** | Phase 1 | Core Domain Models & SQLAlchemy Declarative Base | Phase 0 Approval |
| **T1.1.2** | Phase 1 | Synthetic Commerce Generator (Realistic E-Commerce Dataset) | T1.1.1 |
| **T1.2.1** | Phase 1 | Digital Twin State Engine & Inventory Balance Equations | T1.1.2 |
| **T1.2.2** | Phase 1 | Financial Propagation Engine (Contribution Margin & Cash) | T1.2.1 |
| **T1.3.1** | Phase 1 | Multi-Scenario Simulation Runner (Baseline vs Disruption) | T1.2.2 |
| **T1.4.1** | Phase 1 | Google OR-Tools Heuristic Decision Optimizer | T1.3.1 |
| **T1.5.1** | Phase 1 | FastAPI Endpoints & Contract Testing | T1.4.1 |
