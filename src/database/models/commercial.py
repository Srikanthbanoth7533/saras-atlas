"""
SARAS ATLAS — Commercial & Customer Demand Domain Models.
Customers, Orders, Order Lines, Carrier Zones, and Landed Contribution Margins.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Numeric, Integer, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base, TimestampMixin, generate_uuid


class Customer(Base, TimestampMixin):
    """Customer entity with geographic metadata for parcel zone modeling."""
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    org_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    state: Mapped[str] = mapped_column(String(32), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(32), nullable=False)
    country: Mapped[str] = mapped_column(String(3), default="USA", nullable=False)
    total_orders_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    lifetime_value: Mapped[float] = mapped_column(Numeric(12, 2), default=0.00, nullable=False)

    # Relationships
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="customer")


class Order(Base, TimestampMixin):
    """Customer order with exact shipping zone and contribution margin metrics."""
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    org_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    order_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)  # e.g. ORD-10821
    order_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    customer_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("customers.id"), nullable=True, index=True)
    
    # Destination & Carrier Zone Routing (USPS/FedEx Zone 1 through 8)
    destination_state: Mapped[str] = mapped_column(String(32), nullable=False)
    destination_postal_code: Mapped[str] = mapped_column(String(32), nullable=False)
    destination_zone: Mapped[int] = mapped_column(Integer, nullable=False)  # Carrier Zone 1 to 8
    order_channel: Mapped[str] = mapped_column(String(32), default="SHOPIFY", nullable=False)  # SHOPIFY, AMAZON, WHOLESALE
    
    # Financial Statement Per Order
    gross_revenue: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    discounts_total: Mapped[float] = mapped_column(Numeric(10, 2), default=0.00, nullable=False)
    net_revenue: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="FULFILLED", nullable=False)  # FULFILLED, SPLIT_FULFILLED, BACKORDERED
    
    # Fulfillment & Carrier Shipping Economics
    fulfilling_warehouse_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("warehouses.id"), nullable=True, index=True)
    outbound_shipping_cost: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)  # Ground local vs Zone 8 cross-zone
    allocated_ad_spend: Mapped[float] = mapped_column(Numeric(10, 2), default=0.00, nullable=False)  # Target CAC allocated
    contribution_margin: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)  # GAAP Unit CM

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="orders")
    customer: Mapped[Optional["Customer"]] = relationship("Customer", back_populates="orders")
    fulfilling_warehouse: Mapped[Optional["Warehouse"]] = relationship("Warehouse", back_populates="fulfilled_orders")
    lines: Mapped[List["OrderLine"]] = relationship("OrderLine", back_populates="order", cascade="all, delete-orphan")


class OrderLine(Base, TimestampMixin):
    """Line items for customer orders."""
    __tablename__ = "order_lines"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    order_id: Mapped[str] = mapped_column(String(36), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    sku_id: Mapped[str] = mapped_column(String(36), ForeignKey("skus.id"), nullable=False, index=True)
    qty: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    unit_cogs: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    line_revenue: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="lines")
    sku: Mapped["Sku"] = relationship("Sku", back_populates="order_lines")
