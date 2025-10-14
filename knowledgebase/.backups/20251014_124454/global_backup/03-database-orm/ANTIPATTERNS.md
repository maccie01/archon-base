# Database Anti-Patterns: What NOT to Do

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Production experience, "SQL Antipatterns" by Bill Karwin, PostgreSQL community wisdom

## Overview

This document catalogs common database anti-patterns observed in production systems. Learning what NOT to do is as important as learning best practices.

## Schema Design Anti-Patterns

### Anti-Pattern: EAV (Entity-Attribute-Value)

**What it is:**
Storing data in generic key-value tables instead of proper columns.

```sql
-- TODO: Add EAV anti-pattern example
-- Generic attributes table
-- Why it's terrible
```

**Why it's bad:**
- No data type enforcement
- Poor query performance
- Can't use indexes effectively
- Difficult to validate data
- Breaks referential integrity

**Proper solution:**
Use proper columns, JSONB for truly flexible data.

### Anti-Pattern: God Tables

**What it is:**
Tables with 50+ columns, many nullable, covering multiple concerns.

**Why it's bad:**
- Difficult to understand and maintain
- Many NULL values waste space
- Unclear relationships
- Violates single responsibility principle

**Proper solution:**
Normalize into multiple related tables, use JSONB for truly optional metadata.

### Anti-Pattern: Using VARCHAR(255) Everywhere

**What it is:**
Defaulting to VARCHAR(255) without considering actual data requirements.

**Why it's bad:**
- Often unnecessary (most names/emails are much shorter)
- Historical artifact from old MySQL limitations
- Use TEXT for unlimited length
- Use appropriate length constraints when validation matters

**Proper solution:**
```sql
-- TODO: Add proper VARCHAR usage examples
-- TEXT for no limits
-- VARCHAR(n) only when validation needed
```

### Anti-Pattern: Using Strings for Booleans

**What it is:**
Storing "yes"/"no", "Y"/"N", "true"/"false" as strings.

**Why it's bad:**
- Wastes space (vs 1 byte boolean)
- Allows invalid values
- Harder to query
- Type confusion

**Proper solution:**
Use PostgreSQL BOOLEAN type.

### Anti-Pattern: Using Strings for Enums Without Constraints

**What it is:**
VARCHAR columns for status/type fields without CHECK constraints.

**Why it's bad:**
- Allows typos and invalid values
- No database-level validation
- Inconsistent casing

**Proper solution:**
```sql
-- TODO: Add enum solutions
-- CHECK constraints
-- PostgreSQL ENUM type (with caveats)
-- Reference tables for large value sets
```

### Anti-Pattern: No Foreign Key Constraints

**What it is:**
"We'll enforce relationships in the application."

**Why it's bad:**
- Application bugs cause orphaned records
- No referential integrity guarantee
- Manual cleanup required
- Performance: missing FK indexes

**Proper solution:**
ALWAYS use foreign key constraints.

### Anti-Pattern: UUID as String

**What it is:**
Storing UUIDs as VARCHAR(36) instead of UUID type.

**Why it's bad:**
- Wastes 20 bytes per UUID
- Slower comparisons
- No validation

**Proper solution:**
```sql
-- TODO: Add UUID type example
-- Use PostgreSQL UUID type
-- Use pg_crypto extension for generation
```

### Anti-Pattern: Storing Calculated Values Without Reason

**What it is:**
Denormalizing calculated values without clear performance need.

**Why it's bad:**
- Can become stale
- Update anomalies
- Wasted storage
- Maintenance burden

**When it's acceptable:**
- Proven performance bottleneck
- Values are expensive to calculate
- Have update triggers or application logic to maintain

## Indexing Anti-Patterns

### Anti-Pattern: No Indexes on Foreign Keys

**What it is:**
Foreign key columns without indexes.

**Why it's bad:**
- Slow JOIN queries
- Slow DELETE/UPDATE on parent table
- Lock contention during cascades

**Proper solution:**
ALWAYS index foreign keys.

### Anti-Pattern: Indexing Everything

**What it is:**
Creating indexes on every column "just in case."

**Why it's bad:**
- Slows down writes (INSERT/UPDATE/DELETE)
- Wastes storage
- Query planner confusion with too many choices
- Index maintenance overhead

**Proper solution:**
Index based on query patterns, monitor usage, remove unused indexes.

### Anti-Pattern: Wrong Column Order in Composite Indexes

