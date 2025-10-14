# Database Documentation

Created: 2025-10-13

## Overview

This directory contains comprehensive documentation of the Netzwächter database schema, relationships, and configuration.

## Documentation Files

### 1. DATABASE_OVERVIEW.md
High-level database architecture and configuration information:
- Database type (PostgreSQL)
- Connection pool configuration and management
- ORM setup (Drizzle)
- SSL configuration
- Health monitoring and metrics
- Performance optimizations
- German energy monitoring standards compliance

### 2. SCHEMA_TABLES.md
Complete table-by-table documentation including:
- 20 data tables + 1 view
- Column definitions (name, type, nullable, defaults)
- Purpose and description for each table
- JSONB structure definitions
- Tables organized by functional domain:
  - Authentication & Sessions (1 table)
  - User Management (3 tables)
  - Tenant Management (1 table)
  - Object Management (4 tables)
  - Energy & Temperature Data (3 tables)
  - Maintenance & Tasks (2 tables)
  - System Configuration (1 table)
  - Collaboration Features (3 tables)
  - Automation (2 tables)
  - Activity Logging (1 table)

### 3. RELATIONSHIPS.md
Foreign key relationships and data connections:
- Entity relationship diagrams (text-based)
- 30+ foreign key relationships documented
- Cascade delete behavior
- Multi-tenant data isolation strategy
- Self-referencing relationships
- Many-to-many relationships
- Orphan prevention strategies

### 4. INDEXES_CONSTRAINTS.md
Index and constraint documentation:
- 72+ total indexes (20 PK + 4 unique + 48 secondary)
- 5 composite indexes for optimized queries
- Primary key definitions
- Unique constraints
- Index coverage analysis
- Performance recommendations
- JSONB indexing considerations
- NOT NULL and DEFAULT constraints

## Quick Reference

### Database Technology Stack
- **Database:** PostgreSQL
- **ORM:** Drizzle ORM
- **Connection Pool:** Custom ConnectionPoolManager (pg library)
- **Schema Location:** `/packages/shared-types/schema.ts`
- **Config File:** `/config/build/drizzle.config.ts`
- **Pool Manager:** `/apps/backend-api/connection-pool.ts`

### Key Statistics
- **Total Tables:** 21 (20 tables + 1 view)
- **Total Indexes:** 72+ (including PK, unique, and secondary)
- **JSONB Columns:** 35+ flexible schema fields
- **Foreign Key Relationships:** 30+
- **Composite Indexes:** 5

### Connection Pool Defaults
- Minimum connections: 5
- Maximum connections: 20
- Idle timeout: 30 seconds
- Connection timeout: 5 seconds
- Health check interval: 30 seconds

## Database Architecture Highlights

### Multi-Tenant Design
- **Primary isolation:** `mandantId` foreign keys
- **Secondary isolation:** `mandantAccess` JSONB arrays
- **Junction table:** `object_mandant` (deprecated, redundant)

### Time-Series Data
- **Daily aggregation:** `day_comp` table
- **Monthly view:** `view_mon_comp` (PostgreSQL view)
- **Temperature data:** `daily_outdoor_temperatures` (German standards)

### Collaboration Features
- **Annotations:** Real-time team monitoring with threading
- **Reactions:** Team engagement on annotations
- **Subscriptions:** Notification preferences

### Automation
- **Agents:** Configurable data collection and processing
- **Agent logs:** Execution history and metrics
- **Sources:** API, database, file, InfluxDB2, MQTT

### Flexible Schema
35+ JSONB columns provide flexible data structures for:
- Object monitoring data (energy, temperature, alarms)
- User permissions and settings
- Agent configurations
- Annotation metadata
- Attachment information

## Performance Characteristics

### Optimized for
- Multi-tenant filtering (indexed mandantId fields)
- Time-series queries (composite time + object indexes)
- Location-based queries (postal code, city indexes)
- Status filtering (status field indexes)
- Collaboration queries (context, creator, status indexes)
- Audit trail queries (composite resource indexes)

### Connection Pool Features
- Circuit breaker pattern (failure protection)
- Pre-warming (faster initial queries)
- Health monitoring (automatic checks)
- Graceful shutdown (data integrity)
- Prometheus metrics (observability)

## Data Standards Compliance

### German Energy Monitoring Standards
- **GEG 2024:** Gebäudeenergiegesetz (Building Energy Act)
- **DIN V 18599:** Energy efficiency of buildings
- **VDI 3807:** Energy consumption characteristics

