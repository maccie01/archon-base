# Netzwächter Backend Patterns Analysis

Created: 2025-10-13
Project: Netzwächter Monitoring System

## Overview

Analysis of backend patterns used in the Netzwächter project - a production monitoring system built with Node.js, Express, TypeScript, and PostgreSQL.

## Architecture Pattern Used

### Three-Layer Architecture (Controller-Service-Repository)

The Netzwächter project implements a clean three-layer architecture:

```
modules/
├── auth/
│   ├── auth.controller.ts      # HTTP request handling
│   ├── auth.service.ts         # Business logic
│   ├── auth.repository.ts      # Data access
│   ├── auth.routes.ts          # Route definitions
│   ├── auth.types.ts           # TypeScript interfaces
│   ├── auth.middleware.ts      # Module-specific middleware
│   └── __tests__/              # Unit tests
```

**Why this works well:**
- Clear separation of concerns
- Easy to test each layer independently
- Business logic is isolated from HTTP and database
- Feature-based modules (not layer-based)

## Key Patterns Observed

### 1. Controller Pattern

Location: `/apps/backend-api/modules/auth/auth.controller.ts`

**Pattern:**
```typescript
export const authController = {
  login: asyncHandler(async (req: Request, res: Response) => {
    const { username, password } = req.body;
    
    if (!username || !password) {
      throw createValidationError('Username and password required');
    }
    
    const user = await authService.validateCredentials({ username, password });
    
    if (!user.isValid) {
      throw createAuthError('Invalid credentials');
    }
    
    req.session.user = authService.createUserSession(user);
    
    res.json({ message: 'Login successful', user });
  }),
};
```

**Strengths:**
- Uses asyncHandler for error catching
- Thin controllers - delegates to service
- Clear input validation
- Proper error handling with custom errors
- JSDoc comments document API endpoints

### 2. Service Pattern

Location: `/apps/backend-api/modules/auth/auth.service.ts`

**Pattern:**
```typescript
export class AuthService {
  async validateUserCredentials(username: string, password: string): Promise<User | null> {
    const user = await authRepository.findUserByUsernameOrEmail(username);
    
    if (!user || !user.password) {
      // Timing attack prevention
      await bcrypt.compare(password, '$2b$12$dummy');
      return null;
    }
    
    const isValid = await bcrypt.compare(password, user.password);
    return isValid ? user : null;
  }

  createUserSession(user: User): SessionUser {
    return {
      id: user.id,
      email: user.email,
      role: user.role,
      sessionStart: Date.now(),
      lastActivity: Date.now(),
    };
  }
}

export const authService = new AuthService();
```

**Strengths:**
- Contains all business logic
- Singleton pattern for service instance
- Security best practices (timing attack prevention)
- Framework-independent (no HTTP concepts)
- Returns domain objects

### 3. Error Handling Pattern

Location: `/apps/backend-api/middleware/error.ts`

**Pattern:**
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

export function errorHandler(err: Error | AppError, req, res, next) {
  console.error('Error occurred:', { message, stack, url, method });
  
  let errorResponse = { message: "Internal Server Error", status: 500 };
  
  if (err instanceof AppError) {
    errorResponse = {
      message: err.message,
      status: err.statusCode,
      details: err.details
    };
  }
  
  res.status(errorResponse.status).json(errorResponse);
}

export function asyncHandler(fn: Function) {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}
```

**Strengths:**
- Custom error class with status codes
- Centralized error handling
- asyncHandler prevents unhandled promise rejections
- Factory functions for common errors
- Hides stack traces from clients

### 4. Middleware Pattern

Location: `/apps/backend-api/middleware/auth.ts`

**Pattern:**
```typescript
export function requireAuth(req, res, next) {
  originalIsAuthenticated(req, res, (err) => {
    if (err) {
      return res.status(401).json({ 
        message: "Unauthorized",
        error: "Authentication failed" 
      });
    }
    next();
  });
}

export function requireRole(role: string) {
  return (req, res, next) => {
    const user = req.session?.user;
    
    if (!user) {
      return res.status(401).json({ message: "Unauthorized" });
    }
    
    if (user.role !== role && user.role !== 'superadmin') {
      return res.status(403).json({ message: "Forbidden" });
    }
    
    next();
  };
}
```

**Strengths:**
- Reusable middleware functions
- Proper error responses
- Role-based access control
- Composable (can chain multiple)

### 5. Validation Pattern

Location: `/apps/backend-api/middleware/validate.ts`

**Pattern:**
```typescript
export function validate(schema: ZodSchema, source = "body") {
  return async (req, res, next) => {
    try {
      const validatedData = await schema.parseAsync(req[source]);
      req[source] = validatedData;
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        const formattedErrors = error.errors.map((err) => ({
          field: err.path.join("."),
          message: err.message,
        }));
        return next(createValidationError('Validation error', formattedErrors));
      }
      next(error);
    }
  };
}
```

**Strengths:**
- Uses Zod for type-safe validation
- Validates body, query, or params
- Clear error messages
- Type inference from schemas

### 6. Connection Pool Pattern

Location: `/apps/backend-api/connection-pool.ts`

**Pattern:**
```typescript
export class ConnectionPoolManager {
  private pool: PgPool;
  
