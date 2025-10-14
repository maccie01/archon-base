# Testing Strategy

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Industry best practices, Testing Trophy, Kent C. Dodds principles

## Overview

A comprehensive testing strategy ensures code quality, prevents regressions, and enables confident refactoring. This document outlines a balanced approach to testing modern web applications.

## Core Principles

1. **Test Behavior, Not Implementation** - Focus on what the code does, not how it does it
2. **Write Tests for Confidence** - Test to ensure your code works, not to achieve coverage metrics
3. **Maintain Test Independence** - Each test should run in isolation
4. **Keep Tests Simple** - Tests should be easier to understand than the code they test
5. **Fast Feedback Loops** - Optimize for quick test execution

## The Testing Pyramid

The traditional testing pyramid guides test distribution:

```
        /\
       /E2E\      10% - End-to-End Tests
      /------\
     /Integr-\   20% - Integration Tests
    /----------\
   /   Unit     \ 70% - Unit Tests
  /--------------\
```

### Unit Tests (70%)
- Test individual functions, methods, or components in isolation
- Fast execution (milliseconds)
- High volume, low maintenance
- Mock external dependencies

### Integration Tests (20%)
- Test interactions between modules or components
- Moderate execution time (seconds)
- Test real integrations where possible
- Balance between coverage and speed

### End-to-End Tests (10%)
- Test complete user workflows
- Slower execution (seconds to minutes)
- Test critical user paths
- Run against production-like environment

## Alternative: The Testing Trophy

Some teams prefer the Testing Trophy model, which emphasizes integration tests:

```
        /\
       /E2E\      5% - End-to-End Tests
      /------\
     /Integr-\   50% - Integration Tests
    /----------\
   /   Unit     \ 40% - Unit Tests
  /--------------\
   Static Analysis  - ESLint, TypeScript, etc.
```

Choose based on your application characteristics:
- API-heavy apps: More integration tests
- UI-heavy apps: More component tests
- Utility libraries: More unit tests

## Testing Levels Defined

### Static Testing
- TypeScript type checking
- ESLint for code patterns
- Prettier for formatting
- Cost: Zero runtime cost
- Benefit: Catches errors before runtime

### Unit Testing
**When to use:**
- Pure functions
- Business logic
- Utility functions
- Complex algorithms

**What to test:**
```typescript
// TODO: Add example - testing pure utility function
```

### Integration Testing
**When to use:**
- Component interactions
- API endpoint flows
- Database operations
- Service layer logic

**What to test:**
```typescript
// TODO: Add example - testing API endpoint with database
```

### End-to-End Testing
**When to use:**
- Critical user journeys
- Authentication flows
- Checkout processes
- Complex multi-step workflows

**What to test:**
```typescript
// TODO: Add example - testing login to dashboard flow
```

## Test Naming Conventions

Use descriptive names that explain the scenario:

```typescript
// Good
describe('UserService.createUser', () => {
  it('should create user with valid data', () => {})
  it('should throw ValidationError when email is invalid', () => {})
  it('should hash password before storing', () => {})
})

// Avoid
describe('UserService', () => {
  it('works', () => {})
  it('test 2', () => {})
})
```

## AAA Pattern (Arrange-Act-Assert)

Structure tests consistently:

```typescript
it('should calculate total with tax', () => {
  // Arrange - Set up test data
  const items = [{ price: 100 }, { price: 200 }]
  const taxRate = 0.1

  // Act - Execute the function
  const result = calculateTotal(items, taxRate)

  // Assert - Verify the result
  expect(result).toBe(330)
})
```

## Test Data Management

### Test Fixtures
Create reusable test data:

```typescript
// TODO: Add example - test fixture factory
```

### Database Seeding
For integration tests:

```typescript
// TODO: Add example - database seeding strategy
```

## Coverage Goals

### Recommended Thresholds
- **Overall Coverage**: 75-80%
- **Critical Paths**: 90%+
- **New Code**: 80%+
- **Branch Coverage**: 75%+

### What NOT to Test
- Third-party libraries
- Framework code
- Type definitions
- Simple getters/setters
- Configuration files

### Meaningful Coverage
Focus on:
- Business logic
- User interactions
- Error handling
- Edge cases
- Critical paths

## Testing in CI/CD

### Pre-commit
- Unit tests for changed files
- Linting and formatting
- Type checking

### Pre-push
- All unit tests
- Integration tests
- Quick E2E smoke tests

### CI Pipeline
- Full test suite
- Coverage reporting
- E2E tests on staging
- Visual regression tests

## Test Maintenance

### Red Flags
- Tests break on refactoring
- Tests test implementation details
- Tests require frequent updates
- Flaky tests (intermittent failures)
- Tests take too long to run

### Best Practices
- Review tests in code reviews
- Refactor tests with production code
- Remove obsolete tests
- Update test data regularly
- Monitor test execution time

## Common Anti-Patterns

### 1. Testing Implementation Details
```typescript
// Bad - tests internal state
expect(component.state.count).toBe(1)

// Good - tests user-visible behavior
expect(screen.getByText('Count: 1')).toBeInTheDocument()
```

### 2. Excessive Mocking
```typescript
// Bad - mocks everything
vi.mock('./dependency1')
vi.mock('./dependency2')
vi.mock('./dependency3')

// Good - only mock external boundaries
// TODO: Add better mocking example
```

### 3. One Large Test
```typescript
// Bad - tests everything in one test
it('should handle entire user lifecycle', () => {
  // 200 lines of test code
})

// Good - split into focused tests
it('should create user', () => {})
it('should update user profile', () => {})
it('should delete user', () => {})
```

## Tools and Libraries

### Test Runners
- **Vitest** - Fast, modern, Vite-native
- **Jest** - Mature, widely adopted
- **Mocha** - Flexible, minimalist

### Assertion Libraries
- Built-in assertions (Vitest, Jest)
- Chai (with Mocha)

### Mocking
- Vitest/Jest mock functions
- MSW (Mock Service Worker) for API mocking
- Test doubles (stubs, spies, fakes)

### Coverage
- c8 (native Node.js coverage)
- Istanbul/nyc
- V8 coverage provider

## Framework-Specific Guides

- [VITEST_PATTERNS.md](./VITEST_PATTERNS.md) - Vitest setup and patterns
- [REACT_TESTING.md](./REACT_TESTING.md) - React Testing Library
- [BACKEND_TESTING.md](./BACKEND_TESTING.md) - API and backend testing
- [E2E_TESTING.md](./E2E_TESTING.md) - Playwright and Cypress

## Additional Resources

- [Testing Trophy by Kent C. Dodds](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)
- [Testing Best Practices](https://testingjavascript.com/)
- [Vitest Documentation](https://vitest.dev/)
- [Testing Library Documentation](https://testing-library.com/)
