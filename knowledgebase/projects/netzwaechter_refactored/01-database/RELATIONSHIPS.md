# Database Relationships

Created: 2025-10-13

## Entity Relationship Overview

This document details all foreign key relationships and data connections in the Netzwächter database schema.

---

## Relationship Diagrams

### Core Entity Relationships

```
mandants (Tenants)
    ├─→ users (1:N)
    ├─→ objects (1:N)
    ├─→ settings (1:N)
    └─→ agents (1:N)

users
    ├─→ user_profiles (N:1)
    ├─→ mandants (N:1) [default tenant]
    ├─→ settings (1:N)
    ├─→ agents (1:N) [created by]
    ├─→ collaboration_annotations (1:N) [created by]
    ├─→ collaboration_annotations (1:N) [updated by]
    ├─→ collaboration_annotations (1:N) [assigned to]
    ├─→ annotation_reactions (1:N)
    ├─→ annotation_subscriptions (1:N)
    ├─→ logbook_entries (1:N) [created by]
    ├─→ logbook_entries (1:N) [updated by]
    ├─→ system_alerts (1:N) [resolved by]
    └─→ user_activity_logs (1:N)

objects
    ├─→ mandants (N:1) [primary tenant]
    ├─→ system_alerts (1:N)
    ├─→ day_comp (1:N)
    ├─→ view_mon_comp (1:N)
    ├─→ logbook_entries (1:N)
    ├─→ todo_tasks (1:N)
    ├─→ collaboration_annotations (1:N)
    ├─→ annotation_subscriptions (1:N)
    └─→ object_mandant (1:N)
```

### Collaboration & Annotation Relationships

```
collaboration_annotations
    ├─→ objects (N:1)
    ├─→ users (N:1) [created by]
    ├─→ users (N:1) [updated by]
    ├─→ users (N:1) [assigned to]
    ├─→ collaboration_annotations (N:1) [parent - self-reference]
    ├─→ collaboration_annotations (1:N) [replies]
    └─→ annotation_reactions (1:N)

annotation_reactions
    ├─→ collaboration_annotations (N:1)
    └─→ users (N:1)

annotation_subscriptions
    ├─→ users (N:1)
    └─→ objects (N:1)
```

### Automation (Agents) Relationships

```
agents
    ├─→ users (N:1) [created by]
    ├─→ mandants (N:1)
    └─→ agent_logs (1:N)

agent_logs
    └─→ agents (N:1) [CASCADE delete]
```

### Maintenance & Tasks Relationships

```
logbook_entries
    ├─→ objects (N:1)
    ├─→ users (N:1) [created by]
    ├─→ users (N:1) [updated by]
    └─→ todo_tasks (1:N)

todo_tasks
    ├─→ objects (N:1)
    └─→ logbook_entries (N:1)
```

---

## Detailed Foreign Key Relationships

### 1. User Management Relationships

#### users → mandants
- **Column:** `users.mandantId`
- **References:** `mandants.id`
- **Type:** Many-to-One
- **Purpose:** Default tenant assignment for user
- **Cascade:** Not specified

#### users → user_profiles
- **Column:** `users.userProfileId`
- **References:** `user_profiles.id`
- **Type:** Many-to-One
- **Purpose:** User access profile and permissions
- **Cascade:** Not specified

#### user_activity_logs → users
- **Column:** `user_activity_logs.userId`
- **References:** `users.id`
- **Type:** Many-to-One
- **Purpose:** Track user actions
- **Cascade:** Not specified

---

### 2. Tenant (Mandant) Relationships

#### objects → mandants
- **Column:** `objects.mandantId`
- **References:** `mandants.id`
- **Type:** Many-to-One
- **Purpose:** Primary tenant ownership of object
- **Cascade:** Not specified

#### object_mandant → mandants
- **Column:** `object_mandant.mandantId`
- **References:** `mandants.id`
- **Type:** Many-to-One
- **Purpose:** Additional tenant access to objects
- **Cascade:** Not specified

#### settings → mandants
- **Column:** `settings.mandant_id`
- **References:** `mandants.id`
- **Type:** Many-to-One
- **Purpose:** Tenant-specific settings
- **Cascade:** Not specified

#### agents → mandants
- **Column:** `agents.mandantId`
- **References:** `mandants.id`
- **Type:** Many-to-One
- **Purpose:** Agent ownership by tenant
- **Cascade:** Not specified

---

### 3. Object Relationships

#### object_mandant → objects
- **Column:** `object_mandant.objectId`
- **References:** `objects.objectid`
- **Type:** Many-to-One
- **Purpose:** Object-tenant association
- **Cascade:** Not specified
- **Note:** Unique constraint on objectId

