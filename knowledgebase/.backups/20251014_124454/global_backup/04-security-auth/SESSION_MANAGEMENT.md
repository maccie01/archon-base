# Session Management Security

Created: 2025-10-13
Last Updated: 2025-10-13
Sources: OWASP Session Management Cheat Sheet, NIST Guidelines, Industry Best Practices

## Overview

Secure session management is critical for maintaining authenticated state and protecting user sessions from hijacking, fixation, and other attacks. This document covers session lifecycle, storage, security controls, and best practices.

## Session Lifecycle

```
1. Session Creation (Login)
   “
2. Session Validation (Each Request)
   “
3. Session Renewal (Activity)
   “
4. Session Termination (Logout/Timeout)
```

## Session Storage Comparison

| Storage Type | Scalability | Performance | Security | Best For |
|--------------|-------------|-------------|----------|----------|
| **Memory (MemoryStore)** | Poor | Excellent | Medium | Development only |
| **Redis** | Excellent | Excellent | High | Production (recommended) |
| **PostgreSQL** | Good | Good | High | Existing PostgreSQL apps |
| **MongoDB** | Excellent | Very Good | High | NoSQL environments |
| **File System** | Poor | Poor | Low | Never use in production |

## Pattern 1: Redis Session Store (Recommended)

### Overview
Redis provides fast, scalable session storage with built-in expiration and excellent performance for high-traffic applications.

### When to Use
- Production applications with multiple servers
- High-traffic applications requiring fast session access
- Microservices architectures
- When horizontal scaling is needed

### Implementation Pattern

```typescript
// TODO: Add Redis session store implementation

import session from 'express-session';
import RedisStore from 'connect-redis';
import { createClient } from 'redis';

// Redis client configuration
const redisClient = createClient({
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
  password: process.env.REDIS_PASSWORD,
  db: parseInt(process.env.REDIS_DB || '0'),

  // Connection retry strategy
  retry_strategy: (options) => {
    if (options.error && options.error.code === 'ECONNREFUSED') {
      console.error('Redis connection refused');
      return new Error('Redis server refused connection');
    }
    if (options.total_retry_time > 1000 * 60 * 60) {
      return new Error('Redis retry time exhausted');
    }
    if (options.attempt > 10) {
      return undefined; // Stop retrying
    }
    return Math.min(options.attempt * 100, 3000);
  }
});

// Connect to Redis
await redisClient.connect();

// Session middleware configuration
const sessionMiddleware = session({
  store: new RedisStore({
    client: redisClient,
    prefix: 'sess:',     // Key prefix in Redis
    ttl: 86400,          // Session TTL in seconds (24 hours)
  }),

  // Session ID configuration
  name: 'sessionId',     // Cookie name (don't use 'connect.sid')
  secret: process.env.SESSION_SECRET!,  // Strong random secret
  resave: false,         // Don't save session if unmodified
  saveUninitialized: false, // Don't create session until something stored

  // Cookie security configuration
  cookie: {
    httpOnly: true,      // Prevent JavaScript access (XSS protection)
    secure: process.env.NODE_ENV === 'production', // HTTPS only in production
    sameSite: 'strict',  // CSRF protection
    maxAge: 1000 * 60 * 60 * 24, // 24 hours
    domain: process.env.COOKIE_DOMAIN, // Set domain if needed
    path: '/',           // Cookie path
  },

  // Session rolling - extend session on activity
  rolling: true,         // Reset maxAge on each request

  // Security options
  proxy: true,           // Trust proxy if behind reverse proxy
  unset: 'destroy',      // Destroy session when unsetting req.session
});

// TODO: Add session health check
// TODO: Add session cleanup job for expired sessions
```

### Security Considerations

**Strengths**:
- Fast session lookup (in-memory)
- Automatic expiration handling
- Horizontal scaling support
- Persistent across server restarts
- Built-in pub/sub for session updates

**Weaknesses**:
- Requires Redis infrastructure
- Network latency for each session check
- Cost of running Redis cluster
- Need backup/persistence configuration

**Best Practices**:
1. Use Redis Cluster for high availability
2. Enable Redis persistence (AOF or RDB)
3. Set up Redis authentication
4. Use TLS for Redis connections in production
5. Monitor Redis memory usage
6. Implement connection pooling
7. Set appropriate TTL values
8. Use key prefixes for organization
9. Implement graceful degradation if Redis unavailable
10. Regular Redis backup strategy

