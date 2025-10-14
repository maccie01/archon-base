# API Endpoints Documentation

Created: 2025-10-13
Timestamp: 16:52:00

Comprehensive documentation of all Netzwächter API endpoints, request/response schemas, and frontend-backend integration.

## Documentation Files

### API_OVERVIEW.md
High-level overview of the API architecture including:
- Base configuration (URLs, authentication, rate limiting)
- Authentication approach and user roles
- Common patterns and conventions
- Error handling
- Middleware chain
- Special routes

### ENDPOINTS_BY_MODULE.md
Complete catalog of all API endpoints organized by module:
- 22 backend modules documented
- 120+ endpoints catalogued
- Each endpoint includes: HTTP method, route, authentication requirements, parameters, and response format
- Organized by functional area (admin, auth, objects, energy, monitoring, etc.)

### ENDPOINTS_ALPHABETICAL.md
Quick alphabetical reference of all endpoints:
- Organized A-Z for rapid lookup
- Includes summary statistics
- Documents naming conventions
- Shows HTTP method distribution

### REQUEST_RESPONSE_SCHEMAS.md
Detailed schemas for all request and response formats:
- Common request patterns (authentication, pagination, filtering)
- Common response patterns (success, error, status codes)
- Module-specific schemas for all major entities
- Validation schema references
- Special handling (BigInt, dates, JSON fields)

### FRONTEND_USAGE_MAP.md
Cross-reference between frontend and backend:
- Maps which frontend features call which API endpoints
- Identifies API mismatches and missing endpoints
- Documents path and method mismatches
- Provides recommendations for fixes
- Organized by frontend module

## Quick Statistics

- Total API Endpoints: 120+
- Backend Modules: 22
- Public Endpoints: 10
- Authenticated Endpoints: 110+
- Rate-Limited Endpoints: 7
- Deprecated Endpoints: 1

## Module Summary

1. admin - Database status, settings, portal configuration (18 endpoints)
2. auth - Authentication and session management (5 endpoints)
3. database - Connection pool status (1 endpoint)
4. efficiency - Efficiency analysis (2 endpoints)
5. energy - Energy data and consumption (13 endpoints)
6. export - PDF email export (1 endpoint)
7. health - System health monitoring (3 endpoints)
8. ki-reports - AI-generated reports (1 endpoint)
9. legacy - Deprecated endpoints (1 endpoint)
10. logbook - Logbook entries CRUD (10 endpoints)
11. mandants - Tenant management (4 endpoints)
12. monitoring - Dashboard, alerts, KPIs (7 endpoints)
13. object-groups - Object group management (4 endpoints)
14. objects - Object management (24 endpoints)
15. settings - Application settings (8 endpoints)
16. setup - Setup configuration (1 endpoint)
17. temperature - Temperature data (8 endpoints)
18. todo-tasks - Task management (5 endpoints)
19. user-logs - User activity logging (3 endpoints)
20. user-profiles - User profile management (4 endpoints)
21. users - User management (9 endpoints)
22. weather - Weather data (4 endpoints)

## Key Findings

### API Mismatches
18 endpoints are called by the frontend but not defined in the backend, including:
- Missing monitoring dashboard routes (should redirect)
- Missing energy data endpoints
- Missing object-mandant assignment routes (path mismatch)
- Missing database info/test endpoints

### Path Inconsistencies
- Frontend uses `/api/dashboard/*` but backend defines `/api/monitoring/dashboard/*`
- Frontend uses `/api/object-mandant/*` but backend defines `/api/objects/:id/assignments*`
- Frontend uses query params where backend expects path params

### Method Inconsistencies
- Frontend uses PUT where backend defines PATCH (e.g., coordinates update)

## Authentication & Authorization

### Session-Based Authentication
- Express-session with PostgreSQL store
- Session timeout monitoring
- Automatic session extension via heartbeat

### User Roles
- superadmin: Full system access
- admin: Mandant-level administration
- user: Standard read access

### Protected Routes
- Most routes require authentication via `requireAuth` middleware
- Role checks performed in controllers (not middleware)
- Public routes: weather data, some test endpoints

## Rate Limiting

### Global Rate Limiting
- Applied to all `/api/*` routes
- 10mb request size limit

### Endpoint-Specific Rate Limiting
- Authentication: 5 attempts per 15 minutes
- Export: 10 exports per hour
- Password reset: 3 attempts per hour
- User registration: 5 registrations per hour

## Error Handling

### Standard Error Types
- 400 Bad Request - Validation errors
- 401 Unauthorized - Authentication required
- 403 Forbidden - Insufficient permissions
- 404 Not Found - Resource not found
- 500 Internal Server Error - Server errors
- 503 Service Unavailable - Database connection failed

### Error Response Format
```json
{
  "message": "Error description",
  "error": "Error details"
}
```

## Database Connections

### Primary Database (Portal-DB)
- Environment: `DATABASE_URL`
- Connection pooling: ConnectionPoolManager
- Used for: users, objects, mandants, settings, sessions

### External Energy Database
- Configuration: stored in settings table
- Dynamic connection with stored credentials
- Used for: energy meter readings (view_mon_comp)

## Documentation Maintenance

When adding new endpoints:
1. Update ENDPOINTS_BY_MODULE.md with full endpoint details
2. Add to ENDPOINTS_ALPHABETICAL.md alphabetically
3. Document request/response schemas in REQUEST_RESPONSE_SCHEMAS.md
4. Update FRONTEND_USAGE_MAP.md if frontend uses the endpoint
5. Update statistics in this README

When modifying existing endpoints:
1. Check all documentation files for references
2. Update schemas if request/response format changes
3. Check frontend usage map for breaking changes
4. Update version notes if breaking change

## Related Documentation

- Database Schema: /.archon-knowledge-base/01-database/
- Authentication: /.archon-knowledge-base/03-authentication/
- Frontend Components: /.archon-knowledge-base/04-frontend/
- Backend Architecture: /.archon-knowledge-base/05-backend/

## Notes

- Documentation generated through systematic analysis of backend routes and controllers
- Frontend usage derived from API client files and hooks
- Mismatches identified by comparing frontend API calls with backend route definitions
- No pagination is currently implemented in any endpoints
- All dates use ISO 8601 format
- BigInt values automatically converted to Number in JSON responses
