# Vitest Patterns and Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Vitest documentation, Vite ecosystem best practices

## Overview

Vitest is a blazing-fast unit testing framework powered by Vite. It provides Jest-compatible APIs with modern features and significantly faster execution.

## Core Principles

1. **Fast by Default** - Uses Vite's transformation pipeline
2. **ESM First** - Native ES modules support
3. **TypeScript Native** - First-class TypeScript support
4. **Watch Mode** - Intelligent test re-running
5. **Jest Compatible** - Easy migration from Jest

## Configuration

### Basic Configuration
```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'node', // or 'jsdom' for browser-like
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      provider: 'v8', // or 'istanbul'
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.test.ts',
        '**/*.d.ts',
      ],
    },
  },
})
```

### Frontend Configuration (React)
```typescript
// TODO: Add complete React/Vitest config
// Include jsdom, React plugin, test utils setup
```

### Backend Configuration (Node.js)
```typescript
// TODO: Add complete Node.js/Vitest config
// Include node environment, database setup
```

### Monorepo Configuration
```typescript
// TODO: Add monorepo workspace config
// Shared config, path aliases, coverage aggregation
```

## Test Structure

### Basic Test Syntax
```typescript
import { describe, it, expect, beforeEach, afterEach } from 'vitest'

describe('Feature Name', () => {
  beforeEach(() => {
    // Setup before each test
  })

  it('should do something', () => {
    expect(true).toBe(true)
  })

  it.skip('should skip this test', () => {
    // Temporarily skip
  })

  it.only('should run only this test', () => {
    // Run in isolation
  })

  it.todo('should implement this later')
})
```

### Lifecycle Hooks
```typescript
// TODO: Add complete lifecycle hooks example
// beforeAll, afterAll, beforeEach, afterEach
```

## Mocking Patterns

### Mock Functions
```typescript
import { vi } from 'vitest'

// Create mock function
const mockFn = vi.fn()

// Mock with return value
mockFn.mockReturnValue('value')

// Mock with implementation
mockFn.mockImplementation((x) => x * 2)

// Mock once
mockFn.mockReturnValueOnce('first')
      .mockReturnValueOnce('second')

// TODO: Add more mock function examples
```

### Module Mocking
```typescript
// Auto-mock entire module
vi.mock('./module')

// Mock with factory
vi.mock('./module', () => ({
  fetchData: vi.fn(),
  processData: vi.fn(),
}))

// Partial mock
vi.mock('./module', async () => {
  const actual = await vi.importActual('./module')
  return {
    ...actual,
    fetchData: vi.fn(), // Override one function
  }
})

// TODO: Add complete module mocking examples
```

### Mocking Timers
```typescript
import { vi, it, expect } from 'vitest'

it('should work with fake timers', () => {
  vi.useFakeTimers()

  const callback = vi.fn()
  setTimeout(callback, 1000)

  vi.advanceTimersByTime(1000)
  expect(callback).toHaveBeenCalled()

  vi.useRealTimers()
})

// TODO: Add more timer mocking patterns
```

### Mocking Dates
```typescript
import { vi } from 'vitest'

// Mock Date.now()
vi.setSystemTime(new Date('2024-01-01'))

// Restore real time
vi.useRealTimers()

// TODO: Add date mocking examples
```

## Async Testing

### Async/Await
```typescript
it('should handle async operations', async () => {
  const result = await asyncFunction()
  expect(result).toBe('value')
})
```

### Promises
```typescript
it('should resolve promise', () => {
  return expect(promise).resolves.toBe('value')
})

it('should reject promise', () => {
  return expect(promise).rejects.toThrow('error')
})
```

### Testing Callbacks
```typescript
// TODO: Add callback testing examples
```

## Snapshot Testing

### Basic Snapshots
```typescript
it('should match snapshot', () => {
  const data = generateData()
  expect(data).toMatchSnapshot()
})
```

### Inline Snapshots
```typescript
it('should match inline snapshot', () => {
  expect(data).toMatchInlineSnapshot(`
    {
      "key": "value"
    }
  `)
})
```

### When to Use Snapshots
- Complex object structures
- Generated output (HTML, configs)
- Regression prevention

### When NOT to Use Snapshots
- Simple values (use explicit assertions)
- Frequently changing data
- Non-deterministic output

## Coverage Configuration

### V8 Coverage (Recommended)
```typescript
// TODO: Add V8 coverage config
// Fast, accurate, native Node.js
```

### Istanbul Coverage
```typescript
// TODO: Add Istanbul coverage config
// More mature, broader support
```

### Coverage Thresholds
```typescript
coverage: {
  thresholds: {
    lines: 75,
    functions: 75,
    branches: 75,
    statements: 75,
  },
}
```

### Excluding Files from Coverage
```typescript
// TODO: Add exclusion patterns
// Test files, config, types, generated code
```

