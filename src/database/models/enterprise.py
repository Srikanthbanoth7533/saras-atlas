"""
SARAS ATLAS — Enterprise Domain Models.
Organizations, Warehouses, Suppliers, and Sku-Supplier Relationships.
"""

from typing import List, Optional
from sqlalchemy import String, Numeric, Integer, Boolean, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base, TimestampMixin, generate_uuid


class Organization(Base, TimestampMixin):
    """Represents a merchant or enterprise tenant."""
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), default="America/Los_Angeles", nullable=False)
    is_synthetic: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    data_provenance: Mapped[Optional[str]] = mapped_column(String(64), default="SARAS_ATLAS_SYNTHETIC_BENCHMARK_V1", nullable=True)

    # Relationships
    warehouses: Mapped[List["Warehouse"]] = relationship("Warehouse", back_populates="organization", cascade="all, delete-orphan")
    suppliers: Mapped[List["Supplier"]] = relationship("Supplier", back_populates="organization", cascade="all, delete-orphan")
    products: Mapped[List["Product"]] = relationship("Product", back_populates="organization", cascade="all, delete-orphan")
    purchase_orders: Mapped[List["PurchaseOrder"]] = relationship("PurchaseOrder", back_populates="organization", cascade="all, delete-orphan")
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="organization", cascade="all, delete-orphan")
    scenarios: Mapped[List["Scenario"]] = relationship("Scenario", back_populates="organization", cascade="all, delete-orphan")


class Warehouse(Base, TimestampMixin):
    """Physical logistics node (3PL distribution center, central hub, retail location)."""
    __tablename__ = "warehouses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    org_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)  # e.g. WH-WEST-RENO
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    warehouse_type: Mapped[str] = mapped_column(String(32), default="3PL", nullable=False)  # 3PL, CENTRAL_HUB, RETAIL_STORE
    
    # Geographic Location
    street_address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(32), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(32), nullable=False)
    country: Mapped[str] = mapped_column(String(3), default="USA", nullable=False)
    latitude: Mapped[Optional[float]] = mapped_column(Numeric(10, 6), nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Numeric(10, 6), nullable=True)

    # Operational Capacity & Cost Parameters
    max_pallet_capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    daily_holding_cost_per_unit: Mapped[float] = mapped_column(Numeric(10, 4), default=0.0150, nullable=False)
    pick_pack_base_fee: Mapped[float] = mapped_column(Numeric(10, 2), default=4.50, nullable=False)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="warehouses")
    inventory_snapshots: Mapped[List["InventorySnapshot"]] = relationship("InventorySnapshot", back_populates="warehouse", cascade="all, delete-orphan")
    destination_pos: Mapped[List["PurchaseOrder"]] = relationship("PurchaseOrder", back_populates="destination_warehouse")
    fulfilled_orders: Mapped[List["Order"]] = relationship("Order", back_populates="fulfilling_warehouse")


class Supplier(Base, TimestampMixin):
    """Manufacturing facility, overseas factory, or primary vendor."""
    __tablename__ = "suppliers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    org_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    vendor_code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)  # e.g. VEND-SHENZHEN-01
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    origin_country: Mapped[str] = mapped_column(String(3), nullable=False)  # CHN, VNM, IND, USA
    origin_port: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)  # Yantian, Haiphong
    
    # Lead Times & Reliability
    standard_lead_time_days: Mapped[int] = mapped_column(Integer, nullable=False)
    expedited_air_lead_time_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    reliability_score: Mapped[float] = mapped_column(Numeric(5, 4), default=0.9200, nullable=False)
    payment_terms: Mapped[str] = mapped_column(String(64), default="Net 60", nullable=False)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="suppliers")
    sku_mappings: Mapped[List["SkuSupplierMap"]] = relationship("SkuSupplierMap", back_populates="supplier", cascade="all, delete-orphan")
    purchase_orders: Mapped[List["PurchaseOrder"]] = relationship("PurchaseOrder", back_populates="supplier")


class SkuSupplierMap(Base, TimestampMixin):
    """Many-to-many relationship linking SKUs with primary and backup suppliers."""
    __tablename__ = "sku_supplier_maps"
    __table_args__ = (
        UniqueConstraint("sku_id", "supplier_id", name="uq_sku_supplier"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    sku_id: Mapped[str] = mapped_column(String(36), ForeignKey("skus.id", ondelete="CASCADE"), nullable=False, index=True)
    supplier_id: Mapped[str] = mapped_column(String(36), ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=False, index=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Economic & Order Parameters
    supplier_unit_cost: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)  # Contracted FOB cost
    minimum_order_qty: Mapped[int] = mapped_column(Integer, default=500, nullable=False)
    inbound_freight_cost_ocean: Mapped[float] = mapped_column(Numeric(10, 2), default=6.00, nullable=False)
    inbound_freight_cost_air: Mapped[float] = mapped_column(Numeric(10, 2), default=14.50, nullable=False)
    lead_time_days: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    sku: Mapped["Sku"] = relationship("Sku", back_populates="supplier_mappings")
    supplier: Mapped["Supplier"] = relationship("Supplier", back_populates="sku_mappings")
