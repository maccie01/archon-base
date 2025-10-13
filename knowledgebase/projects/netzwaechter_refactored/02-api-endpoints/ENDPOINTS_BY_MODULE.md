# API Endpoints by Module

Created: 2025-10-13
Timestamp: 16:45:00

## Admin Module (`/api/admin`)

All routes require authentication. Most require admin/superadmin role.

### Database Status
- `GET /api/admin/database/status` - Get database connection status
  - Auth: Required
  - Returns: settingdbOnline, portalDbOnline, connection info

### Data Management
- `GET /api/admin/objects` - Get all objects (admin view)
  - Auth: Required (admin/superadmin)
  - Returns: Array of objects

- `GET /api/admin/mandants` - Get all mandants
  - Auth: Required
  - Returns: Array of mandants

- `GET /api/admin/settings` - Get all settings
  - Auth: Required
  - Query: `?category=string` (optional)
  - Returns: Array of settings

- `POST /api/admin/settings` - Save a setting
  - Auth: Required
  - Body: `{ category, keyName, value, userId, mandantId }`
  - Returns: Saved setting

- `GET /api/admin/dashboard/kpis` - Get dashboard KPIs
  - Auth: Required
  - Returns: criticalSystems, totalFacilities, totalMandants, activeUsers

### Portal Configuration
- `GET /api/admin/portal/config` - Get portal configuration
  - Auth: Required (admin/superadmin)
  - Returns: settingdb_app config (secure, no passwords)

- `GET /api/admin/portal/fallback-config` - Get fallback database config
  - Auth: Required (admin/superadmin)
  - Returns: Fallback config from setup-app.json

- `POST /api/admin/portal/save-fallback-config` - Save fallback config
  - Auth: Required (admin/superadmin)
  - Body: Fallback database configuration
  - Returns: Success message

- `POST /api/admin/portal/test-connection` - Test database connection
  - Auth: Required (admin/superadmin)
  - Body: `{ host, port, database, username, password, connectionTimeout }`
  - Returns: Connection test result

- `GET /api/admin/portal/load-config/:configType` - Load config by type
  - Auth: Required (admin/superadmin)
  - Path: configType (portal_database, settingdb, etc.)
  - Returns: Config data

- `POST /api/admin/portal/test-config/:configType` - Test config by type
  - Auth: Required (admin/superadmin)
  - Path: configType
  - Body: Config data to test
  - Returns: Test result

- `POST /api/admin/portal/save-config/:configType` - Save config by type
  - Auth: Required (admin/superadmin)
  - Path: configType
  - Body: Config data
  - Returns: Success message

- `POST /api/admin/portal/activate-config` - Activate portal config
  - Auth: Required (admin/superadmin)
  - Body: `{ configType }`
  - Returns: Activation result

- `GET /api/admin/portal/active-config` - Get active portal config
  - Auth: Required (admin/superadmin)
  - Returns: Active configuration info

## Auth Module (`/api/auth`)

Authentication endpoints with rate limiting.

- `POST /api/auth/superadmin-login` - Superadmin login
  - Auth: Public (rate limited: 5 per 15 min)
  - Body: `{ username, password }`
  - Returns: `{ message, user }`

- `POST /api/auth/login` - Standard user login
  - Auth: Public (rate limited: 5 per 15 min)
  - Body: `{ username, password }`
  - Returns: `{ message, user }`

- `GET /api/auth/me` - Get current user info
  - Auth: Required (session)
  - Returns: Complete user data with profile

- `POST /api/auth/logout` - Logout and destroy session
  - Auth: Required
  - Returns: `{ message }`

- `POST /api/auth/heartbeat` - Extend session
  - Auth: Required
  - Returns: `{ message, timestamp }`

## Database Module (`/api/database`)

- `GET /api/database/status` - Get database connection pool status
  - Auth: Not required (lightweight, UI polls this)
  - Returns: Connection pool statistics

