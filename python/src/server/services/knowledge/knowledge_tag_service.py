"""
Knowledge Tag Service

Handles knowledge tag operations including tag retrieval, categorization, and usage tracking.
"""

from typing import Any

from ...config.logfire_config import get_logger

logger = get_logger(__name__)


class KnowledgeTagService:
    """
    Service for managing knowledge tags.

    Provides operations for retrieving tag definitions, filtering by category,
    and tracking tag usage across knowledge sources.
    """

    def __init__(self, supabase_client):
        """
        Initialize the knowledge tag service.

        Args:
            supabase_client: The Supabase client for database operations
        """
        self.supabase = supabase_client

    async def get_all_tags(self, category: str | None = None) -> list[dict[str, Any]]:
        """
        Get all knowledge tags, optionally filtered by category.

        Args:
            category: Optional category filter (e.g., "framework", "language", "security")

        Returns:
            List of tag dicts with full metadata

        Raises:
            Exception: If tag retrieval fails
        """
        try:
            logger.info(f"Getting all tags | category={category}")

            # Build query
            query = self.supabase.from_("archon_knowledge_tags").select("*")

            # Apply category filter if provided
            if category:
                query = query.eq("category", category)

            # Order by usage count (descending) and then by tag name
            result = query.order("usage_count", desc=True).order("tag_name").execute()

            tags = result.data if result.data else []

            logger.info(f"Retrieved tags | count={len(tags)} | category={category}")

            return tags

        except Exception as e:
            logger.error(f"Failed to get tags | error={str(e)} | category={category}")
            raise

    async def get_tag_by_name(self, tag_name: str) -> dict[str, Any] | None:
        """
        Get a specific tag by its name.

        Args:
            tag_name: Name of the tag (e.g., "react", "python")

        Returns:
            Dict containing tag data, or None if not found
        """
        try:
            logger.info(f"Getting tag by name | tag_name={tag_name}")

            # Validate tag_name
            if not tag_name:
                return None

            # Normalize tag name to lowercase for consistent lookup
            normalized_name = tag_name.lower().strip()

            result = (
                self.supabase.from_("archon_knowledge_tags")
                .select("*")
                .ilike("tag_name", normalized_name)
                .single()
                .execute()
            )

            if not result.data:
                logger.info(f"Tag not found | tag_name={tag_name}")
                return None

            return result.data

        except Exception as e:
            # Log but don't raise for get operations - return None
            logger.warning(f"Failed to get tag by name | error={str(e)} | tag_name={tag_name}")
            return None

    async def get_tags_by_category(self) -> dict[str, list[str]]:
        """
        Get all tags organized by category.

        Returns:
            Dict mapping category names to lists of tag names
            Example: {"framework": ["react", "nextjs"], "language": ["python", "typescript"]}

        Raises:
            Exception: If tag retrieval fails
        """
        try:
            logger.info("Getting tags grouped by category")

            # Get all tags
            result = (
                self.supabase.from_("archon_knowledge_tags")
                .select("tag_name, category")
                .order("category")
                .order("tag_name")
                .execute()
            )

            tags = result.data if result.data else []

            # Group tags by category
            tags_by_category: dict[str, list[str]] = {}
            for tag in tags:
                category = tag["category"]
                tag_name = tag["tag_name"]

                if category not in tags_by_category:
                    tags_by_category[category] = []

                tags_by_category[category].append(tag_name)

            logger.info(
                f"Retrieved tags by category | categories={len(tags_by_category)} | total_tags={len(tags)}"
            )

            return tags_by_category

        except Exception as e:
            logger.error(f"Failed to get tags by category | error={str(e)}")
            raise

    async def increment_tag_usage(self, tag_name: str) -> None:
        """
        Increment the usage count for a tag.

        This should be called when a tag is added to a knowledge source.

        Args:
            tag_name: Name of the tag to increment

        Raises:
            Exception: If increment fails
        """
        try:
            logger.info(f"Incrementing tag usage | tag_name={tag_name}")

            # Validate tag_name
            if not tag_name:
                raise ValueError("tag_name is required")

            # Normalize tag name
            normalized_name = tag_name.lower().strip()

            # Check if tag exists
            tag = await self.get_tag_by_name(normalized_name)
            if not tag:
                logger.warning(
                    f"Cannot increment usage for non-existent tag | tag_name={normalized_name}"
                )
                return

            # Increment usage count
            current_count = tag.get("usage_count", 0)
            new_count = current_count + 1

            result = (
                self.supabase.from_("archon_knowledge_tags")
                .update({"usage_count": new_count})
                .ilike("tag_name", normalized_name)
                .execute()
            )

            if result.data:
                logger.info(
                    f"Tag usage incremented | tag_name={normalized_name} | new_count={new_count}"
                )
            else:
                logger.warning(f"Tag usage increment returned no data | tag_name={normalized_name}")

        except Exception as e:
            logger.error(
                f"Failed to increment tag usage | error={str(e)} | tag_name={tag_name}"
            )
            raise

    async def decrement_tag_usage(self, tag_name: str) -> None:
        """
        Decrement the usage count for a tag.

        This should be called when a tag is removed from a knowledge source.
        Usage count will not go below 0.

        Args:
            tag_name: Name of the tag to decrement

        Raises:
            Exception: If decrement fails
        """
        try:
            logger.info(f"Decrementing tag usage | tag_name={tag_name}")

            # Validate tag_name
            if not tag_name:
                raise ValueError("tag_name is required")

            # Normalize tag name
            normalized_name = tag_name.lower().strip()

            # Check if tag exists
            tag = await self.get_tag_by_name(normalized_name)
            if not tag:
                logger.warning(
                    f"Cannot decrement usage for non-existent tag | tag_name={normalized_name}"
                )
                return

            # Decrement usage count (minimum 0)
            current_count = tag.get("usage_count", 0)
            new_count = max(0, current_count - 1)

            result = (
                self.supabase.from_("archon_knowledge_tags")
                .update({"usage_count": new_count})
                .ilike("tag_name", normalized_name)
                .execute()
            )

            if result.data:
                logger.info(
                    f"Tag usage decremented | tag_name={normalized_name} | new_count={new_count}"
                )
            else:
                logger.warning(f"Tag usage decrement returned no data | tag_name={normalized_name}")

        except Exception as e:
            logger.error(
                f"Failed to decrement tag usage | error={str(e)} | tag_name={tag_name}"
            )
            raise
