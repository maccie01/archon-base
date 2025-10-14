# Backend Patterns - Netzwächter Project Standards

Created: 2025-10-13

This document defines the **REQUIRED backend patterns** for the Netzwächter project. All new backend code MUST follow these patterns.

---

## 4-Layer Architecture Pattern

All backend modules MUST follow this 4-layer pattern:

```
Routes → Controller → Service → Repository
```

### Layer 1: Routes (HTTP Routes Only)

**Location**: `apps/backend-api/modules/[module]/[module].routes.ts`

**Responsibility**: Define HTTP endpoints, apply middleware

**Rules**:
- NO business logic
- NO database access
- NO validation (validation happens in schemas)
- Apply middleware (auth, validation)
- Pass to controller

**Example**:

```typescript
// apps/backend-api/modules/settings/settings.routes.ts
import { Router } from 'express'
import { SettingsController } from './settings.controller'
import { requireAuth, requireRole } from '@/middleware/auth'
import { validate } from '@/middleware/validation'
import { settingsSchemas } from './settings.validation'
import { asyncHandler } from '@/middleware/asyncHandler'

const router = Router()
const controller = new SettingsController()

// GET /api/settings - Get all settings (requires auth)
router.get('/',
  requireAuth,
  asyncHandler(controller.getAll.bind(controller))
)

// GET /api/settings/:id - Get single setting (requires auth)
router.get('/:id',
  requireAuth,
  asyncHandler(controller.getById.bind(controller))
)

// POST /api/settings - Create setting (requires admin)
router.post('/',
  requireAuth,
  requireRole('admin'),
  validate(settingsSchemas.create),
  asyncHandler(controller.create.bind(controller))
)

// PUT /api/settings/:id - Update setting (requires admin)
router.put('/:id',
  requireAuth,
  requireRole('admin'),
  validate(settingsSchemas.update),
  asyncHandler(controller.update.bind(controller))
)

// DELETE /api/settings/:id - Delete setting (requires superadmin)
router.delete('/:id',
  requireAuth,
  requireRole('superadmin'),
  asyncHandler(controller.delete.bind(controller))
)

export default router
```

---

### Layer 2: Controller (HTTP Layer)

**Location**: `apps/backend-api/modules/[module]/[module].controller.ts`

**Responsibility**: Handle HTTP request/response, call service

**Rules**:
- Extract data from req (params, query, body, session)
- Call service with extracted data
- Return response with appropriate status code
- NO business logic
- NO database access
- NO validation (already done in routes)

**Example**:

```typescript
// apps/backend-api/modules/settings/settings.controller.ts
import { Request, Response } from 'express'
import { SettingsService } from './settings.service'
import { AppError } from '@/utils/errors'

export class SettingsController {
  private service: SettingsService

  constructor() {
    this.service = new SettingsService()
  }

  async getAll(req: Request, res: Response) {
    const mandantId = req.session.mandantId
    const settings = await this.service.getAllByMandant(mandantId)
    res.json(settings)
  }

  async getById(req: Request, res: Response) {
    const { id } = req.params
    const mandantId = req.session.mandantId

    const setting = await this.service.getById(id, mandantId)

    if (!setting) {
      throw new AppError('Setting not found', 404)
    }

    res.json(setting)
  }

  async create(req: Request, res: Response) {
    const mandantId = req.session.mandantId
    const userId = req.session.userId
    const data = req.body

    const setting = await this.service.create({
      ...data,
      mandantId,
      createdBy: userId
    })

    res.status(201).json(setting)
  }

  async update(req: Request, res: Response) {
    const { id } = req.params
    const mandantId = req.session.mandantId
    const data = req.body

    const setting = await this.service.update(id, data, mandantId)

    if (!setting) {
      throw new AppError('Setting not found', 404)
    }

    res.json(setting)
  }

  async delete(req: Request, res: Response) {
    const { id } = req.params
    const mandantId = req.session.mandantId

    await this.service.delete(id, mandantId)

    res.status(204).send()
  }
}
```

---

### Layer 3: Service (Business Logic)

**Location**: `apps/backend-api/modules/[module]/[module].service.ts`

**Responsibility**: Business logic, orchestrate repositories

