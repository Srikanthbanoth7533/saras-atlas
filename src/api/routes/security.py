"""
SARAS ATLAS — Security Audit & Health Routes
"""

from typing import List
from fastapi import APIRouter, Depends, Query
from src.security.models import AuditLogEntry, User, UserRole
from src.security.auth import require_roles
from src.security.audit import read_audit_logs

router = APIRouter(prefix="/security", tags=["Security & Audit"])


@router.get("/audit-trail", response_model=List[AuditLogEntry])
def get_security_audit_trail(
    limit: int = Query(50, ge=1, le=200),
    user: User = Depends(require_roles(UserRole.ADMIN, UserRole.AUDITOR, UserRole.CFO)),
):
    return read_audit_logs(limit=limit)
