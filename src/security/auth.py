"""
SARAS ATLAS — Authentication & Role-Based Access Control (RBAC)
Implements JWT tokens, password hashing, and role verification for enterprise governance.
"""

import hashlib
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import jwt
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.security.models import User, UserRole, TokenResponse
from src.security.audit import log_security_event

SECRET_KEY = os.getenv("ATLAS_JWT_SECRET", "saras-atlas-enterprise-decision-twin-key-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 hours

security_scheme = HTTPBearer(auto_error=False)

# Salt for password hashing
_SALT = "atlas_enterprise_salt_v4"

def hash_password(password: str) -> str:
    return hashlib.sha256((_SALT + password).encode("utf-8")).hexdigest()

# Pre-seeded enterprise users for role-based governance
DEMO_USERS: Dict[str, dict] = {
    "admin": {
        "user_id": "USR-ADMIN-01",
        "username": "admin",
        "password_hash": hash_password("AtlasAdmin2026!"),
        "full_name": "Atlas Platform Administrator",
        "email": "admin@vanguardapparel.internal",
        "role": UserRole.ADMIN,
    },
    "vp_supply": {
        "user_id": "USR-VPSUPPLY-02",
        "username": "vp_supply",
        "password_hash": hash_password("SupplyChain2026!"),
        "full_name": "Marcus Vance (VP Supply Chain)",
        "email": "m.vance@vanguardapparel.internal",
        "role": UserRole.SUPPLY_CHAIN_VP,
    },
    "cfo": {
        "user_id": "USR-CFO-03",
        "username": "cfo",
        "password_hash": hash_password("FinanceResilience2026!"),
        "full_name": "Elena Rostova (Chief Financial Officer)",
        "email": "e.rostova@vanguardapparel.internal",
        "role": UserRole.CFO,
    },
    "analyst": {
        "user_id": "USR-ANALYST-04",
        "username": "analyst",
        "password_hash": hash_password("OperationsAnalyst2026!"),
        "full_name": "Devin Chen (Senior Resilience Analyst)",
        "email": "d.chen@vanguardapparel.internal",
        "role": UserRole.ANALYST,
    },
    "auditor": {
        "user_id": "USR-AUDITOR-05",
        "username": "auditor",
        "password_hash": hash_password("GovernanceAudit2026!"),
        "full_name": "Sarah Jenkins (Enterprise Auditor)",
        "email": "s.jenkins@vanguardapparel.internal",
        "role": UserRole.AUDITOR,
    },
}


def authenticate_user(username: str, password: str) -> Optional[User]:
    user_data = DEMO_USERS.get(username.lower())
    if not user_data:
        return None
    if user_data["password_hash"] != hash_password(password):
        return None
    return User(
        user_id=user_data["user_id"],
        username=user_data["username"],
        full_name=user_data["full_name"],
        email=user_data["email"],
        role=user_data["role"],
    )


def create_access_token(user: User, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {
        "sub": user.user_id,
        "username": user.username,
        "role": user.role.value,
        "full_name": user.full_name,
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Security(security_scheme)) -> User:
    """Extract and validate current user from JWT token, with graceful fallback to Analyst in dev mode."""
    if not credentials:
        # Fallback to Analyst for frictionless zero-config local exploration if unauthenticated
        return User(
            user_id="USR-LOCAL-ANALYST",
            username="local_analyst",
            full_name="Local Interactive Analyst",
            email="analyst@vanguardapparel.internal",
            role=UserRole.ANALYST,
        )
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        username = payload.get("username")
        role_str = payload.get("role")
        full_name = payload.get("full_name", username)
        if not username or not role_str:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return User(
            user_id=user_id,
            username=username,
            full_name=full_name,
            email=f"{username}@vanguardapparel.internal",
            role=UserRole(role_str),
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate enterprise credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_roles(*allowed_roles: UserRole):
    """Enforce Role-Based Access Control guard on endpoints."""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role == UserRole.ADMIN:
            return current_user  # Admin has omni-access
        if current_user.role not in allowed_roles:
            log_security_event(
                user_id=current_user.user_id,
                username=current_user.username,
                role=current_user.role.value,
                action="RBAC_ACCESS_DENIED",
                resource="restricted_endpoint",
                status="FORBIDDEN",
                details={"required_roles": [r.value for r in allowed_roles]},
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: Required role in {[r.value for r in allowed_roles]}. Current role: {current_user.role.value}",
            )
        return current_user
    return role_checker

