"""
SARAS ATLAS — Synthetic Data Loader & DuckDB Exporter.
Persists generated Vanguard benchmark datasets to SQLite (OLTP) and Parquet / DuckDB (OLAP).
"""

from pathlib import Path
from typing import Dict, Any
import duckdb
import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.config import settings
from src.database.session import SessionLocal, init_db, get_duckdb_connection
from src.database.models import (
    Organization,
    Warehouse,
    Supplier,
    Product,
    Sku,
    SkuSupplierMap,
    PurchaseOrder,
    PurchaseOrderLine,
    InventorySnapshot,
    Customer,
    Order,
    OrderLine,
)
from src.synthetic.generator import VanguardSyntheticGenerator


def persist_synthetic_dataset(data: Dict[str, Any], session: Session) -> Dict[str, int]:
    """
    Inserts generated synthetic entities into SQLite in transactional batches.
    Returns row counts per table.
    """
    counts = {}

    # 1. Organization
    org_obj = Organization(**data["organization"])
    session.add(org_obj)
    session.flush()
    counts["organizations"] = 1

    # 2. Warehouses & Suppliers
    session.bulk_insert_mappings(Warehouse, data["warehouses"])
    session.bulk_insert_mappings(Supplier, data["suppliers"])
    session.flush()
    counts["warehouses"] = len(data["warehouses"])
    counts["suppliers"] = len(data["suppliers"])

    # 3. Products & SKUs
    session.bulk_insert_mappings(Product, data["products"])
    session.bulk_insert_mappings(Sku, data["skus"])
    session.flush()
    counts["products"] = len(data["products"])
    counts["skus"] = len(data["skus"])

    # 4. Sku Supplier Maps
    session.bulk_insert_mappings(SkuSupplierMap, data["sku_supplier_maps"])
    session.flush()
    counts["sku_supplier_maps"] = len(data["sku_supplier_maps"])

    # 5. Purchase Orders & Lines
    session.bulk_insert_mappings(PurchaseOrder, data["purchase_orders"])
    session.bulk_insert_mappings(PurchaseOrderLine, data["po_lines"])
    session.flush()
    counts["purchase_orders"] = len(data["purchase_orders"])
    counts["po_lines"] = len(data["po_lines"])

    # 6. Inventory Snapshots
    session.bulk_insert_mappings(InventorySnapshot, data["inventory_snapshots"])
    session.flush()
    counts["inventory_snapshots"] = len(data["inventory_snapshots"])

    # 7. Customers
    session.bulk_insert_mappings(Customer, data["customers"])
    session.flush()
    counts["customers"] = len(data["customers"])

    # 8. Orders & Order Lines (Chunked for memory safety on 8GB host)
    chunk_size = 5000
    for i in range(0, len(data["orders"]), chunk_size):
        session.bulk_insert_mappings(Order, data["orders"][i:i+chunk_size])
    for i in range(0, len(data["order_lines"]), chunk_size):
        session.bulk_insert_mappings(OrderLine, data["order_lines"][i:i+chunk_size])
    
    session.commit()
    counts["orders"] = len(data["orders"])
    counts["order_lines"] = len(data["order_lines"])

    return counts


def export_to_parquet_and_duckdb(data: Dict[str, Any], output_dir: Path) -> None:
    """
    Exports synthetic tabular data to compressed Parquet files and loads into embedded DuckDB
    using DuckDB's native high-performance C++ Parquet engine (zero pyarrow dependency).
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    duckdb_conn = get_duckdb_connection()

    for table_name in ["skus", "warehouses", "suppliers", "inventory_snapshots", "purchase_orders", "orders"]:
        df = pd.DataFrame(data[table_name])
        parquet_file = output_dir / f"{table_name}.parquet"
        
        # Register Pandas DataFrame in DuckDB and write Parquet natively
        duckdb_conn.register("temp_df", df)
        duckdb_conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM temp_df;")
        duckdb_conn.execute(f"COPY {table_name} TO '{parquet_file.as_posix()}' (FORMAT PARQUET);")
        duckdb_conn.unregister("temp_df")

    duckdb_conn.close()


def seed_database(num_days: int = 180) -> Dict[str, int]:
    """
    Orchestrates end-to-end benchmark data generation and loading.
    """
    init_db()
    generator = VanguardSyntheticGenerator(seed=settings.SYNTHETIC_SEED)
    data = generator.generate_all(num_days=num_days)

    with SessionLocal() as session:
        # Check if already seeded to prevent duplicate key violations
        existing = session.execute(text("SELECT count(*) FROM organizations WHERE id = 'org_vanguard_01'")).scalar()
        if existing and existing > 0:
            print("[INFO] Vanguard benchmark dataset already seeded. Skipping reload.")
            return {"status": "ALREADY_SEEDED"}

        row_counts = persist_synthetic_dataset(data, session)

    parquet_dir = settings.DATA_DIR / "parquet"
    export_to_parquet_and_duckdb(data, parquet_dir)

    return row_counts


if __name__ == "__main__":
    print("[INFO] Seeding SARAS ATLAS benchmark dataset...")
    counts = seed_database()
    print("[SUCCESS] Seeded row counts:", counts)
