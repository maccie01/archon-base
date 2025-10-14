# Archon Knowledge Base Design Guide

## Overview

Archon uses a hybrid model that combines:

1. **Centralized Knowledge Base** (all sources in one pool)
2. **Project-specific linking** (connect relevant sources to projects)

## Architecture

### Knowledge Base (Global Pool)
```
├── Source 1: React Documentation
├── Source 2: Express Documentation
├── Source 3: Netzwächter Architecture Docs
├── Source 4: Netzwächter Coding Standards
├── Source 5: Authentication Patterns
└── Source 6: Drizzle ORM Guide
```

### Projects (Work Organization)
```
├── Project: Netzwächter Refactor
│   ├── Links to: Source 3, 4, 5
│   ├── Tasks: 457 refactoring tasks
│   └── Documents: Refactor plans, decisions
└── Project: Another Project
    ├── Links to: Source 1, 2, 6
    └── Tasks: ...
```

## Key Database Tables

### `archon_sources`: Global Knowledge Base
- Each source (website crawl, uploaded doc) gets unique `source_id`
- Metadata includes: `knowledge_type`, `tags`, `title`, `summary`
- No direct project relationship

### `archon_projects`: Project Management
- Projects have `features`, `docs`, `github_repo`
- Independent of sources

### `archon_project_sources`: Many-to-Many Linking
- Links projects to relevant sources
- One source can be linked to multiple projects
- One project can link to multiple sources

## Recommended Usage Patterns

### Pattern 1: Centralized Global Knowledge (Recommended)

#### How It Works
- Store **ALL** knowledge in one global pool
- Use `knowledge_type` and `tags` to organize
- Projects link to relevant sources
- Search works across everything

#### For Netzwächter: Knowledge Base Sources
1. React docs (`knowledge_type: "dependency"`, `tags: ["react", "ui"]`)
2. Express docs (`knowledge_type: "dependency"`, `tags: ["express", "backend"]`)
3. Drizzle docs (`knowledge_type: "dependency"`, `tags: ["drizzle", "database"]`)
4. Netzwächter Architecture (`knowledge_type: "documentation"`, `tags: ["netzwaechter", "architecture"]`)
5. Coding Standards (`knowledge_type: "standards"`, `tags: ["netzwaechter", "patterns"]`)
6. Legacy Patterns to Avoid (`knowledge_type: "legacy"`, `tags: ["netzwaechter", "deprecated"]`)

#### Project: Netzwächter Refactor
```
├── Linked Sources: #4, #5, #6
├── Tasks reference knowledge via MCP search
└── AI searches all sources but weighted toward linked ones
```

#### Advantages
- ✅ Single source of truth
- ✅ No duplication
- ✅ Easy to share knowledge across projects
- ✅ Can search everything at once
- ✅ Sources like "React docs" benefit all React projects

#### Disadvantages
- ⚠️ Need good tagging discipline
- ⚠️ Large knowledge base (but search is smart)

### Pattern 2: Project-Specific Knowledge

#### How It Works
- Upload project-specific docs with project name in tags
- Filter searches by project tags
- More isolated

#### Example: Sources
- "Netzwächter Auth Module" (`tags: ["netzwaechter", "auth"]`)
- "Netzwächter Frontend Patterns" (`tags: ["netzwaechter", "frontend"]`)
- "OtherProject API Docs" (`tags: ["otherproject", "api"]`)

**Search:** `query="authentication"` + source filter by tag `"netzwaechter"`  
**Result:** Only Netzwächter auth content

#### Advantages
- ✅ Clear project boundaries
- ✅ Smaller search spaces
- ✅ Easy to delete project knowledge

#### Disadvantages
- ❌ Duplication (React docs for each React project?)
- ❌ More maintenance
- ❌ Harder to share patterns across projects

### Pattern 3: Minimal High-Level (Not Recommended)

#### How It Works
- Only store high-level architecture and patterns
- Rely on external docs via URLs
- Minimal storage

#### Why Not Recommended
- ❌ Defeats the purpose of RAG
- ❌ Can't search external docs
- ❌ No code example extraction
- ❌ Slower AI responses (needs to fetch external)

## Best Practice for Multiple Projects

Based on your situation (multiple projects in `/Users/janschubert/code-projects`):

### Recommended Strategy

#### Shared Knowledge (stored once, used everywhere)

**Global Sources:**
```
├── React Documentation (all React projects use)
├── Express Documentation (all Express projects use)
├── TypeScript Handbook (all TS projects use)
├── Drizzle ORM Docs (all Drizzle projects use)
├── TanStack Query Docs (all React projects use)
└── Radix UI Docs (all Radix projects use)
```

**Tags:** `["shared", "dependency", "framework-name"]`

