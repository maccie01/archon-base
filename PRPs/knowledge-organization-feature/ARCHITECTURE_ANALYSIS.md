# Archon Knowledge Base Architecture Analysis

**Date**: 2025-10-14
**Purpose**: Analyze current architecture and identify extension points for implementing 2-layer knowledge organization (global vs project-scoped)

---

## Executive Summary

The Archon knowledge base currently operates as a **flat, global system** where all knowledge sources are shared across the entire application. The existing `archon_project_sources` junction table provides a foundation for implementing **project-scoped knowledge**, enabling a 2-layer system:

1. **Global Knowledge**: Shared sources accessible across all projects (current behavior)
2. **Project Knowledge**: Sources linked to specific projects, filtered by project context

**Key Finding**: The infrastructure for 2-layer organization already exists. Implementation requires:
- Adding optional `project_id` filtering to search/query operations
- Updating UI to show project-scoped vs global sources
- Extending MCP tools to support project context
- Creating management interfaces for linking/unlinking sources from projects

---

## 1. Current Database Schema

### Core Knowledge Tables

#### `archon_sources` (Main Source Registry)
```sql
CREATE TABLE archon_sources (
    source_id TEXT PRIMARY KEY,              -- 16-char SHA256 hash
    source_url TEXT,                         -- Original URL
    source_display_name TEXT,                -- Human-readable name
    summary TEXT,
    total_word_count INTEGER DEFAULT 0,
    title TEXT,
    metadata JSONB DEFAULT '{}',            -- knowledge_type, tags, etc.
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Key indexes
CREATE INDEX idx_archon_sources_knowledge_type ON archon_sources((metadata->>'knowledge_type'));
CREATE INDEX idx_archon_sources_metadata ON archon_sources USING GIN(metadata);
```

**Current Usage**: All sources are global. No project_id field exists.

#### `archon_crawled_pages` (Document Chunks)
```sql
CREATE TABLE archon_crawled_pages (
    id BIGSERIAL PRIMARY KEY,
    url VARCHAR NOT NULL,
    chunk_number INTEGER NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    source_id TEXT NOT NULL,
    -- Multi-dimensional embeddings (384, 768, 1024, 1536, 3072)
    embedding_1536 VECTOR(1536),            -- Default OpenAI
    -- ... other embedding dimensions
    page_id UUID REFERENCES archon_page_metadata(id),
    FOREIGN KEY (source_id) REFERENCES archon_sources(source_id) ON DELETE CASCADE
);
```

**Current Filtering**: Uses `source_id` parameter in search functions. No project awareness.

#### `archon_code_examples` (Extracted Code)
```sql
CREATE TABLE archon_code_examples (
    id BIGSERIAL PRIMARY KEY,
    url VARCHAR NOT NULL,
    content TEXT NOT NULL,
    summary TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    source_id TEXT NOT NULL,
    embedding_1536 VECTOR(1536),
    FOREIGN KEY (source_id) REFERENCES archon_sources(source_id) ON DELETE CASCADE
);
```

**Current Filtering**: Similar to crawled_pages - source_id only.

#### `archon_page_metadata` (Full Page Storage)
```sql
CREATE TABLE archon_page_metadata (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id TEXT NOT NULL,
    url TEXT NOT NULL,
    full_content TEXT NOT NULL,
    section_title TEXT,
    word_count INT NOT NULL,
    chunk_count INT NOT NULL DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    FOREIGN KEY (source_id) REFERENCES archon_sources(source_id) ON DELETE CASCADE
);
```

**Current Usage**: Stores complete pages for agent retrieval. No project scoping.

### Existing Project Integration

