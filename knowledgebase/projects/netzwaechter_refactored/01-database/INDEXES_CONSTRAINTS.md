# Database Indexes and Constraints

Created: 2025-10-13

## Overview

This document details all indexes, unique constraints, and primary keys in the Netzwächter database schema.

---

## Primary Keys

All tables use SERIAL (auto-incrementing integer) or VARCHAR primary keys:

| Table | Primary Key Column | Type |
|-------|-------------------|------|
| sessions | sid | VARCHAR |
| user_profiles | id | SERIAL |
| users | id | VARCHAR |
| mandants | id | SERIAL |
| objects | id | SERIAL |
| object_mandant | id | SERIAL |
| object_groups | id | SERIAL |
| system_alerts | id | SERIAL |
| day_comp | counter | SERIAL |
| view_mon_comp | counter | SERIAL |
| daily_outdoor_temperatures | id | SERIAL |
| settings | id | SERIAL |
| logbook_entries | id | SERIAL |
| todo_tasks | id | SERIAL |
| collaboration_annotations | id | SERIAL |
| annotation_reactions | id | SERIAL |
| annotation_subscriptions | id | SERIAL |
| agents | id | SERIAL |
| agent_logs | id | SERIAL |
| user_activity_logs | id | SERIAL |

---

## Unique Constraints

### sessions
- `sid` (Primary Key - implicit unique)

### user_profiles
- `name` (Explicit unique constraint)

### users
- `id` (Primary Key - implicit unique)
- `username` (Explicit unique constraint)
- `email` (Explicit unique constraint)

### objects
- `objectid` (Explicit unique constraint)
  - Note: `id` is the primary key, but `objectid` is the business identifier

### object_mandant
- `objectId` (Explicit unique constraint)
  - Ensures each object can only have one record in this table

### No other tables have explicit unique constraints beyond primary keys.

---

## Indexes by Table

### sessions
**Total Indexes:** 2 (1 PK + 1 secondary)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | sid | Primary Key | Session lookup |
| IDX_session_expire | expire | B-tree | Session cleanup queries |

### user_profiles
**Total Indexes:** 1 (PK only)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | id | Primary Key | Profile lookup |

### users
**Total Indexes:** 3 (1 PK + 2 unique)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | id | Primary Key | User lookup |
| (Unique) | username | Unique | Username uniqueness |
| (Unique) | email | Unique | Email uniqueness |

### mandants
**Total Indexes:** 1 (PK only)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | id | Primary Key | Mandant lookup |

### objects
**Total Indexes:** 7 (1 PK + 1 unique + 5 secondary)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | id | Primary Key | Internal lookup |
| (Unique) | objectid | Unique | Business identifier |
| idx_objects_objectid | objectid | B-tree | Object queries |
| idx_objects_mandant_id | mandantId | B-tree | Tenant filtering |
| idx_objects_type | objectType | B-tree | Object type filtering |
| idx_objects_status | status | B-tree | Status filtering |
| idx_objects_city | city | B-tree | Location queries |
| idx_objects_postal_code | postalCode | B-tree | Postal code queries |

**Index Coverage:** Excellent coverage for common query patterns including tenant filtering, type filtering, status filtering, and location-based queries.

### object_mandant
**Total Indexes:** 3 (1 PK + 1 unique + 1 secondary)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | id | Primary Key | Record lookup |
| (Unique) | objectId | Unique | One record per object |
| idx_object_mandant_objectid | objectId | B-tree | Object association queries |
| idx_object_mandant_mandant_id | mandantId | B-tree | Mandant association queries |

### object_groups
**Total Indexes:** 1 (PK only)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | id | Primary Key | Group lookup |

### system_alerts
**Total Indexes:** 1 (PK only)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | id | Primary Key | Alert lookup |

**Note:** Missing indexes on `objectId`, `isResolved`, and `createdAt` could impact performance.

