# Archon Knowledge Base Integration Plan

Created: 2025-10-13

## Executive Summary

After analyzing the Archon how-to guide and reviewing what the 6 agents created, here's the assessment:

**Current Status**: The agents created excellent PROJECT-SPECIFIC documentation (42 files, 656 KB)

**What's Missing**: GLOBAL SHARED knowledge (framework documentation that can be reused across projects)

**Recommendation**: Use Archon's recommended 2-level approach:
1. Level 1: Global shared dependencies (store once, use everywhere)
2. Level 2: Project-specific documentation (what we have now)

---

## Analysis of Current Knowledge Base

### What We Have (Project-Specific)

The 6 agents created comprehensive Netzwächter-specific documentation:

**Coverage: EXCELLENT**
- Database schemas (PostgreSQL/Drizzle specific to Netzwächter)
- API endpoints (120+ Netzwächter endpoints)
- Authentication (Netzwächter's session-based auth)
- Frontend patterns (Netzwächter UI components and inconsistencies)
- Backend architecture (Netzwächter's 23 modules)
- Configuration (Netzwächter's environment and setup)

**Quality: EXCELLENT**
- Well-organized, concise, properly structured
- Accurate (verified against actual code)
- Cross-referenced
- Ready for RAG ingestion

**Archon Classification:**
- `knowledge_type`: "documentation"
- `tags`: ["netzwaechter", "project-specific", "architecture", "api", "database", etc.]

### What We're Missing (Global Shared)

According to Archon best practices, we should also have GLOBAL SHARED knowledge that benefits ALL projects using these technologies:

**Missing Level 1: Framework Documentation**
1. React documentation (for all React projects)
2. Express documentation (for all Express projects)
3. TypeScript handbook (for all TypeScript projects)
4. Drizzle ORM docs (for all Drizzle projects)
5. TanStack Query docs (for all React Query projects)
6. Radix UI docs (for all Radix projects)
7. Tailwind CSS docs (for all Tailwind projects)
8. Vitest docs (for all Vitest projects)
9. PostgreSQL docs (for all PostgreSQL projects)

**Why Missing?**
- The agents focused on Netzwächter-specific implementation
- They documented HOW Netzwächter uses these frameworks
- They didn't include the framework documentation itself

**Why It Matters:**
- Archon's RAG needs base framework knowledge to understand project-specific code
- Prevents duplication across multiple projects
- AI gets better context for suggestions (knows both framework patterns AND project patterns)

---

## Recommended Approach

### Two-Level Knowledge Base Structure

#### Level 1: Global Shared Knowledge (Store Once, Use Everywhere)

**Upload to Archon with:**
- `knowledge_type`: "dependency"
- `tags`: ["shared", "framework-name"]
- No project linking initially

**Sources to Add:**

1. **React Documentation**
   - URL: https://react.dev/reference/react
   - Coverage: Hooks, components, APIs
   - Size: ~500-1000 pages (Archon will crawl and chunk)
   - Tags: ["shared", "react", "frontend", "ui"]

2. **Express Documentation**
   - URL: https://expressjs.com/en/5x/api.html
   - Coverage: Routing, middleware, request/response
   - Tags: ["shared", "express", "backend", "nodejs"]

3. **TypeScript Handbook**
   - URL: https://www.typescriptlang.org/docs/handbook/
   - Coverage: Types, interfaces, generics
   - Tags: ["shared", "typescript", "language"]

4. **Drizzle ORM Documentation**
   - URL: https://orm.drizzle.team/docs/overview
   - Coverage: Schema, queries, migrations
   - Tags: ["shared", "drizzle", "database", "orm"]

5. **TanStack Query Documentation**
   - URL: https://tanstack.com/query/latest/docs/framework/react/overview
   - Coverage: Data fetching, caching, mutations
   - Tags: ["shared", "tanstack-query", "react-query", "data-fetching"]

6. **Radix UI Documentation**
   - URL: https://www.radix-ui.com/primitives/docs/overview/introduction
   - Coverage: Accessible components, primitives
   - Tags: ["shared", "radix-ui", "ui", "components", "accessibility"]

7. **Tailwind CSS Documentation**
   - URL: https://tailwindcss.com/docs
   - Coverage: Utility classes, configuration, customization
   - Tags: ["shared", "tailwind", "css", "styling"]

8. **Vitest Documentation**
   - URL: https://vitest.dev/guide/
   - Coverage: Testing, mocking, coverage
   - Tags: ["shared", "vitest", "testing"]

9. **PostgreSQL Documentation**
   - URL: https://www.postgresql.org/docs/16/index.html
   - Coverage: SQL, indexes, performance
   - Tags: ["shared", "postgresql", "database"]

**Total Estimated Size**: 3,000-5,000 pages (Archon handles chunking automatically)

#### Level 2: Project-Specific Knowledge (What We Already Have)

**Upload to Archon with:**
- `knowledge_type`: "documentation"
- `tags`: ["netzwaechter", "project-specific"]
- Link to "Netzwächter Refactor" project

**What to Upload:**
- All 42 markdown files in `.archon-knowledge-base/`
- Additional: All 222 existing docs in `docs/` directory (if needed)

**Organization:**

1. **Database Documentation** (5 files)
   - Tags: ["netzwaechter", "database", "schema", "postgresql", "drizzle"]

2. **API Documentation** (6 files)
   - Tags: ["netzwaechter", "api", "endpoints", "express", "backend"]

3. **Authentication Documentation** (5 files)
   - Tags: ["netzwaechter", "auth", "security", "session"]

4. **Frontend Documentation** (8 files)
   - Tags: ["netzwaechter", "frontend", "ui", "react", "components"]

5. **Backend Documentation** (8 files)
   - Tags: ["netzwaechter", "backend", "architecture", "patterns", "modules"]

6. **Configuration Documentation** (8 files)
   - Tags: ["netzwaechter", "configuration", "environment", "deployment"]

7. **Dead Code Analysis** (8 files in `.dead-code-analysis-reports/`)
   - Tags: ["netzwaechter", "technical-debt", "cleanup", "refactoring"]

#### Level 3: Project Standards (CRITICAL - Not Yet Created)

**What's Missing: Coding Standards & Patterns**

According to Archon best practices, we need explicit standards documentation:

**Files to Create:**

1. **CODING_STANDARDS.md**
   - TypeScript style guide
   - Naming conventions
   - File organization rules
   - Comment standards

2. **BACKEND_PATTERNS.md**
   - 4-layer pattern (Routes → Controller → Service → Repository)
   - Error handling patterns
   - Validation patterns
   - Database access patterns

3. **FRONTEND_PATTERNS.md**
   - Component composition patterns
   - TanStack Query usage patterns
   - Form handling patterns
   - State management patterns

4. **TESTING_PATTERNS.md**
   - Unit test patterns
   - Integration test patterns
   - E2E test patterns
   - Mock patterns

5. **SECURITY_PATTERNS.md**
   - Authentication patterns
   - Authorization patterns
   - Input validation patterns
   - Error handling patterns

6. **LEGACY_PATTERNS_TO_AVOID.md** (CRITICAL FOR AI)
   - Old API client patterns (don't use)
   - Deprecated auth patterns
   - Old form patterns
   - Duplicate implementations to avoid

**Upload with:**
- `knowledge_type`: "standards"
- `tags`: ["netzwaechter", "standards", "critical", "patterns"]
- Link to "Netzwächter Refactor" project

**Why Critical:**
- AI needs to know WHICH patterns to follow vs avoid
- Prevents AI from suggesting deprecated patterns
- Guides AI to use correct 4-layer pattern

---

## Implementation Plan

### Phase 1: Upload Global Shared Knowledge (1-2 hours)

**Step 1.1: Start Archon**
```bash
cd /path/to/archon
archon start
```

**Step 1.2: Upload React Documentation**
```bash
curl -X POST http://localhost:8181/api/knowledge-items/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://react.dev/reference/react",
    "knowledge_type": "dependency",
    "tags": ["shared", "react", "frontend", "ui"]
  }'
```

**Step 1.3: Upload Express Documentation**
```bash
curl -X POST http://localhost:8181/api/knowledge-items/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://expressjs.com/en/5x/api.html",
    "knowledge_type": "dependency",
    "tags": ["shared", "express", "backend", "nodejs"]
  }'
```

**Step 1.4: Upload TypeScript Documentation**
```bash
curl -X POST http://localhost:8181/api/knowledge-items/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.typescriptlang.org/docs/handbook/",
    "knowledge_type": "dependency",
    "tags": ["shared", "typescript", "language"]
  }'
```

**Step 1.5: Upload Drizzle ORM Documentation**
```bash
curl -X POST http://localhost:8181/api/knowledge-items/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://orm.drizzle.team/docs/overview",
    "knowledge_type": "dependency",
    "tags": ["shared", "drizzle", "database", "orm"]
  }'
```

**Step 1.6: Upload TanStack Query Documentation**
```bash
curl -X POST http://localhost:8181/api/knowledge-items/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://tanstack.com/query/latest/docs/framework/react/overview",
    "knowledge_type": "dependency",
    "tags": ["shared", "tanstack-query", "react-query", "data-fetching"]
  }'
```

**Step 1.7: Upload Radix UI Documentation**
```bash
curl -X POST http://localhost:8181/api/knowledge-items/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.radix-ui.com/primitives/docs/overview/introduction",
    "knowledge_type": "dependency",
    "tags": ["shared", "radix-ui", "ui", "components", "accessibility"]
  }'
```

**Step 1.8: Upload Tailwind CSS Documentation**
```bash
curl -X POST http://localhost:8181/api/knowledge-items/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://tailwindcss.com/docs",
    "knowledge_type": "dependency",
    "tags": ["shared", "tailwind", "css", "styling"]
  }'
```

**Step 1.9: Upload Vitest Documentation**
```bash
curl -X POST http://localhost:8181/api/knowledge-items/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://vitest.dev/guide/",
    "knowledge_type": "dependency",
    "tags": ["shared", "vitest", "testing"]
  }'
```

**Step 1.10: Upload PostgreSQL Documentation**
```bash
curl -X POST http://localhost:8181/api/knowledge-items/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.postgresql.org/docs/16/index.html",
    "knowledge_type": "dependency",
    "tags": ["shared", "postgresql", "database"]
  }'
```

**Estimated Time**: 1-2 hours (Archon crawls and processes in background)

### Phase 2: Create Project Standards Documentation (2-3 hours)

**Step 2.1: Create Standards Directory**
```bash
mkdir -p .archon-knowledge-base/07-standards/
```

**Step 2.2: Create CODING_STANDARDS.md**
- Extract naming conventions from existing code
- Document TypeScript style preferences
- File organization rules
- Comment standards

**Step 2.3: Create BACKEND_PATTERNS.md**
- Document 4-layer pattern (use settings module as reference)
- Error handling patterns (AppError, asyncHandler)
- Validation patterns (Zod schemas)
- Database access patterns (Drizzle + repositories)

**Step 2.4: Create FRONTEND_PATTERNS.md**
- Component composition patterns
- TanStack Query patterns (from hooks analysis)
- Form handling patterns (React Hook Form)
- State management patterns

**Step 2.5: Create TESTING_PATTERNS.md**
- Unit test patterns (from existing tests)
- Integration test patterns
- E2E test patterns (Playwright)
- Mock patterns

**Step 2.6: Create SECURITY_PATTERNS.md**
- Authentication flow (from auth docs)
- Authorization checks (requireAuth, requireRole)
- Input validation (Zod)
- Error sanitization

**Step 2.7: Create LEGACY_PATTERNS_TO_AVOID.md**
- Old API clients (apiClient.ts, api-utils.ts - DEPRECATED)
- Direct fetch calls (use TanStack Query instead)
- Old form patterns (document deprecated approaches)
- Duplicate implementations to avoid

**Estimated Time**: 2-3 hours

### Phase 3: Upload Project-Specific Documentation (30 minutes)

**Option A: Upload Individual Files (Recommended)**

Create upload script:
```bash
#!/bin/bash
# upload-to-archon.sh

BASE_DIR="/Users/janschubert/code-projects/monitoring_firma/netzwaechter-refactored/.archon-knowledge-base"

# Upload database docs
for file in "$BASE_DIR/01-database"/*.md; do
  curl -X POST http://localhost:8181/api/documents/upload \
    -F "file=@$file" \
    -F "knowledge_type=documentation" \
    -F 'tags=["netzwaechter", "database", "schema"]'
done

# Upload API docs
for file in "$BASE_DIR/02-api-endpoints"/*.md; do
  curl -X POST http://localhost:8181/api/documents/upload \
    -F "file=@$file" \
    -F "knowledge_type=documentation" \
    -F 'tags=["netzwaechter", "api", "endpoints"]'
done

# Upload auth docs
for file in "$BASE_DIR/03-authentication"/*.md; do
  curl -X POST http://localhost:8181/api/documents/upload \
    -F "file=@$file" \
    -F "knowledge_type=documentation" \
    -F 'tags=["netzwaechter", "auth", "security"]'
done

# Upload frontend docs
for file in "$BASE_DIR/04-frontend"/*.md; do
  curl -X POST http://localhost:8181/api/documents/upload \
    -F "file=@$file" \
    -F "knowledge_type=documentation" \
    -F 'tags=["netzwaechter", "frontend", "ui", "react"]'
done

# Upload backend docs
for file in "$BASE_DIR/05-backend"/*.md; do
  curl -X POST http://localhost:8181/api/documents/upload \
    -F "file=@$file" \
    -F "knowledge_type=documentation" \
    -F 'tags=["netzwaechter", "backend", "architecture"]'
done

# Upload config docs
for file in "$BASE_DIR/06-configuration"/*.md; do
  curl -X POST http://localhost:8181/api/documents/upload \
    -F "file=@$file" \
    -F "knowledge_type=documentation" \
    -F 'tags=["netzwaechter", "configuration", "deployment"]'
done

# Upload standards docs (CRITICAL)
for file in "$BASE_DIR/07-standards"/*.md; do
  curl -X POST http://localhost:8181/api/documents/upload \
    -F "file=@$file" \
    -F "knowledge_type=standards" \
    -F 'tags=["netzwaechter", "standards", "critical"]'
done
```

**Estimated Time**: 30 minutes

**Option B: Bulk Upload via Directory**
If Archon supports directory upload, use that instead.

### Phase 4: Create Archon Project and Link Sources (15 minutes)

**Step 4.1: Create Project in Archon UI**
```
Project Name: Netzwächter Refactor
Description: Energy monitoring system refactoring and cleanup
GitHub Repo: (optional)
```

**Step 4.2: Link Global Shared Sources**
In Archon UI, link these sources to the project:
- React Documentation
- Express Documentation
- TypeScript Handbook
- Drizzle ORM Documentation
- TanStack Query Documentation
- Radix UI Documentation
- Tailwind CSS Documentation
- Vitest Documentation
- PostgreSQL Documentation

**Step 4.3: Link Project-Specific Sources**
Archon should auto-link based on tags, but verify:
- All database documentation
- All API documentation
- All authentication documentation
- All frontend documentation
- All backend documentation
- All configuration documentation
- All standards documentation (CRITICAL)

**Estimated Time**: 15 minutes

### Phase 5: Test RAG Search (15 minutes)

**Test Queries via MCP:**

```javascript
// Test 1: Framework knowledge (should return React docs + Netzwächter usage)
archon:rag_search_knowledge_base({
  query: "React hooks useEffect cleanup pattern"
})

// Test 2: Project-specific (should return Netzwächter API docs)
archon:rag_search_knowledge_base({
  query: "authentication middleware implementation"
})

// Test 3: Standards (CRITICAL - should return Netzwächter patterns)
archon:rag_search_knowledge_base({
  query: "backend controller service repository pattern"
})

// Test 4: What to avoid (should return legacy patterns doc)
archon:rag_search_knowledge_base({
  query: "deprecated API client patterns"
})

// Test 5: Code examples
archon:rag_search_code_examples({
  query: "TanStack Query mutation example"
})
```

**Expected Results:**
- Queries should return mix of framework knowledge + project-specific implementation
- AI should prefer project-specific patterns when available
- Legacy patterns should be clearly marked as "avoid"

**Estimated Time**: 15 minutes

---

## Total Implementation Timeline

| Phase | Task | Time | Status |
|-------|------|------|--------|
| **Phase 1** | Upload global shared knowledge | 1-2 hours | Pending |
| **Phase 2** | Create project standards docs | 2-3 hours | Pending |
| **Phase 3** | Upload project-specific docs | 30 min | Pending |
| **Phase 4** | Create project & link sources | 15 min | Pending |
| **Phase 5** | Test RAG search | 15 min | Pending |
| **TOTAL** | **Complete Archon setup** | **4-6 hours** | **Pending** |

---

## What Agents Created vs What's Needed

### ✅ Already Created (Excellent Quality)

1. **Database Documentation** - Complete, ready to upload
2. **API Documentation** - Complete, ready to upload
3. **Authentication Documentation** - Complete, ready to upload
4. **Frontend Documentation** - Complete, ready to upload
5. **Backend Documentation** - Complete, ready to upload
6. **Configuration Documentation** - Complete, ready to upload
7. **Master Index** - Complete, helpful for navigation

**Status**: 42 files, 656 KB, 100% project-specific coverage

### ❌ Missing (Need to Create)

1. **Global Shared Framework Docs** - Not created (need to crawl)
2. **Project Standards Documentation** - Not created (critical for AI)
3. **Legacy Patterns to Avoid** - Not documented (AI will suggest wrong patterns)
4. **Upload Scripts** - Not created (need automation)

**Status**: 0% global knowledge, 0% standards documentation

### ⚠️ Partially Missing (Consider Adding)

1. **Existing Project Docs** - 222 .md files in `docs/` directory
   - May contain additional context
   - Consider uploading if agents' docs don't cover everything

2. **Dead Code Analysis Reports** - 8 files in `.dead-code-analysis-reports/`
   - Helpful for understanding technical debt
   - Should upload with tags ["netzwaechter", "technical-debt", "cleanup"]

---

## Recommendations

### Priority 1: CRITICAL (Do This Week)

**1. Create Standards Documentation (Phase 2)**
- Without this, AI will suggest incorrect patterns
- AI needs to know 4-layer pattern is the standard
- AI needs to know old API clients are deprecated
- AI needs explicit guidance on what to avoid

**Recommended Action**: Create 6 standards files (2-3 hours)

**2. Upload Global Framework Docs (Phase 1)**
- AI needs framework knowledge to understand project code
- Reusable across future projects
- Significantly improves AI suggestions

**Recommended Action**: Upload 9 framework documentation sites (1-2 hours)

### Priority 2: HIGH (Do This Week)

**3. Upload Project-Specific Docs (Phase 3)**
- We already have excellent documentation
- Just needs to be uploaded to Archon
- Quick win

**Recommended Action**: Run upload script (30 minutes)

**4. Create and Link Project (Phase 4)**
- Connects everything together
- Enables project-specific RAG

**Recommended Action**: Setup in Archon UI (15 minutes)

### Priority 3: MEDIUM (Do Within 2 Weeks)

**5. Upload Dead Code Analysis Reports**
- Helpful for understanding technical debt
- Guides refactoring decisions

**Recommended Action**: Add to upload script (10 minutes)

**6. Consider Uploading Existing Docs**
- 222 .md files in `docs/` directory
- May have additional context
- Review for gaps first

**Recommended Action**: Review and selectively upload (1-2 hours)

---

## Success Metrics

After complete Archon setup, you should be able to:

**1. Ask Framework Questions**
- "How do I use useEffect cleanup in React?"
- AI returns: React docs + Netzwächter hook examples

**2. Ask Project Questions**
- "How do I add a new API endpoint?"
- AI returns: Netzwächter backend pattern + example from settings module

**3. Ask Standards Questions**
- "What pattern should I use for backend services?"
- AI returns: 4-layer pattern from standards doc + settings module example

**4. Avoid Legacy Patterns**
- "How do I make API calls?"
- AI returns: TanStack Query pattern (correct) + warning about deprecated apiClient.ts

**5. Get Code Examples**
- "Show me TanStack Query mutation example"
- AI returns: Extracted code from both React Query docs + Netzwächter hooks

---

## Next Steps

**Immediate (Today):**
1. Review this plan
2. Decide priority order

**This Week:**
1. Create standards documentation (Phase 2)
2. Upload global framework docs (Phase 1)
3. Upload project-specific docs (Phase 3)
4. Setup Archon project (Phase 4)
5. Test RAG search (Phase 5)

**Next Week:**
1. Upload dead code analysis
2. Review and upload existing docs if needed
3. Start using Archon with Claude Code + MCP

---

## Conclusion

**What Agents Did**: Created excellent PROJECT-SPECIFIC documentation (42 files, ready to use)

**What's Missing**:
1. GLOBAL SHARED framework documentation (need to crawl)
2. PROJECT STANDARDS documentation (need to create)
3. Upload automation (need scripts)

**Recommendation**: Follow the 5-phase plan above (4-6 hours total)

**Result**: Complete Archon knowledge base that combines:
- Framework knowledge (React, Express, etc.)
- Project-specific implementation (what agents created)
- Explicit standards (what patterns to use/avoid)

This gives AI the best possible context for helping with Netzwächter development and refactoring.

---

**Plan Created**: 2025-10-13
**Estimated Completion**: 4-6 hours
**Status**: Ready to implement
