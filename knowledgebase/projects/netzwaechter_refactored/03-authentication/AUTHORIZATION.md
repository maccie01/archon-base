# Authorization and Access Control

Created: 2025-10-13

## Role System

### Role Hierarchy

```
superadmin (highest privilege)
    ↓
admin
    ↓
user (standard user)
```

### Role Definitions

**superadmin:**
- System-level administrative access
- Can access system setup and configuration
- Bypasses all role checks (acts as wildcard)
- Only accessible via superadmin login endpoint
- Not stored in database (configuration-based)

**admin:**
- Mandant-level administrative access
- User management within mandant
- Object management
- Full dashboard and monitoring access
- Cannot access system setup

**user:**
- Standard user access
- Read-only or limited write access
- Dashboard and monitoring views
- No user or object management

## Permission Model

### User Permissions

Each user has the following permission attributes:

**role:** Base role (superadmin, admin, user)
**mandantId:** Primary mandant association
**mandantAccess:** Array of mandant IDs user can access
**userProfileId:** Links to custom permission profile

### User Profile Sidebar Configuration

User profiles define granular UI permissions:

```typescript
{
  showSystemSetup: boolean      // System configuration access
  showLogbook: boolean           // Logbook access
  showDashboard: boolean         // Dashboard access
  showEnergyData: boolean        // Energy data access
  showNetworkMonitor: boolean    // Network monitoring access
  showUserManagement: boolean    // User management access
  showObjectManagement: boolean  // Object management access
  showGrafanaDashboards: boolean // Grafana dashboard access
  showEfficiencyStrategy: boolean // Efficiency strategy access
}
```

### Default Sidebar Configurations

**Superadmin:**
```typescript
{
  showSystemSetup: true,      // Only superadmin has this
  showLogbook: false,
  showDashboard: false,
  showEnergyData: false,
  showNetworkMonitor: false,
  showUserManagement: false,
  showObjectManagement: false,
  showGrafanaDashboards: false,
  showEfficiencyStrategy: false
}
```

**Admin:**
```typescript
{
  showSystemSetup: false,
  showLogbook: true,
  showDashboard: true,
  showEnergyData: true,
  showNetworkMonitor: true,
  showUserManagement: true,       // Admins can manage users
  showObjectManagement: true,     // Admins can manage objects
  showGrafanaDashboards: true,
  showEfficiencyStrategy: true
}
```

**User:**
```typescript
{
  showSystemSetup: false,
  showLogbook: true,
  showDashboard: true,
  showEnergyData: true,
  showNetworkMonitor: true,
  showUserManagement: false,      // Users cannot manage users
  showObjectManagement: false,    // Users cannot manage objects
  showGrafanaDashboards: true,
  showEfficiencyStrategy: true
}
```

## Authorization Middleware

### 1. requireAuth

**Purpose:** Ensure user is authenticated

**Location:** `/apps/backend-api/middleware/auth.ts`

**Usage:**
```typescript
router.use(requireAuth);
```

**Behavior:**
- Calls isAuthenticated middleware
- Returns 401 if not authenticated
- Continues to next middleware if authenticated

### 2. isAuthenticated

**Purpose:** Core authentication check

**Location:** `/apps/backend-api/auth.ts`

**Behavior:**
```typescript
1. Check session.user exists
2. Check session timeouts (absolute and inactivity)
3. Update lastActivity timestamp
4. Continue if valid, 401 if invalid
```

### 3. validateSession

**Purpose:** Additional session validation

**Location:** `/apps/backend-api/middleware/auth.ts`

**Behavior:**
```typescript
1. Check session exists
2. Check session.user exists
3. Check expires_at if present
4. Return 401 if invalid
```

### 4. requireRole(role)

**Purpose:** Require specific role

**Location:** `/apps/backend-api/middleware/auth.ts`

**Usage:**
```typescript
router.post('/admin-only', requireRole('admin'), handler);
```

**Behavior:**
```typescript
1. Extract user from session
2. If no user → 401 Unauthorized
3. If user.role !== role AND user.role !== 'superadmin' → 403 Forbidden
4. Continue if authorized
```

**Response on failure:**
```json
{
  "message": "Forbidden",
  "error": "Role 'admin' required"
}
```

### 5. requireAdmin

**Purpose:** Convenience middleware for admin role

**Usage:**
```typescript
router.post('/admin-endpoint', requireAdmin, handler);
```

