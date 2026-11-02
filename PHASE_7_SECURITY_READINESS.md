# SARAS ATLAS — PHASE 7: SECURITY & PRODUCTION HARDENING READINESS
## Online Demonstration Security Architecture, Threat Modeling & Access Governance

**Platform:** SARAS ATLAS — Commerce Resilience & Decision Simulation Platform  
**Target Enterprise:** Vanguard Apparel Co. ($45M GMV Digital Twin)  
**Author:** Autonomous Chief Information Security Officer (CISO) & Security Architect  
**Budget:** Strictly ₹0 / $0.00  
**Date:** November 3, 2026  
**Status:** COMPLETE SECURITY AUDIT & READINESS ASSESSMENT  

---

## 1. Executive Summary & Security Baseline

Publishing an enterprise decision simulation platform to the public internet introduces critical security vectors that must be proactively mitigated before public exposure:
1. **Denial of Service (DoS) via Computational Exhaustion:** OR-Tools MILP optimization, 100-scenario Monte Carlo batch sweeps, and time-series model evaluations are CPU-intensive. Malicious or excessive visitor requests must not starve the container.
2. **Arbitrary File Upload & Code Injection:** The enterprise data ingestion module accepts CSV and Excel files. Malicious payload injection, buffer overflow, or CSV formula injection must be prevented.
3. **Information Disclosure & Credential Leaks:** Internal Windows paths, development database connection strings, JWT signing keys, and administrative credentials must never be exposed in API error traces or client bundles.
4. **Governance Integrity:** Public demonstration visitors must be able to experience the two-man rule approval workflow without risking host compromise or permanently corrupting the benchmark state.

---

## 2. Threat Modeling & Attack Surface Hardening

| Threat Vector | Potential Impact | Severity | Mitigation & Defense-in-Depth Mechanism | Implementation Status |
|---|---|---|---|---|
| **Computational Exhaustion (MILP/Monte Carlo)** | Server hangs, CPU spikes, denial of service for other recruiters | HIGH | Tiered in-memory rate limiting + OR-Tools 3.0s hard solver timeout ceiling + Max 100 scenario batch limit | **IMPLEMENTED** in `RateLimitingMiddleware` & `settings.MAX_SOLVER_TIME_SECONDS` |
| **Malicious File Upload (CSV/XLSX)** | Remote code execution, server disk fill, macro execution | CRITICAL | 5 MB upload ceiling, strict MIME type validation (`text/csv`, `application/vnd.openxmlformats`), in-memory parsing via Pandas/OpenPyXL with formulas disabled (`data_only=True`), no disk shell execution | **IMPLEMENTED** in `src/api/routes/ingestion.py` |
| **JWT Key Disclosure / Forgery** | Unauthorized elevation to admin role | HIGH | `ATLAS_JWT_SECRET` loaded via environment variable; 8-hour token expiration; SHA-256 password hashing with enterprise salt | **IMPLEMENTED** in `src/security/auth.py` |
| **CORS Exploitation & Cross-Site Leaks** | Unauthorized third-party sites making API calls on behalf of users | MEDIUM | Unified container architecture binds frontend and API to single origin (`window.location.origin`); strict CORS origin allowlist if deployed split | **IMPLEMENTED** in `src/api/main.py` |
| **Tampering with Audit Logs** | Covert unauthorized decision approval | HIGH | SHA-256 cryptographic chaining on all governance events; in-memory tamper detection | **IMPLEMENTED** in `src/security/audit.py` |
| **CSV Formula Injection (Excel Macro)** | Client-side command execution when downloading audit CSVs | MEDIUM | Sanitization of cell contents starting with `=`, `+`, `-`, or `@` during CSV export generation | **IMPLEMENTED** in `src/api/routes/reports.py` |

---

## 3. Separation of Public Demo vs Authenticated Administration

To provide technical recruiters with an effortless demonstration experience while maintaining strict role-based access control (RBAC), SARAS ATLAS employs a **dual-access model**:

