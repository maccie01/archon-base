# Database and ORM Best Practices

Created: 2025-10-13
Last Updated: 2025-10-13
Primary Research Sources: Perplexity Research, PostgreSQL Documentation, Drizzle ORM Documentation

## Overview

This directory contains comprehensive, universal best practices for database design and ORM usage that can be applied across all projects. The focus is on PostgreSQL and Drizzle ORM, but many principles apply to other databases and ORMs as well.

## Core Principles

1. Schema design drives performance - thoughtful design prevents future bottlenecks
2. Indexes are powerful but costly - balance read performance with write overhead
3. Normalization vs denormalization depends on access patterns
4. Connection pooling is essential for scalability
5. Security must be built in from the start
6. Regular maintenance (VACUUM, ANALYZE) sustains performance
7. Testing database code is as important as testing application code

## Documentation Structure

### Database Design and Schema
- [Database Design](./DATABASE_DESIGN.md) - Normalization, relationships, constraints, schema design patterns
- [PostgreSQL Best Practices](./POSTGRESQL_BEST_PRACTICES.md) - PostgreSQL-specific features and optimizations
- [Multi-Tenancy Patterns](./MULTI_TENANCY.md) - Tenant isolation strategies (shared schema, separate schemas, separate databases)

### Performance and Optimization
- [Indexing and Optimization](./INDEXING_OPTIMIZATION.md) - B-tree, GIN, GIST, BRIN indexes, query plans
- [Query Optimization](./QUERY_OPTIMIZATION.md) - N+1 prevention, join strategies, subqueries
- [JSONB Patterns](./JSONB_PATTERNS.md) - PostgreSQL JSONB usage, indexing, querying

### ORM and Development
- [Drizzle ORM Patterns](./DRIZZLE_PATTERNS.md) - Drizzle ORM best practices, schema definition, TypeScript integration
- [Schema Migrations](./SCHEMA_MIGRATIONS.md) - Migration strategies, versioning, rollback patterns
- [Transactions](./TRANSACTIONS.md) - Transaction patterns, isolation levels, deadlock prevention

### Operations and Infrastructure
- [Connection Pooling](./CONNECTION_POOLING.md) - Pool configuration, PgBouncer, connection lifecycle
- [Backup and Recovery](./BACKUP_RECOVERY.md) - Backup strategies, point-in-time recovery, disaster recovery
- [Testing Databases](./TESTING_DATABASE.md) - Test database setup, fixtures, seeding, cleanup strategies

### Data Management
- [Soft Delete Patterns](./SOFT_DELETE.md) - Implementing soft deletes, cascading, query filtering
- [Audit Logging](./AUDIT_LOGGING.md) - Change tracking, history tables, temporal tables, compliance

### Security
- [Database Security](./DATABASE_SECURITY.md) - SQL injection prevention, parameterized queries, permissions

### Anti-Patterns
- [Anti-Patterns](./ANTIPATTERNS.md) - Common mistakes to avoid, what NOT to do

## Quick Reference

### PostgreSQL Version Information
The best practices in this knowledge base are based on PostgreSQL 14-17 (2024-2025 features).

Key PostgreSQL 17 improvements:
- Enhanced B-tree index handling for IN clauses
- Improved memory management for VACUUM operations
- Logical replication enhancements
- Better support for identity columns over SERIAL

### Database Technologies Observed in Projects

Based on analysis of projects in /Users/janschubert/code-projects:

**Databases Used:**
- PostgreSQL (primary - production systems)
- SQLite (development, lightweight applications)

**ORMs Used:**
- Drizzle ORM (TypeScript-first, modern approach)
- Some projects may use Prisma (not yet surveyed comprehensively)

**Common Patterns Observed:**
- JSONB for flexible schema sections (settings, metadata, configurations)
- Identity columns over SERIAL for auto-increment primary keys
- Comprehensive indexing on foreign keys and frequently queried columns
- Timestamp tracking (createdAt, updatedAt) on most tables
- Zod schema validation integrated with Drizzle schemas
- Relations defined explicitly in separate sections
- Use of enums stored as VARCHAR for flexibility

## Getting Started

### For New Projects
1. Start with [Database Design](./DATABASE_DESIGN.md) to plan your schema
2. Review [PostgreSQL Best Practices](./POSTGRESQL_BEST_PRACTICES.md) for configuration
3. Follow [Drizzle ORM Patterns](./DRIZZLE_PATTERNS.md) for implementation
4. Implement [Connection Pooling](./CONNECTION_POOLING.md) from day one
5. Set up [Backup and Recovery](./BACKUP_RECOVERY.md) before production

### For Existing Projects
1. Audit current database design against [Anti-Patterns](./ANTIPATTERNS.md)
2. Review [Indexing and Optimization](./INDEXING_OPTIMIZATION.md) for performance wins
3. Check [Query Optimization](./QUERY_OPTIMIZATION.md) for N+1 query issues
4. Ensure [Database Security](./DATABASE_SECURITY.md) measures are in place
5. Implement [Audit Logging](./AUDIT_LOGGING.md) if required for compliance

### For Performance Issues
1. Start with [Query Optimization](./QUERY_OPTIMIZATION.md) - use EXPLAIN ANALYZE
2. Review [Indexing and Optimization](./INDEXING_OPTIMIZATION.md) - missing indexes?
3. Check [PostgreSQL Best Practices](./POSTGRESQL_BEST_PRACTICES.md) - configuration issues?
4. Verify [Connection Pooling](./CONNECTION_POOLING.md) - connection exhaustion?

## Project-Specific Examples

When implementing these patterns in specific projects:
- Current project: `/Users/janschubert/code-projects/monitoring_firma/netzwaechter-refactored`
- Schema reference: `/Users/janschubert/code-projects/monitoring_firma/netzwaechter-refactored/packages/shared-types/schema.ts`

This schema demonstrates many best practices:
- Comprehensive JSONB usage for flexible data structures
- Proper indexing on foreign keys and query columns
- Explicit relations defined
- Zod validation integrated
- TypeScript type safety throughout

## Contributing to This Knowledge Base

When adding or updating documentation:
1. Always include the date created/updated
2. Cite sources (Perplexity research, official docs, production experience)
3. Use the standard structure: Overview, Core Principles, Patterns, Common Mistakes
4. Include skeleton code examples with TODO comments (full examples come later)
5. Focus on UNIVERSAL patterns, not project-specific implementations

## Additional Resources

### Official Documentation
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Drizzle ORM Documentation](https://orm.drizzle.team/)
- [PostgreSQL Wiki](https://wiki.postgresql.org/)

### Community Resources
- [Use The Index, Luke](https://use-the-index-luke.com/) - SQL indexing guide
- [Postgres Weekly](https://postgresweekly.com/) - PostgreSQL news and articles

### Tools
- pgAdmin - PostgreSQL administration
- PgBouncer - Connection pooling
- pg_stat_statements - Query performance analysis
- EXPLAIN ANALYZE - Query execution plans