## Pattern 2: PostgreSQL Session Store

### Overview
Store sessions in existing PostgreSQL database for applications already using PostgreSQL.

### When to Use
- Applications already using PostgreSQL
- When Redis is not available
- When session data needs to be queried
- When strong consistency is required

### Implementation Pattern

```typescript
// TODO: Add PostgreSQL session store implementation

import session from 'express-session';
import pgSession from 'connect-pg-simple';
import pg from 'pg';

const PostgresSessionStore = pgSession(session);

// PostgreSQL connection pool
const pgPool = new pg.Pool({
  host: process.env.POSTGRES_HOST,
  port: parseInt(process.env.POSTGRES_PORT || '5432'),
  database: process.env.POSTGRES_DB,
  user: process.env.POSTGRES_USER,
  password: process.env.POSTGRES_PASSWORD,
  max: 20, // Maximum pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Session middleware with PostgreSQL store
const sessionMiddleware = session({
  store: new PostgresSessionStore({
    pool: pgPool,
    tableName: 'user_sessions',  // Custom table name

    // Session cleanup
    pruneSessionInterval: 60 * 15, // Cleanup every 15 minutes

    // Error handling
    errorLog: (error) => {
      console.error('Session store error:', error);
    },
  }),

  name: 'sessionId',
  secret: process.env.SESSION_SECRET!,
  resave: false,
  saveUninitialized: false,

  cookie: {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    maxAge: 1000 * 60 * 60 * 24, // 24 hours
  },

  rolling: true,
});

// Create sessions table
const createSessionTableSQL = `
CREATE TABLE IF NOT EXISTS user_sessions (
  sid VARCHAR NOT NULL PRIMARY KEY,
  sess JSON NOT NULL,
  expire TIMESTAMP(6) NOT NULL
);

CREATE INDEX IF NOT EXISTS IDX_session_expire ON user_sessions (expire);
`;

// TODO: Add session table migration
// TODO: Add index on expire column for efficient cleanup
```

### Security Considerations

**Strengths**:
- No additional infrastructure needed
- ACID transactions for session operations
- Can query session data
- Strong consistency guarantees
- Existing backup procedures apply

**Weaknesses**:
- Slower than Redis (disk I/O)
- Database load from session queries
- Requires database maintenance
- Less efficient for high-traffic sites

**Best Practices**:
1. Use connection pooling
2. Create index on expire column
3. Implement automatic session pruning
4. Monitor database performance
5. Use read replicas for session reads if needed
6. Implement connection retry logic
7. Set appropriate pool sizes
8. Use prepared statements
9. Regular VACUUM on session table
10. Archive old sessions before deletion

## Session Security Controls

### 1. Session ID Generation

```typescript
// TODO: Add secure session ID generation

import crypto from 'crypto';

/**
 * Generate cryptographically secure session ID
 * express-session handles this, but for reference:
 */
function generateSessionId(): string {
  // 128 bits of entropy (16 bytes = 32 hex chars)
  return crypto.randomBytes(16).toString('hex');
}

// Session ID Requirements:
// - At least 128 bits of entropy
// - Cryptographically random (use crypto.randomBytes)
// - Never predictable or sequential
// - Unique across all sessions
// - URL-safe characters
```

### 2. Session Regeneration

```typescript
// TODO: Add session regeneration pattern

/**
 * Regenerate session ID after authentication
 * Prevents session fixation attacks
 */
function regenerateSession(req: Request, res: Response, next: NextFunction) {
  const oldSessionData = { ...req.session };

  req.session.regenerate((err) => {
    if (err) {
      console.error('Session regeneration failed:', err);
      return next(err);
    }

    // Restore session data (except session ID)
    Object.assign(req.session, oldSessionData);

    next();
  });
}

// Usage: After login
app.post('/login', async (req, res) => {
  // Validate credentials
  const user = await authenticateUser(req.body.username, req.body.password);

  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // Regenerate session to prevent fixation
  req.session.regenerate((err) => {
    if (err) {
      return res.status(500).json({ error: 'Session error' });
    }

    // Set user data in new session
    req.session.user = {
      id: user.id,
      username: user.username,
      role: user.role,
    };

    // Timestamp tracking
    req.session.createdAt = Date.now();
    req.session.lastActivity = Date.now();

    res.json({ message: 'Login successful', user });
  });
});
```

