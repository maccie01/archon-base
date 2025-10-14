# Indexing and Optimization Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Perplexity research on PostgreSQL indexing strategies 2024-2025, index types, query optimization

## Overview

Indexes are the primary tool for optimizing query performance in PostgreSQL. However, indexes come with costs: storage overhead and write performance impact. This document covers when and how to use different index types effectively.

## Core Principles

1. Index foreign keys - always, without exception
2. Index columns used in WHERE, JOIN, and ORDER BY clauses
3. Composite indexes: most selective column first
4. Covering indexes reduce table access overhead
5. Monitor index usage - remove unused indexes
6. Partial indexes for filtered queries
7. Too many indexes hurt write performance

## Index Types in PostgreSQL

### B-tree Indexes (Default)

The workhorse of PostgreSQL indexing. Used for:
- Equality operations (=)
- Range queries (<, <=, >, >=)
- LIKE with prefix matching ('prefix%')
- IN clauses
- IS NULL / IS NOT NULL

```sql
-- TODO: Add B-tree index examples
-- Single column index
-- Composite index
-- Unique index
```

**When to use:**
- 95% of indexing needs
- Primary keys and foreign keys
- Columns with high cardinality
- Range queries

**PostgreSQL 17 improvement:**
Enhanced handling of IN clauses with better skip scan optimization.

### GIN Indexes (Generalized Inverted Index)

Used for indexing composite values:
- Arrays
- JSONB documents
- Full-text search (tsvector)
- Containment operations

```sql
-- TODO: Add GIN index examples
-- Array containment
-- JSONB path operations
-- jsonb_ops vs jsonb_path_ops
-- Full-text search indexes
```

**When to use:**
- JSONB column queries
- Array containment checks
- Full-text search
- Any "contains" operations

**Trade-offs:**
- Larger index size than B-tree
- Slower writes (more index updates)
- Excellent for read-heavy workloads

### GIST Indexes (Generalized Search Tree)

Used for geometric and spatial data:
- PostGIS spatial queries
- Range types
- Text similarity (pg_trgm)
- Nearest-neighbor searches

```sql
-- TODO: Add GIST index examples
-- Range type indexes
-- Geometric data
-- Text similarity (trigram matching)
```

**When to use:**
- Spatial data (coordinates, polygons)
- Range overlaps
- Fuzzy text matching
- K-nearest neighbor queries

### BRIN Indexes (Block Range Index)

Extremely compact indexes for large, ordered tables:
- Time-series data
- Append-only tables
- Naturally ordered data

```sql
-- TODO: Add BRIN index examples
-- Time-series table indexes
-- Configuration: pages_per_range
-- When BRIN outperforms B-tree
```

**When to use:**
- Very large tables (>10GB)
- Strong correlation between column value and physical storage order
- Append-only insert patterns
- Time-series data ordered by timestamp

**Trade-offs:**
- Much smaller than B-tree (100x-1000x smaller)
- Requires sorted data for effectiveness
- Less precise than B-tree (scans ranges of blocks)

### Hash Indexes

Used for equality comparisons only:
```sql
-- TODO: Add hash index examples
-- When hash indexes make sense
```

**When to use:**
- Almost never - B-tree is typically better
- Only for exact equality comparisons
- Cannot be used for range queries
- Historical reasons make B-tree preferred

## Composite Indexes

### Column Order Matters

Index on (A, B, C) supports queries filtering on:
- A
- A and B
- A and B and C

Does NOT efficiently support:
- B alone
- C alone
- B and C

```sql
-- TODO: Add composite index examples
-- Correct column ordering
-- Query patterns that benefit
-- Query patterns that don't benefit
```

### Ordering Strategy

**General rule:** Most selective column first

**Exceptions:**
- Equality before ranges
- Consider query patterns holistically

```sql
-- TODO: Add composite index ordering examples
-- (status, created_at) vs (created_at, status)
-- When order matters for performance
```

## Covering Indexes (Index-Only Scans)

PostgreSQL 11+ supports INCLUDE clause for covering indexes:

```sql
-- TODO: Add covering index examples
-- CREATE INDEX idx_users_email_covering ON users(email) INCLUDE (first_name, last_name);
-- When index-only scans are possible
-- EXPLAIN showing Index Only Scan
```

**Benefits:**
- Eliminates heap access for covered columns
- Can dramatically improve query performance
- Especially valuable for frequently executed queries

**Trade-offs:**
- Larger index size
- Slightly slower writes
- More storage required

**When to use:**
- Frequently executed queries selecting specific columns
- Read-heavy tables
- When index size increase is acceptable

## Partial Indexes

Indexes that cover only a subset of rows:

```sql
-- TODO: Add partial index examples
-- CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';
-- Use cases: soft deletes, status filtering
-- Query must match index predicate for use
```

**Benefits:**
- Smaller index size
- Faster writes (fewer rows indexed)
- Better cache utilization
- Ideal for filtered queries

**When to use:**
- Queries consistently filter on specific condition
- Large percentage of rows can be excluded
- Status-based filtering (active/inactive, published/draft)

## Expression Indexes

Indexes on computed values:

```sql
-- TODO: Add expression index examples
-- CREATE INDEX idx_users_lower_email ON users(LOWER(email));
-- Use cases: case-insensitive searches
-- Performance considerations
```

**When to use:**
- Case-insensitive searches
- Computed columns frequently queried
- Function results in WHERE clauses

## Index Maintenance

### Monitoring Index Usage

```sql
-- TODO: Add index usage monitoring queries
-- pg_stat_user_indexes
-- Finding unused indexes
-- Index scan vs sequential scan ratios
```

