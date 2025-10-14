# Phase 2 API Endpoints Documentation

**Date**: October 14, 2025
**Phase**: Phase 2 - API Endpoints
**Status**: ✅ Complete

---

## Executive Summary

Successfully implemented all API endpoints for the Knowledge Organization System. This includes updates to existing knowledge endpoints to support scope filtering and two new API modules for folder and tag management. All endpoints follow FastAPI best practices, include comprehensive error handling, and integrate seamlessly with the Phase 1 backend services.

---

## Updated Endpoints

### 1. GET /api/knowledge-items

**Enhanced with scope filtering**

**URL**: `GET /api/knowledge-items`

**Query Parameters**:
- `page` (int): Page number (default: 1)
- `per_page` (int): Items per page (default: 20)
- `knowledge_type` (str, optional): Filter by type
- `search` (str, optional): Search term
- **`project_id` (str, optional)**: Filter by project ID (NEW)
- **`scope` (str, optional)**: Scope filter - "all" (default), "global", "project" (NEW)

**Example Requests**:
```bash
# Get all knowledge
GET /api/knowledge-items?scope=all

# Get only global knowledge
GET /api/knowledge-items?scope=global

# Get project-specific knowledge
GET /api/knowledge-items?scope=project&project_id=proj_123

# Search within project knowledge
GET /api/knowledge-items?scope=project&project_id=proj_123&search=authentication
```

**Response**:
```json
{
  "items": [...],
  "total": 42,
  "page": 1,
  "per_page": 20,
  "pages": 3
}
```

---

### 2. POST /api/knowledge-items/crawl

**Enhanced with scope and folder parameters**

**URL**: `POST /api/knowledge-items/crawl`

**Request Body** (NEW fields):
```json
{
  "url": "https://example.com",
  "knowledge_type": "technical",
  "tags": ["documentation"],
  "max_depth": 2,
  "extract_code_examples": true,
  "scope": "project",
  "project_id": "proj_123",
  "folder_id": "folder_xyz"
}
```

**New Fields**:
- `scope` (str): "global" (default) or "project"
- `project_id` (str, optional): Required when scope="project"
- `folder_id` (str, optional): Folder for organization

---

## New API Module: Knowledge Folders

**Base Path**: `/api/knowledge/folders`

### POST /api/knowledge/folders

**Create a new knowledge folder for a project**

**Request Body**:
```json
{
  "project_id": "proj_123",
  "folder_name": "API Documentation",
  "description": "REST API endpoints and schemas",
  "color_hex": "#3b82f6",
  "icon_name": "api"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "folder": {
    "id": "folder_abc",
    "project_id": "proj_123",
    "folder_name": "API Documentation",
    "description": "REST API endpoints and schemas",
    "color_hex": "#3b82f6",
    "icon_name": "api",
    "sort_order": 0,
    "created_at": "2025-10-14T10:30:00Z",
    "updated_at": "2025-10-14T10:30:00Z"
  }
}
```

---

### GET /api/knowledge/folders/{folder_id}

**Get a specific folder by ID**

**URL**: `GET /api/knowledge/folders/folder_abc`

**Response**:
```json
{
  "success": true,
  "folder": {
    "id": "folder_abc",
    "project_id": "proj_123",
    "folder_name": "API Documentation",
    "description": "REST API endpoints and schemas",
    "color_hex": "#3b82f6",
    "icon_name": "api",
    "sort_order": 0,
    "source_count": 5,
    "created_at": "2025-10-14T10:30:00Z",
    "updated_at": "2025-10-14T10:30:00Z"
  }
}
```

**Error Responses**:
- 404 Not Found: Folder doesn't exist

---

### PUT /api/knowledge/folders/{folder_id}

**Update folder metadata**

**Request Body** (all fields optional):
```json
{
  "folder_name": "Updated Name",
  "description": "Updated description",
  "color_hex": "#ef4444",
  "icon_name": "folder",
  "sort_order": 5
}
```

**Response**:
```json
{
  "success": true,
  "folder": {
    "id": "folder_abc",
    "folder_name": "Updated Name",
    ...
  }
}
```

**Error Responses**:
- 400 Bad Request: No update fields provided
- 404 Not Found: Folder doesn't exist

---

### DELETE /api/knowledge/folders/{folder_id}

**Delete a folder (sources remain, folder_id set to NULL)**

**URL**: `DELETE /api/knowledge/folders/folder_abc`

**Response**:
```json
{
  "success": true,
  "message": "Folder folder_abc deleted successfully"
}
```

**Error Responses**:
- 404 Not Found: Folder doesn't exist

**Important**: Sources in this folder are NOT deleted. They are unlinked (folder_id set to NULL) but remain in the knowledge base.

---