**What it is:**
Creating index(B, A) when queries filter on A.

**Why it's bad:**
- Index won't be used for queries on A alone
- Wastes resources

**Proper solution:**
```sql
-- TODO: Add composite index ordering examples
-- Most selective column first (usually)
-- Consider query patterns
```

### Anti-Pattern: Not Using CONCURRENTLY in Production

**What it is:**
CREATE INDEX without CONCURRENTLY locks tables.

**Why it's bad:**
- Tables locked for the duration
- Blocks all writes
- Can take hours on large tables

**Proper solution:**
Always use CREATE INDEX CONCURRENTLY in production.

## Query Anti-Patterns

### Anti-Pattern: SELECT *

**What it is:**
Selecting all columns when only a few are needed.

**Why it's bad:**
- Network overhead
- Memory waste
- Prevents index-only scans
- Breaks when columns added

**Proper solution:**
SELECT only needed columns.

### Anti-Pattern: N+1 Queries

**What it is:**
Fetching related data in loops.

```typescript
// TODO: Add N+1 example and solution
// Bad: loop with queries
// Good: JOIN or eager loading
```

**Why it's bad:**
- Exponential query count growth
- Network latency multiplied
- Poor performance

**Proper solution:**
See [QUERY_OPTIMIZATION.md](./QUERY_OPTIMIZATION.md)

### Anti-Pattern: OR in WHERE Without Indexes

**What it is:**
```sql
WHERE column1 = 'value' OR column2 = 'other'
```

**Why it's bad:**
- Can't use indexes effectively
- Often results in sequential scan

**Proper solution:**
```sql
-- TODO: Add UNION solution
-- Rewrite with UNION if needed
-- Or use GIN index on array
```

### Anti-Pattern: NOT IN with Nullable Columns

**What it is:**
```sql
WHERE id NOT IN (SELECT foreign_id FROM other_table)
```

**Why it's bad:**
- Returns unexpected results if subquery has NULL
- Use NOT EXISTS instead

**Proper solution:**
```sql
-- TODO: Add NOT EXISTS example
```

### Anti-Pattern: OFFSET Pagination for Large Datasets

**What it is:**
```sql
LIMIT 20 OFFSET 100000
```

**Why it's bad:**
- Database must scan and skip 100,000 rows
- Performance degrades linearly
- Inconsistent results with concurrent inserts

**Proper solution:**
Use cursor-based or keyset pagination.

## Connection Management Anti-Patterns

### Anti-Pattern: Not Using Connection Pooling

**What it is:**
Creating new connections for every request.

**Why it's bad:**
- Connection overhead is expensive
- PostgreSQL connections are heavyweight
- Runs out of connections quickly
- Poor scalability

**Proper solution:**
Always use connection pooling. See [CONNECTION_POOLING.md](./CONNECTION_POOLING.md)

### Anti-Pattern: Setting max_connections Too High

**What it is:**
Increasing max_connections to 1000+.

**Why it's bad:**
- Each connection uses significant memory
- Doesn't solve the real problem
- Can crash the server

**Proper solution:**
Use PgBouncer or similar connection pooler.

### Anti-Pattern: Long-Running Transactions

**What it is:**
Keeping transactions open for minutes/hours.

**Why it's bad:**
- Blocks other transactions
- Prevents VACUUM from cleaning up
- Bloat accumulates
- Lock contention

**Proper solution:**
Keep transactions as short as possible.

## ORM Anti-Patterns

### Anti-Pattern: Lazy Loading Everywhere

**What it is:**
Relying on ORM's default lazy loading for related data.

**Why it's bad:**
- Causes N+1 queries
- Hidden performance costs
- Hard to debug

**Proper solution:**
Explicit eager loading, monitor queries in development.

### Anti-Pattern: Using ORM for Everything

**What it is:**
Complex reporting queries through ORM query builder.

**Why it's bad:**
- ORM overhead for complex operations
- Difficult to optimize
- Less readable than raw SQL

**Proper solution:**
Use raw SQL for complex analytics, ORM for CRUD.

### Anti-Pattern: Ignoring ORM-Generated Queries

**What it is:**
Not reviewing actual SQL generated by ORM.

**Why it's bad:**
- Can generate inefficient queries
- N+1 queries hidden
- Index opportunities missed

**Proper solution:**
Log queries in development, use EXPLAIN ANALYZE.

## Transaction Anti-Patterns

### Anti-Pattern: No Transactions for Multi-Step Operations

