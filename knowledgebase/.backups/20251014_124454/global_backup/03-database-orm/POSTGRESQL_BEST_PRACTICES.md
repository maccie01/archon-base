# PostgreSQL Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Perplexity research on PostgreSQL 2024-2025 best practices, PostgreSQL 17 release notes, production optimization guides

## Overview

PostgreSQL is a powerful, feature-rich open-source database. This document covers PostgreSQL-specific best practices including configuration, memory management, maintenance, and modern features introduced in PostgreSQL 14-17.

## Core Principles

1. Memory configuration directly impacts performance
2. Regular VACUUM and ANALYZE operations are essential
3. Connection pooling is mandatory for production systems
4. Monitor query performance with pg_stat_statements
5. Use PostgreSQL 17+ features (identity columns, improved B-tree indexes)

## PostgreSQL Version Considerations

### PostgreSQL 17 (2025) Key Features
- Enhanced B-tree index handling for IN clauses
- Improved memory management for VACUUM operations
- Better logical replication support
- Identity columns officially recommended over SERIAL
- Performance improvements for high concurrency workloads

### Upgrade Recommendations
- Stay within 2 major versions of current (currently 17)
- Plan for major version upgrades annually
- Test thoroughly in staging before production upgrades
- Use logical replication for zero-downtime upgrades

## Memory Configuration

### Critical Memory Parameters

**shared_buffers:**
- Controls PostgreSQL's main cache for data and indexes
- Recommended: 25% of system RAM for dedicated servers
- Range: 25-40% for read-heavy workloads
- Leave room for OS page cache

```sql
-- TODO: Add configuration example
-- shared_buffers = '8GB' (for 32GB RAM system)
```

**work_mem:**
- Memory for per-operation sorting and hashing
- Multiplies by concurrent operations and connections
- Conservative global setting, increase per-session for heavy queries
- Recommended: Start with 4MB-16MB globally

```sql
-- TODO: Add configuration example
-- work_mem = '8MB' (global default)
-- Then: SET work_mem = '256MB'; (for specific heavy query)
```

