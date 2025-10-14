# Security Features

Created: 2025-10-13

## Password Security

### Hashing Algorithm

**Algorithm:** bcrypt
**Default Rounds:** 10 (2^10 = 1024 iterations)
**Implementation:** `/apps/backend-api/modules/auth/auth.service.ts`

**Password Hashing:**
```typescript
const hashedPassword = await bcrypt.hash(password, 10);
```

**Password Verification:**
```typescript
const isValid = await bcrypt.compare(password, user.password);
```

### Timing Attack Prevention

**Problem:** Attackers can determine if username exists by measuring response time

**Solution:** Dummy hash comparison when user not found

```typescript
async validateUserCredentials(username: string, password: string) {
  const user = await authRepository.findUserByUsernameOrEmail(username);

  if (!user || !user.password) {
    // Perform dummy comparison to prevent timing attacks
    await bcrypt.compare(
      password,
      '$2b$12$dummy.hash.to.prevent.timing.attacks.xxxxxxxxxxxxxxxxxxxxx'
    );
    return null;
  }

  const isValid = await bcrypt.compare(password, user.password);
  return isValid ? user : null;
}
```

**Result:** Response time is consistent whether user exists or not

### Password Requirements

**Current Implementation:**
- No explicit password complexity requirements in backend
- Validation handled by shared-validation package
- Minimum length enforced by validation schema

**Location:** `/packages/shared-validation/src/index.ts`

**Recommendations:**
- Minimum 8 characters
- Mix of uppercase, lowercase, numbers, special characters
- Password strength meter on frontend
- Password history to prevent reuse

## Session Security

### Session Configuration

**Session Secret:**
- **Required:** Minimum 64 characters
- **Validation:** Checked at startup
- **Production:** Throws error if weak or missing
- **Development:** Warns but allows weak secret

**Secret Validation:**
```typescript
const sessionSecret = process.env.SESSION_SECRET;
if (!sessionSecret ||
    sessionSecret === 'your-session-secret-here' ||
    sessionSecret.length < 64) {
  console.error('SESSION_SECRET is weak or missing!');
  if (process.env.NODE_ENV === 'production') {
    throw new Error('Strong SESSION_SECRET required in production');
  }
}
```

**Generate Strong Secret:**
```bash
node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"
```

### Cookie Configuration

**Security Settings:**

```typescript
cookie: {
  httpOnly: true,              // Prevents XSS access to cookies
  secure: isProduction,        // HTTPS-only in production
  maxAge: 24 * 60 * 60 * 1000, // 24 hours
  sameSite: isProduction ? 'strict' : 'lax', // CSRF protection
  domain: undefined,           // Let browser determine
  path: '/'                    // Cookie valid for all paths
}
```

**httpOnly Flag:**
- Prevents JavaScript access to session cookie
- Mitigates XSS attacks
- Cookie only sent in HTTP requests

**secure Flag:**
- Enforces HTTPS in production
- Prevents cookie transmission over unencrypted connections
- Automatically disabled in development for localhost

**sameSite Flag:**
- **strict (production):** Cookie only sent for same-site requests
- **lax (development):** Cookie sent for top-level navigation
- Prevents CSRF attacks

**Cookie Name:**
- Custom name: `sid` (not default `connect.sid`)
- Security through obscurity
- Harder for attackers to identify session cookie

### Session Storage

**Storage Type:** PostgreSQL database
**Table:** sessions
**Auto-pruning:** Every 15 minutes

**Benefits:**
- Persistent across server restarts
- Scalable to multiple server instances
- Automatic cleanup of expired sessions
- Audit trail capability

**Session Store Configuration:**
```typescript
new pgStore({
  pool: pool,
  tableName: "sessions",
  createTableIfMissing: false,
  pruneSessionInterval: 60 * 15, // 15 minutes
  errorLog: console.error.bind(console)
})
```

### Session Timeouts

**Absolute Timeout:**
- **Duration:** 24 hours from login
- **Purpose:** Force re-authentication after extended period
- **Bypass:** None (applies to all users including superadmin)

**Inactivity Timeout:**
- **Duration:** 2 hours from last activity
- **Purpose:** Auto-logout for inactive sessions
- **Activity Extension:** Every authenticated request

