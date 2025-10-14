# Service Layer Best Practices

Created: 2025-10-13
Last Updated: 2025-10-13

## Overview

Services contain business logic and orchestrate operations between repositories. They are the heart of your application.

## Core Principles

1. **Business Logic**: All business rules live here
2. **Orchestration**: Coordinate multiple repositories
3. **Transaction Management**: Handle database transactions
4. **Framework Independence**: No HTTP or database specifics
5. **Testability**: Easy to unit test

## Service Pattern

```typescript
import { userRepository } from './user.repository';
import { emailService } from '../email/email.service';
import { createValidationError, createNotFoundError } from '../../middleware/error';
import type { User, CreateUserData, UpdateUserData } from './user.types';

export class UserService {
  /**
   * Get user by ID with business logic
   */
  async getUser(id: string): Promise<User | null> {
    const user = await userRepository.findById(id);
    
    if (!user) {
      return null;
    }
    
    // Business logic: Hide sensitive fields
    return this.sanitizeUser(user);
  }

  /**
   * Create new user with validation and email notification
   */
  async createUser(data: CreateUserData): Promise<User> {
    // Business rule: Check if username exists
    const existingUser = await userRepository.findByUsername(data.username);
    if (existingUser) {
      throw createValidationError('Username already taken');
    }

    // Business rule: Validate email format
    if (!this.isValidEmail(data.email)) {
      throw createValidationError('Invalid email format');
    }

    // Create user
    const user = await userRepository.create(data);

    // Send welcome email (async, non-blocking)
    emailService.sendWelcome(user.email).catch(err => {
      console.error('Failed to send welcome email:', err);
    });

    return this.sanitizeUser(user);
  }

  /**
   * Update user with validation
   */
  async updateUser(id: string, updates: UpdateUserData): Promise<User> {
    const user = await userRepository.findById(id);
    
    if (!user) {
      throw createNotFoundError('User not found');
    }

    // Business rule: Cannot change username
    if (updates.username && updates.username !== user.username) {
      throw createValidationError('Username cannot be changed');
    }

    const updatedUser = await userRepository.update(id, updates);
    return this.sanitizeUser(updatedUser);
  }

  /**
   * Delete user with cascade logic
   */
  async deleteUser(id: string): Promise<void> {
    const user = await userRepository.findById(id);
    
    if (!user) {
      throw createNotFoundError('User not found');
    }

    // Business rule: Cannot delete active users
    if (user.status === 'active') {
      throw createValidationError('Cannot delete active user');
    }

    await userRepository.delete(id);
  }

  /**
   * Business logic helper: Sanitize user data
   */
  private sanitizeUser(user: User): User {
    const { password, ...sanitized } = user;
    return sanitized as User;
  }

  /**
   * Business logic helper: Validate email
   */
  private isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
}

// Export singleton
export const userService = new UserService();
```

## Transaction Management

```typescript
import { getConnectionPool } from '../../connection-pool';

export class OrderService {
  /**
   * Create order with transaction
   */
  async createOrder(data: CreateOrderData): Promise<Order> {
    const pool = getConnectionPool().getPool();
    const client = await pool.connect();

    try {
      await client.query('BEGIN');

      // Multiple operations in transaction
      const order = await orderRepository.create(data, client);
      await inventoryRepository.decrementStock(data.items, client);
      await paymentRepository.createCharge(data.payment, client);

      await client.query('COMMIT');
      return order;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }
}
```

## Common Patterns

### Singleton Pattern

```typescript
class UserService {
  private static instance: UserService;

  private constructor() {}

  static getInstance(): UserService {
    if (!UserService.instance) {
      UserService.instance = new UserService();
    }
    return UserService.instance;
  }
}

export const userService = UserService.getInstance();
```

### Dependency Injection

```typescript
export class UserService {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService
  ) {}

  async createUser(data: CreateUserData): Promise<User> {
    const user = await this.userRepository.create(data);
    await this.emailService.sendWelcome(user.email);
    return user;
  }
}
```

## Best Practices

1. **Single Responsibility**: Each service handles one domain
2. **Business Logic Only**: No HTTP or database concerns
3. **Return Domain Objects**: Not database rows
4. **Handle Transactions**: Use transactions for multi-step operations
5. **Validate Business Rules**: Check constraints and rules
6. **Error Handling**: Throw descriptive errors
7. **Testability**: Easy to mock dependencies

## Additional Resources

- See REPOSITORY_LAYER.md for data access
- See ARCHITECTURE_PATTERNS.md for layering
- See DATABASE_PATTERNS.md for transactions
