# Data Access Layer Documentation

Created: 2025-10-13

## Overview

The Data Access Layer (Repository Pattern) handles all database operations, abstracting the underlying database implementation from business logic.

## Repository Layer Responsibilities

1. **Database Queries**: Execute all SQL queries
2. **Result Mapping**: Transform database results to application types
3. **Error Handling**: Catch and log database errors
4. **Transaction Management**: Handle database transactions
5. **Connection Management**: Use connection pool efficiently

## Three Database Access Patterns

### Pattern 1: Drizzle ORM (Preferred)

**When to use**: New code, refactoring, Portal-DB queries

**Modules using**: monitoring, auth (partial)

**Example**:
```typescript
import { getDb } from "../../db";
import { objects, systemAlerts } from "@shared/schema";
import { eq, and, or, sql, inArray, desc } from "drizzle-orm";

export class MonitoringRepository {
  async getDashboardKPIs(): Promise<DashboardKPIs> {
    try {
      const db = getDb();

      // Parallel query execution
      const [totalFacilitiesResult, activeFacilitiesResult, criticalSystemsResult] =
        await Promise.all([
          db.select({ count: sql<number>`COUNT(*)::int` }).from(objects),
          db.select({ count: sql<number>`COUNT(*)::int` })
            .from(objects)
            .where(eq(objects.status, 'active')),
          db.select({ count: sql<number>`COUNT(*)::int` })
            .from(systemAlerts)
            .where(eq(systemAlerts.isResolved, false))
        ]);

      return {
        totalFacilities: totalFacilitiesResult[0]?.count || 0,
        activeFacilities: activeFacilitiesResult[0]?.count || 0,
        criticalSystems: criticalSystemsResult[0]?.count || 0
      };
    } catch (error) {
      console.error('Error fetching KPIs:', error);
      throw error;
    }
  }
}
```

**Benefits**:
- Type-safe queries
- Better IDE autocomplete
- Query builder pattern
- Migration support
- Less SQL injection risk

**Drawbacks**:
- Learning curve
- Complex queries may be verbose
- Not all SQL features supported

### Pattern 2: ConnectionPoolManager (Legacy)

**When to use**: Existing code, complex SQL, Portal-DB queries

**Modules using**: settings, logbook, energy, efficiency, most modules

**Example**:
```typescript
import { ConnectionPoolManager } from "../../connection-pool";
import type { Settings, InsertSettings } from "@shared/schema";

export class SettingsRepository {
  async getSettings(filters?: { category?: string; user_id?: string; mandant_id?: number; }): Promise<Settings[]> {
    try {
      const pool = ConnectionPoolManager.getInstance().getPool();

      let query = `SELECT * FROM settings WHERE 1=1`;
      const params: any[] = [];
      let paramIndex = 1;

      if (filters?.category) {
        query += ` AND category = $${paramIndex++}`;
        params.push(filters.category);
      }
      if (filters?.user_id) {
        query += ` AND user_id = $${paramIndex++}`;
        params.push(filters.user_id);
      }
      if (filters?.mandant_id) {
        query += ` AND mandant_id = $${paramIndex++}`;
        params.push(filters.mandant_id);
      }

      query += ` ORDER BY created_at DESC`;

      const result = await pool.query(query, params);
      return result.rows;
    } catch (error) {
      console.error('Error fetching settings:', error);
      return [];
    }
  }
}
```

**Benefits**:
- Full SQL power
- Familiar to developers
- Works with complex queries
- Direct control

**Drawbacks**:
- No type safety
- Manual parameter binding
- SQL injection risk if not careful
- No query builder

### Pattern 3: Dynamic Pool (External Databases)

**When to use**: External databases ONLY (Energy DB)

**Modules using**: efficiency, energy

**Example**:
```typescript
export class EfficiencyController {
  async getEfficiencyAnalysis(req: Request, res: Response) {
    try {
      // Get external DB config from settings
      const energySettings = await energyRepository.getSettings({ category: "data" });
      const dbConfig = energySettings.find(s => s.key_name === "dbEnergyData_view_day_comp");
      const config = dbConfig.value;

      // Create temporary pool
      const { Pool } = await import("pg");
      const energyDbPool = new Pool({
        host: config.host,
        port: config.port,
        database: config.database,
        user: config.username,
        password: config.password,
        ssl: config.ssl || false,
        connectionTimeoutMillis: config.connectionTimeout || 15000,
        max: 5,
        idleTimeoutMillis: 30000,
        allowExitOnIdle: true,
      });

      // Execute query
      const energyResult = await energyDbPool.query(energyQuery, [meterId]);

      // IMPORTANT: Always end the pool
      await energyDbPool.end();

      return energyResult.rows;
    } catch (error) {
      console.error('Error querying external database:', error);
      throw error;
    }
  }
}
```

