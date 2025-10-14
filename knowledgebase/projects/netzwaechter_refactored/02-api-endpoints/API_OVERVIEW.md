# API Overview

Created: 2025-10-13
Timestamp: 16:45:00

## Base Configuration

- Base URL: `/api`
- Authentication: Session-based (express-session)
- Rate Limiting: Global rate limiting on `/api/*` routes (10mb request size limit)
- Response Format: JSON

## Authentication Approach

### Session-Based Authentication
- Sessions managed via express-session with PostgreSQL store
- Session timeout monitoring via middleware
- Lightweight authentication without JWT overhead
- Session stored in `req.session.user`

### User Roles
- `superadmin`: Full system access, setup configuration management
- `admin`: Mandant-level administration, can manage users and objects within mandant
- `user`: Standard user with read access to assigned mandants

### Protected Routes
- Most routes require authentication via `requireAuth` middleware
- Public routes: weather data, some test endpoints
- Role-specific routes checked in controllers (not middleware)

## Common Patterns

### Request Authentication
```typescript
const sessionUser = (req as any).session?.user;
if (!sessionUser) {
  throw createAuthError("Benutzer nicht authentifiziert");
}
```

### Mandant-Based Filtering
- Users see only objects/data from their assigned mandant(s)
- Admins can see all data within their mandant
- Superadmins see all data across all mandants

### Error Handling
- Standardized error handling via asyncHandler wrapper
- Error types: createAuthError, createValidationError, createNotFoundError, createDatabaseError
- HTTP status codes: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 500 (Internal Server Error)

### Response Formats
Success responses typically return:
```json
{
  "message": "Success message",
  "data": {...}
}
```

Error responses:
```json
{
  "message": "Error message",
  "error": "Error details"
}
```

## Rate Limiting

### Global Rate Limiting
- Applied to all `/api/*` routes
- Default configuration in middleware/rate-limit.ts

### Endpoint-Specific Rate Limiting
- `authRateLimiter`: 5 failed login attempts per 15 minutes
- `exportRateLimiter`: 10 exports per hour per IP
- `passwordResetRateLimiter`: 3 password resets per hour per IP
- `registrationRateLimiter`: 5 user registrations per hour per IP

## Special Routes

### Health Checks
- `/health`: Application health check (no auth, defined in index.ts)
- `/api/health`: Database and connection pool health check
- `/api/health/pool`: Connection pool statistics
- `/api/health/metrics`: Prometheus-style metrics

### Legacy Routes
- `/startki`: iframe wrapper for KI system (public route)

## API Versioning

Current version: No explicit API versioning
- All endpoints use `/api` prefix
- No version numbers in URLs
- Breaking changes managed through backward compatibility

## Module Organization

Backend API organized into 22 modules:
1. admin - Database status, settings, portal configuration
2. auth - Authentication and session management
3. database - Database connection pool status
4. efficiency - Efficiency analysis reports
5. energy - Energy consumption and meter data
6. export - PDF export via email
7. health - System health monitoring
8. ki-reports - AI-generated reports
9. legacy - Deprecated endpoints (temperature-efficiency-chart)
10. logbook - Logbook entries CRUD
11. mandants - Tenant management
12. monitoring - Dashboard KPIs, alerts, critical systems
13. object-groups - Object group management
14. objects - Object management (facilities/buildings)
15. settings - Application settings management
16. setup - Setup configuration access
17. temperature - Temperature data and efficiency
18. todo-tasks - Task management
19. user-logs - User activity logging
20. user-profiles - User profile management
21. users - User management and authentication
22. weather - Public weather data endpoints

## Common Query Parameters

- `startDate`, `endDate`: ISO date strings for date range filtering
- `timeRange`: Predefined time ranges (e.g., 'last-365-days', '2023', 'last-year')
- `objectId`: Object identifier (integer)
- `mandantId`: Mandant identifier (integer)
- `status`: Status filter (varies by endpoint)
- `priority`: Priority filter (varies by endpoint)
- `limit`: Result limit (integer)

## Common Path Parameters

- `:id`: Primary key identifier (integer)
- `:objectId`: Object identifier (integer or bigint)
- `:objectid`: Object bigint identifier
- `:mandantId`: Mandant identifier (integer)
- `:postalCode`: German postal code (string)

## Database Connections

### Primary Database (Portal-DB)
- Environment variable: `DATABASE_URL`
- Connection pooling via ConnectionPoolManager
- Used for: users, objects, mandants, settings, sessions

### External Energy Database
- Configuration stored in settings table
- Dynamic connection via stored credentials
- Used for: energy meter readings (view_mon_comp)

## Middleware Chain

1. JSON body parser (10mb limit)
2. URL-encoded body parser (10mb limit)
3. Global API rate limiter (`/api/*`)
4. Request logging middleware
5. Session initialization (express-session)
6. Session timeout check (`checkSessionTimeouts`)
7. Route-specific authentication (`requireAuth`)
8. Route-specific rate limiters
9. Request validation (`validateBody`)
10. Controller handler
11. Error handler (global)
12. 404 handler (unmatched routes)
