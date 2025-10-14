# Soft Delete Patterns

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Production experience, soft delete best practices, audit trail requirements

## Overview

Soft delete is the practice of marking records as deleted rather than physically removing them from the database. This preserves data for audit trails, compliance, and potential recovery.

## Core Principles

1. Soft delete for audit trail and compliance requirements
2. Hard delete for sensitive data (GDPR right to be forgotten)
3. Always filter soft-deleted records in queries
4. Consider cascading soft deletes for related records
5. Periodic cleanup of very old soft-deleted records

## Implementation Patterns

### Pattern 1: deleted_at Timestamp

```typescript
// TODO: Add deleted_at pattern
# Nullable timestamp column
# NULL = active, timestamp = deleted
# Preserves deletion time
```

### Pattern 2: is_deleted Boolean

```typescript
// TODO: Add is_deleted pattern
# Boolean column
# true/false
# Simpler but loses deletion time
```

### Pattern 3: status Column

```typescript
// TODO: Add status enum pattern
# 'active', 'deleted', 'archived'
# More flexibility
```

## Querying with Soft Deletes

### Filtering Deleted Records

```typescript
// TODO: Add query filtering examples
# WHERE deleted_at IS NULL
# Drizzle filter patterns
```

### Including Deleted Records

```typescript
// TODO: Add queries including soft-deleted
# Admin interfaces
# Audit reports
```

## Cascading Soft Deletes

```typescript
// TODO: Add cascading soft delete pattern
# Marking related records as deleted
# Maintaining referential integrity
```

## Hard Delete for Compliance

```typescript
// TODO: Add hard delete pattern
# GDPR right to be forgotten
# When to permanently delete
```

## Additional Resources

### Related Knowledge Base Articles
- [Audit Logging](./AUDIT_LOGGING.md)
- [Database Design](./DATABASE_DESIGN.md)