**Implementation:**
```typescript
const inactivityTimeout = 2 * 60 * 60 * 1000; // 2 hours
const absoluteTimeout = 24 * 60 * 60 * 1000;  // 24 hours

// Check absolute timeout
if (now - sessionUser.sessionStart > absoluteTimeout) {
  req.session.destroy();
  return res.status(401).json({
    message: "Session expired",
    reason: "absolute_timeout"
  });
}

// Check inactivity timeout
if (now - sessionUser.lastActivity > inactivityTimeout) {
  req.session.destroy();
  return res.status(401).json({
    message: "Session expired",
    reason: "inactivity_timeout"
  });
}

// Update activity
sessionUser.lastActivity = now;
```

## Rate Limiting

### Authentication Rate Limiting

**Endpoint:** `/api/auth/login`, `/api/auth/superadmin-login`

**Configuration:**
```typescript
{
  windowMs: 15 * 60 * 1000,      // 15 minutes
  max: 5,                         // 5 failed attempts per IP
  skipSuccessfulRequests: true,   // Only count failed attempts
  message: {
    error: "Too many login attempts from this IP. Please try again in 15 minutes.",
    code: "AUTH_RATE_LIMIT_EXCEEDED",
    retryAfter: "15 minutes"
  }
}
```

**Purpose:**
- Prevents brute force password attacks
- Limits authentication attempts per IP
- Only failed attempts count toward limit

### Password Reset Rate Limiting

**Configuration:**
```typescript
{
  windowMs: 60 * 60 * 1000,  // 1 hour
  max: 3,                     // 3 attempts per IP
  skipSuccessfulRequests: true
}
```

**Purpose:**
- Prevents enumeration attacks
- Limits password reset requests

### Registration Rate Limiting

**Configuration:**
```typescript
{
  windowMs: 60 * 60 * 1000,  // 1 hour
  max: 5,                     // 5 registrations per IP
}
```

**Purpose:**
- Prevents spam account creation
- Limits automated registration

### API Rate Limiting

**Applied to:** All `/api/*` routes

**Configuration:**
```typescript
{
  windowMs: 1 * 60 * 1000,  // 1 minute
  max: 300,                  // 300 requests per IP
  skip: (req) => {
    // Skip health and public endpoints
    if (req.path === '/api/health') return true;
    if (req.path === '/api/database/status') return true;
    if (req.path.startsWith('/api/public-')) return true;
    return false;
  }
}
```

**Purpose:**
- Prevents API abuse
- Protects against DoS attacks
- Allows higher throughput for UI-driven polling

### Export Rate Limiting

**Configuration:**
```typescript
{
  windowMs: 60 * 60 * 1000,  // 1 hour
  max: 10,                    // 10 exports per IP
}
```

**Purpose:**
- Prevents resource exhaustion
- Limits expensive data export operations

### Rate Limit Headers

**Standard Headers Sent:**
- `RateLimit-Limit`: Maximum requests allowed
- `RateLimit-Remaining`: Remaining requests
- `RateLimit-Reset`: Time when limit resets

**Legacy Headers:**
- Disabled (X-RateLimit-* headers not sent)

## CORS Configuration

**Status:** Not explicitly configured

**Current Behavior:**
- No CORS middleware detected
- Same-origin policy enforced by default
- Frontend and backend served from same origin

**Recommendations:**
- Configure CORS if frontend deployed separately
- Use restrictive origin whitelist
- Set credentials: true for cookie support

**Example Configuration:**
```typescript
import cors from 'cors';

app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
```

## CSRF Protection

**Status:** Partial protection via sameSite cookie attribute

**Current Protection:**
- **sameSite: strict (production):** Prevents CSRF by blocking cross-site cookies
- **sameSite: lax (development):** Allows cookies for top-level navigation

**Limitations:**
- No CSRF token validation
- Relies on sameSite attribute (not supported in all browsers)

**Recommendations:**
- Implement CSRF token middleware
- Use csurf or csrf packages
- Add CSRF token to forms and AJAX requests

**Example Implementation:**
```typescript
import csrf from 'csurf';

const csrfProtection = csrf({ cookie: true });
app.use(csrfProtection);

app.get('/form', (req, res) => {
  res.json({ csrfToken: req.csrfToken() });
});
```

## SQL Injection Prevention

**ORM:** Drizzle ORM
**Protection:** Parameterized queries

