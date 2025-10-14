# Unit Testing Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Industry standards, FIRST principles, testing best practices

## Overview

Unit tests verify individual functions, methods, or components in isolation. They should be fast, focused, and independent.

## Core Principles

1. **Fast** - Execute in milliseconds
2. **Isolated** - No dependencies on external systems
3. **Repeatable** - Same input always produces same output
4. **Self-validating** - Pass or fail, no manual inspection
5. **Thorough** - Test edge cases and error conditions

## What to Unit Test

### Pure Functions (High Priority)
```typescript
// TODO: Add example - pure utility function test
```

### Business Logic
```typescript
// TODO: Add example - business logic validation
```

### Calculations and Algorithms
```typescript
// TODO: Add example - complex calculation test
```

### Error Handling
```typescript
// TODO: Add example - error handling test
```

## Test Structure

### Basic Template
```typescript
import { describe, it, expect } from 'vitest'

describe('FunctionName', () => {
  it('should handle normal case', () => {
    // Arrange
    const input = createInput()

    // Act
    const result = functionUnderTest(input)

    // Assert
    expect(result).toBe(expectedValue)
  })

  it('should handle edge case', () => {
    // Test edge cases
  })

  it('should throw error for invalid input', () => {
    expect(() => functionUnderTest(invalidInput))
      .toThrow('Expected error message')
  })
})
```

## Testing Patterns

### Pattern 1: Testing Pure Functions

**When to use**: Functions with no side effects

**Example**:
```typescript
// TODO: Add complete example
// Function: formatCurrency(amount: number, locale: string): string
// Tests: various amounts, locales, edge cases (0, negative, very large)
```

### Pattern 2: Testing with Dependencies

**When to use**: Functions that depend on other modules

**Example**:
```typescript
// TODO: Add dependency injection example
// Show how to inject mocks for dependencies
```

### Pattern 3: Testing Async Functions

**When to use**: Promises, async/await

**Example**:
```typescript
// TODO: Add async testing examples
// Show async/await and promise testing patterns
```

### Pattern 4: Testing Error Conditions

**When to use**: Validating error handling

**Example**:
```typescript
// TODO: Add error testing patterns
// Show toThrow, try-catch, error messages
```

## Isolation Techniques

### Mocking Dependencies
```typescript
import { vi } from 'vitest'

// Mock module
vi.mock('./dependency', () => ({
  fetchData: vi.fn().mockResolvedValue({ data: 'mock' })
}))

// TODO: Add complete example
```

### Stubbing Functions
```typescript
// TODO: Add stub example
// Show difference between mocks and stubs
```

### Test Doubles
```typescript
// TODO: Add test doubles example
// Fakes, stubs, spies, mocks
```

## Testing Different Constructs

### Testing Classes
```typescript
// TODO: Add class testing example
// Constructor, methods, private methods (indirectly)
```

### Testing Closures
```typescript
// TODO: Add closure testing example
```

### Testing Higher-Order Functions
```typescript
// TODO: Add HOF testing example
```

## Assertion Patterns

### Equality Assertions
```typescript
expect(value).toBe(expected)           // Strict equality (===)
expect(object).toEqual(expected)       // Deep equality
expect(array).toStrictEqual(expected)  // Strict deep equality
```

### Truthiness
```typescript
expect(value).toBeTruthy()
expect(value).toBeFalsy()
expect(value).toBeNull()
expect(value).toBeUndefined()
expect(value).toBeDefined()
```

### Numbers
```typescript
expect(value).toBeGreaterThan(5)
expect(value).toBeLessThanOrEqual(10)
expect(value).toBeCloseTo(0.3, 5) // Floating point
```

### Strings
```typescript
expect(string).toMatch(/pattern/)
expect(string).toContain('substring')
```

### Arrays and Iterables
```typescript
expect(array).toContain(item)
expect(array).toHaveLength(3)
expect(array).toContainEqual({ id: 1 })
```

### Objects
```typescript
expect(object).toHaveProperty('key')
expect(object).toHaveProperty('key', 'value')
expect(object).toMatchObject({ subset: 'value' })
```

### Exceptions
```typescript
expect(() => throwError()).toThrow()
expect(() => throwError()).toThrow(Error)
expect(() => throwError()).toThrow('message')
expect(() => throwError()).toThrow(/pattern/)
```

## Edge Cases to Test

### Boundary Values
- Empty strings, arrays, objects
- Null and undefined
- Zero and negative numbers
- Maximum values

### Invalid Input
- Wrong types
- Out of range values
- Malformed data
- Missing required fields

### State Transitions
- Initial state
- Intermediate states
- Final state
- Invalid state transitions

## Test Data Management

### Factory Functions
```typescript
// TODO: Add factory function example
// Show how to create test data builders
```

### Fixtures
```typescript
// TODO: Add fixture management
// Load from files, generate programmatically
```

### Parameterized Tests
```typescript
// TODO: Add test.each example
// Multiple test cases with different inputs
```

## Performance Considerations

### Keep Tests Fast
- Avoid I/O operations
- Mock heavy computations
- Use in-memory implementations
- Parallelize test execution

### Optimize Test Setup
```typescript
// Use beforeEach for shared setup
beforeEach(() => {
  // Setup that runs before each test
})

// Use beforeAll for expensive one-time setup
beforeAll(() => {
  // One-time setup
})
```

## Common Mistakes

### 1. Testing Implementation Details
```typescript
// Bad - relies on internal structure
expect(instance._privateMethod()).toBe(true)

// Good - tests public API
expect(instance.publicMethod()).toBe(expected)
```

### 2. Test Interdependence
```typescript
// Bad - tests depend on execution order
let sharedState
it('test 1', () => { sharedState = 'value' })
it('test 2', () => { expect(sharedState).toBe('value') })

// Good - each test is independent
it('test 1', () => {
  const state = 'value'
  expect(state).toBe('value')
})
```

### 3. Over-Mocking
```typescript
// Bad - mocks too much
vi.mock('./utils')
vi.mock('./helpers')
vi.mock('./constants')

// Good - only mock external boundaries
// TODO: Add better example
```

## Tools and Utilities

### Vitest
- Built-in mocking
- Fast execution
- ESM support
- Watch mode

### Jest
- Mature ecosystem
- Snapshot testing
- Wide adoption

### Assertion Libraries
- Expect (built-in)
- Custom matchers
- Asymmetric matchers

## Best Practices Checklist

- [ ] Each test tests one thing
- [ ] Tests are independent
- [ ] Tests run fast (< 100ms each)
- [ ] Test names describe behavior
- [ ] Edge cases are covered
- [ ] Error cases are tested
- [ ] No side effects
- [ ] Mock external dependencies
- [ ] Use meaningful assertions
- [ ] Clean up after tests

## Additional Resources

- [TESTING_STRATEGY.md](./TESTING_STRATEGY.md) - Overall testing approach
- [MOCKING_PATTERNS.md](./MOCKING_PATTERNS.md) - Advanced mocking
- [VITEST_PATTERNS.md](./VITEST_PATTERNS.md) - Vitest-specific patterns
- [TDD_PATTERNS.md](./TDD_PATTERNS.md) - Test-driven development
