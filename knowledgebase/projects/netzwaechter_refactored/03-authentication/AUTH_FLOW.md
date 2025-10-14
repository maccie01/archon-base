# Authentication Flow

Created: 2025-10-13

## Login Flow

### 1. Superadmin Login

**Endpoint:** `POST /api/auth/superadmin-login`

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Flow:**
```
1. Request arrives at authController.superadminLogin
2. Validate credentials are present
3. authService.validateSuperadminCredentials() checks:
   a. Load superadmin config from setup-app.json
   b. Check username/password match
   c. If not found, check environment variables
4. If valid:
   a. Create superadmin session data
   b. Set session.user object
   c. Initialize sessionStart and lastActivity timestamps
   d. Prepare response with user profile
5. Return success response
```

**Session Created:**
```typescript
{
  user: {
    id: 'superadmin',
    email: 'superadmin@system.local',
    firstName: 'Super',
    lastName: 'Admin',
    role: 'superadmin',
    userProfileId: null,
    mandantId: null,
    mandantRole: 'superadmin',
    sessionStart: 1697203200000,
    lastActivity: 1697203200000
  }
}
```

**Response:**
```json
{
  "message": "Superadmin erfolgreich angemeldet",
  "user": {
    "id": "superadmin",
    "email": "superadmin@system.local",
    "firstName": "Super",
    "lastName": "Admin",
    "role": "superadmin",
    "userProfileId": null,
    "mandantId": null
  }
}
```

### 2. Regular User Login

**Endpoint:** `POST /api/auth/login`

**Request:**
```json
{
  "username": "user@example.com",
  "password": "securePassword123"
}
```

**Flow:**
```
1. Request arrives at authController.userLogin
2. Validate credentials are present
3. authService.validateCredentials() performs:
   a. Check if superadmin (fallback if using wrong endpoint)
   b. authRepository.findUserByUsernameOrEmail()
   c. bcrypt.compare(password, user.password)
   d. Timing attack prevention if user not found
4. If valid:
   a. Create user session data
   b. Set session.user object
   c. Initialize sessionStart and lastActivity timestamps
   d. Fetch user profile if userProfileId exists
   e. Prepare response with user profile and mandant data
5. Return success response
```

**Session Created:**
```typescript
{
  user: {
    id: 'user-uuid',
    email: 'user@example.com',
    firstName: 'John',
    lastName: 'Doe',
    role: 'admin',
    userProfileId: 1,
    mandantId: 5,
    mandantAccess: [5, 10, 15],
    sessionStart: 1697203200000,
    lastActivity: 1697203200000
  }
}
```

**Response:**
```json
{
  "message": "Erfolgreich angemeldet",
  "user": {
    "id": "user-uuid",
    "email": "user@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "role": "admin",
    "userProfileId": 1,
    "mandantId": 5,
    "mandantAccess": [5, 10, 15]
  }
}
```

## Session Validation Flow

### Authenticated Request

**Flow:**
```
1. Request to protected endpoint (e.g., GET /api/users)
2. requireAuth middleware or isAuthenticated middleware triggered
3. Check session exists: req.session?.user
4. If no user in session → 401 Unauthorized
5. checkSessionTimeouts middleware (on /api routes):
   a. Calculate time since sessionStart
   b. Calculate time since lastActivity
   c. If absolute timeout exceeded (24h) → destroy session, 401
   d. If inactivity timeout exceeded (2h) → destroy session, 401
   e. Update lastActivity timestamp
6. Continue to next middleware/controller
```

### Session Timeout Check (Detailed)

**Absolute Timeout Check:**
```typescript
const absoluteTimeout = 24 * 60 * 60 * 1000; // 24 hours
const now = Date.now();

if (now - sessionUser.sessionStart > absoluteTimeout) {
  req.session.destroy();
  return res.status(401).json({
    message: "Session expired",
    reason: "absolute_timeout"
  });
}
```

**Inactivity Timeout Check:**
```typescript
const inactivityTimeout = 2 * 60 * 60 * 1000; // 2 hours
const now = Date.now();

if (now - sessionUser.lastActivity > inactivityTimeout) {
  req.session.destroy();
  return res.status(401).json({
    message: "Session expired",
    reason: "inactivity_timeout"
  });
}
```

**Activity Update:**
```typescript
sessionUser.lastActivity = Date.now();
```

## Get Current User Flow

**Endpoint:** `GET /api/auth/me`