### 3. Session Timeout Management

```typescript
// TODO: Add session timeout middleware

interface SessionTimeoutConfig {
  maxAge: number;        // Absolute session lifetime (ms)
  idleTimeout: number;   // Inactivity timeout (ms)
}

const TIMEOUT_CONFIG: SessionTimeoutConfig = {
  maxAge: 1000 * 60 * 60 * 12,    // 12 hours absolute
  idleTimeout: 1000 * 60 * 30,     // 30 minutes idle
};

/**
 * Session timeout middleware
 * Implements both idle timeout and absolute timeout
 */
function sessionTimeoutMiddleware(req: Request, res: Response, next: NextFunction) {
  if (!req.session || !req.session.user) {
    return next();
  }

  const now = Date.now();
  const createdAt = req.session.createdAt || now;
  const lastActivity = req.session.lastActivity || now;

  // Check absolute timeout
  if (now - createdAt > TIMEOUT_CONFIG.maxAge) {
    req.session.destroy((err) => {
      if (err) console.error('Session destruction error:', err);
    });
    return res.status(401).json({
      error: 'Session expired',
      reason: 'absolute_timeout'
    });
  }

  // Check idle timeout
  if (now - lastActivity > TIMEOUT_CONFIG.idleTimeout) {
    req.session.destroy((err) => {
      if (err) console.error('Session destruction error:', err);
    });
    return res.status(401).json({
      error: 'Session expired',
      reason: 'idle_timeout'
    });
  }

  // Update last activity timestamp
  req.session.lastActivity = now;

  next();
}

// Apply to protected routes
app.use('/api', sessionTimeoutMiddleware);
```

### 4. Concurrent Session Control

```typescript
// TODO: Add concurrent session limit

interface SessionTracking {
  userId: string;
  sessionIds: Set<string>;
  maxSessions: number;
}

/**
 * Limit concurrent sessions per user
 */
class SessionManager {
  private userSessions: Map<string, Set<string>> = new Map();
  private maxSessionsPerUser = 3; // Maximum concurrent sessions

  /**
   * Track new session for user
   */
  async trackSession(userId: string, sessionId: string): Promise<void> {
    let sessions = this.userSessions.get(userId);

    if (!sessions) {
      sessions = new Set();
      this.userSessions.set(userId, sessions);
    }

    sessions.add(sessionId);

    // Enforce session limit (remove oldest sessions)
    if (sessions.size > this.maxSessionsPerUser) {
      const oldestSession = sessions.values().next().value;
      await this.destroySession(userId, oldestSession);
    }
  }

  /**
   * Remove session tracking
   */
  async destroySession(userId: string, sessionId: string): Promise<void> {
    const sessions = this.userSessions.get(userId);
    if (sessions) {
      sessions.delete(sessionId);

      // TODO: Destroy session in Redis/PostgreSQL

      if (sessions.size === 0) {
        this.userSessions.delete(userId);
      }
    }
  }

  /**
   * Get active session count for user
   */
  getSessionCount(userId: string): number {
    return this.userSessions.get(userId)?.size || 0;
  }

  /**
   * Destroy all sessions for user (e.g., password change)
   */
  async destroyAllSessions(userId: string): Promise<void> {
    const sessions = this.userSessions.get(userId);
    if (sessions) {
      for (const sessionId of sessions) {
        // TODO: Destroy each session in store
      }
      this.userSessions.delete(userId);
    }
  }
}

// TODO: Implement Redis-backed session tracking for distributed systems
```

### 5. Session Data Validation

```typescript
// TODO: Add session data validation middleware

/**
 * Validate session integrity on each request
 */
function validateSessionMiddleware(req: Request, res: Response, next: NextFunction) {
  if (!req.session || !req.session.user) {
    return next();
  }

  // Validate required session fields
  if (!req.session.user.id || !req.session.user.role) {
    req.session.destroy((err) => {
      if (err) console.error('Session destruction error:', err);
    });
    return res.status(401).json({ error: 'Invalid session data' });
  }

  // Validate session hasn't been tampered with
  // (express-session handles signature validation)

  // Optional: Check user still exists and is active
  // TODO: Add user validation against database

  next();
}
```

## Cookie Security Configuration

### Secure Cookie Attributes