#### `archon_project_sources` (Junction Table) ✅ **KEY INFRASTRUCTURE**
```sql
CREATE TABLE archon_project_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES archon_projects(id) ON DELETE CASCADE,
    source_id TEXT NOT NULL,                -- References archon_sources
    linked_at TIMESTAMPTZ DEFAULT NOW(),
    created_by TEXT DEFAULT 'system',
    notes TEXT,
    UNIQUE(project_id, source_id)
);

CREATE INDEX idx_archon_project_sources_project_id ON archon_project_sources(project_id);
CREATE INDEX idx_archon_project_sources_source_id ON archon_project_sources(source_id);
```

**Current Status**: Table exists but is **not actively used** in search/query operations.

**Potential**: This table is the foundation for project-scoped knowledge. It can be used to:
- Link sources to specific projects
- Filter search results by project context
- Show project-specific knowledge in UI
- Provide project-aware MCP tools

---

## 2. Service Layer Analysis

### Knowledge Item Service
**Location**: `python/src/server/services/knowledge/knowledge_item_service.py`

**Current Implementation**:
```python
async def list_items(
    self,
    page: int = 1,
    per_page: int = 20,
    knowledge_type: str | None = None,
    search: str | None = None,
) -> dict[str, Any]:
    # Queries archon_sources directly
    query = self.supabase.from_("archon_sources").select("*")

    # Applies knowledge_type filter
    if knowledge_type:
        query = query.contains("metadata", {"knowledge_type": knowledge_type})
```

**Extension Points**:
- Add optional `project_id` parameter
- When `project_id` provided:
  - Join with `archon_project_sources` to filter sources
  - Only return sources linked to that project
- When `project_id` is `None`:
  - Return all sources (global view) OR
  - Return sources NOT linked to any project (strict global)

**Recommended Signature**:
```python
async def list_items(
    self,
    page: int = 1,
    per_page: int = 20,
    knowledge_type: str | None = None,
    search: str | None = None,
    project_id: str | None = None,  # NEW
    scope: str = "all",  # "all", "global", "project"
) -> dict[str, Any]:
```

### RAG Service
**Location**: `python/src/server/services/search/rag_service.py`

**Current Implementation**:
```python
async def perform_rag_query(
    self,
    query: str,
    source: str = None,  # source_id filter
    match_count: int = 5,
    return_mode: str = "chunks"
) -> tuple[bool, dict[str, Any]]:
    # Builds filter_metadata
    filter_metadata = {"source": source} if source else None

    # Calls search_documents
    results = await self.search_documents(
        query=query,
        match_count=match_count,
        filter_metadata=filter_metadata,
        use_hybrid_search=use_hybrid_search,
    )
```

**Extension Points**:
- Add `project_id` parameter
- When `project_id` provided:
  - Query `archon_project_sources` to get linked source_ids
  - Filter search to only those source_ids
  - Update filter_metadata to include project context

**Database Search Functions**:
```sql
-- Current: match_archon_crawled_pages_multi
CREATE OR REPLACE FUNCTION match_archon_crawled_pages_multi (
  query_embedding VECTOR,
  embedding_dimension INTEGER,
  match_count INT DEFAULT 10,
  filter JSONB DEFAULT '{}'::jsonb,
  source_filter TEXT DEFAULT NULL  -- Single source_id
) RETURNS TABLE (...)
```

**Enhancement Needed**:
```sql
-- Option 1: Add project_filter parameter
CREATE OR REPLACE FUNCTION match_archon_crawled_pages_multi (
  ...
  source_filter TEXT DEFAULT NULL,
  project_filter UUID DEFAULT NULL  -- NEW: Filter by project
) RETURNS TABLE (...)
AS $$
BEGIN
  -- When project_filter provided, join with archon_project_sources
  IF project_filter IS NOT NULL THEN
    sql_query := format('
      SELECT ... FROM archon_crawled_pages cp
      INNER JOIN archon_project_sources ps
        ON cp.source_id = ps.source_id
      WHERE ps.project_id = $5
        AND (cp.%I IS NOT NULL)
        AND metadata @> $3
      ORDER BY cp.%I <=> $1
      LIMIT $2',
      embedding_column, embedding_column, embedding_column);
  ELSE
    -- Existing logic
  END IF;
END;
$$;

-- Option 2: Accept array of source_ids
CREATE OR REPLACE FUNCTION match_archon_crawled_pages_multi (
  ...
  source_filter TEXT DEFAULT NULL,
  source_ids_filter TEXT[] DEFAULT NULL  -- NEW: Array of source_ids
) RETURNS TABLE (...)
```

