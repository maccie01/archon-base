# Testing Patterns - Netzwächter Project Standards

Created: 2025-10-13

This document defines the **REQUIRED testing patterns** for the Netzwächter project.

---

## Testing Strategy

### Test Coverage Goals

| Type | Coverage | Priority |
|------|----------|----------|
| **Unit Tests** | 80%+ for business logic (services, repositories) | P0 |
| **Integration Tests** | All API endpoints | P0 |
| **E2E Tests** | Critical user flows | P1 |
| **Component Tests** | Shared components | P1 |

### Testing Pyramid

```
       ┌────────┐
       │  E2E   │  ← Few, slow, expensive
       │  (10%) │
       ├────────┤
       │ Integr.│  ← Some, medium speed
       │  (30%) │
       ├────────┤
       │  Unit  │  ← Many, fast, cheap
       │  (60%) │
       └────────┘
```

---

## Unit Testing Pattern (Vitest)

### Backend: Service Tests

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
    // Create mock repository with all methods
    mockRepository = {
      findById: vi.fn(),
      findByMandant: vi.fn(),
      findByKey: vi.fn(),
      create: vi.fn(),
      update: vi.fn(),
      delete: vi.fn()
    }

    // Inject mock
    service = new SettingsService()
    service['repository'] = mockRepository
  })

  describe('getAllByMandant', () => {
    it('should return all settings for mandant', async () => {
      const mockSettings = [
        { id: '1', key: 'key1', value: 'value1', mandantId: 'mandant1' },
        { id: '2', key: 'key2', value: 'value2', mandantId: 'mandant1' }
      ]
      mockRepository.findByMandant.mockResolvedValue(mockSettings)

      const result = await service.getAllByMandant('mandant1')

      expect(result).toEqual(mockSettings)
      expect(mockRepository.findByMandant).toHaveBeenCalledWith('mandant1')
      expect(mockRepository.findByMandant).toHaveBeenCalledTimes(1)
    })

    it('should return empty array when no settings', async () => {
      mockRepository.findByMandant.mockResolvedValue([])

      const result = await service.getAllByMandant('mandant1')

      expect(result).toEqual([])
    })
  })

  describe('getById', () => {
    it('should return setting when found and authorized', async () => {
      const mockSetting = {
        id: '1',
        key: 'key1',
        value: 'value1',
        mandantId: 'mandant1'
      }
      mockRepository.findById.mockResolvedValue(mockSetting)

      const result = await service.getById('1', 'mandant1')

      expect(result).toEqual(mockSetting)
    })

    it('should return null when setting not found', async () => {
      mockRepository.findById.mockResolvedValue(null)

      const result = await service.getById('nonexistent', 'mandant1')

      expect(result).toBeNull()
    })

    it('should throw 403 when accessing other mandant setting', async () => {
      const mockSetting = {
        id: '1',
        mandantId: 'mandant2' // Different mandant
      }
      mockRepository.findById.mockResolvedValue(mockSetting)

      await expect(
        service.getById('1', 'mandant1')
      ).rejects.toThrow(AppError)

      await expect(
        service.getById('1', 'mandant1')
      ).rejects.toThrow('Access denied')
    })
  })

  describe('create', () => {
    it('should create setting with valid data', async () => {
      const createData = {
        key: 'new_key',
        value: 'new_value',
        mandantId: 'mandant1'
      }
      const mockCreated = { id: '1', ...createData }

      mockRepository.findByKey.mockResolvedValue(null) // No duplicate
      mockRepository.create.mockResolvedValue(mockCreated)

      const result = await service.create(createData)

      expect(result).toEqual(mockCreated)
      expect(mockRepository.findByKey).toHaveBeenCalledWith('new_key', 'mandant1')
      expect(mockRepository.create).toHaveBeenCalledWith(createData)
    })

    it('should throw 409 when duplicate key exists', async () => {
      const createData = {
        key: 'existing_key',
        value: 'value',
        mandantId: 'mandant1'
      }

      mockRepository.findByKey.mockResolvedValue({ id: '1', key: 'existing_key' })

      await expect(
        service.create(createData)
      ).rejects.toThrow(AppError)

      await expect(
        service.create(createData)
      ).rejects.toThrow('already exists')

      // Should not attempt to create
      expect(mockRepository.create).not.toHaveBeenCalled()
    })
  })
})
```

### Backend: Repository Tests

```typescript
// apps/backend-api/modules/settings/__tests__/settings.repository.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { SettingsRepository } from '../settings.repository'
import { db } from '@/db'
import { settings } from '@/db/schema'
import { eq } from 'drizzle-orm'

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
    // Cleanup - ALWAYS clean up test data
    await db.delete(settings).where(eq(settings.id, testSettingId))
  })

  it('should find setting by ID', async () => {
    const result = await repository.findById(testSettingId)

    expect(result).toBeDefined()
    expect(result?.id).toBe(testSettingId)
    expect(result?.key).toBe('test_key')
    expect(result?.value).toBe('test_value')
  })

  it('should return undefined for non-existent ID', async () => {
    const result = await repository.findById('non-existent')

    expect(result).toBeUndefined()
  })

  it('should find settings by mandant', async () => {
    const results = await repository.findByMandant('test_mandant')

    expect(results.length).toBeGreaterThan(0)
    expect(results.some(s => s.id === testSettingId)).toBe(true)
  })

  it('should create setting', async () => {
    const newSetting = await repository.create({
      key: 'new_key',
      value: 'new_value',
      mandantId: 'test_mandant'
    })

    expect(newSetting).toBeDefined()
    expect(newSetting.key).toBe('new_key')

    // Cleanup
    await db.delete(settings).where(eq(settings.id, newSetting.id))
  })

  it('should update setting', async () => {
    const updated = await repository.update(testSettingId, {
      value: 'updated_value'
    })

    expect(updated).toBeDefined()
    expect(updated?.value).toBe('updated_value')
  })

  it('should delete setting', async () => {
    await repository.delete(testSettingId)

    const result = await repository.findById(testSettingId)
    expect(result).toBeUndefined()
  })
})
```

### Frontend: Hook Tests

```typescript
// apps/frontend-web/src/features/settings/hooks/__tests__/useSettingForm.test.ts
import { describe, it, expect, vi } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { useSettingForm } from '../useSettingForm'
import { useUpdateSetting } from '@/features/shared/hooks/api/useSettings'