### day_comp
**Total Indexes:** 4 (1 PK + 3 secondary)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | counter | Primary Key | Record lookup |
| idx_day_comp_time | time | B-tree | Time-based queries |
| idx_day_comp_log | log | B-tree | Object-based queries |
| idx_day_comp_time_log | (time, log) | Composite B-tree | Time + object queries |

**Index Coverage:** Excellent time-series indexing with composite index for combined queries.

### view_mon_comp
**Total Indexes:** 1 (PK only)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | counter | Primary Key | Record lookup |

**Note:** As a view, performance depends on underlying table indexes.

### daily_outdoor_temperatures
**Total Indexes:** 5 (1 PK + 4 secondary)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | id | Primary Key | Record lookup |
| idx_daily_temp_date | date | B-tree | Date-based queries |
| idx_daily_temp_postal_code | postalCode | B-tree | Location queries |
| idx_daily_temp_date_postal_code | (date, postalCode) | Composite B-tree | Combined date + location |
| idx_daily_temp_city | city | B-tree | City-based queries |

**Index Coverage:** Excellent coverage for time-series and location-based temperature queries.

### settings
**Total Indexes:** 5 (1 PK + 4 secondary)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | id | Primary Key | Setting lookup |
| idx_settings_category | category | B-tree | Category filtering |
| idx_settings_key_name | key_name | B-tree | Key lookup |
| idx_settings_user_id | user_id | B-tree | User settings |
| idx_settings_mandant_id | mandant_id | B-tree | Tenant settings |

**Index Coverage:** Comprehensive coverage for all common setting query patterns.

### logbook_entries
**Total Indexes:** 4 (1 PK + 3 secondary)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | id | Primary Key | Entry lookup |
| idx_logbook_entries_object_id | objectId | B-tree | Object maintenance history |
| idx_logbook_entries_status | status | B-tree | Status filtering |
| idx_logbook_entries_scheduled_date | scheduledDate | B-tree | Scheduling queries |

**Index Coverage:** Good coverage for maintenance tracking queries.

### todo_tasks
**Total Indexes:** 4 (1 PK + 3 secondary)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | id | Primary Key | Task lookup |
| idx_todo_tasks_object_id | objectId | B-tree | Object tasks |
| idx_todo_tasks_status | status | B-tree | Status filtering |
| idx_todo_tasks_due_date | dueDate | B-tree | Due date queries |

**Index Coverage:** Good coverage for task management queries.

### collaboration_annotations
**Total Indexes:** 7 (1 PK + 6 secondary)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | id | Primary Key | Annotation lookup |
| idx_annotations_object_id | objectId | B-tree | Object annotations |
| idx_annotations_context | (contextType, contextId) | Composite B-tree | Context-specific annotations |
| idx_annotations_created_by | createdBy | B-tree | User's annotations |
| idx_annotations_status | status | B-tree | Status filtering |
| idx_annotations_type | type | B-tree | Type filtering |
| idx_annotations_parent_id | parentId | B-tree | Threading/replies |

**Index Coverage:** Excellent coverage for collaboration features with composite index for context lookups.

### annotation_reactions
**Total Indexes:** 3 (1 PK + 2 secondary)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | id | Primary Key | Reaction lookup |
| idx_reactions_annotation_id | annotationId | B-tree | Annotation reactions |
| idx_reactions_user_id | userId | B-tree | User reactions |

**Index Coverage:** Sufficient for reaction queries.

### annotation_subscriptions
**Total Indexes:** 3 (1 PK + 2 secondary)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | id | Primary Key | Subscription lookup |
| idx_subscriptions_user_id | userId | B-tree | User subscriptions |
| idx_subscriptions_object_id | objectId | B-tree | Object subscriptions |

**Index Coverage:** Sufficient for subscription queries.

### agents
**Total Indexes:** 4 (1 PK + 3 secondary)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | id | Primary Key | Agent lookup |
| idx_agents_status | status | B-tree | Status filtering |
| idx_agents_next_run | nextRun | B-tree | Scheduling queries |
| idx_agents_mandant_id | mandantId | B-tree | Tenant agents |

**Index Coverage:** Good coverage for agent scheduling and management.

