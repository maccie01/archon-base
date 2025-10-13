# Security Patterns - Netzwächter Project Standards

Created: 2025-10-13

This document defines **REQUIRED security patterns** for the Netzwächter project. These are NON-NEGOTIABLE security requirements.

---

## Authentication Pattern

### Session-Based Authentication

**Use**: Express session with PostgreSQL store

```typescript
// apps/backend-api/config/session.ts
import session from 'express-session'
import connectPgSimple from 'connect-pg-simple'
import { pool } from '@/connection-pool'

const PgSession = connectPgSimple(session)

export const sessionMiddleware = session({
  store: new PgSession({
    pool,
    tableName: 'sessions',
    createTableIfMissing: true
  }),
  secret: process.env.SESSION_SECRET!, // Must be 32+ characters
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production', // HTTPS only in production
    httpOnly: true, // Prevent XSS
    maxAge: 1000 * 60 * 60 * 24, // 24 hours
    sameSite: 'lax' // CSRF protection
  },
  name: 'sessionId' // Don't use default 'connect.sid'
})
```

### Password Security

**Use**: Argon2id for password hashing

```typescript
// apps/backend-api/utils/password.ts
import argon2 from 'argon2'

export async function hashPassword(password: string): Promise<string> {
  return await argon2.hash(password, {
    type: argon2.argon2id, // Resistant to GPU attacks
    memoryCost: 19456, // 19 MB
    timeCost: 2, // 2 iterations
    parallelism: 1 // 1 thread
  })
}

export async function verifyPassword(
  hash: string,
  password: string
): Promise<boolean> {
  try {
    return await argon2.verify(hash, password)
  } catch (error) {
    return false
  }
}

// ❌ NEVER do this:
// const hash = bcrypt.hashSync(password, 10) // Synchronous - blocks event loop
// const hash = crypto.createHash('sha256').update(password).digest('hex') // Not suitable for passwords
```

### Login Endpoint Pattern

```typescript
// apps/backend-api/modules/auth/auth.controller.ts
import { Request, Response } from 'express'
import { AuthService } from './auth.service'
import { AppError } from '@/utils/errors'

export class AuthController {
  private service: AuthService

  constructor() {
    this.service = new AuthService()
  }

  async login(req: Request, res: Response) {
    const { username, password } = req.body

    // Validate input
    if (!username || !password) {
      throw new AppError('Username and password required', 400)
    }

    // Authenticate user
    const user = await this.service.authenticate(username, password)

    if (!user) {
      // Don't reveal whether username or password was wrong
      throw new AppError('Invalid credentials', 401)
    }

    // Check if account is active
    if (!user.active) {
      throw new AppError('Account is disabled', 403)
    }

    // Create session
    req.session.userId = user.id
    req.session.username = user.username
    req.session.role = user.role
    req.session.mandantId = user.mandantId

    // Don't send password hash to client
    const { password: _, ...userWithoutPassword } = user

    res.json({
      user: userWithoutPassword,
      message: 'Login successful'
    })
  }

  async logout(req: Request, res: Response) {
    // Destroy session
    req.session.destroy((err) => {
      if (err) {
        throw new AppError('Logout failed', 500)
      }

      res.clearCookie('sessionId')
      res.json({ message: 'Logout successful' })
    })
  }

  async getCurrentUser(req: Request, res: Response) {
    const userId = req.session.userId

    if (!userId) {
      throw new AppError('Not authenticated', 401)
    }

    const user = await this.service.getUserById(userId)

    if (!user) {
      throw new AppError('User not found', 404)
    }

    // Don't send password hash
    const { password: _, ...userWithoutPassword } = user

    res.json(userWithoutPassword)
  }
}
```

---

## Authorization Pattern

### Role-Based Access Control (RBAC)

**Roles**:
- `superadmin` - Full system access
- `admin` - Mandant management
- `user` - Standard user access

### Authentication Middleware

```typescript
// apps/backend-api/middleware/auth.ts
import { Request, Response, NextFunction } from 'express'
import { AppError } from '@/utils/errors'

export function requireAuth(req: Request, res: Response, next: NextFunction) {
  if (!req.session?.userId) {
    throw new AppError('Authentication required', 401)
  }
  next()
}

export function requireRole(...allowedRoles: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    const userRole = req.session.role

    if (!userRole) {
      throw new AppError('Authentication required', 401)
    }

    if (!allowedRoles.includes(userRole)) {
      throw new AppError(
        `Access denied. Required roles: ${allowedRoles.join(', ')}`,
        403
      )
    }

    next()
  }
}

export function requireMandant(req: Request, res: Response, next: NextFunction) {
  if (!req.session?.mandantId) {
    throw new AppError('Mandant context required', 400)
  }
  next()
}

// Usage in routes:
router.get('/api/settings',
  requireAuth,
  requireMandant,
  controller.getAll
)

router.post('/api/settings',
  requireAuth,
  requireRole('admin'),
  controller.create
)

router.delete('/api/users/:id',
  requireAuth,
  requireRole('superadmin'),
  controller.delete
)
```

