"""
SARAS ATLAS — Unit Tests for SQLAlchemy 2.0 Models & SQLite Integrity.
"""

from datetime import date, datetime, timezone
import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker

from src.database.base import Base
from src.database.models import (
    Organization,
    Warehouse,
    Supplier,
    Product,
    Sku,
    SkuSupplierMap,
    InventorySnapshot,
    PurchaseOrder,
    PurchaseOrderLine,
    Customer,
    Order,
    OrderLine,
    Scenario,
    ScenarioParam,
    SimulationRun,
    Recommendation,
    ApprovalRecord,
)


@pytest.fixture
def test_db():
    """In-memory SQLite test database fixture."""
    engine = create_engine(
        "sqlite:///:memory:",
        echo=False,
        connect_args={"check_same_thread": False}
    )
    with engine.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys=ON;"))
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def test_enterprise_and_catalog_hierarchy(test_db):
    """Verify Organization, Warehouse, Supplier, Product, and SKU relationships."""
    org = Organization(name="Vanguard Apparel Co.", currency="USD")
    test_db.add(org)
    test_db.commit()

    wh_reno = Warehouse(
        org_id=org.id,
        code="WH-WEST-RENO",
        name="West Coast 3PL (Reno, NV)",
        city="Reno",
        state="NV",
        postal_code="89501",
        country="USA",
        daily_holding_cost_per_unit=0.0150,
        pick_pack_base_fee=4.50
    )
    test_db.add(wh_reno)

    supplier_china = Supplier(
        org_id=org.id,
        vendor_code="VEND-SHENZHEN-01",
        name="Shenzhen Premier Garments",
        origin_country="CHN",
        origin_port="Yantian",
        standard_lead_time_days=45,
        expedited_air_lead_time_days=8
    )
    test_db.add(supplier_china)

    product = Product(org_id=org.id, title="Apex All-Weather Jacket", category="Technical Outerwear")
    test_db.add(product)
    test_db.commit()

    sku = Sku(
        product_id=product.id,
        sku_code="APEX-JKT-BLK-M",
        size="M",
        color="Black",
        retail_price=180.00,
        base_cogs=42.00,
        inbound_tariff_rate=0.0750,
        payment_processing_fee_rate=0.0290,
        target_margin_rate=0.3500
    )
    test_db.add(sku)
    test_db.commit()

    # Link SKU with Supplier via Mapping
    mapping = SkuSupplierMap(
        sku_id=sku.id,
        supplier_id=supplier_china.id,
        is_primary=True,
        supplier_unit_cost=42.00,
        minimum_order_qty=500,
        inbound_freight_cost_ocean=6.00,
        inbound_freight_cost_air=14.50,
        lead_time_days=45
    )
    test_db.add(mapping)
    test_db.commit()

    # Queries & Verifications
    fetched_org = test_db.execute(select(Organization).where(Organization.name == "Vanguard Apparel Co.")).scalar_one()
    assert len(fetched_org.warehouses) == 1
    assert fetched_org.warehouses[0].code == "WH-WEST-RENO"
    assert len(fetched_org.suppliers) == 1
    assert fetched_org.suppliers[0].vendor_code == "VEND-SHENZHEN-01"

    fetched_sku = test_db.execute(select(Sku).where(Sku.sku_code == "APEX-JKT-BLK-M")).scalar_one()
    assert fetched_sku.product.title == "Apex All-Weather Jacket"
    assert fetched_sku.retail_price == 180.00
    assert fetched_sku.supplier_mappings[0].supplier.origin_country == "CHN"


