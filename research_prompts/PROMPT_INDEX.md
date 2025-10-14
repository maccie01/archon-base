# Research Prompts Index

Created: 2025-10-13
Last Updated: 2025-10-13

---

## Overview

Complete index of all 24 research prompts organized by category and priority.

**Total Prompts**: 24 (excludes existing perplexity research)
**Status**: All prompts created ✅
**Results Placeholders**: All created ✅

---

## Directory Structure

```
research_prompts.md/
├── prompts/
│   ├── security/          (14 prompts - P0)
│   ├── database/          (3 prompts - P1)
│   ├── frontend/          (4 prompts - P1)
│   └── testing/           (3 prompts - P1)
└── results/
    ├── security/          (14 placeholders)
    ├── database/          (3 placeholders)
    ├── frontend/          (4 placeholders)
    └── testing/           (3 placeholders)
```

---

## P0 - CRITICAL (Security) - 20-25 hours

| # | Prompt File | Target File | Effort | Status |
|---|-------------|-------------|--------|--------|
| 01 | `security/01_JWT_PATTERNS.md` | `global/04-security-auth/JWT_PATTERNS.md` | 2h | Not Started |
| 02 | `security/02_CORS_CONFIGURATION.md` | `global/04-security-auth/CORS_CONFIGURATION.md` | 1.5h | Not Started |
| 03 | `security/03_RATE_LIMITING.md` | `global/04-security-auth/RATE_LIMITING.md` | 1.5h | Not Started |
| 04 | `security/04_CSRF_PROTECTION.md` | `global/04-security-auth/CSRF_PROTECTION.md` | 1.5h | Not Started |
| 05 | `security/05_XSS_PREVENTION.md` | `global/04-security-auth/XSS_PREVENTION.md` | 1.5h | Not Started |
| 06 | `security/06_SQL_INJECTION_PREVENTION.md` | `global/04-security-auth/SQL_INJECTION_PREVENTION.md` | 1.5h | Not Started |
| 07 | `security/07_INPUT_VALIDATION.md` | `global/04-security-auth/INPUT_VALIDATION.md` | 2h | Not Started |
| 08 | `security/08_SECURITY_HEADERS.md` | `global/04-security-auth/SECURITY_HEADERS.md` | 1.5h | Not Started |
| 09 | `security/09_API_SECURITY.md` | `global/04-security-auth/API_SECURITY.md` | 2h | Not Started |
| 10 | `security/10_SECRETS_MANAGEMENT.md` | `global/04-security-auth/SECRETS_MANAGEMENT.md` | 2h | Not Started |
| 11 | `security/11_SSL_TLS.md` | `global/04-security-auth/SSL_TLS.md` | 1.5h | Not Started |
| 12 | `security/12_SECURITY_TESTING.md` | `global/04-security-auth/SECURITY_TESTING.md` | 2h | Not Started |
| 13 | `security/13_OAUTH2_OPENID.md` | `global/04-security-auth/OAUTH2_OPENID.md` | 2.5h | Not Started |
| 14 | `security/14_MFA_PATTERNS.md` | `global/04-security-auth/MFA_PATTERNS.md` | 2h | Not Started |

**Subtotal**: 14 tasks, 20-25 hours

---

## P1 - HIGH PRIORITY (Database) - 15-20 hours

| # | Prompt File | Target File | Effort | Status |
|---|-------------|-------------|--------|--------|
| 15 | `database/01_DRIZZLE_QUERY_EXAMPLES.md` | `global/03-database-orm/DRIZZLE_PATTERNS.md` | 6-8h | Not Started |
| 16 | `database/02_SCHEMA_MIGRATIONS.md` | `global/03-database-orm/SCHEMA_MIGRATIONS.md` | 4-5h | Not Started |
| 17 | `database/03_QUERY_OPTIMIZATION.md` | `global/03-database-orm/QUERY_OPTIMIZATION.md` | 5-7h | Not Started |

**Subtotal**: 3 tasks, 15-20 hours

---

## P1 - HIGH PRIORITY (Frontend) - 25-30 hours

