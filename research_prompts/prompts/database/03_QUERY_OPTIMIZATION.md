# Research Task: Query Optimization with Drizzle ORM

Created: 2025-10-13
Priority: P1
Estimated Effort: 5-7 hours
Status: Not Started

---

## Objective

Add comprehensive query optimization patterns with before/after examples showing performance improvements.

---

## Context

**Current State**: Structure exists, needs 150+ lines of optimization patterns
**Target**: Performance optimization patterns with benchmarks
**Location**: `knowledgebase/global/03-database-orm/QUERY_OPTIMIZATION.md`

---

## Requirements

### Optimization Topics

1. **Index Strategies**
   - When to add indexes
   - Composite indexes
   - Partial indexes
   - Index maintenance

2. **Query Analysis**
   - Using EXPLAIN ANALYZE
   - Reading query plans
   - Identifying bottlenecks

3. **N+1 Query Prevention**
   - What is N+1 problem
   - Using joins instead of separate queries
   - Eager loading with Drizzle

4. **Caching Strategies**
   - Query result caching
   - Redis integration
   - Cache invalidation

5. **Connection Pooling**
   - Pool configuration
   - Connection limits
   - Pool monitoring

6. **Prepared Statements**
   - How Drizzle uses prepared statements
   - Performance benefits
   - When to use them

7. **Batch Operations**
   - Batch inserts vs single inserts
   - Bulk updates
   - Performance comparisons

8. **JSONB Optimization**
   - GIN indexes on JSONB
   - Efficient JSONB queries
   - When to normalize vs JSONB

---

## Code Examples Required

Each optimization must show:
- ❌ Before (slow query)
- ✅ After (optimized query)
- Performance improvement metrics
- EXPLAIN ANALYZE output comparison

---

## References

- PostgreSQL Performance Tuning
- Drizzle ORM Performance
- Database indexing best practices

---

## Success Criteria

- [ ] 8 optimization patterns with before/after
- [ ] EXPLAIN ANALYZE examples
- [ ] Performance metrics included
- [ ] N+1 query prevention examples
- [ ] Caching strategies
- [ ] 150+ lines added

---

Update: `global/03-database-orm/QUERY_OPTIMIZATION.md`
Tags: ["shared", "database", "performance", "optimization"]

Created: 2025-10-13
