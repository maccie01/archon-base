# Backend Module Pattern Standard

Created: 2025-10-13

## Standard Module Pattern

The ideal module structure follows a layered architecture with clear separation of concerns.

## Complete Module Structure

```
modules/[module-name]/
├── __tests__/
│   ├── [module].controller.test.ts
│   ├── [module].service.test.ts
│   └── [module].repository.test.ts
├── dto/                              # Optional: Data Transfer Objects
│   ├── create-[entity].dto.ts
│   └── update-[entity].dto.ts
├── index.ts                          # Module exports
├── [module].controller.ts            # HTTP layer
├── [module].service.ts               # Business logic layer
├── [module].repository.ts            # Data access layer
├── [module].routes.ts                # Route definitions
└── [module].types.ts                 # TypeScript types/interfaces
```

## Layer Responsibilities

### 1. Routes Layer (`*.routes.ts`)

**Purpose**: Define HTTP endpoints and apply middleware

**Responsibilities**:
- Mount Express routes
- Apply authentication middleware
- Apply validation middleware
- Map routes to controller methods
- Apply rate limiting (if needed)

**Pattern**:
```typescript
import { Router } from "express";
import { [module]Controller } from "./[module].controller";
import { requireAuth } from "../../middleware/auth";

const router = Router();

// Apply auth middleware to all routes (if needed)
router.use(requireAuth);

// Define routes
router.get("/", [module]Controller.getAll);
router.get("/:id", [module]Controller.getById);
router.post("/", [module]Controller.create);
router.put("/:id", [module]Controller.update);
router.delete("/:id", [module]Controller.delete);

export default router;
```

**Key Rules**:
- NO business logic
- NO database queries
- NO error handling (delegated to controller)
- Export as default
- Document each route with JSDoc comments

### 2. Controller Layer (`*.controller.ts`)

**Purpose**: Handle HTTP request/response cycle

**Responsibilities**:
- Extract parameters from request (params, query, body)
- Validate session/authentication
- Call service layer methods
- Format response data
- Handle HTTP status codes
- Wrap handlers with `asyncHandler()`

**Pattern**:
```typescript
import type { Request, Response } from "express";
import { [module]Service } from "./[module].service";
import {
  asyncHandler,
  createAuthError,
  createValidationError,
  createNotFoundError
} from "../../middleware/error";

export const [module]Controller = {
  /**
   * API: GET /api/[module]
   * Get all [entities]
   * Auth: Requires authentication
   * Returns: Array of [Entity] records
   */
  getAll: asyncHandler(async (req: Request, res: Response) => {
    const sessionUser = (req as any).session?.user;

    if (!sessionUser) {
      throw createAuthError("Benutzer nicht authentifiziert");
    }

    const data = await [module]Service.getAll();
    res.json(data);
  }),

  // More handlers...
};
```

**Key Rules**:
- NO direct database access
- NO business logic (delegate to service)
- Always wrap with `asyncHandler()`
- Use error creator functions from middleware
- Extract session user consistently
- Include JSDoc with API route, auth requirements, return type
- Export as object with named methods

### 3. Service Layer (`*.service.ts`)

**Purpose**: Implement business logic and validation

**Responsibilities**:
- Validate business rules
- Coordinate between multiple repositories
- Transform data
- Implement business calculations
- Handle complex workflows
- Validate input data

**Pattern**:
```typescript
import { [module]Repository } from "./[module].repository";
import type { [Entity], Insert[Entity] } from "@shared/schema";

export class [Module]Service {
  /**
   * Get all [entities] with validation
   * @returns Array of [Entity] records
   */
  async getAll(): Promise<[Entity][]> {
    return await [module]Repository.getAll();
  }

  /**
   * Create [entity] with validation
   * @param data - Entity data to create
   * @returns Created [Entity] record
   */
  async create(data: Insert[Entity]): Promise<[Entity]> {
    // Business validation
    this.validateEntityData(data);

    return await [module]Repository.create(data);
  }

  // Private validation methods
  private validateEntityData(data: Insert[Entity]): void {
    if (!data.name) {
      throw new Error('Name is required');
    }
    // More validation...
  }
}

// Singleton instance
export const [module]Service = new [Module]Service();
```

**Key Rules**:
- NO HTTP-specific code (no req/res)
- NO direct database queries (delegate to repository)
- Validate all input data
- Use private methods for validation
- Export as singleton instance
- Use class pattern for better testing
- Include JSDoc for all public methods

### 4. Repository Layer (`*.repository.ts`)

**Purpose**: Handle database operations

**Responsibilities**:
- Execute SQL queries
- Transform database results
- Handle database errors
- Manage transactions (if needed)
- Use Drizzle ORM OR ConnectionPoolManager

