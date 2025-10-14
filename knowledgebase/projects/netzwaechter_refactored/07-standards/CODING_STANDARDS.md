# Coding Standards - Netzwächter Project

Created: 2025-10-13

This document defines coding style, naming conventions, and best practices for the Netzwächter project.

---

## TypeScript Standards

### Always Use Strict Mode

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

### Type Definitions

```typescript
// ✅ GOOD: Explicit types for function parameters and return values
function getUserById(id: string): Promise<User | null> {
  return db.query.users.findFirst({ where: eq(users.id, id) })
}

// ❌ BAD: Implicit any types
function getUserById(id) {
  return db.query.users.findFirst({ where: eq(users.id, id) })
}

// ✅ GOOD: Interface for object shapes
interface User {
  id: string
  username: string
  email: string
  role: 'superadmin' | 'admin' | 'user'
  mandantId: string
  createdAt: Date
  updatedAt: Date
}

// ❌ BAD: Using 'any'
interface User {
  id: string
  username: string
  data: any // Don't use any!
}

// ✅ GOOD: Unknown for values you'll type-guard
function processData(data: unknown) {
  if (typeof data === 'string') {
    return data.toUpperCase()
  }
  if (typeof data === 'object' && data !== null) {
    return JSON.stringify(data)
  }
  throw new Error('Invalid data type')
}
```

### Type vs Interface

```typescript
// Use INTERFACE for object shapes
interface User {
  id: string
  username: string
}

// Use TYPE for:
// 1. Unions
type Role = 'superadmin' | 'admin' | 'user'

// 2. Intersections
type AdminUser = User & { permissions: string[] }

// 3. Mapped types
type Readonly<T> = {
  readonly [P in keyof T]: T[P]
}

// 4. Conditional types
type NonNullable<T> = T extends null | undefined ? never : T
```

---

## Naming Conventions

### General Rules

| Type | Convention | Example |
|------|------------|---------|
| **Variables** | camelCase | `userName`, `isActive` |
| **Constants** | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT`, `API_URL` |
| **Functions** | camelCase | `getUserById`, `calculateTotal` |
| **Classes** | PascalCase | `UserService`, `SettingsController` |
| **Interfaces** | PascalCase | `User`, `Setting`, `ApiResponse` |
| **Types** | PascalCase | `UserId`, `RoleType` |
| **Enums** | PascalCase | `UserRole`, `HttpStatus` |
| **Files** | kebab-case | `user-service.ts`, `settings.controller.ts` |
| **React Components** | PascalCase | `UserProfile.tsx`, `SettingsForm.tsx` |

### Examples

```typescript
// ✅ GOOD: Consistent naming
const MAX_RETRY_COUNT = 3
const userName = 'john'
let isActive = true

class UserService {
  async getUserById(id: string): Promise<User | null> {
    return await this.repository.findById(id)
  }
}

interface User {
  id: string
  username: string
}

type UserId = string

// ❌ BAD: Inconsistent naming
const max_retry_count = 3 // Should be UPPER_SNAKE_CASE
const UserName = 'john' // Should be camelCase
let IsActive = true // Should be camelCase

class userService { // Should be PascalCase
  async GetUserById(id: string): Promise<User | null> { // Should be camelCase
    return await this.repository.findById(id)
  }
}
```

### Boolean Variables

```typescript
// ✅ GOOD: Use is/has/can/should prefix
const isActive = true
const hasPermission = false
const canEdit = true
const shouldRetry = false

// ❌ BAD: Ambiguous names
const active = true // Is it a verb or adjective?
const permission = false // Is it the permission or a boolean?
```

### Function Names

```typescript
// ✅ GOOD: Verb-based names
function getUser() { }
function createSetting() { }
function updatePassword() { }
function deleteRecord() { }
function validateInput() { }
function calculateTotal() { }

// ❌ BAD: Noun-based names
function user() { } // What does this do?
function setting() { } // Get? Create? Update?
```

---

## File Organization

### Import Order

```typescript
// 1. Node.js built-ins
import { readFile } from 'fs/promises'
import crypto from 'crypto'

// 2. External dependencies
import express from 'express'
import { z } from 'zod'

// 3. Internal modules (aliased imports)
import { db } from '@/db'
import { AppError } from '@/utils/errors'

// 4. Relative imports (same feature)
import { UserService } from './user.service'
import { userSchema } from './user.validation'

