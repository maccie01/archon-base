# Database Testing Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Database testing patterns, test database strategies, fixture management

## Overview

Testing database code is essential but often neglected. Proper testing strategies balance speed, isolation, and realism.

## Core Principles

1. Test database code like any other code
2. Use separate test database - never test on production
3. Each test should be isolated and idempotent
4. Fast tests encourage frequent testing
5. Test both happy paths and edge cases

## Test Database Setup

### Separate Test Database

```typescript
// TODO: Add test database configuration
# Separate DATABASE_URL for tests
# Docker containers for test databases
```

### Schema Setup

```typescript
// TODO: Add test schema setup
# Running migrations before tests
# Resetting database between test suites
```

## Testing Strategies

### Strategy 1: Transactions (Fast)

```typescript
// TODO: Add transaction-based testing
# Wrap each test in transaction
# Rollback after test
# Fast but limited
```

### Strategy 2: Truncate Tables

```typescript
// TODO: Add truncate strategy
# Delete all data between tests
# Faster than migrations
# Preserves schema
```

### Strategy 3: Full Reset

```typescript
// TODO: Add full reset strategy
# Drop and recreate database
# Slowest but most thorough
```

## Fixture Management

### Test Data Setup

```typescript
// TODO: Add fixture patterns
# Factory functions
# Seed scripts
# Reusable test data
```

### Factory Pattern

```typescript
// TODO: Add factory example
# createUser(), createPost(), etc.
# Faker for realistic data
```

## Testing Patterns

### Unit Testing Queries

```typescript
// TODO: Add query unit tests
# Testing individual queries
# Mocking vs real database
```

### Integration Testing

```typescript
// TODO: Add integration test examples
# Testing full workflows
# Multiple operations
```

### Testing Migrations

```typescript
// TODO: Add migration testing
# Up and down migrations
# Data integrity after migration
```

## Mocking Strategies

### When to Mock

```
# TODO: Add mocking guidance
# Unit tests: mock database
# Integration tests: real database
```

### Mocking with Vitest/Jest

```typescript
// TODO: Add mocking examples
# Mocking Drizzle
# Mocking database queries
```

## Testing Tools

### Testing Frameworks

- Vitest
- Jest
- Mocha/Chai

### Database Testing Tools

- Testcontainers
- Docker Compose
- In-memory SQLite (for simple tests)

## Common Testing Scenarios

### Testing Constraints

```typescript
// TODO: Add constraint testing
# Foreign key violations
# Unique constraints
# CHECK constraints
```

### Testing Transactions

```typescript
// TODO: Add transaction testing
# Rollback on error
# Nested transactions
```

## CI/CD Integration

```yaml
# TODO: Add CI pipeline database setup
# Docker services
# Running migrations
# Running tests
```

## Additional Resources

### Related Knowledge Base Articles
- [Drizzle ORM Patterns](./DRIZZLE_PATTERNS.md)
- [Schema Migrations](./SCHEMA_MIGRATIONS.md)
- [Database Design](./DATABASE_DESIGN.md)
