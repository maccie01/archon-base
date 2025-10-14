# Middleware Patterns

Created: 2025-10-13

## Overview

Middleware functions have access to request, response, and next. They can modify requests, end responses, or pass control to the next middleware.

## Common Middleware Types

### 1. Authentication Middleware

```typescript
export function requireAuth(req, res, next) {
  if (!req.session?.user) {
    throw createAuthError('Authentication required');
  }
  next();
}

// Usage
router.get('/profile', requireAuth, userController.getProfile);
```

### 2. Authorization Middleware

```typescript
export function requireRole(role: string) {
  return (req, res, next) => {
    if (req.session?.user?.role !== role) {
      throw createForbiddenError('Insufficient permissions');
    }
    next();
  };
}

// Usage
router.delete('/users/:id', requireRole('admin'), userController.deleteUser);
```

### 3. Validation Middleware

```typescript
export function validate(schema: ZodSchema, source = 'body') {
  return async (req, res, next) => {
    try {
      req[source] = await schema.parseAsync(req[source]);
      next();
    } catch (error) {
      throw createValidationError('Validation failed', error.errors);
    }
  };
}

// Usage
router.post('/users', validate(createUserSchema), userController.createUser);
```

### 4. Error Handling Middleware

```typescript
export function errorHandler(err, req, res, next) {
  console.error(err);
  
  const status = err.statusCode || 500;
  const message = err.message || 'Internal Server Error';
  
  res.status(status).json({ message, status });
}

// Must be last middleware
app.use(errorHandler);
```

### 5. Logging Middleware

```typescript
export function requestLogger(req, res, next) {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    logger.info({
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration,
    });
  });
  
  next();
}
```

## Best Practices

1. **Order matters**: Place middleware in correct order
2. **Always call next()**: Or end the response
3. **Error handling**: Use next(error) for errors
4. **Reusability**: Create composable middleware
5. **Type safety**: Use TypeScript types

## Additional Resources

- See EXPRESS_BEST_PRACTICES.md for order
- See AUTHENTICATION.md for auth patterns
- See VALIDATION.md for validation