**Rules**:
- Contain ALL business logic
- Call repository for data
- Transform/process data
- Enforce business rules
- NO HTTP concerns (req, res)
- NO database queries (use repository)

**Example**:

```typescript
// apps/backend-api/modules/settings/settings.service.ts
import { SettingsRepository } from './settings.repository'
import { AppError } from '@/utils/errors'
import { encrypt, decrypt } from '@/utils/crypto'
import type { Setting, CreateSettingData, UpdateSettingData } from './settings.types'

export class SettingsService {
  private repository: SettingsRepository

  constructor() {
    this.repository = new SettingsRepository()
  }

  async getAllByMandant(mandantId: string): Promise<Setting[]> {
    const settings = await this.repository.findByMandant(mandantId)

    // Business logic: Decrypt sensitive values
    return settings.map(setting => this.decryptSensitiveFields(setting))
  }

  async getById(id: string, mandantId: string): Promise<Setting | null> {
    const setting = await this.repository.findById(id)

    if (!setting) {
      return null
    }

    // Business rule: Users can only access their mandant's settings
    if (setting.mandantId !== mandantId) {
      throw new AppError('Access denied', 403)
    }

    return this.decryptSensitiveFields(setting)
  }

  async create(data: CreateSettingData): Promise<Setting> {
    // Business rule: Check for duplicate keys
    const existing = await this.repository.findByKey(data.key, data.mandantId)

    if (existing) {
      throw new AppError('Setting with this key already exists', 409)
    }

    // Business logic: Encrypt sensitive values
    const encryptedData = this.encryptSensitiveFields(data)

    const setting = await this.repository.create(encryptedData)

    return this.decryptSensitiveFields(setting)
  }

  async update(
    id: string,
    data: UpdateSettingData,
    mandantId: string
  ): Promise<Setting | null> {
    const existing = await this.repository.findById(id)

    if (!existing) {
      return null
    }

    // Business rule: Users can only update their mandant's settings
    if (existing.mandantId !== mandantId) {
      throw new AppError('Access denied', 403)
    }

    // Business logic: Encrypt sensitive values
    const encryptedData = this.encryptSensitiveFields(data)

    const updated = await this.repository.update(id, encryptedData)

    return updated ? this.decryptSensitiveFields(updated) : null
  }

  async delete(id: string, mandantId: string): Promise<void> {
    const existing = await this.repository.findById(id)

    if (!existing) {
      throw new AppError('Setting not found', 404)
    }

    // Business rule: Users can only delete their mandant's settings
    if (existing.mandantId !== mandantId) {
      throw new AppError('Access denied', 403)
    }

    await this.repository.delete(id)
  }

  // Private helper methods for business logic
  private decryptSensitiveFields(setting: Setting): Setting {
    if (setting.isSecret && setting.value) {
      return {
        ...setting,
        value: decrypt(setting.value)
      }
    }
    return setting
  }

  private encryptSensitiveFields(data: any): any {
    if (data.isSecret && data.value) {
      return {
        ...data,
        value: encrypt(data.value)
      }
    }
    return data
  }
}
```

---

### Layer 4: Repository (Data Access)

**Location**: `apps/backend-api/modules/[module]/[module].repository.ts`

**Responsibility**: Database operations only

**Rules**:
- ONLY database queries (Drizzle ORM)
- NO business logic
- NO validation
- Return raw data from database
- Simple CRUD operations

**Example**:

