"""
Knowledge Tags API Module

This module handles tag management and auto-tagging operations.
Tags provide categorical organization across all knowledge sources.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..middleware.auth_middleware import require_auth

from ..config.logfire_config import get_logger, safe_logfire_error, safe_logfire_info
from ..services.knowledge import AutoTaggingService, KnowledgeTagService
from ..utils import get_supabase_client

# Get logger for this module
logger = get_logger(__name__)

# Create router
router = APIRouter(prefix="/api/knowledge/tags", tags=["knowledge-tags"])


# Pydantic models
class SuggestTagsRequest(BaseModel):
    url: str
    title: str
    summary: str

    class Config:
        schema_extra = {
            "example": {
                "url": "https://react.dev",
                "title": "React Documentation",
                "summary": "Learn React with comprehensive documentation covering hooks, components, and best practices"
            }
        }


@router.get("")
async def get_tags(category: str | None = None, auth = Depends(require_auth)):
    """
    Get all knowledge tags, optionally filtered by category.

    Args:
        category: Optional category filter (framework, language, architecture, etc.)

    Returns:
        List of tags with metadata and usage counts
    """
    try:
        safe_logfire_info(f"Getting knowledge tags | category={category}")

        # Use KnowledgeTagService to get tags
        service = KnowledgeTagService(get_supabase_client())
        tags = await service.get_all_tags(category=category)

        safe_logfire_info(
            f"Knowledge tags retrieved | tag_count={len(tags)} | category={category}"
        )

        return {
            "success": True,
            "tags": tags,
            "count": len(tags)
        }

    except Exception as e:
        safe_logfire_error(
            f"Failed to get knowledge tags | error={str(e)} | category={category}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e)}
        )


@router.get("/{tag_name}")
async def get_tag(tag_name: str, auth = Depends(require_auth)):
    """
    Get a specific tag by name.

    Args:
        tag_name: Name of the tag (case-insensitive)

    Returns:
        Tag with all metadata and usage information
    """
    try:
        safe_logfire_info(f"Getting specific tag | tag_name={tag_name}")

        # Use KnowledgeTagService to get tag
        service = KnowledgeTagService(get_supabase_client())
        tag = await service.get_tag_by_name(tag_name)

        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": f"Tag '{tag_name}' not found"}
            )

        safe_logfire_info(f"Tag retrieved | tag_name={tag_name}")

        return {
            "success": True,
            "tag": tag
        }

    except HTTPException:
        raise
    except Exception as e:
        safe_logfire_error(
            f"Failed to get tag | error={str(e)} | tag_name={tag_name}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e)}
        )


@router.get("/categories/grouped")
async def get_tags_by_category(auth = Depends(require_auth)):
    """
    Get all tags organized by category.

    Returns:
        Dictionary mapping category names to lists of tag names
    """
    try:
        safe_logfire_info("Getting tags grouped by category")

        # Use KnowledgeTagService to get grouped tags
        service = KnowledgeTagService(get_supabase_client())
        categories = await service.get_tags_by_category()

        # Count tags per category
        category_counts = {cat: len(tags) for cat, tags in categories.items()}

        safe_logfire_info(
            f"Tags grouped by category | category_count={len(categories)} | "
            f"total_tags={sum(category_counts.values())}"
        )

        return {
            "success": True,
            "categories": categories,
            "category_counts": category_counts,
            "total_tags": sum(category_counts.values())
        }

    except Exception as e:
        safe_logfire_error(
            f"Failed to get tags by category | error={str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e)}
        )


@router.post("/suggest")
async def suggest_tags(request: SuggestTagsRequest, auth = Depends(require_auth)):
    """
    Suggest tags for a knowledge source based on URL and content.

    Uses pattern matching and keyword analysis to recommend appropriate tags.

    Args:
        request: Contains URL, title, and summary for tag suggestion

    Returns:
        List of suggested tag names
    """
    try:
        safe_logfire_info(
            f"Suggesting tags | url={request.url} | title={request.title[:50]}"
        )

        # Use AutoTaggingService to suggest tags
        service = AutoTaggingService()
        suggested_tags = await service.suggest_tags(
            url=request.url,
            title=request.title,
            summary=request.summary
        )

        safe_logfire_info(
            f"Tags suggested | url={request.url} | tag_count={len(suggested_tags)} | "
            f"tags={suggested_tags}"
        )

        return {
            "success": True,
            "suggested_tags": suggested_tags,
            "count": len(suggested_tags),
            "source": {
                "url": request.url,
                "title": request.title
            }
        }

    except Exception as e:
        safe_logfire_error(
            f"Failed to suggest tags | error={str(e)} | url={request.url}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": str(e)}
        )