// Mock API hook
vi.mock('@/features/shared/hooks/api/useSettings')

describe('useSettingForm', () => {
  const mockSetting = {
    id: '1',
    key: 'test_key',
    value: 'test_value',
    description: 'test description'
  }

  beforeEach(() => {
    vi.mocked(useUpdateSetting).mockReturnValue({
      mutate: vi.fn(),
      isPending: false
    } as any)
  })

  it('should initialize with setting values', () => {
    const { result } = renderHook(() => useSettingForm(mockSetting))

    expect(result.current.form.getValues()).toEqual({
      key: 'test_key',
      value: 'test_value',
      description: 'test description'
    })
  })

  it('should call mutation on submit', async () => {
    const mutateMock = vi.fn()
    vi.mocked(useUpdateSetting).mockReturnValue({
      mutate: mutateMock,
      isPending: false
    } as any)

    const { result } = renderHook(() => useSettingForm(mockSetting))

    result.current.form.setValue('value', 'new_value')
    result.current.onSubmit()

    await waitFor(() => {
      expect(mutateMock).toHaveBeenCalledWith(
        expect.objectContaining({
          id: '1',
          value: 'new_value'
        }),
        expect.any(Object)
      )
    })
  })
})
```

---

## Integration Testing Pattern

### Backend: API Endpoint Tests

```typescript
// apps/backend-api/modules/settings/__tests__/settings.api.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import request from 'supertest'
import { app } from '@/index'
import { db } from '@/db'
import { settings, users } from '@/db/schema'
import { eq } from 'drizzle-orm'