  async initialize() {
    this.pool = new PgPool({
      connectionString: process.env.DATABASE_URL,
      min: 5,
      max: 20,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 5000,
      keepAlive: true,
    });
    
    this.pool.on('error', (err) => {
      console.error('Pool error:', err);
      this.totalErrors++;
    });
    
    await this.prewarmConnections(5);
  }
  
  async query(text: string, params?: any[]) {
    const client = await this.pool.connect();
    try {
      const result = await client.query(text, params);
      return result.rows;
    } finally {
      client.release();
    }
  }
  
  async shutdown() {
    await this.pool.end();
  }
}
```

**Strengths:**
- Singleton pattern for pool
- Health monitoring and metrics
- Circuit breaker for failure handling
- Graceful shutdown
- Pre-warming connections
- Optimized pool size (5-20 connections)

### 7. Route Organization

Location: `/apps/backend-api/routes/index.ts`

**Pattern:**
```typescript
export async function setupRoutes(app: Express) {
  await initializeAuth(app);
  
  // Public routes first
  app.use('/api/outdoor-temperatures', weatherRoutes);
  
  // Protected module routes (alphabetically)
  app.use('/api/admin', adminRoutes);
  app.use('/api/auth', authRoutes);
  app.use('/api/users', usersRoutes);
  // ... more routes
  
  // 404 handler
  app.use('/api/*', notFoundHandler);
  
  // Error handler (must be last)
  app.use(errorHandler);
}
```

**Strengths:**
- Centralized route registration
- Clear ordering (public first, then protected)
- Alphabetical organization for maintainability
- 404 and error handlers at the end

## What Works Well

### 1. Clear Separation of Concerns
Every layer has a single responsibility, making code easy to understand and maintain.

### 2. Type Safety
TypeScript is used throughout with strict types, preventing many runtime errors.

### 3. Security Practices
- Bcrypt password hashing
- Timing attack prevention
- Session-based authentication
- Input validation with Zod
- Custom error handling

### 4. Testability
Each layer can be tested independently with proper mocks:
- Controllers tested with request/response mocks
- Services tested with repository mocks
- Repositories tested with real database

### 5. Error Handling
- Custom error classes
- Centralized error middleware
- asyncHandler wrapper
- Consistent error responses

### 6. Feature-Based Organization
Modules are organized by feature/domain, not by technical layer, making it easy to find related code.

## Areas for Improvement

### 1. Dependency Injection
Currently uses singleton pattern. Could benefit from proper DI for better testability:

```typescript
// Current (singleton)
export const authService = new AuthService();

// Better (DI)
export class AuthService {
  constructor(
    private authRepository: AuthRepository,
    private emailService: EmailService
  ) {}
}
```

### 2. Repository Transaction Support
Some repositories could better support transactions:

```typescript
// Add optional client parameter
async create(data: CreateUserData, client?: PoolClient): Promise<User> {
  const db = client || this.pool;
  // ... query using db
}
```

### 3. API Documentation
Could add OpenAPI/Swagger documentation for better API discoverability.

### 4. More Comprehensive Testing
While tests exist, could benefit from:
- Higher test coverage
- More integration tests
- E2E tests for critical flows

## Recommended Patterns for New Projects

Based on Netzwächter analysis:

1. **Use Three-Layer Architecture**: Controller-Service-Repository
2. **Feature-Based Modules**: Organize by domain, not layer
3. **Custom Error Classes**: With status codes
4. **asyncHandler**: For all async routes
5. **Zod Validation**: Type-safe input validation
6. **Connection Pooling**: Optimized pool size
7. **Middleware Composition**: Reusable, composable middleware
8. **TypeScript Strict Mode**: Catch errors at compile time
9. **Session-Based Auth**: For server-side rendered or traditional apps
10. **Structured Logging**: JSON logs with context

## Resources

- Full patterns documented in this directory
- Netzwächter project: `/Users/janschubert/code-projects/monitoring_firma/netzwaechter-refactored`
- See individual pattern files for detailed examples

## Conclusion

Netzwächter demonstrates a well-architected Node.js backend with:
- Clear layered architecture
- Strong type safety
- Good security practices
- Testable code structure
- Production-ready patterns

These patterns are suitable for any medium to large Node.js backend project.
