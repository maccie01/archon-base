# Research Task: SQL Injection Prevention

Created: 2025-10-13
Priority: P0
Estimated Effort: 1.5 hours
Status: Not Started

---

## Objective

Create comprehensive documentation on SQL injection prevention patterns, focusing on Drizzle ORM usage, parameterized queries, and input validation for PostgreSQL applications.

---

## Context

**Current State**: File exists but is empty (0 bytes)
**Target**: 250+ lines of SQL injection prevention documentation
**Location**: `knowledgebase/global/04-security-auth/SQL_INJECTION_PREVENTION.md`

**Tech Stack**: PostgreSQL + Drizzle ORM + Node.js

---

## Requirements

### 1. SQL Injection Fundamentals
- What is SQL injection
- How attacks work (classic examples)
- Types: Classic, Blind, Second-order
- Real-world breach examples

### 2. Drizzle ORM Protection
- How Drizzle ORM prevents SQL injection
- Parameterized queries
- Query building safety
- Raw SQL queries (when and how)

### 3. Parameterized Queries
- What are parameterized queries
- How they prevent SQL injection
- Implementation examples
- Performance benefits

### 4. Input Validation
- Validate before queries
- Whitelist vs blacklist
- Type checking
- Zod schema validation

### 5. Least Privilege Database Access
- Principle of least privilege
- Database user permissions
- Connection pooling security
- Service account best practices

### 6. Common Vulnerabilities
- String concatenation in queries
- Dynamic table/column names
- LIKE clauses
- ORDER BY clauses
- Second-order SQL injection

### 7. Safe Patterns
- Using Drizzle ORM query builders
- Handling dynamic filters
- Safe LIKE queries
- Safe ORDER BY implementation

### 8. Testing for SQL Injection
- Manual testing techniques
- Automated tools (SQLMap)
- Unit testing database queries

---

## Code Examples Required

1. **Unsafe SQL (String Concatenation)**
```typescript
// ❌ VULNERABLE - Never do this
const username = req.body.username
const query = `SELECT * FROM users WHERE username = '${username}'`
await db.execute(query)
// Attack: username = "admin' OR '1'='1"
```

2. **Safe with Drizzle ORM**
```typescript
// ✅ SAFE - Drizzle uses parameterized queries
import { eq } from 'drizzle-orm'
import { users } from './schema'

const user = await db
  .select()
  .from(users)
  .where(eq(users.username, username)) // Safely parameterized
  .limit(1)
```

3. **Dynamic Filters (Safe)**
```typescript
import { and, eq, gte, lte } from 'drizzle-orm'

function buildFilters(filters: UserFilters) {
  const conditions = []
  
  if (filters.status) {
    conditions.push(eq(users.status, filters.status))
  }
  
  if (filters.createdAfter) {
    conditions.push(gte(users.createdAt, filters.createdAfter))
  }
  
  return and(...conditions)
}

const results = await db
  .select()
  .from(users)
  .where(buildFilters(req.query))
```

4. **LIKE Queries (Safe)**
```typescript
import { like } from 'drizzle-orm'

// ✅ SAFE - Parameterized LIKE
const searchTerm = req.query.search
const users = await db
  .select()
  .from(users)
  .where(like(users.name, `%${searchTerm}%`))

// Drizzle handles escaping
```

5. **Raw SQL (When Necessary)**
```typescript
import { sql } from 'drizzle-orm'

// If raw SQL is unavoidable, use sql`` template with parameters
const results = await db.execute(
  sql`SELECT * FROM ${users} WHERE ${users.id} = ${userId}`
)

// ❌ NEVER do this with raw SQL:
// sql.raw(`SELECT * FROM users WHERE id = ${userId}`)
```

6. **Input Validation with Zod**
```typescript
import { z } from 'zod'

const userQuerySchema = z.object({
  username: z.string().min(3).max(50).regex(/^[a-zA-Z0-9_]+$/),
  status: z.enum(['active', 'inactive', 'suspended']).optional()
})

app.get('/api/users', async (req, res) => {
  const validated = userQuerySchema.parse(req.query)
  
  const user = await db
    .select()
    .from(users)
    .where(eq(users.username, validated.username))
})
```

---

## References

1. **OWASP SQL Injection Cheat Sheet**
   - https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html

2. **Drizzle ORM Documentation**
   - https://orm.drizzle.team/docs/overview

3. **OWASP Top 10 - Injection**
   - https://owasp.org/Top10/A03_2021-Injection/

4. **PostgreSQL Security Best Practices**
   - https://www.postgresql.org/docs/current/sql-security.html

5. **Bobby Tables (XKCD)**
   - https://bobby-tables.com/

---

## Success Criteria

- [ ] SQL injection fundamentals explained
- [ ] Drizzle ORM protection mechanisms covered
- [ ] At least 6 code examples (unsafe vs safe)
- [ ] Dynamic query building patterns
- [ ] LIKE and ORDER BY safe implementations
- [ ] Input validation integration
- [ ] Least privilege principles
- [ ] Testing methodology
- [ ] Minimum 250 lines
- [ ] Follows existing format

---

## Integration

Replace: `global/04-security-auth/SQL_INJECTION_PREVENTION.md`
Tags: ["shared", "security", "database", "sql-injection"]

---

Created: 2025-10-13
Status: Ready for execution
