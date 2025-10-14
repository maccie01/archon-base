# Controller Layer Best Practices

Created: 2025-10-13
Last Updated: 2025-10-13
Research Sources: Express.js patterns, Netzwächter project analysis

## Overview

Controllers are the HTTP layer - they handle requests, call services, and return responses. Controllers should be thin, focusing only on HTTP concerns.

## Core Principles

1. **Thin Controllers**: Only HTTP request/response handling
2. **No Business Logic**: Delegate to services
3. **Consistent Responses**: Use standard formats
4. **Error Handling**: Use asyncHandler wrapper
5. **Input Validation**: Validate before processing

## Controller Pattern

```typescript
import type { Request, Response } from 'express';
import { asyncHandler, createValidationError, createNotFoundError } from '../../middleware/error';
import { userService } from './user.service';

export const userController = {
  /**
   * GET /api/users/:id
   * Get user by ID
   */
  getUser: asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;
    
    const user = await userService.getUser(id);
    
    if (!user) {
      throw createNotFoundError('User not found');
    }
    
    res.json({ data: user });
  }),

  /**
   * POST /api/users
   * Create new user
   */
  createUser: asyncHandler(async (req: Request, res: Response) => {
    const userData = req.body;
    
    const user = await userService.createUser(userData);
    
    res.status(201).json({ 
      data: user,
      message: 'User created successfully' 
    });
  }),

  /**
   * PATCH /api/users/:id
   * Update user
   */
  updateUser: asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;
    const updates = req.body;
    
    const user = await userService.updateUser(id, updates);
    
    res.json({ 
      data: user,
      message: 'User updated successfully' 
    });
  }),

  /**
   * DELETE /api/users/:id
   * Delete user
   */
  deleteUser: asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;
    
    await userService.deleteUser(id);
    
    res.status(204).send();
  }),
};
```

## Response Patterns

### Success Responses

```typescript
// 200 OK - Resource retrieved
res.json({ data: user });

// 201 Created - Resource created
res.status(201).json({ data: newUser, id: newUser.id });

// 204 No Content - Resource deleted
res.status(204).send();

// 200 OK with message
res.json({ data: result, message: 'Operation successful' });
```

### Error Responses

```typescript
// Let error middleware handle errors
throw createValidationError('Invalid input');
throw createNotFoundError('User not found');
throw createAuthError('Unauthorized');
throw createForbiddenError('Access denied');
```

## Request Validation

### Using Validation Middleware

```typescript
import { validate } from '../../middleware/validate';
import { createUserSchema, updateUserSchema } from './user.schemas';

export const userController = {
  createUser: asyncHandler(async (req: Request, res: Response) => {
    // Body is already validated by middleware
    const userData = req.body; // Type-safe after validation
    const user = await userService.createUser(userData);
    res.status(201).json({ data: user });
  }),
};

// In routes file
router.post('/users', validate(createUserSchema), userController.createUser);
```

### Manual Validation

```typescript
createUser: asyncHandler(async (req: Request, res: Response) => {
  const { username, email, password } = req.body;
  
  if (!username || !email || !password) {
    throw createValidationError('Username, email, and password are required');
  }
  
  if (password.length < 8) {
    throw createValidationError('Password must be at least 8 characters');
  }
  
  const user = await userService.createUser({ username, email, password });
  res.status(201).json({ data: user });
}),
```

## Common Mistakes

1. **Business Logic in Controllers**: Move to services
2. **Database Queries in Controllers**: Use repositories
3. **Not Using asyncHandler**: Async errors won't be caught
4. **Inconsistent Response Formats**: Use standard patterns
5. **Missing Input Validation**: Always validate user input
6. **Not Setting Status Codes**: Use appropriate HTTP codes
7. **Exposing Internal Errors**: Use error middleware

## Best Practices

1. **Use asyncHandler**: Wrap all async route handlers
2. **Validate Input**: Use middleware or manual validation
3. **Delegate to Services**: Controllers should be thin
4. **Consistent Responses**: Follow standard formats
5. **Document Endpoints**: Add JSDoc comments
6. **Type Safety**: Use TypeScript types
7. **Error Handling**: Throw custom errors, let middleware handle

## Additional Resources

- See SERVICE_LAYER.md for business logic patterns
- See MIDDLEWARE_PATTERNS.md for validation middleware
- See ERROR_HANDLING.md for error patterns
