"""
SARAS ATLAS — Deterministic Synthetic Benchmark Generator.
Generates Vanguard Apparel Co. ($45M GMV) multi-echelon supply chain topology,
50 SKUs, 3 warehouses, 2 overseas suppliers, maritime POs, and 180 days of orders.
Seeded with seed=42 for 100% mathematical reproducibility.
"""

from datetime import date, datetime, timedelta, timezone
from typing import Dict, List, Any
import numpy as np
import pandas as pd

from src.database.base import generate_uuid

# Strict Reproducibility Seed
RANDOM_SEED = 42

# Carrier Zone Pricing Lookup (Origin Warehouse -> Customer State -> Parcel Cost)
# In US parcel shipping, local ground is Zone 2-3 (~$8.50), cross-country is Zone 8 ($21.50)
WEST_STATES = {"CA", "OR", "WA", "NV", "AZ", "UT", "ID", "MT", "WY", "CO", "NM"}
EAST_STATES = {"NY", "NJ", "PA", "MA", "CT", "RI", "VT", "NH", "ME", "MD", "VA", "NC", "SC", "GA", "FL", "DC"}
CENTRAL_STATES = {"TX", "IL", "OH", "MI", "IN", "WI", "MO", "TN", "AL", "MS", "LA", "AR", "OK", "KS", "NE", "IA", "MN", "ND", "SD"}


def get_carrier_zone(warehouse_code: str, dest_state: str) -> int:
    """Calculate parcel carrier zone (1 to 8) based on warehouse origin and customer destination."""
    if "WEST" in warehouse_code:
        if dest_state in WEST_STATES:
            return 2
        elif dest_state in CENTRAL_STATES:
            return 5
        else:
            return 8  # Cross-country to East Coast
    elif "EAST" in warehouse_code:
        if dest_state in EAST_STATES:
            return 2
        elif dest_state in CENTRAL_STATES:
            return 5
        else:
            return 8  # Cross-country to West Coast
    else:  # CENTRAL
        if dest_state in CENTRAL_STATES:
            return 3
        elif dest_state in EAST_STATES:
            return 5
        else:
            return 6


def get_parcel_shipping_cost(zone: int, surcharge_rate: float = 0.0) -> float:
    """Calculates outbound shipping cost based on carrier zone and optional congestion surcharge."""
    base_rates = {
        1: 7.20,
        2: 8.50,
        3: 8.80,
        4: 10.50,
        5: 12.20,
        6: 14.80,
        7: 17.50,
        8: 21.50
    }
    cost = base_rates.get(zone, 12.50)
    return round(cost * (1.0 + surcharge_rate), 2)