describe('Settings API', () => {
  let authCookie: string
  let testUserId: string
  let testMandantId: string
  let testSettingId: string

  beforeEach(async () => {
    // Setup: Create test user
    const [user] = await db.insert(users).values({
      username: 'testuser',
      email: 'test@example.com',
      password: 'hashed_password',
      mandantId: 'test_mandant',
      role: 'admin'
    }).returning()

    testUserId = user.id
    testMandantId = user.mandantId

    // Login to get auth cookie
    const loginResponse = await request(app)
      .post('/api/auth/login')
      .send({ username: 'testuser', password: 'password' })

    authCookie = loginResponse.headers['set-cookie']

    // Create test setting
    const [setting] = await db.insert(settings).values({
      key: 'test_key',
      value: 'test_value',
      mandantId: testMandantId
    }).returning()

    testSettingId = setting.id
  })

  afterEach(async () => {
    // Cleanup
    await db.delete(settings).where(eq(settings.id, testSettingId))
    await db.delete(users).where(eq(users.id, testUserId))
  })

  describe('GET /api/settings', () => {
    it('should return all settings for authenticated user', async () => {
      const response = await request(app)
        .get('/api/settings')
        .set('Cookie', authCookie)

      expect(response.status).toBe(200)
      expect(Array.isArray(response.body)).toBe(true)
      expect(response.body.some((s: any) => s.id === testSettingId)).toBe(true)
    })

    it('should return 401 without authentication', async () => {
      const response = await request(app)
        .get('/api/settings')

      expect(response.status).toBe(401)
      expect(response.body.error).toBe('Authentication required')
    })
  })

  describe('GET /api/settings/:id', () => {
    it('should return setting by ID', async () => {
      const response = await request(app)
        .get(`/api/settings/${testSettingId}`)
        .set('Cookie', authCookie)

      expect(response.status).toBe(200)
      expect(response.body.id).toBe(testSettingId)
      expect(response.body.key).toBe('test_key')
    })

    it('should return 404 for non-existent setting', async () => {
      const response = await request(app)
        .get('/api/settings/non-existent')
        .set('Cookie', authCookie)

      expect(response.status).toBe(404)
    })
  })

  describe('POST /api/settings', () => {
    it('should create setting with valid data', async () => {
      const response = await request(app)
        .post('/api/settings')
        .set('Cookie', authCookie)
        .send({
          key: 'new_key',
          value: 'new_value'
        })

      expect(response.status).toBe(201)
      expect(response.body.key).toBe('new_key')

      // Cleanup
      await db.delete(settings).where(eq(settings.id, response.body.id))
    })

    it('should return 400 with invalid data', async () => {
      const response = await request(app)
        .post('/api/settings')
        .set('Cookie', authCookie)
        .send({
          // Missing required fields
        })

      expect(response.status).toBe(400)
    })

    it('should return 403 without admin role', async () => {
      // Create user without admin role
      const [regularUser] = await db.insert(users).values({
        username: 'regularuser',
        email: 'regular@example.com',
        password: 'hashed_password',
        mandantId: testMandantId,
        role: 'user' // Not admin
      }).returning()

      // Login as regular user
      const loginResponse = await request(app)
        .post('/api/auth/login')
        .send({ username: 'regularuser', password: 'password' })

      const regularUserCookie = loginResponse.headers['set-cookie']

      const response = await request(app)
        .post('/api/settings')
        .set('Cookie', regularUserCookie)
        .send({
          key: 'new_key',
          value: 'new_value'
        })

      expect(response.status).toBe(403)

      // Cleanup
      await db.delete(users).where(eq(users.id, regularUser.id))
    })
  })

  describe('PUT /api/settings/:id', () => {
    it('should update setting', async () => {
      const response = await request(app)
        .put(`/api/settings/${testSettingId}`)
        .set('Cookie', authCookie)
        .send({
          value: 'updated_value'
        })

      expect(response.status).toBe(200)
      expect(response.body.value).toBe('updated_value')
    })
  })

  describe('DELETE /api/settings/:id', () => {
    it('should delete setting', async () => {
      const response = await request(app)
        .delete(`/api/settings/${testSettingId}`)
        .set('Cookie', authCookie)

      expect(response.status).toBe(204)

      // Verify deletion
      const getResponse = await request(app)
        .get(`/api/settings/${testSettingId}`)
        .set('Cookie', authCookie)

      expect(getResponse.status).toBe(404)
    })
  })
})
```

---

## E2E Testing Pattern (Playwright)

```typescript
// testing/e2e/settings.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Settings Management', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login')
    await page.fill('[name="username"]', 'admin')
    await page.fill('[name="password"]', 'admin123')
    await page.click('button[type="submit"]')
    await expect(page).toHaveURL('/dashboard')
  })

  test('should display settings page', async ({ page }) => {
    await page.goto('/settings')

    // Check page loaded
    await expect(page.locator('h1')).toContainText('Settings')

    // Check settings list visible
    await expect(page.locator('[data-testid="settings-list"]')).toBeVisible()
  })

  test('should create new setting', async ({ page }) => {
    await page.goto('/settings')

    // Click create button
    await page.click('[data-testid="create-setting-button"]')

    // Fill form
    await page.fill('[name="key"]', 'test_key')
    await page.fill('[name="value"]', 'test_value')
    await page.fill('[name="description"]', 'test description')

    // Submit
    await page.click('button[type="submit"]')

    // Verify success
    await expect(page.locator('.toast-success')).toContainText('Setting created')

    // Verify in list
    await expect(page.locator('[data-testid="setting-key"]')).toContainText('test_key')
  })

  test('should edit setting', async ({ page }) => {
    await page.goto('/settings')

    // Click first setting edit button
    await page.click('[data-testid="edit-setting"]:first-of-type')

    // Update value
    await page.fill('[name="value"]', 'updated_value')

    // Submit
    await page.click('button[type="submit"]')

    // Verify success
    await expect(page.locator('.toast-success')).toContainText('Setting updated')
  })

  test('should delete setting', async ({ page }) => {
    await page.goto('/settings')

    // Get initial count
    const initialCount = await page.locator('[data-testid="setting-card"]').count()

    // Click first setting delete button
    await page.click('[data-testid="delete-setting"]:first-of-type')

    // Confirm deletion
    await page.click('[data-testid="confirm-delete"]')

    // Verify success
    await expect(page.locator('.toast-success')).toContainText('Setting deleted')

    // Verify count decreased
    const newCount = await page.locator('[data-testid="setting-card"]').count()
    expect(newCount).toBe(initialCount - 1)
  })

  test('should validate required fields', async ({ page }) => {
    await page.goto('/settings')

    // Click create button
    await page.click('[data-testid="create-setting-button"]')

    // Submit without filling fields
    await page.click('button[type="submit"]')

    // Verify validation errors
    await expect(page.locator('.error-message')).toContainText('Key is required')
    await expect(page.locator('.error-message')).toContainText('Value is required')
  })
})
```

---

## Component Testing Pattern (React Testing Library)

```typescript
// apps/frontend-web/src/features/settings/components/__tests__/SettingCard.test.tsx
import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { SettingCard } from '../SettingCard'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const mockSetting = {
  id: '1',
  key: 'test_key',
  value: 'test_value',
  description: 'test description'
}

