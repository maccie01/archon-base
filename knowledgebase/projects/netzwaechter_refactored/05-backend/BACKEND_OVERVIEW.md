# Backend Overview - Netzwächter API

Created: 2025-10-13

## Architecture Summary

The Netzwächter backend is an Express.js REST API built with TypeScript, following a modular architecture pattern with 23 feature modules.

## Technology Stack

- **Framework**: Express.js 4.x
- **Language**: TypeScript
- **Database**: PostgreSQL (Primary) + External Energy DB
- **ORM**: Drizzle ORM (partial) + Raw SQL (legacy)
- **Authentication**: Session-based with express-session
- **Validation**: Zod schemas
- **Connection Management**: Custom ConnectionPoolManager singleton

## Application Entry Point

**File**: `/apps/backend-api/index.ts`

### Startup Sequence

1. Enable BigInt JSON serialization
2. Initialize Express app with middleware:
   - `express.json()` with 10mb limit
   - `express.urlencoded()` with 10mb limit
   - API rate limiter (300 req/min)
   - Request logging middleware
3. Initialize database connection (async)
4. Register health check endpoint (`/health`)
5. Register special `/startki` iframe route
6. Setup all API routes via `setupRoutes()`
7. Register global error handler
8. Setup Vite dev server (development) or static serving (production)
9. Start HTTP server on port from `PORT` env variable (default: 3000)
10. Initialize email service
11. Setup graceful shutdown handlers (SIGINT)

## Express Middleware Stack

Applied in this order:

1. **Body Parsers**: JSON and URL-encoded (10mb limit)
2. **Rate Limiting**: `/api` routes limited to 300 req/min
3. **Request Logger**: Logs API requests with duration
4. **Authentication**: Session-based auth (initialized in routes setup)
5. **Session Timeout Checker**: Validates session expiry
6. **Route Handlers**: Module-specific routers
7. **404 Handler**: Catches unmatched `/api/*` routes
8. **Error Handler**: Global error handler (must be last)

## Module Organization

**Location**: `/apps/backend-api/modules/`

### All 23 Modules

1. **admin** - Admin operations and user management
2. **auth** - Authentication and session management
3. **database** - Database status and health checks
4. **efficiency** - Energy efficiency analysis
5. **energy** - Energy consumption data and metrics
6. **export** - Data export functionality
7. **health** - Application health endpoints
8. **ki-reports** - AI-generated reports
9. **legacy** - Legacy API compatibility routes
10. **logbook** - System activity logging
11. **mandants** - Multi-tenant management
12. **monitoring** - System monitoring and KPIs
13. **object-groups** - Object grouping functionality
14. **objects** - Core object management
15. **settings** - Application settings and preferences
16. **setup** - Initial setup and configuration
17. **temperature** - Temperature monitoring
18. **todo-tasks** - Task management
19. **user-logs** - User activity logging
20. **user-profiles** - User profile management
21. **users** - User CRUD operations
22. **weather** - Weather data integration
23. (Implicit) **public routes** - Public API endpoints

## Route Registration

**File**: `/apps/backend-api/routes/index.ts`

### Route Mounting Order

Routes are mounted in this specific order to prevent conflicts:

```typescript
// Public routes first (backward compatibility)
app.use('/api/outdoor-temperatures', weatherRoutes);

// Module routes (alphabetically sorted)
app.use('/api/admin', adminRoutes);
app.use('/api/auth', authRoutes);
app.use('/api', energyRoutes);        // Special: mounted at /api level
app.use('/api', efficiencyRoutes);    // Special: mounted at /api level
app.use('/api/database', databaseRoutes);
// ... (18 more module routes)

// Error handlers
app.use('/api/*', notFoundHandler);   // 404 for unmatched API routes
app.use(errorHandler);                // Global error handler
```

### Important Mounting Notes

- **Energy and Efficiency routes** are mounted AFTER auth routes to prevent their `requireAuth` middleware from catching `/api/auth/*` paths
- Public routes are defined before authenticated routes for backward compatibility
- 404 handler specifically catches `/api/*` to avoid interfering with frontend routes
- Error handler MUST be registered last

## Database Architecture

### Primary Database (Portal-DB)

- **Access Method**: ConnectionPoolManager singleton + Drizzle ORM
- **Connection String**: `DATABASE_URL` environment variable
- **Pool Configuration**:
  - Min connections: 5 (configurable via `DB_POOL_MIN`)
  - Max connections: 20 (configurable via `DB_POOL_MAX`)
  - Idle timeout: 30s
  - Connection timeout: 5s
- **Initialization**: Async via `initializeDatabase()` in `db.ts`

### External Energy Database

- **Access Method**: Dynamic Pool instances created per-request
- **Configuration**: Stored in settings table (category: 'data')
- **Tables**: `view_day_comp`, `view_mon_comp`
- **Usage**: Energy efficiency calculations and consumption data

### Database Access Patterns

**Three patterns exist across the codebase:**

1. **Drizzle ORM** (preferred, modern):
   ```typescript
   const db = getDb();
   const results = await db.select().from(table).where(condition);
   ```

2. **ConnectionPoolManager** (legacy, common):
   ```typescript
   const pool = ConnectionPoolManager.getInstance().getPool();
   const result = await pool.query(sql, params);
   ```

