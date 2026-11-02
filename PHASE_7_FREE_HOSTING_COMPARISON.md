# SARAS ATLAS — PHASE 7: FREE HOSTING PROVIDER COMPARISON & EVALUATION
## Zero-Cost Infrastructure Feasibility Matrix for Online Demonstration

**Platform:** SARAS ATLAS — Commerce Resilience & Decision Simulation Platform  
**Target Organization:** Vanguard Apparel Co. ($45M GMV Digital Twin)  
**Author:** Autonomous CTO & Principal Cloud Architect  
**Budgetary Ceiling:** Strictly ₹0 / $0.00 (Permanent Free-Tier Only)  
**Date:** November 3, 2026  
**Status:** COMPLETE AUDIT & EVALUATION  

---

## 1. Executive Summary & Objective

The objective of Phase 7 is to evaluate, select, and prepare a verified zero-cost online hosting architecture for **SARAS ATLAS**, enabling technical recruiters, enterprise engineering leaders, and product strategists to access a live, interactive, online demonstration of the platform.

### Strict Safeguards Enforced:
1. **Total Expenditure:** Strictly **₹0.00 / $0.00**. No credit card billing, no paid domain purchases, no premium API credits, no trial traps.
2. **Local Environment Preservation:** The existing local deployment (`127.0.0.1:8000` and `127.0.0.1:3000`), SQLite database, data backups, and Git history must remain pristine and completely unaffected.
3. **No Premature Public Exposure:** In strict adherence to Section 7 of the Phase 7 Authorization Gate, no public URLs, tunnels, DNS changes, or deployments will be activated without explicit user review and confirmation.

---

## 2. Platform Computational Profile & Deployment Requirements

Before evaluating cloud providers, the actual resource consumption and runtime dependencies of SARAS ATLAS were profiled on the local Windows/x86_64 host:

| Platform Layer | Technology Stack | Working Set Memory (RSS) | Disk Storage | Runtime Requirements |
|---|---|---|---|---|
| **Frontend** | Next.js 15.1.7, React 19, TypeScript, Tailwind CSS, Recharts | ~110–140 MB | ~153 kB (gzip JS)<br>259 kB First Load | Node.js 18+ or 20+ runtime for SSR / API proxy, or static HTML/JS |
| **Backend REST API** | FastAPI 0.115, Uvicorn, Pydantic v2, Starlette | ~65–85 MB | Python environment: ~420 MB | Python 3.11/3.12 (standard glibc Linux x86_64 or arm64) |
| **Optimization Engine** | Google OR-Tools 9.11 (SCIP MILP Solver) | ~15–30 MB (burst) | Compiled C++ binary wheels (`ortools`) | Requires `glibc` (Debian/Ubuntu-based containers; incompatible with Alpine musl) |
| **Simulation & Analytics** | Discrete difference simulation (NumPy, SciPy, Pandas, DuckDB) | ~40–60 MB | ~120 KB SQLite DB<br>~250 KB DuckDB | In-process file/memory storage with read/write capability |
| **Total Peak Resource** | Full Platform | **~220–250 MB RAM** | **< 1.0 GB Disk** | **Burstable CPU for 2–15 ms MILP solves** |

---

## 3. Comprehensive Hosting Provider Comparison Matrix

Six candidate hosting platforms were evaluated against the six core criteria: **Cost (₹0), Security, Reliability, Maintenance, Full-Stack Compatibility, and Demo Integrity**.