**Recommendation**: Use **Option 2** (array of source_ids) for better flexibility and performance. The application layer can query `archon_project_sources` and pass the list of source_ids.

---

## 3. MCP Tools Analysis

### Current RAG Tools
**Location**: `python/src/mcp_server/features/rag/rag_tools.py`

**Existing Tools**:
```python
@mcp.tool()
async def rag_search_knowledge_base(
    ctx: Context,
    query: str,
    source_id: str | None = None,      # Single source filter
    match_count: int = 5,
    return_mode: str = "pages"
) -> str:

@mcp.tool()
async def rag_search_code_examples(
    ctx: Context,
    query: str,
    source_id: str | None = None,      # Single source filter
    match_count: int = 5
) -> str:

@mcp.tool()
async def rag_get_available_sources(ctx: Context) -> str:
    # Returns ALL sources
```

**Extension Points**:

#### 1. Add Project-Aware Search Tools
```python
@mcp.tool()
async def rag_search_project_knowledge(
    ctx: Context,
    query: str,
    project_id: str,                    # Required for project scope
    match_count: int = 5,
    return_mode: str = "pages"
) -> str:
    """
    Search knowledge base within a specific project's context.
    Only returns results from sources linked to the project.
    """

@mcp.tool()
async def rag_get_project_sources(
    ctx: Context,
    project_id: str
) -> str:
    """
    Get sources linked to a specific project.
    """
```

#### 2. Add Source Management Tools
```python
@mcp.tool()
async def project_link_source(
    ctx: Context,
    project_id: str,
    source_id: str,
    notes: str | None = None
) -> str:
    """
    Link a knowledge source to a project.
    """

@mcp.tool()
async def project_unlink_source(
    ctx: Context,
    project_id: str,
    source_id: str
) -> str:
    """
    Remove source link from a project.
    """

@mcp.tool()
async def project_list_linked_sources(
    ctx: Context,
    project_id: str
) -> str:
    """
    List all sources linked to a project.
    """
```

**Backward Compatibility**: Keep existing tools unchanged. Add new project-scoped tools as separate functions.

---

## 4. API Endpoints Analysis

### Current Knowledge API
**Location**: `python/src/server/api_routes/knowledge_api.py`

**Key Endpoints**:
```python
@router.get("/knowledge-items")
async def get_knowledge_items(
    page: int = 1,
    per_page: int = 20,
    knowledge_type: str | None = None,
    search: str | None = None
):
    # Returns all knowledge items (global)

@router.post("/rag/query")
async def perform_rag_query(request: RagQueryRequest):
    # RagQueryRequest: query, source, match_count, return_mode
    # No project filtering
```

**Required Changes**:

#### 1. Add Optional Project Filtering
```python
@router.get("/knowledge-items")
async def get_knowledge_items(
    page: int = 1,
    per_page: int = 20,
    knowledge_type: str | None = None,
    search: str | None = None,
    project_id: str | None = None,      # NEW
    scope: str = "all"                   # NEW: "all", "global", "project"
):

class RagQueryRequest(BaseModel):
    query: str
    source: str | None = None
    match_count: int = 5
    return_mode: str = "chunks"
    project_id: str | None = None       # NEW
```

