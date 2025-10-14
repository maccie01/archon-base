# Project Standards - Netzwächter

Created: 2025-10-13

This directory contains **REQUIRED** coding standards, patterns, and best practices for the Netzwächter project.

---

## Purpose

These standards ensure:
- **Consistency** across the codebase
- **Security** in all implementations
- **Quality** in code and tests
- **AI Guidance** - AI agents reference these to suggest correct patterns

---

## Documents Overview

### 1. LEGACY_PATTERNS_TO_AVOID.md ⚠️ CRITICAL

**Purpose**: Lists DEPRECATED patterns that exist in the codebase but should NEVER be used in new code.

**When to use**: When AI suggests old patterns, reject them and request modern alternatives.

**Priority**: P0 - Read first before any development

**Key content**:
- Old API clients (apiClient.ts) → Use TanStack Query
- Raw SQL → Use Drizzle ORM
- Manual forms → Use React Hook Form + Zod
- Direct database access in controllers → Use 4-layer pattern
- Unprotected routes → Use requireAuth middleware

---

### 2. BACKEND_PATTERNS.md 🏗️ REQUIRED

**Purpose**: Defines the 4-layer backend architecture pattern.

**When to use**: When creating/modifying any backend module.

**Priority**: P0 - All backend code MUST follow this

**Key content**:
- **4-Layer Pattern**: Routes → Controller → Service → Repository
- Error handling with AppError + asyncHandler
- Validation with Zod schemas
- Authentication/authorization middleware
- Module file structure

**Example structure**:
```
Routes (HTTP only) → Controller (Extract req/res) → Service (Business logic) → Repository (DB only)
```

---

### 3. FRONTEND_PATTERNS.md 🎨 REQUIRED

**Purpose**: Defines frontend development patterns.

**When to use**: When creating/modifying any React component or frontend logic.

**Priority**: P0 - All frontend code MUST follow this

**Key content**:
- Data fetching with TanStack Query (queries + mutations)
- Form handling with React Hook Form + Zod
- State management decision tree (TanStack Query vs Zustand vs Context vs useState)
- Component composition patterns
- Custom hooks patterns
- Styling with Tailwind CSS

**Decision trees**:
- Server state → TanStack Query
- Complex client state → Zustand
- Simple local state → useState
- Shared context → React Context

---

### 4. TESTING_PATTERNS.md 🧪 REQUIRED

**Purpose**: Defines testing strategy and patterns.

**When to use**: When writing any test.

**Priority**: P0 - All new code MUST have tests

**Key content**:
- Testing pyramid (60% unit, 30% integration, 10% E2E)
- Unit tests with Vitest (services, repositories, hooks)
- Integration tests with Supertest (API endpoints)
- E2E tests with Playwright (user flows)
- Component tests with React Testing Library
- Test coverage goals (80%+ for business logic)

**Test structure**:
```typescript
describe('Feature', () => {
  beforeEach(() => { /* setup */ })
  afterEach(() => { /* cleanup */ })

  it('should handle happy path', () => { /* test */ })
  it('should handle error case', () => { /* test */ })
})
```

---

### 5. SECURITY_PATTERNS.md 🔒 CRITICAL

**Purpose**: Defines non-negotiable security requirements.

**When to use**: For ALL code (security is always relevant).

**Priority**: P0 - Security is non-negotiable

**Key content**:
- Authentication with session-based auth
- Password hashing with Argon2id
- Authorization with requireAuth/requireRole middleware
- Multi-tenancy isolation (mandantId checks)
- Input validation with Zod
- SQL injection prevention (Drizzle ORM only)
- XSS prevention (React auto-escaping, DOMPurify)
- CSRF protection (SameSite cookies)
- Secrets management (environment variables)
- Rate limiting (brute force protection)
- Error handling (never leak sensitive info)

**Security checklist**: Use before every deployment

---

### 6. CODING_STANDARDS.md 📝 REQUIRED

**Purpose**: Defines coding style, naming conventions, and best practices.

**When to use**: For ALL code.

**Priority**: P1 - Consistency and readability

**Key content**:
- TypeScript strict mode configuration
- Naming conventions (camelCase, PascalCase, kebab-case)
- File organization (import order, export order)
- Function best practices (< 50 lines, single responsibility)
- Error handling patterns
- Comments and documentation (when and what to comment)
- Code style (const vs let, arrow functions, destructuring)
- React/JSX standards
- Git commit message format

**Naming conventions**:
- Variables: camelCase (`userName`)
- Functions: camelCase (`getUserById`)
- Classes: PascalCase (`UserService`)
- Files: kebab-case (`user-service.ts`)
- Components: PascalCase (`UserProfile.tsx`)

---

## Priority Guide

### P0 - Critical (Must Follow)

1. **LEGACY_PATTERNS_TO_AVOID.md** - Never use deprecated patterns
2. **BACKEND_PATTERNS.md** - All backend code follows 4-layer pattern
3. **FRONTEND_PATTERNS.md** - All frontend code follows TanStack Query + React Hook Form
4. **TESTING_PATTERNS.md** - All code has tests (80%+ coverage for business logic)
5. **SECURITY_PATTERNS.md** - Security requirements are non-negotiable

### P1 - High Priority (Should Follow)

6. **CODING_STANDARDS.md** - Code style and naming conventions

---

## How to Use These Documents

### For Developers