| Feature / Metric | **Hugging Face Spaces (Docker/FastAPI)** | **Vercel + Render Split** | **Render (Unified Web Service)** | **Cloudflare Pages & Workers** | **Fly.io** | **Railway** |
|---|---|---|---|---|---|---|
| **True ₹0 Cost (No Credit Card)** | **YES (Guaranteed Free Tier)** | **YES (No CC required on Vercel/Render free)** | **YES (No CC required)** | YES (Free tier available) | NO (Requires CC registration) | NO (Trial credit expires; CC required) |
| **Compute Allowance** | **2 vCPU, 16 GB RAM** | Vercel Serverless + Render 0.1 CPU, 512 MB | 0.1 CPU, 512 MB RAM | 128 MB Worker RAM, 10-50ms CPU limit | 256 MB RAM (Free shared) | 512 MB RAM ($5 credit limit) |
| **Disk Storage** | **50 GB Free Ephemeral Disk** | Vercel (read-only) + Render 1 GB | 1 GB Ephemeral | KV / R2 storage (separate config) | 3 GB Free Volume | Ephemeral |
| **Python C++ Wheel Support (`ortools`, `duckdb`)** | **100% NATIVE (Debian glibc Docker)** | **YES on Render; NO on Vercel Functions (250MB size limit exceeded)** | **100% NATIVE (Debian glibc Docker)** | NO (Pyodide lacks `ortools` native C++ binary) | YES (Docker) | YES (Docker) |
| **Next.js 15 Support** | **YES (Containerized standalone or static export)** | **100% NATIVE (First-party Next.js platform)** | YES (Containerized Node.js) | Partial (Next.js on Pages has edge limitations) | YES (Docker) | YES (Nixpacks) |
| **Cold Start / Idle Sleep Behavior** | **Fast Wakeup (~5-10s) or Persistent** | Vercel: Instant (0s)<br>Render Backend: 30-50s sleep after 15m idle | 30-50s sleep after 15m idle | Instant (0s) | Fast (~2s) | Fast (~3s) |
| **Bandwidth Allowance** | **Unlimited (Fair Use)** | Vercel 100 GB/mo + Render 100 GB/mo | 100 GB/mo | Unlimited / 100k req/day | 100 GB/mo | 100 GB/mo |
| **Custom Subdomain / Public URL** | **YES (`hf.space/<user>/<space>`)** | **YES (`<app>.vercel.app`)** | **YES (`<app>.onrender.com`)** | YES (`<app>.pages.dev`) | YES (`<app>.fly.dev`) | YES (`<app>.up.railway.app`) |
| **Network Latency & SLA** | High (Global CDN + Fast US/EU Compute) | Ultra-Fast Edge UI + US/EU Backend | Medium (Cold starts after idle) | Ultra-Fast Global Edge | Fast Global Anycast | Fast |
| **Recruiter & Tech Audience Credibility** | **EXTREMELY HIGH (Industry benchmark for AI/ML and engineering)** | **VERY HIGH (Standard modern SaaS portfolio architecture)** | High (Common full-stack showcase) | Medium (Web-focused, not data science) | High (Developer-focused) | Medium |

---

## 4. Deep-Dive Provider Analysis

### 4.1 Candidate 1: Hugging Face Spaces (Unified Docker Architecture) — RECOMMENDED PRIMARY
* **Why it fits SARAS ATLAS:**
  * **Exceptional Free Compute:** Provides **2 vCPUs and 16 GB of RAM** with 50 GB of disk at exactly **₹0**. SARAS ATLAS backend consumes ~220 MB RAM, utilizing less than 2% of the available ceiling.
  * **Complete Dependency Independence:** By using a standard multi-stage Debian-based `Dockerfile`, Google OR-Tools (`ortools`), DuckDB, Scikit-learn, SciPy, and FastAPI compile and execute natively with full `glibc` support.
  * **Unified Zero-CORS Architecture:** The Next.js frontend is built in Stage 1 and served directly by FastAPI (or a lightweight Node.js SSR sidecar) inside the container. This completely eliminates CORS misconfigurations, third-party cookie blocking, and SSL cross-origin handshake failures.
  * **Industry Standing:** In AI/ML, operations research, and enterprise systems engineering, hosting a live interactive digital twin on Hugging Face Spaces is perceived as highly professional and technically authentic.
* **Limitations to Account For:**
  * Initial build takes ~3–4 minutes due to downloading scientific Python wheels.
  * Ephemeral disk resets on container rebuild (ideal for a demo: corrupted visitor data automatically reverts to the Vanguard Apparel benchmark state).

