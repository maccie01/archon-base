# Repository Layer Best Practices

Created: 2025-10-13

## Overview

Repositories abstract data access, hiding database implementation details from services.

## Repository Pattern

```typescript
import { Pool, PoolClient } from 'pg';

export class UserRepository {
  constructor(private pool: Pool) {}

  async findById(id: string): Promise<User | null> {
    const result = await this.pool.query(
      'SELECT * FROM users WHERE id = $1',
      [id]
    );
    return result.rows[0] || null;
  }

  async findAll(limit = 100, offset = 0): Promise<User[]> {
    const result = await this.pool.query(
      'SELECT * FROM users LIMIT $1 OFFSET $2',
      [limit, offset]
    );
    return result.rows;
  }

  async create(data: CreateUserData): Promise<User> {
    const result = await this.pool.query(
      `INSERT INTO users (username, email, password)
       VALUES ($1, $2, $3) RETURNING *`,
      [data.username, data.email, data.password]
    );
    return result.rows[0];
  }

  async update(id: string, data: Partial<User>): Promise<User> {
    const result = await this.pool.query(
      `UPDATE users 
       SET username = COALESCE($1, username),
           email = COALESCE($2, email),
           updated_at = NOW()
       WHERE id = $3 RETURNING *`,
      [data.username, data.email, id]
    );
    return result.rows[0];
  }

  async delete(id: string): Promise<void> {
    await this.pool.query('DELETE FROM users WHERE id = $1', [id]);
  }
}

export const userRepository = new UserRepository(pool);
```

## Transaction Support

```typescript
// Support optional client for transactions
async create(data: CreateUserData, client?: PoolClient): Promise<User> {
  const db = client || this.pool;
  const result = await db.query(
    'INSERT INTO users (...) VALUES (...) RETURNING *',
    [...]
  );
  return result.rows[0];
}
```

## Best Practices

1. **Single Responsibility**: One repository per table/entity
2. **Hide Database Details**: Return domain objects
3. **Parameterized Queries**: Prevent SQL injection
4. **Transaction Support**: Accept optional client
5. **Error Handling**: Let errors bubble up

See DATABASE_PATTERNS.md for more details.
