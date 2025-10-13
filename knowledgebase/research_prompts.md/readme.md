# Research Prompts Organization

Created: 2025-10-13
Last Updated: 2025-10-13

---

## Purpose

This directory organizes research tasks needed to complete the Archon knowledge base. Each prompt is designed to be executed by a task agent to fill gaps in documentation.

---

## Directory Structure

```
research_prompts.md/
├── README.md              # This file
├── prompts/               # Research task prompts for agents
│   ├── security/          # 14 empty security files (CRITICAL)
│   ├── database/          # Drizzle ORM examples
│   ├── frontend/          # React implementation examples
│   └── testing/           # Testing suite examples
├── answers/               # Completed research results
│   └── [same structure as prompts/]
└── TASK_TRACKER.md        # Progress tracking
```

---

## Workflow

### For Task Agents

1. Select a prompt file from `prompts/`
2. Research the topic using authoritative sources
3. Create comprehensive documentation following the template
4. Save result to `answers/` with same filename
5. Update `TASK_TRACKER.md` with completion status

### For Developers

1. Review `TASK_TRACKER.md` for priority tasks
2. Assign tasks to task agents
3. Review completed answers in `answers/`
4. Integrate completed documentation into knowledge base
5. Update knowledge base README with new content

---

## Priority Levels

- **P0 (Critical)**: Must complete - Week 1
  - 14 empty security files

- **P1 (High)**: Should complete - Week 2-3
  - Drizzle ORM examples
  - React implementation examples
  - Testing suite examples

- **P2 (Medium)**: Nice to have - Week 4+
  - Design system documentation
  - Refactoring guides

---

## Research Prompt Template

Each prompt file follows this structure:

```markdown
# Research Task: [Topic Name]

Created: YYYY-MM-DD
Priority: P0/P1/P2
Estimated Effort: X hours
Status: Not Started

---

## Objective
[What needs to be researched/created]

## Context
[Existing documentation, related files, current state]

## Requirements
- [Specific requirement 1]
- [Specific requirement 2]

## Output Format
[Expected structure, length, sections]

## Code Examples Required
- [Type 1]
- [Type 2]

## References
- [Authoritative sources to consult]

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Integration
[Where this content will be added in knowledge base]
```

---

## Current Status

### Security Research (14 files) - P0
- [ ] JWT_PATTERNS.md (0 → 400+ lines)
- [ ] CORS_CONFIGURATION.md (0 → 300 lines)
- [ ] CSRF_PROTECTION.md (0 → 250 lines)
- [ ] RATE_LIMITING.md (0 → 300 lines)
- [ ] XSS_PREVENTION.md (0 → 250 lines)
- [ ] SQL_INJECTION_PREVENTION.md (0 → 250 lines)
- [ ] INPUT_VALIDATION.md (0 → 300 lines)
- [ ] SECURITY_HEADERS.md (0 → 250 lines)
- [ ] API_SECURITY.md (0 → 350 lines)
- [ ] SECRETS_MANAGEMENT.md (0 → 300 lines)
- [ ] SSL_TLS.md (0 → 250 lines)
- [ ] SECURITY_TESTING.md (0 → 300 lines)
- [ ] OAUTH2_OPENID.md (0 → 400 lines)
- [ ] MFA_PATTERNS.md (0 → 300 lines)

**Total Estimated Effort**: 20-25 hours

### Database Research (3 files) - P1
- [ ] Drizzle ORM query examples
- [ ] Schema migration workflows
- [ ] Query optimization patterns

**Total Estimated Effort**: 15-20 hours

### Frontend Research (4 files) - P1
- [ ] React component patterns with code
- [ ] Custom hooks implementations
- [ ] Form validation examples
- [ ] State management patterns

**Total Estimated Effort**: 25-30 hours

### Testing Research (3 files) - P1
- [ ] Vitest complete test suites
- [ ] Playwright E2E examples
- [ ] MSW mocking patterns

**Total Estimated Effort**: 20-25 hours

---

## Quality Standards

All research outputs must include:

- Clear, concise explanations
- Working code examples (tested)
- Security considerations
- Best practices and anti-patterns
- Real-world use cases
- Performance implications
- References to authoritative sources
- Integration with existing patterns

---

## Next Steps

1. Create all prompt files in `prompts/` subdirectories
2. Start with P0 security prompts (highest priority)
3. Execute prompts using task agents
4. Review and integrate completed answers
5. Update main knowledge base README

---

Status: Research framework ready
Next: Create individual prompt files
