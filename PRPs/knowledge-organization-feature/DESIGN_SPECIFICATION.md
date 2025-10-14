# Two-Layer Knowledge Organization System - Design Specification

**Version**: 1.0
**Date**: 2025-01-14
**Author**: Archon Design Team
**Status**: Design Phase

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current State Analysis](#current-state-analysis)
3. [Design Goals](#design-goals)
4. [Database Schema Design](#database-schema-design)
5. [Tagging & Index System](#tagging--index-system)
6. [MCP Tool Enhancements](#mcp-tool-enhancements)
7. [API Endpoint Changes](#api-endpoint-changes)
8. [UI Structure](#ui-structure)
9. [Search Strategy for Agents](#search-strategy-for-agents)
10. [Implementation Phases](#implementation-phases)
11. [Migration Strategy](#migration-strategy)
12. [Testing Strategy](#testing-strategy)

---

## Executive Summary

This document outlines a comprehensive 2-layer knowledge organization system for Archon, designed to separate global knowledge (shared across all work) from project-specific knowledge (scoped to individual projects). The system provides clear discernability for AI agents through MCP tools, organized UI navigation, and a robust tagging system.

### Key Benefits

- **Clear Separation**: Global vs Project-specific knowledge with distinct storage and retrieval
- **Agent Discernability**: MCP tools designed for easy identification and scoped searching
- **Organized UI**: Tab-based navigation with folder structures for projects
- **Efficient Search**: Optimized query patterns for agents to find relevant knowledge quickly
- **Scalability**: Foundation for multi-project knowledge management

---

## Current State Analysis

### Existing Architecture

**Database Schema** (`archon_sources` table):
```sql
CREATE TABLE archon_sources (
    source_id TEXT PRIMARY KEY,
    source_url TEXT,
    source_display_name TEXT,
    summary TEXT,
    total_word_count INTEGER DEFAULT 0,
    title TEXT,
    metadata JSONB DEFAULT '{}',  -- Contains knowledge_type, tags
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
);
```

**Current MCP Tools**:
- `rag_get_available_sources()` - Lists all sources without scope distinction
- `rag_search_knowledge_base(query, source_id, match_count, return_mode)` - Searches all knowledge
- `rag_search_code_examples(query, source_id, match_count)` - Searches all code examples
- `rag_list_pages_for_source(source_id, section)` - Lists pages within a source
- `rag_read_full_page(page_id, url)` - Retrieves full page content

**Current UI**: Single list view showing all knowledge items without hierarchical organization.

### Limitations

1. No separation between global and project-specific knowledge
2. Agents cannot easily identify which knowledge applies to which context
3. No folder/organizational structure for project knowledge
4. Tags exist but lack descriptions and usage guidelines
5. Search results mix global and project-specific content without distinction

---

## Design Goals

### Primary Objectives

1. **Two-Layer Separation**
   - Global knowledge accessible from any context
   - Project-specific knowledge scoped to individual projects
   - Clear database-level distinction

2. **MCP Discernability**
   - Dedicated tools for global vs project searches
   - Scope parameter in search tools
   - Clear metadata indicating knowledge scope

3. **UI Organization**
   - Tab-based interface: Global / Projects / Tags
   - Project folders with nested knowledge items
   - Visual indicators for scope

4. **Tagging System**
   - Predefined tag categories with descriptions
   - Usage guidelines for consistent tagging
   - Auto-tagging rules for common patterns

5. **Search Optimization**
   - Context-aware search (know which project agent is working on)
   - Scoped queries with clear syntax
   - Template patterns for agent CLAUDE.md files

### Non-Goals

- Multi-user collaboration (single-user deployment remains)
- Fine-grained permissions (all knowledge accessible to user)
- Real-time knowledge synchronization across projects
- Knowledge versioning/history (use existing version control for projects)

---

## Database Schema Design

### 1. Add Scope and Project Tracking to `archon_sources`

```sql
-- Migration: 012_add_knowledge_scope_and_project_linking.sql

-- Add scope column to archon_sources
ALTER TABLE archon_sources
ADD COLUMN knowledge_scope TEXT DEFAULT 'global' CHECK (knowledge_scope IN ('global', 'project')),
ADD COLUMN project_id UUID REFERENCES archon_projects(id) ON DELETE CASCADE;

-- Add index for scope filtering
CREATE INDEX idx_archon_sources_scope ON archon_sources(knowledge_scope);

-- Add composite index for project-scoped queries
CREATE INDEX idx_archon_sources_project_scope ON archon_sources(project_id, knowledge_scope)
WHERE project_id IS NOT NULL;

-- Add constraint: project_id required when scope is 'project'
ALTER TABLE archon_sources
ADD CONSTRAINT chk_project_scope
CHECK (
    (knowledge_scope = 'global' AND project_id IS NULL) OR
    (knowledge_scope = 'project' AND project_id IS NOT NULL)
);

-- Add comments
COMMENT ON COLUMN archon_sources.knowledge_scope IS 'Scope of knowledge: global (shared) or project (specific to a project)';
COMMENT ON COLUMN archon_sources.project_id IS 'Foreign key to archon_projects when knowledge_scope=project';
```

### 2. Create Knowledge Tags Table

```sql
-- Create knowledge_tags table for tag definitions
CREATE TABLE IF NOT EXISTS archon_knowledge_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tag_name TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    usage_guidelines TEXT,
    color_hex TEXT,
    icon_name TEXT,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    -- Tag categories: framework, language, architecture, security, testing, deployment, documentation
    CONSTRAINT chk_tag_category CHECK (category IN (
        'framework',
        'language',
        'architecture',
        'security',
        'testing',
        'deployment',
        'documentation',
        'database',
        'api',
        'ui',
        'general'
    ))
);

-- Create indexes
CREATE INDEX idx_knowledge_tags_category ON archon_knowledge_tags(category);
CREATE INDEX idx_knowledge_tags_name ON archon_knowledge_tags(tag_name);

-- Create trigger for updated_at
CREATE TRIGGER update_archon_knowledge_tags_updated_at
    BEFORE UPDATE ON archon_knowledge_tags
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Enable RLS
ALTER TABLE archon_knowledge_tags ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access to archon_knowledge_tags"
    ON archon_knowledge_tags FOR SELECT TO public
    USING (true);
```

### 3. Create Project Knowledge Folders Table

```sql
-- Create project knowledge folders for organization
CREATE TABLE IF NOT EXISTS archon_project_knowledge_folders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES archon_projects(id) ON DELETE CASCADE,
    folder_name TEXT NOT NULL,
    description TEXT,
    color_hex TEXT DEFAULT '#6366f1',
    icon_name TEXT DEFAULT 'folder',
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    -- Ensure unique folder names per project
    UNIQUE(project_id, folder_name)
);

-- Add folder_id to archon_sources for project-scoped knowledge
ALTER TABLE archon_sources
ADD COLUMN folder_id UUID REFERENCES archon_project_knowledge_folders(id) ON DELETE SET NULL;

-- Create indexes
CREATE INDEX idx_project_folders_project_id ON archon_project_knowledge_folders(project_id);
CREATE INDEX idx_project_folders_sort_order ON archon_project_knowledge_folders(project_id, sort_order);
CREATE INDEX idx_sources_folder_id ON archon_sources(folder_id);

-- Create trigger
CREATE TRIGGER update_archon_project_knowledge_folders_updated_at
    BEFORE UPDATE ON archon_project_knowledge_folders
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Enable RLS
ALTER TABLE archon_project_knowledge_folders ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access to archon_project_knowledge_folders"
    ON archon_project_knowledge_folders FOR SELECT TO public
    USING (true);

-- Add constraint: folder_id only allowed when scope is 'project'
ALTER TABLE archon_sources
ADD CONSTRAINT chk_folder_project_scope
CHECK (
    (knowledge_scope = 'global' AND folder_id IS NULL) OR
    (knowledge_scope = 'project')
);

-- Add comment
COMMENT ON TABLE archon_project_knowledge_folders IS 'Organizational folders for project-specific knowledge sources';
COMMENT ON COLUMN archon_sources.folder_id IS 'Optional folder for organizing project-scoped knowledge';
```

### 4. Seed Standard Tags

```sql
-- Insert standard tag definitions
INSERT INTO archon_knowledge_tags (tag_name, category, description, usage_guidelines, color_hex) VALUES
-- Framework Tags
('react', 'framework', 'React framework for building user interfaces', 'Use for React-specific documentation, component patterns, hooks usage', '#61dafb'),
('nextjs', 'framework', 'Next.js React framework', 'Use for Next.js routing, SSR, API routes', '#000000'),
('fastapi', 'framework', 'FastAPI Python web framework', 'Use for FastAPI endpoints, dependency injection, Pydantic models', '#009688'),
('django', 'framework', 'Django Python web framework', 'Use for Django models, views, ORM', '#092e20'),
('express', 'framework', 'Express.js Node framework', 'Use for Express routing, middleware', '#000000'),

-- Language Tags
('python', 'language', 'Python programming language', 'Use for Python code, syntax, standard library', '#3776ab'),
('typescript', 'language', 'TypeScript programming language', 'Use for TypeScript code, types, interfaces', '#3178c6'),
('javascript', 'language', 'JavaScript programming language', 'Use for vanilla JS, ES6+ features', '#f7df1e'),
('rust', 'language', 'Rust programming language', 'Use for Rust code, ownership patterns', '#ce412b'),
('go', 'language', 'Go programming language', 'Use for Go code, concurrency patterns', '#00add8'),

-- Architecture Tags
('microservices', 'architecture', 'Microservices architecture pattern', 'Use for service design, inter-service communication', '#4caf50'),
('rest-api', 'architecture', 'REST API design and implementation', 'Use for RESTful endpoint design, HTTP methods', '#ff9800'),
('graphql', 'architecture', 'GraphQL API design', 'Use for GraphQL schemas, resolvers, queries', '#e535ab'),
('event-driven', 'architecture', 'Event-driven architecture', 'Use for event sourcing, message queues, pub/sub', '#2196f3'),
('monolith', 'architecture', 'Monolithic architecture', 'Use for single-codebase applications', '#9e9e9e'),

-- Security Tags
('authentication', 'security', 'Authentication mechanisms', 'Use for login systems, OAuth, JWT, session management', '#f44336'),
('authorization', 'security', 'Authorization and access control', 'Use for permissions, RBAC, policies', '#e91e63'),
('encryption', 'security', 'Data encryption', 'Use for TLS, data-at-rest encryption, hashing', '#9c27b0'),
('security-best-practices', 'security', 'General security best practices', 'Use for OWASP guidelines, secure coding', '#673ab7'),

-- Testing Tags
('unit-testing', 'testing', 'Unit testing practices', 'Use for test frameworks, mocking, assertions', '#8bc34a'),
('integration-testing', 'testing', 'Integration testing', 'Use for API tests, database integration', '#4caf50'),
('e2e-testing', 'testing', 'End-to-end testing', 'Use for Playwright, Cypress, full user flows', '#009688'),

-- Deployment Tags
('docker', 'deployment', 'Docker containerization', 'Use for Dockerfile, docker-compose, container best practices', '#2496ed'),
('kubernetes', 'deployment', 'Kubernetes orchestration', 'Use for K8s manifests, deployments, services', '#326ce5'),
('ci-cd', 'deployment', 'CI/CD pipelines', 'Use for GitHub Actions, GitLab CI, automated deployments', '#2088ff'),

-- Database Tags
('postgresql', 'database', 'PostgreSQL database', 'Use for Postgres-specific features, queries, indexes', '#336791'),
('mongodb', 'database', 'MongoDB NoSQL database', 'Use for document models, aggregation pipelines', '#47a248'),
('redis', 'database', 'Redis in-memory data store', 'Use for caching, pub/sub, data structures', '#dc382d'),
('vector-search', 'database', 'Vector similarity search', 'Use for embeddings, pgvector, semantic search', '#6366f1'),

-- API Tags
('openapi', 'api', 'OpenAPI/Swagger specification', 'Use for API documentation, schema definitions', '#85ea2d'),
('websockets', 'api', 'WebSocket real-time communication', 'Use for bidirectional communication, Socket.IO', '#010101'),

-- UI Tags
('tailwind', 'ui', 'Tailwind CSS framework', 'Use for utility-first CSS, responsive design', '#06b6d4'),
('radix-ui', 'ui', 'Radix UI primitives', 'Use for accessible components, headless UI', '#8b5cf6'),
('design-system', 'ui', 'Design system and components', 'Use for UI patterns, component libraries', '#f59e0b'),

-- Documentation Tags
('api-reference', 'documentation', 'API reference documentation', 'Use for endpoint docs, request/response formats', '#3b82f6'),
('tutorial', 'documentation', 'Tutorial and how-to guides', 'Use for step-by-step instructions, learning paths', '#10b981'),
('architecture-docs', 'documentation', 'Architecture documentation', 'Use for system design docs, diagrams, ADRs', '#8b5cf6'),
('troubleshooting', 'documentation', 'Troubleshooting and debugging', 'Use for error resolution, common issues', '#ef4444')

ON CONFLICT (tag_name) DO NOTHING;
```

### 5. Update Existing Data

```sql
-- Migration function to set default scope for existing sources
UPDATE archon_sources
SET knowledge_scope = 'global'
WHERE knowledge_scope IS NULL;

-- Optionally: Update metadata to include scope for backward compatibility
UPDATE archon_sources
SET metadata = jsonb_set(
    COALESCE(metadata, '{}'::jsonb),
    '{knowledge_scope}',
    to_jsonb(knowledge_scope)
);
```

---

## Tagging & Index System

### Tag Categories

1. **framework** - Web frameworks, libraries (React, FastAPI, Django)
2. **language** - Programming languages (Python, TypeScript, Rust)
3. **architecture** - Architecture patterns (Microservices, REST API, GraphQL)
4. **security** - Security practices (Authentication, Encryption)
5. **testing** - Testing methodologies (Unit, Integration, E2E)
6. **deployment** - Deployment tools (Docker, Kubernetes, CI/CD)
7. **database** - Database systems (PostgreSQL, MongoDB, Redis)
8. **api** - API specifications (OpenAPI, WebSockets)
9. **ui** - UI frameworks and patterns (Tailwind, Radix UI)
10. **documentation** - Documentation types (API Ref, Tutorials)
11. **general** - Catch-all for uncategorized tags

### Tag Schema

Each tag includes:
- **tag_name**: Unique identifier (e.g., "react", "fastapi")
- **category**: One of the categories above
- **description**: Clear explanation of what the tag represents
- **usage_guidelines**: When and how to use the tag
- **color_hex**: Visual identifier in UI
- **icon_name**: Icon for UI display
- **usage_count**: Track how often tag is used

### Auto-Tagging Rules

Auto-tagging triggers during source creation/crawl:

```python
# python/src/server/services/knowledge/auto_tagging_service.py

class AutoTaggingService:
    """Service for automatically applying tags based on content analysis."""

    # URL pattern matching
    URL_TAG_PATTERNS = {
        r'react\.dev|reactjs\.org': ['react', 'javascript'],
        r'nextjs\.org': ['nextjs', 'react'],
        r'fastapi\.tiangolo\.com': ['fastapi', 'python'],
        r'docs\.docker\.com': ['docker', 'deployment'],
        r'postgresql\.org': ['postgresql', 'database'],
        # ... more patterns
    }

    # Content keyword matching (in page titles, summaries)
    CONTENT_TAG_KEYWORDS = {
        'authentication': ['authentication', 'security'],
        'testing': ['testing'],
        'api reference': ['api-reference', 'documentation'],
        'tutorial': ['tutorial', 'documentation'],
        # ... more keywords
    }

    def suggest_tags(self, url: str, title: str, summary: str) -> list[str]:
        """Suggest tags based on URL patterns and content analysis."""
        suggested_tags = []

        # Check URL patterns
        for pattern, tags in self.URL_TAG_PATTERNS.items():
            if re.search(pattern, url, re.IGNORECASE):
                suggested_tags.extend(tags)

        # Check content keywords
        content = f"{title} {summary}".lower()
        for keyword, tags in self.CONTENT_TAG_KEYWORDS.items():
            if keyword in content:
                suggested_tags.extend(tags)

        # Remove duplicates, maintain order
        return list(dict.fromkeys(suggested_tags))
```

### Tag Management UI

**GET /api/knowledge/tags**
```json
{
  "tags": [
    {
      "id": "uuid",
      "tag_name": "react",
      "category": "framework",
      "description": "React framework for building user interfaces",
      "usage_guidelines": "Use for React-specific documentation, component patterns, hooks usage",
      "color_hex": "#61dafb",
      "icon_name": "react-icon",
      "usage_count": 15
    }
  ],
  "categories": [
    {
      "name": "framework",
      "count": 5,
      "tags": ["react", "nextjs", "fastapi", "django", "express"]
    }
  ]
}
```

---

## MCP Tool Enhancements

### Updated Tool Signatures

#### 1. Enhanced `rag_get_available_sources` with Scope Filter

```python
@mcp.tool()
async def rag_get_available_sources(
    ctx: Context,
    scope: str | None = None,  # "global", "project", or None for all
    project_id: str | None = None  # Filter by project when scope="project"
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
        {
            "success": bool,
            "sources": [
                {
                    "id": "src_abc123",
                    "title": "React Documentation",
                    "scope": "global",
                    "project_id": null,
                    "project_title": null,
                    "folder_name": null,
                    "tags": ["react", "javascript"],
                    "summary": "...",
                    "url": "https://react.dev"
                },
                {
                    "id": "src_xyz789",
                    "title": "Custom Auth Implementation",
                    "scope": "project",
                    "project_id": "proj_123",
                    "project_title": "E-commerce Platform",
                    "folder_name": "Authentication",
                    "tags": ["authentication", "security"],
                    "summary": "...",
                    "url": "file://auth-spec.md"
                }
            ],
            "count": 2,
            "scope_filter": "global",
            "project_filter": null
        }

    Usage Examples:
        # Get all sources
        rag_get_available_sources()

        # Get only global sources
        rag_get_available_sources(scope="global")

        # Get sources for specific project
        rag_get_available_sources(scope="project", project_id="proj_123")
    """
```

#### 2. Enhanced `rag_search_knowledge_base` with Scope Parameter

```python
@mcp.tool()
async def rag_search_knowledge_base(
    ctx: Context,
    query: str,
    scope: str = "all",  # "global", "project", "all"
    project_id: str | None = None,  # Required when scope="project"
    source_id: str | None = None,  # Existing parameter
    match_count: int = 5,
    return_mode: str = "pages"
) -> str:
    """
    Search knowledge base with scope filtering.

    Args:
        query: Search query (keep SHORT and FOCUSED - 2-5 keywords)
        scope: Knowledge scope to search
            - "all": Search all knowledge (global + current project if in context)
            - "global": Only search global knowledge sources
            - "project": Only search project-specific knowledge
        project_id: Project ID when scope="project" or scope="all" with project context
        source_id: Optional specific source filter
        match_count: Maximum results (default: 5)
        return_mode: "pages" (full pages) or "chunks" (raw chunks)

    Returns:
        JSON with search results including scope indicators:
        {
            "success": true,
            "results": [
                {
                    "page_id": "uuid",
                    "url": "https://...",
                    "title": "...",
                    "preview": "...",
                    "source_id": "src_abc",
                    "scope": "global",
                    "project_id": null,
                    "similarity": 0.89,
                    "tags": ["react", "hooks"]
                }
            ],
            "search_scope": "global",
            "project_context": null,
            "return_mode": "pages"
        }

    Usage Examples:
        # Search only global knowledge
        rag_search_knowledge_base("React hooks", scope="global")

        # Search project-specific knowledge
        rag_search_knowledge_base("authentication flow", scope="project", project_id="proj_123")

        # Search all with project context (prioritizes project sources)
        rag_search_knowledge_base("API endpoints", scope="all", project_id="proj_123")
    """
```

#### 3. New Tool: `rag_search_project_knowledge`

```python
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
        query: Search query (keep SHORT and FOCUSED)
        project_id: Project ID to search within
        folder_name: Optional folder name filter (e.g., "Authentication", "API")
        match_count: Maximum results

    Returns:
        JSON with project-scoped results including folder information

    Usage:
        # Search all project knowledge
        rag_search_project_knowledge("database schema", "proj_123")

        # Search within specific folder
        rag_search_project_knowledge("login endpoint", "proj_123", folder_name="API")
    """
```

#### 4. New Tool: `rag_search_global_knowledge`

```python
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
        query: Search query (keep SHORT and FOCUSED)
        tags: Optional tag filters (e.g., ["react", "typescript"])
        match_count: Maximum results

    Returns:
        JSON with global knowledge results

    Usage:
        # Search all global knowledge
        rag_search_global_knowledge("REST API design")

        # Search global knowledge with tags
        rag_search_global_knowledge("authentication", tags=["security", "fastapi"])
    """
```

#### 5. New Tool: `rag_list_project_folders`

```python
@mcp.tool()
async def rag_list_project_folders(
    ctx: Context,
    project_id: str
) -> str:
    """
    List all knowledge folders for a project.

    Args:
        project_id: Project ID

    Returns:
        JSON with folder list:
        {
            "success": true,
            "project_id": "proj_123",
            "project_title": "E-commerce Platform",
            "folders": [
                {
                    "id": "folder_1",
                    "name": "Authentication",
                    "description": "Auth system documentation",
                    "source_count": 3,
                    "color": "#6366f1"
                }
            ]
        }
    """
```

---

## API Endpoint Changes

### New Endpoints

#### 1. **GET /api/knowledge/global**
Get all global knowledge sources.

**Response**:
```json
{
  "items": [
    {
      "id": "src_abc123",
      "title": "React Documentation",
      "url": "https://react.dev",
      "scope": "global",
      "source_type": "url",
      "tags": ["react", "javascript", "framework"],
      "metadata": {
        "knowledge_type": "technical",
        "chunks_count": 150,
        "code_examples_count": 45
      }
    }
  ],
  "total": 10,
  "page": 1,
  "per_page": 20
}
```

#### 2. **GET /api/knowledge/projects/:projectId**
Get knowledge sources for a specific project.

**Query Parameters**:
- `folder_id` (optional): Filter by folder
- `page`, `per_page`: Pagination

**Response**:
```json
{
  "project_id": "proj_123",
  "project_title": "E-commerce Platform",
  "items": [
    {
      "id": "src_xyz789",
      "title": "Payment Gateway Integration",
      "scope": "project",
      "project_id": "proj_123",
      "folder_id": "folder_payment",
      "folder_name": "Payment System",
      "tags": ["payment", "api", "stripe"],
      "metadata": {...}
    }
  ],
  "folders": [
    {
      "id": "folder_auth",
      "name": "Authentication",
      "source_count": 3
    },
    {
      "id": "folder_payment",
      "name": "Payment System",
      "source_count": 2
    }
  ],
  "total": 5
}
```

#### 3. **GET /api/knowledge/tags**
Get all knowledge tags with descriptions.

**Query Parameters**:
- `category` (optional): Filter by category

**Response**:
```json
{
  "tags": [
    {
      "id": "tag_1",
      "tag_name": "react",
      "category": "framework",
      "description": "React framework for building user interfaces",
      "usage_guidelines": "Use for React-specific documentation...",
      "color_hex": "#61dafb",
      "usage_count": 15
    }
  ],
  "categories": {
    "framework": ["react", "nextjs", "fastapi"],
    "language": ["python", "typescript", "javascript"]
  },
  "total": 40
}
```

#### 4. **POST /api/knowledge/folders**
Create a knowledge folder for a project.

**Request Body**:
```json
{
  "project_id": "proj_123",
  "folder_name": "API Documentation",
  "description": "REST API endpoints and schemas",
  "color_hex": "#3b82f6"
}
```

**Response**:
```json
{
  "success": true,
  "folder": {
    "id": "folder_new",
    "project_id": "proj_123",
    "folder_name": "API Documentation",
    "description": "REST API endpoints and schemas",
    "color_hex": "#3b82f6",
    "sort_order": 0
  }
}
```

#### 5. **PUT /api/knowledge/folders/:folderId**
Update folder metadata.

#### 6. **DELETE /api/knowledge/folders/:folderId**
Delete folder (sets source.folder_id to NULL, doesn't delete sources).

### Modified Endpoints

#### **POST /api/knowledge-items/crawl**
Add `scope` and `project_id` parameters.

**Request Body**:
```json
{
  "url": "https://docs.stripe.com/api",
  "knowledge_type": "technical",
  "tags": ["stripe", "api", "payment"],
  "scope": "project",
  "project_id": "proj_123",
  "folder_id": "folder_payment",
  "max_depth": 2,
  "extract_code_examples": true
}
```

#### **POST /api/documents/upload**
Add `scope`, `project_id`, and `folder_id` to form data.

---

## UI Structure

### Tab-Based Navigation

```
┌─────────────────────────────────────────────────────────────┐
│  Knowledge Base                                              │
│                                                              │
│  ┌─────────────┬──────────────┬─────────────┐              │
│  │   Global    │   Projects   │    Tags     │              │
│  └─────────────┴──────────────┴─────────────┘              │
│                                                              │
│  [Current Tab Content]                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Global Tab

**Features**:
- Grid/list view of all global knowledge sources
- Filter by tags, knowledge_type
- Search bar for quick filtering
- "Add Global Knowledge" button (crawl URL or upload file)
- Tag badges on each card
- Quick actions: Refresh, Delete, Inspect

**Text-based Mockup**:
```
┌─────────────────────────────────────────────────────────────────┐
│ GLOBAL KNOWLEDGE                                                │
│                                                                 │
│ [Search...] [Filter by Tags ▼] [Add Global Knowledge +]       │
│                                                                 │
│ ┌─────────────────────┐ ┌─────────────────────┐              │
│ │ React Documentation │ │ FastAPI Guide       │              │
│ │ react.dev           │ │ fastapi.tiangolo... │              │
│ │                     │ │                     │              │
│ │ 150 chunks          │ │ 200 chunks          │              │
│ │ 45 code examples    │ │ 30 code examples    │              │
│ │                     │ │                     │              │
│ │ [react] [javascript]│ │ [fastapi] [python]  │              │
│ │                     │ │                     │              │
│ │ [Refresh] [Delete]  │ │ [Refresh] [Delete]  │              │
│ └─────────────────────┘ └─────────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Projects Tab

**Features**:
- Accordion/tree structure showing projects
- Each project expands to show folders
- Folders expand to show knowledge sources
- Visual hierarchy: Project > Folder > Source
- "Add to Project" button for active project
- Drag-and-drop for organizing sources into folders

**Text-based Mockup**:
```
┌─────────────────────────────────────────────────────────────────┐
│ PROJECT KNOWLEDGE                                               │
│                                                                 │
│ [Select Project ▼]                                              │
│                                                                 │
│ ▼ E-commerce Platform                                           │
│   │                                                             │
│   ├─ 📁 Authentication (3 sources)                             │
│   │  ├─ OAuth 2.0 Implementation Guide                         │
│   │  │  [oauth] [security] [authentication]                    │
│   │  ├─ JWT Best Practices                                     │
│   │  │  [jwt] [security]                                       │
│   │  └─ Custom Auth Specification (uploaded)                   │
│   │     [internal] [specification]                             │
│   │                                                             │
│   ├─ 📁 Payment System (2 sources)                             │
│   │  ├─ Stripe API Documentation                               │
│   │  │  [stripe] [api] [payment]                               │
│   │  └─ Payment Flow Diagram (uploaded)                        │
│   │     [payment] [architecture]                               │
│   │                                                             │
│   └─ 📁 [+ New Folder]                                         │
│                                                                 │
│ ▼ Mobile App Redesign                                          │
│   │                                                             │
│   ├─ 📁 UI Components (5 sources)                              │
│   └─ 📁 API Integration (3 sources)                            │
│                                                                 │
│ [Add Knowledge to Project +]                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Tags Tab

**Features**:
- Tag index organized by category
- Each tag shows:
  - Description
  - Usage guidelines
  - Usage count
  - Color indicator
- Click tag to see all sources with that tag
- Search tags by name or category

**Text-based Mockup**:
```
┌─────────────────────────────────────────────────────────────────┐
│ KNOWLEDGE TAGS                                                  │
│                                                                 │
│ [Search tags...] [Filter by Category ▼]                        │
│                                                                 │
│ ━━━ FRAMEWORK (5 tags) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                 │
│ ● react (15 uses) #61dafb                                      │
│   React framework for building user interfaces                 │
│   → Use for React-specific documentation, component patterns   │
│   [View Sources →]                                              │
│                                                                 │
│ ● nextjs (8 uses) #000000                                      │
│   Next.js React framework                                      │
│   → Use for Next.js routing, SSR, API routes                   │
│   [View Sources →]                                              │
│                                                                 │
│ ━━━ LANGUAGE (5 tags) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                 │
│ ● python (20 uses) #3776ab                                     │
│   Python programming language                                  │
│   → Use for Python code, syntax, standard library              │
│   [View Sources →]                                              │
│                                                                 │
│ ━━━ SECURITY (4 tags) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│ ...                                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Add Knowledge Dialog

**Enhanced with Scope Selection**:
```
┌──────────────────────────────────────────────────┐
│ Add Knowledge Source                             │
│                                                  │
│ Scope:  ◉ Global   ○ Project-Specific           │
│                                                  │
│ [ Project-specific fields only shown when        │
│   "Project-Specific" is selected ]              │
│                                                  │
│ Project: [Select Project ▼]                     │
│ Folder:  [Select Folder ▼] or [+ New Folder]    │
│                                                  │
│ Source Type:  ◉ URL   ○ Upload File             │
│                                                  │
│ URL: [_________________________________]         │
│                                                  │
│ Tags: [react] [typescript] [+ Add Tag]          │
│                                                  │
│ [Cancel]  [Add Knowledge]                       │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## Search Strategy for Agents

### Decision Tree for Search Scope

```
Agent needs knowledge
    │
    ├─ Working on specific project?
    │   │
    │   ├─ YES → Search project knowledge first
    │   │   │
    │   │   ├─ Found relevant results? → Use project knowledge
    │   │   │
    │   │   └─ No relevant results? → Expand to global search
    │   │
    │   └─ NO → Search global knowledge only
    │
    └─ Need general/framework knowledge? → Global search with tags
```

### Agent Query Patterns

#### Pattern 1: Project Context Known

```typescript
// Agent knows current project context
const projectId = getCurrentProjectId(); // From context/environment

// Search project-specific knowledge first
const projectResults = await rag_search_project_knowledge(
  "authentication flow",
  projectId
);

if (projectResults.length === 0) {
  // Fall back to global knowledge
  const globalResults = await rag_search_global_knowledge(
    "authentication best practices",
    tags: ["authentication", "security"]
  );
}
```

#### Pattern 2: Framework/Language Questions

```typescript
// General questions always search global
const results = await rag_search_global_knowledge(
  "React hooks patterns",
  tags: ["react", "hooks"]
);
```

#### Pattern 3: Folder-Scoped Search

```typescript
// Search within specific folder (e.g., "API Documentation")
const results = await rag_search_project_knowledge(
  "payment endpoints",
  projectId: "proj_123",
  folder_name: "API Documentation"
);
```

### Template CLAUDE.md Updates

Add to project-level CLAUDE.md:

````markdown
## Knowledge Base Context

**Current Project**: {PROJECT_NAME}
**Project ID**: {PROJECT_ID}

### Available Knowledge Sources

**Project-Specific Knowledge**:
- Folder: "Authentication" - OAuth implementation, JWT handling
- Folder: "API Documentation" - REST endpoints, request/response schemas
- Folder: "Database" - Schema design, migration scripts

**Global Knowledge**:
- React Documentation (react.dev)
- FastAPI Guide (fastapi.tiangolo.com)
- PostgreSQL Reference (postgresql.org/docs)

### Search Guidelines

1. **For project-specific questions** (implementation details, custom code):
   ```
   rag_search_project_knowledge("authentication flow", "{PROJECT_ID}")
   ```

2. **For framework/language questions** (how React hooks work):
   ```
   rag_search_global_knowledge("React hooks", tags=["react"])
   ```

3. **For folder-specific searches**:
   ```
   rag_search_project_knowledge("API schema", "{PROJECT_ID}", folder_name="API Documentation")
   ```

### MCP Tools Quick Reference

- `rag_get_available_sources(scope="project", project_id="{PROJECT_ID}")` - List project sources
- `rag_get_available_sources(scope="global")` - List global sources
- `rag_search_project_knowledge(query, "{PROJECT_ID}")` - Search this project
- `rag_search_global_knowledge(query)` - Search global knowledge
- `rag_list_project_folders("{PROJECT_ID}")` - List knowledge folders
````

### Example Agent Workflow

```python
# Agent task: Implement user authentication for e-commerce project

# Step 1: Get project context
project_id = "proj_ecommerce_123"

# Step 2: Check what project-specific auth knowledge exists
sources = rag_get_available_sources(scope="project", project_id=project_id)
# Returns: Custom Auth Specification, OAuth Integration Notes

# Step 3: Search project knowledge for implementation details
project_auth = rag_search_project_knowledge(
    "authentication implementation",
    project_id=project_id,
    folder_name="Authentication"
)

# Step 4: Get global best practices for reference
global_auth = rag_search_global_knowledge(
    "OAuth 2.0 best practices",
    tags=["oauth", "security", "authentication"]
)

# Step 5: Combine knowledge
# - Use project-specific details for custom implementation
# - Reference global best practices for security patterns
# - Generate implementation plan
```

---

## Implementation Phases

### Phase 1: Database Schema (Week 1)

**Deliverables**:
- Migration script `012_add_knowledge_scope_and_project_linking.sql`
- Create `archon_knowledge_tags` table
- Create `archon_project_knowledge_folders` table
- Seed standard tags
- Update existing sources to `scope='global'`

**Testing**:
- Verify schema changes apply cleanly
- Test constraints (project_id required for project scope)
- Validate tag uniqueness and categories
- Check foreign key cascades

**Files**:
- `supabase/migrations/20250115000000_add_knowledge_scope.sql`
- `python/tests/test_knowledge_scope_migration.py`

---

### Phase 2: Backend Services (Week 2)

**Deliverables**:
- Update `KnowledgeItemService` to support scope filtering
- Create `KnowledgeFolderService` for folder management
- Create `KnowledgeTagService` for tag operations
- Update `CrawlingService` to set scope and project_id
- Create `AutoTaggingService` for tag suggestions

**API Routes**:
- `GET /api/knowledge/global`
- `GET /api/knowledge/projects/:projectId`
- `GET /api/knowledge/tags`
- `POST /api/knowledge/folders`
- `PUT /api/knowledge/folders/:folderId`
- `DELETE /api/knowledge/folders/:folderId`

**Testing**:
- Unit tests for all services
- Integration tests for API routes
- Test scope filtering logic
- Validate auto-tagging accuracy

**Files**:
- `python/src/server/services/knowledge/knowledge_folder_service.py`
- `python/src/server/services/knowledge/knowledge_tag_service.py`
- `python/src/server/services/knowledge/auto_tagging_service.py`
- `python/src/server/api_routes/knowledge_folders_api.py`
- `python/tests/server/services/test_knowledge_folders.py`

---

### Phase 3: MCP Tool Updates (Week 3)

**Deliverables**:
- Update `rag_get_available_sources` with scope filter
- Update `rag_search_knowledge_base` with scope parameter
- Create `rag_search_project_knowledge` tool
- Create `rag_search_global_knowledge` tool
- Create `rag_list_project_folders` tool

**Testing**:
- Test each tool with various scope combinations
- Verify project_id validation
- Test folder filtering
- Validate response formats

**Files**:
- `python/src/mcp_server/features/rag/rag_tools.py`
- `python/tests/mcp/test_rag_tools_scoped.py`

---

### Phase 4: Frontend UI (Week 4)

**Deliverables**:
- Create tab navigation component (Global/Projects/Tags)
- Build Global tab view
- Build Projects tab with folder tree
- Build Tags tab with category organization
- Update AddKnowledgeDialog with scope selection
- Create folder management dialogs

**Components**:
- `KnowledgeTabs.tsx` - Tab container
- `GlobalKnowledgeView.tsx` - Global tab content
- `ProjectKnowledgeView.tsx` - Projects tab with folders
- `TagsIndexView.tsx` - Tags tab
- `KnowledgeFolderTree.tsx` - Folder tree component
- `AddKnowledgeScopeSelector.tsx` - Scope selection in add dialog

**Types**:
- Update `KnowledgeItem` interface with scope fields
- Create `KnowledgeFolder` type
- Create `KnowledgeTag` type

**Testing**:
- Component tests for all new components
- Integration tests for tab navigation
- Test folder tree interaction
- Validate scope selection flow

**Files**:
- `archon-ui-main/src/features/knowledge/components/KnowledgeTabs.tsx`
- `archon-ui-main/src/features/knowledge/components/GlobalKnowledgeView.tsx`
- `archon-ui-main/src/features/knowledge/components/ProjectKnowledgeView.tsx`
- `archon-ui-main/src/features/knowledge/components/KnowledgeFolderTree.tsx`
- `archon-ui-main/src/features/knowledge/types/knowledge.ts`

---

### Phase 5: Integration & Testing (Week 5)

**Deliverables**:
- End-to-end testing of complete workflow
- Performance testing with large knowledge bases
- Documentation updates
- User guide for knowledge organization
- Migration guide for existing users

**Testing Scenarios**:
1. Create global knowledge source
2. Create project-specific knowledge source with folder
3. Search global knowledge via MCP
4. Search project knowledge via MCP
5. Move source between global and project scope
6. Delete folder (verify sources remain)
7. Test auto-tagging accuracy

**Documentation**:
- Update main README with knowledge organization section
- Create user guide: `KNOWLEDGE_ORGANIZATION.md`
- Update MCP tools documentation
- Add agent workflow examples

**Files**:
- `KNOWLEDGE_ORGANIZATION.md`
- `PRPs/ai_docs/KNOWLEDGE_ORGANIZATION_GUIDE.md`
- Updated `CLAUDE.md` template

---

## Migration Strategy

### For Existing Archon Installations

#### Step 1: Database Migration

```bash
# Run migration via Supabase SQL Editor
# File: supabase/migrations/20250115000000_add_knowledge_scope.sql
```

All existing sources automatically set to `scope='global'`.

#### Step 2: Backend Update

```bash
cd python
uv sync
docker compose restart archon-server
```

#### Step 3: Frontend Update

```bash
cd archon-ui-main
npm install
npm run build
```

#### Step 4: Optional - Organize Existing Knowledge

Users can manually:
1. Create projects via UI
2. Create folders within projects
3. Move global sources to project-specific (change scope, assign project_id)

### Backward Compatibility

- All existing MCP tools continue to work without scope parameter
- Default behavior: search all knowledge (scope="all")
- Existing CLAUDE.md files don't need updates to function
- New features are opt-in

---

## Testing Strategy

### Unit Tests

**Backend**:
- `test_knowledge_scope_service.py` - Scope filtering logic
- `test_knowledge_folder_service.py` - Folder CRUD operations
- `test_auto_tagging_service.py` - Tag suggestion accuracy
- `test_knowledge_tag_service.py` - Tag management

**Frontend**:
- `KnowledgeTabs.test.tsx` - Tab navigation
- `KnowledgeFolderTree.test.tsx` - Folder tree interaction
- `ScopeSelector.test.tsx` - Scope selection logic

### Integration Tests

**API Routes**:
- Test all new endpoints with various scenarios
- Verify scope filtering in search queries
- Test folder assignment and deletion
- Validate project_id constraints

**MCP Tools**:
- Test scope parameter in all search tools
- Verify project-specific searches
- Test folder filtering
- Validate response formats match specs

### End-to-End Tests

**Scenarios**:
1. **Create Global Knowledge**
   - Add URL as global
   - Verify appears in Global tab
   - Search via MCP global tool

2. **Create Project Knowledge**
   - Create project
   - Create folder
   - Add source to folder
   - Verify appears in Projects tab
   - Search via MCP project tool

3. **Scope Migration**
   - Create source as global
   - Change to project-specific
   - Verify UI updates
   - Verify search results reflect change

4. **Auto-Tagging**
   - Add React documentation URL
   - Verify "react", "javascript" tags applied
   - Add custom tags
   - Search by tags

### Performance Tests

- **Large Knowledge Base**: 1000+ sources across global and 10 projects
- **Search Performance**: <200ms for scoped searches
- **Folder Tree Rendering**: <100ms for 50 folders
- **Tag Index**: <50ms to load 200 tags

---

## Summary

This design specification provides a complete blueprint for implementing a 2-layer knowledge organization system in Archon. The key innovations are:

1. **Clear Separation**: Database-level scope distinction with optional project assignment
2. **Flexible Organization**: Folders for project knowledge, tags for all knowledge
3. **Agent-Friendly**: MCP tools designed for easy scope selection and filtering
4. **Backward Compatible**: Existing installations work without changes
5. **User-Centric UI**: Tab-based navigation with visual hierarchy

### Next Steps

1. Review and approve this design specification
2. Begin Phase 1 (Database Schema)
3. Iterate based on implementation learnings
4. Gather user feedback during Phase 4
5. Release as Archon v0.2.0

### Open Questions

1. Should we support moving sources between projects? (Recommended: Yes, via UI)
2. Should folders be shareable across projects? (Recommended: No, per-project only)
3. Should we implement folder hierarchy (nested folders)? (Recommended: Phase 2, single-level first)
4. Should tags be hierarchical? (Recommended: No, flat with categories)

---

**Document Control**:
- Created: 2025-01-14
- Version: 1.0
- Status: Design Phase
- Next Review: After Phase 1 completion
