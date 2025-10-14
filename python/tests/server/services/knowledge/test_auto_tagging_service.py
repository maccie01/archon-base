"""
Unit tests for AutoTaggingService

Tests URL pattern matching and content keyword analysis for auto-tagging.

Created: 2025-10-14
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.server.services.knowledge.auto_tagging_service import AutoTaggingService


@pytest.fixture
def auto_tagging_service():
    """Create AutoTaggingService instance."""
    return AutoTaggingService()


class TestSuggestTags:
    """Tests for suggest_tags method."""

    @pytest.mark.asyncio
    async def test_suggest_tags_react_url(self, auto_tagging_service):
        """Should suggest React tags from react.dev URL."""
        url = "https://react.dev/learn/installation"
        title = "Installation Guide"
        summary = "How to install React"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "react" in result
        assert "javascript" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_nextjs_url(self, auto_tagging_service):
        """Should suggest Next.js tags from nextjs.org URL."""
        url = "https://nextjs.org/docs/getting-started"
        title = "Getting Started"
        summary = "Start building with Next.js"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "nextjs" in result
        assert "react" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_fastapi_url(self, auto_tagging_service):
        """Should suggest FastAPI tags from fastapi.tiangolo.com URL."""
        url = "https://fastapi.tiangolo.com/tutorial/first-steps/"
        title = "First Steps"
        summary = "Tutorial for FastAPI"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "fastapi" in result
        assert "python" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_github_url(self, auto_tagging_service):
        """Should suggest GitHub tags from github.com URL."""
        url = "https://github.com/facebook/react"
        title = "React Repository"
        summary = "The React library"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "github" in result
        assert "documentation" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_npm_url(self, auto_tagging_service):
        """Should suggest npm tags from npmjs.com URL."""
        url = "https://www.npmjs.com/package/react"
        title = "React Package"
        summary = "React npm package"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "npm" in result
        assert "javascript" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_typescript_url(self, auto_tagging_service):
        """Should suggest TypeScript tags from typescriptlang.org URL."""
        url = "https://www.typescriptlang.org/docs/handbook/intro.html"
        title = "TypeScript Handbook"
        summary = "Learn TypeScript"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "typescript" in result
        assert "javascript" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_tailwind_url(self, auto_tagging_service):
        """Should suggest Tailwind tags from tailwindcss.com URL."""
        url = "https://tailwindcss.com/docs/installation"
        title = "Installation"
        summary = "Install Tailwind CSS"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "tailwindcss" in result
        assert "css" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_supabase_url(self, auto_tagging_service):
        """Should suggest Supabase tags from supabase.com URL."""
        url = "https://supabase.com/docs/guides/database"
        title = "Database Guide"
        summary = "Using Supabase database"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "supabase" in result
        assert "database" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_authentication_content(self, auto_tagging_service):
        """Should suggest authentication tags from content keywords."""
        url = "https://example.com/docs"
        title = "User Authentication Guide"
        summary = "How to implement authentication and authorization"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "authentication" in result
        assert "security" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_testing_content(self, auto_tagging_service):
        """Should suggest testing tags from content keywords."""
        url = "https://example.com/docs"
        title = "Testing Best Practices"
        summary = "Learn about unit testing and integration testing"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "testing" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_deployment_content(self, auto_tagging_service):
        """Should suggest deployment tags from content keywords."""
        url = "https://example.com/docs"
        title = "Deployment Guide"
        summary = "How to deploy your application to production"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "deployment" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_docker_content(self, auto_tagging_service):
        """Should suggest Docker tags from content keywords."""
        url = "https://example.com/docs"
        title = "Docker Setup"
        summary = "Using Docker containers for development"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "docker" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_api_content(self, auto_tagging_service):
        """Should suggest API tags from content keywords."""
        url = "https://example.com/docs"
        title = "REST API Documentation"
        summary = "Building RESTful APIs with best practices"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "api" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_database_content(self, auto_tagging_service):
        """Should suggest database tags from content keywords."""
        url = "https://example.com/docs"
        title = "Database Design"
        summary = "SQL database schema design patterns"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "database" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_multiple_matches(self, auto_tagging_service):
        """Should combine tags from URL and content matches."""
        url = "https://react.dev/learn/state-management"
        title = "State Management with Testing"
        summary = "Learn how to test React components with proper authentication"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "react" in result
        assert "javascript" in result
        assert "testing" in result
        assert "authentication" in result
        assert "security" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_no_duplicates(self, auto_tagging_service):
        """Should not return duplicate tags."""
        url = "https://react.dev/learn/installation"
        title = "React Installation"
        summary = "Install React with JavaScript"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert len(result) == len(set(result))

    @pytest.mark.asyncio
    async def test_suggest_tags_case_insensitive(self, auto_tagging_service):
        """Should match keywords case-insensitively."""
        url = "https://example.com/docs"
        title = "AUTHENTICATION Guide"
        summary = "Learn about TESTING and DEPLOYMENT"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "authentication" in result
        assert "testing" in result
        assert "deployment" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_empty_content(self, auto_tagging_service):
        """Should handle empty title and summary."""
        url = "https://react.dev/docs"
        title = ""
        summary = ""

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "react" in result
        assert "javascript" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_no_matches(self, auto_tagging_service):
        """Should return empty list when no patterns match."""
        url = "https://example.com/random-page"
        title = "Random Page"
        summary = "Some random content"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert result == []

    @pytest.mark.asyncio
    async def test_suggest_tags_postgresql_url(self, auto_tagging_service):
        """Should suggest PostgreSQL tags from postgresql.org URL."""
        url = "https://www.postgresql.org/docs/current/"
        title = "PostgreSQL Documentation"
        summary = "Official PostgreSQL docs"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "postgresql" in result
        assert "database" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_docker_url(self, auto_tagging_service):
        """Should suggest Docker tags from docker.com URL."""
        url = "https://docs.docker.com/get-started/"
        title = "Get Started with Docker"
        summary = "Docker introduction"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "docker" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_vscode_url(self, auto_tagging_service):
        """Should suggest VS Code tags from code.visualstudio.com URL."""
        url = "https://code.visualstudio.com/docs"
        title = "VS Code Documentation"
        summary = "Learn VS Code"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "vscode" in result
        assert "tools" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_mdn_url(self, auto_tagging_service):
        """Should suggest MDN tags from developer.mozilla.org URL."""
        url = "https://developer.mozilla.org/en-US/docs/Web/JavaScript"
        title = "JavaScript Guide"
        summary = "MDN JavaScript documentation"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "mdn" in result
        assert "javascript" in result

    @pytest.mark.asyncio
    async def test_suggest_tags_stack_overflow_url(self, auto_tagging_service):
        """Should suggest Stack Overflow tags from stackoverflow.com URL."""
        url = "https://stackoverflow.com/questions/12345/some-question"
        title = "Some Question"
        summary = "Stack Overflow discussion"

        result = await auto_tagging_service.suggest_tags(url, title, summary)

        assert "stackoverflow" in result
        assert "qa" in result
