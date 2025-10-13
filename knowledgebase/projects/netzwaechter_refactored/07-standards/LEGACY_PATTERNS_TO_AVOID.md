# Legacy Patterns to Avoid

Created: 2025-10-13

This document lists **DEPRECATED patterns** that exist in the codebase but should NOT be used in new code. When AI suggests these patterns, reject them and use the modern alternatives instead.

---

## CRITICAL: Old API Clients (DEPRECATED)

### DO NOT USE

❌ **src/features/shared/api/apiClient.ts**
❌ **src/features/shared/api/api-utils.ts**
❌ **Direct fetch() calls in components**
❌ **Direct axios calls in components**

### REASON

- No cache management
- No automatic retries
- No request deduplication
- No background refetching
- Inconsistent error handling
- Manual loading state management
- No optimistic updates
- Stale data problems

### USE INSTEAD

✅ **TanStack Query hooks** in `src/features/shared/hooks/api/`

#### Example: Fetching Data

```typescript
// ❌ BAD (deprecated)
import { apiClient } from '@/features/shared/api/apiClient'

function MyComponent() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    apiClient.get('/api/settings')
      .then(res => setData(res))
      .finally(() => setLoading(false))
  }, [])
}

// ✅ GOOD (current standard)
import { useSettings } from '@/features/shared/hooks/api/useSettings'

function MyComponent() {
  const { data, isLoading, error } = useSettings()
  // Cache, retries, refetching all handled automatically
}
```

#### Example: Mutations

```typescript
// ❌ BAD (deprecated)
import { apiClient } from '@/features/shared/api/apiClient'

async function updateSettings(values) {
  try {
    await apiClient.post('/api/settings', values)
    // Must manually refetch data
  } catch (error) {
    // Manual error handling
  }
}

// ✅ GOOD (current standard)
import { useUpdateSettings } from '@/features/shared/hooks/api/useSettings'

function MyComponent() {
  const mutation = useUpdateSettings()

  const handleSubmit = (values) => {
    mutation.mutate(values, {
      onSuccess: () => {
        // Cache automatically invalidated
      }
    })
  }
}
```

**Migration Priority**: P0 - Do not use in any new code

---

## Backend: Old Controller Patterns (DEPRECATED)

### DO NOT USE

❌ **Controllers with direct database access**
❌ **Controllers with business logic**
❌ **Mixing route definitions and controller logic in same file**

### REASON

- Violates separation of concerns
- Makes testing difficult
- Creates tight coupling
- No code reuse
- Hard to maintain

### USE INSTEAD

✅ **4-Layer Pattern**: Routes → Controller → Service → Repository

#### Example: Proper Backend Structure

```typescript
// ❌ BAD (deprecated pattern found in legacy modules)
// apps/backend-api/modules/legacy/settings.ts
router.get('/api/settings', async (req, res) => {
  const settings = await db.select().from(settingsTable)
  const processedSettings = settings.map(s => ({
    ...s,
    value: decrypt(s.value) // Business logic in route!
  }))
  res.json(processedSettings)
})

// ✅ GOOD (current 4-layer pattern)
// apps/backend-api/modules/settings/settings.routes.ts
router.get('/', asyncHandler(controller.getAll))

// apps/backend-api/modules/settings/settings.controller.ts
export class SettingsController {
  async getAll(req: Request, res: Response) {
    const settings = await this.service.getAll()
    res.json(settings)
  }
}

// apps/backend-api/modules/settings/settings.service.ts
export class SettingsService {
  async getAll() {
    const settings = await this.repository.findAll()
    return settings.map(s => this.decryptValue(s))
  }

  private decryptValue(setting: Setting) {
    return { ...setting, value: decrypt(setting.value) }
  }
}

// apps/backend-api/modules/settings/settings.repository.ts
export class SettingsRepository {
  async findAll() {
    return await db.select().from(settingsTable)
  }
}
```

**Migration Priority**: P0 - All new modules MUST use 4-layer pattern

**Reference**: See `.archon-knowledge-base/07-standards/BACKEND_PATTERNS.md` for complete guide

---

## Frontend: Old Form Patterns (DEPRECATED)

### DO NOT USE

❌ **Manual form state management with useState**
❌ **Manual validation with if/else chains**
❌ **Forms without schema validation**

### REASON

- Verbose and error-prone
- Inconsistent validation
- No type safety
- Hard to test
- Poor error messages

### USE INSTEAD

✅ **React Hook Form + Zod** for all forms

#### Example: Form Implementation

