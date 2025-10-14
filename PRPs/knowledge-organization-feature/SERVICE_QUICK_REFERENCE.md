# Backend Services Quick Reference

Quick reference guide for using the knowledge organization backend services.

---

## Import Services

```python
from src.server.services.knowledge import (
    KnowledgeFolderService,
    KnowledgeTagService,
    AutoTaggingService,
    KnowledgeItemService,
)
from src.server.utils import get_supabase_client

# Initialize services
supabase = get_supabase_client()
folder_service = KnowledgeFolderService(supabase)
tag_service = KnowledgeTagService(supabase)
auto_tag_service = AutoTaggingService()
item_service = KnowledgeItemService(supabase)
```

---

## KnowledgeFolderService

### Create Folder
```python
folder = await folder_service.create_folder(
    project_id="proj_123",
    folder_name="API Documentation",
    description="REST API endpoints and schemas",
    color_hex="#3b82f6",
    icon_name="api"
)
# Returns: {"id": "folder_abc", "project_id": "proj_123", "folder_name": "API Documentation", ...}
```

### List Project Folders
```python
folders = await folder_service.list_project_folders("proj_123")
# Returns: [{"id": "...", "folder_name": "API Documentation", "source_count": 5}, ...]
```

### Update Folder
```python
updated = await folder_service.update_folder(
    folder_id="folder_abc",
    updates={"description": "Updated description", "color_hex": "#10b981"}
)
```

### Delete Folder
```python
success = await folder_service.delete_folder("folder_abc")
# Returns True, sources in folder have folder_id set to NULL
```

### Get Folder
```python
folder = await folder_service.get_folder("folder_abc")
# Returns: {"id": "folder_abc", ...} or None if not found
```

### Get Source Count
```python
count = await folder_service.get_folder_source_count("folder_abc")
# Returns: 5
```

---

## KnowledgeTagService

### Get All Tags
```python
# Get all tags
all_tags = await tag_service.get_all_tags()

# Get tags by category
framework_tags = await tag_service.get_all_tags(category="framework")
# Returns: [{"tag_name": "react", "category": "framework", "usage_count": 15, ...}, ...]
```

### Get Tag By Name
```python
tag = await tag_service.get_tag_by_name("react")
# Returns: {"id": "...", "tag_name": "react", "category": "framework", ...} or None
```

### Get Tags By Category
```python
tags_by_cat = await tag_service.get_tags_by_category()
# Returns: {
#   "framework": ["react", "nextjs", "fastapi"],
#   "language": ["python", "typescript", "javascript"],
#   "security": ["authentication", "encryption"]
# }
```

### Track Tag Usage
```python
# When tag is added to a source
await tag_service.increment_tag_usage("react")

# When tag is removed from a source
await tag_service.decrement_tag_usage("react")
```

---

## AutoTaggingService

### Suggest Tags
```python
# From URL only
tags = await auto_tag_service.suggest_tags(url="https://react.dev")
# Returns: ["react", "javascript"]

# From URL + content
tags = await auto_tag_service.suggest_tags(
    url="https://docs.stripe.com/api",
    title="Stripe API Reference",
    summary="Complete API documentation for Stripe payment processing"
)
# Returns: ["stripe", "api", "payment", "api-reference", "documentation"]
```

### Add Custom Patterns
```python
# Add URL pattern
auto_tag_service.add_url_pattern(
    pattern=r"mycompany\.com",
    tags=["internal", "company"]
)

# Add content keyword
auto_tag_service.add_content_keyword(
    keyword="machine learning",
    tags=["ml", "ai"]
)
```

---

## KnowledgeItemService

### List Items with Scope

#### Get All Knowledge
```python
result = await item_service.list_items(
    page=1,
    per_page=20,
    scope="all"  # Default
)
# Returns: {"items": [...], "total": 50, "page": 1, "pages": 3}
```

#### Get Global Knowledge Only
```python
result = await item_service.list_items(
    scope="global"
)
# Returns only sources where knowledge_scope='global'
```

#### Get Project Knowledge
```python
result = await item_service.list_items(
    scope="project",
    project_id="proj_123"
)
# Returns only sources where knowledge_scope='project' AND project_id='proj_123'
```

#### Combined Filters
```python
result = await item_service.list_items(
    scope="project",
    project_id="proj_123",
    knowledge_type="technical",
    search="authentication",
    page=1,
    per_page=10
)
# Filters by scope, project, type, and search term
```

---

## Common Workflows

### Creating Project Knowledge with Folder

