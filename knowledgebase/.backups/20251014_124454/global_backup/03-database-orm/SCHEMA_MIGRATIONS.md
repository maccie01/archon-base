# Schema Migration Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Perplexity research on database migrations 2024, zero-downtime deployment strategies, migration tools comparison

## Overview

Schema migrations manage database structure changes over time. Proper migration strategy prevents data loss, minimizes downtime, and enables safe deployments.

## Core Principles

1. Migrations are append-only - never edit existing migrations
2. Test migrations on production-sized data before deployment
3. Always have a rollback plan
4. Make migrations backward-compatible when possible
5. Version control your migrations
6. Run migrations as part of deployment pipeline

## Migration Tools

### Drizzle Kit

```typescript
// TODO: Add Drizzle Kit migration workflow
# drizzle-kit generate
# drizzle-kit migrate
# drizzle-kit push (for development)
```

### Migration File Structure

```
# TODO: Add migration file structure example
# Sequential numbering
# Descriptive names
# SQL vs TypeScript migrations
```

## Migration Patterns

### Additive Changes (Safe)

```sql
# TODO: Add safe migration examples
# Adding columns (with defaults)
# Adding tables
# Adding indexes (CONCURRENTLY)
```

### Destructive Changes (Dangerous)

```sql
# TODO: Add destructive migration handling
# Removing columns (multi-step process)
# Renaming columns (expand/contract pattern)
# Changing column types
```

## Zero-Downtime Migrations

### Expand/Contract Pattern

```sql
# TODO: Add expand/contract pattern
# Phase 1: Add new column
# Phase 2: Dual-write to both columns
# Phase 3: Backfill data
# Phase 4: Switch reads to new column
# Phase 5: Remove old column
```

### Adding Columns with Defaults

```sql
# TODO: Add column with default pattern
# PostgreSQL 11+ optimization
# Avoiding full table rewrite
```

### Online Index Creation

```sql
# TODO: Add CONCURRENTLY index creation
# Non-blocking index builds
# Handling failures
```

## Rollback Strategies

### Writing Reversible Migrations

```sql
# TODO: Add up/down migration pattern
# Testing rollback procedures
# Backward compatibility
```

### Data Migrations

```sql
# TODO: Add data migration patterns
# Backfilling data
# Batch processing for large tables
# Progress tracking
```

## Testing Migrations

### Testing on Production-Sized Data

```bash
# TODO: Add migration testing workflow
# Restore production snapshot
# Run migration
# Measure duration
# Verify data integrity
```

### Automated Migration Tests

```typescript
# TODO: Add automated migration tests
# Schema validation
# Data integrity checks
```

## Common Migration Scenarios

### Adding a Foreign Key

```sql
# TODO: Add foreign key addition steps
# 1. Add column (nullable)
# 2. Backfill data
# 3. Add NOT NULL constraint
# 4. Add foreign key constraint
```

### Splitting a Table

```sql
# TODO: Add table split pattern
# Creating new table
# Migrating data
# Updating application code
```

### Changing Column Type

```sql
# TODO: Add type change pattern
# Create new column
# Migrate data
# Switch reads
# Remove old column
```

## Additional Resources

### Documentation
- Drizzle Kit: https://orm.drizzle.team/kit-docs/overview

### Related Knowledge Base Articles
- [Drizzle ORM Patterns](./DRIZZLE_PATTERNS.md)
- [PostgreSQL Best Practices](./POSTGRESQL_BEST_PRACTICES.md)
- [Database Design](./DATABASE_DESIGN.md)
