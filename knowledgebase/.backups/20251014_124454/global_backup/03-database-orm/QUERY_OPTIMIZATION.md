# Query Optimization Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Perplexity research on N+1 problem, query optimization patterns, PostgreSQL query performance

## Overview

Query optimization is essential for application performance. This document covers detecting and preventing N+1 queries, optimizing joins, understanding query execution, and other query performance patterns.

## Core Principles

1. The N+1 problem is the most common performance killer
2. Use EXPLAIN ANALYZE to understand query execution
3. Fetch only the columns you need
4. Use appropriate join strategies
5. Batch queries when possible
6. Monitor slow queries continuously
7. Index columns used in WHERE, JOIN, and ORDER BY

## The N+1 Query Problem

### What is N+1?

The N+1 problem occurs when:
1. Execute 1 query to fetch N records
2. Execute N additional queries (one per record) to fetch related data
3. Total: N+1 queries instead of 1-2 optimized queries

### Example

```typescript
// TODO: Add N+1 problem example
// BAD: N+1 queries
// Fetching users, then fetching posts for each user in a loop

// GOOD: Optimized approach
// Single query with JOIN or eager loading
```

### Detection

```typescript
// TODO: Add N+1 detection methods
// Logging all queries in development
// Counting queries per request
// Using database query logs
// APM tools
```

### Prevention Strategies

**Strategy 1: Eager Loading with Joins**
```typescript
// TODO: Add eager loading examples in Drizzle
// Using .with() for relations
// leftJoin for optional relations
```

**Strategy 2: Batching with DataLoader**
```typescript
// TODO: Add DataLoader pattern
// Batching queries
// Caching within request
// GraphQL integration
```

**Strategy 3: Subquery or CTE**
```typescript
// TODO: Add subquery examples
// WITH (Common Table Expression)
// Subqueries for aggregations
```

## Join Optimization

### Join Types

**INNER JOIN:**
```sql
-- TODO: Add INNER JOIN examples
-- When to use: matching records only
-- Performance characteristics
```

**LEFT JOIN:**
```sql
-- TODO: Add LEFT JOIN examples
-- When to use: optional related data
-- NULL handling
```

**RIGHT JOIN:**
```sql
-- TODO: Add RIGHT JOIN examples
-- When to use (rarely): reverse of LEFT JOIN
```

**FULL OUTER JOIN:**
```sql
-- TODO: Add FULL OUTER JOIN examples
-- When to use (rarely): both sides with NULLs
```

### Join Strategies (Query Planner)

**Nested Loop Join:**
- Best for small result sets
- Uses indexes effectively
- Inner loop index scan

**Hash Join:**
- Good for large result sets
- Equality conditions
- Builds hash table in memory

**Merge Join:**
- Pre-sorted data
- Equality conditions
- Efficient for sorted inputs

```sql
-- TODO: Add EXPLAIN output showing different join strategies
-- How planner chooses strategy
```

### Join Performance Tips

1. Index foreign key columns (always)
2. Join on indexed columns
3. Filter early (WHERE before JOIN when possible)
4. Consider join order in complex queries
5. Use appropriate join type (INNER vs LEFT)

## Subqueries and CTEs

### Subqueries

```sql
-- TODO: Add subquery examples
-- Correlated vs non-correlated
-- IN vs EXISTS
-- Performance considerations
```

### Common Table Expressions (WITH)

```sql
-- TODO: Add CTE examples
-- Readability benefits
-- Recursive CTEs
-- Materialized vs non-materialized (PostgreSQL 12+)
```

**When to use CTEs:**
- Complex queries that need readability
- Recursive operations (tree structures)
- Multiple references to same subquery
- Window functions

## Aggregations

### GROUP BY Optimization

```sql
-- TODO: Add GROUP BY examples
-- Proper indexing for GROUP BY
-- HAVING vs WHERE
-- Aggregate functions: COUNT, SUM, AVG, MIN, MAX
```

### Window Functions

```sql
-- TODO: Add window function examples
-- ROW_NUMBER, RANK, DENSE_RANK
-- Partitioning
-- Performance characteristics
```

## Pagination Patterns

### Offset-Based Pagination (Simple but Problematic)

```typescript
// TODO: Add offset pagination example
// LIMIT and OFFSET
// Problems: performance degrades with large offsets
// Inconsistent results with concurrent inserts
```

### Cursor-Based Pagination (Recommended)

```typescript
// TODO: Add cursor pagination example
// Using unique ID or timestamp
// Consistent results
// Better performance for large datasets
```

### Keyset Pagination

```typescript
// TODO: Add keyset pagination example
// WHERE id > last_id ORDER BY id LIMIT n
// Most efficient for large tables
```

## Selecting Columns Efficiently

### Avoid SELECT *

```typescript
// TODO: Add SELECT * anti-pattern
// Why it's bad: fetches unused data
// Network overhead
// Index-only scan prevention

// GOOD: Select only needed columns
```

### Covering Indexes

```typescript
// TODO: Add covering index examples for queries
// Index includes all selected columns
// Index-only scans
```

See [INDEXING_OPTIMIZATION.md](./INDEXING_OPTIMIZATION.md) for detailed index patterns.

## Query Execution Analysis

### Using EXPLAIN

```sql
-- TODO: Add EXPLAIN examples
-- Reading execution plans
-- Cost estimation
-- Row count estimates
-- Scan types
```

### Using EXPLAIN ANALYZE

```sql
-- TODO: Add EXPLAIN ANALYZE examples
-- Actual vs estimated rows
-- Execution time breakdown
-- Buffer usage
-- I/O statistics
```

### Understanding Costs

