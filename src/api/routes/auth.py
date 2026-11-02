"""
SARAS ATLAS — Authentication & User Profile Routes
"""

from fastapi import APIRouter, HTTPException, Depends, status
from src.security.models import LoginRequest, TokenResponse, User
from src.security.auth import authenticate_user, create_access_token, get_current_user
from src.security.audit import log_security_event

router = APIRouter(prefix="/auth", tags=["Authentication & RBAC"])


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    user = authenticate_user(request.username, request.password)
    if not user:
        log_security_event(
            user_id="UNKNOWN",
            username=request.username,
            role="ANONYMOUS",
            action="LOGIN_FAILED",
            resource="/api/v1/auth/login",
            status="FAILURE",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token(user)
    log_security_event(
        user_id=user.user_id,
        username=user.username,
        role=user.role.value,
        action="LOGIN_SUCCESS",
        resource="/api/v1/auth/login",
        status="SUCCESS",
    )
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in_seconds=480 * 60,
        user=user,
    )


@router.get("/me", response_model=User)
def get_current_user_profile(user: User = Depends(get_current_user)):
    return user