def test_inventory_and_purchase_order_flow(test_db):
    """Verify Inventory Snapshots and Inbound Purchase Order delay tracking."""
    org = Organization(name="Vanguard Apparel Co.")
    test_db.add(org)
    test_db.commit()

    wh = Warehouse(org_id=org.id, code="WH-EAST-ALLENTOWN", name="East 3PL", city="Allentown", state="PA", postal_code="18101")
    supplier = Supplier(org_id=org.id, vendor_code="VEND-VN-02", name="Mekong Textiles", origin_country="VNM", standard_lead_time_days=30)
    prod = Product(org_id=org.id, title="Active Tech Tee", category="Activewear")
    test_db.add_all([wh, supplier, prod])
    test_db.commit()

    sku = Sku(product_id=prod.id, sku_code="ACT-TEE-NAVY-L", retail_price=48.00, base_cogs=12.00)
    test_db.add(sku)
    test_db.commit()

    # Inventory Snapshot
    snap = InventorySnapshot(
        snapshot_date=date(2026, 11, 2),
        sku_id=sku.id,
        warehouse_id=wh.id,
        qty_on_hand=1200,
        qty_reserved=200,
        qty_available=1000,
        qty_in_transit=3000,
        safety_stock_threshold=150,
        days_of_coverage=24.5
    )
    test_db.add(snap)

    # Inbound PO with 21-day delay
    po = PurchaseOrder(
        org_id=org.id,
        po_number="PO-9012",
        supplier_id=supplier.id,
        destination_warehouse_id=wh.id,
        status="PORT_CONGESTION",
        transport_mode="OCEAN",
        vessel_name="Ever Forward",
        scheduled_arrival_date=date(2026, 11, 8),
        revised_arrival_date=date(2026, 11, 29),
        delay_days=21,
        inbound_freight_total=18000.00
    )
    test_db.add(po)
    test_db.commit()

    po_line = PurchaseOrderLine(purchase_order_id=po.id, sku_id=sku.id, qty_ordered=3000, unit_price=12.00, line_total=36000.00)
    test_db.add(po_line)
    test_db.commit()

    fetched_po = test_db.execute(select(PurchaseOrder).where(PurchaseOrder.po_number == "PO-9012")).scalar_one()
    assert fetched_po.delay_days == 21
    assert fetched_po.status == "PORT_CONGESTION"
    assert len(fetched_po.lines) == 1
    assert fetched_po.lines[0].qty_ordered == 3000


def test_scenario_and_governance_records(test_db):
    """Verify Scenario branching, simulation output run, and cryptographic approval."""
    org = Organization(name="Vanguard Apparel Co.")
    test_db.add(org)
    test_db.commit()

    scenario = Scenario(
        org_id=org.id,
        name="Tri-Disruption Test Scenario",
        scenario_type="DISRUPTION"
    )
    test_db.add(scenario)
    test_db.commit()

    param1 = ScenarioParam(scenario_id=scenario.id, param_key="SUPPLIER_DELAY_DAYS", param_value=21.0, target_entity_id="PO-9012")
    param2 = ScenarioParam(scenario_id=scenario.id, param_key="FREIGHT_SURCHARGE_PCT", param_value=0.28, target_entity_id="EAST_COAST_LANE")
    test_db.add_all([param1, param2])
    test_db.commit()

    sim_run = SimulationRun(
        scenario_id=scenario.id,
        execution_duration_ms=88,
        horizon_days=90,
        total_projected_revenue=1425600.00,
        total_projected_cogs=412500.00,
        total_projected_freight=182400.00,
        total_projected_contribution_margin=461800.00,
        projected_margin_rate=0.3239,
        total_lost_revenue_stockouts=142000.00,
        stockout_days_count=9,
        working_capital_required=35000.00
    )
    test_db.add(sim_run)
    test_db.commit()

    rec = Recommendation(
        simulation_run_id=sim_run.id,
        recommendation_type="MILP_GLOBAL_OPTIMAL",
        action_payload={"air_units": 1500, "transfer_units": 600, "ad_throttle": 0.18},
        estimated_margin_saved=241800.00,
        estimated_capital_required=20670.00,
        status="APPROVED"
    )
    test_db.add(rec)
    test_db.commit()

    approval = ApprovalRecord(
        recommendation_id=rec.id,
        approver_user_id="usr_coo_sarah",
        role="COO",
        decision="APPROVED",
        digital_signature_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    test_db.add(approval)
    test_db.commit()

    fetched_rec = test_db.execute(select(Recommendation).where(Recommendation.id == rec.id)).scalar_one()
    assert fetched_rec.estimated_margin_saved == 241800.00
    assert fetched_rec.approvals[0].role == "COO"
    assert fetched_rec.approvals[0].digital_signature_hash.startswith("e3b0c4")