## Efficiency Module (`/api/efficiency`, `/api`)

### Public Endpoints
- `GET /api/test-efficiency-analysis/:objectId` - Test efficiency analysis
  - Auth: Public
  - Path: objectId
  - Returns: Efficiency report

### Protected Endpoints
- `GET /api/efficiency/analysis/:objectId` - Get efficiency analysis
  - Auth: Required
  - Path: objectId
  - Returns: Efficiency report with recommendations

## Energy Module (`/api/energy`, `/api`)

### Public Endpoints
- `GET /api/public-daily-consumption/:objectId` - Public daily consumption
  - Auth: Public (for testing)
  - Path: objectId
  - Query: `?timeRange=last-365-days` (optional)
  - Returns: `{ success, data, source, message }`

- `GET /api/public-monthly-consumption/:objectId` - Public monthly consumption
  - Auth: Public (for testing)
  - Path: objectId
  - Query: `?timeRange=last-365-days` (optional)
  - Returns: `{ success, data, source, message }`

- `GET /api/monthly-netz/:objectId` - Monthly Netz meter data
  - Auth: Public
  - Path: objectId
  - Query: `?timeRange=last-365-days` (optional)
  - Returns: `{ success, data, source, message }`

### Day Comp Data
- `GET /api/energy/day-comp/:objectId` - Get day compensation data
  - Auth: Required
  - Path: objectId
  - Query: `?startDate=ISO&endDate=ISO` (optional)
  - Returns: Array of DayComp records

- `POST /api/energy/day-comp` - Create day compensation data
  - Auth: Required (admin/superadmin)
  - Body: `{ log, time, ... }`
  - Returns: Created DayComp record

- `GET /api/energy/day-comp/:objectId/latest` - Get latest day comp data
  - Auth: Required
  - Path: objectId
  - Returns: Latest DayComp record

### Daily Consumption
- `GET /api/energy/daily-consumption/:objectId` - Get daily consumption
  - Auth: Required
  - Path: objectId
  - Query: `?startDate=ISO&endDate=ISO` (optional)
  - Returns: Array of daily consumption data

- `GET /api/energy/daily-consumption-data/:objectId` - Daily consumption by meter
  - Auth: Required
  - Path: objectId
  - Query: `?timeRange=string` (required)
  - Returns: Object with consumption per meter

### External Energy Data
- `GET /api/energy/external/:objectId` - Get external energy data
  - Auth: Required
  - Path: objectId
  - Query: `?limit=12` (optional)
  - Returns: Array from view_mon_comp

- `GET /api/energy/all-meters/:objectId` - Energy data for all meters
  - Auth: Required
  - Path: objectId
  - Query: `?timeRange=string` (optional)
  - Body: `{ meterData }` (required)
  - Returns: Object with data per meter

- `GET /api/energy/specific-meter/:meterId/:objectId` - Specific meter data
  - Auth: Required
  - Path: meterId, objectId
  - Query: `?fromDate=ISO&toDate=ISO` (optional)
  - Returns: Array of meter readings

- `GET /api/energy/object/:objectId` - Energy data for object
  - Auth: Required
  - Path: objectId
  - Query: `?startDate=ISO&endDate=ISO&timeRange=string` (all optional)
  - Returns: Array of energy records

## Export Module (`/api/export`)

- `POST /api/export/send-email` - Send PDF export via email
  - Auth: Required (rate limited: 10 per hour)
  - Body: Email and PDF data
  - Returns: Success message

## Health Module (`/api/health`)

- `GET /api/health` - Comprehensive health check
  - Auth: Not required
  - Returns: `{ status, database, timestamp, version, pool }`

- `GET /api/health/pool` - Connection pool statistics
  - Auth: Not required
  - Returns: Pool stats and health metrics

- `GET /api/health/metrics` - Prometheus metrics
  - Auth: Not required
  - Returns: Plain text Prometheus format

## KI Reports Module (`/api/ki-reports`)