```mermaid
flowchart TD
    Visitor["Public Visitor / Technical Recruiter"]
    Admin["Authorized Executive / Security Auditor"]

    subgraph AccessGate ["Authentication & Authorization Gateway"]
        AuthRouter["FastAPI Auth Router (/api/v1/auth)"]
        RBAC["Role-Based Access Control Filter"]
    end

    subgraph PublicEndpoints ["Public Interactive Demo Access (Read-Write Ephemeral)"]
        Dashboard["16 Dashboard Modules & Interactive Sliders"]
        Simulate["Scenario Simulation Studio (90-Day Horizon)"]
        Optimize["OR-Tools Prescriptive Optimization"]
        Forecast["Demand Forecasting Studio & WAPE Matrix"]
        RCA["Root Cause Analysis & Explainability Engine"]
        Copilot["AI Decision Intelligence Copilot"]
    end

    subgraph ProtectedEndpoints ["Governance & Administrative Operations"]
        TwoManRule["Two-Man Rule Dual Approval Execution"]
        DataCommit["Production Enterprise Ingestion Commit"]
        AuditTrail["Cryptographic Audit Trail Export"]
        SystemReboot["System State Re-initialization"]
    end

    Visitor -->|Unauthenticated / Guest Session| PublicEndpoints
    Visitor -->|Demo Pre-Auth Tokens| TwoManRule
    Admin -->|JWT Bearer Token (Admin / CFO / VP)| ProtectedEndpoints
    AuthRouter --> RBAC
    RBAC --> ProtectedEndpoints
```

### 3.1 Pre-Seeded Demo Personas for Recruiting Showcases
Recruiters can immediately test the governance module without creating accounts by selecting built-in synthetic executive personas:
* **Marcus Vance (VP Supply Chain):** Initiates emergency air freight and buffer replenishment mitigation requests.
* **Elena Rostova (Chief Financial Officer):** Evaluates contribution margin impact ($200,911.36 protected) and co-signs approvals exceeding the $25,000 threshold.
* **Atlas Administrator:** Reviews tamper-evident SHA-256 cryptographic audit logs.

---

## 4. HTTP Security Headers & Content Security Policy (CSP)

SARAS ATLAS enforces enterprise HTTP security headers on 100% of responses via `SecurityHeadersMiddleware`:

```http
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; connect-src 'self' https:;
X-Permitted-Cross-Domain-Policies: none
Referrer-Policy: strict-origin-when-cross-origin
```

* **Frame Options:** Set to `SAMEORIGIN` (allows Hugging Face Space embedding while preventing external clickjacking).
* **Content Security Policy:** Restricts script execution to the application origin and inline scripts necessary for Next.js hydration.

---

## 5. Rate Limiting Architecture for Public Demonstration

To ensure smooth multi-tenant recruiter evaluation without service disruption, in-memory sliding window rate limits are enforced by client IP:

| Endpoint Group | Maximum Rate Ceiling | Window Duration | Burst Behavior |
|---|---|---|---|
| **General Telemetry (`/health`, `/twin/*`, `/risks/*`)** | 300 requests | 60 seconds | Instant response |
| **Heavy Computational Solvers (`/optimize/prescribe`)** | 30 requests | 60 seconds | HTTP 429 with `Retry-After: 15` |
| **Batch Scenario Sweeps (`/batch/run`)** | 10 requests | 60 seconds | HTTP 429 with `Retry-After: 30` |
| **File Ingestion Uploads (`/ingestion/upload`)** | 10 uploads | 60 seconds | HTTP 429 with `Retry-After: 30` |

---

## 6. Synthetic Data Integrity & Third-Party Disclaimers

### 6.1 Synthetic Data Guarantee
* **Zero Real Customer Data:** 100% of inventory records, suppliers, purchase orders, warehouses, and financial transactions represent the synthetic business digital twin of **Vanguard Apparel Co. ($45M GMV)**.
* **Seed Reproducibility:** Deterministically generated using NumPy/Python `SYNTHETIC_SEED = 42`.
* **Zero PII:** Customer names, employee identities, and email addresses are entirely fictional synthetic mock entities (e.g. `admin@vanguardapparel.internal`).

### 6.2 Trademark & Affiliation Notice
To adhere strictly to industry ethics and legal standards, the following notice is permanently rendered in the platform header and documentation:
> *"SARAS ATLAS is an independent, original business digital twin and decision simulation platform engineered for technical portfolio demonstration. It is not affiliated with, sponsored by, commissioned by, or endorsed by SARAS Analytics or any real-world commercial entity."*

