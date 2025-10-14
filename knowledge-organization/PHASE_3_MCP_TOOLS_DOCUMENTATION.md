# Phase 3 MCP Tools Documentation

**Date**: October 14, 2025
**Phase**: Phase 3 - MCP Tool Updates
**Status**: Complete

---

## Overview

This document provides comprehensive documentation for the enhanced and new MCP tools that support scope-aware knowledge retrieval in Archon's two-layer knowledge organization system. These tools enable AI agents to efficiently discover and search knowledge based on scope (global vs project-specific) with folder-level granularity.

---

## Enhanced MCP Tools

### 1. rag_get_available_sources (Enhanced)

**Purpose**: List available knowledge sources with optional scope and project filtering.

**Signature**:
```python
async def rag_get_available_sources(
    ctx: Context,
    scope: str | None = None,
    project_id: str | None = None
) -> str
```

**Parameters**:
- `scope` (optional): Filter by knowledge scope
  - `"global"` - Only global knowledge sources
  - `"project"` - Only project-specific sources
  - `None` - All sources (default)
- `project_id` (optional): When `scope="project"`, filter by specific project

**Returns**: JSON string with:
- `success`: bool - Operation status
- `sources`: list[dict] - Source objects with scope, project_id, folder_name, tags
- `count`: int - Total number of sources
- `scope_filter`: str|null - Applied scope filter
- `project_filter`: str|null - Applied project filter
- `error`: str - Error description if failed

**Usage Examples**:
```python
# Get all sources
rag_get_available_sources()

# Get only global sources
rag_get_available_sources(scope="global")

# Get sources for specific project
rag_get_available_sources(scope="project", project_id="proj_123")
```

**When to Use**:
- Discovery phase: Understanding what knowledge is available
- Before targeted searches: Identifying relevant sources
- Scoping decisions: Determining whether global or project knowledge exists

---

### 2. rag_search_knowledge_base (Enhanced)

**Purpose**: Search knowledge base with scope filtering and project context.

**Signature**:
```python
async def rag_search_knowledge_base(
    ctx: Context,
    query: str,
    scope: str = "all",
    project_id: str | None = None,
    source_id: str | None = None,
    match_count: int = 5,
    return_mode: str = "pages"
) -> str
```

**Parameters**:
- `query`: Search query (keep SHORT and FOCUSED - 2-5 keywords)
- `scope`: Knowledge scope to search
  - `"all"` - Search all knowledge (default)
  - `"global"` - Only search global knowledge
  - `"project"` - Only search project-specific knowledge
- `project_id` (optional): Project ID when `scope="project"` or `scope="all"` with context
- `source_id` (optional): Filter by specific source ID
- `match_count`: Maximum results (default: 5)
- `return_mode`: `"pages"` (default) or `"chunks"`

**Returns**: JSON string with:
- `success`: bool
- `results`: list[dict] - Pages/chunks with content, metadata, scope indicators
- `search_scope`: str - Scope used for search
- `project_context`: str|null - Project ID if provided
- `return_mode`: str
- `reranked`: bool
- `error`: str|null

**Usage Examples**:
```python
# Search only global knowledge
rag_search_knowledge_base("React hooks", scope="global")

# Search project-specific knowledge
rag_search_knowledge_base("authentication flow", scope="project", project_id="proj_123")

# Search all with project context (prioritizes project sources)
rag_search_knowledge_base("API endpoints", scope="all", project_id="proj_123")
```

**When to Use**:
- Flexible searches across scopes
- When you need fine-grained control over search scope
- Combining global and project knowledge with prioritization

---

## New MCP Tools

### 3. rag_search_project_knowledge (New)

**Purpose**: Convenience wrapper for searching project-specific knowledge with optional folder filtering.

**Signature**:
```python
async def rag_search_project_knowledge(
    ctx: Context,
    query: str,
    project_id: str,
    folder_name: str | None = None,
    match_count: int = 5
) -> str
```

**Parameters**:
- `query`: Search query (SHORT and FOCUSED)
- `project_id`: Project ID to search within (required)
- `folder_name` (optional): Filter by folder (e.g., "Authentication", "API")
- `match_count`: Maximum results (default: 5)

**Returns**: JSON string with:
- `success`: bool
- `results`: list[dict] - Project-scoped results with folder information
- `project_id`: str - Project ID searched
- `folder_filter`: str|null - Folder name filter if provided
- `error`: str|null

**Usage Examples**:
```python
# Search all project knowledge
rag_search_project_knowledge("database schema", "proj_123")

# Search within specific folder
rag_search_project_knowledge("login endpoint", "proj_123", folder_name="API")

# Search authentication docs in Authentication folder
rag_search_project_knowledge("OAuth flow", "proj_123", folder_name="Authentication")
```

**When to Use**:
- You know you're working on a specific project
- Need project-specific implementation details
- Want to search within a specific knowledge folder
- Simplicity over flexibility (vs using rag_search_knowledge_base with scope="project")

