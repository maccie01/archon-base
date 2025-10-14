# Research Task: Schema Migrations with Drizzle

Created: 2025-10-13
Priority: P1
Estimated Effort: 4-5 hours
Status: Not Started

---

## Objective

Add comprehensive migration workflow examples to existing schema migrations documentation.

---

## Context

**Current State**: Structure exists, needs 150+ lines of workflow examples
**Target**: Complete migration workflows with Drizzle Kit
**Location**: `knowledgebase/global/03-database-orm/SCHEMA_MIGRATIONS.md`

---

## Requirements

### Topics to Cover

1. **Creating Migrations**
   - Generate migrations from schema changes
   - Manual migration creation
   - Migration file structure

2. **Running Migrations**
   - Apply migrations (up)
   - Rollback migrations (down)
   - Migration status checking

3. **Migration Strategies**
   - Zero-downtime migrations
   - Data migrations vs schema migrations
   - Handling breaking changes

4. **Seeding Data**
   - Seed file structure
   - Development vs production seeds
   - Idempotent seeds

5. **Testing Migrations**
   - Testing migration up/down
   - Integration tests with migrations
   - CI/CD integration

6. **Production Best Practices**
   - Backup before migration
   - Migration monitoring
   - Rollback procedures
   - Blue-green deployments

---

## Code Examples Needed

- Drizzle Kit configuration
- Generate migration command
- Apply migrations script
- Rollback procedure
- Seed data implementation
- Test migrations in CI/CD

---

## References

- Drizzle Kit Documentation
- PostgreSQL migration best practices
- Zero-downtime migration patterns

---

## Success Criteria

- [ ] Complete workflow from schema change to production
- [ ] At least 10 code examples
- [ ] Rollback procedures documented
- [ ] Seeding examples
- [ ] Testing examples
- [ ] 150+ lines added

---

Update: `global/03-database-orm/SCHEMA_MIGRATIONS.md`
Tags: ["shared", "database", "migrations", "drizzle-kit"]

Created: 2025-10-13
