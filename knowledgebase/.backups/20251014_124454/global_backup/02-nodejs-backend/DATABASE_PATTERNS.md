# Database Patterns for Node.js

Created: 2025-10-13
Last Updated: 2025-10-13

## Overview

Database patterns for PostgreSQL with pg driver, including connection pooling, transactions, and query patterns.

## Connection Pooling

```typescript
import { Pool } from 'pg';

export class ConnectionPoolManager {
  private pool: Pool;

  async initialize() {
    this.pool = new Pool({
      connectionString: process.env.DATABASE_URL,
      min: 5,                    // Minimum connections
      max: 20,                   // Maximum connections
      idleTimeoutMillis: 30000,  // Close idle connections
      connectionTimeoutMillis: 5000,
      keepAlive: true,
    });

    this.pool.on('error', (err) => {
      console.error('Unexpected pool error:', err);
    });
  }

  getPool() {
    return this.pool;
  }

  async query(text: string, params?: any[]) {
    return await this.pool.query(text, params);
  }

  async shutdown() {
    await this.pool.end();
  }
}
```

## Repository Pattern

```typescript
export class UserRepository {
  constructor(private pool: Pool) {}

  async findById(id: string): Promise<User | null> {
    const result = await this.pool.query(
      'SELECT * FROM users WHERE id = $1',
      [id]
    );
    return result.rows[0] || null;
  }

  async findByEmail(email: string): Promise<User | null> {
    const result = await this.pool.query(
      'SELECT * FROM users WHERE email = $1',
      [email]
    );
    return result.rows[0] || null;
  }

  async create(data: CreateUserData): Promise<User> {
    const result = await this.pool.query(
      `INSERT INTO users (username, email, password, role)
       VALUES ($1, $2, $3, $4)
       RETURNING *`,
      [data.username, data.email, data.password, data.role]
    );
    return result.rows[0];
  }

  async update(id: string, data: Partial<User>): Promise<User> {
    const result = await this.pool.query(
      `UPDATE users 
       SET username = COALESCE($1, username),
           email = COALESCE($2, email),
           updated_at = NOW()
       WHERE id = $3
       RETURNING *`,
      [data.username, data.email, id]
    );
    return result.rows[0];
  }

  async delete(id: string): Promise<void> {
    await this.pool.query('DELETE FROM users WHERE id = $1', [id]);
  }
}
```

## Transaction Patterns

```typescript
// Service with transaction
export class OrderService {
  async createOrder(data: CreateOrderData): Promise<Order> {
    const client = await pool.connect();

    try {
      await client.query('BEGIN');

      const order = await this.createOrderRecord(data, client);
      await this.updateInventory(data.items, client);
      await this.createPayment(data.payment, client);

      await client.query('COMMIT');
      return order;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }

  private async createOrderRecord(data: CreateOrderData, client: PoolClient) {
    const result = await client.query(
      'INSERT INTO orders (...) VALUES (...) RETURNING *',
      [...]
    );
    return result.rows[0];
  }
}
```

## Query Optimization

```typescript
// Use indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_posts_user_id ON posts(user_id);

// Use prepared statements (automatic with parameterized queries)
const result = await pool.query(
  'SELECT * FROM users WHERE email = $1',
  [email]
);

// Avoid N+1 queries
// BAD: N+1 queries
const posts = await postRepository.findAll();
for (const post of posts) {
  post.author = await userRepository.findById(post.userId);
}

// GOOD: Join query
const posts = await pool.query(`
  SELECT posts.*, users.username as author_name
  FROM posts
  JOIN users ON posts.user_id = users.id
`);
```

## Best Practices

1. **Always Use Parameterized Queries**: Prevent SQL injection
2. **Connection Pooling**: Reuse connections
3. **Transactions**: Use for multi-step operations
4. **Indexes**: Index foreign keys and frequent queries
5. **Error Handling**: Always release connections
6. **Timeouts**: Set connection and query timeouts

## Additional Resources

- See REPOSITORY_LAYER.md for patterns
- See SERVICE_LAYER.md for transaction management
- PostgreSQL documentation
