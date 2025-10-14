# Database Schema Tables

Created: 2025-10-13

## Table Organization

Tables are organized by functional domain:
1. Authentication & Sessions
2. User Management
3. Tenant Management (Mandants)
4. Object Management
5. Energy & Temperature Data
6. Maintenance & Tasks
7. System Configuration
8. Collaboration Features
9. Automation (Agents)
10. Activity Logging

---

## 1. Authentication & Sessions

### sessions
**Purpose:** Store user session data for session-based authentication

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| sid | VARCHAR | No | - | Session ID (Primary Key) |
| sess | JSONB | No | - | Session data |
| expire | TIMESTAMP | No | - | Session expiration timestamp |

**Indexes:**
- `IDX_session_expire` on `expire`

---

## 2. User Management

### users
**Purpose:** Central user management with authentication and authorization

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | VARCHAR | No | - | User ID (Primary Key) |
| username | VARCHAR(255) | Yes | - | Unique username |
| email | VARCHAR(255) | Yes | - | Unique email address |
| password | VARCHAR(255) | Yes | - | Hashed password |
| role | VARCHAR(50) | Yes | 'user' | User role |
| mandantId | INTEGER | Yes | 1 | Default tenant ID (FK to mandants) |
| firstName | VARCHAR(255) | Yes | - | First name |
| lastName | VARCHAR(255) | Yes | - | Last name |
| profileImageUrl | VARCHAR | Yes | - | Profile image URL |
| userProfileId | INTEGER | Yes | - | User profile ID (FK to user_profiles) |
| address | JSONB | Yes | - | Address information |
| mandantAccess | JSONB | Yes | [] | List of accessible tenant IDs |
| createdAt | TIMESTAMP | Yes | NOW() | Creation timestamp |
| updatedAt | TIMESTAMP | Yes | NOW() | Last update timestamp |

**Unique Constraints:**
- `username` (unique)
- `email` (unique)

### user_profiles
**Purpose:** Define user access profiles with sidebar permissions

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | SERIAL | No | - | Profile ID (Primary Key) |
| name | VARCHAR(255) | No | - | Profile name (unique) |
| startPage | VARCHAR(100) | Yes | '/maps' | Default landing page |
| sidebar | JSONB | Yes | {} | Sidebar access permissions object |
| createdAt | TIMESTAMP | Yes | NOW() | Creation timestamp |
| updatedAt | TIMESTAMP | Yes | NOW() | Last update timestamp |

**Unique Constraints:**
- `name` (unique)

**Sidebar Permissions Structure (JSONB):**
```typescript
{
  showDashboard?: boolean;
  showMaps?: boolean;
  showNetworkMonitor?: boolean;
  showEfficiencyStrategy?: boolean;
  showObjectManagement?: boolean;
  showLogbook?: boolean;
  showGrafanaDashboards?: boolean;
  showEnergyData?: boolean;
  showSystemSetup?: boolean;
  showUserManagement?: boolean;
  showUser?: boolean;
  showEfficiencyModule?: boolean;
}
```

### user_activity_logs
**Purpose:** Track user actions for audit trail and security monitoring

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | SERIAL | No | - | Log ID (Primary Key) |
| userId | VARCHAR | Yes | - | User ID (FK to users) |
| action | VARCHAR(100) | No | - | Action type (login, logout, created_object, etc.) |
| resourceType | VARCHAR(50) | Yes | - | Resource type (object, user, mandant, etc.) |
| resourceId | VARCHAR(50) | Yes | - | Resource ID |
| details | JSONB | Yes | - | Additional action details |
| ipAddress | VARCHAR(45) | Yes | - | IPv4/IPv6 address |
| userAgent | TEXT | Yes | - | User agent string |
| timestamp | TIMESTAMP | No | NOW() | Action timestamp |

**Indexes:**
- `idx_user_activity_logs_user_id` on `userId`
- `idx_user_activity_logs_action` on `action`
- `idx_user_activity_logs_timestamp` on `timestamp`
- `idx_user_activity_logs_resource` on `(resourceType, resourceId)`

---

## 3. Tenant Management (Mandants)

### mandants
**Purpose:** Multi-tenant organization/client management

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | SERIAL | No | - | Mandant ID (Primary Key) |
| name | VARCHAR(100) | No | - | Mandant name |
| description | TEXT | Yes | - | Description |
| category | VARCHAR(100) | Yes | - | Category/classification |
| info | JSONB | Yes | {} | Contact and address information |
| createdAt | TIMESTAMP | Yes | NOW() | Creation timestamp |