**Before writing code:**
1. Check **LEGACY_PATTERNS_TO_AVOID.md** - Don't repeat deprecated patterns
2. Check **BACKEND_PATTERNS.md** or **FRONTEND_PATTERNS.md** - Follow required patterns
3. Check **SECURITY_PATTERNS.md** - Ensure security requirements are met

**While writing code:**
1. Follow **CODING_STANDARDS.md** - Naming, style, comments
2. Reference **TESTING_PATTERNS.md** - Write tests alongside code

**Before committing:**
1. Run tests (must pass)
2. Review security checklist in **SECURITY_PATTERNS.md**
3. Check code style in **CODING_STANDARDS.md**

### For AI Agents

**When suggesting code:**
1. **ALWAYS check LEGACY_PATTERNS_TO_AVOID.md** - Never suggest deprecated patterns
2. **ALWAYS follow BACKEND_PATTERNS.md** for backend code
3. **ALWAYS follow FRONTEND_PATTERNS.md** for frontend code
4. **ALWAYS include security patterns** from SECURITY_PATTERNS.md
5. Follow coding style from **CODING_STANDARDS.md**

**When user asks for patterns:**
1. Search these documents
2. Reference specific sections
3. Provide examples from the documents

### For Code Review

**Checklist:**
- [ ] No legacy patterns used (check LEGACY_PATTERNS_TO_AVOID.md)
- [ ] Backend follows 4-layer pattern (check BACKEND_PATTERNS.md)
- [ ] Frontend uses TanStack Query + React Hook Form (check FRONTEND_PATTERNS.md)
- [ ] Tests written and passing (check TESTING_PATTERNS.md)
- [ ] Security requirements met (check SECURITY_PATTERNS.md)
- [ ] Code style consistent (check CODING_STANDARDS.md)

---

## Quick Decision Trees

### Backend: Which layer does this code belong in?

```
Is it HTTP routing?
├─ YES → Routes layer
└─ NO → Is it extracting req/res data?
    ├─ YES → Controller layer
    └─ NO → Is it business logic?
        ├─ YES → Service layer
        └─ NO → Is it database access?
            ├─ YES → Repository layer
            └─ NO → Utility function
```

### Frontend: How should I fetch data?

```
Is it server data (from API)?
├─ YES → TanStack Query
│   ├─ Read (GET) → useQuery
│   └─ Write (POST/PUT/DELETE) → useMutation
└─ NO → Is it complex client state?
    ├─ YES → Zustand store
    └─ NO → Is it simple local state?
        ├─ YES → useState
        └─ NO → Is it shared context?
            ├─ YES → React Context
            └─ NO → URL params
```

### Testing: What type of test should I write?

```
What am I testing?
├─ Business logic in service → Unit test (Vitest + mocks)
├─ Database queries → Integration test (Vitest + real DB)
├─ API endpoint → Integration test (Supertest)
├─ Component rendering → Component test (React Testing Library)
└─ User flow (login → create → delete) → E2E test (Playwright)
```

---

## Integration with Archon

These standards are uploaded to Archon knowledge base with tags:
- `["netzwaechter", "standards", "critical", "must-follow"]`

**AI agents search these documents when:**
- Planning new features
- Reviewing code
- Suggesting patterns
- Creating modules

**Result**: AI suggestions are consistent with project standards.

---

## Maintenance

### When to Update

**Update these documents when:**
- Technology stack changes (e.g., migrate to different ORM)
- New patterns are adopted (e.g., new state management library)
- Security requirements change (e.g., new OWASP Top 10)
- Common mistakes are identified (add to LEGACY_PATTERNS_TO_AVOID.md)

**How to update:**
1. Update the document
2. Update "Last Updated" timestamp
3. Re-upload to Archon knowledge base
4. Announce changes to team

### Document Status

| Document | Status | Last Updated |
|----------|--------|--------------|
| LEGACY_PATTERNS_TO_AVOID.md | Active | 2025-10-13 |
| BACKEND_PATTERNS.md | Active | 2025-10-13 |
| FRONTEND_PATTERNS.md | Active | 2025-10-13 |
| TESTING_PATTERNS.md | Active | 2025-10-13 |
| SECURITY_PATTERNS.md | Active | 2025-10-13 |
| CODING_STANDARDS.md | Active | 2025-10-13 |

---

## Summary

**These 6 documents are the source of truth for:**
- ✅ What patterns to use
- ❌ What patterns to avoid
- 🔒 How to secure code
- 🧪 How to test code
- 🎨 How to style code

**Expected outcome:**
- Consistent codebase
- Secure implementations
- High code quality
- Better AI suggestions
- Faster development (less decision fatigue)

---

**Created**: 2025-10-13
**Purpose**: Project standards for Netzwächter
**Priority**: P0 - MUST follow in all new code
**Integration**: Uploaded to Archon knowledge base

---

## Next Steps

1. ✅ Standards documents created (6 files)
2. ⏳ Upload to Archon knowledge base (see ARCHON_IMPROVEMENT_RECOMMENDATIONS.md)
3. ⏳ Link to Archon project
4. ⏳ Test AI agent suggestions against standards
5. ⏳ Train team on standards

**Implementation time**: 2-3 hours for standards creation (DONE)
**Next**: Upload to Archon (30 minutes) - See Phase 1 Action #5 in ARCHON_IMPROVEMENT_RECOMMENDATIONS.md