```typescript
// apps/backend-api/modules/settings/settings.repository.ts
import { db } from '@/db'
import { settings } from '@/db/schema'
import { eq, and } from 'drizzle-orm'
import type { Setting, CreateSettingData, UpdateSettingData } from './settings.types'

export class SettingsRepository {
  async findAll(): Promise<Setting[]> {
    return await db.select().from(settings)
  }

  async findByMandant(mandantId: string): Promise<Setting[]> {
    return await db.select()
      .from(settings)
      .where(eq(settings.mandantId, mandantId))
  }

  async findById(id: string): Promise<Setting | undefined> {
    return await db.query.settings.findFirst({
      where: eq(settings.id, id)
    })
  }

  async findByKey(key: string, mandantId: string): Promise<Setting | undefined> {
    return await db.query.settings.findFirst({
      where: and(
        eq(settings.key, key),
        eq(settings.mandantId, mandantId)
      )
    })
  }

  async create(data: CreateSettingData): Promise<Setting> {
    const [setting] = await db.insert(settings)
      .values(data)
      .returning()

    return setting
  }

  async update(id: string, data: UpdateSettingData): Promise<Setting | undefined> {
    const [updated] = await db.update(settings)
      .set({ ...data, updatedAt: new Date() })
      .where(eq(settings.id, id))
      .returning()

    return updated
  }

  async delete(id: string): Promise<void> {
    await db.delete(settings)
      .where(eq(settings.id, id))
  }
}
```

---

## Error Handling Pattern

### Use AppError for All Business Errors

```typescript
// apps/backend-api/utils/errors.ts
export class AppError extends Error {
  constructor(
    public message: string,
    public statusCode: number = 500,
    public code?: string
  ) {
    super(message)
    this.name = 'AppError'
  }
}

// Usage in services:
throw new AppError('User not found', 404)
throw new AppError('Invalid credentials', 401, 'INVALID_CREDENTIALS')
throw new AppError('Duplicate email', 409, 'DUPLICATE_EMAIL')
```

### Use asyncHandler for All Route Handlers

```typescript
// apps/backend-api/middleware/asyncHandler.ts
import { Request, Response, NextFunction } from 'express'

export const asyncHandler = (fn: Function) => {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next)
  }
}

// Usage in routes:
router.get('/', asyncHandler(controller.getAll.bind(controller)))
// No try-catch needed - asyncHandler catches and passes to error middleware
```

### Global Error Middleware

```typescript
// apps/backend-api/middleware/errorHandler.ts
import { Request, Response, NextFunction } from 'express'
import { AppError } from '@/utils/errors'

export const errorHandler = (
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  // Log error
  console.error('Error:', err)

  // Handle known AppError
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: err.message,
      code: err.code
    })
  }

  // Handle unknown errors (don't leak internal details)
  res.status(500).json({
    error: 'Internal server error'
  })
}

// Register in app.ts:
app.use(errorHandler)
```

---

## Validation Pattern

### Use Zod Schemas for Input Validation

**Location**: `apps/backend-api/modules/[module]/[module].validation.ts`

```typescript
// apps/backend-api/modules/settings/settings.validation.ts
import { z } from 'zod'

export const settingsSchemas = {
  create: z.object({
    body: z.object({
      key: z.string().min(1, 'Key is required'),
      value: z.string(),
      isSecret: z.boolean().optional().default(false),
      description: z.string().optional()
    })
  }),

  update: z.object({
    params: z.object({
      id: z.string().uuid('Invalid setting ID')
    }),
    body: z.object({
      value: z.string().optional(),
      isSecret: z.boolean().optional(),
      description: z.string().optional()
    })
  }),

  getById: z.object({
    params: z.object({
      id: z.string().uuid('Invalid setting ID')
    })
  })
}
```

### Validation Middleware

```typescript
// apps/backend-api/middleware/validation.ts
import { Request, Response, NextFunction } from 'express'
import { AnyZodObject, ZodError } from 'zod'
import { AppError } from '@/utils/errors'

export const validate = (schema: AnyZodObject) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      await schema.parseAsync({
        body: req.body,
        query: req.query,
        params: req.params
      })
      next()
    } catch (error) {
      if (error instanceof ZodError) {
        const message = error.errors.map(e => `${e.path.join('.')}: ${e.message}`).join(', ')
        return next(new AppError(message, 400, 'VALIDATION_ERROR'))
      }
      next(error)
    }
  }
}

// Usage in routes:
router.post('/',
  requireAuth,
  validate(settingsSchemas.create),
  asyncHandler(controller.create.bind(controller))
)
```

---

## Authentication & Authorization Pattern

### Authentication Middleware

