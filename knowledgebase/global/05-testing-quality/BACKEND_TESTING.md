# Backend Testing Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: API testing best practices, Express testing patterns, Node.js testing

## Overview

Backend testing covers API endpoints, business logic, database operations, and service integrations. This guide focuses on Node.js/Express patterns but principles apply broadly.

## Core Principles

1. **Test Business Logic First** - Core logic is most critical
2. **Integration Tests for APIs** - Test full request/response cycle
3. **Mock External Services** - Don't depend on third parties
4. **Use Test Database** - Isolated test data
5. **Test Error Paths** - Not just happy paths

## Test Layers

### Unit Tests
- Service functions
- Utilities
- Business logic
- Validators

### Integration Tests
- API endpoints
- Database operations
- Service layer
- Middleware

### Contract Tests
- API contracts
- Third-party integrations

## Testing API Endpoints

### Supertest Setup
```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest'
import request from 'supertest'
import { app } from '../app'

describe('API Endpoints', () => {
  beforeAll(async () => {
    // Setup test database
  })

  afterAll(async () => {
    // Cleanup
  })

  it('GET /api/users should return users', async () => {
    const response = await request(app)
      .get('/api/users')
      .expect(200)

    expect(response.body).toHaveProperty('users')
    expect(Array.isArray(response.body.users)).toBe(true)
  })
})
```

### Testing Different HTTP Methods
```typescript
// TODO: Add examples for GET, POST, PUT, DELETE, PATCH
```

### Testing Request Bodies
```typescript
// TODO: Add request body validation testing
```

### Testing Query Parameters
```typescript
// TODO: Add query param testing
// Filtering, sorting, pagination
```

### Testing Headers
```typescript
// TODO: Add header testing
// Authorization, Content-Type, custom headers
```

## Authentication Testing

### Testing Protected Routes
```typescript
// TODO: Add auth middleware testing
// Without token, invalid token, valid token
```

### Testing Authorization
```typescript
// TODO: Add role-based access control testing
```

### Token Management
```typescript
// TODO: Add JWT token generation for tests
```

## Database Testing

### Test Database Setup
```typescript
// TODO: Add test database configuration
// In-memory, separate test DB, Docker
```

### Seeding Test Data
```typescript
// TODO: Add data seeding patterns
// Factories, fixtures, builders
```

### Transaction Rollback
```typescript
// TODO: Add rollback pattern
// Each test in transaction, rollback after
```

### Testing Queries
```typescript
// TODO: Add database query testing
// Create, read, update, delete operations
```

## Testing Services

### Service Layer Tests
```typescript
// TODO: Add service testing pattern
// Business logic, data transformation
```

### Dependency Injection
```typescript
// TODO: Add DI pattern for testing
// Mock repositories, services
```

## Mocking External Services

### HTTP Client Mocking
```typescript
// TODO: Add axios/fetch mocking
// Using msw or vi.mock
```

### Third-Party APIs
```typescript
// TODO: Add third-party service mocking
// Payment gateways, email services
```

### File System Operations
```typescript
// TODO: Add fs mocking
```

## Testing Middleware

### Testing Express Middleware
```typescript
// TODO: Add middleware testing
// Error handling, authentication, logging
```

### Testing Request/Response Flow
```typescript
// TODO: Add req/res/next testing pattern
```

## Error Handling

### Testing Error Responses
```typescript
it('should return 400 for invalid input', async () => {
  const response = await request(app)
    .post('/api/users')
    .send({ email: 'invalid' })
    .expect(400)

  expect(response.body).toHaveProperty('error')
})
```

### Testing Error Middleware
```typescript
// TODO: Add error middleware testing
```

### Testing Async Errors
```typescript
// TODO: Add async error handling tests
```

## Testing WebSockets

### Socket.io Testing
```typescript
// TODO: Add Socket.io testing patterns
```

### Real-time Events
```typescript
// TODO: Add event emission/reception testing
```

## Testing Background Jobs