### Identifying Missing Indexes

```sql
-- TODO: Add queries to identify missing indexes
-- Tables with high sequential scan counts
-- Foreign keys without indexes
```

### Index Bloat

```sql
-- TODO: Add index bloat detection queries
-- pgstattuple extension
-- When to REINDEX
-- REINDEX CONCURRENTLY (PostgreSQL 12+)
```

### Removing Unused Indexes

```sql
-- TODO: Add unused index identification and removal
-- DROP INDEX CONCURRENTLY (avoids locking table)
```

## Query Optimization Patterns

### Using EXPLAIN ANALYZE

```sql
-- TODO: Add EXPLAIN ANALYZE examples
-- Reading execution plans
-- Cost interpretation
-- Identifying missing indexes
-- Buffer cache statistics
```

### Index Scan Types

**Index Scan:**
```sql
-- TODO: Add index scan example
-- Follows index, fetches rows from heap
```

**Index Only Scan:**
```sql
-- TODO: Add index only scan example
-- All data comes from index
-- Requires covering index or visibility map
```

**Bitmap Index Scan:**
```sql
-- TODO: Add bitmap index scan example
-- Combines multiple indexes
-- Large result sets
```

**Sequential Scan:**
```sql
-- TODO: Add sequential scan example
-- When it's appropriate (small tables, large result sets)
-- When it's a problem (missing indexes)
```

### Forcing Index Usage (Rarely Needed)

```sql
-- TODO: Add examples of influencing query planner
-- SET enable_seqscan = off; (debugging only)
-- Why this is rarely needed
```

## Index Creation Strategies

### CREATE INDEX CONCURRENTLY

```sql
-- TODO: Add CONCURRENT index creation examples
-- Non-blocking index creation
-- Trade-offs: slower, more disk space during creation
-- Required for production databases
```

### Index Creation Performance

```sql
-- TODO: Add index creation optimization tips
-- maintenance_work_mem configuration
-- max_parallel_maintenance_workers (PostgreSQL 11+)
-- Parallel index builds
```

## Common Indexing Patterns

### Foreign Key Indexes

**Always index foreign keys:**
```sql
-- TODO: Add foreign key indexing examples
-- Why this is critical
-- Performance impact of missing FK indexes
```

### Multi-Column Searches

```sql
-- TODO: Add multi-column search patterns
-- Composite indexes for common WHERE clauses
```

### Date Range Queries

```sql
-- TODO: Add date range indexing patterns
-- B-tree indexes on timestamps
-- BRIN for large time-series tables
```

### Text Search

```sql
-- TODO: Add text search indexing
-- GIN indexes for full-text search
-- GIST indexes for trigram matching
-- pg_trgm extension
```

### JSONB Indexing

```sql
-- TODO: Add JSONB indexing examples
-- GIN indexes on JSONB columns
-- jsonb_ops vs jsonb_path_ops
-- Path-specific indexes
```

See [JSONB_PATTERNS.md](./JSONB_PATTERNS.md) for detailed JSONB indexing strategies.

## Anti-Patterns

### Anti-Pattern: Indexing Everything
More indexes = slower writes. Index strategically based on query patterns.

### Anti-Pattern: Wrong Column Order in Composite Indexes
Column order matters. Test and measure performance.

### Anti-Pattern: Not Indexing Foreign Keys
This causes severe performance problems during JOINs and cascades.

### Anti-Pattern: Using SELECT * with Large Indexes
Covering indexes are wasted if you select all columns anyway.

### Anti-Pattern: Never Analyzing Index Usage
Unused indexes waste storage and hurt write performance. Monitor and remove.

### Anti-Pattern: Creating Indexes Without CONCURRENTLY in Production
Non-concurrent index creation locks tables. Always use CONCURRENTLY in production.

### Anti-Pattern: Ignoring Index Bloat
Bloated indexes waste space and slow queries. Monitor and REINDEX when needed.

## Index Design Workflow

1. **Identify slow queries** - pg_stat_statements, application logs
2. **Analyze query plans** - EXPLAIN ANALYZE
3. **Design appropriate indexes** - type, columns, order
4. **Create indexes concurrently** - avoid table locks
5. **Measure performance improvement** - before/after metrics
6. **Monitor ongoing usage** - pg_stat_user_indexes
7. **Remove unused indexes** - periodic cleanup

## Tools and Extensions

### Monitoring Tools
- **pg_stat_statements** - Query performance statistics
- **pganalyze** - Visual query performance insights
- **pgBadger** - Log analyzer

### Index Analysis Extensions
- **pgstattuple** - Index and table bloat statistics
- **pg_trgm** - Trigram matching for text search
- **btree_gist** - B-tree operations in GIST indexes

### Index Management Tools
- **pg_index_watch** - Index usage monitoring
- **Dexter** - Automated index recommendations

## Additional Resources

### Documentation
- PostgreSQL Index Types: https://www.postgresql.org/docs/current/indexes-types.html
- EXPLAIN Guide: https://www.postgresql.org/docs/current/using-explain.html
- Index-Only Scans: https://www.postgresql.org/docs/current/indexes-index-only-scans.html

### Books and Guides
- "Use The Index, Luke" by Markus Winand: https://use-the-index-luke.com/
- "The Art of PostgreSQL" by Dimitri Fontaine

### Related Knowledge Base Articles
- [PostgreSQL Best Practices](./POSTGRESQL_BEST_PRACTICES.md)
- [Query Optimization](./QUERY_OPTIMIZATION.md)
- [JSONB Patterns](./JSONB_PATTERNS.md)
- [Database Design](./DATABASE_DESIGN.md)