#### system_alerts → objects
- **Column:** `system_alerts.objectId`
- **References:** `objects.objectid`
- **Type:** Many-to-One
- **Purpose:** Alerts associated with objects
- **Cascade:** Not specified

#### day_comp → objects
- **Column:** `day_comp.log`
- **References:** `objects.objectid`
- **Type:** Many-to-One
- **Purpose:** Daily energy data for objects
- **Cascade:** Not specified

#### logbook_entries → objects
- **Column:** `logbook_entries.objectId`
- **References:** `objects.objectid`
- **Type:** Many-to-One
- **Purpose:** Maintenance records for objects
- **Cascade:** Not specified

#### todo_tasks → objects
- **Column:** `todo_tasks.objectId`
- **References:** `objects.objectid`
- **Type:** Many-to-One
- **Purpose:** Tasks associated with objects
- **Cascade:** Not specified

#### collaboration_annotations → objects
- **Column:** `collaboration_annotations.objectId`
- **References:** `objects.objectid`
- **Type:** Many-to-One
- **Purpose:** Annotations for object monitoring
- **Cascade:** Not specified

#### annotation_subscriptions → objects
- **Column:** `annotation_subscriptions.objectId`
- **References:** `objects.objectid`
- **Type:** Many-to-One
- **Purpose:** Subscribe to object annotations
- **Cascade:** Not specified

---

### 4. Settings Relationships

#### settings → users
- **Column:** `settings.user_id`
- **References:** `users.id`
- **Type:** Many-to-One
- **Purpose:** User-specific settings
- **Cascade:** Not specified

---

### 5. Alert Relationships

#### system_alerts → users (resolved by)
- **Column:** `system_alerts.resolvedBy`
- **References:** `users.id`
- **Type:** Many-to-One
- **Purpose:** Track who resolved the alert
- **Cascade:** Not specified

---

### 6. Maintenance & Task Relationships

#### logbook_entries → users (created by)
- **Column:** `logbook_entries.createdBy`
- **References:** `users.id`
- **Type:** Many-to-One
- **Purpose:** Track entry creator
- **Cascade:** Not specified

#### logbook_entries → users (updated by)
- **Column:** `logbook_entries.updatedBy`
- **References:** `users.id`
- **Type:** Many-to-One
- **Purpose:** Track entry updater
- **Cascade:** Not specified

#### todo_tasks → logbook_entries
- **Column:** `todo_tasks.logbookEntryId`
- **References:** `logbook_entries.id`
- **Type:** Many-to-One
- **Purpose:** Link tasks to logbook entries
- **Cascade:** Not specified

---

### 7. Collaboration Annotation Relationships

#### collaboration_annotations → users (created by)
- **Column:** `collaboration_annotations.createdBy`
- **References:** `users.id`
- **Type:** Many-to-One
- **Purpose:** Track annotation creator
- **Cascade:** Not specified
- **Relation Name:** "createdBy"

#### collaboration_annotations → users (updated by)
- **Column:** `collaboration_annotations.updatedBy`
- **References:** `users.id`
- **Type:** Many-to-One
- **Purpose:** Track annotation updater
- **Cascade:** Not specified
- **Relation Name:** "updatedBy"

#### collaboration_annotations → users (assigned to)
- **Column:** `collaboration_annotations.assignedTo`
- **References:** `users.id`
- **Type:** Many-to-One
- **Purpose:** Assign annotation to team member
- **Cascade:** Not specified
- **Relation Name:** "assignedTo"

#### collaboration_annotations → collaboration_annotations (self-reference)
- **Column:** `collaboration_annotations.parentId`
- **References:** `collaboration_annotations.id`
- **Type:** Many-to-One (Self)
- **Purpose:** Threading/replies on annotations
- **Cascade:** Not specified
- **Relation Name:** "parent"

#### annotation_reactions → collaboration_annotations
- **Column:** `annotation_reactions.annotationId`
- **References:** `collaboration_annotations.id`
- **Type:** Many-to-One
- **Purpose:** Reactions to annotations
- **Cascade:** Not specified

#### annotation_reactions → users
- **Column:** `annotation_reactions.userId`
- **References:** `users.id`
- **Type:** Many-to-One
- **Purpose:** User who reacted
- **Cascade:** Not specified

#### annotation_subscriptions → users
- **Column:** `annotation_subscriptions.userId`
- **References:** `users.id`
- **Type:** Many-to-One
- **Purpose:** User subscription
- **Cascade:** Not specified

---

### 8. Agent & Automation Relationships

#### agents → users (created by)
- **Column:** `agents.createdBy`
- **References:** `users.id`
- **Type:** Many-to-One
- **Purpose:** Track agent creator
- **Cascade:** Not specified