// 5. Type imports (last)
import type { User, CreateUserData } from './user.types'
```

### Export Order

```typescript
// 1. Constants
export const MAX_RETRY_COUNT = 3

// 2. Types/Interfaces
export interface User {
  id: string
  username: string
}

export type UserId = string

// 3. Classes
export class UserService {
  // ...
}

// 4. Functions
export function validateUser(user: User): boolean {
  // ...
}

// 5. Default export (if needed, prefer named exports)
export default UserService
```

---

## Function Best Practices

### Function Length

**Rule**: Functions should be **< 50 lines** (ideally < 30)

```typescript
// ✅ GOOD: Small, focused function
function calculateTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0)
}

// ❌ BAD: Too long (split into smaller functions)
function processOrder(order: Order) {
  // 100+ lines of validation, calculation, database updates, etc.
  // Split this into smaller functions!
}

// ✅ GOOD: Split into focused functions
function processOrder(order: Order) {
  validateOrder(order)
  const total = calculateOrderTotal(order)
  const tax = calculateTax(total)
  const finalAmount = total + tax
  return createInvoice(order, finalAmount)
}
```

### Function Parameters

**Rule**: Max **3-4 parameters**. Use object for more.

```typescript
// ✅ GOOD: Few parameters
function createUser(username: string, email: string, role: string) {
  // ...
}

// ❌ BAD: Too many parameters
function createUser(
  username: string,
  email: string,
  password: string,
  role: string,
  mandantId: string,
  isActive: boolean,
  createdBy: string
) {
  // Hard to remember order!
}

// ✅ GOOD: Use object for many parameters
interface CreateUserParams {
  username: string
  email: string
  password: string
  role: string
  mandantId: string
  isActive?: boolean
  createdBy: string
}

function createUser(params: CreateUserParams) {
  // Clear and extensible
}

// Usage:
createUser({
  username: 'john',
  email: 'john@example.com',
  password: 'hashed',
  role: 'user',
  mandantId: 'mandant1',
  createdBy: 'admin'
})
```

### Single Responsibility

```typescript
// ✅ GOOD: Each function does ONE thing
function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

function sendWelcomeEmail(user: User): Promise<void> {
  return emailService.send({
    to: user.email,
    subject: 'Welcome!',
    template: 'welcome'
  })
}

function createUser(data: CreateUserData): Promise<User> {
  return userRepository.create(data)
}

// ❌ BAD: Function does too many things
async function createUserAndSendEmail(data: CreateUserData): Promise<User> {
  // Validates email
  if (!validateEmail(data.email)) {
    throw new Error('Invalid email')
  }

  // Creates user
  const user = await userRepository.create(data)

  // Sends email
  await emailService.send({
    to: user.email,
    subject: 'Welcome!',
    template: 'welcome'
  })

  // Updates analytics
  await analytics.track('user_created', { userId: user.id })

  return user
}

// Split into separate functions with clear responsibilities!
```

---

## Error Handling

### Use Custom Error Classes

```typescript
// Define custom errors
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

export class NotFoundError extends AppError {
  constructor(message: string) {
    super(message, 404, 'NOT_FOUND')
  }
}

export class ValidationError extends AppError {
  constructor(message: string) {
    super(message, 400, 'VALIDATION_ERROR')
  }
}

// ✅ GOOD: Throw specific errors
function getUserById(id: string): Promise<User> {
  const user = await userRepository.findById(id)

  if (!user) {
    throw new NotFoundError('User not found')
  }

  return user
}

// ❌ BAD: Generic error strings
function getUserById(id: string): Promise<User> {
  const user = await userRepository.findById(id)

  if (!user) {
    throw new Error('not found') // No context!
  }

  return user
}
```

### Always Catch Async Errors

```typescript
// ✅ GOOD: Use asyncHandler wrapper
router.get('/', asyncHandler(controller.getAll.bind(controller)))

// ❌ BAD: Unhandled promise rejection
router.get('/', controller.getAll.bind(controller))
// If controller throws, it's an unhandled rejection!

