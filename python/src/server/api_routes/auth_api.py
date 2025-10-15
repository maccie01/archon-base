"""
Authentication API endpoints for API key management.

Created: 2025-10-15
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from ..middleware.auth_middleware import require_admin, require_auth
from ..services.api_key_service import APIKeyService
from ..services.client_manager import get_supabase_client

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/auth", tags=["authentication"])


# Request Models
class CreateAPIKeyRequest(BaseModel):
    name: str
    permissions: dict | None = None
    metadata: dict | None = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Production Key",
                "permissions": {
                    "read": True,
                    "write": True,
                    "admin": False
                },
                "metadata": {
                    "purpose": "Production deployment",
                    "environment": "production"
                }
            }
        }


class UpdateAPIKeyRequest(BaseModel):
    key_name: str | None = None
    permissions: dict | None = None
    metadata: dict | None = None


class BootstrapRequest(BaseModel):
    bootstrap_secret: str
    key_name: str = "Initial Admin Key"


@router.post("/bootstrap")
async def bootstrap_api_key(request: BootstrapRequest):
    """
    Create the initial API key for Archon.

    This endpoint is only available when no API keys exist in the database.
    Requires a bootstrap secret from environment variable ARCHON_BOOTSTRAP_SECRET.

    Once the first API key is created, this endpoint will no longer work.
    """
    import os

    try:
        # Check for bootstrap secret in environment
        expected_secret = os.getenv("ARCHON_BOOTSTRAP_SECRET")
        if not expected_secret:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "Bootstrap not configured",
                    "message": "ARCHON_BOOTSTRAP_SECRET environment variable is not set",
                    "error_type": "bootstrap_not_configured"
                }
            )

        # Verify bootstrap secret
        if request.bootstrap_secret != expected_secret:
            logger.warning("Invalid bootstrap secret attempt")
            raise HTTPException(
                status_code=401,
                detail={
                    "error": "Invalid bootstrap secret",
                    "message": "The provided bootstrap secret is incorrect",
                    "error_type": "invalid_bootstrap_secret"
                }
            )

        # Check if any API keys already exist
        supabase = get_supabase_client()
        result = supabase.table("api_keys").select("id", count="exact").limit(1).execute()

        if result.data and len(result.data) > 0:
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "Bootstrap not available",
                    "message": "API keys already exist. Use the API key management endpoints.",
                    "error_type": "bootstrap_already_complete"
                }
            )

        # Create the initial admin API key
        service = APIKeyService(supabase)
        success, result_data = await service.create_api_key(
            name=request.key_name,
            permissions={
                "read": True,
                "write": True,
                "admin": True  # First key gets admin permissions
            },
            metadata={
                "bootstrap": True,
                "purpose": "Initial admin key for Archon setup"
            }
        )

        if success:
            logger.info(f"Bootstrap API key created | key_name={request.key_name}")
            return {
                "success": True,
                "message": "Initial API key created successfully. Store this key securely!",
                "api_key": result_data["api_key"],
                "key_name": result_data["key_name"],
                "key_id": result_data["id"],
                "warning": "This is the only time you will see this API key. Store it securely!"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Failed to create bootstrap key",
                    "message": result_data.get("error", "Unknown error"),
                    "error_type": "bootstrap_creation_failed"
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Bootstrap error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Bootstrap failed",
                "message": str(e),
                "error_type": "bootstrap_error"
            }
        )


@router.post("/keys")
async def create_api_key(
    request: CreateAPIKeyRequest,
    auth = Depends(require_admin)
):
    """
    Create a new API key (admin only).

    Returns the plain-text API key - this is the ONLY time it will be visible.
    """
    try:
        service = APIKeyService(get_supabase_client())
        success, result = await service.create_api_key(
            name=request.name,
            permissions=request.permissions,
            metadata=request.metadata
        )

        if success:
            return {
                "success": True,
                **result
            }
        else:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Failed to create API key",
                    "message": result.get("error", "Unknown error"),
                    "error_type": "key_creation_failed"
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating API key: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to create API key",
                "message": str(e),
                "error_type": "key_creation_error"
            }
        )


@router.get("/keys")
async def list_api_keys(
    include_inactive: bool = False,
    auth = Depends(require_auth)
):
    """
    List all API keys.

    Admin users can see all keys. Regular users only see their own.
    """
    try:
        service = APIKeyService(get_supabase_client())
        success, result = await service.list_api_keys(include_inactive=include_inactive)

        if success:
            return {
                "success": True,
                **result
            }
        else:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Failed to list API keys",
                    "message": result.get("error", "Unknown error"),
                    "error_type": "key_list_failed"
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing API keys: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to list API keys",
                "message": str(e),
                "error_type": "key_list_error"
            }
        )


@router.get("/keys/{key_id}")
async def get_api_key(
    key_id: str,
    auth = Depends(require_auth)
):
    """Get details for a specific API key."""
    try:
        service = APIKeyService(get_supabase_client())
        success, result = await service.get_api_key(key_id)

        if success:
            return {
                "success": True,
                **result
            }
        else:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "API key not found",
                    "message": result.get("error", "Unknown error"),
                    "error_type": "key_not_found"
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting API key: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to get API key",
                "message": str(e),
                "error_type": "key_get_error"
            }
        )


@router.put("/keys/{key_id}")
async def update_api_key(
    key_id: str,
    request: UpdateAPIKeyRequest,
    auth = Depends(require_admin)
):
    """Update an API key's metadata (admin only)."""
    try:
        service = APIKeyService(get_supabase_client())
        success, result = await service.update_api_key(
            key_id=key_id,
            key_name=request.key_name,
            permissions=request.permissions,
            metadata=request.metadata
        )

        if success:
            return {
                "success": True,
                **result
            }
        else:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "Failed to update API key",
                    "message": result.get("error", "Unknown error"),
                    "error_type": "key_update_failed"
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating API key: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to update API key",
                "message": str(e),
                "error_type": "key_update_error"
            }
        )