function renderWithQuery(ui: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false }
    }
  })

  return render(
    <QueryClientProvider client={queryClient}>
      {ui}
    </QueryClientProvider>
  )
}

describe('SettingCard', () => {
  it('should render setting details', () => {
    renderWithQuery(<SettingCard setting={mockSetting} />)

    expect(screen.getByText('test_key')).toBeInTheDocument()
    expect(screen.getByText('test_value')).toBeInTheDocument()
    expect(screen.getByText('test description')).toBeInTheDocument()
  })

  it('should toggle edit mode', () => {
    renderWithQuery(<SettingCard setting={mockSetting} />)

    // Initially in view mode
    expect(screen.getByText('test_value')).toBeInTheDocument()

    // Click edit button
    fireEvent.click(screen.getByRole('button', { name: /edit/i }))

    // Should show edit form
    expect(screen.getByRole('textbox', { name: /value/i })).toBeInTheDocument()
  })

  it('should handle delete', async () => {
    const onDelete = vi.fn()
    renderWithQuery(<SettingCard setting={mockSetting} onDelete={onDelete} />)

    // Click delete button
    fireEvent.click(screen.getByRole('button', { name: /delete/i }))

    // Confirm deletion
    fireEvent.click(screen.getByRole('button', { name: /confirm/i }))

    expect(onDelete).toHaveBeenCalledWith('1')
  })

  it('should handle keyboard navigation', () => {
    renderWithQuery(<SettingCard setting={mockSetting} />)

    const editButton = screen.getByRole('button', { name: /edit/i })

    // Focus with Tab
    editButton.focus()
    expect(editButton).toHaveFocus()

    // Activate with Enter
    fireEvent.keyDown(editButton, { key: 'Enter', code: 'Enter' })

    // Should open edit form
    expect(screen.getByRole('textbox', { name: /value/i })).toBeInTheDocument()
  })
})
```

---

## Test Best Practices

### 1. Always Clean Up

```typescript
afterEach(async () => {
  // Clean up database
  await db.delete(testTable).where(eq(testTable.id, testId))

  // Clear mocks
  vi.clearAllMocks()

  // Reset query client
  queryClient.clear()
})
```

### 2. Use Test Data Builders

```typescript
// testing/builders/settingBuilder.ts
export function buildSetting(overrides = {}) {
  return {
    id: '1',
    key: 'test_key',
    value: 'test_value',
    mandantId: 'test_mandant',
    isSecret: false,
    description: 'test',
    createdAt: new Date(),
    updatedAt: new Date(),
    ...overrides
  }
}