```typescript
// ❌ BAD (deprecated)
function MyForm() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [errors, setErrors] = useState({})

  const handleSubmit = async (e) => {
    e.preventDefault()
    const newErrors = {}

    if (!name) newErrors.name = 'Required'
    if (!email.includes('@')) newErrors.email = 'Invalid email'

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    await fetch('/api/users', {
      method: 'POST',
      body: JSON.stringify({ name, email })
    })
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={name} onChange={e => setName(e.target.value)} />
      {errors.name && <span>{errors.name}</span>}
      <input value={email} onChange={e => setEmail(e.target.value)} />
      {errors.email && <span>{errors.email}</span>}
      <button type="submit">Submit</button>
    </form>
  )
}

// ✅ GOOD (current standard)
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useCreateUser } from '@/features/shared/hooks/api/useUsers'

const schema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email address')
})

type FormData = z.infer<typeof schema>

function MyForm() {
  const form = useForm<FormData>({
    resolver: zodResolver(schema)
  })

  const mutation = useCreateUser()

  const onSubmit = (data: FormData) => {
    mutation.mutate(data)
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <input {...form.register('name')} />
      {form.formState.errors.name?.message}

      <input {...form.register('email')} />
      {form.formState.errors.email?.message}

      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  )
}
```

**Migration Priority**: P1 - Use for all new forms

**Reference**: See `.archon-knowledge-base/07-standards/FRONTEND_PATTERNS.md`

---

## Authentication: Inconsistent Auth Checks (DEPRECATED)

### DO NOT USE

❌ **Manual auth checks in controllers**
❌ **Different auth patterns across modules**
❌ **No role-based access control**

### REASON

- Security vulnerabilities
- Inconsistent behavior
- Hard to audit
- Difficult to change auth logic

### USE INSTEAD

✅ **Centralized middleware**: `requireAuth` and `requireRole`

#### Example: Protected Routes

```typescript
// ❌ BAD (deprecated - found in legacy modules)
router.get('/api/settings', async (req, res) => {
  if (!req.session?.userId) {
    return res.status(401).json({ error: 'Unauthorized' })
  }
  // ... controller logic
})

// ✅ GOOD (current standard)
import { requireAuth, requireRole } from '@/middleware/auth'

// Require authentication
router.get('/api/settings', requireAuth, asyncHandler(controller.getAll))

// Require specific role
router.post('/api/settings',
  requireAuth,
  requireRole('admin'),
  asyncHandler(controller.create)
)

// Require superadmin
router.delete('/api/users/:id',
  requireAuth,
  requireRole('superadmin'),
  asyncHandler(controller.delete)
)
```

**Migration Priority**: P0 - Security critical

**Reference**: See `.archon-knowledge-base/03-authentication/MIDDLEWARE.md`

---

## Database: Raw SQL Queries (DEPRECATED)

### DO NOT USE

❌ **Raw SQL with template strings**
❌ **String concatenation for queries**
❌ **Manual parameter binding**

### REASON

- SQL injection vulnerabilities
- No type safety
- Hard to test
- Database-specific syntax
- Difficult refactoring

### USE INSTEAD

✅ **Drizzle ORM** for all database operations

#### Example: Database Queries

```typescript
// ❌ BAD (deprecated)
import { pool } from '@/connection-pool'

async function getUser(id: string) {
  const result = await pool.query(
    `SELECT * FROM users WHERE id = $1`,
    [id]
  )
  return result.rows[0]
}

async function searchUsers(name: string) {
  // SQL INJECTION VULNERABILITY!
  const result = await pool.query(
    `SELECT * FROM users WHERE name LIKE '%${name}%'`
  )
  return result.rows
}

// ✅ GOOD (current standard)
import { db } from '@/db'
import { users } from '@/db/schema'
import { eq, like } from 'drizzle-orm'

async function getUser(id: string) {
  return await db.query.users.findFirst({
    where: eq(users.id, id)
  })
}

async function searchUsers(name: string) {
  // Safe from SQL injection
  return await db.select()
    .from(users)
    .where(like(users.name, `%${name}%`))
}
```

**Migration Priority**: P0 - Security critical

**Reference**: See `.archon-knowledge-base/01-database/DRIZZLE_PATTERNS.md`

---

## Error Handling: Inconsistent Patterns (DEPRECATED)

### DO NOT USE

❌ **Try-catch in every controller**
❌ **Inconsistent error responses**
❌ **Exposing internal errors to client**

### REASON

- Verbose and repetitive
- Security risks (error leaks)
- Inconsistent error format
- Hard to add logging/monitoring

### USE INSTEAD

✅ **AppError + asyncHandler** for consistent error handling

#### Example: Error Handling