- `GET /api/ki-reports/yearly-summary/:objectId` - AI yearly summary
  - Auth: Required (rate limited: 10 per hour)
  - Path: objectId
  - Returns: AI-generated yearly report

## Legacy Module (`/api/legacy`)

Deprecated endpoints for backward compatibility.

- `GET /api/legacy/temperature-efficiency-chart/:objectId` - Legacy chart
  - Auth: Required
  - Path: objectId
  - Status: DEPRECATED
  - Returns: Chart data

## Logbook Module (`/api/logbook`)

All routes require authentication.

- `GET /api/logbook` - Get logbook entries
  - Auth: Required
  - Query: `?objectId=int&status=string&priority=string&entryType=string` (all optional)
  - Returns: Array of logbook entries

- `GET /api/logbook/entries` - Get logbook entries (alias)
  - Auth: Required
  - Same as above

- `GET /api/logbook/:id` - Get single logbook entry
  - Auth: Required
  - Path: id
  - Returns: Logbook entry

- `GET /api/logbook/entries/:id` - Get single entry (alias)
  - Auth: Required
  - Path: id
  - Returns: Logbook entry

- `POST /api/logbook` - Create logbook entry
  - Auth: Required
  - Body: `{ title, entryType, description, objectId, status, priority }`
  - Returns: Created entry

- `POST /api/logbook/entries` - Create entry (alias)
  - Auth: Required
  - Same as above

- `PUT /api/logbook/:id` - Update logbook entry
  - Auth: Required
  - Path: id
  - Body: Partial logbook data
  - Returns: Updated entry

- `PUT /api/logbook/entries/:id` - Update entry (alias)
  - Auth: Required
  - Same as above

- `DELETE /api/logbook/:id` - Delete logbook entry
  - Auth: Required
  - Path: id
  - Returns: Success message

- `DELETE /api/logbook/entries/:id` - Delete entry (alias)
  - Auth: Required
  - Path: id
  - Returns: Success message

## Mandants Module (`/api/mandants`)

All routes require authentication.

- `GET /api/mandants` - Get all mandants
  - Auth: Required
  - Returns: Array of mandants

- `POST /api/mandants` - Create mandant
  - Auth: Required
  - Body: Mandant data
  - Returns: Created mandant

- `PATCH /api/mandants/:id` - Update mandant
  - Auth: Required
  - Path: id
  - Body: Partial mandant data
  - Returns: Updated mandant

- `DELETE /api/mandants/:id` - Delete mandant
  - Auth: Required
  - Path: id
  - Returns: Success message

## Monitoring Module (`/api/monitoring`)

All routes require authentication.

### Dashboard
- `GET /api/monitoring/dashboard/kpis` - Dashboard KPIs
  - Auth: Required
  - Returns: KPI metrics

### Critical Systems
- `GET /api/monitoring/systems/critical` - Get critical systems
  - Auth: Required
  - Query: `?mandantIds=1,2,3` (optional)
  - Returns: Array of critical systems

### Energy Classification
- `GET /api/monitoring/systems/by-energy-class` - Systems by energy class
  - Auth: Required
  - Query: `?mandantIds=1,2,3` (optional)
  - Returns: Systems grouped by energy class

### Alerts
- `GET /api/monitoring/alerts` - Get system alerts
  - Auth: Required
  - Query: `?systemId=int&unresolved=bool&mandantIds=1,2,3` (all optional)
  - Returns: Array of alerts

- `POST /api/monitoring/alerts` - Create system alert
  - Auth: Required
  - Body: `{ message, alertType, severity, objectId, metadata }`
  - Returns: Created alert

- `PATCH /api/monitoring/alerts/:id/resolve` - Resolve alert
  - Auth: Required
  - Path: id
  - Returns: Updated alert

## Object Groups Module (`/api/object-groups`)

All routes require authentication.

- `GET /api/object-groups` - Get all object groups
  - Auth: Required
  - Returns: Array of object groups

