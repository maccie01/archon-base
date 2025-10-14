"""
RAG Module for Archon MCP Server (HTTP-based version)

This module provides tools for:
- RAG query and search
- Source management
- Code example extraction and search

This version uses HTTP calls to the server service instead of importing
service modules directly, enabling true microservices architecture.
"""

import json
import logging
import os
from urllib.parse import urljoin

import httpx
from mcp.server.fastmcp import Context, FastMCP

# Import service discovery for HTTP communication
from src.server.config.service_discovery import get_api_url

logger = logging.getLogger(__name__)


def get_setting(key: str, default: str = "false") -> str:
    """Get a setting from environment variable."""
    return os.getenv(key, default)


def get_bool_setting(key: str, default: bool = False) -> bool:
    """Get a boolean setting from environment variable."""
    value = get_setting(key, "false" if not default else "true")
    return value.lower() in ("true", "1", "yes", "on")


def register_rag_tools(mcp: FastMCP):
    """Register all RAG tools with the MCP server."""

    @mcp.tool()
    async def rag_get_available_sources(
        ctx: Context,
        scope: str | None = None,
        project_id: str | None = None
    ) -> str:
        """
        Get list of available sources in the knowledge base with scope filtering.

        Args:
            scope: Filter by knowledge scope
                - "global": Only global knowledge sources
                - "project": Only project-specific sources
                - None: All sources (default)
            project_id: When scope="project", optionally filter by specific project

        Returns:
            JSON string with structure:
            - success: bool - Operation success status
            - sources: list[dict] - Array of source objects with scope, project_id, folder_name, tags
            - count: int - Total number of sources
            - scope_filter: str|null - Applied scope filter
            - project_filter: str|null - Applied project filter
            - error: str - Error description if success=false

        Usage Examples:
            # Get all sources
            rag_get_available_sources()

            # Get only global sources
            rag_get_available_sources(scope="global")

            # Get sources for specific project
            rag_get_available_sources(scope="project", project_id="proj_123")
        """
        try:
            api_url = get_api_url()
            timeout = httpx.Timeout(30.0, connect=5.0)

            async with httpx.AsyncClient(timeout=timeout) as client:
                params = {}
                if scope:
                    params["scope"] = scope
                if project_id:
                    params["project_id"] = project_id

                response = await client.get(
                    urljoin(api_url, "/api/rag/sources"),
                    params=params
                )

                if response.status_code == 200:
                    result = response.json()
                    sources = result.get("sources", [])

                    return json.dumps(
                        {
                            "success": True,
                            "sources": sources,
                            "count": len(sources),
                            "scope_filter": scope,
                            "project_filter": project_id,
                        },
                        indent=2
                    )
                else:
                    error_detail = response.text
                    return json.dumps(
                        {"success": False, "error": f"HTTP {response.status_code}: {error_detail}"},
                        indent=2,
                    )

        except Exception as e:
            logger.error(f"Error getting sources: {e}")
            return json.dumps({"success": False, "error": str(e)}, indent=2)

    @mcp.tool()
    async def rag_search_knowledge_base(
        ctx: Context,
        query: str,
        scope: str = "all",
        project_id: str | None = None,
        source_id: str | None = None,
        match_count: int = 5,
        return_mode: str = "pages"
    ) -> str:
        """
        Search knowledge base for relevant content using RAG with scope filtering.

        Args:
            query: Search query - Keep it SHORT and FOCUSED (2-5 keywords).
                   Good: "vector search", "authentication JWT", "React hooks"
                   Bad: "how to implement user authentication with JWT tokens in React with TypeScript and handle refresh tokens"
            scope: Knowledge scope to search
                - "all": Search all knowledge (global + current project if in context)
                - "global": Only search global knowledge sources
                - "project": Only search project-specific knowledge
            project_id: Project ID when scope="project" or scope="all" with project context
            source_id: Optional source ID filter from rag_get_available_sources().
                      This is the 'id' field from available sources, NOT a URL or domain name.
                      Example: "src_1234abcd" not "docs.anthropic.com"
            match_count: Max results (default: 5)
            return_mode: "pages" (default, full pages with metadata) or "chunks" (raw text chunks)

        Returns:
            JSON string with structure:
            - success: bool - Operation success status
            - results: list[dict] - Array of pages/chunks with content, metadata, scope indicators
            - search_scope: str - Scope used for search
            - project_context: str|null - Project ID if provided
            - return_mode: str - Mode used ("pages" or "chunks")
            - reranked: bool - Whether results were reranked
            - error: str|null - Error description if success=false

        Usage Examples:
            # Search only global knowledge
            rag_search_knowledge_base("React hooks", scope="global")

            # Search project-specific knowledge
            rag_search_knowledge_base("authentication flow", scope="project", project_id="proj_123")

            # Search all with project context (prioritizes project sources)
            rag_search_knowledge_base("API endpoints", scope="all", project_id="proj_123")

        Note: Use "pages" mode for better context (recommended), or "chunks" for raw granular results.
        After getting pages, use rag_read_full_page() to retrieve complete page content.
        """
        try:
            api_url = get_api_url()
            timeout = httpx.Timeout(30.0, connect=5.0)

            async with httpx.AsyncClient(timeout=timeout) as client:
                request_data = {
                    "query": query,
                    "scope": scope,
                    "match_count": match_count,
                    "return_mode": return_mode
                }
                if project_id:
                    request_data["project_id"] = project_id
                if source_id:
                    request_data["source"] = source_id

                response = await client.post(urljoin(api_url, "/api/rag/query"), json=request_data)

                if response.status_code == 200:
                    result = response.json()
                    return json.dumps(
                        {
                            "success": True,
                            "results": result.get("results", []),
                            "search_scope": scope,
                            "project_context": project_id,
                            "return_mode": result.get("return_mode", return_mode),
                            "reranked": result.get("reranked", False),
                            "error": None,
                        },
                        indent=2,
                    )
                else:
                    error_detail = response.text
                    return json.dumps(
                        {
                            "success": False,
                            "results": [],
                            "error": f"HTTP {response.status_code}: {error_detail}",
                        },
                        indent=2,
                    )

        except Exception as e:
            logger.error(f"Error performing RAG query: {e}")
            return json.dumps({"success": False, "results": [], "error": str(e)}, indent=2)

    @mcp.tool()
    async def rag_search_code_examples(
        ctx: Context, query: str, source_id: str | None = None, match_count: int = 5
    ) -> str:
        """
        Search for relevant code examples in the knowledge base.

        Args:
            query: Search query - Keep it SHORT and FOCUSED (2-5 keywords).
                   Good: "React useState", "FastAPI middleware", "vector pgvector"
                   Bad: "React hooks useState useEffect useContext useReducer useMemo useCallback"
            source_id: Optional source ID filter from rag_get_available_sources().
                      This is the 'id' field from available sources, NOT a URL or domain name.
                      Example: "src_1234abcd" not "docs.anthropic.com"
            match_count: Max results (default: 5)

        Returns:
            JSON string with structure:
            - success: bool - Operation success status
            - results: list[dict] - Array of code examples with content and summaries
            - reranked: bool - Whether results were reranked
            - error: str|null - Error description if success=false
        """
        try:
            api_url = get_api_url()
            timeout = httpx.Timeout(30.0, connect=5.0)

            async with httpx.AsyncClient(timeout=timeout) as client:
                request_data = {"query": query, "match_count": match_count}
                if source_id:
                    request_data["source"] = source_id

                # Call the dedicated code examples endpoint
                response = await client.post(
                    urljoin(api_url, "/api/rag/code-examples"), json=request_data
                )

                if response.status_code == 200:
                    result = response.json()
                    return json.dumps(
                        {
                            "success": True,
                            "results": result.get("results", []),
                            "reranked": result.get("reranked", False),
                            "error": None,
                        },
                        indent=2,
                    )
                else:
                    error_detail = response.text
                    return json.dumps(
                        {
                            "success": False,
                            "results": [],
                            "error": f"HTTP {response.status_code}: {error_detail}",
                        },
                        indent=2,
                    )

        except Exception as e:
            logger.error(f"Error searching code examples: {e}")
            return json.dumps({"success": False, "results": [], "error": str(e)}, indent=2)

    @mcp.tool()
    async def rag_list_pages_for_source(
        ctx: Context, source_id: str, section: str | None = None
    ) -> str:
        """
        List all pages for a given knowledge source.

        Use this after rag_get_available_sources() to see all pages in a source.
        Useful for browsing documentation structure or finding specific pages.

        Args:
            source_id: Source ID from rag_get_available_sources() (e.g., "src_1234abcd")
            section: Optional filter for llms-full.txt section title (e.g., "# Core Concepts")

        Returns:
            JSON string with structure:
            - success: bool - Operation success status
            - pages: list[dict] - Array of page objects with id, url, section_title, word_count
            - total: int - Total number of pages
            - source_id: str - The source ID that was queried
            - error: str|null - Error description if success=false

        Example workflow:
            1. Call rag_get_available_sources() to get source_id
            2. Call rag_list_pages_for_source(source_id) to see all pages
            3. Call rag_read_full_page(page_id) to read specific pages
        """
        try:
            api_url = get_api_url()
            timeout = httpx.Timeout(30.0, connect=5.0)

            async with httpx.AsyncClient(timeout=timeout) as client:
                params = {"source_id": source_id}
                if section:
                    params["section"] = section

                response = await client.get(
                    urljoin(api_url, "/api/pages"),
                    params=params
                )

                if response.status_code == 200:
                    result = response.json()
                    return json.dumps(
                        {
                            "success": True,
                            "pages": result.get("pages", []),
                            "total": result.get("total", 0),
                            "source_id": result.get("source_id", source_id),
                            "error": None,
                        },
                        indent=2,
                    )
                else:
                    error_detail = response.text
                    return json.dumps(
                        {
                            "success": False,
                            "pages": [],
                            "total": 0,
                            "source_id": source_id,
                            "error": f"HTTP {response.status_code}: {error_detail}",
                        },
                        indent=2,
                    )

        except Exception as e:
            logger.error(f"Error listing pages for source {source_id}: {e}")
            return json.dumps(
                {
                    "success": False,
                    "pages": [],
                    "total": 0,
                    "source_id": source_id,
                    "error": str(e)
                },
                indent=2
            )

    @mcp.tool()
    async def rag_read_full_page(
        ctx: Context, page_id: str | None = None, url: str | None = None
    ) -> str:
        """
        Retrieve full page content from knowledge base.
        Use this to get complete page content after RAG search.

        Args:
            page_id: Page UUID from search results (e.g., "550e8400-e29b-41d4-a716-446655440000")
            url: Page URL (e.g., "https://docs.example.com/getting-started")

        Note: Provide EITHER page_id OR url, not both.

        Returns:
            JSON string with structure:
            - success: bool
            - page: dict with full_content, title, url, metadata
            - error: str|null
        """
        try:
            if not page_id and not url:
                return json.dumps(
                    {"success": False, "error": "Must provide either page_id or url"},
                    indent=2
                )

            api_url = get_api_url()
            timeout = httpx.Timeout(30.0, connect=5.0)

            async with httpx.AsyncClient(timeout=timeout) as client:
                if page_id:
                    response = await client.get(urljoin(api_url, f"/api/pages/{page_id}"))
                else:
                    response = await client.get(
                        urljoin(api_url, "/api/pages/by-url"),
                        params={"url": url}
                    )

                if response.status_code == 200:
                    page_data = response.json()
                    return json.dumps(
                        {
                            "success": True,
                            "page": page_data,
                            "error": None,
                        },
                        indent=2,
                    )
                else:
                    error_detail = response.text
                    return json.dumps(
                        {
                            "success": False,
                            "page": None,
                            "error": f"HTTP {response.status_code}: {error_detail}",
                        },
                        indent=2,
                    )

        except Exception as e:
            logger.error(f"Error reading page: {e}")
            return json.dumps({"success": False, "page": None, "error": str(e)}, indent=2)

    @mcp.tool()
    async def rag_search_project_knowledge(
        ctx: Context,
        query: str,
        project_id: str,
        folder_name: str | None = None,
        match_count: int = 5
    ) -> str:
        """
        Search knowledge specific to a project with optional folder filtering.

        This is a convenience wrapper around rag_search_knowledge_base with
        project scope and additional folder filtering.

        Args:
            query: Search query - Keep it SHORT and FOCUSED (2-5 keywords).
                   Good: "database schema", "login endpoint", "payment flow"
                   Bad: "how do we implement the user authentication and login endpoint with OAuth"
            project_id: Project ID to search within
            folder_name: Optional folder name filter (e.g., "Authentication", "API")
            match_count: Maximum results (default: 5)

        Returns:
            JSON string with structure:
            - success: bool - Operation success status
            - results: list[dict] - Project-scoped results with folder information
            - project_id: str - Project ID searched
            - folder_filter: str|null - Folder name filter if provided
            - error: str|null - Error description if success=false

        Usage Examples:
            # Search all project knowledge
            rag_search_project_knowledge("database schema", "proj_123")

            # Search within specific folder
            rag_search_project_knowledge("login endpoint", "proj_123", folder_name="API")

            # Search authentication docs in Authentication folder
            rag_search_project_knowledge("OAuth flow", "proj_123", folder_name="Authentication")
        """
        try:
            api_url = get_api_url()
            timeout = httpx.Timeout(30.0, connect=5.0)

            async with httpx.AsyncClient(timeout=timeout) as client:
                request_data = {
                    "query": query,
                    "scope": "project",
                    "project_id": project_id,
                    "match_count": match_count,
                    "return_mode": "pages"
                }
                if folder_name:
                    request_data["folder_name"] = folder_name

                response = await client.post(urljoin(api_url, "/api/rag/query"), json=request_data)

                if response.status_code == 200:
                    result = response.json()
                    results = result.get("results", [])

                    # If folder_name specified, filter results by folder
                    if folder_name:
                        results = [
                            r for r in results
                            if r.get("folder_name") == folder_name
                        ]

                    return json.dumps(
                        {
                            "success": True,
                            "results": results,
                            "project_id": project_id,
                            "folder_filter": folder_name,
                            "error": None,
                        },
                        indent=2,
                    )
                else:
                    error_detail = response.text
                    return json.dumps(
                        {
                            "success": False,
                            "results": [],
                            "project_id": project_id,
                            "folder_filter": folder_name,
                            "error": f"HTTP {response.status_code}: {error_detail}",
                        },
                        indent=2,
                    )

        except Exception as e:
            logger.error(f"Error searching project knowledge: {e}")
            return json.dumps(
                {
                    "success": False,
                    "results": [],
                    "project_id": project_id,
                    "folder_filter": folder_name,
                    "error": str(e)
                },
                indent=2
            )

    @mcp.tool()
    async def rag_search_global_knowledge(
        ctx: Context,
        query: str,
        tags: list[str] | None = None,
        match_count: int = 5
    ) -> str:
        """
        Search global knowledge base with optional tag filtering.

        Convenience wrapper for searching only global knowledge sources.

        Args:
            query: Search query - Keep it SHORT and FOCUSED (2-5 keywords).
                   Good: "REST API design", "React hooks patterns", "OAuth security"
                   Bad: "how to design REST APIs with proper authentication and error handling"
            tags: Optional tag filters (e.g., ["react", "typescript"], ["security", "fastapi"])
            match_count: Maximum results (default: 5)

        Returns:
            JSON string with structure:
            - success: bool - Operation success status
            - results: list[dict] - Global knowledge results with tags
            - tag_filters: list[str]|null - Tags used for filtering
            - error: str|null - Error description if success=false

        Usage Examples:
            # Search all global knowledge
            rag_search_global_knowledge("REST API design")

            # Search global knowledge with specific tags
            rag_search_global_knowledge("authentication", tags=["security", "fastapi"])

            # Search framework documentation
            rag_search_global_knowledge("hooks patterns", tags=["react"])
        """
        try:
            api_url = get_api_url()
            timeout = httpx.Timeout(30.0, connect=5.0)

            async with httpx.AsyncClient(timeout=timeout) as client:
                request_data = {
                    "query": query,
                    "scope": "global",
                    "match_count": match_count,
                    "return_mode": "pages"
                }
                if tags:
                    request_data["tags"] = tags

                response = await client.post(urljoin(api_url, "/api/rag/query"), json=request_data)

                if response.status_code == 200:
                    result = response.json()
                    results = result.get("results", [])

                    # If tags specified, filter results by tags
                    if tags:
                        filtered_results = []
                        for r in results:
                            result_tags = r.get("tags", [])
                            if any(tag in result_tags for tag in tags):
                                filtered_results.append(r)
                        results = filtered_results

                    return json.dumps(
                        {
                            "success": True,
                            "results": results,
                            "tag_filters": tags,
                            "error": None,
                        },
                        indent=2,
                    )
                else:
                    error_detail = response.text
                    return json.dumps(
                        {
                            "success": False,
                            "results": [],
                            "tag_filters": tags,
                            "error": f"HTTP {response.status_code}: {error_detail}",
                        },
                        indent=2,
                    )

        except Exception as e:
            logger.error(f"Error searching global knowledge: {e}")
            return json.dumps(
                {
                    "success": False,
                    "results": [],
                    "tag_filters": tags,
                    "error": str(e)
                },
                indent=2
            )

    @mcp.tool()
    async def rag_list_project_folders(
        ctx: Context,
        project_id: str
    ) -> str:
        """
        List all knowledge folders for a project.

        Args:
            project_id: Project ID to list folders for

        Returns:
            JSON string with structure:
            - success: bool - Operation success status
            - project_id: str - Project ID queried
            - project_title: str|null - Project name if available
            - folders: list[dict] - Folders with id, name, description, source_count, color
            - total: int - Total number of folders
            - error: str|null - Error description if success=false

        Usage Examples:
            # List all folders for a project
            rag_list_project_folders("proj_123")

            # Use to discover available knowledge organization
            folders = rag_list_project_folders("proj_ecommerce")
            # Then search specific folder:
            # rag_search_project_knowledge("API endpoints", "proj_ecommerce", folder_name="API")
        """
        try:
            api_url = get_api_url()
            timeout = httpx.Timeout(30.0, connect=5.0)

            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(
                    urljoin(api_url, f"/api/knowledge/folders/projects/{project_id}/list")
                )

                if response.status_code == 200:
                    result = response.json()
                    return json.dumps(
                        {
                            "success": True,
                            "project_id": project_id,
                            "project_title": result.get("project_title"),
                            "folders": result.get("folders", []),
                            "total": len(result.get("folders", [])),
                            "error": None,
                        },
                        indent=2,
                    )
                else:
                    error_detail = response.text
                    return json.dumps(
                        {
                            "success": False,
                            "project_id": project_id,
                            "project_title": None,
                            "folders": [],
                            "total": 0,
                            "error": f"HTTP {response.status_code}: {error_detail}",
                        },
                        indent=2,
                    )

        except Exception as e:
            logger.error(f"Error listing project folders: {e}")
            return json.dumps(
                {
                    "success": False,
                    "project_id": project_id,
                    "project_title": None,
                    "folders": [],
                    "total": 0,
                    "error": str(e)
                },
                indent=2
            )

    # Log successful registration
    logger.info("✓ RAG tools registered (HTTP-based version)")
