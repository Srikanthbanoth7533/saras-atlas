"""
SARAS ATLAS — Unit Tests for Digital Twin State & Operational Risk Sentinels.
"""

import pytest
from src.database.session import SessionLocal
from src.domain.twin.state import DigitalTwinState
from src.domain.twin.sentinels import OperationalRiskSentinel


@pytest.fixture
def twin_fixture():
    """Initializes digital twin state from active database session."""
    with SessionLocal() as session:
        twin = DigitalTwinState(session=session, org_id="org_vanguard_01")
        yield twin


def test_digital_twin_topology_and_graph(twin_fixture):
    """Verify in-memory NetworkX graph loads correctly."""
    topology = twin_fixture.get_topology()
    assert topology["total_nodes"] == 5  # 3 warehouses + 2 suppliers
    assert topology["total_edges"] >= 3  # Active maritime POs

    # Verify warehouse status flags
    wh_reno = next(n for n in topology["nodes"] if n["id"] == "wh_reno_01")
    assert wh_reno["status"] == "CRITICAL_STOCKOUT_RISK"
    assert wh_reno["lat"] == 39.5296


def test_digital_twin_inventory_summary(twin_fixture):
    """Verify aggregated inventory summary returns all 50 SKUs."""
    summary = twin_fixture.get_inventory_summary()
    assert len(summary) == 50

    # Verify Hero SKU status
    hero_item = next(item for item in summary if "APEX-JKT" in item["sku_code"])
    assert hero_item["total_on_hand"] > 0
    assert hero_item["retail_price"] == 180.00
    assert hero_item["status"] in ["CRITICAL_STOCKOUT", "AT_RISK", "HEALTHY"]


def test_risk_sentinel_detections(twin_fixture):
    """Verify risk sentinels detect PO-9012 port delay and cross-zone penalty."""
    sentinel = OperationalRiskSentinel(twin_fixture)
    active_risks = sentinel.detect_active_risks()

    assert len(active_risks) >= 3

    po_risk = next(r for r in active_risks if r["risk_type"] == "SUPPLIER_INBOUND_DELAY")
    assert po_risk["severity"] == "CRITICAL"
    assert po_risk["delay_days"] == 21
    assert "PO-9012" in po_risk["title"]
    assert len(po_risk["vulnerable_skus"]) > 0

    cz_risk = next(r for r in active_risks if r["risk_type"] == "OUT_OF_ZONE_EXPEDITED_DRAIN")
    assert cz_risk["severity"] == "CRITICAL"
    assert cz_risk["cost_delta_per_unit"] == 13.00