#### 2. Add Project-Source Management Endpoints
```python
@router.post("/projects/{project_id}/sources")
async def link_source_to_project(
    project_id: str,
    request: LinkSourceRequest
):
    """Link a knowledge source to a project"""

@router.delete("/projects/{project_id}/sources/{source_id}")
async def unlink_source_from_project(
    project_id: str,
    source_id: str
):
    """Unlink a knowledge source from a project"""

@router.get("/projects/{project_id}/sources")
async def get_project_sources(
    project_id: str,
    page: int = 1,
    per_page: int = 20
):
    """Get all sources linked to a project"""

@router.get("/sources/{source_id}/projects")
async def get_source_projects(source_id: str):
    """Get all projects that have linked this source"""
```

---

## 5. Frontend Components Analysis

### Current UI Structure
**Location**: `archon-ui-main/src/features/knowledge/`

**Main Components**:
```
knowledge/
├── views/
│   └── KnowledgeView.tsx           # Main view with grid/table
├── components/
│   ├── KnowledgeHeader.tsx         # Search, filters, add button
│   ├── KnowledgeList.tsx           # Grid/table of items
│   ├── KnowledgeCard.tsx           # Individual knowledge card
│   └── AddKnowledgeDialog.tsx      # Crawl/upload dialog
├── inspector/
│   └── KnowledgeInspector.tsx      # Document/code viewer
└── hooks/
    └── useKnowledgeQueries.ts      # TanStack Query hooks
```

**Current Filter State**:
```typescript
const [typeFilter, setTypeFilter] = useState<"all" | "technical" | "business">("all");
const [searchQuery, setSearchQuery] = useState("");

const filter = useMemo<KnowledgeItemsFilter>(() => {
    const f: KnowledgeItemsFilter = {
        page: 1,
        per_page: 100,
    };
    if (searchQuery) f.search = searchQuery;
    if (typeFilter !== "all") f.knowledge_type = typeFilter;
    return f;
}, [searchQuery, typeFilter]);
```

**Extension Points**:

#### 1. Add Scope Filter to Header
```typescript
// New filter state
const [scopeFilter, setScopeFilter] = useState<"all" | "global" | "project">("all");
const [selectedProject, setSelectedProject] = useState<string | null>(null);

// When viewing within a project context
const projectId = useProjectContext(); // From router or context

const filter = useMemo<KnowledgeItemsFilter>(() => {
    return {
        page: 1,
        per_page: 100,
        search: searchQuery || undefined,
        knowledge_type: typeFilter !== "all" ? typeFilter : undefined,
        project_id: selectedProject || undefined,  // NEW
        scope: scopeFilter,                         // NEW
    };
}, [searchQuery, typeFilter, selectedProject, scopeFilter]);
```

#### 2. Update Knowledge Card with Project Badge
```typescript
// KnowledgeCard.tsx
interface KnowledgeCardProps {
    item: KnowledgeItem;
    linkedProjects?: string[];  // NEW: Array of project IDs this source is linked to
}

// Show badge if source is linked to projects
{linkedProjects && linkedProjects.length > 0 && (
    <Badge variant="outline">
        🔗 {linkedProjects.length} project{linkedProjects.length > 1 ? 's' : ''}
    </Badge>
)}
```

#### 3. Add Project Management UI
```typescript
// New component: ProjectSourceManager.tsx
interface ProjectSourceManagerProps {
    projectId: string;
    onLinkSource: (sourceId: string) => void;
    onUnlinkSource: (sourceId: string) => void;
}

// Shows:
// - List of linked sources (project knowledge)
// - Button to link additional sources
// - Dialog to browse and select from global sources
```

### Type Definitions
**Location**: `archon-ui-main/src/features/knowledge/types/`

**Current Types**:
```typescript
export interface KnowledgeItem {
    id: string;
    title: string;
    url: string;
    source_id: string;
    source_type: "url" | "file";
    code_examples: CodeExample[];
    metadata: {
        knowledge_type: "technical" | "business";
        tags: string[];
        source_type: string;
        // ... other fields
    };
}

export interface KnowledgeItemsFilter {
    page?: number;
    per_page?: number;
    knowledge_type?: string;
    search?: string;
}
```

