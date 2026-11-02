"""
SARAS ATLAS — Canonical Schema Definitions & Header Aliases.
Registry of target entities, data types, and fuzzy column matching patterns.
"""

from typing import Dict, List
from src.domain.ingestion.models import IngestionEntity, CanonicalSchemaField


CANONICAL_SCHEMAS: Dict[IngestionEntity, List[CanonicalSchemaField]] = {
    IngestionEntity.INVENTORY_SNAPSHOT: [
        CanonicalSchemaField(
            field_name="sku_code",
            data_type="string",
            required=True,
            description="Unique SKU product identifier",
            aliases=["sku", "sku_id", "item_code", "item_id", "product_code", "material"],
        ),
        CanonicalSchemaField(
            field_name="warehouse_code",
            data_type="string",
            required=True,
            description="Target fulfillment center or warehouse node code",
            aliases=["warehouse", "warehouse_id", "location", "facility", "whse", "site", "node"],
        ),
        CanonicalSchemaField(
            field_name="units_on_hand",
            data_type="integer",
            required=True,
            description="Physically present unreserved inventory count",
            aliases=["on_hand", "quantity", "qty", "stock", "units", "current_stock", "qoh", "inventory"],
        ),
        CanonicalSchemaField(
            field_name="units_allocated",
            data_type="integer",
            required=False,
            description="Inventory reserved for pending unfulfilled orders",
            aliases=["allocated", "reserved", "committed", "held"],
        ),
        CanonicalSchemaField(
            field_name="units_in_transit",
            data_type="integer",
            required=False,
            description="Inventory in transit inbound from suppliers or transfer lanes",
            aliases=["in_transit", "on_order", "incoming", "pipeline", "open_po_units"],
        ),
        CanonicalSchemaField(
            field_name="safety_stock_threshold",
            data_type="integer",
            required=False,
            description="Minimum inventory buffer threshold before reorder triggers",
            aliases=["safety_stock", "min_stock", "reorder_point", "threshold", "buffer"],
        ),
    ],
    IngestionEntity.PURCHASE_ORDER: [
        CanonicalSchemaField(
            field_name="po_number",
            data_type="string",
            required=True,
            description="Purchase order identifier (e.g. PO-9012)",
            aliases=["po", "po_id", "order_number", "purchase_order_id", "doc_number"],
        ),
        CanonicalSchemaField(
            field_name="supplier_code",
            data_type="string",
            required=True,
            description="Vendor or manufacturing partner identifier",
            aliases=["supplier", "supplier_id", "vendor", "vendor_id", "factory", "manufacturer"],
        ),
        CanonicalSchemaField(
            field_name="destination_warehouse_code",
            data_type="string",
            required=True,
            description="Destination port or warehouse node",
            aliases=["destination", "dest_warehouse", "warehouse", "delivery_location", "whse"],
        ),
        CanonicalSchemaField(
            field_name="sku_code",
            data_type="string",
            required=True,
            description="Ordered SKU identifier",
            aliases=["sku", "sku_id", "item_code", "item_id", "product_code"],
        ),
        CanonicalSchemaField(
            field_name="units_ordered",
            data_type="integer",
            required=True,
            description="Total units committed on the purchase order",
            aliases=["units", "quantity", "qty", "ordered_qty", "order_quantity"],
        ),
        CanonicalSchemaField(
            field_name="unit_cost",
            data_type="float",
            required=True,
            description="Landed unit cost of goods from supplier ($)",
            aliases=["unit_cost", "cogs", "cost", "unit_price", "purchase_price"],
        ),
        CanonicalSchemaField(
            field_name="status",
            data_type="string",
            required=False,
            description="Current logistics lifecycle status",
            aliases=["status", "po_status", "lifecycle", "state"],
        ),
    ],
    IngestionEntity.SKU_CATALOG: [
        CanonicalSchemaField(
            field_name="sku_code",
            data_type="string",
            required=True,
            description="Unique SKU product code",
            aliases=["sku", "sku_id", "item_code", "product_code"],
        ),
        CanonicalSchemaField(
            field_name="product_name",
            data_type="string",
            required=True,
            description="Public merchandise product title",
            aliases=["name", "title", "product_title", "description", "item_name"],
        ),
        CanonicalSchemaField(
            field_name="category",
            data_type="string",
            required=False,
            description="Product merchandising department/category",
            aliases=["category", "dept", "department", "collection", "family"],
        ),
        CanonicalSchemaField(
            field_name="unit_retail_price",
            data_type="float",
            required=True,
            description="Target Net Retail MSRP ($)",
            aliases=["price", "retail_price", "msrp", "unit_price", "selling_price"],
        ),
        CanonicalSchemaField(
            field_name="standard_unit_cost",
            data_type="float",
            required=True,
            description="Standard landed manufacturing unit COGS ($)",
            aliases=["cogs", "standard_cost", "cost", "unit_cost"],
        ),
        CanonicalSchemaField(
            field_name="velocity_tier",
            data_type="string",
            required=False,
            description="ABC velocity categorization tier (e.g. A, B, C)",
            aliases=["velocity", "tier", "abc_tier", "sales_velocity"],
        ),
    ],
    IngestionEntity.SALES_ORDER: [
        CanonicalSchemaField(
            field_name="order_id",
            data_type="string",
            required=True,
            description="DTC eCommerce order identifier",
            aliases=["order_id", "order_number", "order_no", "invoice", "transaction_id"],
        ),
        CanonicalSchemaField(
            field_name="customer_id",
            data_type="string",
            required=False,
            description="Buyer or account identifier",
            aliases=["customer", "customer_id", "buyer_id", "user_id"],
        ),
        CanonicalSchemaField(
            field_name="order_date",
            data_type="string",
            required=True,
            description="Order placement date timestamp",
            aliases=["date", "order_date", "created_at", "order_timestamp", "time"],
        ),
        CanonicalSchemaField(
            field_name="gross_revenue",
            data_type="float",
            required=True,
            description="Total gross customer payment amount ($)",
            aliases=["total", "amount", "revenue", "order_total", "gross_amount"],
        ),
        CanonicalSchemaField(
            field_name="status",
            data_type="string",
            required=False,
            description="Fulfillment completion status",
            aliases=["status", "fulfillment_status", "order_status"],
        ),
    ],
}


def suggest_column_mapping(detected_columns: List[str], target_entity: IngestionEntity) -> Dict[str, str]:
    """
    Fuzzy header matching mapping detected source columns to canonical ATLAS attributes.
    Performs priority exact matching first, followed by substring matching, enforcing 1-to-1 mappings.
    """
    schema = CANONICAL_SCHEMAS.get(target_entity, [])
    mapping: Dict[str, str] = {}
    assigned_canonicals = set()

    # Pass 1: Exact matches (exact field name or exact alias)
    for col in detected_columns:
        norm_col = col.strip().lower().replace(" ", "_").replace("-", "_")
        for field in schema:
            if field.field_name in assigned_canonicals:
                continue
            if norm_col == field.field_name.lower() or any(norm_col == a.lower() for a in field.aliases):
                mapping[col] = field.field_name
                assigned_canonicals.add(field.field_name)
                break

    # Pass 2: Substring matches for remaining unmapped columns
    for col in detected_columns:
        if col in mapping:
            continue
        norm_col = col.strip().lower().replace(" ", "_").replace("-", "_")
        for field in schema:
            if field.field_name in assigned_canonicals:
                continue
            if any(a.lower() in norm_col for a in field.aliases if len(a) >= 4):
                mapping[col] = field.field_name
                assigned_canonicals.add(field.field_name)
                break

    return mapping
