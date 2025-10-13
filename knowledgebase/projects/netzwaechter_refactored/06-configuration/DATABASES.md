# Database Configuration

Documentation for all databases, connection configuration, and data persistence in the Netzwächter project.

Created: 2025-10-13
Last Updated: 2025-10-13

---

## Overview

The Netzwächter application uses PostgreSQL as its primary database, hosted on Neon's serverless PostgreSQL platform. All data persistence, session storage, and transactional operations are handled through PostgreSQL.

---

## Primary Database: PostgreSQL

### Database Provider

**Provider:** Neon (Serverless PostgreSQL)
**Technology:** PostgreSQL 15+
**Connection:** `@neondatabase/serverless` driver

**Benefits:**
- Serverless architecture (auto-scaling)
- Automatic backups
- Point-in-time recovery
- Branching support
- Global edge network

### Database Information

**Database Name:** `netzwaechter`
**Access:** Via `DATABASE_URL` environment variable
**ORM:** Drizzle ORM
**Migration Tool:** Drizzle Kit

### Connection String Format

```
postgresql://username:password@host:port/database?sslmode=MODE
```

**Components:**
- `username` - Database user
- `password` - User password
- `host` - Database server hostname
- `port` - Database port (default: 5432)
- `database` - Database name
- `sslmode` - SSL mode (require/prefer/disable)

**Example:**
```
postgresql://user:pass@ep-cool-name-123456.us-east-2.aws.neon.tech:5432/netzwaechter?sslmode=require
```

---

## Connection Pool Configuration

### Connection Pool Manager

**File:** `apps/backend-api/connection-pool.ts`
**Class:** `ConnectionPoolManager`
**Driver:** `pg` (node-postgres)

### Pool Settings

| Setting | Environment Variable | Default | Purpose |
|---------|---------------------|---------|---------|
| Min Connections | `DB_POOL_MIN` | 5 | Persistent connections |
| Max Connections | `DB_POOL_MAX` | 20 | Maximum concurrent |
| Idle Timeout | `DB_POOL_IDLE_TIMEOUT` | 30000ms | Close idle after 30s |
| Connection Timeout | `DB_CONNECTION_TIMEOUT` | 5000ms | Acquire timeout |
| Keep Alive | N/A | true | TCP keepalive |
| Keep Alive Delay | N/A | 10000ms | Start after 10s |

### Pool Optimization

**Before Optimization:**
- Min connections: 50
- Max connections: 50
- Idle timeout: Never
- Resource usage: High

**After Optimization:**
- Min connections: 5 (90% reduction)
- Max connections: 20 (60% reduction)
- Idle timeout: 30s (auto-cleanup)
- Resource usage: Low

**Benefits:**
- Auto-scaling between 5-20 based on demand
- Idle connections automatically closed
- Significant resource savings
- Better performance under variable load

### Pool Features

#### 1. Health Monitoring
- Periodic health checks (every 30s)
- Connection validation queries
- Error rate tracking
- Performance metrics

#### 2. Circuit Breaker
- Opens after 5 consecutive failures
- Prevents cascade failures
- Auto-resets after 30s
- Graceful degradation

#### 3. Metrics & Monitoring
- Total/active/idle connection counts
- Query execution times
- Error tracking
- Prometheus-compatible metrics

#### 4. Graceful Shutdown
- Waits for active queries (max 30s)
- Closes connections cleanly
- SIGTERM/SIGINT handling

### Connection Pool Usage

**Initialize:**
```typescript
import { ConnectionPoolManager } from './connection-pool';

const poolManager = ConnectionPoolManager.getInstance();
await poolManager.initialize();
```

**Execute Query:**
```typescript
const result = await poolManager.query(
  'SELECT * FROM objects WHERE id = $1',
  [objectId]
);
```

**Get Pool Stats:**
```typescript
const stats = poolManager.getStats();
console.log(`Active connections: ${stats.activeConnections}`);
```

**Health Check:**
```typescript
const health = await poolManager.healthCheck();
console.log(`Pool healthy: ${health.healthy}`);
```

---

## SSL/TLS Configuration

### SSL Modes

| Mode | Description | Use Case | Encryption |
|------|-------------|----------|------------|
| `require` | SSL required, fail if unavailable | Production | Yes |
| `prefer` | Use SSL if available, fallback | Development | Maybe |
| `disable` | Never use SSL | Local dev only | No |
| `verify-ca` | SSL with CA verification | High security | Yes |
| `verify-full` | SSL with full verification | Maximum security | Yes |

### SSL Configuration by Environment

#### Development
```bash
DATABASE_URL=postgresql://...?sslmode=prefer
```
- SSL optional
- Allows local development
- No certificate verification

#### Production
```bash
DATABASE_URL=postgresql://...?sslmode=require
```
- SSL enforced
- Encrypted connections
- Rejects unencrypted

### SSL Certificate Verification

