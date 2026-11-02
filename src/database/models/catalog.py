"""
SARAS ATLAS — Product Catalog Domain Models.
Product Families, SKUs, and Unit Economics.
"""

from typing import List, Optional
from sqlalchemy import String, Numeric, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base, TimestampMixin, generate_uuid


class Product(Base, TimestampMixin):
    """Product parent family (e.g. Apex All-Weather Jacket)."""
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    org_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g. Technical Outerwear, Activewear

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="products")
    skus: Mapped[List["Sku"]] = relationship("Sku", back_populates="product", cascade="all, delete-orphan")


class Sku(Base, TimestampMixin):
    """Stock Keeping Unit (SKU) with granular unit economics."""
    __tablename__ = "skus"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    product_id: Mapped[str] = mapped_column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    sku_code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)  # e.g. APEX-JKT-BLK-M
    barcode: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    size: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    color: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    weight_kg: Mapped[float] = mapped_column(Numeric(8, 3), default=0.500, nullable=False)
    
    # Financial Unit Economics (GAAP Baseline)
    retail_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    base_cogs: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    inbound_tariff_rate: Mapped[float] = mapped_column(Numeric(5, 4), default=0.0750, nullable=False)  # 7.5% duty
    payment_processing_fee_rate: Mapped[float] = mapped_column(Numeric(5, 4), default=0.0290, nullable=False)  # 2.9% Stripe
    target_margin_rate: Mapped[float] = mapped_column(Numeric(5, 4), default=0.3500, nullable=False)  # 35% target CM
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", nullable=False)

    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="skus")
    supplier_mappings: Mapped[List["SkuSupplierMap"]] = relationship("SkuSupplierMap", back_populates="sku", cascade="all, delete-orphan")
    inventory_snapshots: Mapped[List["InventorySnapshot"]] = relationship("InventorySnapshot", back_populates="sku", cascade="all, delete-orphan")
    po_lines: Mapped[List["PurchaseOrderLine"]] = relationship("PurchaseOrderLine", back_populates="sku")
    order_lines: Mapped[List["OrderLine"]] = relationship("OrderLine", back_populates="sku")