**Agent Decision Pattern**:
```
Working on specific project?
  ├─ YES → Use rag_search_project_knowledge(query, project_id)
  │   └─ Results found? → Use project knowledge
  │       └─ No results? → Fall back to rag_search_global_knowledge
  └─ NO → Use rag_search_global_knowledge
```

---

### 4. rag_search_global_knowledge (New)

**Purpose**: Convenience wrapper for searching only global knowledge sources with optional tag filtering.

**Signature**:
```python
async def rag_search_global_knowledge(
    ctx: Context,
    query: str,
    tags: list[str] | None = None,
    match_count: int = 5
) -> str
```

**Parameters**:
- `query`: Search query (SHORT and FOCUSED)
- `tags` (optional): Tag filters (e.g., `["react", "typescript"]`, `["security", "fastapi"]`)
- `match_count`: Maximum results (default: 5)

**Returns**: JSON string with:
- `success`: bool
- `results`: list[dict] - Global knowledge results with tags
- `tag_filters`: list[str]|null - Tags used for filtering
- `error`: str|null

**Usage Examples**:
```python
# Search all global knowledge
rag_search_global_knowledge("REST API design")

# Search global knowledge with specific tags
rag_search_global_knowledge("authentication", tags=["security", "fastapi"])

# Search framework documentation
rag_search_global_knowledge("hooks patterns", tags=["react"])
```

**When to Use**:
- Need framework/language documentation
- Looking for general best practices
- Want cross-cutting knowledge not specific to current project
- Filter by technology stack using tags

**Tag Categories Available**:
- Framework: `react`, `nextjs`, `fastapi`, `django`, `express`
- Language: `python`, `typescript`, `javascript`, `rust`, `go`
- Architecture: `microservices`, `rest-api`, `graphql`, `event-driven`
- Security: `authentication`, `authorization`, `encryption`, `security-best-practices`
- Testing: `unit-testing`, `integration-testing`, `e2e-testing`
- Deployment: `docker`, `kubernetes`, `ci-cd`
- Database: `postgresql`, `mongodb`, `redis`, `vector-search`
- API: `openapi`, `websockets`
- UI: `tailwind`, `radix-ui`, `design-system`
- Documentation: `api-reference`, `tutorial`, `architecture-docs`, `troubleshooting`

---

### 5. rag_list_project_folders (New)

**Purpose**: List all knowledge folders for a project to discover organizational structure.

**Signature**:
```python
async def rag_list_project_folders(
    ctx: Context,
    project_id: str
) -> str
```

**Parameters**:
- `project_id`: Project ID to list folders for (required)

**Returns**: JSON string with:
- `success`: bool
- `project_id`: str - Project ID queried
- `project_title`: str|null - Project name if available
- `folders`: list[dict] - Folders with id, name, description, source_count, color
- `total`: int - Total number of folders
- `error`: str|null

**Folder Object Structure**:
```json
{
  "id": "folder_abc",
  "name": "Authentication",
  "description": "Auth system documentation",
  "source_count": 3,
  "color": "#6366f1",
  "icon_name": "lock"
}
```

**Usage Examples**:
```python
# List all folders for a project
rag_list_project_folders("proj_123")

# Discovery workflow
folders = rag_list_project_folders("proj_ecommerce")
# Inspect folders, then search specific one:
rag_search_project_knowledge("API endpoints", "proj_ecommerce", folder_name="API")
```

**When to Use**:
- Starting work on an existing project
- Discovery: Understanding how project knowledge is organized
- Before folder-specific searches
- Deciding which folder to search within

**Typical Workflow**:
```python
# Step 1: Discover folders
folders = rag_list_project_folders("proj_123")
# Returns: Authentication, API, Database, UI Components

# Step 2: Search within relevant folder
results = rag_search_project_knowledge(
    "login endpoint",
    "proj_123",
    folder_name="API"
)
```

---

## Search Strategy Guide for Agents

### Decision Tree

```
Agent needs knowledge
    │
    ├─ Working on specific project?
    │   │
    │   ├─ YES → rag_search_project_knowledge(query, project_id)
    │   │   │
    │   │   ├─ Found relevant results? → Use project knowledge
    │   │   │
    │   │   └─ No relevant results? → rag_search_global_knowledge(query)
    │   │
    │   └─ NO → rag_search_global_knowledge(query)
    │
    └─ Need general/framework knowledge? → rag_search_global_knowledge(query, tags)
```

### Query Best Practices

**Good Queries** (2-5 keywords):
- "vector search"
- "authentication JWT"
- "React hooks patterns"
- "database schema design"
- "API error handling"

**Bad Queries** (too long, conversational):
- "how to implement user authentication with JWT tokens in React with TypeScript and handle refresh tokens"
- "what are the best practices for designing REST APIs with proper error handling and validation"

### Folder-Scoped Search Pattern

```python
# Pattern 1: Know the folder
rag_search_project_knowledge(
    "payment flow",
    "proj_123",
    folder_name="Payment System"
)

# Pattern 2: Discover folders first
folders = rag_list_project_folders("proj_123")
# Inspect folders, identify "Authentication" folder
rag_search_project_knowledge(
    "OAuth implementation",
    "proj_123",
    folder_name="Authentication"
)
```

