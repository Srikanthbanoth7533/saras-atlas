"""
SARAS ATLAS — Enterprise Warehouse & API Connectors Routes
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path
from src.domain.connectors.models import (
    ConnectorConfig,
    ConnectionTestResult,
    SchemaDiscoveryResponse,
)
from src.domain.connectors.manager import EnterpriseConnectorManager
from src.security.models import User, UserRole
from src.security.auth import get_current_user, require_roles

router = APIRouter(prefix="/connectors", tags=["Enterprise Connectors"])


@router.get("/list", response_model=List[ConnectorConfig])
def list_connectors(user: User = Depends(get_current_user)):
    return EnterpriseConnectorManager.list_connectors()


@router.post("/{connector_id}/test", response_model=ConnectionTestResult)
def test_connector(
    connector_id: str = Path(..., description="Target connector identifier"),
    user: User = Depends(require_roles(UserRole.ADMIN, UserRole.SUPPLY_CHAIN_VP, UserRole.ANALYST)),
):
    return EnterpriseConnectorManager.test_connection(connector_id)


@router.get("/{connector_id}/schema", response_model=SchemaDiscoveryResponse)
def discover_schema(
    connector_id: str = Path(..., description="Target connector identifier"),
    user: User = Depends(get_current_user),
):
    return EnterpriseConnectorManager.discover_schema(connector_id)