**Info Structure (JSONB):**
```typescript
{
  adresse?: {
    strasse?: string;
    hausnummer?: string;
    plz?: string;
    ort?: string;
    land?: string;
  };
  kontakt?: {
    email?: string;
    telefon?: string;
    mobil?: string;
    website?: string;
  };
}
```

---

## 4. Object Management

### objects
**Purpose:** Central object/asset management with comprehensive monitoring data

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | SERIAL | No | - | Internal ID (Primary Key) |
| objectid | BIGINT | No | - | Object identifier (unique, indexed) |
| name | VARCHAR(255) | Yes | - | Object name |
| objectType | VARCHAR(50) | Yes | - | Object type classification |
| status | VARCHAR(50) | Yes | 'active' | Object status |
| postalCode | VARCHAR(10) | Yes | - | Postal code |
| city | VARCHAR(100) | Yes | - | City name |
| country | VARCHAR(100) | Yes | 'Deutschland' | Country |
| latitude | DECIMAL(10,8) | Yes | - | Latitude coordinate |
| longitude | DECIMAL(11,8) | Yes | - | Longitude coordinate |
| description | TEXT | Yes | - | Description |
| objdata | JSONB | Yes | - | Object data |
| objanlage | JSONB | Yes | - | Facility/installation data |
| portdata | JSONB | Yes | - | Port/interface data |
| meter | JSONB | Yes | - | Meter data |
| dashboard | JSONB | Yes | - | Dashboard configuration |
| alarm | JSONB | Yes | - | Alarm data |
| kianalyse | JSONB | Yes | - | AI analysis data |
| statusdata | JSONB | Yes | - | Status data |
| auswertung | JSONB | Yes | - | Evaluation data |
| report | JSONB | Yes | - | Report data |
| diagramm | JSONB | Yes | - | Diagram data |
| fltemp | JSONB | Yes | - | Flow temperature data |
| rttemp | JSONB | Yes | - | Return temperature data |
| energy | JSONB | Yes | - | Energy data |
| temperaturGrenzwert | VARCHAR(50) | Yes | - | Temperature threshold |
| mandantAccess | JSONB | Yes | [] | Tenant access list |
| mandantId | INTEGER | Yes | - | Primary tenant ID (FK to mandants) |
| createdAt | TIMESTAMP | Yes | NOW() | Creation timestamp |
| updatedAt | TIMESTAMP | Yes | NOW() | Last update timestamp |

**Indexes:**
- `idx_objects_objectid` on `objectid`
- `idx_objects_mandant_id` on `mandantId`
- `idx_objects_type` on `objectType`
- `idx_objects_status` on `status`
- `idx_objects_city` on `city`
- `idx_objects_postal_code` on `postalCode`

**Unique Constraints:**
- `objectid` (unique)

### object_mandant
**Purpose:** Many-to-many relationship between objects and tenants (NOTE: Marked as redundant, superseded by objects.mandantAccess)

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | SERIAL | No | - | Record ID (Primary Key) |
| objectId | BIGINT | No | - | Object ID (FK to objects.objectid, unique) |
| mandantId | INTEGER | No | - | Mandant ID (FK to mandants) |
| mandantRole | VARCHAR(255) | Yes | - | Mandant role for this object |
| createdAt | TIMESTAMP | Yes | NOW() | Creation timestamp |
| updatedAt | TIMESTAMP | Yes | NOW() | Last update timestamp |

**Indexes:**
- `idx_object_mandant_objectid` on `objectId`
- `idx_object_mandant_mandant_id` on `mandantId`

**Unique Constraints:**
- `objectId` (unique)

### object_groups
**Purpose:** Organize objects into logical groups

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | SERIAL | No | - | Group ID (Primary Key) |
| name | VARCHAR(255) | No | - | Group name |
| description | TEXT | Yes | - | Group description |
| type | VARCHAR(100) | No | 'standard' | Group type |
| createdAt | TIMESTAMP | Yes | NOW() | Creation timestamp |
| updatedAt | TIMESTAMP | Yes | NOW() | Last update timestamp |

