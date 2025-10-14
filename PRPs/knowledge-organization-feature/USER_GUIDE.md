# Knowledge Organization System - User Guide

**Version**: 1.0.0
**Date**: 2025-10-14
**For**: Archon Users

---

## Table of Contents

1. [Introduction](#introduction)
2. [Key Concepts](#key-concepts)
3. [Getting Started](#getting-started)
4. [Managing Global Knowledge](#managing-global-knowledge)
5. [Managing Project Knowledge](#managing-project-knowledge)
6. [Using Folders](#using-folders)
7. [Working with Tags](#working-with-tags)
8. [AI Agent Integration](#ai-agent-integration)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Introduction

The Knowledge Organization System provides a structured way to manage documentation and code examples in Archon. It separates **global knowledge** (shared across all work) from **project-specific knowledge** (scoped to individual projects), making it easier for you and AI agents to find relevant information quickly.

### What's New

- **Two-Layer Organization**: Global vs Project-specific knowledge
- **Folder Structure**: Organize project knowledge into folders
- **Auto-Tagging**: Automatic tag suggestions based on content
- **Agent-Friendly**: AI assistants can search by scope and folder
- **Tab Navigation**: Clear separation in the UI

---

## Key Concepts

### Global Knowledge

**Definition**: Documentation and resources that are useful across multiple projects or as general reference.

**Examples**:
- React documentation (react.dev)
- FastAPI framework guides
- PostgreSQL reference documentation
- Security best practices
- General coding patterns

**When to use**: When adding documentation that could be useful for any project, not tied to specific implementation details.

### Project Knowledge

**Definition**: Documentation specific to a particular project's implementation, architecture, or requirements.

**Examples**:
- Custom authentication specification
- Project API endpoint documentation
- Database schema for this project
- Business logic documentation
- Project-specific design decisions

**When to use**: When adding documentation about how THIS specific project works, not general framework knowledge.

### Folders

**Definition**: Organizational containers within a project for grouping related knowledge sources.

**Examples**:
- "Authentication" folder - OAuth, JWT, login docs
- "API Documentation" folder - Endpoint specs, schemas
- "Database" folder - Schema, migrations, query patterns
- "UI Components" folder - Component library docs

**Benefits**: Keep related documentation together, easier to find what you need.

### Tags

**Definition**: Categorical labels that describe the content or technology stack.

**Categories** (11 total):
1. **framework** - React, FastAPI, Django, etc.
2. **language** - Python, TypeScript, JavaScript, etc.
3. **architecture** - Microservices, REST API, GraphQL, etc.
4. **security** - Authentication, Encryption, etc.
5. **testing** - Unit testing, E2E, etc.
6. **deployment** - Docker, Kubernetes, CI/CD
7. **database** - PostgreSQL, MongoDB, Vector search
8. **api** - OpenAPI, WebSockets
9. **ui** - Tailwind, Radix UI, Design systems
10. **documentation** - API reference, Tutorials
11. **general** - Best practices, Getting started

---

## Getting Started

### Accessing the Knowledge Base

1. Navigate to the Knowledge Base page in Archon
2. You'll see three tabs at the top:
   - **Global** - Shared knowledge across all projects
   - **Projects** - Project-specific knowledge with folders
   - **Tags** - Browse by technology/category

### Your First Knowledge Source

**Adding Global Documentation**:
1. Click the **Global** tab
2. Click "Add Global Knowledge" button
3. Enter the URL (e.g., https://react.dev)
4. Tags will be auto-suggested
5. Click "Crawl" to start indexing

**Adding Project Documentation**:
1. Click the **Projects** tab
2. Select a project from the dropdown
3. Click "Add to Project" button
4. Select "Project-Specific" scope
5. Choose a folder (or leave as "Unfiled")
6. Enter URL or upload file
7. Click "Crawl" or "Upload"

---

## Managing Global Knowledge

### Viewing Global Knowledge

1. Click the **Global** tab
2. See all shared documentation sources
3. Sources display:
   - Title and URL
   - Number of chunks (document sections)
   - Number of code examples extracted
   - Tags applied
   - Actions (Refresh, Delete)

### Adding Global Knowledge

**Via URL Crawl**:
```
1. Click "Add Global Knowledge"
2. Select "Crawl URL" tab
3. Enter URL: https://docs.example.com
4. Review suggested tags (auto-generated from URL)
5. Add/remove tags as needed
6. Set crawl depth (default: 2)
7. Toggle "Extract code examples" if needed
8. Click "Crawl"
```

**Via File Upload**:
```
1. Click "Add Global Knowledge"
2. Select "Upload File" tab
3. Choose file (.pdf, .md, .txt)
4. Review/edit suggested tags
5. Click "Upload"
```

### When to Use Global

Use global knowledge when:
- Documentation is useful for multiple projects
- It's framework or language reference material
- It contains general best practices
- Multiple team members might need it
- It's not project-specific implementation details

---

## Managing Project Knowledge

### Viewing Project Knowledge

1. Click the **Projects** tab
2. Select a project from dropdown
3. See folders and unfiled items:
   - **Folders** - Expandable sections with counts
   - **Unfiled Items** - Not assigned to any folder
   - Each item shows title, tags, folder (if any)

### Adding Project Knowledge

**Step-by-Step**:
```
1. Click "Add to Project" (in Projects tab)
2. Dialog opens with scope pre-selected as "Project-Specific"
3. Project is pre-selected (from dropdown)
4. Choose a folder (optional):
   - Select existing folder OR
   - Click "+ New Folder" to create one
5. Enter URL or upload file
6. Review/edit tags
7. Click "Crawl" or "Upload"
```

### When to Use Project Knowledge

Use project-scoped knowledge when:
- Documentation describes this project's architecture
- It contains project-specific implementation details
- It's custom code or specifications
- It's only relevant to this project
- Team needs to understand THIS project, not general concepts

---

## Using Folders

### Creating Folders

**From Projects Tab**:
```
1. Select a project
2. Click "+ New Folder" button
3. Enter folder name (e.g., "Authentication")
4. Add description (optional but recommended)
5. Choose color (for visual organization)
6. Choose icon (folder, lock, code, etc.)
7. Click "Create"
```

**From Add Dialog**:
```
1. When adding project knowledge
2. In "Folder" dropdown, select "+ New Folder"
3. Quick-create dialog appears
4. Enter name and click "Create"
5. Automatically selected for current source
```

### Organizing with Folders

**Recommended Folder Structure**:
```
Project: E-commerce Platform
├── 📁 Authentication (3 sources)
│   ├── OAuth 2.0 Implementation
│   ├── JWT Best Practices
│   └── Custom Auth Spec
│
├── 📁 API Documentation (5 sources)
│   ├── Endpoint Reference
│   ├── Request/Response Schemas
│   └── Error Handling Guide
│
├── 📁 Database (2 sources)
│   ├── Schema Design
│   └── Migration Scripts
│
└── 📁 UI Components (4 sources)
    ├── Design System
    ├── Component Library
    └── Styling Guide
```

### Moving Sources Between Folders

Currently, sources are assigned to folders when added. To change folder assignment:
1. Delete source from current location
2. Re-add to project with new folder selection

**Future Enhancement**: Drag-and-drop folder reorganization

### Folder Best Practices

- **Keep folders focused**: Each folder should have a clear theme
- **Use descriptive names**: "Authentication" not "Auth Stuff"
- **Add descriptions**: Help future you remember what goes here
- **Color-code by type**:
  - Blue for UI/Frontend
  - Green for Backend/API
  - Red for Security
  - Yellow for Database
  - Purple for Testing
- **Limit folder count**: 5-10 folders per project is ideal

---

## Working with Tags

### Viewing Tags

1. Click the **Tags** tab
2. See tags organized by category
3. Each tag shows:
   - Tag name with usage count
   - Description
   - Usage guidelines
   - Color indicator

### Auto-Tagging

**How It Works**:
When you add knowledge, tags are automatically suggested based on:

1. **URL Patterns**:
   - `react.dev` → ["react", "javascript"]
   - `fastapi.tiangolo.com` → ["fastapi", "python"]
   - `docs.docker.com` → ["docker", "deployment"]

2. **Content Keywords**:
   - "authentication" in title/summary → ["authentication", "security"]
   - "testing" in content → ["testing"]
   - "API reference" → ["api-reference", "documentation"]

**You Can**:
- Accept suggested tags
- Remove unwanted tags
- Add additional tags
- Edit tags before saving

### Tag Categories Explained

**framework** - Frameworks and libraries
- react, nextjs, fastapi, django, express
- Use for framework-specific documentation

**language** - Programming languages
- python, typescript, javascript, rust, go
- Use for language syntax and standard libraries

**architecture** - Architectural patterns
- microservices, rest-api, graphql, event-driven
- Use for system design and architecture docs

**security** - Security practices and tools
- authentication, authorization, encryption
- Use for security-related documentation

**testing** - Testing methodologies
- unit-testing, integration-testing, e2e-testing
- Use for test frameworks and testing guides

**deployment** - Deployment and infrastructure
- docker, kubernetes, ci-cd
- Use for deployment, containers, pipelines

**database** - Database systems
- postgresql, mongodb, redis, vector-search
- Use for database documentation and queries

**api** - API specifications
- openapi, websockets
- Use for API documentation formats

**ui** - UI frameworks and design
- tailwind, radix-ui, design-system
- Use for UI components and styling

**documentation** - Documentation types
- api-reference, tutorial, architecture-docs
- Use to categorize documentation style

**general** - Miscellaneous
- best-practices, getting-started
- Use for uncategorized or general topics

### Tag Search (Future Feature)

**Planned**:
- Click tag to see all sources with that tag
- Filter knowledge by multiple tags
- Tag-based recommendations

---

## AI Agent Integration

### How Agents Use Knowledge

AI assistants (Claude, Cursor, Windsurf) use MCP tools to search your knowledge base. With the organization system, agents can:

1. **Search Project Knowledge First**:
   ```python
   # Agent working on project "proj_123"
   results = rag_search_project_knowledge(
       "authentication flow",
       "proj_123"
   )
   ```

2. **Fall Back to Global Knowledge**:
   ```python
   # If project search returns nothing
   if not results:
       results = rag_search_global_knowledge(
           "OAuth 2.0 best practices",
           tags=["security", "oauth"]
       )
   ```

3. **Search Specific Folders**:
   ```python
   # Look only in API folder
   results = rag_search_project_knowledge(
       "endpoint schema",
       "proj_123",
       folder_name="API Documentation"
   )
   ```

### Agent Decision Pattern

```
Agent needs information
    │
    ├─ Working on specific project?
    │   │
    │   ├─ YES → Search project knowledge
    │   │   │
    │   │   ├─ Found? → Use that
    │   │   └─ Not found? → Try global
    │   │
    │   └─ NO → Search global only
    │
    └─ General question? → Global search with tags
```

### CLAUDE.md Updates

Update your project's CLAUDE.md file with:

```markdown
## Knowledge Base Context

**Project**: My Project Name
**Project ID**: proj_abc123

### Search Strategy

**For project-specific questions** (implementation details):
```
rag_search_project_knowledge("custom auth", "proj_abc123")
```

**For framework/language questions**:
```
rag_search_global_knowledge("React hooks", tags=["react"])
```

**For folder-specific searches**:
```
rag_search_project_knowledge(
    "API endpoints",
    "proj_abc123",
    folder_name="API Documentation"
)
```

### Available Folders

- Authentication - OAuth, JWT, login flows
- API Documentation - Endpoints, schemas, examples
- Database - Schema, migrations, queries

### MCP Tools

- `rag_get_available_sources(scope="project", project_id="proj_abc123")` - List project sources
- `rag_list_project_folders("proj_abc123")` - List folders
- `rag_search_project_knowledge(query, project_id)` - Search project knowledge
- `rag_search_global_knowledge(query, tags)` - Search global knowledge
```

---

## Best Practices

### Knowledge Organization

1. **Start with Global**:
   - Add framework documentation first
   - Build a shared foundation
   - Keep it curated (don't add everything)

2. **Add Project Knowledge as Needed**:
   - When starting a new project
   - When documenting custom implementations
   - When you need project-specific reference

3. **Use Folders Consistently**:
   - Same folder names across projects (e.g., "Authentication")
   - Helps agents learn patterns
   - Easier to find things

4. **Tag Appropriately**:
   - Accept auto-tags when accurate
   - Add technology stack tags
   - Use consistent tagging across sources

### Content Selection

**Good Global Knowledge**:
- Official framework documentation
- Language reference guides
- Security best practices
- Design pattern libraries
- Testing frameworks

**Good Project Knowledge**:
- Architecture decision records
- Custom API specifications
- Database schema docs
- Project-specific patterns
- Business logic documentation

**Avoid**:
- Duplicate content (if it's in global, don't add to project)
- Outdated documentation
- Tutorial sites (prefer official docs)
- Low-quality content

### Maintenance

**Regular Tasks**:
- Review unfiled items monthly
- Update outdated sources (refresh)
- Remove deprecated documentation
- Reorganize folders as project grows
- Check tag accuracy

**Signs You Need to Reorganize**:
- Can't find documentation quickly
- Folder has 20+ sources (split it)
- Lots of unfiled items
- Duplicate or overlapping sources

---

## Troubleshooting

### Common Issues

**Q: "I added a source but it's not showing up"**

A: Check:
1. Refresh the browser
2. Look in correct tab (Global vs Projects)
3. If project knowledge, make sure correct project selected
4. Check if crawl/upload completed (may take time)

**Q: "Auto-tags are wrong"**

A: You can:
1. Remove incorrect tags before saving
2. Add correct tags manually
3. Tags are suggestions - always review them

**Q: "Can't find a source I added"**

A: Try:
1. Search in the search bar (searches titles and URLs)
2. Check both Global and Projects tabs
3. Look in "Unfiled Items" if project knowledge
4. Check if it was added to a different project

**Q: "Folder organization is confusing"**

A: Best practices:
1. Keep folder names short and clear
2. Add descriptions to folders
3. Use colors consistently (e.g., blue=UI, green=backend)
4. Don't create too many folders (5-10 is ideal)

**Q: "Agent can't find project documentation"**

A: Verify:
1. Source is tagged as project-scoped (not global)
2. Source is linked to correct project
3. Agent knows the project ID (in CLAUDE.md)
4. Source has relevant tags

**Q: "How do I move a source between Global and Project?"**

A: Currently:
1. Note the URL and settings
2. Delete from current location
3. Re-add with new scope
4. Future: UI will support direct moving

**Q: "Can I share folders between projects?"**

A: No, folders are per-project only. This is by design to keep projects independent. If documentation is useful across projects, add it as global knowledge instead.

---

## Tips and Tricks

### Power User Tips

1. **Use Consistent Folder Names**:
   - Same folder names across projects
   - Agents learn patterns
   - Easier mental model

2. **Tag with Tech Stack**:
   - Always include framework tags
   - Include language tags
   - Helps filter later

3. **Organize by Development Phase**:
   - "Architecture" folder for planning docs
   - "Implementation" folder for code guides
   - "Testing" folder for test specs
   - "Deployment" folder for ops docs

4. **Use Color Coding**:
   - Pick colors that make sense to you
   - Be consistent across projects
   - Visual scanning is faster

5. **Review Regularly**:
   - Monthly: Check for outdated sources
   - Quarterly: Reorganize if needed
   - After major refactors: Update docs

### Keyboard Shortcuts

(To be implemented in future versions)

---

## Getting Help

### Documentation

- This User Guide
- `DESIGN_SPECIFICATION.md` - Complete technical design
- `IMPLEMENTATION_STATUS.md` - Current feature status
- MCP Tool docs in knowledge-organization folder

### Support

- GitHub Issues: Report bugs or request features
- Community: Share tips and best practices

---

## What's Next?

### Planned Features (Future Versions)

- **Drag-and-drop**: Move sources between folders in UI
- **Nested folders**: Folders within folders for large projects
- **Tag filtering**: Click tag to filter all knowledge
- **Source sharing**: Share sources across projects
- **Bulk operations**: Move/delete multiple sources at once
- **Knowledge analytics**: Usage stats, popular tags
- **Smart recommendations**: Suggest related documentation

### Current Limitations

- No nested folders (single-level only)
- Can't move sources via UI (must delete/re-add)
- Tags are flat (no hierarchy)
- Folders can't be shared between projects

---

## Summary

The Knowledge Organization System helps you:
- **Separate concerns**: Global (shared) vs Project (specific) knowledge
- **Stay organized**: Folders group related documentation
- **Find quickly**: Tags categorize by technology
- **Help agents**: Clear scope helps AI find relevant docs

**Key Takeaway**: When adding knowledge, ask yourself:
- "Will this be useful for other projects?" → **Global**
- "Is this specific to this project's implementation?" → **Project**

Start simple, organize as you go, and adjust as needed. The system grows with your projects.

---

**Version**: 1.0.0
**Last Updated**: 2025-10-14
**Feedback**: Please report issues or suggestions on GitHub