// Usage in tests:
const setting = buildSetting({ key: 'custom_key' })
```

### 3. Test Error Cases

```typescript
it('should handle API errors', async () => {
  mockRepository.findById.mockRejectedValue(new Error('Database error'))

  await expect(
    service.getById('1', 'mandant1')
  ).rejects.toThrow('Database error')
})
```

### 4. Test Edge Cases

```typescript
describe('edge cases', () => {
  it('should handle empty string', async () => {
    const result = await service.create({ key: '', value: '' })
    expect(result).toThrow('Key is required')
  })

  it('should handle very long strings', async () => {
    const longString = 'a'.repeat(10000)
    const result = await service.create({ key: 'key', value: longString })
    expect(result.value).toHaveLength(10000)
  })

  it('should handle special characters', async () => {
    const result = await service.create({ key: 'key', value: '<script>alert("xss")</script>' })
    // Verify sanitization
  })
})
```

---

## Quick Reference

### When to Write Which Test

| Scenario | Test Type | Tool |
|----------|-----------|------|
| Business logic in service | Unit test | Vitest + mocks |
| Database queries | Integration test | Vitest + real DB |
| API endpoints | Integration test | Supertest |
| Component rendering | Component test | React Testing Library |
| User flow (login → create → delete) | E2E test | Playwright |

### Test File Naming

- Unit/Integration: `[name].test.ts`
- E2E: `[feature].spec.ts`
- Component: `[Component].test.tsx`

### Coverage Commands

```bash
# Backend tests with coverage
npm run test:coverage

# Frontend tests with coverage
npm run test:frontend:coverage

# E2E tests
npm run test:e2e

# Watch mode (development)
npm run test:watch
```

---

Created: 2025-10-13
Status: Active - Required for all new code