```typescript
// apps/backend-api/middleware/auth.ts
import { Request, Response, NextFunction } from 'express'
import { AppError } from '@/utils/errors'

export const requireAuth = (req: Request, res: Response, next: NextFunction) => {
  if (!req.session?.userId) {
    throw new AppError('Authentication required', 401, 'UNAUTHORIZED')
  }
  next()
}

export const requireRole = (...roles: string[]) => {
  return (req: Request, res: Response, next: NextFunction) => {
    const userRole = req.session.role

    if (!userRole || !roles.includes(userRole)) {
      throw new AppError('Insufficient permissions', 403, 'FORBIDDEN')
    }

    next()
  }
}

// Usage:
router.get('/api/settings', requireAuth, controller.getAll)
router.post('/api/settings', requireAuth, requireRole('admin'), controller.create)
router.delete('/api/users/:id', requireAuth, requireRole('superadmin'), controller.delete)
```

---

## Module File Structure

Every backend module MUST have this structure:

```
apps/backend-api/modules/[module]/
  ├── [module].routes.ts       # Routes (Layer 1)
  ├── [module].controller.ts   # Controller (Layer 2)
  ├── [module].service.ts      # Service (Layer 3)
  ├── [module].repository.ts   # Repository (Layer 4)
  ├── [module].types.ts        # TypeScript types
  ├── [module].validation.ts   # Zod schemas
  └── __tests__/
      ├── [module].controller.test.ts
      ├── [module].service.test.ts
      └── [module].repository.test.ts
```

### Example: Settings Module

```
apps/backend-api/modules/settings/
  ├── settings.routes.ts       # HTTP routes
  ├── settings.controller.ts   # HTTP layer
  ├── settings.service.ts      # Business logic
  ├── settings.repository.ts   # Data access
  ├── settings.types.ts        # Types
  ├── settings.validation.ts   # Zod schemas
  └── __tests__/
      ├── settings.controller.test.ts
      ├── settings.service.test.ts
      └── settings.repository.test.ts
```

---

## Database Access Pattern

### Use Drizzle ORM for All Database Operations

```typescript
// ❌ NEVER use raw SQL
const result = await pool.query('SELECT * FROM users WHERE id = $1', [id])

// ✅ ALWAYS use Drizzle ORM
import { db } from '@/db'
import { users } from '@/db/schema'
import { eq } from 'drizzle-orm'

const user = await db.query.users.findFirst({
  where: eq(users.id, id)
})
```

### Common Drizzle Patterns

```typescript
// SELECT all
const allUsers = await db.select().from(users)

// SELECT with WHERE
const user = await db.select()
  .from(users)
  .where(eq(users.email, email))

// SELECT with multiple conditions
const users = await db.select()
  .from(users)
  .where(and(
    eq(users.mandantId, mandantId),
    eq(users.active, true)
  ))

// SELECT with relations
const user = await db.query.users.findFirst({
  where: eq(users.id, id),
  with: {
    mandant: true,
    profile: true
  }
})

// INSERT
const [newUser] = await db.insert(users)
  .values({ username, email, password })
  .returning()

// UPDATE
const [updated] = await db.update(users)
  .set({ email: newEmail, updatedAt: new Date() })
  .where(eq(users.id, id))
  .returning()

// DELETE
await db.delete(users)
  .where(eq(users.id, id))

// SEARCH (LIKE)
const results = await db.select()
  .from(users)
  .where(like(users.username, `%${searchTerm}%`))

// COUNT
const [{ count }] = await db.select({ count: sql`count(*)` })
  .from(users)
  .where(eq(users.mandantId, mandantId))
```

---

## Testing Pattern

### Test Each Layer Separately

#### Repository Tests

```typescript
// apps/backend-api/modules/settings/__tests__/settings.repository.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { SettingsRepository } from '../settings.repository'
import { db } from '@/db'
import { settings } from '@/db/schema'

describe('SettingsRepository', () => {
  let repository: SettingsRepository
  let testSettingId: string

  beforeEach(async () => {
    repository = new SettingsRepository()

    // Create test data
    const [setting] = await db.insert(settings).values({
      key: 'test_key',
      value: 'test_value',
      mandantId: 'test_mandant'
    }).returning()

    testSettingId = setting.id
  })

  afterEach(async () => {
    // Cleanup
    await db.delete(settings).where(eq(settings.id, testSettingId))
  })

  it('should find setting by ID', async () => {
    const result = await repository.findById(testSettingId)

    expect(result).toBeDefined()
    expect(result?.key).toBe('test_key')
  })

  it('should return undefined for non-existent ID', async () => {
    const result = await repository.findById('non-existent')

    expect(result).toBeUndefined()
  })
})
```

