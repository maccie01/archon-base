# Middleware Stack Documentation

Created: 2025-10-13

## Overview

Middleware functions intercept and process HTTP requests before they reach route handlers. The Netzwächter backend uses Express middleware for authentication, error handling, rate limiting, and validation.

## Middleware Location

**Directory**: `/apps/backend-api/middleware/`

**Files**:
- `auth.ts` - Authentication and session management
- `error.ts` - Error handling and custom error classes
- `rate-limit.ts` - Rate limiting configurations
- `validate.ts` - Request validation using Zod schemas

## Global Middleware Order

Applied in `/apps/backend-api/index.ts`:

```
1. express.json() - Parse JSON bodies (10mb limit)
2. express.urlencoded() - Parse URL-encoded bodies (10mb limit)
3. apiRateLimiter - Rate limit all /api routes (300 req/min)
4. Request Logger - Log API requests with duration
5. Authentication Setup - Initialize session middleware
6. Session Timeout Checker - Validate session expiry
7. Route Handlers - Module-specific routes
8. 404 Handler - Catch unmatched /api/* routes
9. Error Handler - Global error handler (MUST BE LAST)
```

## 1. Authentication Middleware

**File**: `/apps/backend-api/middleware/auth.ts`

### Exported Functions

#### `initializeAuth(app: Express)`

Initializes authentication system for the Express app.

```typescript
export async function initializeAuth(app: Express) {
  console.log('Initializing authentication...');
  await setupAuth(app);  // Setup session-based auth
  app.use('/api', checkSessionTimeouts);  // Add timeout middleware
  console.log('Authentication initialized successfully');
}
```

**When called**: During app setup in `routes/index.ts`

#### `requireAuth(req, res, next)`

Middleware to protect routes requiring authentication.

```typescript
export function requireAuth(req: Request, res: Response, next: NextFunction) {
  originalIsAuthenticated(req, res, (err: any) => {
    if (err) {
      console.error('Authentication error:', err);
      return res.status(401).json({
        message: "Unauthorized",
        error: "Authentication failed"
      });
    }
    next();
  });
}
```

**Usage**:
```typescript
// In route files
import { requireAuth } from "../../middleware/auth";

router.use(requireAuth);  // Protect all routes in router
// OR
router.get("/protected", requireAuth, handler);  // Protect specific route
```

**Used in**: All authenticated module routes (settings, logbook, monitoring, etc.)

#### `validateSession(req, res, next)`

Validates session existence and expiry.

```typescript
export function validateSession(req: Request, res: Response, next: NextFunction) {
  const session = (req as any).session;

  if (!session) {
    return res.status(401).json({
      message: "No session found",
      error: "Session required"
    });
  }

  // Check session expiry
  if (session.user?.expires_at) {
    const now = Math.floor(Date.now() / 1000);
    if (session.user.expires_at < now) {
      return res.status(401).json({
        message: "Session expired",
        error: "Please login again"
      });
    }
  }

  next();
}
```

#### `requireRole(role: string)`

Creates middleware to enforce role-based access.

```typescript
export function requireRole(role: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    const user = (req as any).session?.user || (req as any).user;

    if (!user) {
      return res.status(401).json({
        message: "Unauthorized",
        error: "User not found"
      });
    }

    if (user.role !== role && user.role !== 'superadmin') {
      return res.status(403).json({
        message: "Forbidden",
        error: `Role '${role}' required`
      });
    }

    next();
  };
}
```

**Usage**:
```typescript
router.post("/admin-only", requireRole('admin'), handler);
```

#### `requireAdmin(req, res, next)`

Shorthand for admin role requirement.

```typescript
export function requireAdmin(req: Request, res: Response, next: NextFunction) {
  return requireRole('admin')(req, res, next);
}
```

#### `requireSuperAdmin(req, res, next)`

Shorthand for superadmin role requirement.

```typescript
export function requireSuperAdmin(req: Request, res: Response, next: NextFunction) {
  return requireRole('superadmin')(req, res, next);
}
```

### Session User Access Pattern

Controllers access the session user consistently:

```typescript
const sessionUser = (req as any).session?.user;

if (!sessionUser) {
  throw createAuthError("Benutzer nicht authentifiziert");
}

// Use sessionUser.id, sessionUser.role, sessionUser.mandantId, etc.
```