**Benefits**:
- Isolates external DB connections
- Config-driven connection
- Independent pool management

**Drawbacks**:
- Must remember to call `.end()`
- Pool creation overhead
- Risk of connection leaks
- Should be in repository, not controller!

## Standard Repository Pattern

### Class Structure

```typescript
import { getDb } from "../../db";
import { [entities] } from "@shared/schema";
import { eq } from "drizzle-orm";
import type { [Entity], Insert[Entity] } from "@shared/schema";

/**
 * [Module] Repository
 *
 * Data access layer for [module] operations.
 * Handles direct database queries using Drizzle ORM.
 */
export class [Module]Repository {
  /**
   * Get all [entities]
   * @returns Array of [Entity] records
   */
  async getAll(): Promise<[Entity][]> {
    try {
      const db = getDb();
      return await db.select().from([entities]);
    } catch (error) {
      console.error('Error fetching [entities]:', error);
      throw error;
    }
  }

  /**
   * Get [entity] by ID
   * @param id - Entity ID
   * @returns [Entity] record or undefined
   */
  async getById(id: number): Promise<[Entity] | undefined> {
    try {
      const db = getDb();
      const [entity] = await db
        .select()
        .from([entities])
        .where(eq([entities].id, id))
        .limit(1);
      return entity;
    } catch (error) {
      console.error(`Error fetching [entity] ${id}:`, error);
      return undefined;
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

  /**
   * Update [entity]
   * @param id - Entity ID
   * @param data - Partial entity data to update
   * @returns Updated [Entity] record
   */
  async update(id: number, data: Partial<Insert[Entity]>): Promise<[Entity]> {
    try {
      const db = getDb();
      const [updatedEntity] = await db
        .update([entities])
        .set(data)
        .where(eq([entities].id, id))
        .returning();

      if (!updatedEntity) {
        throw new Error(`[Entity] with ID ${id} not found`);
      }

      return updatedEntity;
    } catch (error) {
      console.error(`Error updating [entity] ${id}:`, error);
      throw error;
    }
  }

  /**
   * Delete [entity]
   * @param id - Entity ID
   */
  async delete(id: number): Promise<void> {
    try {
      const db = getDb();
      await db.delete([entities]).where(eq([entities].id, id));
    } catch (error) {
      console.error(`Error deleting [entity] ${id}:`, error);
      throw error;
    }
  }
}

// Singleton instance
export const [module]Repository = new [Module]Repository();
```

## Drizzle ORM Usage Patterns

### Simple Select

```typescript
// Select all
const all = await db.select().from(table);

// Select specific columns
const names = await db.select({ name: table.name }).from(table);

// Select with where
const active = await db.select().from(table).where(eq(table.status, 'active'));
```

### Complex Queries

```typescript
// Multiple conditions (AND)
const results = await db
  .select()
  .from(objects)
  .where(
    and(
      eq(objects.status, 'active'),
      inArray(objects.mandantId, [1, 2, 3])
    )
  );

// Multiple conditions (OR)
const results = await db
  .select()
  .from(objects)
  .where(
    or(
      eq(objects.status, 'critical'),
      eq(objects.status, 'error')
    )
  );

// Complex nested conditions
const results = await db
  .select()
  .from(objects)
  .where(
    and(
      or(
        eq(objects.status, 'critical'),
        eq(objects.status, 'error')
      ),
      inArray(objects.mandantId, mandantIds)
    )
  );
```

### Joins

```typescript
// Left join
const results = await db
  .select({
    id: systemAlerts.id,
    objectName: objects.name,
  })
  .from(systemAlerts)
  .leftJoin(objects, eq(systemAlerts.objectId, objects.objectid));
```

### Aggregations

```typescript
// Count
const [{ count }] = await db
  .select({ count: sql<number>`COUNT(*)::int` })
  .from(objects);

// Group by
const results = await db
  .select({
    mandantId: objects.mandantId,
    count: sql<number>`COUNT(*)::int`
  })
  .from(objects)
  .groupBy(objects.mandantId);
```

### Ordering and Limiting

```typescript
// Order by
const sorted = await db
  .select()
  .from(objects)
  .orderBy(desc(objects.createdAt));

// Limit and offset
const paginated = await db
  .select()
  .from(objects)
  .limit(10)
  .offset(20);
```

### Insert

```typescript
// Single insert
const [newObject] = await db
  .insert(objects)
  .values({
    name: 'New Object',
    status: 'active'
  })
  .returning();

// Batch insert
const newObjects = await db
  .insert(objects)
  .values([
    { name: 'Object 1', status: 'active' },
    { name: 'Object 2', status: 'active' }
  ])
  .returning();
```

### Update

