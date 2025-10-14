# Protected Routes

Created: 2025-10-13

## Route Protection Overview

This document catalogs all API endpoints and their authentication/authorization requirements.

## Public Routes (No Authentication Required)

### Health Check
- `GET /health` - Server health status
- `GET /api/health` - API health check

### Database Status
- `GET /api/database/status` - Database connection status (public for monitoring)

### Weather Data
- `GET /api/outdoor-temperatures` - Public outdoor temperature data

### Energy Data (Testing Endpoints)
- `GET /api/public-daily-consumption/:objectId` - Public daily consumption
- `GET /api/public-monthly-consumption/:objectId` - Public monthly consumption
- `GET /api/monthly-netz/:objectId` - Public monthly network data

### Frontend
- `GET /startki` - Special iframe wrapper route
- `GET /*` - Vite dev server / static files (development/production)

## Authentication Routes

All authentication routes are public (unauthenticated users need to access them to login).

**Protected by Rate Limiting:** 5 failed attempts per 15 minutes per IP

- `POST /api/auth/login` - Regular user login (Rate Limited: authRateLimiter)
- `POST /api/auth/superadmin-login` - Superadmin login (Rate Limited: authRateLimiter)
- `POST /api/auth/logout` - Logout (requires session)
- `GET /api/auth/me` - Get current user (requires session)
- `POST /api/auth/heartbeat` - Session heartbeat (requires session)

## Protected Routes by Module

### Admin Routes

**Base Path:** `/api/admin`
**Protection:** All routes require authentication (`requireAuth`)
**Additional:** Role checks performed in controllers

#### Database Management
- `GET /api/admin/database/status` - Database status (authenticated)
- `GET /api/admin/objects` - Get all objects (admin view)
- `GET /api/admin/mandants` - Get all mandants
- `GET /api/admin/settings` - Get all settings
- `POST /api/admin/settings` - Save setting
- `GET /api/admin/dashboard/kpis` - Dashboard KPIs

#### Portal Configuration
- `GET /api/admin/portal/config` - Portal configuration
- `GET /api/admin/portal/fallback-config` - Fallback config
- `POST /api/admin/portal/save-fallback-config` - Save fallback config
- `POST /api/admin/portal/test-connection` - Test database connection
- `GET /api/admin/portal/load-config/:configType` - Load config by type
- `POST /api/admin/portal/test-config/:configType` - Test config
- `POST /api/admin/portal/save-config/:configType` - Save config
- `POST /api/admin/portal/activate-config` - Activate config
- `GET /api/admin/portal/active-config` - Get active config

### Users Routes

**Base Path:** `/api/users`
**Protection:** All routes require authentication (`requireAuth`)

#### User CRUD
- `GET /api/users/` - Get all users (filtered by mandant access)
- `GET /api/users/:id` - Get single user
- `POST /api/users/` - Create user (Rate Limited: registrationRateLimiter, 5/hour)
- `PATCH /api/users/:id` - Update user (validated: updateUserSchema)
- `DELETE /api/users/:id` - Delete user

#### Password Management
- `POST /api/users/:id/change-password` - Change password (Rate Limited: passwordResetRateLimiter, 3/hour)

#### User Profiles
- `GET /api/users/profiles/list` - Get all user profiles
- `POST /api/users/profiles` - Create user profile
- `PUT /api/users/profiles/:id` - Update user profile
- `DELETE /api/users/profiles/:id` - Delete user profile

### User Profiles Routes

**Base Path:** `/api/user-profiles`
**Protection:** All routes require authentication (`requireAuth`)

- `GET /api/user-profiles/` - Get all user profiles
- `GET /api/user-profiles/:id` - Get specific profile
- `POST /api/user-profiles/` - Create profile
- `PUT /api/user-profiles/:id` - Update profile
- `DELETE /api/user-profiles/:id` - Delete profile

### Mandants Routes

**Base Path:** `/api/mandants`
**Protection:** All routes require authentication (`requireAuth`)

- `GET /api/mandants/` - Get all mandants (filtered by access)
- `GET /api/mandants/:id` - Get specific mandant
- `POST /api/mandants/` - Create mandant
- `PUT /api/mandants/:id` - Update mandant
- `DELETE /api/mandants/:id` - Delete mandant