### Tag-Based Search Pattern

```python
# Search global knowledge for React + TypeScript content
rag_search_global_knowledge(
    "hooks patterns",
    tags=["react", "typescript"]
)

# Search for security best practices in FastAPI
rag_search_global_knowledge(
    "authentication",
    tags=["security", "fastapi"]
)
```

---

## Integration with Backend Services

All MCP tools communicate via HTTP with the archon-server backend. The backend services implemented in Phase 2 provide the data:

### Service Mappings

**rag_get_available_sources** → `GET /api/rag/sources?scope={scope}&project_id={project_id}`
- Backend: `KnowledgeItemService.list_items()` with scope filtering

**rag_search_knowledge_base** → `POST /api/rag/query`
- Backend: RAG service with scope-aware vector search

**rag_search_project_knowledge** → `POST /api/rag/query` (scope="project")
- Backend: RAG service + folder filtering
- Uses: `KnowledgeItemService` for project-scoped sources

**rag_search_global_knowledge** → `POST /api/rag/query` (scope="global")
- Backend: RAG service + tag filtering
- Uses: `KnowledgeTagService` for tag validation

**rag_list_project_folders** → `GET /api/projects/{project_id}/folders`
- Backend: `KnowledgeFolderService.list_project_folders()`

---

## Error Handling

All tools follow consistent error handling:

```json
{
  "success": false,
  "error": "HTTP 404: Project not found",
  "results": [],
  "...": null
}
```

Common error scenarios:
- **404**: Project not found, folder not found
- **400**: Invalid scope parameter, missing required project_id
- **500**: Server error, database connection failure
- **Timeout**: Long-running queries (30s timeout)

Agents should check `success` field and handle errors gracefully.

---

## Performance Considerations

### Query Optimization
- Keep queries SHORT (2-5 keywords)
- Use specific folder filters when possible
- Apply tag filters to narrow global searches
- Use appropriate `match_count` (default: 5, increase if needed)

### Caching Strategy
- Backend implements ETag caching
- Repeated identical queries benefit from HTTP cache
- Smart polling reduces unnecessary requests

### Folder Filtering Performance
- Folder filtering is post-query (applied client-side in MCP tool)
- For large result sets, backend folder filtering would be more efficient
- Current implementation prioritizes simplicity and flexibility

---

## Testing Recommendations

### Unit Tests
Test each tool independently:
- Scope parameter handling
- Project ID validation
- Folder name filtering
- Tag filtering
- Error response handling

### Integration Tests
End-to-end workflows:
1. List sources → Filter by scope
2. Search global → No results → Search project
3. List folders → Search specific folder
4. Tag-based search → Validate results have tags

### Agent Simulation Tests
Simulate agent workflows:
- Project context workflow
- Global knowledge discovery
- Folder-specific deep dives
- Tag-based filtering

---

## Migration Notes

### Backward Compatibility
All enhanced tools maintain backward compatibility:
- `rag_get_available_sources()` without parameters works as before
- `rag_search_knowledge_base(query)` defaults to `scope="all"`
- Existing agent workflows continue to function

### Recommended Updates
Update CLAUDE.md files in projects with:
```markdown
## Knowledge Base Context

**Current Project**: {PROJECT_NAME}
**Project ID**: {PROJECT_ID}

### Search Guidelines

1. For project-specific questions:
   ```
   rag_search_project_knowledge("authentication flow", "{PROJECT_ID}")
   ```

2. For framework/language questions:
   ```
   rag_search_global_knowledge("React hooks", tags=["react"])
   ```

3. For folder-specific searches:
   ```
   rag_list_project_folders("{PROJECT_ID}")
   rag_search_project_knowledge("API schema", "{PROJECT_ID}", folder_name="API")
   ```
```

---

## Next Steps

### Phase 4: API Route Implementation
Backend API routes need to be created/updated to support these tools:
- `GET /api/rag/sources` with scope/project_id parameters
- `POST /api/rag/query` with scope/project_id/folder_name/tags
- `GET /api/projects/{project_id}/folders`

### Phase 5: Frontend UI
UI components for:
- Tab-based knowledge navigation (Global/Projects/Tags)
- Folder tree visualization
- Scope selection in AddKnowledgeDialog
- Tag filtering interface

---

## Conclusion

Phase 3 MCP Tool Updates are complete. All five tools (2 enhanced, 3 new) are implemented with:
- Comprehensive docstrings with usage examples
- Consistent error handling and JSON responses
- HTTP-based communication with archon-server
- Type hints using Python 3.12 syntax
- Backward compatibility with existing workflows

These tools provide AI agents with powerful, scope-aware knowledge retrieval capabilities, enabling efficient discovery and search across Archon's two-layer knowledge organization system.

---

**Implemented by**: Claude Code
**Date**: October 14, 2025
**Status**: Ready for API Route Integration (Phase 4)