```typescript
// Update with returning
const [updated] = await db
  .update(objects)
  .set({ status: 'inactive' })
  .where(eq(objects.id, 123))
  .returning();

// Update multiple
await db
  .update(objects)
  .set({ status: 'archived' })
  .where(inArray(objects.id, [1, 2, 3]));
```

### Delete

```typescript
// Delete single
await db.delete(objects).where(eq(objects.id, 123));

// Delete multiple
await db.delete(objects).where(inArray(objects.id, [1, 2, 3]));

// Delete with condition
await db.delete(objects).where(eq(objects.status, 'archived'));
```

### Raw SQL (when needed)

```typescript
// Custom SQL with type safety
const results = await db.select({
  id: objects.id,
  custom: sql<number>`EXTRACT(YEAR FROM ${objects.createdAt})`
}).from(objects);
```

## ConnectionPoolManager Usage Patterns

### Basic Query

```typescript
const pool = ConnectionPoolManager.getInstance().getPool();
const result = await pool.query('SELECT * FROM table WHERE id = $1', [id]);
return result.rows;
```

### Dynamic Query Building

```typescript
let query = 'SELECT * FROM table WHERE 1=1';
const params: any[] = [];
let paramIndex = 1;

if (filter1) {
  query += ` AND field1 = $${paramIndex++}`;
  params.push(filter1);
}

if (filter2) {
  query += ` AND field2 = $${paramIndex++}`;
  params.push(filter2);
}

const result = await pool.query(query, params);
```

### Insert with RETURNING

```typescript
const result = await pool.query(
  `INSERT INTO table (name, status) VALUES ($1, $2) RETURNING *`,
  [name, status]
);
return result.rows[0];
```

### Update

```typescript
const result = await pool.query(
  `UPDATE table SET status = $1, updated_at = NOW() WHERE id = $2 RETURNING *`,
  [status, id]
);
return result.rows[0];
```

### Delete

```typescript
await pool.query('DELETE FROM table WHERE id = $1', [id]);
```

### Transactions (advanced)

```typescript
const pool = ConnectionPoolManager.getInstance().getPool();
const client = await pool.connect();

try {
  await client.query('BEGIN');

  // Multiple operations
  await client.query('INSERT INTO table1 VALUES ($1)', [value1]);
  await client.query('UPDATE table2 SET field = $1', [value2]);

  await client.query('COMMIT');
} catch (error) {
  await client.query('ROLLBACK');
  throw error;
} finally {
  client.release();
}
```

## Connection Pool Usage

### Primary Database (Portal-DB)

**Connection String**: `DATABASE_URL` environment variable

**Access**:
```typescript
// Via Drizzle
const db = getDb();

// Via ConnectionPoolManager
const pool = ConnectionPoolManager.getInstance().getPool();
```

**Pool Configuration**:
- Min connections: 5 (default)
- Max connections: 20 (default)
- Idle timeout: 30s
- Connection timeout: 5s

**Health Monitoring**:
- Automatic health checks every 30s
- Circuit breaker pattern (opens after 5 failures)
- Metrics tracking (query times, error rates)

### External Energy Database

**Access**: Dynamic Pool instances

**Configuration**: Retrieved from settings table at runtime

**Tables**:
- `view_day_comp` - Daily energy compensation data
- `view_mon_comp` - Monthly energy compensation data

**Usage Pattern**:
```typescript
// Get config
const energySettings = await energyRepository.getSettings({ category: "data" });
const dbConfig = energySettings.find(s => s.key_name === "dbEnergyData_view_day_comp");

// Create pool
const { Pool } = await import("pg");
const pool = new Pool({
  host: dbConfig.value.host,
  port: dbConfig.value.port,
  database: dbConfig.value.database,
  user: dbConfig.value.username,
  password: dbConfig.value.password,
  ssl: dbConfig.value.ssl || false,
  max: 5,
  idleTimeoutMillis: 30000,
  allowExitOnIdle: true
});

// Use pool
const result = await pool.query(sql, params);

// IMPORTANT: Clean up
await pool.end();
```

## Query Optimization Patterns

### 1. Parallel Query Execution

```typescript
// Bad: Sequential queries
const totalFacilities = await db.select({ count: sql`COUNT(*)` }).from(objects);
const activeFacilities = await db.select({ count: sql`COUNT(*)` }).from(objects).where(eq(objects.status, 'active'));

// Good: Parallel queries
const [totalFacilities, activeFacilities] = await Promise.all([
  db.select({ count: sql`COUNT(*)` }).from(objects),
  db.select({ count: sql`COUNT(*)` }).from(objects).where(eq(objects.status, 'active'))
]);
```

**Used in**: monitoring.repository.ts (getDashboardKPIs)

### 2. Limit Results

