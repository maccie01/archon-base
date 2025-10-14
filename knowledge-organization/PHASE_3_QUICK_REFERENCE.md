# Phase 3 MCP Tools - Quick Reference

**Status**: Complete | **Date**: October 14, 2025

---

## Tool Summary

| Tool | Type | Purpose | Key Parameters |
|------|------|---------|----------------|
| `rag_get_available_sources` | Enhanced | List sources with scope filter | `scope`, `project_id` |
| `rag_search_knowledge_base` | Enhanced | Search with scope control | `query`, `scope`, `project_id` |
| `rag_search_project_knowledge` | New | Project-scoped search | `query`, `project_id`, `folder_name` |
| `rag_search_global_knowledge` | New | Global search with tags | `query`, `tags` |
| `rag_list_project_folders` | New | List project folders | `project_id` |

---

## Quick Usage Examples

### List Sources
```python
# All sources
rag_get_available_sources()

# Global only
rag_get_available_sources(scope="global")

# Project-specific
rag_get_available_sources(scope="project", project_id="proj_123")
```

### Search Knowledge
```python
# Search all knowledge
rag_search_knowledge_base("React hooks")

# Search global only
rag_search_knowledge_base("React hooks", scope="global")

# Search project
rag_search_knowledge_base("auth flow", scope="project", project_id="proj_123")
```

### Project Search (Convenience)
```python
# All project knowledge
rag_search_project_knowledge("database schema", "proj_123")

# Specific folder
rag_search_project_knowledge("login endpoint", "proj_123", folder_name="API")
```

### Global Search (Convenience)
```python
# All global
rag_search_global_knowledge("REST API design")

# With tags
rag_search_global_knowledge("authentication", tags=["security", "fastapi"])
```

### Folder Discovery
```python
# List folders
rag_list_project_folders("proj_123")
```

---

## Agent Decision Pattern

```
Need knowledge?
  ├─ On specific project?
  │   ├─ YES → rag_search_project_knowledge(query, project_id)
  │   │   └─ No results? → rag_search_global_knowledge(query)
  │   └─ NO → rag_search_global_knowledge(query)
  │
  └─ Framework/general? → rag_search_global_knowledge(query, tags)
```

---

## Response Format

All tools return JSON strings with consistent structure:

```json
{
  "success": true,
  "results": [...],
  "error": null,
  "...": "context-specific fields"
}
```

---

## Tag Categories

**Common Tags**:
- Framework: `react`, `nextjs`, `fastapi`, `django`
- Language: `python`, `typescript`, `javascript`, `rust`
- Security: `authentication`, `authorization`, `encryption`
- Architecture: `microservices`, `rest-api`, `graphql`
- Database: `postgresql`, `mongodb`, `redis`, `vector-search`
- Testing: `unit-testing`, `integration-testing`, `e2e-testing`
- Deployment: `docker`, `kubernetes`, `ci-cd`
- Documentation: `api-reference`, `tutorial`, `troubleshooting`

See full list: [PHASE_3_MCP_TOOLS_DOCUMENTATION.md](./PHASE_3_MCP_TOOLS_DOCUMENTATION.md)

---

## Files Modified

- `/Users/janschubert/tools/archon/python/src/mcp_server/features/rag/rag_tools.py`
  - Before: 362 lines
  - After: 703 lines
  - Added: ~340 lines (2 enhancements + 3 new tools)

---

## Documentation

- [PHASE_3_MCP_TOOLS_DOCUMENTATION.md](./PHASE_3_MCP_TOOLS_DOCUMENTATION.md) - Full tool documentation with examples
- [PHASE_3_IMPLEMENTATION_REPORT.md](./PHASE_3_IMPLEMENTATION_REPORT.md) - Implementation details and decisions
- [PHASE_3_QUICK_REFERENCE.md](./PHASE_3_QUICK_REFERENCE.md) - This file (quick reference)

---

## Next Phase

**Phase 4: API Route Implementation**
- Update RAG endpoints with scope/project_id/folder_name/tags
- Create folder listing endpoint
- Update crawl/upload endpoints with scope parameters

---

## Testing Status

- [ ] Unit tests for scope filtering
- [ ] Integration tests for HTTP communication
- [ ] Agent workflow simulation tests
- [ ] Backward compatibility verification

---

**Ready for**: API Route Implementation (Phase 4)
