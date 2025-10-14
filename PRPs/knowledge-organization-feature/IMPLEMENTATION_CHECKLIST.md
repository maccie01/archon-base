# Implementation Checklist - Two-Layer Knowledge Organization

**Quick reference for implementing the knowledge organization system.**

---

## Database Changes

- [ ] Create migration `012_add_knowledge_scope_and_project_linking.sql`
- [ ] Add `knowledge_scope` column to `archon_sources` (global/project)
- [ ] Add `project_id` column to `archon_sources`
- [ ] Add `folder_id` column to `archon_sources`
- [ ] Create `archon_knowledge_tags` table
- [ ] Create `archon_project_knowledge_folders` table
- [ ] Add indexes for scope filtering
- [ ] Add constraints (project_id required when scope='project')
- [ ] Seed standard tags (40+ tags across 11 categories)
- [ ] Update existing sources to scope='global'

---

## Backend Services

### New Services

- [ ] `KnowledgeFolderService` - Folder CRUD operations
  - Location: `python/src/server/services/knowledge/knowledge_folder_service.py`
- [ ] `KnowledgeTagService` - Tag management
  - Location: `python/src/server/services/knowledge/knowledge_tag_service.py`
- [ ] `AutoTaggingService` - Automatic tag suggestions
  - Location: `python/src/server/services/knowledge/auto_tagging_service.py`

### Service Updates

- [ ] Update `KnowledgeItemService.list_items()` - Add scope filtering
- [ ] Update `KnowledgeItemService.get_item()` - Include scope info
- [ ] Update `CrawlingService` - Set scope and project_id during crawl
- [ ] Update `DocumentStorageService` - Handle scope for uploads

---

## API Endpoints

### New Endpoints

- [ ] `GET /api/knowledge/global` - List global sources
- [ ] `GET /api/knowledge/projects/:projectId` - List project sources
- [ ] `GET /api/knowledge/tags` - List all tags with descriptions
- [ ] `POST /api/knowledge/folders` - Create folder
- [ ] `PUT /api/knowledge/folders/:folderId` - Update folder
- [ ] `DELETE /api/knowledge/folders/:folderId` - Delete folder

### Endpoint Updates

- [ ] `POST /api/knowledge-items/crawl` - Add scope, project_id, folder_id
- [ ] `POST /api/documents/upload` - Add scope, project_id, folder_id
- [ ] `GET /api/knowledge-items` - Add scope filter parameter
- [ ] `GET /api/knowledge-items/summary` - Include scope info

---

## MCP Tools

### Updated Tools

- [ ] `rag_get_available_sources` - Add scope and project_id parameters
  - Return scope, project_id, folder_name in results
- [ ] `rag_search_knowledge_base` - Add scope and project_id parameters
  - Support "global", "project", "all" scope values

### New Tools

- [ ] `rag_search_project_knowledge` - Convenience wrapper for project search
- [ ] `rag_search_global_knowledge` - Convenience wrapper for global search
- [ ] `rag_list_project_folders` - List folders for a project

---

## Frontend Components

### New Components

- [ ] `KnowledgeTabs.tsx` - Tab container (Global/Projects/Tags)
- [ ] `GlobalKnowledgeView.tsx` - Global knowledge list view
- [ ] `ProjectKnowledgeView.tsx` - Project-scoped knowledge with folders
- [ ] `TagsIndexView.tsx` - Tag index organized by category
- [ ] `KnowledgeFolderTree.tsx` - Folder tree component
- [ ] `FolderManagementDialog.tsx` - Create/edit folders
- [ ] `ScopeSelector.tsx` - Global vs Project selector

### Component Updates

- [ ] `AddKnowledgeDialog.tsx` - Add scope selection
- [ ] `KnowledgeCard.tsx` - Show scope badge
- [ ] `KnowledgeList.tsx` - Filter by scope

### Types

- [ ] Update `KnowledgeItem` interface - Add scope, project_id, folder_id
- [ ] Create `KnowledgeFolder` type
- [ ] Create `KnowledgeTag` type
- [ ] Create `KnowledgeScope` type ("global" | "project")

---

## Frontend Services

- [ ] `knowledgeFolderService.ts` - Folder API calls
- [ ] `knowledgeTagService.ts` - Tag API calls
- [ ] Update `knowledgeService.ts` - Add scope parameters

---

## Frontend Hooks

- [ ] `useKnowledgeFolders(projectId)` - Fetch project folders
- [ ] `useKnowledgeTags()` - Fetch all tags
- [ ] `useCreateFolder()` - Create folder mutation
- [ ] `useUpdateFolder()` - Update folder mutation
- [ ] `useDeleteFolder()` - Delete folder mutation
- [ ] Update `useKnowledgeSummaries()` - Add scope filter

---

## Testing

### Unit Tests

- [ ] `test_knowledge_scope_service.py`
- [ ] `test_knowledge_folder_service.py`
- [ ] `test_knowledge_tag_service.py`
- [ ] `test_auto_tagging_service.py`
- [ ] `KnowledgeTabs.test.tsx`
- [ ] `KnowledgeFolderTree.test.tsx`
- [ ] `ScopeSelector.test.tsx`

### Integration Tests

- [ ] API route tests for new endpoints
- [ ] MCP tool tests with scope parameters
- [ ] End-to-end workflow tests

### Test Scenarios

- [ ] Create global knowledge source
- [ ] Create project-specific source with folder
- [ ] Search global knowledge via MCP
- [ ] Search project knowledge via MCP
- [ ] Move source between scopes
- [ ] Delete folder (sources remain)
- [ ] Auto-tagging accuracy

---

## Documentation

- [ ] Update main `README.md` with knowledge organization section
- [ ] Create `KNOWLEDGE_ORGANIZATION.md` user guide
- [ ] Update `CLAUDE.md` template with search patterns
- [ ] Document MCP tools with scope examples
- [ ] Create migration guide for existing users
- [ ] Add agent workflow examples

---

## Migration

- [ ] Test migration on existing Archon installation
- [ ] Verify all sources default to global scope
- [ ] Test backward compatibility (existing MCP tools)
- [ ] Document migration steps
- [ ] Create rollback plan (if needed)

---

## Performance Targets

- [ ] Scope filtering: <50ms for 1000+ sources
- [ ] Search with scope: <200ms
- [ ] Folder tree render: <100ms for 50 folders
- [ ] Tag index load: <50ms for 200 tags
- [ ] Auto-tagging: <100ms per source

---

## Deployment Checklist

- [ ] Run database migration
- [ ] Restart backend services
- [ ] Deploy frontend changes
- [ ] Verify MCP tools working
- [ ] Test UI tabs and navigation
- [ ] Check auto-tagging functionality
- [ ] Monitor performance metrics
- [ ] Gather user feedback

---

## Future Enhancements (Not in V1)

- [ ] Nested folders (folder hierarchy)
- [ ] Tag hierarchy (parent-child relationships)
- [ ] Knowledge source sharing across projects
- [ ] Bulk tagging operations
- [ ] Tag synonyms and aliases
- [ ] Knowledge analytics dashboard
- [ ] Smart folder suggestions
- [ ] Cross-project knowledge linking

---

**Status**: Ready for Implementation
**Estimated Timeline**: 5 weeks (5 phases)
**Priority**: High
**Impact**: Major feature enhancement