```typescript
// ❌ BAD (deprecated)
router.get('/api/users/:id', async (req, res) => {
  try {
    const user = await db.query.users.findFirst({
      where: eq(users.id, req.params.id)
    })

    if (!user) {
      return res.status(404).json({ error: 'User not found' })
    }

    res.json(user)
  } catch (error) {
    console.error(error)
    res.status(500).json({ error: error.message }) // Leaks internal errors!
  }
})

// ✅ GOOD (current standard)
import { asyncHandler } from '@/middleware/asyncHandler'
import { AppError } from '@/utils/errors'

router.get('/api/users/:id', asyncHandler(async (req, res) => {
  const user = await userService.getById(req.params.id)

  if (!user) {
    throw new AppError('User not found', 404)
  }

  res.json(user)
  // Errors automatically caught, logged, and formatted by middleware
}))
```

**Migration Priority**: P0 - Security and consistency critical

**Reference**: See `.archon-knowledge-base/07-standards/BACKEND_PATTERNS.md`

---

## State Management: Wrong Tool for Job (DEPRECATED)

### DO NOT USE

❌ **TanStack Query for UI state (modals, tabs, etc.)**
❌ **Zustand for server data**
❌ **Props drilling instead of context**

### REASON

- Wrong abstraction
- Performance issues
- Unnecessary complexity
- Hard to debug

### USE INSTEAD

✅ **Use the right tool for each type of state**

#### State Management Decision Tree

```typescript
// Server State (data from API) → TanStack Query
const { data: users } = useUsers()

// Complex Client State (global UI state, multi-component) → Zustand
const { theme, setTheme } = useThemeStore()

// Simple Client State (local UI state) → useState
const [isOpen, setIsOpen] = useState(false)

// Shared Context (auth, settings) → React Context
const { user } = useAuth()
```

#### Examples

```typescript
// ❌ BAD: TanStack Query for modal state
const { data: isModalOpen, mutate: setModalOpen } = useMutation(...)

// ✅ GOOD: useState for local UI state
const [isModalOpen, setModalOpen] = useState(false)

// ❌ BAD: Zustand for API data
const users = useUsersStore(state => state.users)
// Must manually fetch, update, invalidate

// ✅ GOOD: TanStack Query for server data
const { data: users } = useUsers()
// Cache, refetch, invalidation handled automatically

// ❌ BAD: Props drilling through 5 components
<Parent theme={theme}>
  <Child theme={theme}>
    <GrandChild theme={theme}>
      <GreatGrandChild theme={theme} />
    </GrandChild>
  </Child>
</Parent>

// ✅ GOOD: Context for shared state
const { theme } = useTheme()
// Available in any child component
```

**Migration Priority**: P1 - Improves architecture and performance

**Reference**: See `.archon-knowledge-base/07-standards/FRONTEND_PATTERNS.md`

---

## Testing: Incomplete Test Patterns (DEPRECATED)

### DO NOT USE

❌ **Tests without cleanup**
❌ **Tests with hardcoded IDs**
❌ **No error case testing**
❌ **Skipped tests in production code**

### REASON

- Flaky tests
- Tests affect each other
- False positives
- No confidence in test suite

### USE INSTEAD

✅ **Complete test patterns with setup/teardown**

#### Example: Proper Test Structure

```typescript
// ❌ BAD (deprecated)
describe('Users API', () => {
  it('should get user', async () => {
    const response = await request(app).get('/api/users/123')
    expect(response.status).toBe(200)
  })
})

// ✅ GOOD (current standard)
import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import request from 'supertest'
import { app } from '@/index'
import { db } from '@/db'
import { users } from '@/db/schema'

describe('Users API', () => {
  let testUserId: string

  beforeEach(async () => {
    // Setup: Create test data
    const [user] = await db.insert(users).values({
      username: 'testuser',
      email: 'test@example.com',
      password: 'hashed_password'
    }).returning()
    testUserId = user.id
  })

  afterEach(async () => {
    // Cleanup: Remove test data
    await db.delete(users).where(eq(users.id, testUserId))
  })

  it('should get user by ID', async () => {
    const response = await request(app).get(`/api/users/${testUserId}`)

    expect(response.status).toBe(200)
    expect(response.body).toMatchObject({
      id: testUserId,
      username: 'testuser',
      email: 'test@example.com'
    })
  })

  it('should return 404 for non-existent user', async () => {
    const response = await request(app).get('/api/users/nonexistent')

    expect(response.status).toBe(404)
    expect(response.body.error).toBe('User not found')
  })

  it('should return 401 without authentication', async () => {
    const response = await request(app)
      .get(`/api/users/${testUserId}`)
      // No session cookie

    expect(response.status).toBe(401)
  })
})
```

**Migration Priority**: P1 - Improves reliability

**Reference**: See `.archon-knowledge-base/07-standards/TESTING_PATTERNS.md`

---

## Module Organization: Flat Structure (DEPRECATED)

