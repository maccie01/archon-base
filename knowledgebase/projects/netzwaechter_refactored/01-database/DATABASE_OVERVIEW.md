# Database Overview

Created: 2025-10-13

## Database Type

PostgreSQL (Primary relational database)

## Connection Information

### Connection Pool Configuration

The application uses a centralized connection pool manager implemented in `/apps/backend-api/connection-pool.ts`.

**Default Pool Settings:**
- Minimum connections: 5 (configurable via `DB_POOL_MIN`)
- Maximum connections: 20 (configurable via `DB_POOL_MAX`)
- Idle timeout: 30000ms (30 seconds, configurable via `DB_POOL_IDLE_TIMEOUT`)
- Connection timeout: 5000ms (5 seconds, configurable via `DB_CONNECTION_TIMEOUT`)
- TCP keepalive: Enabled (starts after 10 seconds)

**Environment Variables:**
- `DATABASE_URL`: PostgreSQL connection string (required)
- `DB_POOL_MIN`: Minimum persistent connections (default: 5)
- `DB_POOL_MAX`: Maximum concurrent connections (default: 20)
- `DB_POOL_IDLE_TIMEOUT`: Idle connection timeout in milliseconds (default: 30000)
- `DB_CONNECTION_TIMEOUT`: Connection acquisition timeout in milliseconds (default: 5000)

### SSL Configuration

SSL mode is determined by the connection string:
- `sslmode=require` or `sslmode=verify-full`: SSL enforced with certificate validation in production
- `sslmode=prefer` or `sslmode=allow`: SSL preferred, falls back if server doesn't support
- `sslmode=disable`: SSL explicitly disabled (local/development)
- No sslmode parameter: SSL disabled (local databases)

Optional custom CA certificate via `DB_SSL_CERT` environment variable.

## ORM and Migration Tool

**Drizzle ORM** is used for database schema management and queries.

**Configuration File:** `/config/build/drizzle.config.ts`
- Output directory for migrations: `./db/migrations`
- Schema location: `./packages/shared-types/schema.ts`
- Dialect: PostgreSQL

## Connection Pool Features

### Health Monitoring
- Periodic health checks every 30 seconds
- Circuit breaker pattern (opens after 5 consecutive failures, auto-resets after 30 seconds)
- Tracks active connections, error rates, query times
- Health check validates connection with `SELECT 1` query

### Metrics Tracking
- Total queries executed
- Total errors
- Average query time (last 1000 queries)
- Connection pool uptime
- Active/idle/waiting connection counts
- Error rate percentage

### Connection Pre-warming
On initialization, the pool pre-warms minimum connections by:
1. Acquiring the configured minimum number of connections
2. Validating each with a simple query (`SELECT 1`)
3. Releasing connections back to the pool

### Graceful Shutdown
Handles SIGTERM and SIGINT signals:
1. Waits up to 30 seconds for active queries to complete
2. Closes all pool connections
3. Exits cleanly

## Database Architecture

The database follows a multi-tenant architecture with:
- **Mandant-based data isolation**: Primary tenant separation
- **User management**: Role-based access control with profiles
- **Object monitoring**: Central object/asset management
- **Energy data**: Time-series energy consumption and temperature data
- **Maintenance**: Logbook entries and task management
- **Collaboration**: Team annotations and real-time monitoring
- **Automation**: Agent-based data collection and processing
- **Session storage**: PostgreSQL-based session management

## Performance Optimizations

1. **Connection pooling**: Efficient reuse of database connections
2. **Index strategy**: Comprehensive indexes on frequently queried columns
3. **JSONB fields**: Flexible schema for complex nested data
4. **Batch operations**: Support for bulk inserts and updates via Drizzle
5. **Query metrics**: Performance tracking for optimization opportunities

## Monitoring Endpoints

- `GET /api/database/status`: Returns connection pool health status
  - `settingdbOnline`: Database availability
  - `poolStatus.healthy`: Overall pool health
  - `poolStatus.activeConnections`: Current active connections
  - `poolStatus.errorRate`: Error rate percentage
  - `timestamp`: Last check timestamp

## Database Standards Compliance

The schema incorporates German energy monitoring standards:
- GEG 2024 (Gebäudeenergiegesetz)
- DIN V 18599 (Energy efficiency of buildings)
- VDI 3807 (Energy consumption characteristics)

Temperature monitoring includes min/max/mean calculations for heating degree day analysis.
