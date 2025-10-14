# Async Patterns

Created: 2025-10-13

## Overview

Best practices for async/await in Node.js.

## Basic Pattern

```typescript
// Always use async/await
async function getUser(id: string): Promise<User> {
  const user = await userRepository.findById(id);
  return user;
}
```

## Error Handling

```typescript
// Use try/catch for specific error handling
async function createUser(data: CreateUserData): Promise<User> {
  try {
    const user = await userRepository.create(data);
    await emailService.sendWelcome(user.email);
    return user;
  } catch (error) {
    console.error('Failed to create user:', error);
    throw error;
  }
}

// Or let errors bubble up (preferred)
async function getUser(id: string): Promise<User> {
  const user = await userRepository.findById(id);
  if (!user) {
    throw createNotFoundError('User not found');
  }
  return user;
}
```

## Parallel Operations

```typescript
// Sequential (slow)
const user = await getUser(userId);
const posts = await getPosts(userId);
const comments = await getComments(userId);

// Parallel (fast)
const [user, posts, comments] = await Promise.all([
  getUser(userId),
  getPosts(userId),
  getComments(userId),
]);
```

## Best Practices

1. **Always use async/await**: Not callbacks
2. **Handle errors**: Try/catch or let bubble up
3. **Parallel when possible**: Use Promise.all
4. **Don't block event loop**: Use async operations
5. **asyncHandler for routes**: Catch async errors

See ERROR_HANDLING.md for error patterns.