### system_alerts
**Purpose:** System-wide alerts and alarms for objects

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | SERIAL | No | - | Alert ID (Primary Key) |
| alertType | VARCHAR(255) | Yes | - | Alert type classification |
| message | TEXT | No | - | Alert message |
| objectId | BIGINT | Yes | - | Associated object ID (FK to objects.objectid) |
| isResolved | BOOLEAN | No | false | Resolution status |
| resolvedAt | TIMESTAMP | Yes | - | Resolution timestamp |
| resolvedBy | VARCHAR | Yes | - | User who resolved (FK to users.id) |
| createdAt | TIMESTAMP | Yes | NOW() | Creation timestamp |

---

## 5. Energy & Temperature Data

### day_comp
**Purpose:** Daily energy consumption and temperature aggregation data

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| counter | SERIAL | No | - | Record counter (Primary Key) |
| time | TIMESTAMP | No | - | Timestamp of record |
| id | BIGINT | No | - | Record ID |
| log | BIGINT | No | - | Object ID reference (FK to objects.objectid) |
| tpl | TEXT | Yes | - | Template identifier |
| enFirst | DOUBLE PRECISION | Yes | - | Energy meter start of day |
| enLast | DOUBLE PRECISION | Yes | - | Energy meter end of day |
| en2First | DOUBLE PRECISION | Yes | - | Secondary energy meter start |
| en2Last | DOUBLE PRECISION | Yes | - | Secondary energy meter end |
| volFirst | DOUBLE PRECISION | Yes | - | Volume meter start of day |
| volLast | DOUBLE PRECISION | Yes | - | Volume meter end of day |
| fltMean | REAL | Yes | - | Average flow temperature |
| retMean | REAL | Yes | - | Average return temperature |
| fltMax | REAL | Yes | - | Maximum flow temperature |
| retMax | REAL | Yes | - | Maximum return temperature |
| fltMin | REAL | Yes | - | Minimum flow temperature |
| retMin | REAL | Yes | - | Minimum return temperature |
| floMean | REAL | Yes | - | Average flow rate |
| floMax | REAL | Yes | - | Maximum flow rate |
| floMin | REAL | Yes | - | Minimum flow rate |
| powMean | REAL | Yes | - | Average power |
| powMax | REAL | Yes | - | Maximum power |
| powMin | REAL | Yes | - | Minimum power |
| wrkFirst | REAL | Yes | - | Work field |

**Indexes:**
- `idx_day_comp_time` on `time`
- `idx_day_comp_log` on `log`
- `idx_day_comp_time_log` on `(time, log)`

### view_mon_comp
**Purpose:** Monthly aggregated energy data (PostgreSQL View)

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| counter | SERIAL | No | - | Row number (Primary Key) |
| time | TIMESTAMP | No | - | Month date |
| id | BIGINT | No | - | Record ID |
| log | BIGINT | No | - | Log reference |
| objectId | BIGINT | No | - | Object ID (converted from log) |
| tpl | BIGINT | Yes | - | Template ID |
| enFirst | DOUBLE PRECISION | Yes | - | Energy meter month start |
| enLast | DOUBLE PRECISION | Yes | - | Energy meter month end |
| diffEn | DOUBLE PRECISION | Yes | - | Monthly energy difference |
| diffVol | DOUBLE PRECISION | Yes | - | Monthly volume difference |

### daily_outdoor_temperatures
**Purpose:** Daily outdoor temperature data by postal code (German energy monitoring standards)

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | SERIAL | No | - | Record ID (Primary Key) |
| date | DATE | No | - | Measurement date |
| postalCode | VARCHAR(10) | No | - | Postal code |
| city | VARCHAR(100) | Yes | - | City name |
| temperatureMin | DECIMAL(4,1) | Yes | - | Daily minimum temperature (Celsius) |
| temperatureMax | DECIMAL(4,1) | Yes | - | Daily maximum temperature (Celsius) |
| temperatureMean | DECIMAL(4,1) | Yes | - | Daily average temperature (Celsius) |
| dataSource | VARCHAR(100) | Yes | 'DWD (Bright Sky)' | Data source |
| dataQuality | VARCHAR(20) | Yes | 'good' | Data quality indicator |
| createdAt | TIMESTAMP | Yes | NOW() | Creation timestamp |
| updatedAt | TIMESTAMP | Yes | NOW() | Last update timestamp |

**Indexes:**
- `idx_daily_temp_date` on `date`
- `idx_daily_temp_postal_code` on `postalCode`
- `idx_daily_temp_date_postal_code` on `(date, postalCode)`
- `idx_daily_temp_city` on `city`

