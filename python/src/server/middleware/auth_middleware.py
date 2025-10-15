"""
Authentication Middleware for API Key Validation

This middleware validates API keys from the Authorization header and stores
authentication information in the request state for use by route handlers.

Created: 2025-10-15
"""

import logging
import os
from typing import Callable

import bcrypt
from fastapi import HTTPException, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from ..services.client_manager import get_supabase_client

logger = logging.getLogger(__name__)

# Exempt paths that don't require authentication
EXEMPT_PATHS = [
    "/",
    "/health",
    "/api/health",
    "/api/auth/bootstrap",  # Initial API key creation
    "/api/auth/status",     # Public auth status endpoint
    "/internal",  # Internal API uses IP-based auth
]


class APIKeyAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware to validate API keys from Authorization header.

    Checks for 'Authorization: Bearer <api_key>' header,
    validates the key against the database, and stores
    authentication info in request.state.
    """

    def __init__(self, app, enabled: bool = True):
        super().__init__(app)
        self.enabled = enabled
        logger.info(f"API Key Auth Middleware initialized (enabled={enabled})")

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request and validate API key if required."""

        # Skip authentication if disabled
        if not self.enabled:
            return await call_next(request)

        # Check if path is exempt from authentication
        path = request.url.path
        if self._is_exempt_path(path):
            return await call_next(request)

        # Extract API key from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            logger.warning(f"Missing Authorization header | path={path} | ip={request.client.host}")
            return JSONResponse(
                status_code=401,
                content={
                    "error": "Authentication required",
                    "message": "Missing Authorization header. Use 'Authorization: Bearer <api_key>'",
                    "error_type": "missing_auth_header"
                }
            )

        # Parse Bearer token
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            logger.warning(f"Invalid Authorization header format | path={path}")
            return JSONResponse(
                status_code=401,
                content={
                    "error": "Invalid authentication format",
                    "message": "Authorization header must be in format: 'Bearer <api_key>'",
                    "error_type": "invalid_auth_format"
                }
            )

        api_key = parts[1]

        # Validate API key
        try:
            key_info = await self._validate_api_key(api_key)
            if not key_info:
                logger.warning(f"Invalid API key | path={path} | prefix={api_key[:12]}")
                return JSONResponse(
                    status_code=401,
                    content={
                        "error": "Invalid API key",
                        "message": "The provided API key is invalid or has been revoked",
                        "error_type": "invalid_api_key"
                    }
                )

            # Store authentication info in request state
            request.state.authenticated = True
            request.state.api_key_id = key_info["id"]
            request.state.api_key_name = key_info["key_name"]
            request.state.permissions = key_info["permissions"]

            # Update last_used_at timestamp (async, don't await to avoid blocking)
            self._update_last_used(key_info["id"])

            logger.debug(f"API key validated | key_name={key_info['key_name']} | path={path}")

            # Continue with the request
            response = await call_next(request)
            return response

        except Exception as e:
            logger.error(f"Authentication error | error={str(e)} | path={path}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Authentication error",
                    "message": "An error occurred during authentication",
                    "error_type": "auth_error"
                }
            )

    def _is_exempt_path(self, path: str) -> bool:
        """Check if path is exempt from authentication."""
        # Exact matches
        if path in EXEMPT_PATHS:
            return True

        # Prefix matches for internal API
        if path.startswith("/internal/"):
            return True

        return False

    async def _validate_api_key(self, api_key: str) -> dict | None:
        """
        Validate API key against database.

        Args:
            api_key: The API key to validate

        Returns:
            Dict with key info if valid, None if invalid
        """
        try:
            # Hash the provided key
            # Note: We'll need to query all active keys and check each hash
            # This is necessary because bcrypt hashing is one-way

            supabase = get_supabase_client()

            # Get all active API keys
            result = supabase.table("api_keys").select("*").eq("is_active", True).execute()

            if not result.data:
                return None

            # Check each key's hash
            for key_record in result.data:
                key_hash = key_record["key_hash"]

                # Verify the provided key against the stored hash
                if bcrypt.checkpw(api_key.encode('utf-8'), key_hash.encode('utf-8')):
                    # Key is valid
                    return {
                        "id": key_record["id"],
                        "key_name": key_record["key_name"],
                        "permissions": key_record["permissions"],
                        "metadata": key_record.get("metadata", {})
                    }

            # No matching key found
            return None

        except Exception as e:
            logger.error(f"Error validating API key: {e}", exc_info=True)
            return None

    def _update_last_used(self, key_id: str):
        """Update the last_used_at timestamp for the API key (fire and forget)."""
        try:
            import asyncio
            from datetime import datetime

            async def _update():
                try:
                    supabase = get_supabase_client()
                    supabase.table("api_keys").update({
                        "last_used_at": datetime.utcnow().isoformat()
                    }).eq("id", key_id).execute()
                except Exception as e:
                    logger.error(f"Failed to update last_used_at: {e}")

            # Fire and forget
            asyncio.create_task(_update())
        except Exception as e:
            logger.error(f"Error scheduling last_used update: {e}")


async def require_auth(request: Request):
    """
    Dependency function to require authentication.

    Use this as a FastAPI dependency in routes that need authentication:

    Example:
        @router.get("/protected")
        async def protected_route(auth = Depends(require_auth)):
            return {"user": auth.api_key_name}
    """
    if not hasattr(request.state, "authenticated") or not request.state.authenticated:
        raise HTTPException(
            status_code=401,
            detail={
                "error": "Authentication required",
                "message": "This endpoint requires a valid API key",
                "error_type": "authentication_required"
            }
        )

    return request.state


async def require_admin(request: Request):
    """
    Dependency function to require admin permissions.

    Use this for routes that need admin access.
    """
    auth = await require_auth(request)

    permissions = getattr(auth, "permissions", {})
    if not permissions.get("admin", False):
        raise HTTPException(
            status_code=403,
            detail={
                "error": "Admin access required",
                "message": "This endpoint requires admin permissions",
                "error_type": "insufficient_permissions"
            }
        )

    return auth