### Objects Routes

**Base Path:** `/api/objects`
**Protection:** All routes require authentication (`requireAuth`)

- `GET /api/objects/` - Get all objects (filtered by mandant access)
- `GET /api/objects/:id` - Get specific object
- `POST /api/objects/` - Create object
- `PUT /api/objects/:id` - Update object
- `DELETE /api/objects/:id` - Delete object
- `GET /api/objects/:id/meters` - Get meters for object
- `GET /api/objects/:id/energy-data` - Get energy data for object

### Object Groups Routes

**Base Path:** `/api/object-groups`
**Protection:** All routes require authentication (`requireAuth`)

- `GET /api/object-groups/` - Get all object groups
- `GET /api/object-groups/:id` - Get specific group
- `POST /api/object-groups/` - Create group
- `PUT /api/object-groups/:id` - Update group
- `DELETE /api/object-groups/:id` - Delete group

### Energy Routes

**Base Path:** `/api/energy`
**Protection:** Mixed (public test endpoints + authenticated routes)

#### Public Routes
- `GET /api/public-daily-consumption/:objectId` - Public daily consumption
- `GET /api/public-monthly-consumption/:objectId` - Public monthly consumption
- `GET /api/monthly-netz/:objectId` - Public monthly network data

#### Authenticated Routes
**All routes below require authentication (`requireAuth`)**

- `GET /api/energy/day-comp/:objectId` - Day compensation data
- `POST /api/energy/day-comp` - Create day compensation data
- `GET /api/energy/day-comp/:objectId/latest` - Latest day compensation
- `GET /api/energy/daily-consumption/:objectId` - Daily consumption stats
- `GET /api/energy/daily-consumption-data/:objectId` - Daily consumption by meter
- `GET /api/energy/external/:objectId` - External energy data
- `GET /api/energy/all-meters/:objectId` - Energy data for all meters
- `GET /api/energy/specific-meter/:meterId/:objectId` - Specific meter data
- `GET /api/energy/object/:objectId` - Object energy data

### Efficiency Routes

**Base Path:** `/api/efficiency`
**Protection:** Mixed (public test endpoint + authenticated routes)

#### Public Routes
- `GET /api/efficiency/test` - Test efficiency calculations

#### Authenticated Routes
**All routes below require authentication (`requireAuth`)**

- `GET /api/efficiency/strategies` - Get efficiency strategies
- `POST /api/efficiency/strategies` - Create strategy
- `GET /api/efficiency/strategies/:id` - Get specific strategy
- `PUT /api/efficiency/strategies/:id` - Update strategy
- `DELETE /api/efficiency/strategies/:id` - Delete strategy

### Temperature Routes

**Base Path:** `/api/temperature`
**Protection:** All routes require authentication (`requireAuth`)

- `GET /api/temperature/outdoor` - Get outdoor temperatures
- `GET /api/temperature/outdoor/:objectId` - Outdoor temps for object
- `POST /api/temperature/outdoor` - Record outdoor temperature

### Monitoring Routes

**Base Path:** `/api/monitoring`
**Protection:** All routes require authentication (`requireAuth`)

- `GET /api/monitoring/status` - Get monitoring status
- `GET /api/monitoring/alerts` - Get alerts
- `POST /api/monitoring/alerts` - Create alert
- `PUT /api/monitoring/alerts/:id` - Update alert
- `DELETE /api/monitoring/alerts/:id` - Delete alert

### Logbook Routes

**Base Path:** `/api/logbook`
**Protection:** All routes require authentication (`requireAuth`)

- `GET /api/logbook/entries` - Get logbook entries
- `POST /api/logbook/entries` - Create entry
- `PUT /api/logbook/entries/:id` - Update entry
- `DELETE /api/logbook/entries/:id` - Delete entry

### Todo Tasks Routes

**Base Path:** `/api/todo-tasks`
**Protection:** All routes require authentication (`requireAuth`)