@router.delete("/keys/{key_id}")
async def revoke_api_key(
    key_id: str,
    auth = Depends(require_admin)
):
    """Revoke an API key (admin only)."""
    try:
        service = APIKeyService(get_supabase_client())
        success, result = await service.revoke_api_key(key_id)

        if success:
            return {
                "success": True,
                **result
            }
        else:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "Failed to revoke API key",
                    "message": result.get("error", "Unknown error"),
                    "error_type": "key_revoke_failed"
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error revoking API key: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to revoke API key",
                "message": str(e),
                "error_type": "key_revoke_error"
            }
        )


@router.get("/validate")
async def validate_current_key(auth = Depends(require_auth)):
    """
    Validate the current API key.

    Returns information about the authenticated API key.
    """
    return {
        "success": True,
        "valid": True,
        "key_id": auth.api_key_id,
        "key_name": auth.api_key_name,
        "permissions": auth.permissions
    }


@router.get("/status")
async def auth_status():
    """
    Check authentication system status.

    Public endpoint to check if authentication is configured.
    """
    import os

    try:
        supabase = get_supabase_client()
        result = supabase.table("api_keys").select("id", count="exact").limit(1).execute()

        has_keys = result.data and len(result.data) > 0
        has_bootstrap_secret = bool(os.getenv("ARCHON_BOOTSTRAP_SECRET"))

        return {
            "authentication_enabled": True,
            "has_api_keys": has_keys,
            "bootstrap_available": not has_keys and has_bootstrap_secret,
            "message": "Bootstrap endpoint available" if not has_keys else "Use API key authentication"
        }

    except Exception as e:
        logger.error(f"Error checking auth status: {e}", exc_info=True)
        return {
            "authentication_enabled": False,
            "error": str(e)
        }