**Standards Compliance:** GEG 2024, DIN V 18599, VDI 3807 for heating degree day calculations

---

## 6. Maintenance & Tasks

### logbook_entries
**Purpose:** Maintenance logbook for tracking work performed on objects

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | SERIAL | No | - | Entry ID (Primary Key) |
| objectId | BIGINT | Yes | - | Object ID (FK to objects.objectid) |
| entryType | VARCHAR(255) | Yes | - | Entry type |
| category | VARCHAR(255) | Yes | - | Category |
| priority | VARCHAR(255) | Yes | - | Priority level |
| title | VARCHAR(255) | No | - | Entry title |
| description | TEXT | Yes | - | Detailed description |
| status | VARCHAR(255) | Yes | 'offen' | Status |
| technicianName | VARCHAR(100) | Yes | - | Technician name |
| technicianCompany | VARCHAR(100) | Yes | - | Technician company |
| technicianContact | VARCHAR(100) | Yes | - | Technician contact |
| scheduledDate | DATE | Yes | - | Scheduled date |
| startTime | TIMESTAMP | Yes | - | Work start time |
| endTime | TIMESTAMP | Yes | - | Work end time |
| workHours | DECIMAL(4,2) | Yes | - | Total work hours |
| materialCost | DECIMAL(10,2) | Yes | - | Material cost |
| laborCost | DECIMAL(10,2) | Yes | - | Labor cost |
| totalCost | DECIMAL(10,2) | Yes | - | Total cost |
| attachments | JSONB | Yes | - | File attachments array |
| relatedAlarmId | INTEGER | Yes | - | Related alarm ID |
| followUpRequired | BOOLEAN | Yes | false | Follow-up required flag |
| followUpDate | DATE | Yes | - | Follow-up date |
| createdBy | VARCHAR | Yes | - | Creator user ID (FK to users.id) |
| updatedBy | VARCHAR | Yes | - | Last updater user ID (FK to users.id) |
| createdAt | TIMESTAMP | Yes | NOW() | Creation timestamp |
| updatedAt | TIMESTAMP | Yes | NOW() | Last update timestamp |

**Indexes:**
- `idx_logbook_entries_object_id` on `objectId`
- `idx_logbook_entries_status` on `status`
- `idx_logbook_entries_scheduled_date` on `scheduledDate`

**Attachments Structure (JSONB):**
```typescript
[
  {
    filename: string;
    url: string;
    type: string;
    size: number;
  }
]
```

### todo_tasks
**Purpose:** Task management system linked to objects and logbook entries

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | SERIAL | No | - | Task ID (Primary Key) |
| objectId | BIGINT | Yes | - | Object ID (FK to objects.objectid) |
| logbookEntryId | INTEGER | Yes | - | Logbook entry ID (FK to logbook_entries) |
| title | VARCHAR(255) | No | - | Task title |
| description | TEXT | Yes | - | Task description |
| dueDate | DATE | Yes | - | Due date |
| priority | VARCHAR(255) | Yes | - | Priority level |
| assignedTo | VARCHAR(255) | Yes | - | Assigned user |
| status | VARCHAR(255) | Yes | 'offen' | Task status |
| completedAt | TIMESTAMP | Yes | - | Completion timestamp |
| completedBy | VARCHAR(100) | Yes | - | User who completed |
| createdAt | TIMESTAMP | Yes | NOW() | Creation timestamp |

**Indexes:**
- `idx_todo_tasks_object_id` on `objectId`
- `idx_todo_tasks_status` on `status`
- `idx_todo_tasks_due_date` on `dueDate`

---

## 7. System Configuration

### settings
**Purpose:** System-wide, tenant-specific, and user-specific configuration settings

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | SERIAL | No | - | Setting ID (Primary Key) |
| category | VARCHAR(100) | No | - | Setting category |
| key_name | VARCHAR(255) | No | - | Setting key name |
| value | JSONB | No | - | Setting value (flexible JSONB) |
| user_id | VARCHAR | Yes | - | User-specific setting (FK to users.id) |
| mandant_id | INTEGER | Yes | - | Mandant-specific setting (FK to mandants.id) |
| createdAt | TIMESTAMP | Yes | NOW() | Creation timestamp |
| updatedAt | TIMESTAMP | Yes | NOW() | Last update timestamp |

