"""
Unit tests for KnowledgeTagService

Tests tag retrieval and auto-tagging functionality.

Created: 2025-10-14
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from src.server.services.knowledge.knowledge_tag_service import KnowledgeTagService


@pytest.fixture
def mock_supabase():
    """Mock Supabase client."""
    mock = MagicMock()
    mock.from_ = MagicMock(return_value=mock)
    mock.select = MagicMock(return_value=mock)
    mock.eq = MagicMock(return_value=mock)
    mock.order = MagicMock(return_value=mock)
    mock.execute = MagicMock()  # Synchronous, not async
    return mock


@pytest.fixture
def tag_service(mock_supabase):
    """Create KnowledgeTagService with mocked Supabase client."""
    service = KnowledgeTagService(mock_supabase)
    return service


class TestGetAllTags:
    """Tests for get_all_tags method."""

    @pytest.mark.asyncio
    async def test_get_all_tags_success(self, tag_service, mock_supabase):
        """Should return all tags sorted by category and name."""
        mock_tags = [
            {
                "id": str(uuid4()),
                "tag_name": "react",
                "category": "framework",
                "description": "React framework",
                "usage_count": 10,
                "color_hex": "#61dafb",
            },
            {
                "id": str(uuid4()),
                "tag_name": "python",
                "category": "language",
                "description": "Python language",
                "usage_count": 15,
                "color_hex": "#3776ab",
            },
        ]
        mock_supabase.execute.return_value = MagicMock(data=mock_tags)

        result = await tag_service.get_all_tags()

        assert result == mock_tags
        mock_supabase.from_.assert_called_once_with("archon_knowledge_tags")
        mock_supabase.order.assert_any_call("category")
        mock_supabase.order.assert_any_call("tag_name")

    @pytest.mark.asyncio
    async def test_get_all_tags_with_category_filter(self, tag_service, mock_supabase):
        """Should filter tags by category."""
        mock_tags = [
            {
                "id": str(uuid4()),
                "tag_name": "react",
                "category": "framework",
                "description": "React framework",
                "usage_count": 10,
            },
        ]
        mock_supabase.execute.return_value = MagicMock(data=mock_tags)

        result = await tag_service.get_all_tags(category="framework")

        assert result == mock_tags
        mock_supabase.eq.assert_called_once_with("category", "framework")

    @pytest.mark.asyncio
    async def test_get_all_tags_empty(self, tag_service, mock_supabase):
        """Should return empty list when no tags exist."""
        mock_supabase.execute.return_value = MagicMock(data=[])

        result = await tag_service.get_all_tags()

        assert result == []

    @pytest.mark.asyncio
    async def test_get_all_tags_error(self, tag_service, mock_supabase):
        """Should raise exception on database error."""
        mock_supabase.execute.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            await tag_service.get_all_tags()


class TestGetTagByName:
    """Tests for get_tag_by_name method."""

    @pytest.mark.asyncio
    async def test_get_tag_by_name_success(self, tag_service, mock_supabase):
        """Should return tag by name."""
        mock_tag = {
            "id": str(uuid4()),
            "tag_name": "react",
            "category": "framework",
            "description": "React framework",
            "usage_count": 10,
            "color_hex": "#61dafb",
        }
        mock_supabase.execute.return_value = MagicMock(data=[mock_tag])

        result = await tag_service.get_tag_by_name("react")

        assert result == mock_tag
        mock_supabase.from_.assert_called_once_with("archon_knowledge_tags")
        mock_supabase.eq.assert_called_once_with("tag_name", "react")

    @pytest.mark.asyncio
    async def test_get_tag_by_name_not_found(self, tag_service, mock_supabase):
        """Should return None when tag not found."""
        mock_supabase.execute.return_value = MagicMock(data=[])

        result = await tag_service.get_tag_by_name("nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_tag_by_name_error(self, tag_service, mock_supabase):
        """Should raise exception on database error."""
        mock_supabase.execute.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            await tag_service.get_tag_by_name("react")


class TestGetTagsByCategory:
    """Tests for get_tags_by_category method."""

    @pytest.mark.asyncio
    async def test_get_tags_by_category_success(self, tag_service, mock_supabase):
        """Should return tags grouped by category."""
        mock_tags = [
            {
                "id": str(uuid4()),
                "tag_name": "react",
                "category": "framework",
                "description": "React framework",
                "usage_count": 10,
            },
            {
                "id": str(uuid4()),
                "tag_name": "nextjs",
                "category": "framework",
                "description": "Next.js framework",
                "usage_count": 8,
            },
            {
                "id": str(uuid4()),
                "tag_name": "python",
                "category": "language",
                "description": "Python language",
                "usage_count": 15,
            },
        ]
        mock_supabase.execute.return_value = MagicMock(data=mock_tags)

        result = await tag_service.get_tags_by_category()

        assert "framework" in result
        assert "language" in result
        assert len(result["framework"]) == 2
        assert len(result["language"]) == 1
        assert result["framework"][0]["tag_name"] == "react"
        assert result["language"][0]["tag_name"] == "python"

    @pytest.mark.asyncio
    async def test_get_tags_by_category_empty(self, tag_service, mock_supabase):
        """Should return empty dict when no tags exist."""
        mock_supabase.execute.return_value = MagicMock(data=[])

        result = await tag_service.get_tags_by_category()

        assert result == {}

    @pytest.mark.asyncio
    async def test_get_tags_by_category_error(self, tag_service, mock_supabase):
        """Should raise exception on database error."""
        mock_supabase.execute.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            await tag_service.get_tags_by_category()