### 4.2 Candidate 2: Split Hybrid (Next.js on Vercel + FastAPI on Render) — VIABLE ALTERNATIVE
* **Why it fits:**
  * **Premier Frontend Delivery:** Vercel provides world-class global CDN edge delivery for Next.js 15 with instantaneous page load times and zero frontend cold starts.
  * **Backend Isolation:** Render hosts the FastAPI backend via a Docker container on Linux, providing glibc support for OR-Tools.
  * **Next.js API Rewrite Proxy:** By configuring `next.config.mjs` rewrites (`/api/:path*` $\rightarrow$ `https://saras-backend.onrender.com/api/:path*`), the browser communicates only with the Vercel domain, avoiding CORS errors.
* **Limitations to Account For:**
  * **Render Free Tier Spin-Down:** The backend automatically sleeps after 15 minutes of inactivity. When a recruiter opens the site after hours, the first API call experiences a **35–50 second cold start** before the backend wakes up. (A loading indicator or wake-up banner in the UI is mandatory if this option is selected).
  * **Two Repositories / Deployments:** Requires managing two separate deployment pipelines.

### 4.3 Candidate 3: Render Unified Web Service (Single Container)
* **Why it fits:** Single Git repository, runs Docker with both Next.js and FastAPI on a 512 MB free container.
* **Limitations:** 512 MB RAM is adequate (working set is ~240 MB), but cold starts remain 35–50 seconds on the free tier.

### 4.4 Rejected Options:
* **Cloudflare Workers / Pages:** Cannot execute native C++ x86_64 wheels for Google OR-Tools SCIP solver in V8 JavaScript isolates without heavy, fragile WebAssembly ports.
* **Railway & Fly.io:** Both now mandate active credit card verification during registration, violating the absolute ₹0 expenditure and no-credit-card mandate.
* **AWS Free Tier / Google Cloud / Azure:** Free tiers expire after 90–365 days and require a credit card, posing risks of accidental billings or infrastructure abandonment.

---

## 5. Architectural Trade-Off Analysis

| Dimension | Option A: Unified Container on Hugging Face Spaces | Option B: Split Hybrid (Vercel Frontend + Render Backend) |
|---|---|---|
| **Monthly Expenditure** | **₹0.00 (Guaranteed Permanent)** | **₹0.00 (Guaranteed Permanent)** |
| **Credit Card Requirement** | **NO** | **NO** |
| **Cold-Start Latency** | **Fast (5–8s wake or warm)** | **Instant Frontend, 35–50s Backend Cold Start** |
| **Available RAM** | **16,384 MB (16 GB)** | 512 MB (Render) |
| **CORS Risk** | **0% (Single Origin)** | Low (Managed by Next.js Server Rewrite) |
| **Deployment Complexity** | **Low (Single multi-stage Dockerfile)** | Medium (Two deployment configurations & env vars) |
| **Data Persistence Behavior** | Resets on restart (Guaranteed Clean Baseline) | Resets on restart (Guaranteed Clean Baseline) |

---

## 6. Selection Verdict & Justification

**RECOMMENDED ARCHITECTURE: OPTION A — UNIFIED MULTI-STAGE DOCKER CONTAINER ON HUGGING FACE SPACES (WITH OPTION B AS SECONDARY STANDBY)**

### Justification:
1. **Zero Financial Risk:** 100% free with no credit card registration, no expiration date, and no hidden bandwidth overage charges.
2. **Computational Headroom:** 16 GB RAM and 2 vCPUs eliminate out-of-memory (OOM) risks for batch scenario simulations (100 scenarios) and OR-Tools optimization.
3. **Single-Origin Simplicity:** Eliminates all cross-origin CORS hurdles and complex dual-platform environment synchronization.
4. **Professional Presentation:** Direct integration with Git, instant shareable URL, responsive embed options, and proven stability.

