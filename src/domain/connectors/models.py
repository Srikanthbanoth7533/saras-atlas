"""
SARAS ATLAS — Enterprise Warehouse & API Connectors Models
Defines integration schemas for BigQuery, Snowflake, Amazon Redshift, CSV/Excel, and REST Webhooks.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ConnectorType(str, Enum):
    BIGQUERY = "BIGQUERY"
    SNOWFLAKE = "SNOWFLAKE"
    AMAZON_REDSHIFT = "AMAZON_REDSHIFT"
    REST_WEBHOOK = "REST_WEBHOOK"
    CSV_EXCEL = "CSV_EXCEL"


class ConnectorConfig(BaseModel):
    connector_id: str
    name: str
    connector_type: ConnectorType
    is_enabled: bool = True
    host: Optional[str] = None
    database: Optional[str] = None
    warehouse_or_dataset: Optional[str] = None
    auth_mode: str = "SANDBOX_DRYRUN"  # SANDBOX_DRYRUN, SERVICE_ACCOUNT, OAUTH2, API_KEY
    is_sandbox_mode: bool = True
    description: str


class ConnectionTestResult(BaseModel):
    connector_id: str
    connector_type: ConnectorType
    success: bool
    latency_ms: float
    status: str  # CONNECTED, SANDBOX_VERIFIED, AUTH_REQUIRED, FAILED
    message: str
    discovered_tables_count: int
    discovered_tables: List[str]
    sample_rows_previewed: int
    security_posture: str = "ZERO_CREDENTIAL_LEAK_CONFIRMED"


class SchemaDiscoveryResponse(BaseModel):
    connector_id: str
    connector_type: ConnectorType
    dialect: str
    database: str
    schema_name: str
    tables: Dict[str, List[Dict[str, str]]]  # table_name -> list of {column: name, type: type}
    recommended_sync_mode: str
    generated_at: str
