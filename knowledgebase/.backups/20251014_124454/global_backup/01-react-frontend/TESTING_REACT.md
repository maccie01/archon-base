# React Component Testing Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Testing Library docs, Vitest docs, Web Research (Medium, DEV Community, Incubyte)

## Overview

Modern React testing emphasizes testing from the user's perspective using React Testing Library with Vitest. This approach leads to more maintainable tests that provide confidence in application behavior.

## Core Principles

1. **Test Behavior, Not Implementation**: Focus on what users see and do
2. **Query by Accessibility**: Use role-based queries (getByRole)
3. **User-Centric Tests**: Simulate real user interactions
4. **Avoid Implementation Details**: Don't test state or internal methods directly
5. **Test Single Behaviors**: One assertion per test concept

## Testing Setup

### Installation
```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```

### Vitest Configuration (vitest.config.ts)
```typescript
// TODO: Add example code
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    css: true,
  },
})
```

### Setup File (src/test/setup.ts)
```typescript
// TODO: Add example code
import { expect, afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'
import * as matchers from '@testing-library/jest-dom/matchers'

expect.extend(matchers)

afterEach(() => {
  cleanup()
})
```

**References**:
- [Vitest Getting Started](https://vitest.dev/guide/)
- [React Testing Library Setup](https://testing-library.com/docs/react-testing-library/setup)

## Patterns

### Pattern 1: Basic Component Testing

**When to use**: For simple presentational components

**Example skeleton**:
```typescript
// TODO: Add example code
import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import { Button } from './Button'

describe('Button', () => {
  it('renders button with label', () => {
    render(<Button label="Click me" onClick={() => {}} />)

    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument()
  })

  it('calls onClick when clicked', async () => {
    const handleClick = vi.fn()
    const { user } = setup(<Button label="Click" onClick={handleClick} />)

    await user.click(screen.getByRole('button'))

    expect(handleClick).toHaveBeenCalledOnce()
  })

  it('is disabled when disabled prop is true', () => {
    render(<Button label="Click" onClick={() => {}} disabled />)

    expect(screen.getByRole('button')).toBeDisabled()
  })
})
```

### Pattern 2: Testing with User Events

**When to use**: To simulate realistic user interactions

**Example skeleton**:
```typescript
// TODO: Add example code
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect } from 'vitest'

// Setup helper
function setup(jsx: React.ReactElement) {
  return {
    user: userEvent.setup(),
    ...render(jsx),
  }
}

describe('LoginForm', () => {
  it('allows user to login', async () => {
    const handleSubmit = vi.fn()
    const { user } = setup(<LoginForm onSubmit={handleSubmit} />)

    // Type into inputs
    await user.type(screen.getByLabelText(/email/i), 'user@example.com')
    await user.type(screen.getByLabelText(/password/i), 'password123')

    // Submit form
    await user.click(screen.getByRole('button', { name: /log in/i }))

    expect(handleSubmit).toHaveBeenCalledWith({
      email: 'user@example.com',
      password: 'password123',
    })
  })
})
```

**References**:
- [Testing Library - User Event](https://testing-library.com/docs/user-event/intro)

### Pattern 3: Testing Async Components

**When to use**: For components that fetch data or have async operations

**Example skeleton**:
```typescript
// TODO: Add example code
import { render, screen, waitFor } from '@testing-library/react'

describe('UserList', () => {
  it('displays users after loading', async () => {
    // Mock API
    vi.mocked(fetchUsers).mockResolvedValue([
      { id: 1, name: 'John' },
      { id: 2, name: 'Jane' },
    ])

    render(<UserList />)

    // Loading state
    expect(screen.getByText(/loading/i)).toBeInTheDocument()

    // Wait for data to load
    await waitFor(() => {
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument()
    })

    // Check for loaded data
    expect(screen.getByText('John')).toBeInTheDocument()
    expect(screen.getByText('Jane')).toBeInTheDocument()
  })

  it('displays error message on failure', async () => {
    vi.mocked(fetchUsers).mockRejectedValue(new Error('Failed to fetch'))

    render(<UserList />)

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument()
    })
  })
})
```

### Pattern 4: Testing with React Query

**When to use**: For components using TanStack Query

**Example skeleton**:
```typescript
// TODO: Add example code
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen, waitFor } from '@testing-library/react'

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  })

  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}

describe('UserDashboard', () => {
  it('fetches and displays users', async () => {
    const mockUsers = [{ id: 1, name: 'John' }]
    server.use(
      rest.get('/api/users', (req, res, ctx) => {
        return res(ctx.json(mockUsers))
      })
    )

    render(<UserDashboard />, { wrapper: createWrapper() })

    await waitFor(() => {
      expect(screen.getByText('John')).toBeInTheDocument()
    })
  })
})
```

### Pattern 5: Testing Custom Hooks

**When to use**: To test custom hooks in isolation

**Example skeleton**:
```typescript
// TODO: Add example code
import { renderHook, waitFor } from '@testing-library/react'
import { useCounter } from './useCounter'

describe('useCounter', () => {
  it('increments counter', () => {
    const { result } = renderHook(() => useCounter(0))

    expect(result.current.count).toBe(0)

    result.current.increment()

    expect(result.current.count).toBe(1)
  })

  it('decrements counter', () => {
    const { result } = renderHook(() => useCounter(10))

    result.current.decrement()

    expect(result.current.count).toBe(9)
  })
})
```

### Pattern 6: Mocking with MSW (Mock Service Worker)

**When to use**: To mock API calls consistently

**Example skeleton**:
```typescript
// TODO: Add example code
// src/test/mocks/server.ts
import { setupServer } from 'msw/node'
import { rest } from 'msw'

export const handlers = [
  rest.get('/api/users', (req, res, ctx) => {
    return res(
      ctx.json([
        { id: 1, name: 'John' },
        { id: 2, name: 'Jane' },
      ])
    )
  }),

  rest.post('/api/users', async (req, res, ctx) => {
    const user = await req.json()
    return res(ctx.json({ ...user, id: 3 }))
  }),
]

export const server = setupServer(...handlers)

// src/test/setup.ts
import { beforeAll, afterEach, afterAll } from 'vitest'
import { server } from './mocks/server'

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

**References**:
- [MSW Documentation](https://mswjs.io/)

### Pattern 7: Testing Accessibility

**When to use**: Always, to ensure components are accessible

**Example skeleton**:
```typescript
// TODO: Add example code
import { render } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'

expect.extend(toHaveNoViolations)

describe('Button Accessibility', () => {
  it('has no accessibility violations', async () => {
    const { container } = render(<Button label="Click me" onClick={() => {}} />)

    const results = await axe(container)

    expect(results).toHaveNoViolations()
  })
})
```

## Query Priority (Testing Library)

**Use in this order**:

1. **getByRole**: Most accessible queries
   ```typescript
   screen.getByRole('button', { name: /submit/i })
   ```

2. **getByLabelText**: For form fields
   ```typescript
   screen.getByLabelText('Email')
   ```

3. **getByPlaceholderText**: When label isn't available
   ```typescript
   screen.getByPlaceholderText('Enter email')
   ```

4. **getByText**: For non-interactive elements
   ```typescript
   screen.getByText('Welcome')
   ```

5. **getByTestId**: Last resort (use data-testid)
   ```typescript
   screen.getByTestId('user-card')
   ```

**References**:
- [Testing Library Query Priority](https://testing-library.com/docs/queries/about#priority)

## Vitest vs Jest

**Why Vitest?**
- Faster test execution (uses Vite's HMR)
- Native ESM support
- Better TypeScript integration
- Compatible with Jest API
- Smaller bundle size

## Best Practices

1. **Use `screen` over destructuring**: `screen.getByRole()` instead of `const { getByRole } = render()`
2. **Query by role first**: Most accessible and resilient to changes
3. **Wait for async changes**: Use `waitFor`, `findBy*` queries
4. **Test behavior, not implementation**: Don't access state directly
5. **One assertion per test**: Each test should verify a single behavior
6. **Use `user-event` over `fireEvent`**: More realistic user simulation
7. **Mock at the network layer**: Use MSW instead of mocking functions
8. **Test error states**: Don't just test happy paths

## Common Mistakes

1. **Using `getBy*` for async content**: Use `findBy*` or `waitFor`
2. **Testing implementation details**: Accessing state, internal methods
3. **Not cleaning up**: Use `afterEach(() => cleanup())`
4. **Overusing `data-testid`**: Prefer role-based queries
5. **Not using `user-event`**: Using `fireEvent` instead
6. **Synchronous assertions for async operations**: Forgetting `await`
7. **Testing too much in one test**: Keep tests focused

## Testing Coverage

**Run coverage**:
```bash
npm run test:coverage
```

**Coverage targets** (recommended):
- Statements: > 80%
- Branches: > 75%
- Functions: > 80%
- Lines: > 80%

**What to prioritize**:
1. Critical user flows
2. Business logic
3. Error handling
4. Accessibility

## Tools and Libraries

### Testing
- **Vitest**: Modern, fast test runner
- **React Testing Library**: User-centric component testing
- **@testing-library/user-event**: Realistic user interactions
- **@testing-library/jest-dom**: Custom matchers

### Mocking
- **MSW**: Mock Service Worker for API mocking
- **vi.fn()**: Vitest mock functions
- **vi.mock()**: Module mocking

### Accessibility
- **jest-axe**: Automated accessibility testing
- **axe-core**: Accessibility engine

## Additional Resources

- [React Testing Library Documentation](https://testing-library.com/docs/react-testing-library/intro/)
- [Vitest Documentation](https://vitest.dev/)
- [Testing React with Vitest (Medium)](https://vaskort.medium.com/bulletproof-react-testing-with-vitest-rtl-deeaabce9fef)
- [React Testing Best Practices (DEV)](https://dev.to/samuel_kinuthia/testing-react-applications-with-vitest-a-comprehensive-guide-2jm8)
- [Mastering React Testing with Vitest](https://patelvivek.dev/blog/testing-react-vitest)

## Next Steps

- Review [ACCESSIBILITY.md](./ACCESSIBILITY.md) for accessibility testing patterns
- See [HOOKS_PATTERNS.md](./HOOKS_PATTERNS.md) for custom hook testing
- Check [ANTIPATTERNS.md](./ANTIPATTERNS.md) for testing anti-patterns