**Required Updates**:
```typescript
export interface KnowledgeItem {
    // ... existing fields
    linked_projects?: string[];          // NEW: Project IDs this source is linked to
    is_global?: boolean;                 // NEW: True if not linked to any project
}

export interface KnowledgeItemsFilter {
    page?: number;
    per_page?: number;
    knowledge_type?: string;
    search?: string;
    project_id?: string;                 // NEW: Filter by project
    scope?: "all" | "global" | "project";  // NEW: Scope filter
}

export interface ProjectSource {
    id: string;
    project_id: string;
    source_id: string;
    linked_at: string;
    created_by: string;
    notes?: string;
}
```

---

## 6. Migration Strategy

### Phase 1: Backend Foundation (Week 1)

#### 1.1 Database Functions
- [ ] Update `match_archon_crawled_pages_multi` to accept `source_ids_filter TEXT[]`
- [ ] Update `match_archon_code_examples_multi` to accept `source_ids_filter TEXT[]`
- [ ] Update `hybrid_search_archon_crawled_pages_multi` similarly
- [ ] Update `hybrid_search_archon_code_examples_multi` similarly
- [ ] Test all search functions with array filter

**Migration File**: `supabase/migrations/20250114000001_add_project_filtering_to_search.sql`

```sql
-- Update vector search functions to accept array of source_ids
CREATE OR REPLACE FUNCTION match_archon_crawled_pages_multi (
  query_embedding VECTOR,
  embedding_dimension INTEGER,
  match_count INT DEFAULT 10,
  filter JSONB DEFAULT '{}'::jsonb,
  source_filter TEXT DEFAULT NULL,
  source_ids_filter TEXT[] DEFAULT NULL  -- NEW
) RETURNS TABLE (...)
AS $$
BEGIN
  -- Use source_ids_filter if provided, else source_filter
  IF source_ids_filter IS NOT NULL THEN
    sql_query := format('
      SELECT ... FROM archon_crawled_pages
      WHERE source_id = ANY($5)
        AND (%I IS NOT NULL)
        AND metadata @> $3
      ORDER BY %I <=> $1
      LIMIT $2',
      embedding_column, embedding_column, embedding_column);
    RETURN QUERY EXECUTE sql_query USING query_embedding, match_count, filter, NULL, source_ids_filter;
  ELSIF source_filter IS NOT NULL THEN
    -- Existing single source logic
  ELSE
    -- Existing no filter logic
  END IF;
END;
$$;
```

#### 1.2 Service Layer Updates
- [ ] Add `get_project_source_ids(project_id: str) -> list[str]` to knowledge service
- [ ] Update `RAGService.perform_rag_query` to accept `project_id` parameter
- [ ] Update `RAGService.search_code_examples_service` to accept `project_id`
- [ ] Add `ProjectSourceService` for CRUD operations on `archon_project_sources`

**New Service**: `python/src/server/services/project_source_service.py`
```python
class ProjectSourceService:
    async def link_source(self, project_id: str, source_id: str, notes: str = None) -> bool
    async def unlink_source(self, project_id: str, source_id: str) -> bool
    async def get_project_sources(self, project_id: str) -> list[dict]
    async def get_source_projects(self, source_id: str) -> list[dict]
    async def is_source_linked(self, project_id: str, source_id: str) -> bool
```

#### 1.3 API Endpoints
- [ ] Update `/api/knowledge-items` to accept `project_id` and `scope` parameters
- [ ] Update `/api/rag/query` request model with `project_id`
- [ ] Add `/api/projects/{project_id}/sources` POST/GET/DELETE endpoints
- [ ] Add `/api/sources/{source_id}/projects` GET endpoint
- [ ] Update OpenAPI schema

### Phase 2: MCP Tools (Week 2)

