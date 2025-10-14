# Mocking Patterns and Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Testing best practices, test doubles patterns, mocking strategies

## Overview

Mocking is essential for isolating code under test from external dependencies. This guide covers different types of test doubles and when to use each.

## Core Principles

1. **Mock External Boundaries** - Not internal modules
2. **Verify Behavior** - Not implementation
3. **Keep Mocks Simple** - Easy to understand
4. **Mock What You Don't Own** - External APIs, databases
5. **Don't Mock What You Own** - Test real implementations

## Types of Test Doubles

### 1. Dummy
Objects passed but never used. Used to fill parameter lists.

```typescript
// TODO: Add dummy example
```

### 2. Stub
Provides predefined responses to calls.

```typescript
// TODO: Add stub example
```

### 3. Spy
Records information about calls (arguments, call count).

```typescript
// TODO: Add spy example
```

### 4. Mock
Programmed with expectations and verifies calls.

```typescript
// TODO: Add mock example
```

### 5. Fake
Working implementation, usually simplified.

```typescript
// TODO: Add fake example (in-memory database)
```

## Vitest Mocking

### Mock Functions
```typescript
import { vi } from 'vitest'

// Create mock function
const mockFn = vi.fn()

// Mock with return value
mockFn.mockReturnValue('result')

// Mock with implementation
mockFn.mockImplementation((x) => x * 2)

// Mock resolved promise
mockFn.mockResolvedValue('async result')

// Mock rejected promise
mockFn.mockRejectedValue(new Error('failed'))

// TODO: Add complete examples
```

### Module Mocking
```typescript
// Auto-mock entire module
vi.mock('./api')

// Mock with factory
vi.mock('./api', () => ({
  fetchData: vi.fn(),
  postData: vi.fn(),
}))

// Partial mock
vi.mock('./api', async () => {
  const actual = await vi.importActual('./api')
  return {
    ...actual,
    fetchData: vi.fn(), // Mock only this
  }
})

// TODO: Add complete examples
```

### Clearing and Resetting Mocks
```typescript
beforeEach(() => {
  vi.clearAllMocks()    // Clears call history
  vi.resetAllMocks()    // Clears + resets implementation
  vi.restoreAllMocks()  // Restores original implementation
})
```

## API Mocking with MSW

### Setup
```typescript
// TODO: Add MSW setup
// Server setup, handlers, integration
```

### REST API Mocking
```typescript
// TODO: Add REST API handlers
// GET, POST, PUT, DELETE examples
```

### GraphQL Mocking
```typescript
// TODO: Add GraphQL mocking
```

### Error Simulation
```typescript
// TODO: Add error response mocking
```

## Database Mocking

### In-Memory Database
```typescript
// TODO: Add in-memory DB pattern
// SQLite, MongoDB Memory Server
```

### Repository Mocking
```typescript
// TODO: Add repository mock
// Mock data layer
```

### Transaction Mocking
```typescript
// TODO: Add transaction mock
```

## Third-Party Service Mocking

### Payment Gateway
```typescript
// TODO: Add Stripe/payment mock
```

### Email Service
```typescript
// TODO: Add email service mock
```

### Cloud Storage
```typescript
// TODO: Add S3/storage mock
```

## Time and Date Mocking

### Mocking Dates
```typescript
import { vi } from 'vitest'

// Set system time
vi.setSystemTime(new Date('2024-01-01'))

// Advance time
vi.advanceTimersByTime(1000)

// TODO: Add complete time mocking examples
```

### Mocking Timers
```typescript
vi.useFakeTimers()

setTimeout(() => callback(), 1000)

vi.advanceTimersByTime(1000)

vi.useRealTimers()

// TODO: Add timer mocking patterns
```

## Mocking Strategies

### Strategy 1: Mock at Boundaries
```typescript
// Good - mock external API
vi.mock('./api/client')

// Bad - mock internal business logic
vi.mock('./utils/calculate')

// TODO: Add boundary mocking examples
```

### Strategy 2: Dependency Injection
```typescript
// TODO: Add DI pattern for testability
// Constructor injection, function parameters
```

