"""
SARAS ATLAS — Security Audit Logger
Maintains an immutable, append-only JSON audit trail for critical security, governance, and business decisions.
"""

import json
import os
import threading
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from src.security.models import AuditLogEntry

AUDIT_DIR = Path("data/audit")
AUDIT_LOG_FILE = AUDIT_DIR / "security_audit.log"
_lock = threading.Lock()


def ensure_audit_dir():
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    if not AUDIT_LOG_FILE.exists():
        AUDIT_LOG_FILE.touch()


def log_security_event(
    user_id: str,
    username: str,
    role: str,
    action: str,
    resource: str,
    status: str = "SUCCESS",
    client_ip: str = "127.0.0.1",
    details: Optional[Dict[str, Any]] = None,
) -> AuditLogEntry:
    """Log a security event to the append-only audit trail."""
    ensure_audit_dir()
    entry = AuditLogEntry(
        timestamp=datetime.utcnow().isoformat() + "Z",
        event_id=f"EVT-{uuid.uuid4().hex[:12].upper()}",
        user_id=user_id,
        username=username,
        role=role,
        action=action,
        resource=resource,
        status=status,
        client_ip=client_ip,
        details=details or {},
    )
    with _lock:
        with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry.model_dump()) + "\n")
    return entry


def read_audit_logs(limit: int = 50) -> List[AuditLogEntry]:
    """Read the latest audit log entries in reverse chronological order."""
    ensure_audit_dir()
    entries = []
    with _lock:
        if not AUDIT_LOG_FILE.exists():
            return []
        with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in reversed(lines[-limit:]):
                try:
                    data = json.loads(line.strip())
                    entries.append(AuditLogEntry(**data))
                except Exception:
                    continue
    return entries
