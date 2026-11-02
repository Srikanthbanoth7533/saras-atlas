"""
SARAS ATLAS — Unit Tests for Multi-Echelon Simulation Engine & Numerical Accounting Precision.
"""

import pytest
from src.database.session import SessionLocal
from src.domain.twin.state import DigitalTwinState
from src.domain.simulation.accounting import calculate_unit_contribution_margin
from src.domain.simulation.engine import SimulationEngine
from src.domain.simulation.models import (
    SimulationRequest,
    ShocksConfig,
    MitigationsConfig,
    SupplierDelayShock,
    FreightSurchargeShock,
    DemandSurgeShock,
)


def test_gaap_unit_contribution_margin_precision():
    """Verify exact GAAP accounting waterfall down to the penny."""
    res = calculate_unit_contribution_margin(
        retail_price=180.00,
        base_cogs=42.00,
        inbound_tariff_rate=0.0750,      # $3.15
        pick_pack_fee=4.50,
        outbound_shipping_cost=8.50,     # Zone 2 local ground
        payment_fee_rate=0.0290,         # ($180 * 0.029) + $0.30 = $5.52
        allocated_ad_spend=45.00,
        discount=0.00
    )
    assert res["net_revenue"] == 180.00
    assert res["tariffs"] == 3.15
    assert res["landed_cogs"] == 45.15
    assert res["payment_processing_fee"] == 5.52
    assert res["total_variable_costs"] == 108.67
    assert res["contribution_margin_dollars"] == 71.33
    assert abs(res["contribution_margin_percentage"] - 0.3963) < 0.0001


def test_simulation_unmitigated_flagship_disruption():
    """Verify unmitigated tri-disruption cascade creates stockouts and margin collapse."""
    with SessionLocal() as session:
        twin = DigitalTwinState(session=session)

    engine = SimulationEngine(twin)

    # Disruption: PO-9012 delayed 21d + East Coast Surcharge +28% + Viral Surge +45%
    req = SimulationRequest(
        scenario_name="Unmitigated Disruption Test",
        horizon_days=90,
        shocks=ShocksConfig(
            supplier_delays=[SupplierDelayShock(po_number="PO-9012", delay_days=21)],
            freight_surcharges=[FreightSurchargeShock(lane_id="lane_east_coast_parcel", surcharge_percentage=0.28)],
            demand_elasticities=[DemandSurgeShock(sku_code="APEX-JKT", demand_multiplier=1.45, duration_days=30)]
        ),
        mitigations=MitigationsConfig()
    )

    resp = engine.run_simulation(req)

    # Verify execution speed
    assert resp.execution_duration_ms < 200

    # Verify stockout days occur in unmitigated cascade
    assert resp.summary_scorecard.stockout_days >= 8
    assert resp.summary_scorecard.unfulfilled_lost_orders > 0

    # Verify narrative detects operational alert
    assert "OPERATIONAL ALERT" in resp.executive_narrative


def test_simulation_mitigated_flagship_resolution():
    """Verify that applying the optimal mitigation eliminates stockouts and protects margin."""
    with SessionLocal() as session:
        twin = DigitalTwinState(session=session)

    engine = SimulationEngine(twin)

    # Same disruption, but with mitigation: Air-freight 1500 + Transfer 600 + Ad Throttle 18%
    req = SimulationRequest(
        scenario_name="Mitigated Optimal Plan Test",
        horizon_days=90,
        shocks=ShocksConfig(
            supplier_delays=[SupplierDelayShock(po_number="PO-9012", delay_days=21)],
            freight_surcharges=[FreightSurchargeShock(lane_id="lane_east_coast_parcel", surcharge_percentage=0.28)],
            demand_elasticities=[DemandSurgeShock(sku_code="APEX-JKT", demand_multiplier=1.45, duration_days=30)]
        ),
        mitigations=MitigationsConfig(
            emergency_air_freight_units=1500,
            inter_warehouse_transfer_units=600,
            ad_spend_throttle_percentage=0.18
        )
    )

    resp = engine.run_simulation(req)

    # Assert stockouts are completely eliminated
    assert resp.summary_scorecard.stockout_days == 0
    assert resp.summary_scorecard.unfulfilled_lost_orders == 0

    # Assert contribution margin is preserved and healthy
    assert resp.summary_scorecard.contribution_margin_pct >= 0.28
    assert resp.summary_scorecard.net_contribution_margin > 400000.00

    # Assert narrative reflects resilience achieved
    assert "RESILIENCE ACHIEVED" in resp.executive_narrative