### Strategy 3: Factory Functions
```typescript
// TODO: Add factory pattern for dependencies
```

## Assertion on Mocks

### Verify Calls
```typescript
expect(mockFn).toHaveBeenCalled()
expect(mockFn).toHaveBeenCalledTimes(2)
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2')
expect(mockFn).toHaveBeenLastCalledWith('last arg')
expect(mockFn).toHaveBeenNthCalledWith(1, 'first call')
```

### Call Order
```typescript
// TODO: Add call order verification
```

### Mock Return Values Verification
```typescript
// TODO: Add return value assertions
```

## Advanced Mocking

### Conditional Mocking
```typescript
// TODO: Add conditional mock responses
// Based on input arguments
```

### Sequential Mocking
```typescript
mockFn
  .mockReturnValueOnce('first')
  .mockReturnValueOnce('second')
  .mockReturnValue('default')

// TODO: Add sequential mock examples
```

### Async Mocking
```typescript
// TODO: Add async mock patterns
// Promises, delays, cancellation
```

## React-Specific Mocking

### Mocking React Components
```typescript
// TODO: Add component mocking
// Child components, HOCs
```

### Mocking Hooks
```typescript
// TODO: Add React hooks mocking
// useState, useEffect, custom hooks
```

### Mocking Context
```typescript
// TODO: Add context mocking
```

## Node.js Mocking

### File System Mocking
```typescript
// TODO: Add fs mocking
```

### Environment Variables
```typescript
// TODO: Add process.env mocking
```

### Node Modules
```typescript
// TODO: Add Node module mocking
// path, os, crypto, etc.
```

## When NOT to Mock

### 1. Your Own Code
Test real implementations of your business logic.

### 2. Simple Functions
Pure, simple functions don't need mocking.

### 3. Data Structures
Arrays, objects, primitives - use real instances.

### 4. Framework Code
Trust that React, Express, etc. work correctly.

## Common Mocking Mistakes

### 1. Over-Mocking
```typescript
// Bad - mocking everything
vi.mock('./service1')
vi.mock('./service2')
vi.mock('./service3')

// Good - only mock external boundaries
vi.mock('./api-client')
```

### 2. Testing Mock Implementations
```typescript
// Bad - verifying mock behavior
const mock = vi.fn().mockReturnValue('value')
expect(mock()).toBe('value') // Useless test

// Good - verify real code behavior
expect(realFunction()).toBe('expected')
```

### 3. Not Resetting Mocks
```typescript
// Bad - mocks leak between tests
// Good - reset in beforeEach
beforeEach(() => {
  vi.clearAllMocks()
})
```

## Mocking Frameworks Comparison

### Vitest Built-in
- Fast
- Simple API
- ESM support

### Jest
- Mature
- Widely used
- Large ecosystem

### Sinon
- Standalone
- Framework agnostic
- Feature-rich

## Testing with Mocks Best Practices

1. **Mock at System Boundaries** - External services, APIs
2. **Use Real Implementations** - For internal code
3. **Reset Mocks Between Tests** - Clean state
4. **Verify Interactions** - Not just return values
5. **Keep Mocks Simple** - Easy to understand
6. **Don't Test Mocks** - Test real behavior
7. **Use MSW for APIs** - More realistic
8. **Inject Dependencies** - Makes testing easier
9. **Mock Time Carefully** - Restore real timers
10. **Document Complex Mocks** - Explain why needed

## Tools and Libraries

### Mocking
- Vitest/Jest mocks
- Sinon
- testdouble.js

### API Mocking
- MSW (Mock Service Worker)
- nock
- miragejs

### Database
- mongodb-memory-server
- @databases/pg-test
- ioredis-mock

## Additional Resources

- [TESTING_STRATEGY.md](./TESTING_STRATEGY.md) - Overall approach
- [UNIT_TESTING.md](./UNIT_TESTING.md) - Unit test patterns
- [INTEGRATION_TESTING.md](./INTEGRATION_TESTING.md) - Integration tests
- [VITEST_PATTERNS.md](./VITEST_PATTERNS.md) - Vitest specifics