### Multi-Tenancy Security

```typescript
// apps/backend-api/modules/settings/settings.service.ts
export class SettingsService {
  async getById(id: string, mandantId: string): Promise<Setting | null> {
    const setting = await this.repository.findById(id)

    if (!setting) {
      return null
    }

    // CRITICAL: Always verify mandantId
    if (setting.mandantId !== mandantId) {
      throw new AppError('Access denied', 403)
    }

    return setting
  }

  async getAllByMandant(mandantId: string): Promise<Setting[]> {
    // ALWAYS filter by mandantId from session
    return await this.repository.findByMandant(mandantId)
  }

  // ❌ NEVER create methods without mandantId check:
  async getAllDangerous(): Promise<Setting[]> {
    // This returns ALL settings from ALL mandants - NEVER do this!
    return await this.repository.findAll()
  }
}
```

---

## Input Validation Pattern

### Validate ALL Input with Zod

```typescript
// apps/backend-api/modules/settings/settings.validation.ts
import { z } from 'zod'

export const settingsSchemas = {
  create: z.object({
    body: z.object({
      key: z.string()
        .min(1, 'Key is required')
        .max(100, 'Key too long')
        .regex(/^[a-zA-Z0-9_-]+$/, 'Key can only contain letters, numbers, underscores, and hyphens'),

      value: z.string()
        .min(1, 'Value is required')
        .max(5000, 'Value too long'),

      description: z.string()
        .max(500, 'Description too long')
        .optional(),

      isSecret: z.boolean()
        .optional()
        .default(false)
    })
  }),

  update: z.object({
    params: z.object({
      id: z.string().uuid('Invalid setting ID')
    }),
    body: z.object({
      value: z.string()
        .min(1, 'Value is required')
        .max(5000, 'Value too long')
        .optional(),

      description: z.string()
        .max(500, 'Description too long')
        .optional(),

      isSecret: z.boolean().optional()
    }).refine(
      data => Object.keys(data).length > 0,
      { message: 'At least one field must be provided' }
    )
  })
}
```

### Sanitize Output

```typescript
// apps/backend-api/modules/users/users.service.ts
export class UsersService {
  async getById(id: string): Promise<User | null> {
    const user = await this.repository.findById(id)

    if (!user) {
      return null
    }

    // CRITICAL: Remove sensitive fields before returning
    return this.sanitizeUser(user)
  }

  private sanitizeUser(user: User): Omit<User, 'password'> {
    const { password, ...sanitized } = user
    return sanitized
  }

  // ❌ NEVER return raw user with password:
  async getByIdDangerous(id: string): Promise<User | null> {
    return await this.repository.findById(id) // Contains password hash!
  }
}
```

---

## SQL Injection Prevention

### Use Drizzle ORM (NEVER Raw SQL)

```typescript
// ✅ GOOD: Drizzle ORM (safe from SQL injection)
import { db } from '@/db'
import { users } from '@/db/schema'
import { eq, like } from 'drizzle-orm'

export async function searchUsers(searchTerm: string) {
  return await db.select()
    .from(users)
    .where(like(users.username, `%${searchTerm}%`))
  // Drizzle automatically parameterizes queries
}

// ❌ BAD: String concatenation (SQL injection vulnerability!)
export async function searchUsersDangerous(searchTerm: string) {
  const query = `SELECT * FROM users WHERE username LIKE '%${searchTerm}%'`
  const result = await pool.query(query)
  return result.rows
}
// Attacker could inject: searchTerm = "'; DROP TABLE users; --"

// ⚠️ ACCEPTABLE: Raw SQL with parameterization (only if Drizzle can't do it)
export async function complexQuery(userId: string) {
  const result = await pool.query(
    `SELECT * FROM users WHERE id = $1`,
    [userId] // Parameters are safe
  )
  return result.rows
}
```

---

## XSS Prevention

### Frontend: Sanitize User Input Display