### GET /api/knowledge/folders/projects/{project_id}/list

**List all folders for a project**

**URL**: `GET /api/knowledge/folders/projects/proj_123/list`

**Response**:
```json
{
  "success": true,
  "project_id": "proj_123",
  "folders": [
    {
      "id": "folder_abc",
      "folder_name": "API Documentation",
      "description": "REST API endpoints",
      "color_hex": "#3b82f6",
      "icon_name": "api",
      "sort_order": 0,
      "source_count": 5,
      "created_at": "2025-10-14T10:30:00Z",
      "updated_at": "2025-10-14T10:30:00Z"
    }
  ],
  "count": 1
}
```

**Ordering**: Results are ordered by `sort_order` ASC, then `created_at` ASC.

---

## New API Module: Knowledge Tags

**Base Path**: `/api/knowledge/tags`

### GET /api/knowledge/tags

**Get all tags with optional category filter**

**URL**: `GET /api/knowledge/tags`

**Query Parameters**:
- `category` (str, optional): Filter by category

**Example Requests**:
```bash
# Get all tags
GET /api/knowledge/tags

# Get only framework tags
GET /api/knowledge/tags?category=framework
```

**Response**:
```json
{
  "success": true,
  "tags": [
    {
      "id": "tag_1",
      "tag_name": "react",
      "category": "framework",
      "description": "React framework for building user interfaces",
      "usage_guidelines": "Use for React-specific documentation, component patterns, hooks usage",
      "color_hex": "#61dafb",
      "icon_name": "react",
      "usage_count": 15,
      "created_at": "2025-10-14T10:00:00Z",
      "updated_at": "2025-10-14T10:30:00Z"
    }
  ],
  "count": 1
}
```

---

### GET /api/knowledge/tags/{tag_name}

**Get a specific tag by name (case-insensitive)**

**URL**: `GET /api/knowledge/tags/react`

**Response**:
```json
{
  "success": true,
  "tag": {
    "id": "tag_1",
    "tag_name": "react",
    "category": "framework",
    "description": "React framework for building user interfaces",
    "usage_guidelines": "Use for React-specific documentation...",
    "color_hex": "#61dafb",
    "usage_count": 15
  }
}
```

**Error Responses**:
- 404 Not Found: Tag doesn't exist

---

### GET /api/knowledge/tags/categories/grouped

**Get all tags organized by category**

**URL**: `GET /api/knowledge/tags/categories/grouped`

**Response**:
```json
{
  "success": true,
  "categories": {
    "framework": ["react", "nextjs", "fastapi", "django"],
    "language": ["python", "typescript", "javascript"],
    "architecture": ["microservices", "rest-api", "graphql"],
    "security": ["authentication", "authorization", "encryption"]
  },
  "category_counts": {
    "framework": 4,
    "language": 3,
    "architecture": 3,
    "security": 3
  },
  "total_tags": 13
}
```

---

### POST /api/knowledge/tags/suggest

**Suggest tags based on URL and content**

**Request Body**:
```json
{
  "url": "https://react.dev",
  "title": "React Documentation",
  "summary": "Learn React with comprehensive documentation covering hooks, components, and best practices"
}
```

**Response**:
```json
{
  "success": true,
  "suggested_tags": ["react", "javascript", "documentation", "tutorial"],
  "count": 4,
  "source": {
    "url": "https://react.dev",
    "title": "React Documentation"
  }
}
```

**Tag Suggestion Logic**:
- URL pattern matching (e.g., `react.dev` → ["react", "javascript"])
- Content keyword analysis
- Title and summary parsing
- Deduplication and ordering

---

## Error Handling

All endpoints follow consistent error response format:

**400 Bad Request**:
```json
{
  "error": "Validation error message"
}
```

**404 Not Found**:
```json
{
  "error": "Resource not found message"
}
```

**500 Internal Server Error**:
```json
{
  "error": "Error description"
}
```

---

## Integration with Backend Services

### Service Dependencies

1. **KnowledgeItemService** (`knowledge_item_service.py`)
   - Updated `list_items()` method with `project_id` and `scope` parameters
   - Handles scope filtering at database level for performance

2. **KnowledgeFolderService** (`knowledge_folder_service.py`)
   - `create_folder()` - Creates folders with validation
   - `get_folder()` - Retrieves single folder with source count
   - `update_folder()` - Updates metadata fields
   - `delete_folder()` - Soft delete (unlinks sources)
   - `list_project_folders()` - Lists folders with counts

3. **KnowledgeTagService** (`knowledge_tag_service.py`)
   - `get_all_tags()` - Retrieves tags with optional category filter
   - `get_tag_by_name()` - Case-insensitive tag lookup
   - `get_tags_by_category()` - Groups tags by category

