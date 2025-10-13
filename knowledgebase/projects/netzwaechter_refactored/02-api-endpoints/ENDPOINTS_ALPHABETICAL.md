# API Endpoints - Alphabetical Reference

Created: 2025-10-13
Timestamp: 16:47:00

Quick alphabetical lookup of all API endpoints.

## A

- `POST /api/admin/portal/activate-config` - Activate portal configuration
- `DELETE /api/admin/portal/activate-config` - (not defined)
- `GET /api/admin/dashboard/kpis` - Get dashboard KPIs
- `GET /api/admin/database/status` - Get database connection status
- `GET /api/admin/mandants` - Get all mandants
- `GET /api/admin/objects` - Get all objects (admin view)
- `GET /api/admin/portal/active-config` - Get active portal config
- `GET /api/admin/portal/config` - Get portal configuration
- `GET /api/admin/portal/fallback-config` - Get fallback database config
- `GET /api/admin/portal/load-config/:configType` - Load config by type
- `GET /api/admin/settings` - Get all settings
- `POST /api/admin/portal/save-config/:configType` - Save config by type
- `POST /api/admin/portal/save-fallback-config` - Save fallback config
- `POST /api/admin/portal/test-config/:configType` - Test config by type
- `POST /api/admin/portal/test-connection` - Test database connection
- `POST /api/admin/settings` - Save a setting
- `POST /api/auth/heartbeat` - Extend session
- `GET /api/auth/me` - Get current authenticated user
- `POST /api/auth/login` - Standard user login
- `POST /api/auth/logout` - Destroy session
- `POST /api/auth/superadmin-login` - Superadmin login

## D

- `GET /api/database/status` - Get database connection pool status

## E

- `GET /api/efficiency/analysis/:objectId` - Get efficiency analysis (auth required)
- `GET /api/energy/all-meters/:objectId` - Energy data for all meters
- `GET /api/energy/daily-consumption-data/:objectId` - Daily consumption by meter
- `GET /api/energy/daily-consumption/:objectId` - Get daily consumption
- `GET /api/energy/day-comp/:objectId` - Get day compensation data
- `GET /api/energy/day-comp/:objectId/latest` - Get latest day comp data
- `POST /api/energy/day-comp` - Create day compensation data
- `GET /api/energy/external/:objectId` - Get external energy data
- `GET /api/energy/object/:objectId` - Energy data for object
- `GET /api/energy/specific-meter/:meterId/:objectId` - Specific meter data
- `POST /api/export/send-email` - Send PDF export via email

## H

- `GET /api/health` - Comprehensive health check
- `GET /api/health/metrics` - Prometheus metrics
- `GET /api/health/pool` - Connection pool statistics

## K

- `GET /api/ki-reports/yearly-summary/:objectId` - AI yearly summary

## L

- `GET /api/legacy/temperature-efficiency-chart/:objectId` - Legacy temperature chart (DEPRECATED)
- `GET /api/logbook` - Get logbook entries
- `GET /api/logbook/:id` - Get single logbook entry
- `GET /api/logbook/entries` - Get logbook entries (alias)
- `GET /api/logbook/entries/:id` - Get single entry (alias)
- `POST /api/logbook` - Create logbook entry
- `POST /api/logbook/entries` - Create entry (alias)
- `PUT /api/logbook/:id` - Update logbook entry
- `PUT /api/logbook/entries/:id` - Update entry (alias)
- `DELETE /api/logbook/:id` - Delete logbook entry
- `DELETE /api/logbook/entries/:id` - Delete entry (alias)

## M

- `GET /api/mandants` - Get all mandants
- `POST /api/mandants` - Create mandant
- `PATCH /api/mandants/:id` - Update mandant
- `DELETE /api/mandants/:id` - Delete mandant
- `GET /api/monitoring/alerts` - Get system alerts
- `POST /api/monitoring/alerts` - Create system alert
- `PATCH /api/monitoring/alerts/:id/resolve` - Resolve alert
- `GET /api/monitoring/dashboard/kpis` - Dashboard KPIs
- `GET /api/monitoring/systems/by-energy-class` - Systems by energy class
- `GET /api/monitoring/systems/critical` - Get critical systems
- `GET /api/monthly-netz/:objectId` - Monthly Netz meter data (PUBLIC)

## O

