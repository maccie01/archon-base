# Authentication Overview

Created: 2025-10-13

## Authentication Strategy

The Netzwächter application uses a lightweight session-based authentication system with PostgreSQL session storage.

## Core Components

### 1. Session Management

**Technology Stack:**
- express-session: Session middleware
- connect-pg-simple: PostgreSQL session store adapter
- PostgreSQL: Session storage backend

**Implementation Location:**
- `/apps/backend-api/auth.ts` - Core session setup
- `/apps/backend-api/middleware/auth.ts` - Authentication middleware

### 2. Password Security

**Hashing Algorithm:**
- bcrypt with default salt rounds (10)
- Timing attack prevention using dummy hash comparison

**Implementation:**
- `/apps/backend-api/modules/auth/auth.service.ts` - Password validation

### 3. Dual Authentication System

The system supports two authentication methods:

**A. Superadmin Authentication**
- Plain text password comparison (for system setup)
- Credentials stored in:
  - `/server/setup-app.json` (JSON configuration file)
  - Environment variables: `SUPERADMIN_USERNAME`, `SUPERADMIN_PASSWORD`

**B. Regular User Authentication**
- bcrypt-hashed password comparison
- Credentials stored in PostgreSQL `users` table
- Supports username or email login

## Session Configuration

### Session Store

```typescript
Store: connect-pg-simple (PostgreSQL)
Table: sessions
Pool: ConnectionPoolManager singleton instance
Auto-pruning: Every 15 minutes
```

### Session Settings

```typescript
{
  secret: SESSION_SECRET (env variable)
  store: PostgreSQL session store
  resave: false
  saveUninitialized: false  // No session until login
  rolling: true             // Reset expiration on activity
  name: 'sid'              // Cookie name (not default 'connect.sid')
  cookie: {
    httpOnly: true         // XSS protection
    secure: production     // HTTPS only in production
    maxAge: 24 hours
    sameSite: 'strict' (prod) / 'lax' (dev)
    path: '/'
  }
  proxy: true              // Trust proxy headers
}
```

## Environment Variables

**Required:**
- `SESSION_SECRET` - Session signing secret (min 64 characters)
- `DATABASE_URL` - PostgreSQL connection string

**Optional:**
- `SUPERADMIN_USERNAME` - Superadmin username
- `SUPERADMIN_PASSWORD` - Superadmin password
- `SUPERADMIN_ROLE` - Role identifier (default: 'superadmin')
- `NODE_ENV` - Environment mode (affects cookie security)

## Session Lifecycle

### 1. Session Creation

**Login Endpoints:**
- `POST /api/auth/login` - Regular user login
- `POST /api/auth/superadmin-login` - Superadmin login

**Session Data Structure:**
```typescript
{
  user: {
    id: string
    email: string | null
    firstName: string | null
    lastName: string | null
    role: string | null
    userProfileId: number | null
    mandantId: number | null
    mandantAccess: number[] | null
    sessionStart: number (timestamp)
    lastActivity: number (timestamp)
  }
}
```

### 2. Session Validation

**Checks Performed:**
1. Session exists in PostgreSQL
2. User object exists in session
3. Absolute timeout not exceeded (24 hours from login)
4. Inactivity timeout not exceeded (2 hours from last activity)

### 3. Session Timeouts

**Absolute Timeout:**
- Duration: 24 hours from login
- Action: Force logout, destroy session
- Reason: "absolute_timeout"

**Inactivity Timeout:**
- Duration: 2 hours from last activity
- Action: Force logout, destroy session
- Reason: "inactivity_timeout"

**Activity Extension:**
- Every authenticated request updates `lastActivity` timestamp
- Session cookie `maxAge` resets on activity (rolling: true)

### 4. Session Extension

**Heartbeat Endpoint:**
- `POST /api/auth/heartbeat`
- Updates `lastActivity` timestamp
- Used by frontend to keep session alive during user activity

### 5. Session Termination

**Logout Endpoint:**
- `POST /api/auth/logout`
- Destroys session from PostgreSQL
- Clears session cookie

## Security Features

### 1. Cookie Security

**Protection Mechanisms:**
- `httpOnly: true` - Prevents XSS access to cookies
- `secure: true` - HTTPS-only in production
- `sameSite: 'strict'` - CSRF protection in production
- Custom cookie name - Security through obscurity

### 2. Session Secret Validation

**Startup Checks:**
- Validates SESSION_SECRET length (min 64 characters)
- Warns if using weak or default secret
- Throws error in production if secret is weak

### 3. Connection Security

**Database Connection:**
- Connection pooling via ConnectionPoolManager
- SSL support based on connection string `sslmode` parameter
- Session store error logging

### 4. Timing Attack Prevention

**Password Validation:**
- Dummy bcrypt comparison when user not found
- Prevents timing-based username enumeration

## Performance Considerations

### Session Store Optimization

**Auto-pruning:**
- Expired sessions automatically removed every 15 minutes
- Reduces database bloat

**Connection Pooling:**
- Shared connection pool with main application
- Optimized pool size (5-20 connections)

**Rolling Sessions:**
- Session expiration extends on activity
- Reduces unnecessary re-authentication

## Initialization Flow

```
1. Express app starts
2. initializeAuth() called in routes/index.ts
3. setupAuth() configures session middleware
4. getSession() creates PostgreSQL session store
5. Connection pool initialized (if not already)
6. Session middleware registered on app
7. checkSessionTimeouts middleware added to /api routes
8. Express trust proxy enabled
```

## Related Files

- `/apps/backend-api/auth.ts` - Session setup
- `/apps/backend-api/middleware/auth.ts` - Authentication middleware
- `/apps/backend-api/modules/auth/` - Authentication module
- `/apps/backend-api/connection-pool.ts` - Database connection pool
- `/apps/backend-api/routes/index.ts` - Route initialization