```typescript
// TODO: Add comprehensive cookie configuration

interface SecureCookieConfig {
  name: string;          // Custom name (not default)
  httpOnly: boolean;     // Prevent JavaScript access
  secure: boolean;       // HTTPS only
  sameSite: 'strict' | 'lax' | 'none';  // CSRF protection
  maxAge: number;        // Cookie lifetime
  domain?: string;       // Cookie domain
  path: string;          // Cookie path
  signed: boolean;       // Sign cookie
}

const SECURE_COOKIE_CONFIG: SecureCookieConfig = {
  name: 'sid',                    // Don't use default names
  httpOnly: true,                 // XSS protection
  secure: true,                   // HTTPS only
  sameSite: 'strict',             // Strictest CSRF protection
  maxAge: 1000 * 60 * 60 * 24,   // 24 hours
  path: '/',                      // Entire site
  signed: true,                   // Tamper protection
};

// SameSite attribute explanation:
// - 'strict': Cookie sent only for same-site requests (most secure)
// - 'lax': Cookie sent for top-level navigation (balanced)
// - 'none': Cookie sent for all requests (requires Secure flag)
```

### Cookie Security Checklist

- [ ] **HttpOnly**: Always set to true (prevents XSS cookie theft)
- [ ] **Secure**: Always true in production (HTTPS only)
- [ ] **SameSite**: Use 'strict' or 'lax' (CSRF protection)
- [ ] **Custom name**: Don't use default session cookie names
- [ ] **Signed cookies**: Enable cookie signing with secret
- [ ] **Domain restriction**: Set domain if using subdomains
- [ ] **Path restriction**: Set path to minimum required
- [ ] **Max-Age**: Set appropriate expiration
- [ ] **No sensitive data**: Never store sensitive data in cookies

## Session Attack Prevention

### 1. Session Fixation Prevention

```typescript
// TODO: Add session fixation prevention

/**
 * Prevent session fixation attacks
 * Always regenerate session ID after authentication
 */
app.post('/login', async (req, res) => {
  const user = await authenticateUser(req.body);

  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // CRITICAL: Regenerate session ID after successful authentication
  req.session.regenerate((err) => {
    if (err) {
      return res.status(500).json({ error: 'Session error' });
    }

    req.session.user = user;
    res.json({ message: 'Login successful' });
  });
});
```

### 2. Session Hijacking Prevention

```typescript
// TODO: Add session hijacking prevention

/**
 * Detect session hijacking through fingerprinting
 */
interface SessionFingerprint {
  userAgent: string;
  ip: string;
  acceptLanguage: string;
}

function createFingerprint(req: Request): string {
  const data: SessionFingerprint = {
    userAgent: req.headers['user-agent'] || '',
    ip: req.ip || req.connection.remoteAddress || '',
    acceptLanguage: req.headers['accept-language'] || '',
  };

  return crypto
    .createHash('sha256')
    .update(JSON.stringify(data))
    .digest('hex');
}

/**
 * Middleware to detect session hijacking
 */
function sessionFingerprintMiddleware(req: Request, res: Response, next: NextFunction) {
  if (!req.session || !req.session.user) {
    return next();
  }

  const currentFingerprint = createFingerprint(req);

  if (!req.session.fingerprint) {
    // First request, store fingerprint
    req.session.fingerprint = currentFingerprint;
  } else if (req.session.fingerprint !== currentFingerprint) {
    // Fingerprint mismatch - possible hijacking
    console.warn(`Session hijacking attempt detected for user ${req.session.user.id}`);

    req.session.destroy((err) => {
      if (err) console.error('Session destruction error:', err);
    });

    return res.status(401).json({
      error: 'Session invalid',
      reason: 'security_violation'
    });
  }

  next();
}

// Note: Fingerprinting has limitations (proxies, mobile networks, etc.)
// Use as additional security layer, not primary defense
```

### 3. CSRF Protection with Sessions

```typescript
// TODO: Add CSRF token generation and validation

import crypto from 'crypto';

/**
 * Generate CSRF token for session
 */
function generateCSRFToken(req: Request): string {
  if (!req.session.csrfSecret) {
    req.session.csrfSecret = crypto.randomBytes(32).toString('hex');
  }

  // Generate token from secret
  const token = crypto
    .createHash('sha256')
    .update(req.session.csrfSecret)
    .digest('hex');

  return token;
}

/**
 * CSRF protection middleware
 */
function csrfProtection(req: Request, res: Response, next: NextFunction) {
  // Skip for safe methods
  if (['GET', 'HEAD', 'OPTIONS'].includes(req.method)) {
    return next();
  }

  const token = req.headers['x-csrf-token'] || req.body._csrf;
  const expectedToken = generateCSRFToken(req);

  if (!token || token !== expectedToken) {
    return res.status(403).json({ error: 'CSRF token invalid' });
  }

  next();
}

// Provide CSRF token to client
app.get('/api/csrf-token', (req, res) => {
  const token = generateCSRFToken(req);
  res.json({ csrfToken: token });
});
```

