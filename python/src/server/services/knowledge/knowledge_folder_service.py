"""
Knowledge Folder Service

Handles knowledge folder operations for organizing project-specific knowledge sources.
"""

from typing import Any

from ...config.logfire_config import get_logger

logger = get_logger(__name__)


class KnowledgeFolderService:
    """
    Service for managing knowledge folders within projects.

    Folders provide organizational structure for project-specific knowledge sources,
    allowing users to group related documentation, specifications, and references.
    """

    def __init__(self, supabase_client):
        """
        Initialize the knowledge folder service.

        Args:
            supabase_client: The Supabase client for database operations
        """
        self.supabase = supabase_client

    async def create_folder(
        self,
        project_id: str,
        folder_name: str,
        description: str | None = None,
        color_hex: str = "#6366f1",
        icon_name: str = "folder",
    ) -> dict[str, Any]:
        """
        Create a new knowledge folder for a project.

        Args:
            project_id: UUID of the project
            folder_name: Name of the folder
            description: Optional description of folder contents
            color_hex: Hex color for visual identification (default: indigo)
            icon_name: Icon identifier for UI display (default: folder)

        Returns:
            Dict containing the created folder data

        Raises:
            Exception: If folder creation fails
        """
        try:
            logger.info(
                f"Creating knowledge folder | project_id={project_id} | folder_name={folder_name}"
            )

            # Validate required fields
            if not project_id or not folder_name:
                raise ValueError("project_id and folder_name are required")

            if not folder_name.strip():
                raise ValueError("folder_name cannot be empty")

            # Prepare folder data
            folder_data = {
                "project_id": project_id,
                "folder_name": folder_name.strip(),
                "description": description,
                "color_hex": color_hex,
                "icon_name": icon_name,
                "sort_order": 0,  # Default sort order
            }

            # Insert folder
            result = (
                self.supabase.from_("archon_project_knowledge_folders")
                .insert(folder_data)
                .execute()
            )

            if not result.data:
                raise Exception("Failed to create folder - database returned no data")

            folder = result.data[0]
            logger.info(f"Knowledge folder created successfully | folder_id={folder['id']}")

            return folder

        except Exception as e:
            logger.error(
                f"Failed to create knowledge folder | error={str(e)} | project_id={project_id}"
            )
            raise

    async def update_folder(
        self, folder_id: str, updates: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Update a knowledge folder's metadata.

        Args:
            folder_id: UUID of the folder to update
            updates: Dict of fields to update (folder_name, description, color_hex, icon_name, sort_order)

        Returns:
            Dict containing the updated folder data

        Raises:
            Exception: If folder update fails or folder not found
        """
        try:
            logger.info(f"Updating knowledge folder | folder_id={folder_id}")

            # Validate folder_id
            if not folder_id:
                raise ValueError("folder_id is required")

            # Build update data with allowed fields
            allowed_fields = [
                "folder_name",
                "description",
                "color_hex",
                "icon_name",
                "sort_order",
            ]
            update_data = {k: v for k, v in updates.items() if k in allowed_fields}

            if not update_data:
                raise ValueError("No valid update fields provided")

            # Strip folder_name if provided
            if "folder_name" in update_data:
                update_data["folder_name"] = update_data["folder_name"].strip()
                if not update_data["folder_name"]:
                    raise ValueError("folder_name cannot be empty")

            # Update folder
            result = (
                self.supabase.from_("archon_project_knowledge_folders")
                .update(update_data)
                .eq("id", folder_id)
                .execute()
            )

            if not result.data:
                raise Exception(f"Folder with ID {folder_id} not found")

            folder = result.data[0]
            logger.info(f"Knowledge folder updated successfully | folder_id={folder_id}")

            return folder

        except Exception as e:
            logger.error(
                f"Failed to update knowledge folder | error={str(e)} | folder_id={folder_id}"
            )
            raise

    async def delete_folder(self, folder_id: str) -> bool:
        """
        Delete a knowledge folder.

        Note: This sets source.folder_id to NULL for all sources in this folder,
        but does not delete the sources themselves. Sources remain in the project.

        Args:
            folder_id: UUID of the folder to delete

        Returns:
            True if deletion was successful

        Raises:
            Exception: If folder deletion fails
        """
        try:
            logger.info(f"Deleting knowledge folder | folder_id={folder_id}")

            # Validate folder_id
            if not folder_id:
                raise ValueError("folder_id is required")

            # First, unlink all sources from this folder (set folder_id to NULL)
            # This happens automatically via ON DELETE SET NULL constraint
            # but we log it for clarity
            sources_result = (
                self.supabase.from_("archon_sources")
                .select("source_id", count="exact")
                .eq("folder_id", folder_id)
                .execute()
            )
            source_count = sources_result.count if hasattr(sources_result, "count") else 0

            # Delete the folder
            result = (
                self.supabase.from_("archon_project_knowledge_folders")
                .delete()
                .eq("id", folder_id)
                .execute()
            )

            logger.info(
                f"Knowledge folder deleted successfully | folder_id={folder_id} | unlinked_sources={source_count}"
            )

            return True

        except Exception as e:
            logger.error(
                f"Failed to delete knowledge folder | error={str(e)} | folder_id={folder_id}"
            )
            raise

    async def get_folder(self, folder_id: str) -> dict[str, Any] | None:
        """
        Get a specific knowledge folder by ID.

        Args:
            folder_id: UUID of the folder to retrieve

        Returns:
            Dict containing folder data, or None if not found
        """
        try:
            logger.info(f"Getting knowledge folder | folder_id={folder_id}")

            # Validate folder_id
            if not folder_id:
                return None

            result = (
                self.supabase.from_("archon_project_knowledge_folders")
                .select("*")
                .eq("id", folder_id)
                .single()
                .execute()
            )

            if not result.data:
                return None

            return result.data

        except Exception as e:
            # Log but don't raise for get operations - return None
            logger.warning(
                f"Failed to get knowledge folder | error={str(e)} | folder_id={folder_id}"
            )
            return None

    async def list_project_folders(self, project_id: str) -> list[dict[str, Any]]:
        """
        List all knowledge folders for a project, ordered by sort_order.

        Args:
            project_id: UUID of the project

        Returns:
            List of folder dicts with source counts

        Raises:
            Exception: If listing fails
        """
        try:
            logger.info(f"Listing knowledge folders | project_id={project_id}")

            # Validate project_id
            if not project_id:
                raise ValueError("project_id is required")

            # Get all folders for the project
            result = (
                self.supabase.from_("archon_project_knowledge_folders")
                .select("*")
                .eq("project_id", project_id)
                .order("sort_order")
                .order("created_at")
                .execute()
            )

            folders = result.data if result.data else []

            # Get source counts for each folder
            folder_ids = [folder["id"] for folder in folders]
            source_counts = {}

            if folder_ids:
                # Batch count sources for all folders
                for folder_id in folder_ids:
                    count_result = (
                        self.supabase.from_("archon_sources")
                        .select("source_id", count="exact", head=True)
                        .eq("folder_id", folder_id)
                        .execute()
                    )
                    source_counts[folder_id] = (
                        count_result.count if hasattr(count_result, "count") else 0
                    )

            # Add source counts to folder data
            for folder in folders:
                folder["source_count"] = source_counts.get(folder["id"], 0)

            logger.info(
                f"Listed knowledge folders | project_id={project_id} | count={len(folders)}"
            )

            return folders

        except Exception as e:
            logger.error(
                f"Failed to list knowledge folders | error={str(e)} | project_id={project_id}"
            )
            raise

    async def get_folder_source_count(self, folder_id: str) -> int:
        """
        Get the number of sources in a specific folder.

        Args:
            folder_id: UUID of the folder

        Returns:
            Number of sources in the folder
        """
        try:
            logger.info(f"Getting folder source count | folder_id={folder_id}")

            # Validate folder_id
            if not folder_id:
                return 0

            result = (
                self.supabase.from_("archon_sources")
                .select("source_id", count="exact", head=True)
                .eq("folder_id", folder_id)
                .execute()
            )

            count = result.count if hasattr(result, "count") else 0
            logger.info(f"Folder source count retrieved | folder_id={folder_id} | count={count}")

            return count

        except Exception as e:
            logger.warning(
                f"Failed to get folder source count | error={str(e)} | folder_id={folder_id}"
            )
            return 0
