# Multi-Tenancy Database Patterns

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Perplexity research on multi-tenancy patterns 2024, PostgreSQL row-level security, schema isolation strategies

## Overview

Multi-tenancy allows a single application instance to serve multiple customers (tenants) while keeping their data isolated. The choice of multi-tenancy strategy significantly impacts performance, security, maintenance, and cost.

## Core Principles

1. Data isolation is paramount - never leak tenant data
2. Choose strategy based on security, compliance, and scale requirements
3. Balance between isolation and resource efficiency
4. Consider backup and restore complexity
5. Plan for tenant-specific customization needs

## Multi-Tenancy Strategies

### Strategy 1: Shared Database, Shared Schema (tenant_id column)

**Architecture:**
- Single database
- Single schema
- All tenants share tables
- tenant_id/mandant_id column in every table
- Row-level filtering in queries

**Example Schema:**
```sql
-- TODO: Add shared schema example
-- users table with tenant_id
-- Always filtering WHERE tenant_id = ?
```

**Pros:**
- Lowest cost (shared resources)
- Easiest to maintain (single schema)
- Simple to add new tenants
- Efficient resource usage

**Cons:**
- Highest risk of data leakage
- All tenants affected by schema changes
- No tenant-specific customization
- Performance can degrade with many tenants
- Backup/restore is all-or-nothing

**When to use:**
- SaaS with many small tenants
- Low compliance requirements
- Cost-sensitive applications
- Standardized feature set across tenants

**Implementation in Drizzle:**
```typescript
// TODO: Add Drizzle implementation example
// Adding tenant_id foreign key
// Query middleware for automatic filtering
// Type-safe tenant context
```

### Strategy 2: Shared Database, Separate Schemas

**Architecture:**
- Single database
- One schema per tenant
- Each tenant's tables in their own schema
- Application switches schemas per request

**Example Schema:**
```sql
-- TODO: Add separate schemas example
-- tenant_1.users, tenant_2.users, etc.
-- SET search_path TO tenant_1;
```

**Pros:**
- Better data isolation than shared schema
- Tenant-specific customization possible
- Easier per-tenant backup/restore
- Schema-level security possible

**Cons:**
- More complex than shared schema
- Limited by database connection limit
- Schema migrations must run for all tenants
- Performance overhead of switching schemas

**When to use:**
- Medium number of tenants (100s)
- Some tenant-specific customization needed
- Regulatory requirements for logical separation
- Mix of tenant sizes

**Implementation:**
```typescript
// TODO: Add schema switching implementation
// Setting search_path
// Connection pool per tenant
// Migration strategy
```

### Strategy 3: Separate Databases

**Architecture:**
- One database per tenant
- Complete isolation
- Separate connection pools per tenant

**Example:**
```
tenant_1_db
tenant_2_db
tenant_3_db
```

**Pros:**
- Strongest data isolation
- Easiest tenant-specific customization
- Independent backups and restores
- Can scale to different database servers
- Tenant-specific performance tuning possible

**Cons:**
- Highest cost (most resources)
- Complex to maintain (many databases)
- Difficult cross-tenant reporting
- More complex application logic

**When to use:**
- Enterprise customers requiring isolation
- High compliance requirements (HIPAA, SOC2)
- Large tenants with different resource needs
- Need for tenant-specific databases in different regions
- Small number of high-value tenants

**Implementation:**
```typescript
// TODO: Add separate database implementation
// Database connection routing
// Migration strategy for multiple databases
// Cross-tenant reporting challenges
```

## PostgreSQL Row-Level Security (RLS)

### What is RLS?

Row-Level Security provides automatic filtering at the database level based on policies.

**Example:**
```sql
-- TODO: Add RLS policy examples
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY tenant_isolation ON users
--   USING (tenant_id = current_setting('app.current_tenant')::integer);
```

**Benefits:**
- Enforced at database level (even for raw SQL)
- Cannot be bypassed by application bugs
- Reduces code complexity
- Strong security guarantee

**Trade-offs:**
- Performance overhead for policy evaluation
- Complexity in policy management
- Limited ORM support

### RLS with Shared Schema Pattern

```sql
-- TODO: Add complete RLS implementation example
-- Setting tenant context with SET LOCAL
-- Policy creation for all tables
-- Testing policies
```

## Tenant Context Management

### Setting Tenant Context

**Application Level:**
```typescript
// TODO: Add application-level tenant context
// Middleware to extract tenant from request
// Passing tenant to all queries
// Type-safe tenant context
```

**Database Level (with RLS):**
```typescript
// TODO: Add database-level context setting
-- SET LOCAL app.current_tenant = 123;
-- Using in transaction
```

### Drizzle Integration

```typescript
// TODO: Add Drizzle tenant filtering
// Query middleware
// Type-safe tenant filtering
// Automatic tenant_id injection
```

## Migration Strategies

### Shared Schema Migrations

```typescript
// TODO: Add shared schema migration example
// Single migration run
// All tenants updated simultaneously
// Downtime considerations
```

### Per-Schema Migrations

```typescript
// TODO: Add per-schema migration strategy
// Iterate through all tenant schemas
// Rollback strategy
// Progress tracking
```