**Custom CA Certificate:**
```bash
# Environment variable
DB_SSL_CERT=/path/to/ca-cert.pem

# Pool configuration (automatic)
ssl: {
  rejectUnauthorized: true,
  ca: process.env.DB_SSL_CERT
}
```

**Certificate Validation:**
```bash
openssl s_client -connect host:5432 -starttls postgres
```

---

## Database Schema

### ORM: Drizzle

**Package:** `drizzle-orm@0.39.1`
**Dialect:** PostgreSQL
**Schema File:** `packages/shared-types/schema.ts`

### Schema Organization

#### Core Tables
- `users` - User accounts
- `user_profiles` - User access profiles
- `mandants` - Multi-tenant organizations
- `sessions` - Express sessions (connect-pg-simple)

#### Business Data
- `objects` - Monitored energy objects
- `object_groups` - Object grouping
- `object_mandant` - Object-tenant associations

#### Energy Data
- `day_comp` - Daily energy consumption
- `view_mon_comp` - Monthly aggregation (view)
- `daily_outdoor_temperatures` - Weather data

#### Monitoring & Alerts
- `system_alerts` - System alerts
- `logbook_entries` - Maintenance log
- `todo_tasks` - Task management

#### Collaboration
- `collaboration_annotations` - Team annotations
- `annotation_reactions` - Annotation engagement
- `annotation_subscriptions` - Notification subscriptions

#### Automation
- `agents` - Data collection agents
- `agent_logs` - Agent execution logs

#### Configuration
- `settings` - System/user/tenant settings
- `user_activity_logs` - Activity tracking

### Key Data Types

| Type | Usage | Example |
|------|-------|---------|
| `bigint` | Large IDs (objectid) | 123456789012345 |
| `jsonb` | Flexible data structures | {config: {...}} |
| `timestamp` | Date/time with timezone | 2025-01-15 14:30:00+00 |
| `decimal` | Precise numbers | 12345.67 |
| `varchar` | Text with length limit | varchar(255) |
| `text` | Unlimited text | Long descriptions |

### Indexes

**Optimized for:**
- Object lookups by objectid
- Time-series queries (energy data)
- Mandant filtering
- Full-text search (where applicable)
- Composite indexes for common queries

---

## Database Migrations

### Migration System

**Tool:** Drizzle Kit
**Config:** `config/build/drizzle.config.ts`
**Directory:** `db/migrations/`

### Configuration

```typescript
// drizzle.config.ts
export default defineConfig({
  out: "./db/migrations",
  schema: "./packages/shared-types/schema.ts",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL
  }
});
```

### Migration Commands

**Generate Migration:**
```bash
pnpm drizzle-kit generate
```

**Push Schema:**
```bash
pnpm db:push
```

**Inspect Database:**
```bash
pnpm drizzle-kit introspect
```

---

## Session Storage

### Implementation

**Package:** `connect-pg-simple@10.0.0`
**Table:** `sessions`
**Storage:** PostgreSQL (same database)

### Session Table Schema

```sql
CREATE TABLE sessions (
  sid VARCHAR PRIMARY KEY,
  sess JSONB NOT NULL,
  expire TIMESTAMP NOT NULL
);

CREATE INDEX IDX_session_expire ON sessions(expire);
```

### Session Configuration

**Settings:**
- Cookie max age: 24 hours
- Inactivity timeout: 2 hours
- Absolute timeout: 24 hours
- Automatic cleanup: Yes

**Security:**
- HTTP-only cookies
- Secure flag (production)
- SameSite: strict (production)
- Signed with SESSION_SECRET

**Benefits:**
- Persistent sessions across restarts
- Shared state in multi-instance deployments
- Automatic expiration
- Database transaction consistency

---

## Data Import Scripts

### Weather Data Import

**Script:** `apps/backend-api/scripts/importWeatherData.ts`
**Purpose:** Import historical weather data
**Source:** DWD (Deutscher Wetterdienst) via Bright Sky API
**Command:**
```bash
pnpm run import:weather
```

**Daily Update:**
```bash
pnpm run weather:daily
```

### Report Data Migration

**Script:** `apps/backend-api/scripts/populateReportData.ts`
**Purpose:** Populate report data
**Command:**
```bash
pnpm run migrate:reports
```

---

## Database Performance

### Query Optimization

**Strategies:**
1. Connection pooling (5-20 connections)
2. Prepared statements (parameterized queries)
3. Index optimization
4. Query result caching
5. Lazy loading

### Monitoring Metrics

**Available Metrics:**
- Active connections
- Query execution times
- Error rates
- Pool wait times
- Connection acquisition time

**Prometheus Endpoint:**
```typescript
const metrics = poolManager.getPrometheusMetrics();
// Exposes pool metrics in Prometheus format
```

### Performance Recommendations

**Query Best Practices:**
1. Use parameterized queries ($1, $2, etc.)
2. Fetch only required columns
3. Limit result sets
4. Use indexes for WHERE clauses
5. Avoid N+1 queries