**Pattern (Drizzle ORM - Preferred)**:
```typescript
import { getDb } from "../../db";
import { [entities] } from "@shared/schema";
import { eq, and, desc } from "drizzle-orm";
import type { [Entity], Insert[Entity] } from "@shared/schema";

export class [Module]Repository {
  /**
   * Get all [entities]
   * @returns Array of [Entity] records
   */
  async getAll(): Promise<[Entity][]> {
    try {
      const db = getDb();
      return await db
        .select()
        .from([entities])
        .orderBy(desc([entities].createdAt));
    } catch (error) {
      console.error('Error fetching [entities]:', error);
      throw error;
    }
  }

  /**
   * Create [entity]
   * @param data - Entity data to insert
   * @returns Created [Entity] record
   */
  async create(data: Insert[Entity]): Promise<[Entity]> {
    try {
      const db = getDb();
      const [newEntity] = await db
        .insert([entities])
        .values(data)
        .returning();
      return newEntity;
    } catch (error) {
      console.error('Error creating [entity]:', error);
      throw error;
    }
  }
}

// Singleton instance
export const [module]Repository = new [Module]Repository();
```

**Pattern (ConnectionPoolManager - Legacy)**:
```typescript
import { ConnectionPoolManager } from "../../connection-pool";
import type { [Entity], Insert[Entity] } from "@shared/schema";

export class [Module]Repository {
  async getAll(): Promise<[Entity][]> {
    try {
      const pool = ConnectionPoolManager.getInstance().getPool();
      const result = await pool.query('SELECT * FROM [entities] ORDER BY created_at DESC');
      return result.rows;
    } catch (error) {
      console.error('Error fetching [entities]:', error);
      throw error;
    }
  }

  async create(data: Insert[Entity]): Promise<[Entity]> {
    try {
      const pool = ConnectionPoolManager.getInstance().getPool();
      const result = await pool.query(
        'INSERT INTO [entities] (name, ...) VALUES ($1, ...) RETURNING *',
        [data.name, ...]
      );
      return result.rows[0];
    } catch (error) {
      console.error('Error creating [entity]:', error);
      throw error;
    }
  }
}

export const [module]Repository = new [Module]Repository();
```

**Key Rules**:
- NO business logic
- NO HTTP-specific code
- Use try-catch for all queries
- Log all errors with context
- Use parameterized queries to prevent SQL injection
- Prefer Drizzle ORM for new code
- Export as singleton instance
- Include JSDoc for all public methods

### 5. Types Layer (`*.types.ts`)

**Purpose**: Define TypeScript types and interfaces

**Responsibilities**:
- Define request/response types
- Define filter/query types
- Define DTOs
- Re-export shared types

**Pattern**:
```typescript
import type { [Entity] } from "@shared/schema";

// Filters for queries
export interface [Entity]Filters {
  name?: string;
  status?: string;
  createdAfter?: Date;
}

// Response types (if different from entity)
export interface [Entity]Response extends [Entity] {
  computedField: string;
}

// DTO types (if not using separate dto folder)
export interface Create[Entity]DTO {
  name: string;
  description?: string;
}
```

### 6. Index Export (`index.ts`)

**Purpose**: Provide clean module exports

**Pattern**:
```typescript
export { [module]Controller } from './[module].controller';
export { [module]Service } from './[module].service';
export { [module]Repository } from './[module].repository';
export type { [Entity]Filters, [Entity]Response } from './[module].types';
export { default as [module]Routes } from './[module].routes';
```

## Data Flow

```
HTTP Request
    ↓
Routes (middleware, routing)
    ↓
Controller (HTTP handling, session validation)
    ↓
Service (business logic, validation)
    ↓
Repository (database operations)
    ↓
Database
```

## Complete Example: Settings Module

This is the reference implementation that all modules should follow.

### File: settings.routes.ts
```typescript
import { Router } from "express";
import { settingsController } from "./settings.controller";
import { requireAuth } from "../../middleware/auth";

const router = Router();

// All settings routes require authentication
router.use(requireAuth);

router.get("/", settingsController.getSettingsHandler);
router.get("/by-key", settingsController.getSettingHandler);
router.get("/:id", settingsController.getSettingByIdHandler);
router.post("/", settingsController.createSettingHandler);
router.put("/:id", settingsController.updateSettingHandler);
router.delete("/:id", settingsController.deleteSettingHandler);

export default router;
```