**Behavior:**
- Calls requireRole('admin')
- Superadmin also passes (wildcard)

### 6. requireSuperAdmin

**Purpose:** Convenience middleware for superadmin role

**Usage:**
```typescript
router.post('/system-setup', requireSuperAdmin, handler);
```

**Behavior:**
- Calls requireRole('superadmin')
- Only superadmin passes

### 7. checkSessionTimeouts

**Purpose:** Validate session timeouts on API routes

**Location:** `/apps/backend-api/auth.ts`

**Applied to:** All `/api/*` routes

**Behavior:**
- Checks absolute timeout (24h)
- Checks inactivity timeout (2h)
- Updates lastActivity
- Destroys session if expired

## Authorization Patterns

### Route-Level Protection

**All routes require auth:**
```typescript
const router = Router();
router.use(requireAuth);

router.get('/', controller.getAll);
router.post('/', controller.create);
```

**Mixed protection:**
```typescript
const router = Router();

// Public route
router.get('/public', controller.getPublic);

// Protected routes
router.use(requireAuth);
router.get('/private', controller.getPrivate);
```

**Role-specific routes:**
```typescript
const router = Router();
router.use(requireAuth);

// Admin-only
router.post('/admin', requireAdmin, controller.adminAction);

// User or admin
router.get('/user', controller.userAction);
```

### Controller-Level Checks

Controllers can perform additional authorization:

```typescript
export const controller = {
  async updateUser(req: Request, res: Response) {
    const sessionUser = req.session.user;
    const targetUserId = req.params.id;

    // Users can only update themselves
    if (sessionUser.role !== 'admin' && sessionUser.id !== targetUserId) {
      return res.status(403).json({
        message: "Forbidden"
      });
    }

    // Continue with update...
  }
};
```

## Mandant-Based Access Control

### Mandant Isolation

Users are associated with one or more mandants (tenants):

**mandantId:** Primary mandant (required)
**mandantAccess:** Additional mandants user can access (array)

### Data Filtering

Controllers filter data based on mandant access:

```typescript
// Example: Get users filtered by mandant access
const users = await db
  .select()
  .from(users)
  .where(
    or(
      eq(users.mandantId, sessionUser.mandantId),
      inArray(users.mandantId, sessionUser.mandantAccess || [])
    )
  );
```

### Superadmin Bypass

Superadmin bypasses mandant restrictions:

```typescript
if (sessionUser.role === 'superadmin') {
  // No mandant filter - return all data
  return getAllUsers();
}

// Apply mandant filter for other roles
return getUsersByMandantAccess(sessionUser);
```

## Security Considerations

### Privilege Escalation Prevention

**Superadmin Role Protection:**
- Superadmin cannot be assigned via user creation
- Only accessible through superadmin login
- Not stored in database

**Role Change Protection:**
- User role changes should require admin permission
- Users cannot change their own role

**Mandant Access Validation:**
- Validate mandantId exists before assignment
- Validate user has access to target mandant

### Session Hijacking Prevention

**Cookie Security:**
- httpOnly flag prevents JavaScript access
- secure flag enforces HTTPS in production
- sameSite flag prevents CSRF

**Session Rotation:**
- Session ID rotates on login
- Old session destroyed on logout

### Authorization Error Responses

**401 Unauthorized:**
- No session or invalid session
- Session expired
- Not authenticated

**403 Forbidden:**
- Authenticated but insufficient permissions
- Role check failed
- Mandant access denied

## Testing Authorization

### Test Scenarios

**1. Unauthenticated Access:**
```
Request: GET /api/users
Expected: 401 Unauthorized
```

**2. Insufficient Role:**
```
User: role=user
Request: POST /api/users (admin only)
Expected: 403 Forbidden
```

**3. Superadmin Bypass:**
```
User: role=superadmin
Request: ANY protected endpoint
Expected: 200 OK (passes all role checks)
```

**4. Mandant Isolation:**
```
User: mandantId=5, mandantAccess=[5]
Request: GET /api/objects?mandantId=10
Expected: Empty array or 403 Forbidden
```

## Related Files

- `/apps/backend-api/middleware/auth.ts` - Authorization middleware
- `/apps/backend-api/auth.ts` - Core authentication
- `/apps/backend-api/modules/auth/auth.service.ts` - User profile logic
- `/apps/backend-api/modules/users/users.controller.ts` - User management with role checks
- `/apps/backend-api/modules/admin/admin.routes.ts` - Admin-only routes
