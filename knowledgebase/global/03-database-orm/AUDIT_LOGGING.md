# Audit Logging and Change Tracking Patterns

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Perplexity research on audit logging, temporal tables, compliance requirements

## Overview

Audit logging tracks who changed what and when in your database. Essential for compliance, debugging, and understanding data history.

## Core Principles

1. Log all changes to sensitive data
2. Include user context (who made the change)
3. Store before/after values for updates
4. Consider retention and storage costs
5. Make audit logs immutable

## Audit Column Pattern

### Standard Audit Columns

```typescript
// TODO: Add standard audit columns
# created_at, updated_at
# created_by, updated_by
# Simple pattern for basic tracking
```

## User Activity Logs

### Activity Log Table

```typescript
// TODO: Add user activity log pattern
# From netzwaechter-refactored
# Action, resource type, resource ID
# IP address, user agent
# JSONB details column
```

## History Tables Pattern

```sql
# TODO: Add history table pattern
# Separate history table per entity
# Triggers to populate history
```

## Temporal Tables Pattern

```sql
# TODO: Add temporal table pattern
# System-versioned tables
# valid_from, valid_to
# Time travel queries
```

## Event Sourcing Pattern

```typescript
// TODO: Add event sourcing pattern
# Append-only event log
# Reconstructing state from events
```

## Compliance Considerations

```
# TODO: Add compliance notes
# GDPR, SOX, HIPAA requirements
# Retention policies
# Audit report generation
```

## Additional Resources

### Related Knowledge Base Articles
- [Soft Delete Patterns](./SOFT_DELETE.md)
- [Database Security](./DATABASE_SECURITY.md)
- [JSONB Patterns](./JSONB_PATTERNS.md)