**Safe Queries:**
```typescript
// Drizzle automatically parameterizes
await db
  .select()
  .from(users)
  .where(eq(users.username, username));
```

**Dangerous Patterns (Avoided):**
```typescript
// RAW SQL - avoid unless necessary
await db.execute(sql`SELECT * FROM users WHERE username = ${username}`);
```

## XSS Prevention

**Cookie Protection:**
- httpOnly flag prevents JavaScript access

**Input Validation:**
- Validation schemas for all user input
- Type checking via TypeScript

**Output Encoding:**
- Frontend framework handles encoding (React)

**Recommendations:**
- Sanitize HTML input if rich text is allowed
- Use Content Security Policy headers

## Database Connection Security

### SSL Configuration

**Connection String Based:**
- SSL enabled if `sslmode=require` in DATABASE_URL
- SSL preferred if `sslmode=prefer` in DATABASE_URL
- SSL disabled if `sslmode=disable` in DATABASE_URL

**Current Configuration:**
```
DATABASE_URL=postgresql://...?sslmode=disable
```

**SSL is DISABLED** in current configuration

**Implementation:**
```typescript
if (connectionString.includes('sslmode=require')) {
  poolConfig.ssl = {
    rejectUnauthorized: process.env.NODE_ENV === 'production',
    ca: process.env.DB_SSL_CERT
  };
}
```

**Recommendations:**
- Enable SSL in production
- Use `sslmode=require` for production databases
- Provide CA certificate if using self-signed certs

### Connection Pool Security

**Circuit Breaker:**
- Opens after 5 consecutive connection failures
- Auto-resets after 30 seconds
- Prevents cascade failures

**Connection Timeout:**
- Default: 5 seconds
- Prevents hanging connections

**Pool Limits:**
- Min: 2-5 connections (configurable)
- Max: 5-20 connections (configurable)
- Prevents connection exhaustion

## Security Headers

**Status:** Not explicitly configured

**Missing Headers:**
- X-Frame-Options
- X-Content-Type-Options
- X-XSS-Protection
- Content-Security-Policy
- Strict-Transport-Security

**Recommendations:**
```typescript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
}));
```

## Audit Logging

**Status:** Basic console logging

**Current Logging:**
- Login attempts (success/failure)
- Session creation/destruction
- Authentication failures
- Rate limit violations

**Recommendations:**
- Log to persistent storage
- Include user ID, IP, timestamp
- Log sensitive operations (role changes, password resets)
- Implement log rotation

## Security Vulnerabilities and Concerns

### Critical

1. **SSL Disabled:** Database connection not encrypted
2. **No CSRF Tokens:** Relies only on sameSite attribute
3. **Weak Session Secret Allowed:** Development mode allows weak secrets

### High

1. **No Security Headers:** Missing helmet middleware
2. **Superadmin Plain Text Password:** Stored in setup-app.json
3. **No Password Complexity Requirements:** Weak passwords allowed

### Medium

1. **No Rate Limiting on Some Endpoints:** Some routes lack rate limiting
2. **No Audit Logging:** Limited security event logging
3. **No Account Lockout:** Unlimited attempts after rate limit window

### Low

1. **Cookie Name Obscurity:** Relies on security through obscurity
2. **No CORS Configuration:** May cause issues with separate frontend deployment

## Security Best Practices

### Implemented

- bcrypt password hashing
- Session-based authentication
- httpOnly secure cookies
- Rate limiting on authentication
- Timing attack prevention
- Input validation
- Parameterized queries (ORM)
- Session timeouts
- Connection pooling with circuit breaker

### Recommended

- Enable SSL for database connections
- Implement CSRF token validation
- Add security headers (helmet)
- Enforce password complexity
- Implement audit logging
- Add account lockout mechanism
- Hash superadmin passwords
- Configure CORS properly
- Add Content Security Policy
- Implement API key rotation
- Add security monitoring

## Related Files

- `/apps/backend-api/auth.ts` - Session configuration
- `/apps/backend-api/middleware/auth.ts` - Authentication middleware
- `/apps/backend-api/middleware/rate-limit.ts` - Rate limiting
- `/apps/backend-api/modules/auth/auth.service.ts` - Password hashing
- `/apps/backend-api/connection-pool.ts` - Database security
- `/.env` - Environment variables (SECRET_SESSION, DATABASE_URL)
