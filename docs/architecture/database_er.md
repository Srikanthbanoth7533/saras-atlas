# SARAS ATLAS — Database Entity-Relationship (ER) Architecture

## 1. Overview
SARAS ATLAS utilizes an embedded relational storage architecture powered by **SQLite 3** operating in **Write-Ahead Logging (WAL)** mode. This design provides atomic, ACID-compliant transactions, foreign key integrity, and non-blocking concurrent reads with zero operational hosting overhead.

---

## 2. Entity-Relationship (ER) Diagram

```mermaid
erDiagram
    organizations ||--o{ warehouses : "operates"
    organizations ||--o{ suppliers : "contracts"
    organizations ||--o{ products : "owns"
    organizations ||--o{ customers : "serves"
    organizations ||--o{ purchase_orders : "issues"
    organizations ||--o{ orders : "fulfills"
    organizations ||--o{ scenarios : "configures"

    products ||--o{ skus : "categorizes"

    skus ||--o{ sku_supplier_maps : "sourced_from"
    suppliers ||--o{ sku_supplier_maps : "supplies"

    warehouses ||--o{ inventory_snapshots : "stocks"
    skus ||--o{ inventory_snapshots : "counted_in"

    suppliers ||--o{ purchase_orders : "fulfills"
    warehouses ||--o{ purchase_orders : "receives"
    purchase_orders ||--o{ purchase_order_lines : "contains"
    skus ||--o{ purchase_order_lines : "itemizes"

    customers ||--o{ orders : "places"
    warehouses ||--o{ orders : "fulfills_from"
    orders ||--o{ order_lines : "contains"
    skus ||--o{ order_lines : "itemizes"

    scenarios ||--o{ scenario_params : "defines"
    scenarios ||--o{ simulation_runs : "generates"
    simulation_runs ||--o{ recommendations : "produces"
    recommendations ||--o{ approval_records : "governed_by"

    organizations {
        uuid id PK
        string name
        string currency
        string timezone
        boolean is_synthetic
        string data_provenance
    }

    warehouses {
        uuid id PK
        uuid org_id FK
        string code
        string name
        string warehouse_type
        decimal latitude
        decimal longitude
        integer max_pallet_capacity
        decimal pick_pack_base_fee
    }

    suppliers {
        uuid id PK
        uuid org_id FK
        string vendor_code
        string name
        string origin_country
        integer standard_lead_time_days
        integer expedited_air_lead_time_days
        decimal reliability_score
    }

    skus {
        uuid id PK
        uuid product_id FK
        string sku_code
        string size
        string color
        decimal retail_price
        decimal base_cogs
        decimal inbound_tariff_rate
        decimal payment_processing_fee_rate
        decimal target_margin_rate
    }

    purchase_orders {
        uuid id PK
        uuid org_id FK
        string po_number
        uuid supplier_id FK
        uuid destination_warehouse_id FK
        string status
        string transport_mode
        string vessel_name
        date departure_date
        date scheduled_arrival_date
        integer delay_days
    }

    orders {
        uuid id PK
        uuid org_id FK
        string order_number
        uuid customer_id FK
        string destination_zone
        decimal gross_revenue
        decimal net_revenue
        uuid fulfilling_warehouse_id FK
        decimal outbound_shipping_cost
        decimal allocated_ad_spend
        decimal contribution_margin
    }

    inventory_snapshots {
        uuid id PK
        date snapshot_date
        uuid sku_id FK
        uuid warehouse_id FK
        integer qty_on_hand
        integer qty_reserved
        integer qty_available
        integer qty_in_transit
        integer safety_stock_threshold
        decimal days_of_coverage
    }

    simulation_runs {
        uuid id PK
        uuid scenario_id FK
        integer execution_duration_ms
        integer horizon_days
        decimal total_projected_revenue
        decimal total_projected_cogs
        decimal total_projected_freight
        decimal total_projected_contribution_margin
        decimal projected_margin_rate
        decimal total_lost_revenue_stockouts
        integer stockout_days_count
        decimal working_capital_required
    }

    recommendations {
        uuid id PK
        uuid simulation_run_id FK
        string recommendation_type
        text action_payload
        decimal estimated_margin_saved
        decimal estimated_capital_required
        string status
    }

    approval_records {
        uuid id PK
        uuid recommendation_id FK
        string approver_user_id
        string role
        string decision
        text comments
        string digital_signature_hash
    }
```

---

## 3. Database Engine Configuration
- **Journal Mode**: `WAL` (Write-Ahead Logging) allows concurrent reads without locking writer transactions.
- **Synchronous Flag**: `NORMAL` maximizes write throughput while guaranteeing crash consistency.
- **Cache Size**: `-64000` (64 MB page cache) ensures high-velocity index lookups during 90-day simulation cycles.
- **Foreign Key Constraints**: `PRAGMA foreign_keys = ON;` strictly enforced across all 17 tables.
