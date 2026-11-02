"""
SARAS ATLAS — Security & Role-Based Access Control Models
Defines user identities, permissions, JWT claims, and security audit log schemas.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    SUPPLY_CHAIN_VP = "SUPPLY_CHAIN_VP"
    CFO = "CFO"
    ANALYST = "ANALYST"
    AUDITOR = "AUDITOR"


class User(BaseModel):
    user_id: str
    username: str
    full_name: str
    email: str
    role: UserRole
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4, max_length=100)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_seconds: int
    user: User


class AuditLogEntry(BaseModel):
    timestamp: str
    event_id: str
    user_id: str
    username: str
    role: str
    action: str
    resource: str
    status: str  # SUCCESS, FAILURE, FORBIDDEN
    client_ip: Optional[str] = "127.0.0.1"
    details: Optional[dict] = Field(default_factory=dict)