```sql
-- TODO: Add cost interpretation guide
-- Startup cost vs total cost
-- Cost units (not milliseconds)
-- When estimates are wrong
```

### Common Plan Issues

**High Cost:**
```sql
-- TODO: Add high cost pattern examples
-- Missing indexes
-- Large sequential scans
```

**Row Estimate Errors:**
```sql
-- TODO: Add row estimate error examples
-- Stale statistics (need ANALYZE)
-- Complex predicates
-- Correlated columns
```

## Batch Operations

### Bulk Inserts

```typescript
// TODO: Add bulk insert examples
// Insert multiple rows in one query
// Performance comparison: 1000 single inserts vs 1 bulk insert
```

### Bulk Updates

```typescript
// TODO: Add bulk update examples
// UPDATE with IN clause
// UPDATE from temporary table
```

### Bulk Deletes

```typescript
// TODO: Add bulk delete examples
// DELETE with IN clause
// Batching large deletes to avoid locks
```

## Query Performance Patterns

### Materialized Views

```sql
-- TODO: Add materialized view examples
-- Pre-computed aggregations
-- REFRESH MATERIALIZED VIEW
-- When to use vs regular views
```

### Partial Indexes for Filtered Queries

```sql
-- TODO: Add partial index examples for common WHERE clauses
-- Active users index
-- Published posts index
```

See [INDEXING_OPTIMIZATION.md](./INDEXING_OPTIMIZATION.md) for index details.

### Prepared Statements

```typescript
// TODO: Add prepared statement examples
-- Query plan caching
-- Performance benefits
-- Parameter binding
```

## Monitoring Slow Queries

### pg_stat_statements

```sql
-- TODO: Add pg_stat_statements queries
-- Finding slowest queries by total time
-- Finding slowest queries by average time
-- Identifying queries needing optimization
```

### Log-Based Monitoring

```sql
-- TODO: Add PostgreSQL slow query log configuration
-- log_min_duration_statement
-- Analyzing slow query logs
```

### Application Performance Monitoring (APM)

- New Relic Database Monitoring
- Datadog APM
- Scout APM
- SolarWinds Database Performance Analyzer

## Database-Specific Optimizations

### PostgreSQL-Specific

**Parallel Queries:**
```sql
-- TODO: Add parallel query examples
-- max_parallel_workers_per_gather
-- When parallel queries are used
```

**JIT Compilation:**
```sql
-- TODO: Add JIT compilation examples
-- jit = on
-- When JIT helps (large queries)
```

**Statistics Targets:**
```sql
-- TODO: Add statistics configuration
-- ALTER TABLE ... ALTER COLUMN ... SET STATISTICS
-- When to increase for complex predicates
```

## ORM-Specific Patterns

### Drizzle ORM Query Optimization

```typescript
// TODO: Add Drizzle-specific optimization patterns
-- Using .select() to limit columns
-- Eager loading with .with()
-- Prepared statements with .prepare()
-- Raw SQL for complex queries
```

### Common ORM Pitfalls

1. **Lazy loading causing N+1**
2. **Over-fetching with SELECT ***
3. **Not using query builders efficiently**
4. **Ignoring database-specific features**

## Anti-Patterns

### Anti-Pattern: Not Using Indexes
See [INDEXING_OPTIMIZATION.md](./INDEXING_OPTIMIZATION.md)

### Anti-Pattern: SELECT * in Production
Always specify needed columns.

### Anti-Pattern: Multiple Round-Trips for Related Data
Use JOINs or eager loading.

### Anti-Pattern: Ignoring EXPLAIN ANALYZE
Always analyze slow queries before optimizing.

### Anti-Pattern: Premature Optimization
Measure first, optimize second. Don't optimize queries that aren't slow.

### Anti-Pattern: Using ORM for Everything
Complex reporting queries often need raw SQL.

### Anti-Pattern: Not Monitoring Query Performance
Set up pg_stat_statements and regular monitoring.

## Query Optimization Checklist

1. Identify slow queries (pg_stat_statements, APM)
2. Run EXPLAIN ANALYZE
3. Check for missing indexes
4. Verify statistics are up-to-date (ANALYZE)
5. Review join conditions and types
6. Check for N+1 patterns
7. Consider query rewrite (subquery to JOIN, etc.)
8. Test optimization impact
9. Monitor ongoing performance

## Tools

### Query Analysis
- **EXPLAIN / EXPLAIN ANALYZE** - Built-in PostgreSQL
- **pg_stat_statements** - Query statistics extension
- **pgBadger** - Log analyzer
- **pganalyze** - Query performance insights

### Performance Monitoring
- **pgAdmin** - GUI with query analysis
- **DataGrip** - JetBrains database IDE
- **Datadog** - APM with database monitoring
- **New Relic** - APM with database insights

### Development Tools
- **Drizzle Studio** - Visual query builder
- **psql** - Command-line interface with \timing

## Additional Resources

### Documentation
- PostgreSQL EXPLAIN: https://www.postgresql.org/docs/current/sql-explain.html
- Query Performance Tips: https://wiki.postgresql.org/wiki/Performance_Optimization

### Books and Guides
- "Use The Index, Luke" by Markus Winand
- "SQL Performance Explained" by Markus Winand

### Online Resources
- EXPLAIN Visualizers: https://explain.dalibo.com/
- PostgreSQL Explain Visualizer (Depesz): https://explain.depesz.com/

### Related Knowledge Base Articles
- [Indexing and Optimization](./INDEXING_OPTIMIZATION.md)
- [PostgreSQL Best Practices](./POSTGRESQL_BEST_PRACTICES.md)
- [Drizzle ORM Patterns](./DRIZZLE_PATTERNS.md)
- [Database Design](./DATABASE_DESIGN.md)