4. **AutoTaggingService** (`auto_tagging_service.py`)
   - `suggest_tags()` - Pattern-based tag suggestion
   - URL pattern matching (20+ patterns)
   - Content keyword analysis (15+ keywords)

---

## Request/Response Patterns

### Standard Success Response
```json
{
  "success": true,
  "data": {...}
}
```

### Paginated Response
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "per_page": 20,
  "pages": 5
}
```

### List Response
```json
{
  "success": true,
  "[resource]s": [...],
  "count": 10
}
```

---

## HTTP Status Codes

- **200 OK**: Successful GET/PUT requests
- **201 Created**: Successful POST requests
- **400 Bad Request**: Validation errors, missing required fields
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side errors

---

## Logging and Monitoring

All endpoints include comprehensive logging:

**Info Level**:
- Operation start with key parameters
- Successful completion with result counts

**Error Level**:
- Failed operations with error details
- Validation failures

**Example Log Output**:
```
INFO  Creating knowledge folder | project_id=proj_123 | folder_name=API Documentation
INFO  Knowledge folder created successfully | folder_id=folder_abc | project_id=proj_123
```

---

## Testing Recommendations

### Manual Testing

**Test Folder CRUD Flow**:
```bash
# Create folder
curl -X POST http://localhost:8181/api/knowledge/folders \
  -H "Content-Type: application/json" \
  -d '{"project_id": "proj_123", "folder_name": "Test Folder"}'

# Get folder
curl http://localhost:8181/api/knowledge/folders/{folder_id}

# Update folder
curl -X PUT http://localhost:8181/api/knowledge/folders/{folder_id} \
  -H "Content-Type: application/json" \
  -d '{"description": "Updated description"}'

# List project folders
curl http://localhost:8181/api/knowledge/folders/projects/proj_123/list

# Delete folder
curl -X DELETE http://localhost:8181/api/knowledge/folders/{folder_id}
```

**Test Tag Endpoints**:
```bash
# Get all tags
curl http://localhost:8181/api/knowledge/tags

# Get specific tag
curl http://localhost:8181/api/knowledge/tags/react

# Get grouped tags
curl http://localhost:8181/api/knowledge/tags/categories/grouped

# Suggest tags
curl -X POST http://localhost:8181/api/knowledge/tags/suggest \
  -H "Content-Type: application/json" \
  -d '{"url": "https://react.dev", "title": "React", "summary": "React documentation"}'
```

**Test Scope Filtering**:
```bash
# Get global knowledge only
curl "http://localhost:8181/api/knowledge-items?scope=global"

# Get project knowledge
curl "http://localhost:8181/api/knowledge-items?scope=project&project_id=proj_123"

# Search within project
curl "http://localhost:8181/api/knowledge-items?scope=project&project_id=proj_123&search=auth"
```

---

## Files Modified/Created

### Created Files
1. `/api_routes/knowledge_folders_api.py` (302 lines)
   - 5 endpoints for folder management
   - Complete CRUD operations
   - Pydantic models for request validation

2. `/api_routes/knowledge_tags_api.py` (201 lines)
   - 4 endpoints for tag operations
   - Tag retrieval and suggestion
   - Category grouping support

### Modified Files
1. `/api_routes/knowledge_api.py`
   - Updated `get_knowledge_items()` with scope parameters
   - Updated `KnowledgeItemRequest` model with scope fields
   - Backward compatible (scope defaults to "all")

2. `/main.py`
   - Added imports for new routers
   - Registered `knowledge_folders_router` and `knowledge_tags_router`

---

## Next Steps (Phase 3)

### MCP Tool Integration
1. Update `rag_get_available_sources` to use scope filtering
2. Update `rag_search_knowledge_base` with scope parameter
3. Create new convenience tools:
   - `rag_search_project_knowledge`
   - `rag_search_global_knowledge`
   - `rag_list_project_folders`

### Frontend Integration (Phase 4)
1. Update AddKnowledgeDialog with scope selector
2. Create folder management UI components
3. Implement tag selection with auto-suggestions
4. Add scope filtering to knowledge list views

---

## Summary

Phase 2 API Endpoints are complete and ready for integration. All endpoints:

- ✅ Follow FastAPI best practices
- ✅ Include comprehensive error handling
- ✅ Use Pydantic for request validation
- ✅ Integrate with Phase 1 backend services
- ✅ Include detailed logging
- ✅ Support proper HTTP status codes
- ✅ Are backward compatible where applicable

**Total Endpoints Created/Updated**: 10 endpoints
**Total Lines of Code**: ~550 lines of production code
**Next Phase**: MCP Tool Updates (Phase 3)

---

**Implemented by**: Claude Code
**Date**: October 14, 2025
**Ready for Phase 3**: ✅ Yes