### Authentication Flow

```
1. User logs in → Auth controller creates session
2. Session stored in express-session
3. Subsequent requests include session cookie
4. requireAuth middleware validates session
5. Session user available in req.session.user
6. Controller checks permissions
7. Service/Repository execute with user context
```

## 2. Error Handling Middleware

**File**: `/apps/backend-api/middleware/error.ts`

### Custom Error Class

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

### Error Handler Middleware

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
    body: req.body,
    user: (req as any).session?.user?.id || 'anonymous'
  });

  // Build error response based on error type
  let errorResponse: ErrorResponse = {
    message: "Internal Server Error",
    status: 500
  };

  if (err instanceof AppError) {
    errorResponse = {
      message: err.message,
      status: err.statusCode,
      details: err.details
    };
  }
  // Handle specific error types (ValidationError, CastError, JWT errors, etc.)
  // ...

  res.status(errorResponse.status).json(errorResponse);
}
```

**Registered**: Last in middleware chain in `index.ts`

### 404 Handler

```typescript
export function notFoundHandler(req: Request, res: Response) {
  console.warn('Route not found:', {
    url: req.url,
    method: req.method,
    user: (req as any).session?.user?.id || 'anonymous'
  });

  res.status(404).json({
    message: "Route not found",
    error: `Cannot ${req.method} ${req.url}`,
    status: 404
  });
}
```

**Registered**: Before error handler for `/api/*` routes

### Async Handler Wrapper

```typescript
export function asyncHandler(fn: (req: Request, res: Response, next: NextFunction) => Promise<any>) {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}
```

**Usage**: Wrap all async route handlers
```typescript
router.get("/", asyncHandler(async (req, res) => {
  const data = await service.getData();
  res.json(data);
}));
```

### Error Creator Functions

#### `createValidationError(message: string, details?: any)`

Creates a 400 validation error.

```typescript
throw createValidationError("Name ist erforderlich");
throw createValidationError("Validation failed", { field: "name", message: "too short" });
```

#### `createAuthError(message: string)`

Creates a 401 authentication error.

```typescript
throw createAuthError("Benutzer nicht authentifiziert");
```

#### `createForbiddenError(message: string)`

Creates a 403 forbidden error.

```typescript
throw createForbiddenError("Keine Berechtigung");
```

#### `createNotFoundError(message: string)`

Creates a 404 not found error.

```typescript
throw createNotFoundError("Setting nicht gefunden");
```

#### `createDatabaseError(message: string, details?: any)`

Creates a 500 database error.

```typescript
throw createDatabaseError("Datenbankfehler");
```

### Error Handling Best Practices

**In Controllers**:
```typescript
export const controller = {
  handler: asyncHandler(async (req: Request, res: Response) => {
    const sessionUser = (req as any).session?.user;

    if (!sessionUser) {
      throw createAuthError("Benutzer nicht authentifiziert");
    }

    if (!req.params.id) {
      throw createValidationError("ID ist erforderlich");
    }

    const data = await service.getData(parseInt(req.params.id));

    if (!data) {
      throw createNotFoundError("Daten nicht gefunden");
    }

    res.json(data);
  })
};
```

**In Services**:
```typescript
private validateData(data: any): void {
  if (!data.name) {
    throw new Error('Name is required');
  }
}
```

**In Repositories**:
```typescript
async getData(id: number): Promise<Data | undefined> {
  try {
    const db = getDb();
    const [data] = await db.select().from(table).where(eq(table.id, id));
    return data;
  } catch (error) {
    console.error('Database error:', error);
    throw error;  // Let error handler deal with it
  }
}
```

## 3. Rate Limiting Middleware

**File**: `/apps/backend-api/middleware/rate-limit.ts`

### Rate Limiter Configurations

#### `apiRateLimiter`

General API rate limit applied to all `/api` routes.

**Config**:
- Window: 1 minute
- Max requests: 300 per window per IP
- Skip: `/api/health`, `/api/database/status`, `/api/public-*`

**Applied in**: `index.ts` with `app.use('/api', apiRateLimiter)`

```typescript
export const apiRateLimiter = rateLimit({
  windowMs: 1 * 60 * 1000,  // 1 minute
  max: 300,  // 300 requests per minute per IP
  message: {
    error: 'Too many requests from this IP. Please slow down.',
    code: 'API_RATE_LIMIT_EXCEEDED',
    retryAfter: '1 minute'
  },
  standardHeaders: true,
  legacyHeaders: false,
  skip: (req) => {
    const path = req.path || '';
    if (path === '/api/health' || path === '/api/database/status') return true;
    if (path.startsWith('/api/public-')) return true;
    return false;
  }
});
```

#### `authRateLimiter`

Strict rate limit for authentication endpoints.

**Config**:
- Window: 15 minutes
- Max requests: 5 failed attempts per window per IP
- Skip: Successful requests

**Usage**: Apply to login/logout routes

```typescript
export const authRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 5,  // 5 attempts per window per IP
  skipSuccessfulRequests: true,
  message: {
    error: 'Too many login attempts from this IP. Please try again in 15 minutes.',
    code: 'AUTH_RATE_LIMIT_EXCEEDED',
    retryAfter: '15 minutes'
  }
});
```

#### `exportRateLimiter`

Rate limit for data export endpoints.

**Config**:
- Window: 1 hour
- Max requests: 10 per window per IP

```typescript
export const exportRateLimiter = rateLimit({
  windowMs: 60 * 60 * 1000,  // 1 hour
  max: 10,  // 10 exports per hour per IP
  message: {
    error: 'Export rate limit exceeded. Please try again in 1 hour.',
    code: 'EXPORT_RATE_LIMIT_EXCEEDED',
    retryAfter: '1 hour'
  }
});
```

#### `passwordResetRateLimiter`

Very strict rate limit for password reset.

**Config**:
- Window: 1 hour
- Max requests: 3 per window per IP
- Skip: Successful requests

```typescript
export const passwordResetRateLimiter = rateLimit({
  windowMs: 60 * 60 * 1000,  // 1 hour
  max: 3,  // 3 attempts per hour per IP
  skipSuccessfulRequests: true,
  message: {
    error: 'Too many password reset requests. Please try again in 1 hour.',
    code: 'PASSWORD_RESET_RATE_LIMIT_EXCEEDED',
    retryAfter: '1 hour'
  }
});
```

#### `registrationRateLimiter`

Rate limit for user registration.

**Config**:
- Window: 1 hour
- Max requests: 5 per window per IP

```typescript
export const registrationRateLimiter = rateLimit({
  windowMs: 60 * 60 * 1000,  // 1 hour
  max: 5,  // 5 registrations per hour per IP
  message: {
    error: 'Too many registration attempts. Please try again in 1 hour.',
    code: 'REGISTRATION_RATE_LIMIT_EXCEEDED',
    retryAfter: '1 hour'
  }
});
```

### Rate Limit Response

When rate limit is exceeded:

**Status Code**: 429 (Too Many Requests)

**Headers**:
- `RateLimit-Limit`: Total requests allowed
- `RateLimit-Remaining`: Remaining requests
- `RateLimit-Reset`: Time when limit resets

**Body**:
```json
{
  "error": "Too many requests from this IP. Please slow down.",
  "code": "API_RATE_LIMIT_EXCEEDED",
  "retryAfter": "1 minute"
}
```

### Usage in Routes

Most routes use the global `apiRateLimiter`. Specific routes can override:

```typescript
// Use specific rate limiter
router.post("/login", authRateLimiter, loginHandler);
router.post("/reset-password", passwordResetRateLimiter, resetHandler);
router.post("/export", exportRateLimiter, exportHandler);
```

## 4. Validation Middleware

**File**: `/apps/backend-api/middleware/validate.ts`

### Validation Functions

#### `validate(schema: ZodSchema, source: "body" | "query" | "params")`

Generic validation function.

```typescript
export function validate(schema: ZodSchema, source: "body" | "query" | "params" = "body") {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      const dataToValidate = req[source];

      // Validate and parse
      const validatedData = await schema.parseAsync(dataToValidate);

      // Replace request data with validated data
      req[source] = validatedData;

      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        // Format Zod validation errors
        const formattedErrors = error.errors.map((err) => ({
          field: err.path.join("."),
          message: err.message
        }));

        const validationError = createValidationError(
          `Validierungsfehler: ${formattedErrors.map(e => `${e.field}: ${e.message}`).join(", ")}`,
          formattedErrors
        );

        return next(validationError);
      }
      next(error);
    }
  };
}
```

#### `validateBody(schema: ZodSchema)`

Shorthand for body validation.

```typescript
export function validateBody(schema: ZodSchema) {
  return validate(schema, "body");
}
```

#### `validateQuery(schema: ZodSchema)`

Shorthand for query parameter validation.

```typescript
export function validateQuery(schema: ZodSchema) {
  return validate(schema, "query");
}
```

#### `validateParams(schema: ZodSchema)`

Shorthand for URL parameter validation.

```typescript
export function validateParams(schema: ZodSchema) {
  return validate(schema, "params");
}
```

### Usage in Routes

**Define Zod schema**:
```typescript
import { z } from "zod";

const createSettingSchema = z.object({
  category: z.string().min(1).max(100),
  key_name: z.string().min(1).max(255),
  value: z.any(),
  user_id: z.string().optional(),
  mandant_id: z.number().int().positive().optional()
});
```

**Apply to route**:
```typescript
import { validateBody } from "../../middleware/validate";

router.post(
  "/",
  validateBody(createSettingSchema),
  settingsController.createSettingHandler
);
```

**Currently not widely used** - Most modules validate in service layer instead.

### Validation Error Response

**Status Code**: 400

**Body**:
```json
{
  "message": "Validierungsfehler: category: Required, key_name: String must contain at least 1 character(s)",
  "status": 400,
  "details": [
    { "field": "category", "message": "Required" },
    { "field": "key_name", "message": "String must contain at least 1 character(s)" }
  ]
}
```

## Custom Middleware in Modules

Some modules have module-specific middleware in their route files:

### Example: Energy Routes

```typescript
// Public routes (no auth)
router.get("/public-daily-consumption/:objectId", energyController.getPublicDailyConsumption);
router.get("/public-monthly-consumption/:objectId", energyController.getPublicMonthlyConsumption);
router.get("/monthly-netz/:objectId", energyController.getMonthlyNetz);

// Protected routes (auth required)
router.use(requireAuth);

router.get("/day-comp/:objectId", energyController.getDayCompDataHandler);
router.post("/day-comp", energyController.createDayCompDataHandler);
// ... more protected routes
```

## Middleware Best Practices

### DO:
1. ✅ Apply `requireAuth` to all authenticated routes
2. ✅ Wrap async handlers with `asyncHandler()`
3. ✅ Use error creator functions (`createAuthError`, etc.)
4. ✅ Apply rate limiting to public endpoints
5. ✅ Validate input with Zod schemas (when practical)
6. ✅ Log errors with context
7. ✅ Return consistent error format

### DON'T:
1. ❌ Skip authentication for sensitive routes
2. ❌ Forget to call `next()` in middleware
3. ❌ Block event loop in middleware (use async/await)
4. ❌ Leak sensitive info in error messages (production)
5. ❌ Apply rate limiting too strictly (breaks UX)
6. ❌ Validate in both middleware AND service (choose one)
7. ❌ Register error handler before route handlers

## Middleware Execution Order Example

Request: `POST /api/settings`

```
1. express.json() → Parse JSON body
2. apiRateLimiter → Check rate limit (300/min)
3. Request Logger → Log request start
4. checkSessionTimeouts → Validate session expiry
5. settingsRoutes → Match route
6. requireAuth → Check authentication
7. asyncHandler → Wrap controller
8. settingsController.createSettingHandler → Execute handler
   ↓ (if error thrown)
9. errorHandler → Format and send error
   ↓ (if success)
10. Request Logger → Log request complete with duration
```

## Conclusion

The Netzwächter backend uses a comprehensive middleware stack for authentication, error handling, rate limiting, and validation. The middleware is well-organized and follows Express best practices. Authentication is consistently applied via `requireAuth`, errors are handled uniformly via `asyncHandler` and custom error creators, and rate limiting protects against abuse.

**Key recommendations**:
1. Continue using `asyncHandler()` for all async route handlers
2. Consistently use error creator functions for better error handling
3. Consider expanding Zod validation usage for complex input validation
4. Maintain current rate limiting configuration
5. Keep error handler as the last middleware
