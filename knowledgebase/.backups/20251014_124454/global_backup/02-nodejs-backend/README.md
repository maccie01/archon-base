# Node.js Backend Best Practices

Created: 2025-10-13
Last Updated: 2025-10-13

## Overview

This directory contains comprehensive best practices and patterns for building production-ready Node.js/Express backend applications. These guidelines are derived from industry standards, modern 2024/2025 practices, and battle-tested patterns from real-world projects.

## Navigation Guide

### Core Architecture
- [Express Best Practices](./EXPRESS_BEST_PRACTICES.md) - General Express.js patterns and setup
- [Architecture Patterns](./ARCHITECTURE_PATTERNS.md) - Layered architecture, MVC, clean architecture
- [API Design](./API_DESIGN.md) - RESTful API principles, versioning, endpoints

### Layer-Specific Patterns
- [Controller Layer](./CONTROLLER_LAYER.md) - HTTP request/response handling
- [Service Layer](./SERVICE_LAYER.md) - Business logic and orchestration
- [Repository Layer](./REPOSITORY_LAYER.md) - Data access patterns

### Cross-Cutting Concerns
- [Middleware Patterns](./MIDDLEWARE_PATTERNS.md) - Auth, validation, logging, error handling
- [Error Handling](./ERROR_HANDLING.md) - Custom errors, error middleware, status codes
- [Validation](./VALIDATION.md) - Zod, Joi, express-validator patterns
- [Authentication](./AUTHENTICATION.md) - JWT, sessions, cookies, OAuth
- [Authorization](./AUTHORIZATION.md) - RBAC, permissions, middleware
- [Security](./SECURITY.md) - CORS, CSRF, injection prevention, rate limiting

### Technical Implementation
- [Database Patterns](./DATABASE_PATTERNS.md) - Connection pooling, transactions, queries
- [Async Patterns](./ASYNC_PATTERNS.md) - Async/await, error handling, promises
- [TypeScript Backend](./TYPESCRIPT_BACKEND.md) - Typing Express, middleware, routes
- [Testing Backend](./TESTING_BACKEND.md) - Unit tests, integration tests, E2E
- [Logging and Monitoring](./LOGGING_MONITORING.md) - Structured logging, health checks

### Reference
- [Antipatterns](./ANTIPATTERNS.md) - Common mistakes and what to avoid

## Key Principles

### 1. Separation of Concerns
- Controllers handle HTTP layer only
- Services contain business logic
- Repositories handle data access
- Middleware handles cross-cutting concerns

### 2. Type Safety
- Use TypeScript for all backend code
- Define strict types for requests, responses, and data models
- Leverage shared types across layers

### 3. Error Handling
- Use custom error classes
- Implement centralized error middleware
- Always use asyncHandler for async routes
- Return consistent error responses

### 4. Security First
- Validate all inputs
- Implement authentication and authorization
- Use rate limiting
- Protect against common vulnerabilities (SQL injection, XSS, CSRF)

### 5. Testability
- Write unit tests for services
- Write integration tests for APIs
- Mock external dependencies
- Aim for high test coverage

### 6. Performance
- Use connection pooling for databases
- Implement caching where appropriate
- Monitor and optimize slow queries
- Use async/await correctly

### 7. Maintainability
- Follow consistent naming conventions
- Document complex business logic
- Keep functions small and focused
- Use dependency injection

## Quick Start Patterns

### Controller Pattern
```typescript
// TODO: See CONTROLLER_LAYER.md for full examples
export const userController = {
  getUser: asyncHandler(async (req, res) => {
    const user = await userService.getUser(req.params.id);
    res.json(user);
  })
};
```

### Service Pattern
```typescript
// TODO: See SERVICE_LAYER.md for full examples
export class UserService {
  async getUser(id: string): Promise<User> {
    return await userRepository.findById(id);
  }
}
```

### Error Handling Pattern
```typescript
// TODO: See ERROR_HANDLING.md for full examples
export class AppError extends Error {
  constructor(message: string, statusCode: number) {
    super(message);
    this.statusCode = statusCode;
  }
}
```

## Technology Stack

### Core
- Node.js 18+
- Express.js 4.x
- TypeScript 5.x

### Database
- PostgreSQL with pg driver
- Connection pooling
- Query builders or ORMs (Drizzle, Prisma, etc.)

### Validation
- Zod (recommended for TypeScript)
- Joi (alternative)
- express-validator (traditional)

### Authentication
- express-session (session-based)
- jsonwebtoken (JWT-based)
- Passport.js (OAuth)

### Testing
- Vitest (modern, fast)
- Jest (traditional)
- Supertest (API testing)

### Logging
- Winston (structured logging)
- Morgan (HTTP request logging)
- Pino (high-performance alternative)

## Project Structure Example

```
apps/backend-api/
├── modules/
│   ├── auth/
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── auth.repository.ts
│   │   ├── auth.routes.ts
│   │   ├── auth.types.ts
│   │   └── __tests__/
│   ├── users/
│   │   ├── users.controller.ts
│   │   ├── users.service.ts
│   │   ├── users.repository.ts
│   │   ├── users.routes.ts
│   │   └── users.types.ts
│   └── ...
├── middleware/
│   ├── auth.ts
│   ├── error.ts
│   ├── validate.ts
│   └── rate-limit.ts
├── routes/
│   └── index.ts
├── config/
│   ├── database.ts
│   └── env.ts
└── index.ts
```

## Resources

### Official Documentation
- [Express.js Documentation](https://expressjs.com/)
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

### Further Reading
- Each topic file contains specific resources and references
- Check ANTIPATTERNS.md for common mistakes to avoid
- Review real-world examples in the Netzwächter project

## Contributing

When adding new patterns or updating existing ones:
1. Include practical code examples
2. Document when to use (and when NOT to use) each pattern
3. Add references to official documentation
4. Update the last modified date
5. Keep examples focused and minimal

## Research Sources

This documentation is based on:
- Express.js 4.x official documentation
- Node.js best practices repository (2024)
- TypeScript 5.x handbook
- Real-world production patterns from Netzwächter project
- Industry standards and security guidelines (OWASP)
- Modern JavaScript/TypeScript practices (2024/2025)
