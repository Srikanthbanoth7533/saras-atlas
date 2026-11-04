# SARAS ATLAS — Synthetic Benchmark Dataset Documentation

## 1. Provenance & Synthetic Disclaimer
All enterprise parameters, customer orders, vendor contracts, inventory records, and financial ledger entries in SARAS ATLAS represent a **synthetic, mathematically calibrated benchmark dataset**.
- **Enterprise Entity**: Vanguard Apparel Co.
- **Commercial Scale**: \$45.0M Annual Gross Merchandise Value (GMV).
- **Privacy & Compliance**: Contains **zero real customer data**, zero real personally identifiable information (PII), and zero confidential vendor pricing.
- **Affiliation**: Independent portfolio engineering demonstration; not affiliated with, sponsored by, or endorsed by Saras Analytics.

---

## 2. Enterprise Network Topology

### 2.1 Distribution Facilities (Fulfillment Nodes)
| Warehouse Code | Facility Name | Location | Capacity | Inbound Transit Role | Pick & Pack Fee |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`WH-WEST`** | Pacific Gateway 3PL | Reno / Los Angeles, NV/CA | 50,000 pallets | Primary Pacific Ocean Port-of-Entry | \$4.50 / unit |
| **`WH-CENTRAL`** | Heartland Logistics Hub | Dallas / Fort Worth, TX | 40,000 pallets | Regional Cross-Dock & Sourcing | \$4.25 / unit |
| **`WH-EAST`** | Liberty Corridor DC | Allentown, PA | 60,000 pallets | East Coast Parcel Hub (Origin Safety Stock) | \$4.75 / unit |

### 2.2 Global Supplier Fabricators
| Vendor Code | Supplier Name | Origin | Transit Mode | Standard Lead Time | Expedited Lead Time | MOQ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`SUP-CN-01`** | Pacific Garments Ltd | Shenzhen, China | Ocean Freight | 18 – 24 Days | — | 1,000 units |
| **`SUP-VN-02`** | Saigon Performance Wear | Saigon, Vietnam | Air Freight | 14 Days | 3 – 5 Days (Air) | 500 units |
| **`SUP-BD-03`** | Bengal Tex Works | Dhaka, Bangladesh | Ocean Freight | 28 – 35 Days | — | 2,000 units |
| **`SUP-PT-04`** | Porto Knits SA | Porto, Portugal | Air / Ocean | 10 – 16 Days | — | 300 units |

---

## 3. Flagship Hero SKU: Apex Shell Jacket (`APEX-JKT`)

### 3.1 Unit Economics (GAAP Baseline Waterfall)
| Component | Unit Rate | % of Gross | Accounting Category |
| :--- | :--- | :--- | :--- |
| **Gross Retail Price** | **\$180.00** | 100.00% | Gross Revenue |
| Factory FOB Manufacturing Cost | -\$42.00 | -23.33% | Inbound Landed COGS |
| US Import Tariffs (Section 301 - 7.5%) | -\$3.15 | -1.75% | Inbound Landed COGS |
| Standard 3PL Pick & Pack Contract Fee | -\$4.50 | -2.50% | Variable Fulfillment |
| Local Outbound Parcel (Zone 2) | -\$8.50 | -4.72% | Outbound Freight |
| Merchant Payment Processing (2.9% + \$0.30) | -\$5.52 | -3.07% | Operating Expense |
| Blended Customer Acquisition Cost (CAC) | -\$45.00 | -25.00% | Allocated Paid Marketing |
| **Net Unit Contribution Margin** | **\$71.33** | **39.63%** | **GAAP Net Margin** |

### 3.2 Disrupted Unit Economics (Zone 8 Out-of-Zone Surcharge)
When WH-WEST runs dry and stock is shipped across the country from Allentown with a +28% spot surcharge:
- Shipping fee increases to **\$21.50** (\$16.80 Zone 8 baseline + \$4.70 surcharge).
- Net unit contribution margin drops to **\$58.33 (32.40%)**, representing an **18.2% margin contraction**.

---

## 4. The Compound Disruption Benchmark (`DISR-PO9012`)

### 4.1 Shock Parameters
1. **Upstream Ocean Delay**: Container vessel `Ever Forward` carrying PO-9012 (10,000 units of APEX-JKT) is held at Shenzhen outer anchorage for **21 days**, extending arrival from Day 18 to Day 39.
2. **Carrier Surcharge**: Outbound parcel carrier applies an emergency **+28% fuel and capacity surcharge** on East Coast lanes.
3. **Viral Social Surge**: Viral marketing visibility triggers an unexpected **+45% demand elasticity spike** for 30 consecutive days.

### 4.2 Financial Loss Reconciliation
- **Gross Commercial Revenue Exposed**: **\$224,500.00** across 1,968 unfulfilled demand units.
- **Unincurred Variable Savings**: **-\$94,655.68** (unincurred factory production and local shipping).
- **Net Contribution Margin Erosion**: **-\$129,844.32** (actual GAAP gross profit lost).