// ✅ GOOD: Try-catch in service for specific error handling
async function updateUser(id: string, data: UpdateUserData): Promise<User> {
  try {
    return await userRepository.update(id, data)
  } catch (error) {
    if (error.code === '23505') { // PostgreSQL unique violation
      throw new ValidationError('Username already exists')
    }
    throw error // Re-throw unknown errors
  }
}
```

---

## Comments & Documentation

### When to Comment

```typescript
// ✅ GOOD: Comment WHY, not WHAT
// Using Argon2id because it's resistant to GPU attacks
const hash = await argon2.hash(password, { type: argon2.argon2id })

// ❌ BAD: Commenting obvious code
// Hash the password
const hash = await argon2.hash(password)

// ✅ GOOD: Explain complex business logic
// Calculate discount: 10% for orders > $100, 15% for > $500
const discount = total > 500 ? 0.15 : total > 100 ? 0.10 : 0

// ✅ GOOD: Warn about gotchas
// NOTE: This must run BEFORE authentication middleware
app.use(sessionMiddleware)
app.use(requireAuth)

// ✅ GOOD: Document workarounds
// WORKAROUND: Drizzle doesn't support window functions yet
// Using raw SQL until https://github.com/drizzle-team/drizzle-orm/issues/123 is fixed
const result = await db.execute(sql`SELECT *, ROW_NUMBER() OVER (PARTITION BY mandant_id ORDER BY created_at) as rn FROM users`)
```

### JSDoc for Public APIs

```typescript
/**
 * Get user by ID
 *
 * @param id - User UUID
 * @returns User object if found, null otherwise
 * @throws {NotFoundError} If user not found
 * @throws {ValidationError} If ID is invalid
 *
 * @example
 * const user = await getUserById('123e4567-e89b-12d3-a456-426614174000')
 */
export async function getUserById(id: string): Promise<User | null> {
  // ...
}
```

### TODO Comments

```typescript
// TODO: Add pagination (limit/offset)
function getUsers(): Promise<User[]> {
  return userRepository.findAll()
}

// TODO(username): Implement caching
// Created: 2025-10-13
// Priority: P1
function getSettings(): Promise<Setting[]> {
  return settingsRepository.findAll()
}

// FIXME: This breaks for very large files
function uploadFile(file: File): Promise<void> {
  return fileService.upload(file)
}
```

---

## Code Style

### Prefer Const Over Let

```typescript
// ✅ GOOD: Use const for values that don't change
const MAX_RETRY_COUNT = 3
const user = await getUserById('123')
const isActive = user.active

// ✅ GOOD: Use let only when value changes
let retryCount = 0
while (retryCount < MAX_RETRY_COUNT) {
  retryCount++
  // ...
}

// ❌ BAD: Using let unnecessarily
let MAX_RETRY_COUNT = 3 // Should be const
let user = await getUserById('123') // Should be const
```

### Arrow Functions vs Function Declarations

```typescript
// ✅ GOOD: Arrow functions for callbacks
const users = await Promise.all(
  ids.map(id => getUserById(id))
)

items.filter(item => item.active)
  .map(item => item.name)

// ✅ GOOD: Function declarations for named functions
function calculateTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price, 0)
}

// ✅ GOOD: Arrow functions for object methods (preserve 'this')
class UserService {
  private repository: UserRepository

  getById = async (id: string): Promise<User | null> => {
    return await this.repository.findById(id)
  }
}
```

### Destructuring

```typescript
// ✅ GOOD: Destructure objects
const { username, email, role } = user
const { params, body, session } = req

// ❌ BAD: Accessing properties repeatedly
const username = user.username
const email = user.email
const role = user.role

// ✅ GOOD: Destructure with defaults
const { retryCount = 3, timeout = 5000 } = options

// ✅ GOOD: Rest parameters
const { password, ...userWithoutPassword } = user
```

### Template Literals

```typescript
// ✅ GOOD: Use template literals for interpolation
const message = `Welcome, ${username}!`
const url = `${baseUrl}/api/users/${userId}`

// ❌ BAD: String concatenation
const message = 'Welcome, ' + username + '!'
const url = baseUrl + '/api/users/' + userId
```

### Optional Chaining

```typescript
// ✅ GOOD: Use optional chaining
const userId = req.session?.userId
const mandantId = user?.mandant?.id

// ❌ BAD: Manual checks
const userId = req.session && req.session.userId
const mandantId = user && user.mandant && user.mandant.id
```

### Nullish Coalescing

```typescript
// ✅ GOOD: Use ?? for null/undefined checks
const retryCount = options.retryCount ?? 3
const username = user.username ?? 'Anonymous'