| # | Prompt File | Target File | Effort | Status |
|---|-------------|-------------|--------|--------|
| 18 | `frontend/01_COMPONENT_PATTERNS.md` | `global/01-react-frontend/COMPONENT_PATTERNS.md` | 8-10h | Not Started |
| 19 | `frontend/02_HOOKS_PATTERNS.md` | `global/01-react-frontend/HOOKS_PATTERNS.md` | 6-8h | Not Started |
| 20 | `frontend/03_FORMS_VALIDATION.md` | `global/01-react-frontend/FORMS_VALIDATION.md` | 6-8h | Not Started |
| 21 | `frontend/04_STATE_MANAGEMENT.md` | `global/01-react-frontend/STATE_MANAGEMENT.md` | 5-6h | Not Started |

**Subtotal**: 4 tasks, 25-30 hours

---

## P1 - HIGH PRIORITY (Testing) - 20-25 hours

| # | Prompt File | Target File | Effort | Status |
|---|-------------|-------------|--------|--------|
| 22 | `testing/01_VITEST_PATTERNS.md` | `global/05-testing-quality/VITEST_PATTERNS.md` | 8-10h | Not Started |
| 23 | `testing/02_E2E_TESTING.md` | `global/05-testing-quality/E2E_TESTING.md` | 7-9h | Not Started |
| 24 | `testing/03_MOCKING_PATTERNS.md` | `global/05-testing-quality/MOCKING_PATTERNS.md` | 5-6h | Not Started |

**Subtotal**: 3 tasks, 20-25 hours

---

## Usage Workflow

### For Each Research Task

1. **Read the Prompt**
   ```bash
   cat prompts/security/01_JWT_PATTERNS.md
   ```

2. **Conduct Research**
   - Use task agent or manual research
   - Follow all requirements in prompt
   - Create working code examples
   - Test all code

3. **Paste Result**
   ```bash
   # Paste completed markdown into:
   results/security/01_JWT_PATTERNS.md
   ```

4. **Integrate into Knowledge Base**
   ```bash
   # Copy result to target location:
   cp results/security/01_JWT_PATTERNS.md \
      ../../global/04-security-auth/JWT_PATTERNS.md
   ```

5. **Update Trackers**
   - Mark task complete in `TASK_TRACKER.md`
   - Update completion percentage
   - Update `knowledgebase/README.md` stats

---

## Execution Strategy

### Week 1 (P0 - Security)
Execute all 14 security prompts (can run in parallel):

**Day 1-2**: Tasks 1-4 (JWT, CORS, Rate Limiting, CSRF)
**Day 3-4**: Tasks 5-8 (XSS, SQL Injection, Input Validation, Headers)
**Day 5-6**: Tasks 9-12 (API Security, Secrets, SSL/TLS, Testing)
**Day 7**: Tasks 13-14 (OAuth2, MFA)

### Week 2 (P1 - Database)
Execute database prompts sequentially:

**Days 1-2**: Task 15 (Drizzle Query Examples)
**Days 3-4**: Task 16 (Schema Migrations)
**Days 5-6**: Task 17 (Query Optimization)

### Week 3 (P1 - Frontend)
Execute frontend prompts (can run in parallel):

**Days 1-2**: Task 18 (Component Patterns)
**Days 3-4**: Task 19 (Hooks Patterns)
**Days 5-6**: Task 20 (Forms Validation)
**Day 7**: Task 21 (State Management)

### Week 4 (P1 - Testing)
Execute testing prompts (can run in parallel):

**Days 1-3**: Task 22 (Vitest Patterns)
**Days 4-6**: Task 23 (E2E Testing)
**Day 7**: Task 24 (Mocking Patterns)

---

## Quality Assurance

Before marking any task complete, ensure:

- [ ] All requirements from prompt met
- [ ] Code examples tested and working
- [ ] Minimum line count achieved
- [ ] References to authoritative sources included
- [ ] Security considerations highlighted (where applicable)
- [ ] Anti-patterns documented
- [ ] Follows existing knowledge base format
- [ ] TypeScript with proper types
- [ ] Error handling examples included (where applicable)

---

## Progress Tracking

Track progress in:
- `TASK_TRACKER.md` - Task-by-task status
- `COMPLETION_TODOS.md` - Detailed action items
- `../README.md` - Overall knowledge base completion

---

## Notes

- All prompts are self-contained and can be executed independently
- Security prompts (P0) can be executed in parallel by multiple agents
- Each prompt includes specific requirements, code examples needed, and success criteria
- Results placeholders are ready for completed research
- Integration paths are clearly defined

---

**Status**: All 24 prompts created ✅
**Next**: Execute P0 security prompts (Week 1)
**Timeline**: 4 weeks to complete all prompts

Created: 2025-10-13