#### Service Tests

```typescript
// apps/backend-api/modules/settings/__tests__/settings.service.test.ts
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { SettingsService } from '../settings.service'
import { SettingsRepository } from '../settings.repository'
import { AppError } from '@/utils/errors'

// Mock repository
vi.mock('../settings.repository')

describe('SettingsService', () => {
  let service: SettingsService
  let mockRepository: any

  beforeEach(() => {
    mockRepository = {
      findById: vi.fn(),
      findByMandant: vi.fn(),
      create: vi.fn(),
      update: vi.fn(),
      delete: vi.fn()
    }

    service = new SettingsService()
    service['repository'] = mockRepository
  })

  it('should return decrypted settings', async () => {
    mockRepository.findByMandant.mockResolvedValue([
      { id: '1', key: 'secret', value: 'encrypted', isSecret: true }
    ])

    const result = await service.getAllByMandant('mandant1')

    expect(result).toHaveLength(1)
    expect(mockRepository.findByMandant).toHaveBeenCalledWith('mandant1')
  })

  it('should throw 403 when accessing other mandant settings', async () => {
    mockRepository.findById.mockResolvedValue({
      id: '1',
      mandantId: 'mandant2'
    })

    await expect(
      service.getById('1', 'mandant1')
    ).rejects.toThrow(AppError)
  })
})
```

#### Controller Tests

```typescript
// apps/backend-api/modules/settings/__tests__/settings.controller.test.ts
import { describe, it, expect, beforeEach } from 'vitest'
import request from 'supertest'
import { app } from '@/index'

describe('SettingsController', () => {
  let authCookie: string

  beforeEach(async () => {
    // Login to get auth cookie
    const loginResponse = await request(app)
      .post('/api/auth/login')
      .send({ username: 'admin', password: 'password' })

    authCookie = loginResponse.headers['set-cookie']
  })

  it('should get all settings (authenticated)', async () => {
    const response = await request(app)
      .get('/api/settings')
      .set('Cookie', authCookie)

    expect(response.status).toBe(200)
    expect(Array.isArray(response.body)).toBe(true)
  })

  it('should return 401 without authentication', async () => {
    const response = await request(app)
      .get('/api/settings')

    expect(response.status).toBe(401)
  })

  it('should create setting (admin only)', async () => {
    const response = await request(app)
      .post('/api/settings')
      .set('Cookie', authCookie)
      .send({
        key: 'new_key',
        value: 'new_value'
      })

    expect(response.status).toBe(201)
    expect(response.body.key).toBe('new_key')
  })
})
```

---

## Quick Reference

### Creating a New Backend Module

1. Create directory: `apps/backend-api/modules/[module]/`
2. Create files in order:
   - `[module].types.ts` - Define TypeScript types
   - `[module].validation.ts` - Define Zod schemas
   - `[module].repository.ts` - Database access (Layer 4)
   - `[module].service.ts` - Business logic (Layer 3)
   - `[module].controller.ts` - HTTP layer (Layer 2)
   - `[module].routes.ts` - Routes (Layer 1)
3. Register routes in `apps/backend-api/routes/index.ts`
4. Write tests for each layer

### Layer Responsibilities

| Layer | File | Responsibilities | NO |
|-------|------|------------------|-----|
| **Routes** | `.routes.ts` | Define endpoints, middleware | Business logic, DB access |
| **Controller** | `.controller.ts` | Extract req data, call service, return res | Business logic, DB access |
| **Service** | `.service.ts` | Business logic, orchestrate repositories | HTTP concerns, DB queries |
| **Repository** | `.repository.ts` | Database queries only | Business logic, validation |

---

Created: 2025-10-13
Last Updated: 2025-10-13
Status: Active - Required for all new backend code
Reference: See `LEGACY_PATTERNS_TO_AVOID.md` for anti-patterns