**Indexes:**
- `idx_settings_category` on `category`
- `idx_settings_key_name` on `key_name`
- `idx_settings_user_id` on `user_id`
- `idx_settings_mandant_id` on `mandant_id`

---

## 8. Collaboration Features

### collaboration_annotations
**Purpose:** Real-time team monitoring annotations and comments

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | SERIAL | No | - | Annotation ID (Primary Key) |
| objectId | BIGINT | Yes | - | Object ID (FK to objects.objectid) |
| contextType | VARCHAR(50) | No | - | Context type (temperature, energy, alarm, etc.) |
| contextId | VARCHAR(255) | Yes | - | Specific context identifier |
| title | VARCHAR(255) | No | - | Annotation title |
| content | TEXT | No | - | Annotation content |
| type | VARCHAR(50) | No | - | Type (note, warning, observation, etc.) |
| priority | VARCHAR(20) | Yes | 'normal' | Priority level |
| position | JSONB | Yes | - | Visual positioning for dashboards |
| timeRange | JSONB | Yes | - | Time range for time-specific annotations |
| isTemporary | BOOLEAN | Yes | false | Auto-expire flag |
| expiresAt | TIMESTAMP | Yes | - | Expiration timestamp |
| tags | JSONB | Yes | - | Categorization tags array |
| assignedTo | VARCHAR | Yes | - | Assigned user (FK to users.id) |
| status | VARCHAR(50) | Yes | 'active' | Status (active, resolved, archived) |
| parentId | INTEGER | Yes | - | Parent annotation for threading (self-reference) |
| createdBy | VARCHAR | No | - | Creator user ID (FK to users.id) |
| updatedBy | VARCHAR | Yes | - | Last updater user ID (FK to users.id) |
| createdAt | TIMESTAMP | Yes | NOW() | Creation timestamp |
| updatedAt | TIMESTAMP | Yes | NOW() | Last update timestamp |

**Indexes:**
- `idx_annotations_object_id` on `objectId`
- `idx_annotations_context` on `(contextType, contextId)`
- `idx_annotations_created_by` on `createdBy`
- `idx_annotations_status` on `status`
- `idx_annotations_type` on `type`
- `idx_annotations_parent_id` on `parentId`

**Position Structure (JSONB):**
```typescript
{
  x: number;
  y: number;
  width?: number;
  height?: number;
}
```

**Time Range Structure (JSONB):**
```typescript
{
  start: timestamp;
  end: timestamp;
}
```

### annotation_reactions
**Purpose:** Team engagement with annotations through reactions

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | SERIAL | No | - | Reaction ID (Primary Key) |
| annotationId | INTEGER | No | - | Annotation ID (FK to collaboration_annotations) |
| userId | VARCHAR | No | - | User ID (FK to users.id) |
| reactionType | VARCHAR(50) | No | - | Reaction type (like, agree, disagree, etc.) |
| createdAt | TIMESTAMP | Yes | NOW() | Creation timestamp |

**Indexes:**
- `idx_reactions_annotation_id` on `annotationId`
- `idx_reactions_user_id` on `userId`

### annotation_subscriptions
**Purpose:** Real-time notification subscriptions for annotations

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | SERIAL | No | - | Subscription ID (Primary Key) |
| userId | VARCHAR | No | - | User ID (FK to users.id) |
| objectId | BIGINT | Yes | - | Object ID (FK to objects.objectid) |
| contextType | VARCHAR(50) | Yes | - | Context type filter |
| isEnabled | BOOLEAN | Yes | true | Subscription enabled flag |
| notificationMethods | JSONB | Yes | {} | Notification method preferences |
| createdAt | TIMESTAMP | Yes | NOW() | Creation timestamp |

**Indexes:**
- `idx_subscriptions_user_id` on `userId`
- `idx_subscriptions_object_id` on `objectId`

**Notification Methods Structure (JSONB):**
```typescript
{
  inApp?: boolean;
  email?: boolean;
  realTime?: boolean;
}
```

---

## 9. Automation (Agents)