### Per-Database Migrations

```typescript
// TODO: Add per-database migration strategy
// Parallel vs sequential execution
// Handling failures
// Tenant-specific customizations
```

## Backup and Restore

### Shared Schema Backups

```bash
# TODO: Add shared schema backup commands
# pg_dump entire database
# Cannot restore single tenant
```

### Per-Schema Backups

```bash
# TODO: Add per-schema backup commands
# pg_dump with --schema flag
# Per-tenant restore possible
```

### Per-Database Backups

```bash
# TODO: Add per-database backup commands
# pg_dump per database
# Independent restore
```

## Performance Considerations

### Query Performance

**Shared Schema:**
- Indexes must account for tenant_id
- Composite indexes: (tenant_id, other_columns)
- Partial indexes for active tenants

```sql
-- TODO: Add multi-tenant index examples
-- CREATE INDEX idx_users_tenant_email ON users(tenant_id, email);
```

**Separate Schemas/Databases:**
- Standard single-tenant indexing
- No tenant_id overhead

### Connection Pooling

```typescript
// TODO: Add multi-tenant connection pooling
-- Shared pool (shared schema)
-- Pool per tenant (separate schemas/databases)
-- Dynamic pool sizing
```

## Security Best Practices

### Data Isolation Verification

```sql
-- TODO: Add tenant isolation tests
-- Test queries cannot access other tenant data
-- Automated testing in CI/CD
```

### Preventing Data Leakage

1. Always filter by tenant_id in WHERE clauses
2. Use RLS as defense-in-depth
3. Audit queries accessing multiple tenants
4. Test cross-tenant isolation regularly
5. Use type-safe tenant context

### Tenant Onboarding

```typescript
// TODO: Add tenant provisioning logic
-- Creating new tenant (shared schema)
-- Creating new schema/database
-- Initial data setup
```

### Tenant Offboarding

```typescript
// TODO: Add tenant deletion logic
-- Soft delete vs hard delete
-- Data retention requirements
-- GDPR/compliance considerations
```

## Hybrid Approaches

### Tiered Multi-Tenancy

- Small tenants: shared schema
- Large tenants: separate database

```typescript
// TODO: Add tiered multi-tenancy routing
-- Determining tenant tier
-- Routing to appropriate database
```

### Geographic Distribution

- Regional databases
- Tenant placement by region
- Compliance with data residency requirements

## Monitoring and Observability

### Tenant-Specific Metrics

```sql
-- TODO: Add tenant monitoring queries
-- Per-tenant query performance
-- Per-tenant storage usage
-- Per-tenant connection counts
```

### Cross-Tenant Reporting

```typescript
// TODO: Add cross-tenant aggregation strategies
-- Challenges with separate schemas/databases
-- ETL to data warehouse
-- Materialized views
```

## Common Patterns from Production

### Pattern: mandant_id as Tenant Identifier

Observed in netzwaechter-refactored:
```typescript
// TODO: Add mandant_id pattern details
-- mandant_id in most tables
-- Foreign key to mandants table
-- Used for filtering
```

### Pattern: mandant_access JSONB Array

```typescript
// TODO: Add mandant_access pattern
-- JSONB array of allowed tenant IDs
-- Flexible multi-tenant access
-- Use cases: shared resources across tenants
```

## Anti-Patterns

### Anti-Pattern: Forgetting tenant_id in WHERE Clauses
Catastrophic data leakage. Use RLS or query middleware.

### Anti-Pattern: Using Shared Schema for Regulated Data
High compliance requirements need stronger isolation.

### Anti-Pattern: Not Testing Cross-Tenant Isolation
Always test that tenant A cannot access tenant B's data.

### Anti-Pattern: Hardcoding Tenant Context
Use dependency injection or context passing.

### Anti-Pattern: No Audit Trail for Cross-Tenant Access
Log any queries that access multiple tenants.

## Decision Matrix

| Criteria | Shared Schema | Separate Schemas | Separate Databases |
|----------|---------------|------------------|-------------------|
| Cost | Low | Medium | High |
| Isolation | Low | Medium | High |
| Customization | Hard | Possible | Easy |
| Maintenance | Easy | Medium | Hard |
| Scalability | Good | Good | Excellent |
| Compliance | Basic | Medium | Strong |

## Tools and Libraries

### Multi-Tenancy Libraries
- **node-tenant** - Node.js multi-tenancy library
- **apartment** (Ruby) - Multi-tenancy for Rails

### Monitoring
- Per-tenant metrics in APM tools
- Custom tenant dashboards

## Additional Resources

### Articles
- "Multi-Tenancy Architecture Patterns" (AWS Architecture Blog)
- "Designing Scalable SaaS Applications" (Microsoft Azure)

### Related Knowledge Base Articles
- [Database Design](./DATABASE_DESIGN.md)
- [PostgreSQL Best Practices](./POSTGRESQL_BEST_PRACTICES.md)
- [Database Security](./DATABASE_SECURITY.md)
- [Audit Logging](./AUDIT_LOGGING.md)
- [Drizzle ORM Patterns](./DRIZZLE_PATTERNS.md)