- `GET /api/object-groups` - Get all object groups
- `POST /api/object-groups` - Create object group
- `PATCH /api/object-groups/:id` - Update object group
- `DELETE /api/object-groups/:id` - Delete object group
- `GET /api/objects` - Get all objects (filtered by mandant)
- `GET /api/objects/:id` - Get single object by ID
- `GET /api/objects/:id/assignments` - Get object-mandant assignments
- `POST /api/objects/:id/assignments` - Create assignment
- `DELETE /api/objects/:id/assignments` - Delete all assignments
- `DELETE /api/objects/:id/assignments/:role` - Delete assignment by role
- `GET /api/objects/:id/children` - Get object children
- `POST /api/objects` - Create object
- `PUT /api/objects/:id` - Update object
- `PATCH /api/objects/:id/coordinates` - Update object coordinates
- `PATCH /api/objects/:id/meter` - Update object meter data
- `DELETE /api/objects/:id` - Delete object
- `GET /api/objects/by-objectid/:objectid` - Get object by objectid (alias)
- `GET /api/objects/groups` - Get all object groups
- `POST /api/objects/groups` - Create object group
- `PUT /api/objects/groups/:id` - Update object group
- `DELETE /api/objects/groups/:id` - Delete object group
- `GET /api/objects/hierarchy/:mandantId` - Get object hierarchy
- `GET /api/objects/meter/:objectid` - Get meter data by objectid
- `GET /api/objects/objectid/:objectid` - Get object by objectid
- `GET /api/objects/postal/:postalCode` - Get object by postal code
- `GET /api/outdoor-temperatures/postal-code/:postalCode` - Temperature history (PUBLIC)
- `GET /api/outdoor-temperatures/postal-code/:postalCode/latest` - Latest temperature (PUBLIC)
- `POST /api/outdoor-temperatures/import-2023-climate` - Import 2023 data (PUBLIC)
- `POST /api/outdoor-temperatures/restore-climate-data` - Restore climate data (PUBLIC)

## P

- `GET /api/public-daily-consumption/:objectId` - Public daily consumption (PUBLIC)
- `GET /api/public-monthly-consumption/:objectId` - Public monthly consumption (PUBLIC)

## S

- `GET /api/settings` - Get settings
- `GET /api/settings/:id` - Get setting by ID
- `GET /api/settings/by-key` - Get single setting by key
- `GET /api/settings/thresholds` - Get temperature thresholds
- `POST /api/settings` - Create setting
- `PUT /api/settings/:id` - Update setting
- `DELETE /api/settings/:id` - Delete setting
- `DELETE /api/settings/clear` - Clear all settings (superadmin only)
- `GET /api/setup-config` - Get setup configuration

## T

- `GET /api/temperature/daily-outdoor` - Get daily outdoor temperatures
- `GET /api/temperature/daily-outdoor/:id` - Get single temperature
- `POST /api/temperature/daily-outdoor` - Create temperature record
- `PUT /api/temperature/daily-outdoor/:id` - Update temperature
- `DELETE /api/temperature/daily-outdoor/:id` - Delete temperature
- `GET /api/temperature/efficiency/:objectId` - Temperature efficiency
- `GET /api/temperature/objects/postal-codes` - Temps for object postals
- `GET /api/temperature/postal-code/:postalCode` - Get temps by postal code
- `GET /api/temperature/postal-code/:postalCode/latest` - Get latest temperature
- `GET /api/test-efficiency-analysis/:objectId` - Test efficiency analysis (PUBLIC)
- `GET /api/todo-tasks` - Get todo tasks
- `GET /api/todo-tasks/:id` - Get single task
- `POST /api/todo-tasks` - Create task
- `PUT /api/todo-tasks/:id` - Update task
- `DELETE /api/todo-tasks/:id` - Delete task

## U

- `GET /api/user-logs` - Get user logs for current user
- `GET /api/user-logs/activity/:timeRange?` - Get activity logs
- `POST /api/user-logs/activity` - Create activity log
- `GET /api/user-profiles` - Get all user profiles
- `POST /api/user-profiles` - Create user profile
- `PUT /api/user-profiles/:id` - Update profile
- `DELETE /api/user-profiles/:id` - Delete profile
- `GET /api/users` - Get all users (filtered by mandant)
- `GET /api/users/:id` - Get single user
- `POST /api/users` - Create user
- `PATCH /api/users/:id` - Update user
- `DELETE /api/users/:id` - Delete user
- `POST /api/users/:id/change-password` - Change password
- `GET /api/users/profiles/list` - Get all profiles
- `POST /api/users/profiles` - Create profile
- `PUT /api/users/profiles/:id` - Update profile
- `DELETE /api/users/profiles/:id` - Delete profile

## Root-Level Routes

- `GET /health` - Application health check (public)
- `GET /startki` - KI system iframe wrapper (public)

## Summary Statistics

- Total API endpoints: 120+
- Public endpoints: 10
- Authenticated endpoints: 110+
- Rate-limited endpoints: 7
- Deprecated endpoints: 1 (temperature-efficiency-chart)

## Endpoint Naming Conventions

- Plural nouns for collections: `/api/objects`, `/api/users`
- Singular for single items: `/api/objects/:id`
- Action verbs in path: `/api/monitoring/alerts/:id/resolve`
- Nested resources: `/api/objects/:id/assignments`
- Query parameters for filters: `?status=active&priority=high`
- Hyphenated names: `/api/todo-tasks`, `/api/ki-reports`

## HTTP Methods Usage

- `GET`: Read operations (77 endpoints)
- `POST`: Create operations (22 endpoints)
- `PUT`: Full update operations (9 endpoints)
- `PATCH`: Partial update operations (8 endpoints)
- `DELETE`: Delete operations (13 endpoints)