### agents
**Purpose:** Automated data collection and processing agents

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | SERIAL | No | - | Agent ID (Primary Key) |
| name | VARCHAR(255) | No | - | Agent name |
| description | TEXT | Yes | - | Agent description |
| configTriggerSchema | JSONB | No | - | Trigger configuration |
| configSourceSchema | JSONB | No | - | Source configuration |
| configProcessingSchema | JSONB | Yes | - | Processing configuration |
| configTargetSchema | JSONB | No | - | Target configuration |
| status | VARCHAR(50) | Yes | 'active' | Agent status |
| lastRun | TIMESTAMP | Yes | - | Last execution timestamp |
| nextRun | TIMESTAMP | Yes | - | Next scheduled execution |
| runCount | INTEGER | Yes | 0 | Total run count |
| errorCount | INTEGER | Yes | 0 | Total error count |
| lastError | TEXT | Yes | - | Last error message |
| createdBy | VARCHAR | Yes | - | Creator user ID (FK to users.id) |
| mandantId | INTEGER | Yes | - | Mandant ID (FK to mandants.id) |
| createdAt | TIMESTAMP | Yes | NOW() | Creation timestamp |
| updatedAt | TIMESTAMP | Yes | NOW() | Last update timestamp |

**Indexes:**
- `idx_agents_status` on `status`
- `idx_agents_next_run` on `nextRun`
- `idx_agents_mandant_id` on `mandantId`

**Configuration Schemas:**

**Trigger Config (JSONB):**
```typescript
{
  type: "interval" | "schedule" | "manual";
  interval?: number; // minutes
  schedule?: string; // cron expression
}
```

**Source Config (JSONB):**
```typescript
{
  type: "api" | "database" | "file" | "influxdb2" | "mqtt";
  // API source
  endpoint?: string;
  method?: "GET" | "POST" | "PUT";
  headers?: Record<string, string>;
  // Database source
  query?: string;
  tableName?: string;
  // File source
  filePath?: string;
  // InfluxDB2 source
  connection?: {
    url: string;
    token: string;
    org: string;
    bucket?: string;
  };
  flux?: string;
  parameters?: Record<string, any>;
  // MQTT source
  broker?: string;
  clientId?: string;
  username?: string;
  password?: string;
  topics?: string[];
  qos?: number;
  collection?: {
    duration: number;
    maxMessages?: number;
    bufferTime?: number;
  };
}
```

**Processing Config (JSONB):**
```typescript
{
  functions?: Array<{
    type: "map" | "filter" | "aggregate" | "calculate";
    field?: string;
    expression?: string;
    condition?: string;
  }>;
  mappings?: Record<string, any>;
}
```

**Target Config (JSONB):**
```typescript
{
  type: "database" | "api" | "file";
  tableName?: string;
  field?: string;
  fields?: Record<string, string>;
  endpoint?: string;
  method?: "POST" | "PUT" | "PATCH";
  filePath?: string;
}
```

### agent_logs
**Purpose:** Execution logs for agent runs

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | SERIAL | No | - | Log ID (Primary Key) |
| agentId | INTEGER | No | - | Agent ID (FK to agents, CASCADE delete) |
| startTime | TIMESTAMP | No | - | Execution start time |
| endTime | TIMESTAMP | Yes | - | Execution end time |
| status | VARCHAR(50) | No | - | Execution status (running, success, error) |
| sourceData | JSONB | Yes | - | Input data from source |
| processedData | JSONB | Yes | - | Data after processing |
| targetData | JSONB | Yes | - | Data written to target |
| recordsProcessed | INTEGER | Yes | 0 | Records processed count |
| recordsCreated | INTEGER | Yes | 0 | Records created count |
| recordsUpdated | INTEGER | Yes | 0 | Records updated count |
| recordsErrors | INTEGER | Yes | 0 | Records with errors count |
| errorMessage | TEXT | Yes | - | Error message |
| executionTimeMs | INTEGER | Yes | - | Execution time in milliseconds |
| createdAt | TIMESTAMP | Yes | NOW() | Creation timestamp |

**Indexes:**
- `idx_agent_logs_agent_id` on `agentId`
- `idx_agent_logs_start_time` on `startTime`
- `idx_agent_logs_status` on `status`

---

## Summary Statistics

**Total Tables:** 21 tables (20 data tables + 1 view)

**Table Count by Domain:**
- Authentication & Sessions: 1
- User Management: 3
- Tenant Management: 1
- Object Management: 4
- Energy & Temperature Data: 3
- Maintenance & Tasks: 2
- System Configuration: 1
- Collaboration Features: 3
- Automation: 2
- Activity Logging: 1

**Total Indexes:** 68+ indexes across all tables
**Total JSONB Columns:** 35+ flexible schema fields
**Foreign Key Relationships:** 30+ relationships