### Queue Testing
```typescript
// TODO: Add job queue testing
// Bull, BullMQ patterns
```

### Scheduled Tasks
```typescript
// TODO: Add cron job testing
```

## Testing File Uploads

### Multipart Form Data
```typescript
// TODO: Add file upload testing
// Using supertest with files
```

### File Validation
```typescript
// TODO: Add file type/size validation tests
```

## Performance Testing

### Load Testing
```typescript
// TODO: Add basic load testing pattern
// Using autocannon or k6
```

### Response Time Testing
```typescript
// TODO: Add response time assertions
```

## Testing Validation

### Input Validation
```typescript
// TODO: Add Zod/Joi validation testing
```

### Schema Validation
```typescript
// TODO: Add schema validation tests
```

## Database-Specific Patterns

### PostgreSQL Testing
```typescript
// TODO: Add PostgreSQL test patterns
// Transactions, rollback, schemas
```

### MongoDB Testing
```typescript
// TODO: Add MongoDB test patterns
// In-memory MongoDB, cleanup
```

### Redis Testing
```typescript
// TODO: Add Redis testing
// Cache testing, session storage
```

## Testing Patterns

### Pattern 1: Repository Pattern Testing
```typescript
// TODO: Add repository pattern tests
// Data layer abstraction testing
```

### Pattern 2: Controller Testing
```typescript
// TODO: Add controller testing
// Request handling, response formatting
```

### Pattern 3: Use Case Testing
```typescript
// TODO: Add use case/command testing
// Business logic orchestration
```

## Test Helpers

### Test Factories
```typescript
// TODO: Add factory pattern
// Generate test users, posts, etc.
```

### Request Builders
```typescript
// TODO: Add request builder pattern
// Fluent API for test requests
```

### Response Matchers
```typescript
// TODO: Add custom matchers
// toBeValidUser, toHaveCorrectSchema
```

## CI/CD Integration

### GitHub Actions for Backend
```yaml
# TODO: Add backend testing workflow
# DB setup, migrations, tests
```

### Docker Compose for Tests
```yaml
# TODO: Add docker-compose for tests
# Database, Redis, services
```

## Best Practices

1. **Use Test Database** - Never test on production data
2. **Reset State** - Clean database between tests
3. **Mock External Services** - Don't call real APIs
4. **Test Error Cases** - Not just happy paths
5. **Use Factories** - Generate test data easily
6. **Test Transactions** - Rollback after each test
7. **Test Authentication** - Protected route coverage
8. **Test Validation** - Invalid input handling
9. **Performance Tests** - Load and stress testing
10. **Integration Over Unit** - API-level tests provide confidence

## Common Mistakes

### 1. Testing Against Production DB
```typescript
// Bad - uses production database
// Good - use test database with cleanup
```

### 2. Shared Test State
```typescript
// Bad - tests depend on each other
// Good - each test sets up own data
```

### 3. Not Mocking External Services
```typescript
// Bad - calls real third-party API
// Good - mock external dependencies
```

## Testing Frameworks Comparison

### Vitest (Recommended for New Projects)
- Fast execution
- ESM native
- Great DX

### Jest (Mature, Stable)
- Widely adopted
- Large ecosystem
- Proven stability

### Mocha + Chai
- Flexible
- Minimal
- More setup required

## Tools and Libraries

### HTTP Testing
- supertest - HTTP assertions
- got/axios - HTTP clients
- msw - API mocking

### Database
- @databases/pg-test - PostgreSQL
- mongodb-memory-server - MongoDB
- ioredis-mock - Redis

### Mocking
- Vitest/Jest mocks
- Sinon - Standalone mocking
- nock - HTTP mocking

## Additional Resources

- [TESTING_STRATEGY.md](./TESTING_STRATEGY.md) - Overall approach
- [INTEGRATION_TESTING.md](./INTEGRATION_TESTING.md) - Integration patterns
- [MOCKING_PATTERNS.md](./MOCKING_PATTERNS.md) - Mocking strategies