## Session Logout and Cleanup

### Secure Logout Implementation

```typescript
// TODO: Add secure logout implementation

/**
 * Secure logout endpoint
 */
app.post('/logout', (req: Request, res: Response) => {
  if (!req.session) {
    return res.status(400).json({ error: 'No active session' });
  }

  const userId = req.session.user?.id;

  // Destroy session
  req.session.destroy((err) => {
    if (err) {
      console.error('Logout error:', err);
      return res.status(500).json({ error: 'Logout failed' });
    }

    // Clear session cookie
    res.clearCookie('sessionId', {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
    });

    // Optional: Log logout event
    if (userId) {
      console.log(`User ${userId} logged out at ${new Date().toISOString()}`);
    }

    res.json({ message: 'Logged out successfully' });
  });
});
```

### Session Cleanup Job

```typescript
// TODO: Add automated session cleanup

/**
 * Cleanup expired sessions (PostgreSQL)
 */
async function cleanupExpiredSessions(): Promise<number> {
  const result = await db.execute(
    'DELETE FROM user_sessions WHERE expire < NOW() RETURNING sid'
  );

  console.log(`Cleaned up ${result.rowCount} expired sessions`);
  return result.rowCount || 0;
}

/**
 * Run cleanup job periodically
 */
function startSessionCleanupJob(): void {
  // Run every 15 minutes
  setInterval(async () => {
    try {
      await cleanupExpiredSessions();
    } catch (error) {
      console.error('Session cleanup error:', error);
    }
  }, 15 * 60 * 1000);
}

// For Redis: Automatic expiration, no cleanup needed
```

## Testing Session Security

```typescript
// TODO: Add session security test suite

describe('Session Security', () => {
  describe('Session Creation', () => {
    it('should create session on login', async () => {});
    it('should regenerate session ID after authentication', async () => {});
    it('should set secure cookie attributes', async () => {});
    it('should create unique session IDs', async () => {});
  });

  describe('Session Timeout', () => {
    it('should expire session after maxAge', async () => {});
    it('should expire session after idle timeout', async () => {});
    it('should extend session on activity', async () => {});
  });

  describe('Session Destruction', () => {
    it('should destroy session on logout', async () => {});
    it('should clear session cookie', async () => {});
    it('should handle concurrent logouts', async () => {});
  });

  describe('Attack Prevention', () => {
    it('should prevent session fixation', async () => {});
    it('should detect session hijacking', async () => {});
    it('should validate CSRF tokens', async () => {});
  });
});
```

## Common Session Security Mistakes

1. **Not regenerating session ID after login** (session fixation)
2. **Using default session cookie names** (easier to target)
3. **Not setting HttpOnly flag** (XSS vulnerability)
4. **Not using HTTPS in production** (session hijacking)
5. **Not implementing session timeout** (indefinite sessions)
6. **Storing sensitive data in cookies** (data exposure)
7. **Not validating session data** (data integrity)
8. **Using weak session secrets** (signature forgery)
9. **Not cleaning up expired sessions** (database bloat)
10. **Not destroying sessions on password change** (account takeover)

## References

- OWASP Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- OWASP Testing Guide - Session Management: https://owasp.org/www-project-web-security-testing-guide/
- Express Session Documentation: https://github.com/expressjs/session
- Redis Best Practices: https://redis.io/docs/manual/patterns/
- NIST Session Management: https://pages.nist.gov/800-63-3/

## Next Steps

1. Implement JWT patterns: [JWT_PATTERNS.md](./JWT_PATTERNS.md)
2. Add CSRF protection: [CSRF_PROTECTION.md](./CSRF_PROTECTION.md)
3. Configure security headers: [SECURITY_HEADERS.md](./SECURITY_HEADERS.md)
4. Implement rate limiting: [RATE_LIMITING.md](./RATE_LIMITING.md)