3. **Dynamic Pool** (external databases only):
   ```typescript
   const { Pool } = await import("pg");
   const energyPool = new Pool(externalConfig);
   // Use and then end()
   ```

## Shared Services

### ConnectionPoolManager

**File**: `/apps/backend-api/connection-pool.ts`

Centralized singleton for PostgreSQL connection pooling:

- Health monitoring with circuit breaker
- Metrics tracking (query times, error rates)
- Prometheus-compatible metrics export
- Graceful shutdown handling
- Pre-warming of connections

### Email Service

**File**: `/apps/backend-api/email-service.ts`

- Initialized at startup
- Ensures Portal-DB entry exists
- Used for notifications and alerts

### Frontend Dev Server

**File**: `/apps/backend-api/frontend-dev-server.ts`

- Vite integration for development mode
- Static file serving for production (optional)
- Catch-all route handling

## Environment Configuration

### Required Variables

- `DATABASE_URL` - PostgreSQL connection string
- `PORT` - Server port (default: 3000)
- `NODE_ENV` - Environment (development/production)

### Optional Variables

- `DB_POOL_MIN` - Minimum pool connections (default: 5)
- `DB_POOL_MAX` - Maximum pool connections (default: 20)
- `DB_POOL_IDLE_TIMEOUT` - Idle connection timeout in ms (default: 30000)
- `DB_CONNECTION_TIMEOUT` - Connection acquisition timeout in ms (default: 5000)
- `DB_SSL_CERT` - Custom SSL certificate for database
- `SERVE_STATIC_FROM_BACKEND` - Serve static files in production (default: false)

## API Response Patterns

### Success Responses

- `200 OK` - Successful GET/PUT/DELETE
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE (some endpoints)

### Error Responses

All errors return JSON with:
```typescript
{
  message: string;      // Error message
  status: number;       // HTTP status code
  error?: string;       // Stack trace (development only)
  details?: any;        // Validation error details
}
```

### Common Status Codes

- `400` - Validation error
- `401` - Unauthenticated
- `403` - Forbidden (insufficient permissions)
- `404` - Resource not found
- `429` - Rate limit exceeded
- `500` - Internal server error
- `503` - Service unavailable (database connection failure)

## Performance Optimizations

1. **Connection Pooling**: 5-20 persistent connections (reduced from 50)
2. **Connection Pre-warming**: Minimum connections established at startup
3. **Rate Limiting**: 300 req/min API throttling
4. **Parallel Queries**: Multiple queries executed concurrently where possible
5. **Circuit Breaker**: Automatic failover after 5 consecutive connection failures
6. **Health Checks**: Periodic pool health monitoring (30s interval)

## Logging Strategy

- **Request Logging**: All `/api/*` requests logged with method, path, status, duration
- **Error Logging**: All errors logged with context (user, request details)
- **Health Checks**: Pool health warnings logged
- **Connection Events**: Pool connect/remove events logged

## Security Measures

1. **Rate Limiting**: Multiple rate limiters for different endpoint types
2. **Session-based Authentication**: Express-session with timeout validation
3. **Input Validation**: Zod schemas for request validation
4. **Error Sanitization**: Stack traces hidden in production
5. **SQL Injection Protection**: Parameterized queries
6. **Body Size Limits**: 10mb max request body
7. **CORS**: (Not explicitly configured - relying on same-origin)

## Special Routes

### Health Check
- **Route**: `GET /health`
- **Auth**: None
- **Purpose**: Load balancer health checks
- **Response**: `{ status, timestamp, uptime }`

### StartKI Iframe
- **Route**: `GET /startki`
- **Auth**: None
- **Purpose**: Iframe wrapper for KI system
- **Response**: HTML with iframe

### Public API Routes
- `/api/outdoor-temperatures/*` - Weather data
- `/api/public-daily-consumption/:objectId` - Energy consumption
- `/api/public-monthly-consumption/:objectId` - Monthly consumption
- `/api/monthly-netz/:objectId` - Netz meter data

## Known Patterns and Conventions

1. **Async Handlers**: All route handlers wrapped with `asyncHandler()` for error handling
2. **Session User**: Accessed via `(req as any).session?.user`
3. **Mandant Filtering**: Security pattern for multi-tenant data isolation
4. **BigInt Serialization**: Custom `toJSON()` on BigInt prototype converts to Number
5. **Singleton Pattern**: Used for ConnectionPoolManager, service instances
6. **Module Exports**: Each module exports via `index.ts` for clean imports

## Development vs Production

### Development Mode
- Vite dev server enabled
- Full error stack traces
- Verbose logging
- SSL disabled by default

### Production Mode
- Optional static file serving (via `SERVE_STATIC_FROM_BACKEND`)
- Sanitized error messages
- SSL required for database connections
- Error logging without stack traces

## Graceful Shutdown

Handles SIGINT and SIGTERM signals:

1. Close HTTP server
2. Wait for active connections to complete
3. Shutdown connection pool
4. Exit process

## References

- Main entry: `/apps/backend-api/index.ts`
- Route setup: `/apps/backend-api/routes/index.ts`
- Database: `/apps/backend-api/db.ts`
- Connection pool: `/apps/backend-api/connection-pool.ts`
- Middleware: `/apps/backend-api/middleware/`
- Modules: `/apps/backend-api/modules/`
