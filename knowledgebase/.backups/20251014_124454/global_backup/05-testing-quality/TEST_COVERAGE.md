# Test Coverage Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Coverage strategies, meaningful metrics

## Overview

Test coverage measures how much of your code is executed during tests. While important, coverage percentage alone doesn't guarantee quality tests.

## Core Principles

1. **Meaningful Coverage** - Not just percentage
2. **Critical Path Focus** - High coverage where it matters
3. **Branch Coverage** - Test all code paths
4. **Quality Over Quantity** - Good tests, not just many tests
5. **Incremental Improvement** - Gradually increase coverage

## Coverage Metrics

### Lines Coverage
Percentage of code lines executed during tests.

### Branch Coverage
Percentage of decision branches tested (if/else, switch).

### Function Coverage
Percentage of functions called during tests.

### Statement Coverage
Percentage of statements executed.

## Coverage Goals

### Recommended Thresholds
- Overall: 75-80%
- Critical business logic: 90%+
- New code: 80%+
- Utility functions: 90%+
- Configuration: Not required

### What to Cover Heavily
- Business logic
- User-facing features
- Security-sensitive code
- Data transformations
- API endpoints
- Error handling

### What Not to Cover
- Third-party code
- Type definitions
- Configuration files
- Trivial getters/setters
- Auto-generated code

## Configuring Coverage

### Vitest
```typescript
// TODO: Add Vitest coverage config
```

### Coverage Thresholds
```typescript
coverage: {
  thresholds: {
    lines: 75,
    functions: 75,
    branches: 75,
    statements: 75
  }
}
```

## Coverage Reports

### HTML Report
Interactive visualization of coverage.

### Console Report
Quick overview in terminal.

### LCOV Report
For CI/CD integration.

## Coverage Anti-Patterns

### 1. Chasing 100%
Not always worth the effort.

### 2. Testing for Coverage
Write tests for behavior, not metrics.

### 3. Ignoring Branch Coverage
Line coverage alone is insufficient.

## CI/CD Integration

### Fail Build on Low Coverage
```typescript
// TODO: Add CI coverage check
```

### Track Coverage Trends
Monitor coverage over time.

## Best Practices

1. Focus on meaningful coverage
2. Test critical paths thoroughly
3. Don't ignore edge cases
4. Track branch coverage
5. Review uncovered code regularly
6. Use coverage to find gaps
7. Don't aim for 100% blindly
8. Combine with other metrics
9. Make coverage visible
10. Improve incrementally

## Additional Resources

- [TESTING_STRATEGY.md](./TESTING_STRATEGY.md) - Testing approach
- [CODE_QUALITY.md](./CODE_QUALITY.md) - Quality practices