```typescript
// React automatically escapes text content, but be careful with:

// ✅ GOOD: Text content (automatically escaped)
function UserProfile({ username }: { username: string }) {
  return <div>{username}</div>
  // Even if username = "<script>alert('xss')</script>", React escapes it
}

// ❌ BAD: dangerouslySetInnerHTML (XSS vulnerability!)
function UserProfileDangerous({ bio }: { bio: string }) {
  return <div dangerouslySetInnerHTML={{ __html: bio }} />
  // If bio contains script tags, they WILL execute!
}

// ✅ GOOD: Sanitize HTML if you must render it
import DOMPurify from 'isomorphic-dompurify'

function UserProfileSafe({ bio }: { bio: string }) {
  const sanitizedBio = DOMPurify.sanitize(bio, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p'],
    ALLOWED_ATTR: ['href']
  })

  return <div dangerouslySetInnerHTML={{ __html: sanitizedBio }} />
}
```

### Backend: Set Security Headers

```typescript
// apps/backend-api/middleware/security.ts
import helmet from 'helmet'

export function securityMiddleware(app: Express) {
  // Use Helmet for security headers
  app.use(helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "'unsafe-inline'"], // Avoid unsafe-inline in production
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", 'data:', 'https:'],
        connectSrc: ["'self'"],
        fontSrc: ["'self'"],
        objectSrc: ["'none'"],
        mediaSrc: ["'self'"],
        frameSrc: ["'none'"]
      }
    },
    xssFilter: true,
    noSniff: true,
    referrerPolicy: { policy: 'no-referrer' },
    hsts: {
      maxAge: 31536000, // 1 year
      includeSubDomains: true,
      preload: true
    }
  }))
}
```

---

## CSRF Protection

### Use SameSite Cookies

```typescript
// apps/backend-api/config/session.ts
export const sessionMiddleware = session({
  // ... other config
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    sameSite: 'lax', // CSRF protection
    // 'lax' allows GET requests from other sites but blocks POST/PUT/DELETE
  }
})
```

### Double Submit Cookie Pattern (Alternative)

```typescript
// For API-heavy apps, use CSRF tokens
import csrf from 'csurf'

const csrfProtection = csrf({
  cookie: {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict'
  }
})

// Apply to state-changing routes
router.post('/api/settings', csrfProtection, controller.create)
router.put('/api/settings/:id', csrfProtection, controller.update)
router.delete('/api/settings/:id', csrfProtection, controller.delete)

// GET /api/csrf-token to get token
router.get('/api/csrf-token', csrfProtection, (req, res) => {
  res.json({ csrfToken: req.csrfToken() })
})
```

---

## Secrets Management

### Environment Variables Pattern

```typescript
// apps/backend-api/config/index.ts
import { z } from 'zod'

const envSchema = z.object({
  // Database
  DATABASE_URL: z.string().url(),

  // Session
  SESSION_SECRET: z.string()
    .min(32, 'Session secret must be at least 32 characters'),

  // Server
  PORT: z.string().transform(val => parseInt(val, 10)),
  NODE_ENV: z.enum(['development', 'production', 'test']),

  // CORS
  ALLOWED_ORIGIN: z.string().url(),

  // Optional secrets
  ENCRYPTION_KEY: z.string().min(32).optional(),
  API_KEY: z.string().optional()
})

// Validate on startup
const env = envSchema.parse(process.env)

export const config = {
  database: {
    url: env.DATABASE_URL
  },
  session: {
    secret: env.SESSION_SECRET
  },
  server: {
    port: env.PORT,
    env: env.NODE_ENV
  },
  cors: {
    origin: env.ALLOWED_ORIGIN
  },
  encryption: {
    key: env.ENCRYPTION_KEY
  }
} as const

// ❌ NEVER hardcode secrets:
// const SESSION_SECRET = 'my-secret-key' // NEVER!
// const API_KEY = 'sk-1234567890' // NEVER!

// ❌ NEVER commit .env file:
// Add to .gitignore:
// .env
// .env.local
// .env.production
```

### Encrypt Sensitive Data at Rest

