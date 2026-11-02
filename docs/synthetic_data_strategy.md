# SYNTHETIC DATA STRATEGY & BENCHMARK DATASET SPECIFICATION

**Document ID:** DATA-SYNTH-001  
**Version:** 1.0.0  
**Phase:** Phase 0 Baseline  
**Author:** Senior Data Engineer & AI/ML Research Engineer  

---

## 1. Objectives & Provenance Guardrails

SARAS ATLAS requires a high-fidelity benchmark dataset to stress-test multi-echelon disruption propagation, mixed-integer optimization, and executive situation room visualization.

To maintain strict ethical boundaries and protect customer confidentiality:
1. **Zero Access to Private Data:** The platform uses **100% synthetic, algorithmically generated data**. It contains no private, proprietary, or customer data from Saras Analytics or any real-world commercial brand.
2. **Deterministic Reproducibility:** All pseudorandom generation is strictly seeded (`seed = 42`), ensuring that every simulation run, unit test, and benchmark produces identical, verifiable numbers.
3. **Mandatory Provenance Metadata:** Every generated record contains explicit metadata fields:
   - `is_synthetic = TRUE`
   - `data_provenance = 'SARAS_ATLAS_SYNTHETIC_BENCHMARK_V1'`
   - `generation_seed = 42`

---

## 2. Benchmark Merchant Profile: "Vanguard Apparel Co."

To mirror the complex operational profile of high-growth omnichannel brands ($10M–$250M GMV), we model **Vanguard Apparel Co.**:

```
+---------------------------------------------------------------------------------+
|                         VANGUARD APPAREL CO. TOPOLOGY                           |
|                                                                                 |
|   SUPPLIERS:                                                                    |
|   1. Shenzhen Premier Garments (China) - Primary FOB Factory (45-day lead time) |
|   2. Mekong Performance Textiles (Vietnam) - Expedited Backup (8-day air lead)  |
|                                                                                 |
|   TRANSIT PIPELINE:                                                             |
|   - Ocean Lane: Yantian -> Long Beach Port -> Rail to West Coast 3PL            |
|   - Air Lane: Tan Son Nhat -> Los Angeles (LAX) / Newark (EWR)                  |
|                                                                                 |
|   FULFILLMENT NETWORK:                                                          |
|   1. Node West: Reno, NV 3PL (45% National Orders, West Coast / Pacific)        |
|   2. Node East: Allentown, PA 3PL (40% National Orders, Mid-Atlantic / East)    |
|   3. Node Central: Dallas, TX 3PL (15% National Orders, Midwest / South)        |
|                                                                                 |
|   COMMERCIAL SCALE:                                                             |
|   - 50 SKUs across Technical Outerwear and Activewear                           |
|   - $45M Annualized Gross Revenue (~250,000 units/year)                         |
|   - 180 Days of Continuous Historical Hourly Transactions (~37,500 orders)      |
+---------------------------------------------------------------------------------+
```

---

## 3. Product Catalog & Unit Economics Hierarchy

The synthetic catalog models 50 active SKUs across two distinct operational velocity tiers:

### 3.1 Tier 1: High-Velocity Hero Products (80% of Volume, 10 SKUs)
- **Flagship SKU:** `APEX-JKT-BLK` (*Apex Technical All-Weather Jacket*, Sizes XS–XXL)
- **Retail Selling Price (RSP):** $180.00
- **Supplier FOB Cost:** $42.00
- **Ocean Inbound Freight:** $6.00 / unit
- **Customs Tariffs (US Harmonized Tariff Schedule):** 7.5% of FOB = $3.15
- **3PL Inbound Receiving Fee:** $0.75 / unit
- **3PL Storage Holding Cost:** $0.015 / unit / day
- **3PL Outbound Pick & Pack Fee:** $4.50 / order
- **Payment Processing (Stripe / Shopify):** 2.9% + $0.30 = $5.52
- **Allocated Ad Spend (Target CAC):** $45.00
- **Baseline Unit Contribution Margin (Zone 2 Local Parcel @ $8.50):**
  $$\text{CM} = \$180.00 - (\$42.00 + \$6.00 + \$3.15 + \$0.75 + \$4.50 + \$5.52 + \$45.00 + \$8.50) = \$64.58 \quad (35.88\%)$$

### 3.2 Tier 2: Core Activewear & Accessories (20% of Volume, 40 SKUs)
- Lightweight technical tees, fleece mid-layers, and running tights.
- RSP ranging from $48.00 to $95.00.
- Supplier FOB costs ranging from $11.00 to $24.00.
- Standard contribution margins between 28% and 42%.

---

## 4. Synthetic Demand & Order Generation Model