#### 2.1 Project-Aware Tools
- [ ] Add `rag_search_project_knowledge()` tool
- [ ] Add `rag_get_project_sources()` tool
- [ ] Add `project_link_source()` tool
- [ ] Add `project_unlink_source()` tool
- [ ] Add `project_list_linked_sources()` tool
- [ ] Keep existing tools for backward compatibility

#### 2.2 Documentation
- [ ] Update MCP tool descriptions
- [ ] Add examples of project-scoped queries
- [ ] Document global vs project knowledge patterns

### Phase 3: Frontend UI (Week 3)

#### 3.1 Type Updates
- [ ] Add `project_id` and `scope` to `KnowledgeItemsFilter`
- [ ] Add `linked_projects` to `KnowledgeItem`
- [ ] Create `ProjectSource` type
- [ ] Update API response types

#### 3.2 Service Layer
- [ ] Create `projectSourceService.ts` with link/unlink/list methods
- [ ] Add query hooks in `useProjectSourceQueries.ts`
- [ ] Update `knowledgeService.ts` to support project filtering

#### 3.3 UI Components
- [ ] Add scope filter to `KnowledgeHeader` (All | Global | Project)
- [ ] Add project badge to `KnowledgeCard`
- [ ] Create `ProjectSourceManager` component for project detail view
- [ ] Add "Link to Project" action in `KnowledgeCardActions`
- [ ] Create `LinkSourceDialog` for selecting sources to link

#### 3.4 Views
- [ ] Update `KnowledgeView` to accept project context
- [ ] Add project-scoped knowledge view within project detail
- [ ] Show linked sources in project overview

### Phase 4: Testing & Polish (Week 4)

#### 4.1 Backend Tests
- [ ] Test search functions with project filtering
- [ ] Test ProjectSourceService CRUD operations
- [ ] Test API endpoints with various filter combinations
- [ ] Test MCP tools with project context

#### 4.2 Frontend Tests
- [ ] Test knowledge filtering UI
- [ ] Test project source linking/unlinking
- [ ] Test scope switching behavior
- [ ] Test optimistic updates for link/unlink

#### 4.3 Integration Tests
- [ ] Test end-to-end project knowledge workflow
- [ ] Test MCP tool integration with project context
- [ ] Test data consistency across views

#### 4.4 Documentation
- [ ] Update user documentation
- [ ] Update API documentation
- [ ] Create migration guide for existing users
- [ ] Add examples and best practices

---

## 7. Key Design Decisions

### Decision 1: Scope Behavior

**Options**:
- **Option A (Recommended)**: "All" shows everything (global + project), "Global" shows unlinked only, "Project" shows linked only
- **Option B**: "All" shows global only, "Project" shows project-scoped only
- **Option C**: No global/project distinction - just show all sources always

**Recommendation**: **Option A** provides maximum flexibility and clarity.

**Reasoning**:
- Users can see everything at once ("All")
- "Global" view helps identify reusable sources
- "Project" view focuses on project context
- Matches mental model of global vs scoped resources

### Decision 2: Search Behavior

**When searching within a project**:
- **Option A (Recommended)**: Search only project-linked sources by default
- **Option B**: Always search all sources, but rank project sources higher
- **Option C**: Let user explicitly choose search scope

**Recommendation**: **Option A** with toggle to expand to global.

**Reasoning**:
- Project context implies you want project-relevant results
- Prevents cognitive overload from unrelated results
- UI can provide "Search all knowledge" button to expand
- MCP tools get project context from active project

### Decision 3: Linking Behavior

**When to allow linking**:
- **Option A (Recommended)**: Any source can be linked to multiple projects
- **Option B**: Sources can only belong to one project (exclusive)
- **Option C**: Sources are either global (unlinked) or project (exclusive)

**Recommendation**: **Option A** (many-to-many).

**Reasoning**:
- Documentation is often relevant to multiple projects
- No need to duplicate sources
- `UNIQUE(project_id, source_id)` constraint prevents duplicates
- More flexible for reuse

