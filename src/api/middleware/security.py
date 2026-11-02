"""
SARAS ATLAS — Security & Production Hardening Middleware
Enforces enterprise security headers, in-memory rate limiting, and request sanitization.
"""

import time
import threading
from typing import Dict, Tuple, List
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

# In-memory IP rate limiter: max requests per minute window
_RATE_LIMIT_LOCK = threading.Lock()
_IP_REQUEST_LOG: Dict[str, List[float]] = {}
MAX_REQUESTS_PER_MINUTE = 300


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Injects enterprise HTTP security headers on all responses."""

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline';"
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response


class RateLimitingMiddleware(BaseHTTPMiddleware):
    """Enforces per-client in-memory sliding window rate limits."""

    async def dispatch(self, request: Request, call_next):
        # Exempt health and metrics from rate limits
        if request.url.path.endswith("/health"):
            return await call_next(request)

        client_ip = request.client.host if request.client else "127.0.0.1"
        now = time.time()

        with _RATE_LIMIT_LOCK:
            timestamps = _IP_REQUEST_LOG.get(client_ip, [])
            # Filter timestamps within last 60 seconds
            valid_timestamps = [t for t in timestamps if now - t < 60.0]
            if len(valid_timestamps) >= MAX_REQUESTS_PER_MINUTE:
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": "Rate limit exceeded. Maximum 300 requests per minute allowed.",
                        "client_ip": client_ip,
                        "retry_after_seconds": 30,
                    },
                    headers={"Retry-After": "30"},
                )
            valid_timestamps.append(now)
            _IP_REQUEST_LOG[client_ip] = valid_timestamps

        return await call_next(request)