- `GET /api/todo-tasks/` - Get all tasks
- `POST /api/todo-tasks/` - Create task
- `PUT /api/todo-tasks/:id` - Update task
- `DELETE /api/todo-tasks/:id` - Delete task

### Settings Routes

**Base Path:** `/api/settings`
**Protection:** All routes require authentication (`requireAuth`)

- `GET /api/settings/` - Get all settings
- `GET /api/settings/:category/:key` - Get specific setting
- `POST /api/settings/` - Save setting
- `PUT /api/settings/:id` - Update setting
- `DELETE /api/settings/:id` - Delete setting

### Setup Config Routes

**Base Path:** `/api/setup-config`
**Protection:** All routes require authentication (`requireAuth`)

- `GET /api/setup-config/` - Get setup configuration
- `POST /api/setup-config/save` - Save setup configuration
- `POST /api/setup-config/test` - Test configuration

### Export Routes

**Base Path:** `/api/export`
**Protection:** All routes require authentication (`requireAuth`)
**Additional:** Rate limited (10 exports per hour per IP)

- `GET /api/export/energy/:objectId` - Export energy data (Rate Limited: exportRateLimiter)
- `GET /api/export/users` - Export users (Rate Limited: exportRateLimiter)
- `GET /api/export/objects` - Export objects (Rate Limited: exportRateLimiter)

### KI Reports Routes

**Base Path:** `/api/ki-reports`
**Protection:** All routes require authentication (`requireAuth`)

- `GET /api/ki-reports/` - Get all KI reports
- `POST /api/ki-reports/generate` - Generate KI report
- `GET /api/ki-reports/:id` - Get specific report
- `DELETE /api/ki-reports/:id` - Delete report

### User Logs Routes

**Base Path:** `/api/user-logs` or `/api/user-activity-logs`
**Protection:** All routes require authentication (`requireAuth`)

- `GET /api/user-logs/` - Get user activity logs
- `POST /api/user-logs/` - Create log entry
- `GET /api/user-logs/:userId` - Get logs for specific user

### Legacy Routes

**Base Path:** `/api/legacy`
**Protection:** All routes require authentication (`requireAuth`)

- Various legacy endpoints for backward compatibility

### Weather Routes

**Base Path:** `/api/outdoor-temperatures`
**Protection:** Public (no authentication required)

- `GET /api/outdoor-temperatures` - Get outdoor temperatures

## Route Protection Patterns

### Pattern 1: All Routes Protected

Most common pattern - all routes in module require authentication:

```typescript
const router = Router();

// Protect all routes
router.use(requireAuth);

// All routes below are protected
router.get('/', controller.getAll);
router.post('/', controller.create);
```

**Modules using this pattern:**
- Users
- Mandants
- Objects
- Object Groups
- Temperature
- Monitoring
- Logbook
- Todo Tasks
- Settings
- Setup Config
- KI Reports
- User Logs
- Legacy
- User Profiles
- Admin (all routes)

### Pattern 2: Mixed Public/Protected

Public routes defined first, then authentication applied:

```typescript
const router = Router();

// Public routes
router.get('/public-endpoint', controller.publicHandler);

// Protected routes
router.use(requireAuth);
router.get('/protected-endpoint', controller.protectedHandler);
```

**Modules using this pattern:**
- Energy (public test endpoints)
- Efficiency (public test endpoint)

### Pattern 3: Role-Based Protection

Additional role checks on top of authentication:

```typescript
const router = Router();
router.use(requireAuth);

// Admin-only routes
router.post('/admin-action', requireAdmin, controller.adminHandler);

// Superadmin-only routes
router.get('/system-setup', requireSuperAdmin, controller.superAdminHandler);

// All authenticated users
router.get('/user-action', controller.userHandler);
```

**Modules using this pattern:**
- Admin (controller-level role checks)
- Users (role checks in controller logic)

### Pattern 4: Rate-Limited Protection

Additional rate limiting on top of authentication:

```typescript
const router = Router();
router.use(requireAuth);

// Rate-limited routes
router.post('/create', registrationRateLimiter, controller.create);
router.post('/change-password', passwordResetRateLimiter, controller.changePassword);
```

