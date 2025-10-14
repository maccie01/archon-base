# Backend Testing Patterns

Created: 2025-10-13

## Overview

Three levels of testing: Unit (services), Integration (repositories), E2E (full API).

## Unit Testing Services

```typescript
import { describe, it, expect, vi } from 'vitest';
import { UserService } from './user.service';

describe('UserService', () => {
  it('should create user', async () => {
    const mockRepository = {
      create: vi.fn().mockResolvedValue(mockUser),
      findByUsername: vi.fn().mockResolvedValue(null),
    };
    
    const service = new UserService(mockRepository);
    const result = await service.createUser(userData);
    
    expect(result).toEqual(mockUser);
    expect(mockRepository.create).toHaveBeenCalledWith(userData);
  });

  it('should throw error if username exists', async () => {
    const mockRepository = {
      findByUsername: vi.fn().mockResolvedValue(mockUser),
    };
    
    const service = new UserService(mockRepository);
    
    await expect(service.createUser(userData))
      .rejects.toThrow('Username already taken');
  });
});
```

## Integration Testing Repositories

```typescript
describe('UserRepository', () => {
  beforeAll(async () => {
    await setupTestDatabase();
  });

  afterAll(async () => {
    await teardownTestDatabase();
  });

  it('should create and retrieve user', async () => {
    const repository = new UserRepository(pool);
    
    const created = await repository.create(userData);
    expect(created).toHaveProperty('id');
    
    const retrieved = await repository.findById(created.id);
    expect(retrieved.username).toBe(userData.username);
  });
});
```

## E2E Testing APIs

```typescript
import request from 'supertest';
import { app } from '../app';

describe('POST /api/users', () => {
  it('should create user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send(userData)
      .expect(201);
    
    expect(response.body.data).toHaveProperty('id');
    expect(response.body.data.username).toBe(userData.username);
  });

  it('should require authentication', async () => {
    await request(app)
      .delete('/api/users/123')
      .expect(401);
  });

  it('should validate input', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ username: 'a' }) // Too short
      .expect(400);
    
    expect(response.body.message).toContain('Validation');
  });
});
```

## Best Practices

1. **Test Pyramid**: 60% unit, 30% integration, 10% E2E
2. **Mock External Dependencies**: Database, APIs, etc.
3. **Clean Test Data**: Setup and teardown
4. **Test Error Cases**: Not just happy path
5. **Use Test Factories**: Create test data easily

## Additional Resources

- Vitest documentation
- Supertest documentation
- See SERVICE_LAYER.md for testable services