### agent_logs
**Total Indexes:** 4 (1 PK + 3 secondary)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | id | Primary Key | Log lookup |
| idx_agent_logs_agent_id | agentId | B-tree | Agent execution history |
| idx_agent_logs_start_time | startTime | B-tree | Time-based queries |
| idx_agent_logs_status | status | B-tree | Status filtering |

**Index Coverage:** Good coverage for log queries and analysis.

### user_activity_logs
**Total Indexes:** 5 (1 PK + 4 secondary)

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| (PK) | id | Primary Key | Log lookup |
| idx_user_activity_logs_user_id | userId | B-tree | User activity history |
| idx_user_activity_logs_action | action | B-tree | Action type queries |
| idx_user_activity_logs_timestamp | timestamp | B-tree | Time-based queries |
| idx_user_activity_logs_resource | (resourceType, resourceId) | Composite B-tree | Resource activity |

**Index Coverage:** Excellent coverage for audit trail queries with composite index.

---

## Index Summary

### Total Index Count by Type
- **Primary Key Indexes:** 20
- **Unique Constraint Indexes:** 4 (username, email, name, objectid)
- **Secondary Indexes:** 48
- **Composite Indexes:** 5

**Grand Total:** 72+ indexes

### Composite Indexes

Composite indexes provide optimized performance for multi-column queries:

1. **idx_day_comp_time_log** (`time`, `log`)
   - Optimizes time-series queries filtered by object

2. **idx_daily_temp_date_postal_code** (`date`, `postalCode`)
   - Optimizes temperature queries by date and location

3. **idx_annotations_context** (`contextType`, `contextId`)
   - Optimizes context-specific annotation lookups

4. **idx_user_activity_logs_resource** (`resourceType`, `resourceId`)
   - Optimizes resource-specific activity queries

5. **idx_object_mandant_objectid** (implicit, but used with mandantId)
   - Supports object-tenant relationship queries

---

## Index Coverage Analysis

### Excellent Coverage (6+ indexes)
- `objects`: 7 indexes
- `collaboration_annotations`: 7 indexes
- `daily_outdoor_temperatures`: 5 indexes
- `settings`: 5 indexes
- `user_activity_logs`: 5 indexes

### Good Coverage (3-5 indexes)
- `day_comp`: 4 indexes
- `logbook_entries`: 4 indexes
- `todo_tasks`: 4 indexes
- `agents`: 4 indexes
- `agent_logs`: 4 indexes
- `object_mandant`: 3 indexes
- `users`: 3 indexes
- `annotation_reactions`: 3 indexes
- `annotation_subscriptions`: 3 indexes

### Minimal Coverage (1-2 indexes)
- `sessions`: 2 indexes (sufficient for session management)
- `user_profiles`: 1 index (simple lookup table)
- `mandants`: 1 index (simple lookup table)
- `object_groups`: 1 index (minimal usage)
- `system_alerts`: 1 index (⚠️ could benefit from more indexes)
- `view_mon_comp`: 1 index (view relies on underlying tables)

---

## Index Performance Considerations

### Well-Optimized Tables
- **objects**: Comprehensive indexing for all query patterns
- **day_comp**: Time-series optimized with composite index
- **settings**: Full coverage for category, key, user, and tenant queries
- **collaboration_annotations**: Excellent indexing for collaboration features
- **user_activity_logs**: Audit trail optimized with composite indexes

### Potential Optimization Opportunities

#### system_alerts
**Current:** Only primary key
**Recommended:** Add indexes on:
- `objectId` (for object-specific alerts)
- `isResolved` (for filtering resolved/unresolved)
- `createdAt` (for time-based queries)
- Composite: `(objectId, isResolved, createdAt)`

#### view_mon_comp
**Current:** Only primary key
**Note:** As a view, relies on underlying `day_comp` indexes. Consider:
- Adding indexes if materialized view
- Ensuring `day_comp` indexes cover view queries

#### object_groups
**Current:** Only primary key
**Potential:** Add indexes on:
- `type` (if filtering by group type is common)
- `name` (for name-based searches)