**Flow:**
```
1. Request arrives at authController.getCurrentUser
2. Extract session.user from request
3. If no session → 401 Unauthorized
4. If superadmin:
   a. Return superadmin profile configuration
5. If regular user:
   a. authRepository.getUserProfile(userProfileId)
   b. Build response with profile and mandant data
   c. Apply default sidebar configuration if no profile
6. Return complete user data
```

**Response:**
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "role": "admin",
  "userProfileId": 1,
  "mandantId": 5,
  "userProfile": {
    "id": 1,
    "name": "Default Admin",
    "startPage": "/dashboard",
    "sidebar": {
      "showSystemSetup": false,
      "showLogbook": true,
      "showDashboard": true,
      "showEnergyData": true,
      "showNetworkMonitor": true,
      "showUserManagement": true,
      "showObjectManagement": true,
      "showGrafanaDashboards": true,
      "showEfficiencyStrategy": true
    }
  }
}
```

## Heartbeat Flow

**Endpoint:** `POST /api/auth/heartbeat`

**Purpose:** Keep session alive by updating activity timestamp

**Flow:**
```
1. Request arrives at authController.heartbeat
2. Check session.user exists → 401 if not
3. Update session.user.lastActivity = Date.now()
4. Update session.lastActivity = Date.now()
5. Session middleware automatically extends cookie maxAge
6. Return success response
```

**Response:**
```json
{
  "message": "Session extended",
  "timestamp": "2025-10-13T12:34:56.789Z"
}
```

## Logout Flow

**Endpoint:** `POST /api/auth/logout`

**Flow:**
```
1. Request arrives at authController.logout
2. Extract session from request
3. Call session.destroy():
   a. Remove session from PostgreSQL sessions table
   b. Clear session cookie from client
4. Return success response
```

**Response:**
```json
{
  "message": "Logged out successfully"
}
```

## Session Lifecycle Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         LOGIN                                │
│  POST /api/auth/login or /api/auth/superadmin-login        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│            Session Created in PostgreSQL                     │
│  - sessionStart = now                                        │
│  - lastActivity = now                                        │
│  - cookie sent to client (sid)                               │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              AUTHENTICATED REQUESTS                          │
│  - Client sends cookie with each request                     │
│  - Middleware validates session                              │
│  - Updates lastActivity on each request                      │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
         ┌────────┴────────┐
         │                 │
         ▼                 ▼
┌────────────────┐  ┌──────────────────┐
│   HEARTBEAT    │  │  SESSION TIMEOUT │
│  (Optional)    │  │                  │
│ Every N mins   │  │ Absolute: 24h   │
│ Extends session│  │ Inactivity: 2h  │
└────────┬───────┘  └────────┬─────────┘
         │                   │
         │                   ▼
         │          ┌──────────────────┐
         │          │  FORCE LOGOUT    │
         │          │ Destroy session  │
         │          └──────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                       LOGOUT                                 │
│  POST /api/auth/logout                                       │
│  - Destroy session                                           │
│  - Clear cookie                                              │
└─────────────────────────────────────────────────────────────┘
```

## Frontend Integration

### Login Flow (Frontend)

```typescript
// Login request
const response = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username, password })
});

if (response.ok) {
  const { user } = await response.json();
  // Store user in frontend state
  // Redirect to start page
}
```

### Session Maintenance

```typescript
// Heartbeat to keep session alive
setInterval(async () => {
  await fetch('/api/auth/heartbeat', { method: 'POST' });
}, 5 * 60 * 1000); // Every 5 minutes
```

### Current User Fetch

```typescript
// Get current user on app load
const response = await fetch('/api/auth/me');
if (response.ok) {
  const user = await response.json();
  // Update frontend state
} else {
  // Redirect to login
}
```

## Error Handling

### Common Error Responses

**401 Unauthorized:**
```json
{
  "message": "Unauthorized"
}
```

**401 Session Expired:**
```json
{
  "message": "Session expired",
  "reason": "absolute_timeout"
}
```
or
```json
{
  "message": "Session expired",
  "reason": "inactivity_timeout"
}
```

**401 Invalid Credentials:**
```json
{
  "message": "Ungültige Anmeldedaten"
}
```

**429 Rate Limited:**
```json
{
  "error": "Too many login attempts from this IP. Please try again in 15 minutes.",
  "code": "AUTH_RATE_LIMIT_EXCEEDED",
  "retryAfter": "15 minutes"
}
```