## Watch Mode

### Running Watch Mode
```bash
vitest --watch
# or
vitest watch
```

### Watch Mode Features
- Rerun failed tests first
- Rerun tests for changed files
- Filter by file name or pattern
- Run all tests or specific suites

### Watch Mode Shortcuts
```
h - Show help
a - Rerun all tests
f - Rerun only failed tests
p - Filter by filename
t - Filter by test name pattern
q - Quit
```

## UI Mode

### Running UI Mode
```bash
vitest --ui
```

### UI Features
- Visual test runner
- Test tree visualization
- Coverage visualization
- Console output
- Test execution graph

## TypeScript Integration

### Type-Safe Tests
```typescript
import { expect, it } from 'vitest'
import type { User } from './types'

it('should type check', () => {
  const user: User = {
    id: '1',
    name: 'Test',
  }

  expect(user).toMatchObject({ id: '1' })
})
```

### Custom Matchers with Types
```typescript
// TODO: Add custom matcher type definitions
```

## Test Utilities

### Setup Files
```typescript
// src/test/setup.ts
import { expect, afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'

// Cleanup after each test
afterEach(() => {
  cleanup()
})

// Custom matchers
expect.extend({
  // TODO: Add custom matchers
})
```

### Test Helpers
```typescript
// TODO: Add common test helper patterns
// Factory functions, render helpers, assertion helpers
```

## Performance Optimization

### Parallel Execution
```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    pool: 'threads', // or 'forks'
    poolOptions: {
      threads: {
        singleThread: false,
      },
    },
  },
})
```

### Isolate Tests
```typescript
export default defineConfig({
  test: {
    isolate: true, // Each test file in own context
  },
})
```

### Sharding for CI
```bash
vitest run --shard=1/3
vitest run --shard=2/3
vitest run --shard=3/3
```

## Debugging

### VS Code Debugging
```json
// TODO: Add VS Code launch config for Vitest
```

### Chrome DevTools
```bash
vitest --inspect-brk
```

### Debug Specific Test
```typescript
it.only('should debug this', () => {
  debugger
  // Your test
})
```

## Benchmarking

### Basic Benchmark
```typescript
import { bench, describe } from 'vitest'

describe('Performance', () => {
  bench('method 1', () => {
    // Code to benchmark
  })

  bench('method 2', () => {
    // Alternative implementation
  })
})
```

## Common Patterns

### Pattern 1: Testing API Endpoints
```typescript
// TODO: Add supertest + Vitest example
```

### Pattern 2: Testing React Components
```typescript
// TODO: Add React Testing Library + Vitest
```

### Pattern 3: Testing Database Operations
```typescript
// TODO: Add database testing pattern
```

### Pattern 4: Testing with Environment Variables
```typescript
// TODO: Add env var testing pattern
```

## Migration from Jest

### Key Differences
- Globals enabled via config
- ESM by default
- Different coverage providers
- Faster execution

### Migration Checklist
- [ ] Install Vitest
- [ ] Update config (jest.config -> vitest.config)
- [ ] Update package.json scripts
- [ ] Enable globals if using global test functions
- [ ] Update coverage config
- [ ] Update CI pipeline
- [ ] Test in watch mode
- [ ] Run full test suite

## Best Practices

1. Use `globals: true` for cleaner test files
2. Prefer V8 coverage for speed
3. Use watch mode during development
4. Enable UI mode for debugging
5. Mock at module boundaries
6. Keep tests fast and isolated
7. Use TypeScript for type safety
8. Leverage Vite's fast HMR
9. Use test.each for parameterized tests
10. Profile slow tests

## Common Mistakes

### 1. Not Clearing Mocks
```typescript
// Bad
vi.mock('./api')
// Mocks persist across tests

// Good
beforeEach(() => {
  vi.clearAllMocks()
})
```

### 2. Async Test Without Await
```typescript
// Bad
it('test', () => {
  asyncFunction() // Not awaited!
})

// Good
it('test', async () => {
  await asyncFunction()
})
```

### 3. Using Real Timers in Async Tests
```typescript
// TODO: Add timer/async interaction example
```

## Tools and Plugins

### Recommended Plugins
- @vitest/ui - Visual test runner
- @vitest/coverage-v8 - Fast coverage
- unplugin-auto-import - Auto-import test functions

### VS Code Extensions
- Vitest extension
- Error Lens
- Jest Runner (works with Vitest)

## Additional Resources

- [TESTING_STRATEGY.md](./TESTING_STRATEGY.md) - Overall testing approach
- [UNIT_TESTING.md](./UNIT_TESTING.md) - Unit testing patterns
- [MOCKING_PATTERNS.md](./MOCKING_PATTERNS.md) - Mocking strategies
- [Vitest Documentation](https://vitest.dev/)
- [Vite Documentation](https://vitejs.dev/)