### File: settings.controller.ts
```typescript
import type { Request, Response } from "express";
import { settingsService } from "./settings.service";
import { asyncHandler, createAuthError, createValidationError } from "../../middleware/error";
import type { InsertSettings } from "@shared/schema";

export const settingsController = {
  getSettingsHandler: asyncHandler(async (req: Request, res: Response) => {
    const sessionUser = (req as any).session?.user;
    if (!sessionUser) {
      throw createAuthError("Benutzer nicht authentifiziert");
    }

    const { category, userId, mandantId } = req.query;
    const filters: any = {};
    if (category) filters.category = category as string;
    if (userId) filters.user_id = userId as string;
    if (mandantId) filters.mandant_id = parseInt(mandantId as string);

    const data = await settingsService.getSettings(filters);
    res.json(data);
  }),
  // More handlers...
};
```

### File: settings.service.ts
```typescript
import { settingsRepository } from "./settings.repository";
import type { Settings, InsertSettings } from "@shared/schema";

export class SettingsService {
  async getSettings(filters?: { category?: string; user_id?: string; mandant_id?: number; }): Promise<Settings[]> {
    // Validate filters
    if (filters?.category) {
      this.validateSettingCategory(filters.category);
    }
    return await settingsRepository.getSettings(filters);
  }

  async createSetting(settingData: InsertSettings): Promise<Settings> {
    this.validateSettingData(settingData);
    return await settingsRepository.createSetting(settingData);
  }

  private validateSettingCategory(category: string): void {
    if (!category || typeof category !== 'string') {
      throw new Error('Category is required and must be a string');
    }
    // More validation...
  }

  private validateSettingData(settingData: InsertSettings): void {
    if (!settingData.category) throw new Error('Category is required');
    if (!settingData.key_name) throw new Error('Key name is required');
    // More validation...
  }
}

export const settingsService = new SettingsService();
```

### File: settings.repository.ts
```typescript
import { ConnectionPoolManager } from "../../connection-pool";
import type { Settings, InsertSettings } from "@shared/schema";

export class SettingsRepository {
  async getSettings(filters?: { category?: string; user_id?: string; mandant_id?: number; }): Promise<Settings[]> {
    try {
      const pool = await ConnectionPoolManager.getInstance().getPool();
      let query = `SELECT * FROM settings WHERE 1=1`;
      const params: any[] = [];
      let paramIndex = 1;

      if (filters?.category) {
        query += ` AND category = $${paramIndex++}`;
        params.push(filters.category);
      }
      // More filters...

      const result = await pool.query(query, params);
      return result.rows;
    } catch (error) {
      console.error('Error fetching settings:', error);
      return [];
    }
  }

  async createSetting(settingData: InsertSettings): Promise<Settings> {
    try {
      const pool = ConnectionPoolManager.getInstance().getPool();
      const result = await pool.query(
        `INSERT INTO settings (category, key_name, value, user_id, mandant_id, created_at, updated_at)
         VALUES ($1, $2, $3, $4, $5, NOW(), NOW()) RETURNING *`,
        [settingData.category, settingData.key_name, settingData.value, settingData.user_id || null, settingData.mandant_id || null]
      );
      return result.rows[0];
    } catch (error) {
      console.error('Error creating setting:', error);
      throw error;
    }
  }
}

export const settingsRepository = new SettingsRepository();
```

## Error Handling Pattern

All layers should use the error helper functions:

```typescript
// From middleware/error.ts
createValidationError(message, details?)  // 400
createAuthError(message)                  // 401
createForbiddenError(message)             // 403
createNotFoundError(message)              // 404
createDatabaseError(message, details?)    // 500
```

Controllers should wrap all handlers with `asyncHandler()` which automatically catches errors and passes them to the error middleware.

## Testing Pattern

Each layer should have corresponding tests:

```
__tests__/
├── [module].controller.test.ts   # Test HTTP handling, session validation
├── [module].service.test.ts      # Test business logic, validation
└── [module].repository.test.ts   # Test database queries (with mocks)
```

## Key Principles

1. **Separation of Concerns**: Each layer has a single responsibility
2. **Dependency Flow**: Controller → Service → Repository (one direction only)
3. **No Skipping Layers**: Controller should never call Repository directly
4. **Singleton Pattern**: Export single instances of Service and Repository
5. **Error Handling**: Use `asyncHandler()` and error creator functions
6. **Type Safety**: Use TypeScript types from `@shared/schema`
7. **Documentation**: JSDoc comments for all public methods
8. **Validation**: Service layer validates business rules
9. **Database Abstraction**: Repository layer abstracts database implementation
10. **Testing**: Each layer independently testable

## Module Checklist

When creating a new module, ensure:

- [ ] Routes file with proper middleware
- [ ] Controller with asyncHandler wrappers
- [ ] Service with validation methods
- [ ] Repository with error handling
- [ ] Types file with interfaces
- [ ] Index file with exports
- [ ] Test files for each layer
- [ ] JSDoc documentation
- [ ] Registered in `/routes/index.ts`
- [ ] Authentication applied if needed
