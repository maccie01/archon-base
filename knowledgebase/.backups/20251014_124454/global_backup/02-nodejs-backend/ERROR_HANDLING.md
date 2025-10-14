# Error Handling Best Practices

Created: 2025-10-13
Last Updated: 2025-10-13

## Overview

Proper error handling is critical for production applications. Use custom error classes and centralized error middleware.

## Custom Error Class

```typescript
export class AppError extends Error {
  public statusCode: number;
  public isOperational: boolean;
  public details?: any;

  constructor(message: string, statusCode = 500, details?: any) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
    this.details = details;
    Error.captureStackTrace(this, this.constructor);
  }
}
```

## Error Factory Functions

```typescript
export function createValidationError(message: string, details?: any) {
  return new AppError(message, 400, details);
}

export function createAuthError(message: string) {
  return new AppError(message, 401);
}

export function createForbiddenError(message: string) {
  return new AppError(message, 403);
}

export function createNotFoundError(message: string) {
  return new AppError(message, 404);
}

export function createDatabaseError(message: string, details?: any) {
  return new AppError(message, 500, details);
}
```

## Error Middleware

```typescript
export function errorHandler(
  err: Error | AppError,
  req: Request,
  res: Response,
  next: NextFunction
) {
  console.error('Error occurred:', {
    message: err.message,
    stack: err.stack,
    url: req.url,
    method: req.method,
  });

  let errorResponse = {
    message: "Internal Server Error",
    status: 500
  };

  if (err instanceof AppError) {
    errorResponse = {
      message: err.message,
      status: err.statusCode,
      ...(err.details && { details: err.details })
    };
  }

  res.status(errorResponse.status).json(errorResponse);
}
```

## Async Handler

```typescript
export function asyncHandler(fn: Function) {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}

// Usage
router.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await userService.getUser(req.params.id);
  res.json({ data: user });
}));
```

## Best Practices

1. **Always use asyncHandler**: Catch async errors
2. **Throw custom errors**: Use AppError
3. **Centralized handling**: Single error middleware
4. **Hide stack traces**: Don't expose in production
5. **Log errors**: Use structured logging
6. **Return consistent formats**: Standard error responses

## Additional Resources

- See EXPRESS_BEST_PRACTICES.md for middleware order
- See CONTROLLER_LAYER.md for error usage