### Decision 4: UI Organization

**Where to manage project knowledge**:
- **Option A (Recommended)**: Both in global Knowledge view AND in Project detail view
- **Option B**: Only in Project detail view
- **Option C**: Only in global Knowledge view with project filter

**Recommendation**: **Option A** (dual access).

**Reasoning**:
- Global view: See all knowledge, identify what to link
- Project view: Focus on project context, manage links
- Supports both top-down (find sources) and bottom-up (organize projects) workflows

### Decision 5: Default Behavior

**For new sources**:
- **Option A (Recommended)**: New sources are global (unlinked) by default
- **Option B**: If crawled/uploaded from project context, auto-link to project
- **Option C**: Ask user whether to link to project during creation

**Recommendation**: **Option A** with optional auto-link in project context.

**Reasoning**:
- Encourages reusable knowledge base
- Prevents accidental scoping
- Users can explicitly link after creation
- In project context, can show "Link to this project?" prompt

---

## 8. Implementation Checklist

### Critical Path Items

#### Backend (Must Have)
- [x] `archon_project_sources` table exists (already done)
- [ ] Update search functions to accept `source_ids[]` parameter
- [ ] Add `ProjectSourceService` for link/unlink operations
- [ ] Update `RAGService.perform_rag_query` with project_id support
- [ ] Add project-source management API endpoints
- [ ] Test all search scenarios with project filtering

#### MCP (Must Have for Agent Support)
- [ ] Add `rag_search_project_knowledge()` tool
- [ ] Add `project_link_source()` tool
- [ ] Add `project_list_linked_sources()` tool
- [ ] Update tool documentation with project context examples

#### Frontend (Must Have for User Experience)
- [ ] Add project_id to knowledge filter types
- [ ] Create ProjectSourceService API client
- [ ] Add scope filter to KnowledgeHeader
- [ ] Show project badge on KnowledgeCard
- [ ] Create ProjectSourceManager component
- [ ] Add link/unlink actions to UI

#### Testing (Must Have for Reliability)
- [ ] Test search with project_id parameter
- [ ] Test link/unlink operations
- [ ] Test UI filter behavior
- [ ] Test MCP tools with project context

### Nice-to-Have Enhancements

#### Advanced Filtering
- [ ] Filter by "linked to project" vs "not linked"
- [ ] Show source usage across projects
- [ ] Bulk link/unlink operations

#### UI Improvements
- [ ] Visual indicator of source scope in search results
- [ ] Quick link/unlink from search results
- [ ] Project knowledge health dashboard
- [ ] Source recommendation based on project type

#### Performance
- [ ] Cache project source mappings
- [ ] Optimize queries with project filtering
- [ ] Add pagination to project source lists

---

## 9. Risks and Mitigations

### Risk 1: Performance Impact
**Risk**: Joining with `archon_project_sources` may slow down queries

**Mitigation**:
- Use indexed queries (`idx_archon_project_sources_project_id`)
- Cache project → source_id mappings in application layer
- Pre-fetch source_ids array before search
- Monitor query performance with Logfire

### Risk 2: User Confusion
**Risk**: Users may not understand global vs project knowledge

**Mitigation**:
- Clear UI labels and tooltips
- Default to "All" scope for familiar behavior
- Add help documentation
- Show visual indicators for scope

### Risk 3: Migration Complexity
**Risk**: Existing users have all-global knowledge, need to adapt

**Mitigation**:
- No breaking changes - all sources remain accessible
- Gradual adoption - linking is optional
- Provide migration guide
- Keep backward compatibility in MCP tools

### Risk 4: Data Consistency
**Risk**: Sources linked to deleted projects

**Mitigation**:
- `ON DELETE CASCADE` on `project_id` foreign key (already in place)
- Gracefully handle missing projects in UI
- Show "orphaned" sources in admin view