#### agent_logs → agents
- **Column:** `agent_logs.agentId`
- **References:** `agents.id`
- **Type:** Many-to-One
- **Purpose:** Execution logs for agents
- **Cascade:** CASCADE (logs deleted when agent is deleted)

---

## Relationship Cardinality Summary

### One-to-Many Relationships (1:N)
- `mandants` → `users` (tenant has many users)
- `mandants` → `objects` (tenant has many objects)
- `mandants` → `settings` (tenant has many settings)
- `mandants` → `agents` (tenant has many agents)
- `user_profiles` → `users` (profile assigned to many users)
- `users` → `settings` (user has many settings)
- `users` → `agents` (user creates many agents)
- `users` → `collaboration_annotations` (user creates/updates/assigned many annotations)
- `users` → `annotation_reactions` (user has many reactions)
- `users` → `annotation_subscriptions` (user has many subscriptions)
- `users` → `logbook_entries` (user creates/updates many entries)
- `users` → `system_alerts` (user resolves many alerts)
- `users` → `user_activity_logs` (user has many activity logs)
- `objects` → `system_alerts` (object has many alerts)
- `objects` → `day_comp` (object has many daily records)
- `objects` → `view_mon_comp` (object has many monthly records)
- `objects` → `logbook_entries` (object has many logbook entries)
- `objects` → `todo_tasks` (object has many tasks)
- `objects` → `collaboration_annotations` (object has many annotations)
- `objects` → `annotation_subscriptions` (object has many subscriptions)
- `objects` → `object_mandant` (object has many tenant associations)
- `logbook_entries` → `todo_tasks` (entry has many tasks)
- `collaboration_annotations` → `annotation_reactions` (annotation has many reactions)
- `collaboration_annotations` → `collaboration_annotations` (annotation has many replies)
- `agents` → `agent_logs` (agent has many logs)

### Many-to-One Relationships (N:1)
- All the inverse of the 1:N relationships above

### Many-to-Many Relationships (N:M)
- `objects` ↔ `mandants` (via `object_mandant` junction table)
  - **Note:** This is redundant with `objects.mandantAccess` JSONB field
- `users` ↔ `mandants` (implicit via `users.mandantAccess` JSONB field)

### Self-Referencing Relationships
- `collaboration_annotations.parentId` → `collaboration_annotations.id` (threading/replies)

---

## Cascade Delete Behavior

### Explicit CASCADE
- `agent_logs.agentId` → `agents.id` (CASCADE)
  - When an agent is deleted, all its execution logs are automatically deleted

### No Explicit CASCADE (Default RESTRICT)
All other foreign keys use the default PostgreSQL behavior (RESTRICT), meaning:
- Cannot delete a referenced record if dependent records exist
- Must manually delete dependent records first
- Prevents accidental data loss

---

## Data Isolation Strategy

### Tenant (Mandant) Isolation

**Primary Method:**
- `objects.mandantId`: Primary tenant ownership
- `users.mandantId`: User's default tenant

**Secondary Method:**
- `objects.mandantAccess`: JSONB array of tenant IDs with access
- `users.mandantAccess`: JSONB array of tenant IDs user can access

**Junction Table (Deprecated):**
- `object_mandant`: Traditional many-to-many table (marked as redundant)

### Access Control Flow

1. **User Login:** User has `mandantId` (default) and `mandantAccess` array
2. **Object Query:** Filter by `objects.mandantId IN user.mandantAccess` OR check `objects.mandantAccess` JSONB
3. **Data Isolation:** All queries respect tenant boundaries via filters

---

## Relationship Integrity

### Orphan Prevention
The lack of CASCADE deletes on most relationships prevents orphaned records and ensures data integrity.

### Reference Integrity
All foreign keys are enforced at the database level via PostgreSQL constraints.

### Soft vs Hard Deletes
No explicit soft delete pattern is implemented in the schema. All deletes are hard deletes, except for:
- Alerts: `isResolved` flag instead of deletion
- Annotations: `status` field (active, resolved, archived)
- Tasks: `status` field and `completedAt` timestamp

---

## Relationship Notes

### User Profile System
- Multiple users can share the same `user_profile`
- Profiles define sidebar permissions and default landing pages
- Profiles are independent entities, not embedded in user records

### Object-Tenant Association
- Objects have a primary tenant (`mandantId`)
- Objects can be shared with multiple tenants via `mandantAccess` JSONB
- `object_mandant` table exists but is marked as redundant

### Annotation Threading
- Annotations support nested replies via `parentId` self-reference
- No depth limit enforced at database level
- Threading enables discussion-style collaboration

### Agent Cascade
- Only relationship with explicit CASCADE behavior
- Agent logs are considered ephemeral and tied to agent lifecycle
- Deleting an agent removes all execution history