```python
from src.server.services.knowledge import (
    KnowledgeFolderService,
    AutoTaggingService,
)
from src.server.utils import get_supabase_client

supabase = get_supabase_client()
folder_service = KnowledgeFolderService(supabase)
auto_tag_service = AutoTaggingService()

# 1. Create folder for project
folder = await folder_service.create_folder(
    project_id="proj_123",
    folder_name="Authentication",
    description="Auth system documentation",
    color_hex="#f59e0b",
    icon_name="lock"
)

# 2. Suggest tags for new knowledge source
suggested_tags = await auto_tag_service.suggest_tags(
    url="https://auth0.com/docs/get-started",
    title="Auth0 Getting Started",
    summary="Complete guide to implementing Auth0 authentication"
)
# Returns: ["authentication", "security"]

# 3. Create knowledge source (use existing crawling service)
# Set: knowledge_scope='project', project_id='proj_123', folder_id=folder['id']
# Add suggested_tags to metadata

# 4. Update tag usage
for tag in suggested_tags:
    await tag_service.increment_tag_usage(tag)
```

### Listing Project Knowledge with Folders

```python
# Get project folders with counts
folders = await folder_service.list_project_folders("proj_123")

# Get all project knowledge items
items = await item_service.list_items(
    scope="project",
    project_id="proj_123"
)

# Build folder tree structure
folder_tree = []
for folder in folders:
    folder_items = [
        item for item in items["items"]
        if item.get("folder_id") == folder["id"]
    ]
    folder_tree.append({
        "folder": folder,
        "items": folder_items
    })

# Items without folder (root level)
root_items = [
    item for item in items["items"]
    if not item.get("folder_id")
]
```

### Tag Management

```python
# Get tags for dropdown
tags_by_category = await tag_service.get_tags_by_category()

# Display in UI grouped by category
for category, tags in tags_by_category.items():
    print(f"{category}: {', '.join(tags)}")

# When user selects tags, validate they exist
for tag_name in user_selected_tags:
    tag = await tag_service.get_tag_by_name(tag_name)
    if not tag:
        # Tag doesn't exist, handle error
        pass
```

---

## Error Handling

All services raise exceptions on errors with detailed logging:

```python
try:
    folder = await folder_service.create_folder(
        project_id="proj_123",
        folder_name="My Folder"
    )
except ValueError as e:
    # Validation error (missing fields, empty name, etc.)
    print(f"Validation error: {e}")
except Exception as e:
    # Database error or other failure
    print(f"Failed to create folder: {e}")
```

For get operations, None is returned instead of raising:

```python
folder = await folder_service.get_folder("invalid_id")
if folder is None:
    # Folder not found
    pass
```

---

## Performance Notes

### Batch Operations

When working with multiple folders or tags, batch your database queries:

```python
# Good: Single query gets all folders with counts
folders = await folder_service.list_project_folders("proj_123")

# Bad: N+1 queries
folder_ids = [...]
for folder_id in folder_ids:
    folder = await folder_service.get_folder(folder_id)
    count = await folder_service.get_folder_source_count(folder_id)
```

### Scope Filtering

Use scope filtering at the database level for better performance:

```python
# Good: Database-level filtering
items = await item_service.list_items(scope="global")

# Bad: Client-side filtering
items = await item_service.list_items(scope="all")
global_items = [item for item in items["items"] if item["scope"] == "global"]
```

---

## Database Schema Reference

### archon_project_knowledge_folders
```sql
id              UUID PRIMARY KEY
project_id      UUID NOT NULL (FK → archon_projects)
folder_name     TEXT NOT NULL
description     TEXT
color_hex       TEXT DEFAULT '#6366f1'
icon_name       TEXT DEFAULT 'folder'
sort_order      INTEGER DEFAULT 0
created_at      TIMESTAMPTZ
updated_at      TIMESTAMPTZ
UNIQUE (project_id, folder_name)
```

### archon_knowledge_tags
```sql
id                UUID PRIMARY KEY
tag_name          TEXT UNIQUE NOT NULL
category          TEXT NOT NULL
description       TEXT NOT NULL
usage_guidelines  TEXT
color_hex         TEXT
icon_name         TEXT
usage_count       INTEGER DEFAULT 0
created_at        TIMESTAMPTZ
updated_at        TIMESTAMPTZ
```

### archon_sources (new columns)
```sql
knowledge_scope   TEXT DEFAULT 'global' ('global' | 'project')
project_id        UUID (FK → archon_projects, nullable)
folder_id         UUID (FK → archon_project_knowledge_folders, nullable)
```

---

## Next Steps

After implementing API routes, update this guide with:
- API endpoint examples
- Request/response formats
- Frontend service integration examples
- MCP tool usage examples