- `POST /api/object-groups` - Create object group
  - Auth: Required
  - Body: Object group data
  - Returns: Created group

- `PATCH /api/object-groups/:id` - Update object group
  - Auth: Required
  - Path: id
  - Body: Partial group data
  - Returns: Updated group

- `DELETE /api/object-groups/:id` - Delete object group
  - Auth: Required
  - Path: id
  - Returns: Success message

## Objects Module (`/api/objects`)

All routes require authentication.

### Object CRUD
- `GET /api/objects` - Get all objects (filtered by mandant)
  - Auth: Required
  - Query: `?status=string&city=string&postalCode=string&objectType=string` (all optional)
  - Returns: Array of objects

- `GET /api/objects/:id` - Get single object by ID
  - Auth: Required
  - Path: id
  - Returns: Object data

- `GET /api/objects/objectid/:objectid` - Get object by objectid
  - Auth: Required
  - Path: objectid (bigint)
  - Returns: Object data

- `GET /api/objects/by-objectid/:objectid` - Get object by objectid (alias)
  - Auth: Required
  - Path: objectid (bigint)
  - Returns: Object data

- `GET /api/objects/postal/:postalCode` - Get object by postal code
  - Auth: Required
  - Path: postalCode
  - Returns: Object data

- `GET /api/objects/meter/:objectid` - Get meter data
  - Auth: Required
  - Path: objectid (bigint)
  - Returns: Meter data

- `GET /api/objects/hierarchy/:mandantId` - Get object hierarchy
  - Auth: Required
  - Path: mandantId
  - Returns: Array of objects in hierarchy

- `GET /api/objects/:id/children` - Get object children
  - Auth: Required
  - Path: id
  - Returns: Array of child objects

- `POST /api/objects` - Create object
  - Auth: Required (admin/superadmin)
  - Body: `{ name, objectid, mandantId, ... }`
  - Returns: Created object

- `PUT /api/objects/:id` - Update object
  - Auth: Required (admin/superadmin)
  - Path: id
  - Body: Partial object data
  - Returns: Updated object

- `PATCH /api/objects/:id/coordinates` - Update coordinates
  - Auth: Required (admin/superadmin)
  - Path: id
  - Body: `{ latitude, longitude }`
  - Returns: Updated object

- `PATCH /api/objects/:id/meter` - Update meter data
  - Auth: Required (admin/superadmin)
  - Path: id
  - Body: Meter data
  - Returns: Updated object

- `DELETE /api/objects/:id` - Delete object
  - Auth: Required (admin/superadmin)
  - Path: id
  - Returns: Success message

### Object-Mandant Assignments
- `GET /api/objects/:id/assignments` - Get assignments
  - Auth: Required
  - Path: id
  - Returns: Array of assignments

- `POST /api/objects/:id/assignments` - Create assignment
  - Auth: Required (admin/superadmin)
  - Path: id
  - Body: `{ mandantId, mandantRole }`
  - Returns: Success message

- `DELETE /api/objects/:id/assignments` - Delete all assignments
  - Auth: Required (admin/superadmin)
  - Path: id
  - Returns: Success message

- `DELETE /api/objects/:id/assignments/:role` - Delete by role
  - Auth: Required (admin/superadmin)
  - Path: id, role
  - Returns: Success message

### Object Groups (nested)
- `GET /api/objects/groups` - Get all groups
  - Auth: Required
  - Returns: Array of groups

- `POST /api/objects/groups` - Create group
  - Auth: Required (admin/superadmin)
  - Body: Group data
  - Returns: Created group

- `PUT /api/objects/groups/:id` - Update group
  - Auth: Required (admin/superadmin)
  - Path: id
  - Body: Partial group data
  - Returns: Updated group

- `DELETE /api/objects/groups/:id` - Delete group
  - Auth: Required (admin/superadmin)
  - Path: id
  - Returns: Success message

## Settings Module (`/api/settings`)