**Modules using this pattern:**
- Users (password reset, registration)
- Export (data exports)
- Auth (login endpoints)

## Special Route Behaviors

### Mandant Filtering

Routes that return data filtered by user's mandant access:
- `/api/users/` - Users filtered by mandantAccess
- `/api/objects/` - Objects filtered by mandantId
- `/api/mandants/` - Mandants filtered by access rights

### Superadmin Bypass

Superadmin role bypasses:
- Mandant filtering (sees all data)
- All role checks (acts as wildcard)
- User profile restrictions

### Session Extension

Routes that extend session activity:
- All authenticated routes update `lastActivity` timestamp
- `/api/auth/heartbeat` - Explicit session extension

## Error Responses

### 401 Unauthorized

**Scenarios:**
- No session cookie
- Session expired (absolute or inactivity timeout)
- Invalid session
- Session not in database

**Response:**
```json
{
  "message": "Unauthorized"
}
```

or

```json
{
  "message": "Session expired",
  "reason": "absolute_timeout" | "inactivity_timeout"
}
```

### 403 Forbidden

**Scenarios:**
- Authenticated but insufficient role
- Mandant access denied
- User trying to access other user's data

**Response:**
```json
{
  "message": "Forbidden",
  "error": "Role 'admin' required"
}
```

### 429 Too Many Requests

**Scenarios:**
- Rate limit exceeded
- Too many login attempts
- Too many exports

**Response:**
```json
{
  "error": "Too many login attempts from this IP. Please try again in 15 minutes.",
  "code": "AUTH_RATE_LIMIT_EXCEEDED",
  "retryAfter": "15 minutes"
}
```

### 404 Not Found

**Scenarios:**
- Route does not exist
- Caught by notFoundHandler middleware

**Response:**
```json
{
  "message": "Not Found",
  "path": "/api/invalid-route"
}
```

## Middleware Application Order

```
1. express.json() - Parse JSON bodies
2. express.urlencoded() - Parse URL-encoded bodies
3. apiRateLimiter - Rate limit all /api routes (300 req/min)
4. Logging middleware - Log request/response
5. setupAuth() - Initialize session middleware
6. checkSessionTimeouts - Check session validity on /api routes
7. Module routes:
   - Public routes (if any)
   - requireAuth - Authentication check
   - Route-specific middleware (rate limiters, validators)
   - Controller handlers
8. notFoundHandler - 404 for unmatched API routes
9. errorHandler - Global error handler
```

## Testing Protected Routes

### Test Unauthenticated Access

```bash
curl -X GET http://localhost:3000/api/users
# Expected: 401 Unauthorized
```

### Test Authenticated Access

```bash
# 1. Login
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user@example.com","password":"password"}' \
  -c cookies.txt

# 2. Use session cookie
curl -X GET http://localhost:3000/api/users \
  -b cookies.txt
# Expected: 200 OK with user list
```

### Test Role Restrictions

```bash
# Login as regular user
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user@example.com","password":"password"}' \
  -c cookies.txt

# Try admin endpoint
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","email":"new@example.com"}' \
  -b cookies.txt
# Expected: 200 OK if admin, 403 Forbidden if regular user
```

### Test Rate Limiting

```bash
# Attempt login 6 times rapidly
for i in {1..6}; do
  curl -X POST http://localhost:3000/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username":"wrong","password":"wrong"}'
done
# Expected: 429 Too Many Requests on 6th attempt
```

## Summary Statistics

**Total Routes:** ~100+ endpoints
**Public Routes:** 7 endpoints
**Protected Routes:** 90+ endpoints
**Rate-Limited Routes:** 8 endpoints
**Role-Specific Routes:** Varies by controller logic

**Protection Methods:**
- Session-based authentication: 90+ routes
- Rate limiting: 8 routes
- Role checks: Varies by controller
- Mandant filtering: 10+ routes

## Related Files

- `/apps/backend-api/routes/index.ts` - Main route configuration
- `/apps/backend-api/middleware/auth.ts` - Authentication middleware
- `/apps/backend-api/middleware/rate-limit.ts` - Rate limiting
- `/apps/backend-api/modules/*/` - Individual module routes