**Connection Management:**
1. Release connections promptly
2. Use connection pool
3. Handle errors properly
4. Monitor pool stats
5. Tune pool size for workload

---

## Database Security

### Access Control

**Network Security:**
- Neon provides built-in firewall
- SSL/TLS encryption required in production
- Connection pooling limits concurrent access
- IP whitelisting (if configured)

**Authentication:**
- Strong passwords (12+ characters)
- Unique credentials per environment
- Regular password rotation (180 days)
- No shared credentials

**Authorization:**
- Database user has full access to schema
- Row-level security (future consideration)
- Audit logging (user_activity_logs table)

### Data Encryption

**In Transit:**
- TLS 1.2+ for all connections
- SSL mode: require (production)
- Certificate verification

**At Rest:**
- Neon provides encryption at rest
- Automatic backups encrypted
- Point-in-time recovery encrypted

### Backup & Recovery

**Automatic Backups:**
- Neon performs automatic backups
- Point-in-time recovery available
- Retention period: 7-30 days (plan dependent)

**Manual Backups:**
```bash
pg_dump $DATABASE_URL > backup.sql
```

**Restore:**
```bash
psql $DATABASE_URL < backup.sql
```

---

## Multi-Tenancy

### Tenant Isolation

**Strategy:** Shared database with tenant ID filtering
**Table:** `mandants`
**ID Field:** `mandant_id` in most tables

### Data Segregation

**Tables with Tenant Isolation:**
- `users` - via `mandant_id`
- `objects` - via `mandant_id` and `mandant_access` JSONB
- `settings` - via `mandant_id`
- `agents` - via `mandant_id`

**Access Control:**
- Users can only access their mandant's data
- Filter queries by `mandant_id`
- Application-level enforcement
- Database constraints (foreign keys)

### Tenant Configuration

**Per-Tenant Settings:**
- System configuration (settings table)
- User access profiles
- Object access permissions
- Custom branding (future)

---

## Database Maintenance

### Regular Tasks

**Daily:**
- Monitor connection pool health
- Check error rates
- Review slow queries

**Weekly:**
- Analyze table statistics
- Review index usage
- Check disk usage

**Monthly:**
- Rotate passwords (if scheduled)
- Review access logs
- Optimize queries
- Update statistics

### Health Checks

**Connection Health:**
```typescript
const health = await poolManager.healthCheck();
if (!health.healthy) {
  console.error('Database unhealthy:', health);
}
```

**Database Status:**
```sql
SELECT version();  -- PostgreSQL version
SELECT current_database();  -- Current database
SELECT pg_database_size(current_database());  -- Database size
```

---

## Troubleshooting

### Connection Issues

**Symptom:** Cannot connect to database

**Checks:**
1. Verify DATABASE_URL is set
2. Check network connectivity
3. Verify credentials
4. Check SSL mode
5. Review Neon dashboard status

**Solutions:**
```bash
# Test connection
psql $DATABASE_URL -c "SELECT 1;"

# Check SSL
psql $DATABASE_URL -c "SHOW ssl;"

# Verify pool health
curl http://localhost:5000/api/health
```

### Pool Exhaustion

**Symptom:** "Timeout acquiring connection"

**Causes:**
- Too many concurrent requests
- Connections not released
- Pool size too small
- Slow queries blocking pool

**Solutions:**
1. Increase `DB_POOL_MAX`
2. Optimize slow queries
3. Review connection release logic
4. Monitor pool metrics

### Performance Issues

**Symptom:** Slow queries

**Diagnosis:**
```sql
-- Find slow queries
SELECT query, mean_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Check missing indexes
SELECT schemaname, tablename, indexname
FROM pg_indexes
WHERE schemaname = 'public';
```

**Solutions:**
1. Add appropriate indexes
2. Optimize query structure
3. Use EXPLAIN ANALYZE
4. Review connection pool stats

---

## Database Limits

### Neon Limits

**Free Tier:**
- 1 project
- 10 branches
- 3 GB storage
- 100 simultaneous connections
- Compute auto-suspend after 5 min

**Pro Tier:**
- Unlimited projects
- Unlimited branches
- Unlimited storage
- 1000+ simultaneous connections
- Configurable compute limits

### Application Limits

**Connection Pool:**
- Min: 5 connections
- Max: 20 connections
- Configurable via environment variables

**Recommended Settings:**
- Development: 5-10 connections
- Production: 10-20 connections
- Scale based on load

---

## References

### Internal Documentation
- `apps/backend-api/connection-pool.ts` - Pool implementation
- `packages/shared-types/schema.ts` - Database schema
- `.env.example` - Configuration template

### External Resources
- [Neon Documentation](https://neon.tech/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Drizzle ORM](https://orm.drizzle.team/)
- [node-postgres](https://node-postgres.com/)
- [connect-pg-simple](https://github.com/voxpelli/node-connect-pg-simple)