---

## Index Maintenance

### Automatic Maintenance
PostgreSQL automatically maintains indexes through:
- B-tree index updates on INSERT/UPDATE/DELETE
- VACUUM operations to reclaim space
- ANALYZE operations to update statistics

### Index Bloat Prevention
- Regular VACUUM operations prevent index bloat
- REINDEX can be used if bloat becomes significant
- Monitor index size growth over time

### Statistics Updates
- Auto-analyze keeps statistics current
- Manual ANALYZE recommended after bulk operations
- Statistics guide query planner decisions

---

## JSONB Indexing

### Current State
No explicit JSONB indexes are defined in the schema.

### JSONB Columns Without Indexes
- `sessions.sess`
- `user_profiles.sidebar`
- `users.address`
- `users.mandantAccess`
- `mandants.info`
- `objects.*` (15+ JSONB columns)
- `logbook_entries.attachments`
- `collaboration_annotations.position`
- `collaboration_annotations.timeRange`
- `collaboration_annotations.tags`
- `annotation_subscriptions.notificationMethods`
- `agents.config*Schema` (4 config columns)
- `agent_logs.*Data` (3 data columns)

### JSONB Index Recommendations

If queries frequently filter on JSONB fields, consider:

```sql
-- GIN indexes for JSONB containment queries
CREATE INDEX idx_objects_mandant_access ON objects USING GIN (mandant_access);
CREATE INDEX idx_users_mandant_access ON users USING GIN (mandant_access);
CREATE INDEX idx_annotations_tags ON collaboration_annotations USING GIN (tags);

-- B-tree indexes for specific JSONB paths
CREATE INDEX idx_mandants_info_email ON mandants ((info->'kontakt'->>'email'));
CREATE INDEX idx_objects_objdata_type ON objects ((objdata->>'type'));
```

**Trade-off:** JSONB indexes increase storage and write overhead but dramatically improve query performance on JSONB fields.

---

## Constraint Summary

### NOT NULL Constraints

#### Strict NOT NULL (Required Fields)
- `sessions.sess`, `sessions.expire`
- `user_profiles.name`
- `mandants.name`
- `objects.objectid`
- `logbook_entries.title`
- `todo_tasks.title`
- `collaboration_annotations.title`, `content`, `type`, `createdBy`
- `annotation_reactions.annotationId`, `userId`, `reactionType`
- `annotation_subscriptions.userId`
- `agents.name`, `config*Schema`
- `agent_logs.agentId`, `startTime`, `status`
- `user_activity_logs.action`, `timestamp`
- `daily_outdoor_temperatures.date`, `postalCode`
- `settings.category`, `key_name`, `value`

#### Nullable (Optional Fields)
Most other columns are nullable to support flexible data entry and partial information.

### DEFAULT Constraints

Common defaults include:
- `NOW()` / `defaultNow()` for timestamps (`createdAt`, `updatedAt`)
- `false` for boolean flags
- `0` for counters
- `'active'` for status fields
- `'user'` for user roles
- `'Deutschland'` for country
- `'/maps'` for start pages
- `{}` for empty JSONB objects
- `[]` for empty JSONB arrays

---

## Performance Best Practices

### Index Usage
1. **Primary keys** are automatically indexed (B-tree)
2. **Foreign keys** should be indexed for join performance (implemented)
3. **Frequently filtered columns** have indexes (good coverage)
4. **Composite indexes** exist for common multi-column queries
5. **Time-series data** has temporal indexes (day_comp, logs)

### Query Optimization
1. Use indexed columns in WHERE clauses
2. Leverage composite indexes for multi-column filters
3. Use EXPLAIN ANALYZE to verify index usage
4. Monitor slow query logs
5. Update statistics regularly with ANALYZE

### Index Considerations
1. Every index adds write overhead
2. Too many indexes slow INSERT/UPDATE operations
3. Unused indexes waste space and maintenance time
4. Composite indexes require correct column order
5. JSONB indexes are powerful but expensive