All routes require authentication.

- `GET /api/settings` - Get settings
  - Auth: Required
  - Query: `?category=string&userId=int&mandantId=int` (all optional)
  - Returns: Array of settings

- `GET /api/settings/by-key` - Get single setting by key
  - Auth: Required
  - Query: `?category=string&keyName=string&userId=int&mandantId=int` (category and keyName required)
  - Returns: Single setting

- `GET /api/settings/thresholds` - Get temperature thresholds
  - Auth: Required
  - Returns: Threshold settings

- `GET /api/settings/:id` - Get setting by ID
  - Auth: Required
  - Path: id
  - Returns: Single setting

- `POST /api/settings` - Create setting
  - Auth: Required
  - Body: `{ category, keyName, value, userId, mandantId }`
  - Returns: Created setting

- `PUT /api/settings/:id` - Update setting
  - Auth: Required
  - Path: id
  - Body: Partial setting data
  - Returns: Updated setting

- `DELETE /api/settings/:id` - Delete setting
  - Auth: Required
  - Path: id
  - Returns: Success message

- `DELETE /api/settings/clear` - Clear all settings
  - Auth: Required (superadmin only)
  - Returns: Success message

## Setup Module (`/api/setup-config`)

- `GET /api/setup-config` - Get setup configuration
  - Auth: Required
  - Returns: Setup configuration data

## Temperature Module (`/api/temperature`)

All routes require authentication.

### Daily Outdoor Temperature
- `GET /api/temperature/daily-outdoor` - Get daily outdoor temps
  - Auth: Required
  - Query: `?postalCode=string&startDate=ISO&endDate=ISO&resolution=string` (all optional)
  - Returns: Array of temperature records

- `GET /api/temperature/daily-outdoor/:id` - Get single temperature
  - Auth: Required
  - Path: id
  - Returns: Temperature record

- `POST /api/temperature/daily-outdoor` - Create temperature record
  - Auth: Required
  - Body: Temperature data
  - Returns: Created record

- `PUT /api/temperature/daily-outdoor/:id` - Update temperature
  - Auth: Required
  - Path: id
  - Body: Partial temperature data
  - Returns: Updated record

- `DELETE /api/temperature/daily-outdoor/:id` - Delete temperature
  - Auth: Required
  - Path: id
  - Returns: Success message

### Postal Code Queries
- `GET /api/temperature/postal-code/:postalCode` - Get temps by postal
  - Auth: Required
  - Path: postalCode
  - Query: `?startDate=ISO&endDate=ISO` (optional)
  - Returns: Array of temperatures

- `GET /api/temperature/postal-code/:postalCode/latest` - Get latest temp
  - Auth: Required
  - Path: postalCode
  - Returns: Latest temperature

- `GET /api/temperature/objects/postal-codes` - Temps for object postals
  - Auth: Required
  - Query: `?objectIds=1,2,3` (optional)
  - Returns: Array of temperatures

### Efficiency Data
- `GET /api/temperature/efficiency/:objectId` - Temperature efficiency
  - Auth: Required
  - Path: objectId
  - Query: `?timeRange=last30days` (optional)
  - Returns: Efficiency data

## Todo Tasks Module (`/api/todo-tasks`)

All routes require authentication.

- `GET /api/todo-tasks` - Get todo tasks
  - Auth: Required
  - Query: `?objectId=int&status=string&priority=string&assignedTo=int` (all optional)
  - Returns: Array of tasks

- `GET /api/todo-tasks/:id` - Get single task
  - Auth: Required
  - Path: id
  - Returns: Task data

- `POST /api/todo-tasks` - Create task
  - Auth: Required
  - Body: `{ title, description, objectId, dueDate, priority, assignedTo, status }`
  - Returns: Created task

- `PUT /api/todo-tasks/:id` - Update task
  - Auth: Required
  - Path: id
  - Body: Partial task data
  - Returns: Updated task