#### Project-Specific Knowledge

**Netzwächter Sources:**
```
├── SYSTEM-ARCHITEKTUR.md (tags: ["netzwaechter", "architecture"])
├── Coding Standards (tags: ["netzwaechter", "standards"])
├── API Documentation (tags: ["netzwaechter", "api"])
└── Legacy Patterns (tags: ["netzwaechter", "legacy", "avoid"])
```

**Other Project Sources:**
```
├── ProjectX Architecture (tags: ["projectx", "architecture"])
└── ...
```

## Practical Example

Let's say you're working on Netzwächter and another project:

### Step 1: Start Archon
```bash
archon start
```

### Step 2: Upload Shared Dependencies (do this once)
```bash
curl -X POST http://localhost:8181/api/knowledge-items/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://react.dev/reference/react",
    "knowledge_type": "dependency",
    "tags": ["shared", "react", "ui"]
  }'
```

### Step 3: Upload Netzwächter-Specific Docs
```bash
curl -X POST http://localhost:8181/api/documents/upload \
  -F "file=@/Users/janschubert/code-projects/monitoring_firma/netzwaechter-refactored/docs/02-architektur/SYSTEM-ARCHITEKTUR.md" \
  -F "knowledge_type=documentation" \
  -F 'tags=["netzwaechter", "architecture"]'
```

### Step 4: Create Project and Link Sources
1. Create Netzwächter project in Archon UI
2. Link relevant sources (both shared and project-specific)

### Step 5: Working on Netzwächter
```bash
cd ~/code-projects/monitoring_firma/netzwaechter-refactored
```

**AI Search Flow:**
- Claude Code with MCP searches knowledge base
- Finds both React docs (shared) and Netzwächter docs (project-specific)
- **AI Query:** "Search knowledge base for React hooks patterns"
- **Returns:** React docs + any Netzwächter-specific React patterns

### Step 6: Working on Another Project
```bash
cd ~/code-projects/other-project
```

**Benefits:**
- Same React docs available
- Different project-specific docs

## Organization Strategy

### Using `knowledge_type` (Archon's Built-in Field)

**Available types (based on code):**
- `"technical"` - Technical documentation
- `"documentation"` - General docs
- `"dependency"` - External library docs
- `"standards"` - Coding standards
- `"architecture"` - Architectural decisions
- `"legacy"` - Deprecated patterns (to avoid)

### Using Tags (Flexible Categorization)

**Recommended tagging scheme:**

```javascript
// Project identification
["netzwaechter", "projectx", "shared"]

// Category
["architecture", "api", "frontend", "backend", "testing"]

// Technology
["react", "express", "drizzle", "typescript"]

// Purpose
["patterns", "examples", "standards", "legacy"]

// Module (for large projects)
["auth", "monitoring", "reports", "users"]
```

**Example:**
```json
{
  "url": "file://Netzwächter-Auth-Patterns.md",
  "knowledge_type": "standards",
  "tags": ["netzwaechter", "auth", "patterns", "express"]
}
```

## Search Behavior

### When You Search via MCP

**Search everything:**
```javascript
archon:rag_search_knowledge_base({
  query: "authentication middleware"
})
// Returns: All sources with relevant content
```

**Filter by source:**
```javascript
archon:rag_search_knowledge_base({
  query: "authentication middleware",
  source_id: "src_netzwaechter_standards"
})
// Returns: Only from that specific source
```

**Filter by tags (via source metadata):**
- Not directly supported in MCP, but can be done via project linking

## My Recommendation for You

Given your setup with Netzwächter and potentially other projects:

### Level 1: Shared Dependencies (Store once, use everywhere)
- React, Express, Drizzle, TanStack Query, Radix UI docs
- **Tags:** `["shared", "dependency"]`

### Level 2: Project Documentation (Per-project)
- Netzwächter: All 222 .md files
- **Tags:** `["netzwaechter", "documentation"]`
- Link to "Netzwächter Refactor" project

### Level 3: Project Standards (Per-project, critical for AI)
- Netzwächter Coding Standards
- Netzwächter Architectural Patterns
- Legacy Patterns to Avoid
- **Tags:** `["netzwaechter", "standards", "critical"]`
- Link to "Netzwächter Refactor" project

### Level 4: Code Examples (Extracted automatically)
- Auto-extracted from uploaded docs
- Searchable via `rag_search_code_examples`

## Summary

This approach gives you:

- ✅ **One centralized knowledge base**
- ✅ **Project-specific filtering via linking**
- ✅ **Shared knowledge reuse**
- ✅ **Clear organization via tags**
- ✅ **Efficient search** (Archon finds relevant content across all)

The AI will search everything but be smart about relevance based on your query and linked sources.
