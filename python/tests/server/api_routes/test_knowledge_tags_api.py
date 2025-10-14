"""
Integration tests for Knowledge Tags API endpoints

Tests tag retrieval and auto-tagging through the API layer.

Created: 2025-10-14
"""

import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from src.server.main import app


@pytest.fixture
def mock_tag_service():
    """Mock KnowledgeTagService."""
    with patch("src.server.api_routes.knowledge_tags_api.KnowledgeTagService") as mock:
        service_instance = mock.return_value
        service_instance.get_all_tags = AsyncMock()
        service_instance.get_tags_by_category = AsyncMock()
        yield service_instance


@pytest.fixture
def mock_auto_tagging_service():
    """Mock AutoTaggingService."""
    with patch("src.server.api_routes.knowledge_tags_api.AutoTaggingService") as mock:
        service_instance = mock.return_value
        service_instance.suggest_tags = AsyncMock()
        yield service_instance


@pytest.mark.asyncio
class TestGetAllTags:
    """Tests for GET /api/knowledge/tags endpoint."""

    async def test_get_all_tags_success(self, mock_tag_service):
        """Should return all tags."""
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
        mock_tag_service.get_all_tags.return_value = mock_tags

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/knowledge/tags")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["tags"] == mock_tags
        mock_tag_service.get_all_tags.assert_called_once_with(category=None)

    async def test_get_all_tags_with_category_filter(self, mock_tag_service):
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
        mock_tag_service.get_all_tags.return_value = mock_tags

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/knowledge/tags?category=framework")

        assert response.status_code == 200
        data = response.json()
        assert data["tags"] == mock_tags
        mock_tag_service.get_all_tags.assert_called_once_with(category="framework")

    async def test_get_all_tags_empty(self, mock_tag_service):
        """Should return empty list when no tags exist."""
        mock_tag_service.get_all_tags.return_value = []

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/knowledge/tags")

        assert response.status_code == 200
        data = response.json()
        assert data["tags"] == []

    async def test_get_all_tags_service_error(self, mock_tag_service):
        """Should return 500 on service error."""
        mock_tag_service.get_all_tags.side_effect = Exception("Database error")

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/knowledge/tags")

        assert response.status_code == 500
        data = response.json()
        assert "Database error" in data["detail"]


@pytest.mark.asyncio
class TestGetTagsByCategory:
    """Tests for GET /api/knowledge/tags/by-category endpoint."""

    async def test_get_tags_by_category_success(self, mock_tag_service):
        """Should return tags grouped by category."""
        mock_tags_by_category = {
            "framework": [
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
            ],
            "language": [
                {
                    "id": str(uuid4()),
                    "tag_name": "python",
                    "category": "language",
                    "description": "Python language",
                    "usage_count": 15,
                },
            ],
        }
        mock_tag_service.get_tags_by_category.return_value = mock_tags_by_category

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/knowledge/tags/by-category")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["tags_by_category"] == mock_tags_by_category
        mock_tag_service.get_tags_by_category.assert_called_once()

    async def test_get_tags_by_category_empty(self, mock_tag_service):
        """Should return empty dict when no tags exist."""
        mock_tag_service.get_tags_by_category.return_value = {}

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/knowledge/tags/by-category")

        assert response.status_code == 200
        data = response.json()
        assert data["tags_by_category"] == {}

    async def test_get_tags_by_category_service_error(self, mock_tag_service):
        """Should return 500 on service error."""
        mock_tag_service.get_tags_by_category.side_effect = Exception("Database error")

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/knowledge/tags/by-category")

        assert response.status_code == 500


@pytest.mark.asyncio
class TestSuggestTags:
    """Tests for POST /api/knowledge/tags/suggest endpoint."""

    async def test_suggest_tags_success(self, mock_auto_tagging_service):
        """Should suggest tags based on URL and content."""
        mock_auto_tagging_service.suggest_tags.return_value = ["react", "javascript", "testing"]

        payload = {
            "url": "https://react.dev/learn/installation",
            "title": "React Installation with Testing",
            "summary": "How to install React and set up testing",
        }

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/knowledge/tags/suggest", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["suggested_tags"] == ["react", "javascript", "testing"]
        mock_auto_tagging_service.suggest_tags.assert_called_once_with(
            url="https://react.dev/learn/installation",
            title="React Installation with Testing",
            summary="How to install React and set up testing",
        )

    async def test_suggest_tags_no_matches(self, mock_auto_tagging_service):
        """Should return empty list when no tags match."""
        mock_auto_tagging_service.suggest_tags.return_value = []

        payload = {
            "url": "https://example.com/random-page",
            "title": "Random Page",
            "summary": "Some random content",
        }

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/knowledge/tags/suggest", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["suggested_tags"] == []

    async def test_suggest_tags_empty_title_summary(self, mock_auto_tagging_service):
        """Should handle empty title and summary."""
        mock_auto_tagging_service.suggest_tags.return_value = ["react", "javascript"]

        payload = {
            "url": "https://react.dev/docs",
            "title": "",
            "summary": "",
        }

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/knowledge/tags/suggest", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert len(data["suggested_tags"]) >= 2

    async def test_suggest_tags_missing_required_fields(self, mock_auto_tagging_service):
        """Should return 422 when required fields are missing."""
        payload = {
            "title": "Some Title",
            "summary": "Some summary",
        }

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/knowledge/tags/suggest", json=payload)

        assert response.status_code == 422

    async def test_suggest_tags_service_error(self, mock_auto_tagging_service):
        """Should return 500 on service error."""
        mock_auto_tagging_service.suggest_tags.side_effect = Exception("Service error")

        payload = {
            "url": "https://react.dev/learn/installation",
            "title": "React Installation",
            "summary": "How to install React",
        }

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/knowledge/tags/suggest", json=payload)

        assert response.status_code == 500

    async def test_suggest_tags_multiple_sources(self, mock_auto_tagging_service):
        """Should combine tags from URL and content."""
        mock_auto_tagging_service.suggest_tags.return_value = [
            "react",
            "javascript",
            "authentication",
            "security",
            "testing",
        ]

        payload = {
            "url": "https://react.dev/learn/state-management",
            "title": "State Management with Testing",
            "summary": "Learn how to test React components with proper authentication",
        }

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/knowledge/tags/suggest", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert len(data["suggested_tags"]) == 5
        assert "react" in data["suggested_tags"]
        assert "authentication" in data["suggested_tags"]
        assert "testing" in data["suggested_tags"]