- `DELETE /api/todo-tasks/:id` - Delete task
  - Auth: Required
  - Path: id
  - Returns: Success message

## User Logs Module (`/api/user-logs`, `/api/user-activity-logs`)

Routes mounted at both paths for compatibility.

- `GET /api/user-logs` - Get user logs for current user
  - Auth: Not explicitly required (relies on session)
  - Returns: Array of user logs

- `GET /api/user-logs/activity/:timeRange?` - Get activity logs
  - Auth: Not explicitly required
  - Path: timeRange (optional)
  - Returns: Array of activity logs

- `POST /api/user-logs/activity` - Create activity log
  - Auth: Not explicitly required
  - Body: Activity log data
  - Returns: Created log

## User Profiles Module (`/api/user-profiles`)

All routes require authentication.

- `GET /api/user-profiles` - Get all user profiles
  - Auth: Required
  - Returns: Array of profiles

- `POST /api/user-profiles` - Create user profile
  - Auth: Required
  - Body: Profile data
  - Returns: Created profile

- `PUT /api/user-profiles/:id` - Update profile
  - Auth: Required
  - Path: id
  - Body: Partial profile data
  - Returns: Updated profile

- `DELETE /api/user-profiles/:id` - Delete profile
  - Auth: Required
  - Path: id
  - Returns: Success message

## Users Module (`/api/users`)

All routes require authentication.

### User CRUD
- `GET /api/users` - Get all users (filtered by mandant)
  - Auth: Required
  - Returns: Array of users

- `GET /api/users/:id` - Get single user
  - Auth: Required
  - Path: id
  - Returns: User data

- `POST /api/users` - Create user
  - Auth: Required (rate limited: 5 per hour)
  - Body: User data (validated by createUserSchema)
  - Returns: Created user

- `PATCH /api/users/:id` - Update user
  - Auth: Required
  - Path: id
  - Body: Partial user data (validated by updateUserSchema)
  - Returns: Updated user

- `DELETE /api/users/:id` - Delete user
  - Auth: Required
  - Path: id
  - Returns: Success message

### Password Management
- `POST /api/users/:id/change-password` - Change password
  - Auth: Required (rate limited: 3 per hour)
  - Path: id
  - Body: Password data
  - Returns: Success message

### User Profiles (nested)
- `GET /api/users/profiles/list` - Get all profiles
  - Auth: Required
  - Returns: Array of profiles

- `POST /api/users/profiles` - Create profile
  - Auth: Required
  - Body: Profile data
  - Returns: Created profile

- `PUT /api/users/profiles/:id` - Update profile
  - Auth: Required
  - Path: id
  - Body: Partial profile data
  - Returns: Updated profile

- `DELETE /api/users/profiles/:id` - Delete profile
  - Auth: Required
  - Path: id
  - Returns: Success message

## Weather Module (`/api/outdoor-temperatures`)

All routes are public (no authentication).

- `GET /api/outdoor-temperatures/postal-code/:postalCode/latest` - Latest temperature
  - Auth: Public
  - Path: postalCode
  - Returns: Latest temperature for postal code

- `GET /api/outdoor-temperatures/postal-code/:postalCode` - Temperature history
  - Auth: Public
  - Path: postalCode
  - Returns: Array of temperatures

- `POST /api/outdoor-temperatures/restore-climate-data` - Restore climate data
  - Auth: Public (should be protected in production)
  - Body: Backup data
  - Returns: Success message

- `POST /api/outdoor-temperatures/import-2023-climate` - Import 2023 data
  - Auth: Public (should be protected in production)
  - Body: 2023 climate data
  - Returns: Success message

## Root-Level Routes

Outside module structure:

- `GET /health` - Application health (defined in index.ts)
  - Auth: Public
  - Returns: `{ status, timestamp, uptime }`

- `GET /startki` - KI system iframe wrapper (defined in index.ts)
  - Auth: Public
  - Returns: HTML iframe page
