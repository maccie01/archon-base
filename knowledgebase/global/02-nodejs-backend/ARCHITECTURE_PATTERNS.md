# Architecture Patterns for Node.js Backend

Created: 2025-10-13
Last Updated: 2025-10-13
Research Sources: Clean Architecture, Domain-Driven Design, Node.js best practices

## Overview

Backend architecture defines how code is organized and how different layers interact. A well-designed architecture promotes maintainability, testability, and scalability.

## Core Principles

1. **Separation of Concerns**: Each layer has a single responsibility
2. **Dependency Rule**: Dependencies point inward (from outer to inner layers)
3. **Testability**: Business logic should be independent of frameworks
4. **Flexibility**: Easy to swap implementations (database, external services)
5. **Maintainability**: Code organization aids understanding and modification

## Layered Architecture (Recommended)

The three-layer pattern used in production applications like Netzwächter.

### Controller-Service-Repository Pattern

```
┌───────────────────────────────────────────────┐
│      HTTP Layer (Express)                     │
│                                                │
│  ┌──────────────────────────────────────┐    │
│  │   Controllers                         │    │  Request/Response handling
│  └──────────────┬───────────────────────┘    │  Input validation
│                 │                              │  HTTP status codes
└─────────────────┼──────────────────────────────┘
                  │
┌─────────────────┼──────────────────────────────┐
│  ┌──────────────▼───────────────────────┐    │
│  │   Services                            │    │  Business logic
│  └──────────────┬───────────────────────┘    │  Orchestration
│                 │                              │  Transaction management
└─────────────────┼──────────────────────────────┘
                  │
┌─────────────────┼──────────────────────────────┐
│  ┌──────────────▼───────────────────────┐    │
│  │   Repositories                        │    │  Data access
│  └──────────────┬───────────────────────┘    │  Query building
│                 │                              │  Database interaction
└─────────────────┼──────────────────────────────┘
                  │
┌─────────────────▼──────────────────────────────┐
│         Database                                │
└─────────────────────────────────────────────────┘
```

### Layer Responsibilities

#### Controller Layer
- **Purpose**: HTTP request/response handling
- **Responsibilities**:
  - Parse and validate request parameters
  - Call appropriate service methods
  - Format responses
  - Set HTTP status codes
  - Handle HTTP-specific concerns
- **Should NOT**: Contain business logic, database queries

#### Service Layer
- **Purpose**: Business logic and orchestration
- **Responsibilities**:
  - Implement business rules
  - Coordinate between multiple repositories
  - Handle transactions
  - Perform calculations and transformations
  - Validate business rules
- **Should NOT**: Know about HTTP, access database directly

#### Repository Layer
- **Purpose**: Data access abstraction
- **Responsibilities**:
  - Execute database queries
  - Map database results to domain models
  - Handle database-specific logic
  - Provide clean data access interface
- **Should NOT**: Contain business logic, know about HTTP

## Module Organization

### Feature-Based Modules

Organize by feature/domain, not by technical layer:

```
modules/
├── auth/
│   ├── auth.controller.ts      # HTTP handlers
│   ├── auth.service.ts         # Business logic
│   ├── auth.repository.ts      # Data access
│   ├── auth.routes.ts          # Route definitions
│   ├── auth.types.ts           # TypeScript types
│   ├── auth.middleware.ts      # Module-specific middleware
│   └── __tests__/              # Module tests
│       ├── auth.controller.test.ts
│       ├── auth.service.test.ts
│       └── auth.repository.test.ts
├── users/
│   ├── users.controller.ts
│   ├── users.service.ts
│   ├── users.repository.ts
│   ├── users.routes.ts
│   ├── users.types.ts
│   └── __tests__/
└── posts/
    ├── posts.controller.ts
    ├── posts.service.ts
    ├── posts.repository.ts
    ├── posts.routes.ts
    └── posts.types.ts
```

See full file content in repository at: /Users/janschubert/code-projects/.global-shared-knowledge/02-nodejs-backend/ARCHITECTURE_PATTERNS.md