Temperature monitoring includes:
- Daily min/max/mean temperatures
- Heating degree day calculations
- DWD (German Weather Service) data integration via Bright Sky API

## Schema Evolution

### Migration Strategy
- Drizzle Kit for schema migrations
- Output directory: `./db/migrations`
- Schema source: Single source of truth in `packages/shared-types/schema.ts`

### Deprecated Features
- `object_mandant` table: Superseded by `objects.mandantAccess` JSONB field
- Still exists for backward compatibility but marked as redundant

## Access Patterns

### Common Query Patterns
1. **Tenant-filtered object lists:** `objects.mandantId IN user.mandantAccess`
2. **Time-series energy data:** `day_comp WHERE log = objectid AND time BETWEEN...`
3. **Object maintenance history:** `logbook_entries WHERE objectId = ? ORDER BY createdAt DESC`
4. **User activity audit:** `user_activity_logs WHERE userId = ? ORDER BY timestamp DESC`
5. **Collaboration context:** `collaboration_annotations WHERE contextType = ? AND contextId = ?`
6. **Agent scheduling:** `agents WHERE status = 'active' AND nextRun <= NOW()`

### Index Support
All common query patterns above are fully supported by indexes for optimal performance.

## Development Guidelines

### Adding New Tables
1. Define schema in `packages/shared-types/schema.ts`
2. Add Drizzle relations if applicable
3. Create insert schema with Zod validation
4. Export TypeScript types
5. Add indexes for foreign keys and filtered columns
6. Document in `SCHEMA_TABLES.md`
7. Document relationships in `RELATIONSHIPS.md`
8. Run Drizzle migrations

### Adding Indexes
1. Identify slow queries via EXPLAIN ANALYZE
2. Add indexes to frequently filtered/joined columns
3. Consider composite indexes for multi-column queries
4. Document in `INDEXES_CONSTRAINTS.md`
5. Monitor index usage and size

### JSONB Best Practices
1. Use JSONB for flexible, nested data structures
2. Define TypeScript types for JSONB structure
3. Consider GIN indexes for containment queries
4. Use B-tree indexes for specific path queries
5. Document JSONB structure in schema table documentation

## Monitoring & Maintenance

### Health Endpoints
- `GET /api/database/status`: Connection pool health and metrics

### Metrics Available
- Active/idle/waiting connections
- Total queries executed
- Error rate percentage
- Average query time
- Pool uptime
- Circuit breaker status

### Maintenance Tasks
1. Regular VACUUM to prevent bloat
2. ANALYZE for statistics updates
3. Monitor slow query logs
4. Review index usage
5. Check connection pool health
6. Rotate logs and old data

## Security Considerations

### Connection Security
- SSL/TLS encryption for production (sslmode=require)
- Connection pooling prevents connection exhaustion
- Circuit breaker prevents cascade failures

### Data Security
- Multi-tenant isolation via foreign keys and JSONB arrays
- User activity logging for audit trails
- Session storage in database (not memory)
- Password hashing (application layer)

### Access Control
- Role-based access via `users.role`
- Profile-based permissions via `user_profiles.sidebar`
- Tenant-based isolation via `mandantId` and `mandantAccess`

## Backup & Recovery

### Backup Strategy (Not Defined in Code)
Recommended approach:
1. Regular PostgreSQL dumps (pg_dump)
2. Point-in-time recovery (WAL archiving)
3. Replica for read scaling
4. Off-site backup storage

### Recovery Testing
Regular testing of backup restoration is recommended.

## Future Considerations

### Potential Optimizations
1. Add missing indexes on `system_alerts` table
2. Consider JSONB indexes for frequently queried paths
3. Materialized views for complex aggregations
4. Partitioning for time-series tables (day_comp, agent_logs)
5. Read replicas for analytics workloads

### Scaling Strategies
1. Connection pool tuning based on load
2. Horizontal scaling via read replicas
3. Vertical scaling for write-heavy workloads
4. Table partitioning for large time-series data
5. Archive old data to separate tables/databases

## Contact & Support

For questions about the database schema or documentation:
1. Review the documentation files in this directory
2. Check the schema source: `packages/shared-types/schema.ts`
3. Consult Drizzle ORM documentation for ORM-specific questions
4. Review PostgreSQL documentation for database-specific features

---

**Documentation Version:** 1.0
**Last Updated:** 2025-10-13
**Schema Location:** `/packages/shared-types/schema.ts`
**Total Documentation Pages:** 4