### DO NOT USE

❌ **All files in single directory**
❌ **No feature-based organization**
❌ **Mixing concerns in same file**

### REASON

- Hard to navigate
- Unclear dependencies
- Difficult to maintain
- No clear ownership

### USE INSTEAD

✅ **Feature-based directory structure**

#### Backend Module Structure

```
apps/backend-api/modules/
  ├── settings/
  │   ├── settings.routes.ts       # Routes only
  │   ├── settings.controller.ts   # HTTP layer
  │   ├── settings.service.ts      # Business logic
  │   ├── settings.repository.ts   # Data access
  │   ├── settings.types.ts        # TypeScript types
  │   ├── settings.validation.ts   # Zod schemas
  │   └── __tests__/
  │       ├── settings.controller.test.ts
  │       ├── settings.service.test.ts
  │       └── settings.repository.test.ts
```

#### Frontend Feature Structure

```
apps/frontend-web/src/features/
  ├── settings/
  │   ├── components/
  │   │   ├── SettingsForm.tsx
  │   │   └── SettingsCard.tsx
  │   ├── hooks/
  │   │   └── useSettingsForm.ts
  │   ├── pages/
  │   │   └── SettingsPage.tsx
  │   └── types/
  │       └── settings.types.ts
```

**Migration Priority**: P2 - Apply to new features

**Reference**: See `.archon-knowledge-base/05-backend/MODULE_STRUCTURE.md`

---

## Environment Variables: Hardcoded Values (DEPRECATED)

### DO NOT USE

❌ **Hardcoded configuration**
❌ **Different env var names in code vs .env**
❌ **No validation of env vars**
❌ **Accessing process.env directly everywhere**

### REASON

- Not deployable to different environments
- Configuration errors discovered at runtime
- No type safety
- Hard to change configuration

### USE INSTEAD

✅ **Centralized configuration with validation**

#### Example: Configuration Management

```typescript
// ❌ BAD (deprecated)
// Scattered throughout codebase
const dbUrl = process.env.DATABASE_URL || 'postgresql://localhost:5432/db'
const port = parseInt(process.env.PORT) || 3000

// ✅ GOOD (current standard)
// apps/backend-api/config/index.ts
import { z } from 'zod'

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  PORT: z.string().transform(val => parseInt(val, 10)),
  NODE_ENV: z.enum(['development', 'production', 'test']),
  SESSION_SECRET: z.string().min(32),
  ALLOWED_ORIGIN: z.string().url()
})

const env = envSchema.parse(process.env)

export const config = {
  database: {
    url: env.DATABASE_URL
  },
  server: {
    port: env.PORT,
    env: env.NODE_ENV
  },
  session: {
    secret: env.SESSION_SECRET
  },
  cors: {
    origin: env.ALLOWED_ORIGIN
  }
} as const

// Usage everywhere:
import { config } from '@/config'
console.log(config.server.port) // Type-safe, validated
```

**Migration Priority**: P1 - Improves reliability and deployment

**Reference**: See `.archon-knowledge-base/06-configuration/ENVIRONMENT_VARIABLES.md`

---

## Summary: Quick Reference

### Immediate Replacements (P0 - Do Not Use in New Code)

1. ❌ `apiClient.ts` / `api-utils.ts` → ✅ TanStack Query hooks
2. ❌ Raw SQL queries → ✅ Drizzle ORM
3. ❌ Manual auth checks → ✅ `requireAuth` / `requireRole` middleware
4. ❌ Try-catch everywhere → ✅ `asyncHandler` + `AppError`
5. ❌ Controllers with business logic → ✅ 4-layer pattern

### High Priority Replacements (P1 - Migrate Soon)

6. ❌ Manual forms → ✅ React Hook Form + Zod
7. ❌ Wrong state management → ✅ Right tool for job
8. ❌ Incomplete tests → ✅ Setup/teardown + error cases
9. ❌ Hardcoded config → ✅ Validated environment variables

### Medium Priority (P2 - Plan for Refactoring)

10. ❌ Flat structure → ✅ Feature-based organization

---

## How to Use This Document

**When AI suggests deprecated patterns:**

1. Recognize the pattern in this document
2. Reject the suggestion
3. Request the modern alternative
4. Reference the specific section of this document

**When reviewing code:**

1. Check for any patterns listed here
2. Flag them for refactoring
3. Prioritize by P0 → P1 → P2
4. Use examples as migration guide

**When writing new code:**

1. Never use deprecated patterns
2. Follow current standards
3. Refer to detailed pattern docs
4. Ask if unsure

---

Created: 2025-10-13
Last Updated: 2025-10-13
Status: Active - Enforce in all new code
Priority: CRITICAL - AI must follow these guidelines
