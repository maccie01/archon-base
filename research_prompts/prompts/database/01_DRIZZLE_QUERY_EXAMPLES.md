# Research Task: Drizzle ORM Query Examples

Created: 2025-10-13
Priority: P1
Estimated Effort: 6-8 hours
Status: Not Started

---

## Objective

Add comprehensive query examples to existing Drizzle ORM patterns documentation, covering all common database operations with PostgreSQL.

---

## Context

**Current State**: Structure exists, needs 200+ lines of query examples
**Target**: Add working code examples for all query patterns
**Location**: `knowledgebase/global/03-database-orm/DRIZZLE_PATTERNS.md`

---

## Requirements

### Query Patterns to Add Examples For

1. **Basic CRUD Operations**
   - Select (all, filtered, with conditions)
   - Insert (single, multiple, with returning)
   - Update (single, multiple, conditional)
   - Delete (soft delete, hard delete)

2. **Complex Joins**
   - Inner join
   - Left join
   - Right join
   - Multiple table joins
   - Join with conditions

3. **Subqueries**
   - Subquery in WHERE
   - Subquery in SELECT
   - EXISTS/NOT EXISTS

4. **Aggregations**
   - COUNT, SUM, AVG, MIN, MAX
   - GROUP BY with HAVING
   - Window functions

5. **Transactions**
   - Begin/commit/rollback
   - Nested transactions
   - Error handling in transactions

6. **Batch Operations**
   - Batch insert
   - Batch update
   - Performance considerations

7. **Pagination Patterns**
   - Offset-based pagination
   - Cursor-based pagination
   - Limit/offset with sorting

8. **Full-Text Search**
   - PostgreSQL full-text search
   - ts_vector usage
   - Ranking results

9. **JSONB Operations**
   - Querying JSONB columns
   - Updating nested JSONB
   - JSONB indexing

10. **Relations and Eager Loading**
    - One-to-many queries
    - Many-to-many queries
    - Nested relations

---

## Code Examples Required

All examples must:
- Use TypeScript with proper types
- Be tested and working
- Include comments explaining the query
- Show both the Drizzle query and what SQL it generates
- Include error handling where appropriate

### Example Format
```typescript
// 1. Basic Select with Filter
import { eq, and, gte } from 'drizzle-orm'
import { users } from './schema'

// Get active users created after a date
const activeUsers = await db
  .select()
  .from(users)
  .where(
    and(
      eq(users.status, 'active'),
      gte(users.createdAt, new Date('2024-01-01'))
    )
  )

// Generated SQL:
// SELECT * FROM users 
// WHERE status = 'active' AND created_at >= '2024-01-01'
```

---

## References

- Drizzle ORM Documentation: https://orm.drizzle.team/docs/overview
- Drizzle ORM Queries: https://orm.drizzle.team/docs/rqb
- PostgreSQL Documentation: https://www.postgresql.org/docs/

---

## Success Criteria

- [ ] Examples for all 10 query pattern categories
- [ ] At least 30 working code examples
- [ ] Each example includes generated SQL comment
- [ ] TypeScript with proper types
- [ ] Performance notes where relevant
- [ ] Error handling examples
- [ ] 200+ lines added to existing file
- [ ] All code tested

---

## Integration

Update existing file: `global/03-database-orm/DRIZZLE_PATTERNS.md`
Add examples to appropriate sections throughout the document

Tags: ["shared", "database", "drizzle-orm", "queries"]

Created: 2025-10-13
Status: Ready for execution