Order arrival times and geographic distribution are generated using realistic physical probability distributions rather than uniform noise:

### 4.1 Temporal Arrival Process (Non-Homogeneous Poisson Process)
Order arrival rate $\lambda(t)$ at hour $t$ is modeled as:
$$\lambda(t) = \bar{\lambda} \cdot S_{\text{day}}(t) \cdot S_{\text{week}}(t) \cdot M_{\text{marketing}}(t)$$
Where:
- $\bar{\lambda}$ = Base hourly rate (approximately 8.5 orders/hour).
- $S_{\text{day}}(t)$ = Diurnal cycle modeled via harmonic Fourier terms peaking at 14:00 and 20:00 local time.
- $S_{\text{week}}(t)$ = Day-of-week multiplier (peaking Sunday evening at 1.25x; troughing Tuesday at 0.85x).
- $M_{\text{marketing}}(t)$ = Marketing promotion shocks (viral TikTok surge = 1.45x multiplier).

### 4.2 Geographic & Carrier Zone Routing Matrix
Orders are probabilistically assigned to US ZIP codes weighted by census population density:
- **Zone Allocation Logic:**
  - West Coast orders (ZIPs 90000–99999): Assigned to Reno 3PL (Carrier Zones 2–3, base parcel $8.50).
  - East Coast orders (ZIPs 01000–29999): Assigned to Allentown 3PL (Carrier Zones 2–3, base parcel $8.50).
  - Central orders (ZIPs 30000–89999): Assigned to Dallas 3PL (Carrier Zones 2–4, base parcel $9.20).
- **Out-of-Zone Fallback Penalty:** When Reno stocks out, West Coast orders route to Allentown:
  - Transit mode transitions from Zone 2/3 Ground to **Carrier Zone 8 Cross-Country**.
  - Outbound shipping cost jumps from **$8.50 to $21.50 per unit** (+153% cost escalation).

---

## 5. Inbound Purchase Order Pipeline & Disruption Fixtures

The synthetic pipeline includes 6 active purchase orders on the water:

| PO Number | SKU Range | Total Units | Origin Port | Vessel Name | Destination 3PL | Scheduled Arrival | Injected Disruption Shock |
| :--- | :--- | :---: | :--- | :--- | :--- | :--- | :--- |
| **PO-9012** | `APEX-JKT-*` | 10,000 | Yantian (CHN) | *Ever Forward* | Reno, NV (West) | Day 6 | **DELAYED +21 DAYS (Port Congestion)** |
| **PO-9013** | `ACT-FLEECE-*`| 6,000 | Haiphong (VNM) | *CMA CGM Marco Polo*| Allentown, PA (East)| Day 14 | On Schedule (0 days) |
| **PO-9014** | `APEX-JKT-*` | 4,000 | Yantian (CHN) | *MSC Gulsun* | Dallas, TX (Central)| Day 28 | On Schedule (0 days) |
| **PO-9015** | `ACT-TEE-*` | 15,000 | Yantian (CHN) | *Cosco Shipping* | Reno, NV (West) | Day 35 | Normal maritime variance (+2 days) |
| **PO-9016** | `APEX-JKT-*` | 5,000 | Haiphong (VNM) | *Maersk Mc-Kinney* | Allentown, PA (East)| Day 48 | On Schedule (0 days) |
| **PO-9017** | `ACT-TIGHTS-*`| 8,000 | Yantian (CHN) | *Ever Given* | Reno, NV (West) | Day 60 | On Schedule (0 days) |

---

## 6. Synthetic Data Generation Engine Architecture

The generator script is implemented in pure Python using NumPy and Pandas:

```python
# Synthetic Data Generator Architecture Overview (scripts/generate_synthetic_data.py)
import numpy as np
import pandas as pd

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

def generate_vanguard_dataset(output_dir: str):
    """
    Generates complete canonical relational tables:
    1. organizations.parquet / .sqlite
    2. warehouses.parquet
    3. suppliers.parquet
    4. skus.parquet
    5. purchase_orders.parquet
    6. inventory_snapshots.parquet
    7. orders_historical.parquet (180 days, ~37,500 rows)
    All tagged with synthetic_flag=True and seed=42.
    """
    pass
```

- **Storage Format:** Stored as both optimized Apache Parquet files (for sub-second DuckDB OLAP scans) and loaded into SQLite (for SQLAlchemy OLTP relational operations).
- **Disk Footprint:** Complete 180-day benchmark dataset consumes $< 25\text{ MB}$ compressed on disk.
- **Generation Time:** Generates in $< 3.5\text{ seconds}$ on the Intel Core i5 host processor.