---

## 10. Success Metrics

### Technical Metrics
- [ ] All search functions support project filtering
- [ ] API response time < 200ms with project filter
- [ ] Zero breaking changes to existing APIs
- [ ] 100% test coverage for project-source operations

### User Experience Metrics
- [ ] Users can link sources to projects in < 3 clicks
- [ ] Project-scoped search returns relevant results
- [ ] Clear visual distinction between global and project knowledge
- [ ] No user confusion reported in first month

### Adoption Metrics
- [ ] 50%+ of users link at least one source to a project
- [ ] Average 5+ sources linked per project
- [ ] 80%+ of searches use project context when available
- [ ] MCP tools used with project context 40%+ of time

---

## 11. Conclusion

The Archon knowledge base architecture is **well-positioned** for implementing 2-layer organization. The `archon_project_sources` junction table provides the necessary infrastructure, requiring primarily:

1. **Backend**: Update search functions and services to respect project filtering
2. **MCP**: Add project-aware tools for agent integration
3. **Frontend**: Add UI for managing project-source relationships and filtering

The implementation can be **incremental and backward-compatible**, allowing users to gradually adopt project-scoped knowledge without disrupting existing workflows.

**Estimated Effort**: 4 weeks (1 engineer)
**Complexity**: Medium (mostly additive, no major architectural changes)
**Risk**: Low (junction table already exists, changes are optional features)

---

## Appendix A: Example Usage Patterns

### Pattern 1: Agent Working on Project Task
```python
# MCP tool call from agent
rag_search_project_knowledge(
    query="authentication implementation",
    project_id="proj_abc123",
    match_count=5
)
# Returns only sources linked to proj_abc123
```

### Pattern 2: User Browsing Global Knowledge
```typescript
// Frontend filter
<KnowledgeView
    scopeFilter="global"
    projectId={null}
/>
// Shows all unlinked sources
```

### Pattern 3: User Managing Project Knowledge
```typescript
// In project detail view
<ProjectSourceManager
    projectId="proj_abc123"
    linkedSources={linkedSources}
    onLinkSource={(sourceId) => linkSourceToProject(projectId, sourceId)}
/>
```

### Pattern 4: Search with Auto-Scoping
```python
# When user is viewing a project, automatically scope search
if current_project_id:
    results = rag_service.perform_rag_query(
        query="API patterns",
        project_id=current_project_id
    )
else:
    # Global search
    results = rag_service.perform_rag_query(
        query="API patterns"
    )
```

---

## Appendix B: Database Query Examples

### Get Project Sources
```sql
SELECT s.*, ps.linked_at, ps.notes
FROM archon_sources s
INNER JOIN archon_project_sources ps ON s.source_id = ps.source_id
WHERE ps.project_id = 'proj_abc123'
ORDER BY ps.linked_at DESC;
```

### Get Global (Unlinked) Sources
```sql
SELECT s.*
FROM archon_sources s
LEFT JOIN archon_project_sources ps ON s.source_id = ps.source_id
WHERE ps.project_id IS NULL;
```

### Get All Sources with Project Count
```sql
SELECT s.*,
       COUNT(DISTINCT ps.project_id) as project_count,
       ARRAY_AGG(DISTINCT ps.project_id) as linked_projects
FROM archon_sources s
LEFT JOIN archon_project_sources ps ON s.source_id = ps.source_id
GROUP BY s.source_id;
```

### Search with Project Filter
```sql
-- Step 1: Get source_ids for project
SELECT source_id
FROM archon_project_sources
WHERE project_id = 'proj_abc123';

-- Step 2: Use in vector search
SELECT * FROM match_archon_crawled_pages_multi(
    query_embedding := $1,
    embedding_dimension := 1536,
    match_count := 10,
    source_ids_filter := ARRAY['src_1', 'src_2', 'src_3']
);
```

---

**End of Analysis**