class VanguardSyntheticGenerator:
    """Deterministic generator for Vanguard Apparel Co. benchmark dataset."""

    def __init__(self, seed: int = RANDOM_SEED):
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    def generate_all(self, start_date: date = date(2026, 5, 6), num_days: int = 180) -> Dict[str, Any]:
        """Generates all synthetic entities matching the Phase 0 specification."""
        self.rng = np.random.default_rng(self.seed)

        # 1. Organization
        org = {
            "id": "org_vanguard_01",
            "name": "Vanguard Apparel Co.",
            "currency": "USD",
            "timezone": "America/Los_Angeles",
            "is_synthetic": True,
            "data_provenance": "SARAS_ATLAS_SYNTHETIC_BENCHMARK_V1"
        }

        # 2. Warehouses (3 Regional Distribution Nodes)
        warehouses = [
            {
                "id": "wh_reno_01",
                "org_id": org["id"],
                "code": "WH-WEST-RENO",
                "name": "West Coast 3PL (Reno, NV)",
                "warehouse_type": "3PL",
                "city": "Reno",
                "state": "NV",
                "postal_code": "89501",
                "country": "USA",
                "latitude": 39.5296,
                "longitude": -119.8138,
                "max_pallet_capacity": 5000,
                "daily_holding_cost_per_unit": 0.0150,
                "pick_pack_base_fee": 4.50
            },
            {
                "id": "wh_allentown_02",
                "org_id": org["id"],
                "code": "WH-EAST-ALLENTOWN",
                "name": "East Coast 3PL (Allentown, PA)",
                "warehouse_type": "3PL",
                "city": "Allentown",
                "state": "PA",
                "postal_code": "18101",
                "country": "USA",
                "latitude": 40.6084,
                "longitude": -75.4902,
                "max_pallet_capacity": 4500,
                "daily_holding_cost_per_unit": 0.0160,
                "pick_pack_base_fee": 4.75
            },
            {
                "id": "wh_dallas_03",
                "org_id": org["id"],
                "code": "WH-CENTRAL-DALLAS",
                "name": "Central Hub (Dallas, TX)",
                "warehouse_type": "CENTRAL_HUB",
                "city": "Dallas",
                "state": "TX",
                "postal_code": "75201",
                "country": "USA",
                "latitude": 32.7767,
                "longitude": -96.7970,
                "max_pallet_capacity": 3000,
                "daily_holding_cost_per_unit": 0.0140,
                "pick_pack_base_fee": 4.25
            }
        ]

        # 3. Suppliers (2 Primary Overseas Factories)
        suppliers = [
            {
                "id": "supp_shenzhen_01",
                "org_id": org["id"],
                "vendor_code": "VEND-SHENZHEN-01",
                "name": "Shenzhen Premier Garments",
                "origin_country": "CHN",
                "origin_port": "Yantian",
                "standard_lead_time_days": 45,
                "expedited_air_lead_time_days": 8,
                "reliability_score": 0.9400,
                "payment_terms": "Net 60"
            },
            {
                "id": "supp_vietnam_02",
                "org_id": org["id"],
                "vendor_code": "VEND-VIETNAM-02",
                "name": "Mekong Performance Textiles",
                "origin_country": "VNM",
                "origin_port": "Haiphong",
                "standard_lead_time_days": 30,
                "expedited_air_lead_time_days": 7,
                "reliability_score": 0.9100,
                "payment_terms": "Net 45"
            }
        ]

        # 4. Products & 50 SKUs Hierarchy
        products = [
            {"id": "prod_apex_jkt", "org_id": org["id"], "title": "Apex Technical All-Weather Jacket", "category": "Technical Outerwear"},
            {"id": "prod_storm_parka", "org_id": org["id"], "title": "StormGuard Expedition Parka", "category": "Technical Outerwear"},
            {"id": "prod_tech_tee", "org_id": org["id"], "title": "AeroVent Seamless Tech Tee", "category": "Activewear"},
            {"id": "prod_trail_pant", "org_id": org["id"], "title": "CrossTerrain Alpine Pant", "category": "Activewear"},
            {"id": "prod_fleece_hoodie", "org_id": org["id"], "title": "Polaris Grid-Fleece Midlayer", "category": "Activewear"}
        ]

        skus = []
        sku_supplier_maps = []
        sizes = ["XS", "S", "M", "L", "XL", "XXL"]
        colors = ["Black", "Slate Gray", "Navy Blue", "Olive Green"]

        sku_counter = 1
        for prod in products:
            p_cat = prod["category"]
            if p_cat == "Technical Outerwear":
                base_price = 180.00 if "Apex" in prod["title"] else 240.00
                base_cogs = 42.00 if "Apex" in prod["title"] else 58.00
                weight = 0.650
            else:
                base_price = 48.00 if "Tee" in prod["title"] else (110.00 if "Pant" in prod["title"] else 88.00)
                base_cogs = 12.00 if "Tee" in prod["title"] else (26.00 if "Pant" in prod["title"] else 22.00)
                weight = 0.280

            # Generate variants for each product to reach exactly 50 SKUs
            variant_limit = 10  # 5 products * 10 variants = 50 SKUs
            v_count = 0
            for sz in sizes:
                for col in colors:
                    if v_count >= variant_limit:
                        break
                    
                    code_prefix = "APEX-JKT" if "Apex" in prod["title"] else (
                        "STORM-PKA" if "Storm" in prod["title"] else (
                            "AERO-TEE" if "Tee" in prod["title"] else (
                                "TRL-PNT" if "Pant" in prod["title"] else "POLAR-FLC"
                            )
                        )
                    )
                    sku_code = f"{code_prefix}-{col[:3].upper()}-{sz}"
                    sku_id = f"sku_{sku_counter:03d}"

                    sku_item = {
                        "id": sku_id,
                        "product_id": prod["id"],
                        "sku_code": sku_code,
                        "barcode": f"8492010{sku_counter:04d}",
                        "size": sz,
                        "color": col,
                        "weight_kg": weight,
                        "retail_price": base_price,
                        "base_cogs": base_cogs,
                        "inbound_tariff_rate": 0.0750,
                        "payment_processing_fee_rate": 0.0290,
                        "target_margin_rate": 0.3500,
                        "status": "ACTIVE"
                    }
                    skus.append(sku_item)

                    # Map primary supplier (Shenzhen) and backup supplier (Vietnam)
                    sku_supplier_maps.append({
                        "id": f"map_{sku_counter:03d}_1",
                        "sku_id": sku_id,
                        "supplier_id": suppliers[0]["id"],
                        "is_primary": True,
                        "supplier_unit_cost": base_cogs,
                        "minimum_order_qty": 500,
                        "inbound_freight_cost_ocean": 6.00,
                        "inbound_freight_cost_air": 14.50,
                        "lead_time_days": 45
                    })
                    sku_supplier_maps.append({
                        "id": f"map_{sku_counter:03d}_2",
                        "sku_id": sku_id,
                        "supplier_id": suppliers[1]["id"],
                        "is_primary": False,
                        "supplier_unit_cost": round(base_cogs * 1.05, 2),  # 5% higher FOB
                        "minimum_order_qty": 300,
                        "inbound_freight_cost_ocean": 7.00,
                        "inbound_freight_cost_air": 12.50,
                        "lead_time_days": 30
                    })

                    sku_counter += 1
                    v_count += 1

        # 5. Inbound Purchase Orders (Including Flagship PO-9012 Disruption)
        purchase_orders = [
            {
                "id": "po_9012_disrupted",
                "org_id": org["id"],
                "po_number": "PO-9012",
                "supplier_id": suppliers[0]["id"],
                "destination_warehouse_id": warehouses[0]["id"],  # Reno
                "status": "PORT_CONGESTION",
                "transport_mode": "OCEAN",
                "vessel_name": "Ever Forward",
                "port_of_entry": "Long Beach",
                "departure_date": date(2026, 9, 20),
                "scheduled_arrival_date": date(2026, 11, 8),
                "revised_arrival_date": date(2026, 11, 29),  # +21 days delayed
                "actual_arrival_date": None,
                "delay_days": 21,
                "inbound_freight_total": 60000.00
            },
            {
                "id": "po_9013_normal",
                "org_id": org["id"],
                "po_number": "PO-9013",
                "supplier_id": suppliers[1]["id"],
                "destination_warehouse_id": warehouses[1]["id"],  # Allentown
                "status": "IN_TRANSIT",
                "transport_mode": "OCEAN",
                "vessel_name": "CMA CGM Marco Polo",
                "port_of_entry": "Newark",
                "departure_date": date(2026, 10, 1),
                "scheduled_arrival_date": date(2026, 11, 15),
                "revised_arrival_date": date(2026, 11, 15),
                "actual_arrival_date": None,
                "delay_days": 0,
                "inbound_freight_total": 36000.00
            },
            {
                "id": "po_9014_normal",
                "org_id": org["id"],
                "po_number": "PO-9014",
                "supplier_id": suppliers[0]["id"],
                "destination_warehouse_id": warehouses[2]["id"],  # Dallas
                "status": "IN_TRANSIT",
                "transport_mode": "OCEAN",
                "vessel_name": "MSC Gulsun",
                "port_of_entry": "Houston",
                "departure_date": date(2026, 10, 5),
                "scheduled_arrival_date": date(2026, 11, 28),
                "revised_arrival_date": date(2026, 11, 28),
                "actual_arrival_date": None,
                "delay_days": 0,
                "inbound_freight_total": 24000.00
            }
        ]

        # PO Lines (PO-9012 has 10,000 units of Apex Jackets across sizes)
        po_lines = []
        apex_skus = [s for s in skus if "APEX-JKT" in s["sku_code"]]
        units_per_sku = 10000 // len(apex_skus)
        for idx, s in enumerate(apex_skus):
            po_lines.append({
                "id": f"pol_9012_{idx+1}",
                "purchase_order_id": purchase_orders[0]["id"],
                "sku_id": s["id"],
                "qty_ordered": units_per_sku,
                "qty_received": 0,
                "unit_price": s["base_cogs"],
                "line_total": round(units_per_sku * s["base_cogs"], 2)
            })

        # 6. Current Inventory Snapshots (Multi-Echelon State)
        inventory_snapshots = []
        for s in skus:
            is_hero = "APEX-JKT" in s["sku_code"]
            # Hero SKU has tighter on-hand stock to demonstrate stockout vulnerability
            wh_stocks = {
                "wh_reno_01": 240 if is_hero else 650,       # 10 sizes * 240 = 2,400 hero units
                "wh_allentown_02": 210 if is_hero else 580,  # 10 sizes * 210 = 2,100 hero units
                "wh_dallas_03": 80 if is_hero else 300       # 10 sizes * 80 = 800 hero units
            }
            for wh_id, qty in wh_stocks.items():
                reserved = int(qty * 0.10)
                available = qty - reserved
                in_transit = 1000 if (wh_id == "wh_reno_01" and is_hero) else 0
                days_doc = round(available / 12.0, 1)  # est. 12 units/day per variant
                inventory_snapshots.append({
                    "id": f"inv_snap_{s['id']}_{wh_id}",
                    "snapshot_date": date(2026, 11, 2),
                    "sku_id": s["id"],
                    "warehouse_id": wh_id,
                    "qty_on_hand": qty,
                    "qty_reserved": reserved,
                    "qty_available": available,
                    "qty_in_transit": in_transit,
                    "qty_backordered": 0,
                    "safety_stock_threshold": 50,
                    "days_of_coverage": days_doc
                })

        # 7. Historical Orders (~37,500 orders across 180 days)
        # Using vectorized array creation for speed
        all_states = list(WEST_STATES) + list(EAST_STATES) + list(CENTRAL_STATES)
        # State distribution weights normalized
        raw_state_weights = [0.45 / len(WEST_STATES)] * len(WEST_STATES) + \
                            [0.40 / len(EAST_STATES)] * len(EAST_STATES) + \
                            [0.15 / len(CENTRAL_STATES)] * len(CENTRAL_STATES)
        state_weights = np.array(raw_state_weights, dtype=np.float64)
        state_weights = state_weights / state_weights.sum()

        num_orders = 37500
        chosen_states = self.rng.choice(all_states, size=num_orders, p=state_weights)
        
        # Date generation with seasonal weekend and evening peaks
        day_offsets = self.rng.integers(0, num_days, size=num_orders)
        hour_prob = np.array([
            0.01, 0.01, 0.01, 0.01, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.07,
            0.08, 0.08, 0.07, 0.06, 0.06, 0.06, 0.07, 0.06, 0.04, 0.03, 0.02, 0.01
        ], dtype=np.float64)
        hour_prob = hour_prob / hour_prob.sum()

        hour_offsets = self.rng.choice(np.arange(24), size=num_orders, p=hour_prob)
        
        order_dates = [
            datetime.combine(start_date + timedelta(days=int(d)), datetime.min.time(), tzinfo=timezone.utc) + timedelta(hours=int(h), minutes=int(self.rng.integers(0, 60)))
            for d, h in zip(day_offsets, hour_offsets)
        ]

        # SKU assignments (Hero SKUs account for 60% of order volume)
        hero_sku_ids = [s["id"] for s in apex_skus]
        other_sku_ids = [s["id"] for s in skus if s["id"] not in hero_sku_ids]
        sku_lookup = {s["id"]: s for s in skus}

        orders = []
        order_lines = []
        customers = []

        # Customer pool of 5,000 repeat buyers
        cust_ids = [f"cust_{i:04d}" for i in range(1, 5001)]
        cust_states = self.rng.choice(all_states, size=5000, p=state_weights)
        for cid, cs in zip(cust_ids, cust_states):
            customers.append({
                "id": cid,
                "org_id": org["id"],
                "email": f"{cid}@example.com",
                "state": cs,
                "postal_code": "90210" if cs == "CA" else ("10001" if cs == "NY" else "75001"),
                "country": "USA",
                "total_orders_count": 0,
                "lifetime_value": 0.0
            })

        for o_idx in range(num_orders):
            cid = cust_ids[o_idx % 5000]
            st = chosen_states[o_idx]
            o_date = order_dates[o_idx]
            order_id = f"ord_{o_idx+1:06d}"
            order_num = f"ORD-{100000 + o_idx + 1}"

            # Select SKU: 60% probability of Hero Apex Jacket
            if self.rng.random() < 0.60:
                chosen_sku_id = self.rng.choice(hero_sku_ids)
            else:
                chosen_sku_id = self.rng.choice(other_sku_ids)

            sku_data = sku_lookup[chosen_sku_id]
            qty = 1 if self.rng.random() < 0.88 else 2
            gross_rev = round(sku_data["retail_price"] * qty, 2)
            discount = 0.00 if self.rng.random() < 0.75 else round(gross_rev * 0.10, 2)
            net_rev = round(gross_rev - discount, 2)

            # Determine primary fulfillment warehouse based on geography
            if st in WEST_STATES:
                wh_id = "wh_reno_01"
                wh_code = "WH-WEST-RENO"
            elif st in EAST_STATES:
                wh_id = "wh_allentown_02"
                wh_code = "WH-EAST-ALLENTOWN"
            else:
                wh_id = "wh_dallas_03"
                wh_code = "WH-CENTRAL-DALLAS"

            zone = get_carrier_zone(wh_code, st)
            shipping_cost = get_parcel_shipping_cost(zone)
            ad_spend = 45.00 * qty if "APEX-JKT" in sku_data["sku_code"] else 12.00 * qty
            cogs = round(sku_data["base_cogs"] * qty, 2)
            tariffs = round(cogs * sku_data["inbound_tariff_rate"], 2)
            pick_pack = 4.50
            processing_fee = round(net_rev * sku_data["payment_processing_fee_rate"], 2)

            # Net Contribution Margin
            cm = round(net_rev - (cogs + tariffs + pick_pack + shipping_cost + processing_fee + ad_spend), 2)

            orders.append({
                "id": order_id,
                "org_id": org["id"],
                "order_number": order_num,
                "order_date": o_date,
                "customer_id": cid,
                "destination_state": st,
                "destination_postal_code": "90210" if st == "CA" else ("10001" if st == "NY" else "75001"),
                "destination_zone": zone,
                "order_channel": "SHOPIFY",
                "gross_revenue": gross_rev,
                "discounts_total": discount,
                "net_revenue": net_rev,
                "status": "FULFILLED",
                "fulfilling_warehouse_id": wh_id,
                "outbound_shipping_cost": shipping_cost,
                "allocated_ad_spend": ad_spend,
                "contribution_margin": cm
            })

            order_lines.append({
                "id": f"ord_line_{o_idx+1:06d}",
                "order_id": order_id,
                "sku_id": chosen_sku_id,
                "qty": qty,
                "unit_price": sku_data["retail_price"],
                "unit_cogs": sku_data["base_cogs"],
                "line_revenue": gross_rev
            })

        return {
            "organization": org,
            "warehouses": warehouses,
            "suppliers": suppliers,
            "products": products,
            "skus": skus,
            "sku_supplier_maps": sku_supplier_maps,
            "purchase_orders": purchase_orders,
            "po_lines": po_lines,
            "inventory_snapshots": inventory_snapshots,
            "customers": customers,
            "orders": orders,
            "order_lines": order_lines
        }
