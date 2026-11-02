"""
SARAS ATLAS — Digital Twin State Manager.
Maintains in-memory network graph (NetworkX) and multi-echelon inventory state.
"""

from typing import Dict, List, Any, Optional
import networkx as nx
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import (
    Warehouse,
    Supplier,
    Product,
    Sku,
    InventorySnapshot,
    PurchaseOrder,
)


class DigitalTwinState:
    """In-memory multi-echelon business digital twin representation."""

    def __init__(self, session: Session, org_id: str = "org_vanguard_01"):
        self.session = session
        self.org_id = org_id
        self.graph = nx.MultiDiGraph()
        self.warehouses: Dict[str, Dict[str, Any]] = {}
        self.suppliers: Dict[str, Dict[str, Any]] = {}
        self.skus: Dict[str, Dict[str, Any]] = {}
        self.inventory: Dict[str, Dict[str, Dict[str, int]]] = {}  # sku_id -> wh_id -> buckets
        self.purchase_orders: List[Dict[str, Any]] = []
        self._load_from_database()

    def _load_from_database(self) -> None:
        """Loads state from SQLite database into memory graph."""
        # 1. Load Warehouses
        wh_rows = self.session.execute(select(Warehouse).where(Warehouse.org_id == self.org_id)).scalars().all()
        for wh in wh_rows:
            wh_dict = {
                "id": wh.id,
                "code": wh.code,
                "name": wh.name,
                "type": wh.warehouse_type,
                "city": wh.city,
                "state": wh.state,
                "postal_code": wh.postal_code,
                "lat": float(wh.latitude) if wh.latitude else 0.0,
                "lng": float(wh.longitude) if wh.longitude else 0.0,
                "pick_pack_fee": float(wh.pick_pack_base_fee),
                "holding_cost_daily": float(wh.daily_holding_cost_per_unit)
            }
            self.warehouses[wh.id] = wh_dict
            self.graph.add_node(wh.id, node_type="WAREHOUSE", **wh_dict)

        # 2. Load Suppliers
        supp_rows = self.session.execute(select(Supplier).where(Supplier.org_id == self.org_id)).scalars().all()
        for supp in supp_rows:
            supp_dict = {
                "id": supp.id,
                "vendor_code": supp.vendor_code,
                "name": supp.name,
                "country": supp.origin_country,
                "origin_port": supp.origin_port,
                "standard_lead_time": supp.standard_lead_time_days,
                "expedited_air_lead_time": supp.expedited_air_lead_time_days or 8,
                "reliability": float(supp.reliability_score)
            }
            self.suppliers[supp.id] = supp_dict
            self.graph.add_node(supp.id, node_type="SUPPLIER", **supp_dict)

        # 3. Load SKUs
        sku_rows = self.session.execute(select(Sku)).scalars().all()
        for s in sku_rows:
            self.skus[s.id] = {
                "id": s.id,
                "sku_code": s.sku_code,
                "product_title": s.product.title if s.product else "Product",
                "category": s.product.category if s.product else "General",
                "retail_price": float(s.retail_price),
                "base_cogs": float(s.base_cogs),
                "tariff_rate": float(s.inbound_tariff_rate),
                "payment_fee_rate": float(s.payment_processing_fee_rate),
                "target_margin_rate": float(s.target_margin_rate),
                "weight_kg": float(s.weight_kg)
            }

        # 4. Load Inventory Snapshots
        inv_rows = self.session.execute(select(InventorySnapshot)).scalars().all()
        for snap in inv_rows:
            if snap.sku_id not in self.inventory:
                self.inventory[snap.sku_id] = {}
            self.inventory[snap.sku_id][snap.warehouse_id] = {
                "on_hand": snap.qty_on_hand,
                "reserved": snap.qty_reserved,
                "available": snap.qty_available,
                "in_transit": snap.qty_in_transit,
                "backordered": snap.qty_backordered,
                "doc": float(snap.days_of_coverage) if snap.days_of_coverage else 0.0
            }

        # 5. Load Active Purchase Orders
        po_rows = self.session.execute(select(PurchaseOrder).where(PurchaseOrder.org_id == self.org_id)).scalars().all()
        for po in po_rows:
            po_dict = {
                "id": po.id,
                "po_number": po.po_number,
                "supplier_id": po.supplier_id,
                "destination_warehouse_id": po.destination_warehouse_id,
                "status": po.status,
                "mode": po.transport_mode,
                "vessel": po.vessel_name,
                "scheduled_arrival": str(po.scheduled_arrival_date),
                "revised_arrival": str(po.revised_arrival_date),
                "delay_days": po.delay_days,
                "freight_total": float(po.inbound_freight_total),
                "lines": [
                    {"sku_id": line.sku_id, "qty": line.qty_ordered, "unit_price": float(line.unit_price)}
                    for line in po.lines
                ]
            }
            self.purchase_orders.append(po_dict)
            
            # Add transit edge to graph
            self.graph.add_edge(
                po.supplier_id,
                po.destination_warehouse_id,
                key=po.po_number,
                mode=po.transport_mode,
                delay_days=po.delay_days,
                status=po.status
            )

    def get_topology(self) -> Dict[str, Any]:
        """Returns JSON-serializable network topology representation for visualization."""
        nodes = []
        for n_id, data in self.graph.nodes(data=True):
            node_type = data.get("node_type", "UNKNOWN")
            node_info = {
                "id": n_id,
                "type": node_type,
                "name": data.get("name", n_id),
                "code": data.get("code") or data.get("vendor_code"),
                "lat": data.get("lat", 0.0),
                "lng": data.get("lng", 0.0),
                "status": "NORMAL"
            }
            # Check if warehouse has delayed inbound shipments
            if node_type == "WAREHOUSE":
                has_delay = any(
                    po["destination_warehouse_id"] == n_id and po["delay_days"] > 0
                    for po in self.purchase_orders
                )
                if has_delay:
                    node_info["status"] = "CRITICAL_STOCKOUT_RISK"
            nodes.append(node_info)

        edges = []
        for u, v, k, data in self.graph.edges(keys=True, data=True):
            edges.append({
                "from_node": u,
                "to_node": v,
                "key": k,
                "mode": data.get("mode", "OCEAN"),
                "delay_days": data.get("delay_days", 0),
                "status": data.get("status", "IN_TRANSIT")
            })

        return {
            "organization": {
                "id": self.org_id,
                "name": "Vanguard Apparel Co.",
                "slug": "vanguard-apparel-co"
            },
            "organization_id": self.org_id,
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "nodes": nodes,
            "edges": edges
        }

    def get_inventory_summary(self) -> List[Dict[str, Any]]:
        """Returns aggregated stock summary per SKU across the network."""
        summary = []
        for sku_id, sku_info in self.skus.items():
            wh_stocks = self.inventory.get(sku_id, {})
            tot_on_hand = sum(s["on_hand"] for s in wh_stocks.values())
            tot_reserved = sum(s["reserved"] for s in wh_stocks.values())
            tot_available = sum(s["available"] for s in wh_stocks.values())
            tot_in_transit = sum(s["in_transit"] for s in wh_stocks.values())
            min_doc = min((s["doc"] for s in wh_stocks.values()), default=0.0)

            status = "HEALTHY"
            if min_doc < 10.0:
                status = "CRITICAL_STOCKOUT"
            elif min_doc < 21.0:
                status = "AT_RISK"

            summary.append({
                "sku_id": sku_id,
                "sku_code": sku_info["sku_code"],
                "product_title": sku_info["product_title"],
                "category": sku_info["category"],
                "retail_price": sku_info["retail_price"],
                "total_on_hand": tot_on_hand,
                "total_reserved": tot_reserved,
                "total_available": tot_available,
                "total_in_transit": tot_in_transit,
                "min_days_of_coverage": min_doc,
                "status": status,
                "warehouse_breakdown": wh_stocks
            })
        return summary