```typescript
// apps/backend-api/utils/encryption.ts
import crypto from 'crypto'
import { config } from '@/config'

const ALGORITHM = 'aes-256-gcm'
const KEY_LENGTH = 32
const IV_LENGTH = 16
const SALT_LENGTH = 64
const TAG_LENGTH = 16

export function encrypt(text: string): string {
  const key = Buffer.from(config.encryption.key!, 'hex')
  const iv = crypto.randomBytes(IV_LENGTH)

  const cipher = crypto.createCipheriv(ALGORITHM, key, iv)

  let encrypted = cipher.update(text, 'utf8', 'hex')
  encrypted += cipher.final('hex')

  const tag = cipher.getAuthTag()

  // Return: iv:tag:encrypted
  return `${iv.toString('hex')}:${tag.toString('hex')}:${encrypted}`
}

export function decrypt(text: string): string {
  const [ivHex, tagHex, encrypted] = text.split(':')

  const key = Buffer.from(config.encryption.key!, 'hex')
  const iv = Buffer.from(ivHex, 'hex')
  const tag = Buffer.from(tagHex, 'hex')

  const decipher = crypto.createDecipheriv(ALGORITHM, key, iv)
  decipher.setAuthTag(tag)

  let decrypted = decipher.update(encrypted, 'hex', 'utf8')
  decrypted += decipher.final('utf8')

  return decrypted
}

// Usage in service:
export class SettingsService {
  async create(data: CreateSettingData): Promise<Setting> {
    // Encrypt secret values before storing
    if (data.isSecret && data.value) {
      data.value = encrypt(data.value)
    }

    return await this.repository.create(data)
  }

  async getById(id: string, mandantId: string): Promise<Setting | null> {
    const setting = await this.repository.findById(id)

    if (!setting) {
      return null
    }

    // Decrypt secret values before returning
    if (setting.isSecret && setting.value) {
      setting.value = decrypt(setting.value)
    }

    return setting
  }
}
```

---

## Rate Limiting

### Protect Against Brute Force

```typescript
// apps/backend-api/middleware/rateLimit.ts
import rateLimit from 'express-rate-limit'

// General API rate limit
export const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Max 100 requests per window
  message: 'Too many requests, please try again later',
  standardHeaders: true,
  legacyHeaders: false
})

// Strict rate limit for authentication
export const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // Max 5 attempts per window
  message: 'Too many login attempts, please try again later',
  skipSuccessfulRequests: true // Don't count successful logins
})

// Usage:
app.use('/api', apiLimiter)
app.use('/api/auth/login', authLimiter)
```

---

## Error Handling Security

### Never Leak Sensitive Information in Errors

```typescript
// apps/backend-api/middleware/errorHandler.ts
import { Request, Response, NextFunction } from 'express'
import { AppError } from '@/utils/errors'

export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  // Log full error for debugging (server-side only)
  console.error('Error:', {
    message: err.message,
    stack: err.stack,
    url: req.url,
    method: req.method,
    userId: req.session?.userId
  })

  // Send sanitized error to client
  if (err instanceof AppError) {
    // Known application errors - safe to send
    return res.status(err.statusCode).json({
      error: err.message,
      code: err.code
    })
  }

  // Unknown errors - don't leak details
  res.status(500).json({
    error: 'Internal server error'
    // DON'T include: stack trace, database errors, file paths, etc.
  })
}

// ❌ NEVER do this:
export function dangerousErrorHandler(err: Error, req: Request, res: Response, next: NextFunction) {
  res.status(500).json({
    error: err.message, // Might contain sensitive info
    stack: err.stack, // Reveals code structure
    details: err // Might contain database errors, passwords, etc.
  })
}
```

---

## Security Checklist

### Pre-Deployment Security Review

- [ ] All secrets in environment variables (not hardcoded)
- [ ] Password hashing uses Argon2id
- [ ] Authentication middleware on all protected routes
- [ ] Role-based authorization implemented
- [ ] Multi-tenancy isolation enforced (mandantId checks)
- [ ] Input validation with Zod on all endpoints
- [ ] SQL queries use Drizzle ORM (no raw SQL)
- [ ] XSS prevention (React auto-escaping, DOMPurify for HTML)
- [ ] CSRF protection enabled (SameSite cookies)
- [ ] Security headers configured (Helmet)
- [ ] Rate limiting on authentication endpoints
- [ ] Error handling doesn't leak sensitive info
- [ ] Sensitive data encrypted at rest
- [ ] HTTPS enforced in production
- [ ] Session cookies: httpOnly, secure, sameSite
- [ ] No console.log with sensitive data
- [ ] Dependencies have no known vulnerabilities (npm audit)

---

## Quick Reference

### Security Middleware Stack

```typescript
// apps/backend-api/index.ts
import express from 'express'
import helmet from 'helmet'
import cors from 'cors'
import { sessionMiddleware } from './config/session'
import { apiLimiter } from './middleware/rateLimit'
import { errorHandler } from './middleware/errorHandler'

const app = express()

// 1. Security headers (Helmet)
app.use(helmet())

// 2. CORS
app.use(cors({
  origin: process.env.ALLOWED_ORIGIN,
  credentials: true
}))

// 3. Body parsing
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

// 4. Session
app.use(sessionMiddleware)

// 5. Rate limiting
app.use('/api', apiLimiter)

// 6. Routes
app.use('/api', routes)

// 7. Error handler (last!)
app.use(errorHandler)
```

---

Created: 2025-10-13
Status: Active - CRITICAL security requirements
Priority: P0 - Security non-negotiable
