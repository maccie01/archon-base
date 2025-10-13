# JSONB Patterns in PostgreSQL

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Perplexity research on PostgreSQL JSONB 2024-2025, JSONB indexing strategies, best practices

## Overview

JSONB is PostgreSQL's binary JSON storage format that provides flexible schema capabilities with strong query performance. This document covers when and how to use JSONB effectively.

## Core Principles

1. JSONB for flexible/optional fields, relational for structured data
2. Index JSONB columns with GIN indexes for query performance
3. Use jsonb_path_ops for smaller indexes when querying specific paths
4. Type JSONB fields in TypeScript for type safety
5. JSONB is not a replacement for proper normalization

## JSONB vs JSON vs Relational

### When to Use JSONB

**Good use cases:**
- User preferences and settings
- Flexible metadata
- API responses to store
- Audit logs
- Feature flags
- Configuration objects
- Semi-structured data from external sources

**Bad use cases:**
- Core business entities (use relational tables)
- Frequently queried structured data
- Data requiring complex joins
- Data with strong referential integrity needs

### JSONB vs JSON Type

```sql
-- TODO: Add comparison example
-- JSON: text storage, preserves formatting
-- JSONB: binary storage, faster to process, supports indexing
-- Always prefer JSONB unless you need exact text preservation
```

## Schema Definition with Drizzle

### Basic JSONB Column

```typescript
// TODO: Add basic JSONB column example in Drizzle
import { pgTable, jsonb } from "drizzle-orm/pg-core";

// Without typing
jsonb("metadata")

// With TypeScript typing (recommended)
jsonb("metadata").$type<{
  key1: string;
  key2?: number;
}>()

// With default value
jsonb("settings").$type<UserSettings>().default({})
```

### Type-Safe JSONB with Zod

```typescript
// TODO: Add Zod validation for JSONB
import { z } from "zod";

const userSettingsSchema = z.object({
  theme: z.enum(["light", "dark"]).optional(),
  language: z.string().optional(),
  notifications: z.object({
    email: z.boolean().optional(),
    push: z.boolean().optional(),
  }).optional(),
});

type UserSettings = z.infer<typeof userSettingsSchema>;
```

## JSONB Indexing

### GIN Index with jsonb_ops (Default)

**Indexes everything - maximum flexibility:**
```sql
-- TODO: Add jsonb_ops GIN index example
-- CREATE INDEX idx_users_metadata ON users USING GIN (metadata);
-- Supports all JSONB operators
-- Larger index size
```

**Supported operators:**
- `@>` (contains)
- `?` (key exists)
- `?&` (all keys exist)
- `?|` (any key exists)
- `@?` (JSON path query)
- `@@` (JSON path predicate)

### GIN Index with jsonb_path_ops

**Indexes value paths - smaller, faster for specific queries:**
```sql
-- TODO: Add jsonb_path_ops GIN index example
-- CREATE INDEX idx_users_metadata_path ON users USING GIN (metadata jsonb_path_ops);
-- Supports only @> operator
-- Smaller index (30-50% reduction)
-- Faster for containment queries
```

**When to use:**
- Only need containment queries (`@>`)
- Want smaller index size
- Query specific paths frequently

### Expression Indexes on JSONB Paths

```sql
-- TODO: Add expression index example
-- CREATE INDEX idx_users_email ON users ((metadata->>'email'));
-- Index specific field for fast equality checks
-- Use when querying specific fields frequently
```

## Querying JSONB

### Operators

```sql
-- TODO: Add JSONB operator examples
-- -> get JSON object field (returns JSONB)
-- ->> get JSON object field as text
-- #> get JSON object at path (returns JSONB)
-- #>> get JSON object at path as text
-- @> contains
-- <@ is contained by
-- ? key exists
-- ?& all keys exist
-- ?| any key exists
```

### Basic Queries

```typescript
// TODO: Add Drizzle JSONB query examples
// Filtering by JSONB field
// Checking key existence
// Containment queries
```

### Path Queries

```sql
-- TODO: Add JSON path query examples
-- @? and @@ operators
-- JSON path syntax
-- Filtering nested objects
```

### Aggregations on JSONB

```sql
-- TODO: Add JSONB aggregation examples
-- jsonb_agg()
-- jsonb_object_agg()
-- Aggregating into JSONB arrays/objects
```

## Updating JSONB

### Replacing Entire Object

```typescript
-- TODO: Add full JSONB update example
-- UPDATE users SET metadata = '{"new": "object"}' WHERE id = 1;
```

### Partial Updates with jsonb_set

```sql
-- TODO: Add jsonb_set example
-- UPDATE users SET metadata = jsonb_set(metadata, '{key}', '"value"');
-- Updating nested values
-- Creating paths if they don't exist
```

### Merging JSONB Objects

```sql
-- TODO: Add JSONB merge example
-- Using || operator
-- jsonb_set for specific paths
```

### Deleting Keys

```sql
-- TODO: Add JSONB key deletion
-- - operator to remove keys
-- #- operator to remove paths
```

## Common JSONB Patterns

### Pattern 1: User Preferences