```typescript
// Always limit large result sets
const recent = await db
  .select()
  .from(objects)
  .orderBy(desc(objects.createdAt))
  .limit(100);  // Prevent returning thousands of rows
```

### 3. Select Only Needed Columns

```typescript
// Bad: Select everything
const objects = await db.select().from(objects);

// Good: Select specific columns
const objects = await db
  .select({
    id: objects.id,
    name: objects.name,
    status: objects.status
  })
  .from(objects);
```

### 4. Use Indexes

Ensure database has indexes on:
- Primary keys (automatic)
- Foreign keys
- Frequently queried columns (status, mandantId, createdAt)
- Columns used in WHERE clauses

### 5. Avoid N+1 Queries

```typescript
// Bad: N+1 queries
const objects = await objectsRepository.getAll();
for (const object of objects) {
  const energy = await energyRepository.getForObject(object.id);  // N queries!
  object.energyData = energy;
}

// Good: Batch query or JOIN
const objects = await db
  .select()
  .from(objects)
  .leftJoin(energy, eq(objects.id, energy.objectId));
```

## Error Handling Patterns

### Repository Error Handling

```typescript
async getById(id: number): Promise<Entity | undefined> {
  try {
    const db = getDb();
    const [entity] = await db
      .select()
      .from(entities)
      .where(eq(entities.id, id))
      .limit(1);
    return entity;
  } catch (error) {
    console.error(`Error fetching entity ${id}:`, error);
    return undefined;  // Return undefined for not found
  }
}
```

### Throw vs Return

**Return undefined/null for not found**:
```typescript
async getById(id: number): Promise<Entity | undefined> {
  // Return undefined if not found
}
```

**Throw errors for failures**:
```typescript
async create(data: InsertEntity): Promise<Entity> {
  try {
    // ...
  } catch (error) {
    console.error('Error creating entity:', error);
    throw error;  // Throw for failures
  }
}
```

## Repository Testing

Repositories should be tested with a test database:

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { settingsRepository } from './settings.repository';

describe('SettingsRepository', () => {
  beforeAll(async () => {
    // Setup test database
    await setupTestDatabase();
  });

  afterAll(async () => {
    // Cleanup test database
    await cleanupTestDatabase();
  });

  describe('getSettings', () => {
    it('should return settings with category filter', async () => {
      // Insert test data
      await insertTestSettings();

      // Test
      const result = await settingsRepository.getSettings({ category: 'test' });

      // Verify
      expect(result).toHaveLength(1);
      expect(result[0].category).toBe('test');
    });
  });
});
```

## Repository Best Practices

### DO:
1. ✅ Use try-catch for all queries
2. ✅ Log all errors with context
3. ✅ Return typed results
4. ✅ Use parameterized queries
5. ✅ Include JSDoc comments
6. ✅ Export as singleton
7. ✅ Prefer Drizzle ORM for new code
8. ✅ Close external pools with `.end()`

### DON'T:
1. ❌ Include business logic
2. ❌ Handle HTTP req/res
3. ❌ Validate data (service layer responsibility)
4. ❌ Transform data excessively (keep close to DB schema)
5. ❌ Use string concatenation for SQL (SQL injection risk)
6. ❌ Return raw database errors (log and throw generic errors)
7. ❌ Leave external pools open (connection leaks)

## Migration Strategy: ConnectionPoolManager → Drizzle

For existing modules using ConnectionPoolManager:

1. **Identify queries** in repository
2. **Create Drizzle schema** (if not exists)
3. **Rewrite queries** using Drizzle query builder
4. **Test thoroughly** with existing tests
5. **Update one method at a time** (incremental)

**Example**:

Before (ConnectionPoolManager):
```typescript
async getSettings(filters?: { category?: string }): Promise<Settings[]> {
  const pool = ConnectionPoolManager.getInstance().getPool();
  let query = 'SELECT * FROM settings WHERE 1=1';
  const params: any[] = [];

  if (filters?.category) {
    query += ' AND category = $1';
    params.push(filters.category);
  }

  const result = await pool.query(query, params);
  return result.rows;
}
```

After (Drizzle):
```typescript
async getSettings(filters?: { category?: string }): Promise<Settings[]> {
  const db = getDb();
  let query = db.select().from(settings);

  if (filters?.category) {
    query = query.where(eq(settings.category, filters.category));
  }

  return await query;
}
```

## Conclusion

The Data Access Layer uses three patterns: Drizzle ORM (preferred), ConnectionPoolManager (legacy), and Dynamic Pools (external DBs). Drizzle ORM should be used for all new code and refactoring efforts. ConnectionPoolManager is acceptable for complex SQL. Dynamic Pools should ONLY be used for external databases and must always be cleaned up with `.end()`.

**Key recommendation**: Gradually migrate ConnectionPoolManager usage to Drizzle ORM, starting with simple CRUD repositories.