// ❌ BAD: Using || (treats 0, '', false as falsy)
const retryCount = options.retryCount || 3
// If retryCount is 0, this returns 3!

// ✅ GOOD: || only for boolean coercion
const isActive = user.active || false
```

---

## React/JSX Standards

### Component Definition

```typescript
// ✅ GOOD: Typed functional component
interface UserProfileProps {
  user: User
  onEdit: (user: User) => void
}

export function UserProfile({ user, onEdit }: UserProfileProps) {
  return (
    <div>
      <h2>{user.username}</h2>
      <button onClick={() => onEdit(user)}>Edit</button>
    </div>
  )
}

// ❌ BAD: Untyped component
export function UserProfile({ user, onEdit }) {
  return (
    <div>
      <h2>{user.username}</h2>
      <button onClick={() => onEdit(user)}>Edit</button>
    </div>
  )
}
```

### Hooks Rules

```typescript
// ✅ GOOD: Hooks at top level
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading } = useUser(userId)
  const [isEditing, setIsEditing] = useState(false)

  if (isLoading) return <Spinner />

  return <div>{/* ... */}</div>
}

// ❌ BAD: Conditional hooks
function UserProfile({ userId }: { userId: string }) {
  if (!userId) return null

  // This breaks Rules of Hooks!
  const { data: user } = useUser(userId)

  return <div>{/* ... */}</div>
}

// ✅ GOOD: Custom hooks follow naming convention
function useUserForm(user: User) {
  const form = useForm()
  const mutation = useUpdateUser()

  // ...

  return { form, onSubmit, isSubmitting }
}
```

### Event Handlers

```typescript
// ✅ GOOD: Named handler functions
function UserForm() {
  const handleSubmit = (data: FormData) => {
    mutation.mutate(data)
  }

  const handleCancel = () => {
    router.push('/users')
  }

  return (
    <form onSubmit={handleSubmit}>
      <button type="submit">Save</button>
      <button type="button" onClick={handleCancel}>Cancel</button>
    </form>
  )
}

// ❌ BAD: Inline anonymous functions
function UserForm() {
  return (
    <form onSubmit={(e) => {
      e.preventDefault()
      mutation.mutate(data)
    }}>
      <button type="button" onClick={() => router.push('/users')}>Cancel</button>
    </form>
  )
}
```

---

## Testing Standards

### Test Naming

```typescript
describe('UserService', () => {
  describe('getById', () => {
    it('should return user when found', async () => {
      // ...
    })

    it('should return null when user not found', async () => {
      // ...
    })

    it('should throw 403 when accessing other mandant user', async () => {
      // ...
    })
  })
})
```

### Arrange-Act-Assert Pattern

```typescript
it('should return user when found', async () => {
  // Arrange
  const mockUser = { id: '1', username: 'john' }
  mockRepository.findById.mockResolvedValue(mockUser)

  // Act
  const result = await service.getById('1', 'mandant1')

  // Assert
  expect(result).toEqual(mockUser)
  expect(mockRepository.findById).toHaveBeenCalledWith('1')
})
```

---

## Git Commit Standards

### Commit Message Format

```
type(scope): subject

body

footer
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring (no behavior change)
- `test`: Adding/updating tests
- `docs`: Documentation only
- `style`: Code style (formatting, semicolons, etc.)
- `chore`: Maintenance (dependencies, build, etc.)
- `perf`: Performance improvement

### Examples

```bash
# Good commits
git commit -m "feat(settings): add encryption for secret values"
git commit -m "fix(auth): prevent session fixation vulnerability"
git commit -m "refactor(users): extract password hashing to utility"
git commit -m "test(settings): add integration tests for API endpoints"

# Bad commits
git commit -m "fixed bug"
git commit -m "WIP"
git commit -m "updates"
```

---

## Quick Reference

### Code Review Checklist

- [ ] Follows naming conventions
- [ ] Functions < 50 lines
- [ ] No unused imports/variables
- [ ] Types defined (no `any`)
- [ ] Error handling present
- [ ] Security patterns followed
- [ ] Tests written
- [ ] Comments explain WHY, not WHAT
- [ ] No hardcoded secrets
- [ ] Consistent code style

---

Created: 2025-10-13
Last Updated: 2025-10-13
Status: Active - Required for all code
