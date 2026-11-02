"""
SARAS ATLAS — Inventory & Inbound Supply Domain Models.
Inventory Snapshots, Multi-Echelon Stock Levels, and Purchase Orders.
"""

from datetime import date
from typing import List, Optional
from sqlalchemy import String, Numeric, Integer, Date, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base, TimestampMixin, generate_uuid


class InventorySnapshot(Base, TimestampMixin):
    """Daily multi-echelon stock levels for a specific SKU at a warehouse node."""
    __tablename__ = "inventory_snapshots"
    __table_args__ = (
        UniqueConstraint("snapshot_date", "sku_id", "warehouse_id", name="uq_inv_snap"),
        Index("idx_inv_snap_lookup", "snapshot_date", "sku_id", "warehouse_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    sku_id: Mapped[str] = mapped_column(String(36), ForeignKey("skus.id", ondelete="CASCADE"), nullable=False, index=True)
    warehouse_id: Mapped[str] = mapped_column(String(36), ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 4 Distinct Inventory Buckets
    qty_on_hand: Mapped[int] = mapped_column(Integer, default=0, nullable=False)        # Physical in facility
    qty_reserved: Mapped[int] = mapped_column(Integer, default=0, nullable=False)       # Committed to open orders
    qty_available: Mapped[int] = mapped_column(Integer, default=0, nullable=False)      # On-Hand - Reserved
    qty_in_transit: Mapped[int] = mapped_column(Integer, default=0, nullable=False)     # Inbound POs on water/air
    qty_backordered: Mapped[int] = mapped_column(Integer, default=0, nullable=False)    # Unfulfilled demand
    
    safety_stock_threshold: Mapped[int] = mapped_column(Integer, default=150, nullable=False)
    days_of_coverage: Mapped[Optional[float]] = mapped_column(Numeric(8, 2), nullable=True)

    # Relationships
    sku: Mapped["Sku"] = relationship("Sku", back_populates="inventory_snapshots")
    warehouse: Mapped["Warehouse"] = relationship("Warehouse", back_populates="inventory_snapshots")


class PurchaseOrder(Base, TimestampMixin):
    """Inbound purchase order tracking overseas transit pipelines."""
    __tablename__ = "purchase_orders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    org_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    po_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)  # e.g. PO-9012
    supplier_id: Mapped[str] = mapped_column(String(36), ForeignKey("suppliers.id"), nullable=False, index=True)
    destination_warehouse_id: Mapped[str] = mapped_column(String(36), ForeignKey("warehouses.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), default="PLANNED", nullable=False, index=True)  # PLANNED, IN_TRANSIT, PORT_CONGESTION, RECEIVED
    transport_mode: Mapped[str] = mapped_column(String(32), default="OCEAN", nullable=False)  # OCEAN, AIR, TRUCK
    
    # Transit Telemetry
    tracking_number: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    vessel_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)  # e.g. Ever Forward
    port_of_entry: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)  # e.g. Long Beach
    departure_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    scheduled_arrival_date: Mapped[date] = mapped_column(Date, nullable=False)
    revised_arrival_date: Mapped[date] = mapped_column(Date, nullable=False)
    actual_arrival_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    delay_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    inbound_freight_total: Mapped[float] = mapped_column(Numeric(12, 2), default=0.00, nullable=False)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="purchase_orders")
    supplier: Mapped["Supplier"] = relationship("Supplier", back_populates="purchase_orders")
    destination_warehouse: Mapped["Warehouse"] = relationship("Warehouse", back_populates="destination_pos")
    lines: Mapped[List["PurchaseOrderLine"]] = relationship("PurchaseOrderLine", back_populates="purchase_order", cascade="all, delete-orphan")


class PurchaseOrderLine(Base, TimestampMixin):
    """Line items for inbound purchase orders."""
    __tablename__ = "purchase_order_lines"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    purchase_order_id: Mapped[str] = mapped_column(String(36), ForeignKey("purchase_orders.id", ondelete="CASCADE"), nullable=False, index=True)
    sku_id: Mapped[str] = mapped_column(String(36), ForeignKey("skus.id"), nullable=False, index=True)
    qty_ordered: Mapped[int] = mapped_column(Integer, nullable=False)
    qty_received: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    line_total: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    # Relationships
    purchase_order: Mapped["PurchaseOrder"] = relationship("PurchaseOrder", back_populates="lines")
    sku: Mapped["Sku"] = relationship("Sku", back_populates="po_lines")