**maintenance_work_mem:**
- Memory for VACUUM, CREATE INDEX, ALTER TABLE operations
- Can be set higher than work_mem (doesn't multiply per connection)
- Recommended: 5-10% of RAM, up to 2GB

```sql
-- TODO: Add configuration example
-- maintenance_work_mem = '2GB'
```

**effective_cache_size:**
- Hint to query planner about available cache
- Should be 50-75% of total RAM
- Does NOT allocate memory, just informs planner

```sql
-- TODO: Add configuration example
-- effective_cache_size = '24GB' (for 32GB RAM system)
```

### Configuration Templates

**Small System (4GB RAM):**
```ini
-- TODO: Add small system config template
```

**Medium System (32GB RAM):**
```ini
-- TODO: Add medium system config template
```

**Large System (128GB+ RAM):**
```ini
-- TODO: Add large system config template
```

## Query Performance

### pg_stat_statements Extension

Essential for identifying slow queries and optimization opportunities.

```sql
-- TODO: Add pg_stat_statements setup
-- CREATE EXTENSION pg_stat_statements;
-- Configuration parameters
-- Query examples to find slow queries
```

### EXPLAIN and EXPLAIN ANALYZE

```sql
-- TODO: Add EXPLAIN examples
-- Basic EXPLAIN
-- EXPLAIN ANALYZE (actually runs query)
-- EXPLAIN (ANALYZE, BUFFERS) (shows I/O patterns)
```

### Understanding Query Plans

**Scan Types:**
- Sequential Scan: Full table scan (can be appropriate for small tables)
- Index Scan: Uses index, fetches rows from table
- Index Only Scan: All data comes from index (covering index)
- Bitmap Index Scan: Multiple indexes combined

**Join Types:**
- Nested Loop: Small result sets, indexed joins
- Hash Join: Large result sets, equality joins
- Merge Join: Sorted data, equality joins

**Cost Interpretation:**
```sql
-- TODO: Add cost interpretation guide
-- Startup cost vs total cost
-- Row count estimates vs actuals
-- When estimates are wrong (stale statistics)
```

## Maintenance Operations

### VACUUM

**Purpose:**
- Reclaims storage from dead tuples
- Updates visibility map for index-only scans
- Prevents transaction ID wraparound

**Autovacuum:**
```sql
-- TODO: Add autovacuum configuration
-- autovacuum = on (default)
-- autovacuum_vacuum_threshold
-- autovacuum_vacuum_scale_factor
-- Per-table autovacuum settings
```

**Manual VACUUM:**
```sql
-- TODO: Add manual VACUUM examples
-- VACUUM; -- reclaim space
-- VACUUM FULL; -- reclaim space and compact (requires table lock)
-- VACUUM ANALYZE; -- vacuum + update statistics
```

### ANALYZE

Updates table statistics for query planner:
```sql
-- TODO: Add ANALYZE examples
-- ANALYZE; -- all tables
-- ANALYZE users; -- specific table
-- ANALYZE users(email); -- specific column
```

### REINDEX

Rebuilds indexes to fix bloat and corruption:
```sql
-- TODO: Add REINDEX examples
-- REINDEX INDEX idx_users_email;
-- REINDEX TABLE users;
-- REINDEX DATABASE mydb; (requires exclusive lock)
```

## Monitoring and Statistics

### System Catalogs and Views

**pg_stat_activity:**
```sql
-- TODO: Add pg_stat_activity queries
-- Current connections and queries
-- Long-running queries
-- Blocked queries
```

**pg_stat_user_tables:**
```sql
-- TODO: Add pg_stat_user_tables queries
-- Table access patterns
-- Sequential vs index scans
-- Dead tuple counts
```

**pg_stat_user_indexes:**
```sql
-- TODO: Add pg_stat_user_indexes queries
-- Index usage statistics
-- Unused indexes
-- Index scan counts
```

**pg_statio_user_tables:**
```sql
-- TODO: Add pg_statio_user_tables queries
-- Buffer cache hit ratios
-- I/O patterns
```

### Key Metrics to Monitor

**Database-Level:**
- Connection count
- Transaction rate
- Buffer cache hit ratio (>95% is good)
- Checkpoint frequency
- Replication lag (if using replication)

**Table-Level:**
- Dead tuple percentage
- Table bloat
- Sequential scan ratio
- Last VACUUM/ANALYZE time

**Query-Level:**
- Query execution time (p50, p95, p99)
- Lock wait time
- I/O wait time
- Query execution counts

## Connection Management

### Max Connections

```sql
-- TODO: Add max_connections configuration
-- max_connections = 100 (default, often too low)
-- Consider connection pooling instead of increasing this
```

### Connection Pooling (Required for Production)

See [CONNECTION_POOLING.md](./CONNECTION_POOLING.md) for detailed patterns.

**Why pooling is essential:**
- PostgreSQL connections are heavyweight processes
- Each connection consumes significant memory
- Connection establishment is expensive
- Application connection patterns often spike

**Pooling solutions:**
- PgBouncer (most common)
- pgpool-II
- Application-level pooling (HikariCP, node-postgres pool)

## Backup Strategies

See [BACKUP_RECOVERY.md](./BACKUP_RECOVERY.md) for detailed patterns.

### pg_dump (Logical Backup)

```bash
# TODO: Add pg_dump examples
# Full database dump
# Specific tables
# Custom format vs SQL format
```

### pg_basebackup (Physical Backup)

```bash
# TODO: Add pg_basebackup examples
# Streaming replication backup
# Point-in-time recovery setup
```

### WAL Archiving

```sql
-- TODO: Add WAL archiving configuration
-- archive_mode = on
-- archive_command
-- Point-in-time recovery
```

## Replication

### Streaming Replication

```sql
-- TODO: Add streaming replication setup
-- Primary server configuration
-- Standby server configuration
-- Monitoring replication lag
```

### Logical Replication

```sql
-- TODO: Add logical replication setup
-- Publications
-- Subscriptions
-- Use cases (selective replication, zero-downtime upgrades)
```

## PostgreSQL 17 Specific Features

### Identity Columns

**Preferred over SERIAL:**
```sql
-- TODO: Add identity column examples
-- GENERATED ALWAYS AS IDENTITY
-- GENERATED BY DEFAULT AS IDENTITY
-- Migration from SERIAL to identity
```

### Improved B-tree Indexes for IN Clauses

PostgreSQL 17 optimizes queries with IN clauses using index skip scans:
```sql
-- TODO: Add IN clause optimization examples
-- How skip scans work
-- Performance comparisons
```

### Enhanced Logical Replication

```sql
-- TODO: Add PostgreSQL 17 logical replication features
-- Standby promotion support
-- Improved conflict resolution
```

## Security Configuration

See [DATABASE_SECURITY.md](./DATABASE_SECURITY.md) for detailed patterns.

### pg_hba.conf

```conf
# TODO: Add pg_hba.conf examples
# Host-based authentication rules
# scram-sha-256 vs md5
# Trust, peer, password authentication
```

### SSL/TLS Configuration

```sql
-- TODO: Add SSL configuration
-- ssl = on
-- Certificate setup
-- Enforcing SSL for connections
```

### Row-Level Security (RLS)

```sql
-- TODO: Add RLS examples
-- CREATE POLICY
-- Multi-tenant isolation
-- User-based access control
```

## Common Mistakes

### Anti-Pattern: Not Using Connection Pooling
Production systems need connection pooling. Period.

### Anti-Pattern: Using Default Configuration
PostgreSQL's default configuration is for small systems. Tune for your workload.

### Anti-Pattern: Ignoring Autovacuum
Letting tables bloat destroys performance. Monitor and tune autovacuum.

### Anti-Pattern: No Monitoring
You can't optimize what you don't measure. Set up pg_stat_statements.

### Anti-Pattern: Running as Superuser
Applications should never connect as superuser. Create role-specific users.

### Anti-Pattern: Not Testing Backups
Untested backups are not backups. Test restore procedures regularly.

## Tools and Libraries

### Administration Tools
- **pgAdmin** - GUI administration tool
- **psql** - Command-line interface
- **Drizzle Studio** - Visual schema browser for Drizzle projects

### Monitoring Tools
- **pganalyze** - Query performance insights
- **pgDash** - Dashboard and monitoring
- **Datadog Database Monitoring** - Commercial solution
- **Prometheus + postgres_exporter** - Open-source metrics

### Connection Pooling
- **PgBouncer** - Lightweight connection pooler
- **pgpool-II** - Connection pooling and load balancing

### Backup Tools
- **pgBackRest** - Advanced backup solution
- **Barman** - Backup and recovery manager
- **WAL-G** - Archival and restoration tool

## Additional Resources

### Official Documentation
- PostgreSQL 17 Release Notes: https://www.postgresql.org/docs/17/release-17.html
- PostgreSQL Performance Tips: https://wiki.postgresql.org/wiki/Performance_Optimization
- PostgreSQL Server Configuration: https://www.postgresql.org/docs/current/runtime-config.html

### Community Resources
- Postgres Weekly: https://postgresweekly.com/
- Planet PostgreSQL: https://planet.postgresql.org/
- PostgreSQL Slack Community

### Books
- "PostgreSQL: Up and Running" by Regina Obe and Leo Hsu
- "Mastering PostgreSQL 15" by Hans-Jürgen Schönig

### Related Knowledge Base Articles
- [Database Design](./DATABASE_DESIGN.md)
- [Indexing and Optimization](./INDEXING_OPTIMIZATION.md)
- [Connection Pooling](./CONNECTION_POOLING.md)
- [Backup and Recovery](./BACKUP_RECOVERY.md)
- [Database Security](./DATABASE_SECURITY.md)
