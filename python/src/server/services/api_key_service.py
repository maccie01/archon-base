"""
API Key Service

Handles API key generation, validation, and management.

Created: 2025-10-15
"""

import logging
import secrets
from datetime import datetime
from typing import Optional

import bcrypt
from supabase import Client

logger = logging.getLogger(__name__)


class APIKeyService:
    """Service for managing API keys."""

    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client

    def generate_api_key(self) -> str:
        """
        Generate a secure random API key.

        Format: ak_XXXX_<random_string>
        where XXXX is a 4-character prefix for identification
        """
        # Generate a 4-character prefix for identification
        prefix_chars = secrets.token_hex(2).upper()  # 4 hex chars
        prefix = f"ak_{prefix_chars}"

        # Generate a secure random token (32 bytes = 43 base64 chars)
        token = secrets.token_urlsafe(32)

        # Combine prefix and token
        api_key = f"{prefix}_{token}"

        return api_key

    async def create_api_key(
        self,
        name: str,
        permissions: Optional[dict] = None,
        metadata: Optional[dict] = None
    ) -> tuple[bool, dict]:
        """
        Create a new API key.

        Args:
            name: Human-readable name for the key
            permissions: Permission dict (read, write, admin)
            metadata: Additional metadata to store

        Returns:
            Tuple of (success: bool, result: dict)
            On success, result contains the plain-text API key (only time it's visible)
        """
        try:
            # Generate the API key
            api_key = self.generate_api_key()

            # Extract prefix for storage
            prefix = api_key[:7]  # "ak_XXXX"

            # Hash the API key using bcrypt
            salt = bcrypt.gensalt()
            key_hash = bcrypt.hashpw(api_key.encode('utf-8'), salt).decode('utf-8')

            # Set default permissions if not provided
            if permissions is None:
                permissions = {
                    "read": True,
                    "write": True,
                    "admin": False
                }

            # Set default metadata if not provided
            if metadata is None:
                metadata = {}

            # Add creation timestamp to metadata
            metadata["created_by"] = "system"
            metadata["created_at_utc"] = datetime.utcnow().isoformat()

            # Insert into database
            result = self.supabase.table("api_keys").insert({
                "key_name": name,
                "key_hash": key_hash,
                "key_prefix": prefix,
                "is_active": True,
                "permissions": permissions,
                "metadata": metadata
            }).execute()

            if not result.data:
                return False, {"error": "Failed to create API key in database"}

            key_record = result.data[0]

            logger.info(f"Created API key | key_name={name} | key_id={key_record['id']}")

            return True, {
                "id": key_record["id"],
                "key_name": name,
                "api_key": api_key,  # Only returned once!
                "key_prefix": prefix,
                "permissions": permissions,
                "created_at": key_record["created_at"],
                "message": "API key created successfully. Store this key securely - it cannot be retrieved again."
            }

        except Exception as e:
            logger.error(f"Failed to create API key: {e}", exc_info=True)
            return False, {"error": f"Failed to create API key: {str(e)}"}

    async def validate_api_key(self, api_key: str) -> tuple[bool, Optional[dict]]:
        """
        Validate an API key against the database.

        Args:
            api_key: The API key to validate

        Returns:
            Tuple of (valid: bool, key_info: dict or None)
        """
        try:
            # Get all active API keys
            result = self.supabase.table("api_keys").select("*").eq("is_active", True).execute()

            if not result.data:
                return False, None

            # Check each key's hash
            for key_record in result.data:
                key_hash = key_record["key_hash"]

                # Verify the provided key against the stored hash
                if bcrypt.checkpw(api_key.encode('utf-8'), key_hash.encode('utf-8')):
                    # Key is valid
                    return True, {
                        "id": key_record["id"],
                        "key_name": key_record["key_name"],
                        "permissions": key_record["permissions"],
                        "created_at": key_record["created_at"],
                        "last_used_at": key_record.get("last_used_at")
                    }

            # No matching key found
            return False, None

        except Exception as e:
            logger.error(f"Error validating API key: {e}", exc_info=True)
            return False, None

    async def revoke_api_key(self, key_id: str) -> tuple[bool, dict]:
        """
        Revoke an API key by setting is_active to false.

        Args:
            key_id: The UUID of the API key to revoke

        Returns:
            Tuple of (success: bool, result: dict)
        """
        try:
            # Update the key to set is_active = false
            result = self.supabase.table("api_keys").update({
                "is_active": False
            }).eq("id", key_id).execute()

            if not result.data:
                return False, {"error": "API key not found"}

            logger.info(f"Revoked API key | key_id={key_id}")

            return True, {
                "message": "API key revoked successfully",
                "key_id": key_id
            }

        except Exception as e:
            logger.error(f"Failed to revoke API key: {e}", exc_info=True)
            return False, {"error": f"Failed to revoke API key: {str(e)}"}

    async def list_api_keys(self, include_inactive: bool = False) -> tuple[bool, dict]:
        """
        List all API keys (excluding hashes for security).

        Args:
            include_inactive: Whether to include revoked keys

        Returns:
            Tuple of (success: bool, result: dict)
        """
        try:
            query = self.supabase.table("api_keys").select(
                "id, key_name, key_prefix, created_at, last_used_at, is_active, permissions, metadata"
            )

            if not include_inactive:
                query = query.eq("is_active", True)

            result = query.order("created_at", desc=True).execute()

            keys = result.data if result.data else []

            return True, {
                "keys": keys,
                "total": len(keys)
            }

        except Exception as e:
            logger.error(f"Failed to list API keys: {e}", exc_info=True)
            return False, {"error": f"Failed to list API keys: {str(e)}"}

    async def get_api_key(self, key_id: str) -> tuple[bool, dict]:
        """
        Get details for a specific API key.

        Args:
            key_id: The UUID of the API key

        Returns:
            Tuple of (success: bool, result: dict)
        """
        try:
            result = self.supabase.table("api_keys").select(
                "id, key_name, key_prefix, created_at, last_used_at, is_active, permissions, metadata"
            ).eq("id", key_id).execute()

            if not result.data:
                return False, {"error": "API key not found"}

            return True, {"key": result.data[0]}

        except Exception as e:
            logger.error(f"Failed to get API key: {e}", exc_info=True)
            return False, {"error": f"Failed to get API key: {str(e)}"}

    async def update_api_key(
        self,
        key_id: str,
        key_name: Optional[str] = None,
        permissions: Optional[dict] = None,
        metadata: Optional[dict] = None
    ) -> tuple[bool, dict]:
        """
        Update an API key's metadata.

        Args:
            key_id: The UUID of the API key
            key_name: New name for the key
            permissions: New permissions
            metadata: New metadata

        Returns:
            Tuple of (success: bool, result: dict)
        """
        try:
            updates = {}
            if key_name is not None:
                updates["key_name"] = key_name
            if permissions is not None:
                updates["permissions"] = permissions
            if metadata is not None:
                updates["metadata"] = metadata

            if not updates:
                return False, {"error": "No updates provided"}

            result = self.supabase.table("api_keys").update(updates).eq("id", key_id).execute()

            if not result.data:
                return False, {"error": "API key not found"}

            logger.info(f"Updated API key | key_id={key_id} | updates={list(updates.keys())}")

            return True, {
                "message": "API key updated successfully",
                "key": result.data[0]
            }

        except Exception as e:
            logger.error(f"Failed to update API key: {e}", exc_info=True)
            return False, {"error": f"Failed to update API key: {str(e)}"}