```typescript
// TODO: Add user preferences example
-- Theme, language, notification settings
-- Type-safe with TypeScript
-- Default values
```

### Pattern 2: Flexible Metadata

```typescript
// TODO: Add metadata pattern
-- Additional optional fields
-- Avoiding 100-column tables
-- API response storage
```

### Pattern 3: Audit Logs

```typescript
// TODO: Add audit log JSONB pattern
-- Before/after values
-- Flexible structure for different entities
-- Easy to query with GIN indexes
```

### Pattern 4: Feature Flags

```typescript
// TODO: Add feature flags pattern
-- Per-user or per-tenant flags
-- Easy to add new flags
-- Quick lookups with GIN index
```

### Pattern 5: API Response Caching

```typescript
// TODO: Add API caching pattern
-- Store full API responses
-- Query by specific fields
-- TTL using timestamp column
```

## Performance Considerations

### JSONB vs Relational Performance

**JSONB Advantages:**
- Flexible schema (no migrations for new fields)
- Single row fetch for all data
- Good for read-heavy optional data

**Relational Advantages:**
- Better for complex joins
- Enforces referential integrity
- More storage efficient for structured data
- Better query planning

### Storage Efficiency

```sql
-- TODO: Add storage comparison
-- JSONB compression
-- Compared to equivalent relational schema
-- When JSONB uses more space
```

### Query Performance Tips

1. Use GIN indexes for frequently queried JSONB columns
2. Use expression indexes for specific fields
3. Consider jsonb_path_ops for containment queries
4. Don't over-nest - keep JSONB structures relatively flat
5. Extract frequently queried fields to regular columns

## Validation Strategies

### Application-Level Validation

```typescript
// TODO: Add Zod validation example
-- Validate before INSERT/UPDATE
-- Type-safe with TypeScript
-- Custom validation rules
```

### Database-Level Validation with CHECK Constraints

```sql
-- TODO: Add CHECK constraint for JSONB
-- CHECK (jsonb_typeof(metadata) = 'object')
-- Validating required keys exist
-- Schema validation with custom functions
```

## Migration Strategies

### Adding JSONB Columns

```sql
-- TODO: Add migration to add JSONB column
-- With default value
-- Non-blocking migration
```

### Migrating from Columns to JSONB

```sql
-- TODO: Add migration example
-- Consolidating sparse columns into JSONB
-- Backward compatibility during transition
```

### Migrating from JSONB to Columns

```sql
-- TODO: Add extraction migration
-- When JSONB field becomes core data
-- Creating columns from JSONB values
-- Index creation
```

## Common Patterns from Production

### Pattern: Sidebar Permissions

From netzwaechter-refactored:
```typescript
// TODO: Add sidebar permissions example
jsonb("sidebar").$type<{
  showDashboard?: boolean;
  showMaps?: boolean;
  // ... other permission flags
}>().default({})
```

### Pattern: Address Information

```typescript
// TODO: Add address JSONB pattern
jsonb("info").$type<{
  adresse?: {
    strasse?: string;
    plz?: string;
    ort?: string;
  };
  kontakt?: {
    email?: string;
    telefon?: string;
  };
}>()
```

## Testing JSONB Queries

```typescript
// TODO: Add JSONB query testing examples
-- Test data setup
-- Query assertions
-- Index usage verification
```

## Anti-Patterns

### Anti-Pattern: Using JSONB for Everything
JSONB is not a replacement for proper database design.

### Anti-Pattern: Deep Nesting
Keep JSONB structures relatively flat. Deep nesting hurts performance.

### Anti-Pattern: Storing Arrays of Objects Without Indexes
Large arrays are hard to query efficiently. Consider separate tables.

### Anti-Pattern: Not Validating JSONB Input
Always validate JSONB data at application or database level.

### Anti-Pattern: Using JSONB for High-Cardinality Foreign Keys
Use proper foreign keys instead.

### Anti-Pattern: Not Indexing Queried JSONB Columns
JSONB queries without indexes can be slow.

## Tools and Functions

### Built-in JSONB Functions

```sql
-- TODO: Add comprehensive function list
-- jsonb_each(), jsonb_object_keys()
-- jsonb_array_elements()
-- jsonb_strip_nulls()
-- jsonb_pretty() (for debugging)
```

### Extensions

- **jsonb_plperl** - JSONB in PL/Perl
- **jsonb_plpython** - JSONB in PL/Python

## Additional Resources

### Documentation
- PostgreSQL JSONB: https://www.postgresql.org/docs/current/datatype-json.html
- JSONB Functions: https://www.postgresql.org/docs/current/functions-json.html
- GIN Indexes: https://www.postgresql.org/docs/current/gin.html

### Articles
- "Faster Operations with the JSONB Data Type in PostgreSQL"
- "PostgreSQL JSON vs JSONB"

### Related Knowledge Base Articles
- [Database Design](./DATABASE_DESIGN.md)
- [Indexing and Optimization](./INDEXING_OPTIMIZATION.md)
- [Drizzle ORM Patterns](./DRIZZLE_PATTERNS.md)
- [Query Optimization](./QUERY_OPTIMIZATION.md)
