"""
SARAS ATLAS — Integration Tests for Synthetic Benchmark Data Generation & DuckDB Export.
"""

from pathlib import Path
import pytest
from src.synthetic.generator import VanguardSyntheticGenerator
from src.synthetic.loader import persist_synthetic_dataset, export_to_parquet_and_duckdb
from src.database.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import duckdb


def test_synthetic_generator_deterministic_fidelity():
    """Verify generator is 100% deterministic given seed=42."""
    gen1 = VanguardSyntheticGenerator(seed=42)
    data1 = gen1.generate_all(num_days=30)

    gen2 = VanguardSyntheticGenerator(seed=42)
    data2 = gen2.generate_all(num_days=30)

    # Assert exact entity counts
    assert len(data1["skus"]) == 50
    assert len(data2["skus"]) == 50
    assert len(data1["warehouses"]) == 3
    assert len(data1["suppliers"]) == 2
    assert len(data1["orders"]) == len(data2["orders"])

    # Assert exact revenue equality
    rev1 = sum(o["net_revenue"] for o in data1["orders"])
    rev2 = sum(o["net_revenue"] for o in data2["orders"])
    assert rev1 == rev2

    # Assert Flagship PO-9012 exists and has 21-day delay
    po_disrupted = next(po for po in data1["purchase_orders"] if po["po_number"] == "PO-9012")
    assert po_disrupted["delay_days"] == 21
    assert po_disrupted["status"] == "PORT_CONGESTION"
    assert po_disrupted["vessel_name"] == "Ever Forward"


def test_synthetic_persistence_and_duckdb(tmp_path):
    """Verify bulk loading into SQLite and Parquet/DuckDB OLAP scanning."""
    # SQLite test engine
    db_file = tmp_path / "test_atlas.db"
    engine = create_engine(f"sqlite:///{db_file.as_posix()}", echo=False)
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine)

    # Generate small dataset (14 days, ~3,000 orders)
    gen = VanguardSyntheticGenerator(seed=42)
    data = gen.generate_all(num_days=14)

    with TestingSession() as session:
        counts = persist_synthetic_dataset(data, session)
        assert counts["skus"] == 50
        assert counts["warehouses"] == 3
        assert counts["orders"] == len(data["orders"])

    # Parquet & DuckDB export
    parquet_dir = tmp_path / "parquet"
    duckdb_file = tmp_path / "analytics.duckdb"
    
    # Custom export to temporary duckdb using native DuckDB engine
    parquet_dir.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(duckdb_file.as_posix())
    for t_name in ["skus", "warehouses", "orders"]:
        import pandas as pd
        df = pd.DataFrame(data[t_name])
        p_path = parquet_dir / f"{t_name}.parquet"
        conn.register("tmp_df", df)
        conn.execute(f"CREATE TABLE {t_name} AS SELECT * FROM tmp_df;")
        conn.execute(f"COPY {t_name} TO '{p_path.as_posix()}' (FORMAT PARQUET);")
        conn.unregister("tmp_df")

    res = conn.execute("SELECT count(*), round(sum(gross_revenue), 2) FROM orders;").fetchone()
    conn.close()

    assert res[0] == len(data["orders"])
    assert res[1] > 0
