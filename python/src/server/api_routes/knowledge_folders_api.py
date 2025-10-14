"""
Knowledge Folders API Module

This module handles all folder management operations for project-specific knowledge.
Folders provide organizational structure for project-scoped knowledge sources.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ..config.logfire_config import get_logger, safe_logfire_error, safe_logfire_info
from ..services.knowledge import KnowledgeFolderService
from ..utils import get_supabase_client

# Get logger for this module
logger = get_logger(__name__)

# Create router
router = APIRouter(prefix="/api/knowledge/folders", tags=["knowledge-folders"])


# Pydantic models
class CreateFolderRequest(BaseModel):
    project_id: str
    folder_name: str
    description: str | None = None
    color_hex: str = "#6366f1"  # Indigo by default
    icon_name: str = "folder"

    class Config:
        schema_extra = {
            "example": {
                "project_id": "proj_123",
                "folder_name": "API Documentation",
                "description": "REST API endpoints and schemas",
                "color_hex": "#3b82f6",
                "icon_name": "api"
            }
        }


class UpdateFolderRequest(BaseModel):
    folder_name: str | None = None
    description: str | None = None
    color_hex: str | None = None
    icon_name: str | None = None
    sort_order: int | None = None

    class Config:
        schema_extra = {
            "example": {
                "folder_name": "Updated Name",
                "description": "Updated description",
                "color_hex": "#ef4444",
                "sort_order": 5
            }
        }


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_folder(request: CreateFolderRequest):
    """
    Create a new knowledge folder for a project.

    Args:
        request: Folder creation request containing project_id, name, and metadata

    Returns:
        Created folder with all metadata
    """
    try:
        safe_logfire_info(
            f"Creating knowledge folder | project_id={request.project_id} | "
            f"folder_name={request.folder_name}"
        )

        # Use KnowledgeFolderService to create folder
        service = KnowledgeFolderService(get_supabase_client())
        folder = await service.create_folder(
            project_id=request.project_id,
            folder_name=request.folder_name,
            description=request.description,
            color_hex=request.color_hex,
            icon_name=request.icon_name
        )

        safe_logfire_info(
            f"Knowledge folder created successfully | folder_id={folder['id']} | "
            f"project_id={request.project_id}"
        )

        return {
            "success": True,
            "folder": folder
        }

    except ValueError as e:
        # Validation errors (missing fields, etc.)
        safe_logfire_error(f"Folder validation error | error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(e)}
        )
    except Exception as e:
        safe_logfire_error(
            f"Failed to create folder | error={str(e)} | "
            f"project_id={request.project_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e)}
        )


@router.get("/{folder_id}")
async def get_folder(folder_id: str):
    """
    Get a specific knowledge folder by ID.

    Args:
        folder_id: UUID of the folder

    Returns:
        Folder with all metadata and source count
    """
    try:
        safe_logfire_info(f"Getting knowledge folder | folder_id={folder_id}")

        # Use KnowledgeFolderService to get folder
        service = KnowledgeFolderService(get_supabase_client())
        folder = await service.get_folder(folder_id)

        if not folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": f"Folder {folder_id} not found"}
            )

        safe_logfire_info(f"Knowledge folder retrieved | folder_id={folder_id}")

        return {
            "success": True,
            "folder": folder
        }

    except HTTPException:
        raise
    except Exception as e:
        safe_logfire_error(
            f"Failed to get folder | error={str(e)} | folder_id={folder_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e)}
        )


@router.put("/{folder_id}")
async def update_folder(folder_id: str, request: UpdateFolderRequest):
    """
    Update a knowledge folder's metadata.

    Args:
        folder_id: UUID of the folder
        request: Update request with optional fields

    Returns:
        Updated folder
    """
    try:
        safe_logfire_info(f"Updating knowledge folder | folder_id={folder_id}")

        # Build update fields from request
        update_fields = {}
        if request.folder_name is not None:
            update_fields["folder_name"] = request.folder_name
        if request.description is not None:
            update_fields["description"] = request.description
        if request.color_hex is not None:
            update_fields["color_hex"] = request.color_hex
        if request.icon_name is not None:
            update_fields["icon_name"] = request.icon_name
        if request.sort_order is not None:
            update_fields["sort_order"] = request.sort_order

        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "No update fields provided"}
            )

        # Use KnowledgeFolderService to update folder
        service = KnowledgeFolderService(get_supabase_client())
        folder = await service.update_folder(folder_id, update_fields)

        if not folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": f"Folder {folder_id} not found"}
            )

        safe_logfire_info(
            f"Knowledge folder updated successfully | folder_id={folder_id}"
        )

        return {
            "success": True,
            "folder": folder
        }

    except HTTPException:
        raise
    except Exception as e:
        safe_logfire_error(
            f"Failed to update folder | error={str(e)} | folder_id={folder_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e)}
        )


@router.delete("/{folder_id}")
async def delete_folder(folder_id: str):
    """
    Delete a knowledge folder.

    Note: Sources in this folder will have their folder_id set to NULL.
    Sources are not deleted, only unlinked from the folder.

    Args:
        folder_id: UUID of the folder

    Returns:
        Success message
    """
    try:
        safe_logfire_info(f"Deleting knowledge folder | folder_id={folder_id}")

        # Use KnowledgeFolderService to delete folder
        service = KnowledgeFolderService(get_supabase_client())
        success = await service.delete_folder(folder_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": f"Folder {folder_id} not found"}
            )

        safe_logfire_info(
            f"Knowledge folder deleted successfully | folder_id={folder_id}"
        )

        return {
            "success": True,
            "message": f"Folder {folder_id} deleted successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        safe_logfire_error(
            f"Failed to delete folder | error={str(e)} | folder_id={folder_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e)}
        )


@router.get("/projects/{project_id}/list")
async def list_project_folders(project_id: str):
    """
    List all knowledge folders for a specific project.

    Args:
        project_id: UUID of the project

    Returns:
        List of folders with source counts, ordered by sort_order
    """
    try:
        safe_logfire_info(f"Listing folders for project | project_id={project_id}")

        # Use KnowledgeFolderService to list folders
        service = KnowledgeFolderService(get_supabase_client())
        folders = await service.list_project_folders(project_id)

        safe_logfire_info(
            f"Project folders retrieved | project_id={project_id} | "
            f"folder_count={len(folders)}"
        )

        return {
            "success": True,
            "project_id": project_id,
            "folders": folders,
            "count": len(folders)
        }

    except Exception as e:
        safe_logfire_error(
            f"Failed to list project folders | error={str(e)} | "
            f"project_id={project_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e)}
        )
