# SARAS ATLAS — PHASE 7: SECURITY & PRODUCTION HARDENING READINESS
## Online Demonstration Security Architecture, Threat Modeling & Access Governance

**Platform:** SARAS ATLAS — Commerce Resilience & Decision Simulation Platform  
**Target Enterprise:** Vanguard Apparel Co. ($45M GMV Digital Twin)  
**Author:** Autonomous Chief Information Security Officer (CISO) & Security Architect  
**Budget:** Strictly ₹0 / $0.00  
**Date:** November 3, 2026 (Corrected Revision)  
**Status:** COMPLETE SECURITY AUDIT & READINESS ASSESSMENT  

---

## 1. Executive Summary & Security Baseline

Publishing an enterprise decision simulation platform to the public internet across a Vercel Hobby + Render Free architecture requires addressing four core threat vectors:
1. **Computational Resource Starvation on 0.1 vCPU:** On a shared 0.1 vCPU core, malicious or automated rapid-fire requests to CPU-heavy endpoints (`/optimize/prescribe`, `/batch/run`) could starve the instance.
2. **Arbitrary File Upload Vulnerabilities:** The enterprise data ingestion module accepts CSV and Excel files. Malicious payload injection, buffer overflow, or CSV formula injection must be prevented.
3. **Information Disclosure & Credential Leaks:** Internal Windows paths, development database connection strings, JWT signing keys, and administrative credentials must never be exposed in API error traces or client bundles.
4. **Governance Integrity:** Public demonstration visitors must be able to experience the two-man rule approval workflow without risking host compromise or permanently corrupting the benchmark state.

---

## 2. Threat Modeling & Attack Surface Hardening

| Threat Vector | Potential Impact | Severity | Mitigation & Defense-in-Depth Mechanism | Implementation Status |
|---|---|---|---|---|
| **Computational Exhaustion (0.1 vCPU)** | Server hangs, CPU spikes, denial of service for other recruiters | HIGH | Tiered in-memory rate limiting + OR-Tools 3.0s hard solver timeout ceiling + Max 100 scenario batch limit | **IMPLEMENTED** in `RateLimitingMiddleware` & `settings.MAX_SOLVER_TIME_SECONDS` |
| **Malicious File Upload (CSV/XLSX)** | Remote code execution, server disk fill, macro execution | CRITICAL | 5 MB upload ceiling, strict MIME type validation (`text/csv`, `application/vnd.openxmlformats`), in-memory parsing via Pandas/OpenPyXL with formulas disabled (`data_only=True`), no disk shell execution | **IMPLEMENTED** in `src/api/routes/ingestion.py` |
| **JWT Key Disclosure / Forgery** | Unauthorized elevation to admin role | HIGH | `ATLAS_JWT_SECRET` loaded via environment variable; 8-hour token expiration; SHA-256 password hashing with enterprise salt | **IMPLEMENTED** in `src/security/auth.py` |
| **CORS Exploitation & Cross-Site Leaks** | Unauthorized third-party sites making API calls on behalf of users | MEDIUM | Vercel Server-Side Rewrite proxy binds frontend and API to single origin (`https://saras-atlas.vercel.app`); CORS allowlist explicitly locks Render backend to Vercel domain | **IMPLEMENTED** in `src/api/main.py` |
| **Tampering with Audit Logs** | Covert unauthorized decision approval | HIGH | SHA-256 cryptographic chaining on all governance events; in-memory tamper detection | **IMPLEMENTED** in `src/security/audit.py` |
| **CSV Formula Injection (Excel Macro)** | Client-side command execution when downloading audit CSVs | MEDIUM | Sanitization of cell contents starting with `=`, `+`, `-`, or `@` during CSV export generation | **IMPLEMENTED** in `src/api/routes/reports.py` |

---

## 3. Public Demonstration vs Authenticated Administration

To provide technical recruiters with an effortless demonstration experience while maintaining strict role-based access control (RBAC), SARAS ATLAS employs a **dual-access model**:

* **Public Interactive Demo (Unauthenticated / Guest Session):**
  * Full access to 16 dashboard modules, interactive sliders, simulation studio, before-vs-after comparison, and OR-Tools MILP optimization.
  * In-memory rate limiting protects server compute (30 req/min for optimization, 10 req/min for batch sweeps).
* **Pre-Seeded Demo Personas for Governance Showcases:**
  * Recruiters can test the Two-Man Rule Governance module without creating accounts by selecting built-in synthetic executive personas:
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

---

## 5. Synthetic Data Integrity & Third-Party Disclaimers

### 5.1 Synthetic Data Guarantee
* **Zero Real Customer Data:** 100% of inventory records, suppliers, purchase orders, warehouses, and financial transactions represent the synthetic business digital twin of **Vanguard Apparel Co. ($45M GMV)**.
* **Seed Reproducibility:** Deterministically generated using NumPy/Python `SYNTHETIC_SEED = 42`.
* **Zero PII:** Customer names, employee identities, and email addresses are entirely fictional synthetic mock entities (e.g. `admin@vanguardapparel.internal`).

### 5.2 Trademark & Affiliation Notice
Permanently rendered in the platform header and documentation:
> *"SARAS ATLAS is an independent, original business digital twin and decision simulation platform engineered for technical portfolio demonstration. It is not affiliated with, sponsored by, commissioned by, or endorsed by SARAS Analytics or any real-world commercial entity."*