**What it is:**
Multiple related operations without wrapping in transaction.

**Why it's bad:**
- Partial failures leave inconsistent state
- No atomicity guarantee

**Proper solution:**
Wrap related operations in transactions.

### Anti-Pattern: Implicit Transaction Behavior

**What it is:**
Not understanding ORM's transaction defaults.

**Why it's bad:**
- Unexpected autocommit behavior
- Nested transaction issues
- Savepoint confusion

**Proper solution:**
Explicit transaction management, understand your ORM.

## Security Anti-Patterns

### Anti-Pattern: String Concatenation in Queries

**What it is:**
```typescript
// DON'T DO THIS
db.query(`SELECT * FROM users WHERE username = '${userInput}'`)
```

**Why it's bad:**
- SQL injection vulnerability
- Security nightmare

**Proper solution:**
ALWAYS use parameterized queries.

### Anti-Pattern: Running as Superuser

**What it is:**
Application connects as `postgres` superuser.

**Why it's bad:**
- Security risk
- No privilege separation
- Can't audit application vs admin actions

**Proper solution:**
Create application-specific users with minimal privileges.

### Anti-Pattern: Storing Passwords in Plain Text

**What it is:**
Storing passwords without hashing.

**Why it's bad:**
- Security catastrophe
- Compliance violation
- Data breach impact

**Proper solution:**
Use bcrypt/scrypt/argon2, never store plain text.

## Maintenance Anti-Patterns

### Anti-Pattern: Ignoring Autovacuum

**What it is:**
Disabling or not tuning autovacuum.

**Why it's bad:**
- Table bloat
- Performance degradation
- Transaction ID wraparound risk

**Proper solution:**
Monitor and tune autovacuum, never disable.

### Anti-Pattern: No Backup Testing

**What it is:**
Taking backups but never testing restore.

**Why it's bad:**
- Backups might be corrupted
- Restore procedure might not work
- False sense of security

**Proper solution:**
Regular restore testing, documented procedures.

### Anti-Pattern: No Monitoring

**What it is:**
Running production without monitoring.

**Why it's bad:**
- Can't detect issues early
- No performance baselines
- Blind troubleshooting

**Proper solution:**
pg_stat_statements, monitoring tools, alerting.

## Migration Anti-Patterns

### Anti-Pattern: No Rollback Plan

**What it is:**
Migrations without considering rollback.

**Why it's bad:**
- Can't easily undo changes
- Production issues with no escape
- Downtime extended

**Proper solution:**
Test rollback procedures, backward-compatible migrations.

### Anti-Pattern: Large Schema Changes Without Testing

**What it is:**
ALTER TABLE on huge table without testing.

**Why it's bad:**
- Can take hours and lock table
- Might fail due to constraints
- Extended downtime

**Proper solution:**
Test on production-sized data, consider online migration strategies.

## Performance Anti-Patterns

### Anti-Pattern: Using PostgreSQL Like MongoDB

**What it is:**
Storing everything in JSONB, no relations.

**Why it's bad:**
- Loses benefits of relational database
- Poor query performance
- No referential integrity

**Proper solution:**
Use relational design, JSONB for truly flexible data only.

### Anti-Pattern: One Index Per Query

**What it is:**
Creating separate indexes for each query variation.

**Why it's bad:**
- Index proliferation
- Maintenance overhead
- Diminishing returns

**Proper solution:**
Composite indexes that serve multiple queries.

## When "Anti-Patterns" Might Be Acceptable

Some anti-patterns have valid use cases:

1. **Denormalization:** For proven performance bottlenecks
2. **Stored calculated values:** When calculation is expensive
3. **JSONB heavy:** For truly schema-less data from external sources
4. **Few indexes:** For write-heavy tables
5. **SELECT *:** In application admin tools where all data is needed

The key: Make informed decisions, not cargo-culted choices.

## Additional Resources

### Books
- "SQL Antipatterns" by Bill Karwin
- "Database Design for Mere Mortals" by Michael J. Hernandez

### Related Knowledge Base Articles
- [Database Design](./DATABASE_DESIGN.md)
- [PostgreSQL Best Practices](./POSTGRESQL_BEST_PRACTICES.md)
- [Query Optimization](./QUERY_OPTIMIZATION.md)
- [Indexing and Optimization](./INDEXING_OPTIMIZATION.md)
- [Database Security](./DATABASE_SECURITY.md)
