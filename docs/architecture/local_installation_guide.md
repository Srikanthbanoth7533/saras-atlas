# SARAS ATLAS — Local Installation & Quickstart Guide

## 1. Prerequisites
To run SARAS ATLAS locally with strictly **₹0 external cloud bills**, ensure the following tools are installed:
- **Operating System**: Windows 10/11, macOS (Apple Silicon or Intel), or Linux (Ubuntu 22.04+).
- **Python**: 3.12+ (requires `ortools`, `fastapi`, `duckdb`, `reportlab`, `pytest`).
- **Node.js**: v20+ LTS (with `npm`).
- **Git**: For version control.
- **Hardware Footprint**: Standard laptop with ≥ 8 GB RAM (ATLAS runtime consumes `< 350 MB RSS`).

---

## 2. Step-by-Step Setup Instructions

### Step 1: Clone Repository
```bash
git clone https://github.com/Srikanthbanoth7533/saras-atlas.git
cd saras-atlas
```

### Step 2: Configure Python Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# Install backend dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Seed Synthetic Benchmark Database
Populate the SQLite WAL database (`data/saras_atlas.db`) and DuckDB OLAP store with the calibrated Vanguard Apparel Co. dataset (50 SKUs, 3 DCs, 4 global suppliers, 37.5k order history lines):
```bash
python -m src.synthetic.loader
```

### Step 4: Launch Backend API Server
```bash
python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000
```
Verify backend health in browser or terminal:
```bash
curl http://127.0.0.1:8000/api/v1/health
# Expected output: {"status": "HEALTHY", "database": "ONLINE", "optimizer": "READY"}
```

### Step 5: Launch Next.js Frontend
Open a separate terminal:
```bash
cd frontend
npm install
npm run build
npm run start -p 3000
```
Open **`http://localhost:3000`** in any web browser.

---

## 3. Running Test & Verification Suites

### Run Backend Unit & Integration Tests (33 Tests)
```bash
pytest
```

### Run Mathematical Optimality & Duality Proof
```bash
python scripts/verify_independent_optimality.py
```

### Run End-to-End Workflow Audit (14 Steps)
```bash
python scripts/verify_full_e2e_workflow.py
```

### Run PDF & CSV Parity Reconciliation
```bash
python scripts/verify_pdf_csv_reconciliation.py
```
