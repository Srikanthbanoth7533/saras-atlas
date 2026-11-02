"""
SARAS ATLAS — Enterprise Ingestion & Data Quality Router.
Endpoints for CSV/Excel upload preview, schema mapping, transactional commit,
safe rollback, and data quality health monitoring.
"""

from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import PlainTextResponse

from src.domain.ingestion.models import (
    IngestionEntity,
    IngestionPreviewResponse,
    IngestionCommitRequest,
    IngestionCommitResponse,
    RollbackRequest,
    RollbackResponse,
    DataQualityReport,
)
from src.domain.ingestion.validator import IngestionValidator
from src.domain.ingestion.pipeline import IngestionPipeline


router = APIRouter(prefix="/ingestion", tags=["Enterprise Data Ingestion"])


@router.post("/preview", response_model=IngestionPreviewResponse)
async def preview_uploaded_dataset(
    file: UploadFile = File(..., description="CSV or Excel file"),
    target_entity: IngestionEntity = Form(default=IngestionEntity.INVENTORY_SNAPSHOT),
):
    """Parses an uploaded CSV or Excel file and returns pre-flight schema preview and validation issues."""
    try:
        content = await file.read()
        return IngestionValidator.generate_preview(
            file_bytes=content,
            filename=file.filename or "upload.csv",
            target_entity=target_entity,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse upload: {str(e)}")


@router.post("/commit", response_model=IngestionCommitResponse)
def commit_ingestion_dataset(request: IngestionCommitRequest):
    """Commits staged data into the database with deduplication and transactional rollback snapshot."""
    try:
        return IngestionPipeline.commit_dataset(request)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Commit failed: {str(e)}")


@router.post("/rollback", response_model=RollbackResponse)
def rollback_ingestion_transaction(request: RollbackRequest):
    """Reverts an ingestion transaction using its rollback token."""
    try:
        return IngestionPipeline.rollback_dataset(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rollback failed: {str(e)}")


@router.get("/quality", response_model=DataQualityReport)
def get_data_quality_report():
    """Generates an enterprise-wide audit of data quality, completeness, and validity."""
    try:
        return IngestionPipeline.audit_data_quality()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data quality audit failed: {str(e)}")


@router.get("/template/{entity}")
def get_sample_csv_template(entity: IngestionEntity):
    """Returns sample CSV template with standard header columns for the specified entity."""
    if entity == IngestionEntity.INVENTORY_SNAPSHOT:
        content = "item_code,warehouse_location,quantity_on_hand,safety_stock_buffer\nAPEX-JKT-BLA-M,reno,1150,500\nAPEX-JKT-BLA-L,allentown,2100,600\nAPEX-JKT-NAV-M,dallas,450,250\n"
    elif entity == IngestionEntity.PURCHASE_ORDER:
        content = "po_number,vendor_code,delivery_facility,sku_id,order_units,unit_cogs,lifecycle_status\nPO-9018,supp_shenzhen_apparel,wh_reno,APEX-JKT-BLA-M,5000,45.15,PLANNED\n"
    elif entity == IngestionEntity.SKU_CATALOG:
        content = "sku_code,product_title,department,retail_price,standard_cogs,sales_velocity\nAPEX-JKT-RED-M,Apex Stormproof Parka Crimson,Outerwear,180.00,45.15,A\n"
    else:
        content = "order_id,customer_id,order_date,gross_revenue,fulfillment_status\nORD-99001,cust_001,2026-11-02,180.00,FULFILLED\n"
    return PlainTextResponse(content=content, media_type="text/csv")

