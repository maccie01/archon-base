# Frontend-Backend API Usage Map

Created: 2025-10-13
Timestamp: 16:50:00

Maps which backend API endpoints are called from which frontend features and components.

## Auth Module

### Frontend Files
- `apps/frontend-web/src/features/auth/api/authApi.ts`
- `apps/frontend-web/src/features/auth/hooks/useAuth.ts`
- `apps/frontend-web/src/features/auth/components/LoginModal.tsx`
- `apps/frontend-web/src/features/auth/pages/Login.tsx`
- `apps/frontend-web/src/features/auth/pages/SuperadminLogin.tsx`

### API Calls
- `POST /api/auth/login` - Used in: LoginModal, Login page
- `POST /api/auth/superadmin-login` - Used in: SuperadminLogin page
- `POST /api/auth/logout` - Used in: Layout, useAuth hook
- `GET /api/auth/me` - Used in: useAuth hook, App.tsx
- `POST /api/auth/heartbeat` - Used in: Layout (session keepalive)
- `GET /api/auth/check` - Used in: useAuth hook (NOTE: endpoint does NOT exist in backend)

### API Mismatches
- `/api/auth/check` is called by frontend but not defined in backend routes

## Objects Module

### Frontend Files
- `apps/frontend-web/src/features/objects/api/objectsApi.ts`
- `apps/frontend-web/src/features/objects/hooks/useObjectMutations.ts`
- `apps/frontend-web/src/features/objects/pages/ObjectManagement.tsx`
- `apps/frontend-web/src/features/objects/components/ObjectListLayout.tsx`
- `apps/frontend-web/src/features/objects/components/NetzView.tsx`
- `apps/frontend-web/src/features/objects/components/ObjektinfoContent.tsx`

### API Calls
- `GET /api/objects` - Used in: ObjectManagement, ObjectListLayout
- `GET /api/objects/:id` - Used in: ObjektinfoContent
- `GET /api/objects/by-objectid?objectid=:objectid` - Used in: monitoringApi (NOTE: Query param instead of path param)
- `POST /api/objects` - Used in: ObjectManagement (create modal)
- `PATCH /api/objects/:id` - Used in: Object edit forms
- `PATCH /api/objects/:id/coordinates` - Used in: Maps page
- `DELETE /api/objects/:id` - Used in: ObjectManagement
- `GET /api/object-groups` - Used in: ObjectManagement
- `POST /api/object-groups` - Used in: ObjectManagement
- `PATCH /api/object-groups/:id` - Used in: ObjectManagement
- `DELETE /api/object-groups/:id` - Used in: ObjectManagement
- `POST /api/object-mandant` - Used in: Object assignment (NOTE: endpoint path differs from backend)
- `PATCH /api/object-mandant/:objectId` - Used in: Object assignment (NOTE: endpoint path differs from backend)
- `DELETE /api/object-mandant/:objectId/:mandantId` - Used in: Object assignment (NOTE: endpoint path differs from backend)

### API Mismatches
- Frontend calls `/api/object-mandant/*` but backend defines `/api/objects/:id/assignments*`
- Frontend calls `/api/objects/by-objectid?objectid=:objectid` (query param) but backend route expects path param `/api/objects/by-objectid/:objectid`

## Energy Module

### Frontend Files
- `apps/frontend-web/src/features/energy/api/energyApi.ts`
- `apps/frontend-web/src/features/energy/pages/EfficiencyAnalysis.tsx`
- `apps/frontend-web/src/features/energy/pages/EnergyData.tsx`
- `apps/frontend-web/src/features/energy/pages/DbEnergyDataConfig.tsx`
- `apps/frontend-web/src/features/energy/components/KI_energy_jahr.tsx`
- `apps/frontend-web/src/features/energy/components/KI_energy_jahr_wrapper.tsx`
- `apps/frontend-web/src/features/energy/components/EfficiencyDistributionCard.tsx`

### API Calls
- `GET /api/heating-systems` - Used in: EnergyData (NOTE: endpoint does NOT exist in backend)
- `GET /api/energy-data?systemId=:systemId` - Used in: EnergyData (NOTE: endpoint does NOT exist in backend)
- `POST /api/energy-data` - Used in: EnergyData (NOTE: endpoint does NOT exist in backend)
- `PUT /api/energy-data/:id` - Used in: EnergyData (NOTE: endpoint does NOT exist in backend)
- `DELETE /api/energy-data/:id` - Used in: EnergyData (NOTE: endpoint does NOT exist in backend)
- `GET /api/test-efficiency-analysis/:objectId` - Used in: EfficiencyAnalysis, energyApi
- `POST /api/energy-balance/:objectId` - Used in: energyApi (NOTE: endpoint does NOT exist in backend)
- `GET /api/settings/dbEnergyData_view_day_comp` - Used in: DbEnergyDataConfig (NOTE: should use /api/settings/by-key)

### API Mismatches
- Multiple energy-related endpoints are called but not defined in backend:
  - `/api/heating-systems`
  - `/api/energy-data*`
  - `/api/energy-balance/:objectId`

## Monitoring Module

### Frontend Files
- `apps/frontend-web/src/features/monitoring/api/monitoringApi.ts`
- `apps/frontend-web/src/features/monitoring/pages/Dashboard.tsx`
- `apps/frontend-web/src/features/monitoring/pages/NetworkMonitor.tsx`
- `apps/frontend-web/src/features/monitoring/pages/Maps.tsx`
- `apps/frontend-web/src/features/monitoring/pages/PerformanceTest.tsx`
- `apps/frontend-web/src/features/monitoring/hooks/useTemperatureAnalysis.ts`
- `apps/frontend-web/src/features/monitoring/components/GrafanaContentEmbedded.tsx`

### API Calls
- `GET /api/dashboard/kpis` - Used in: Dashboard (NOTE: should be /api/monitoring/dashboard/kpis)
- `GET /api/dashboard/critical-systems` - Used in: Dashboard (NOTE: should be /api/monitoring/systems/critical)
- `GET /api/system-alerts` - Used in: Dashboard (NOTE: should be /api/monitoring/alerts)
- `GET /api/settings/thresholds` - Used in: NetworkMonitor, TemperatureAnalysis
- `GET /api/public-daily-consumption/:objectId` - Used in: NetworkMonitor
- `GET /api/public-monthly-consumption/:objectId` - Used in: NetworkMonitor
- `GET /api/test-efficiency-analysis/:objectId` - Used in: PerformanceTest
- `PUT /api/objects/:objectId/coordinates` - Used in: Maps (NOTE: should be PATCH)
- `GET /api/settings?category=grafana` - Used in: GrafanaContentEmbedded

### API Mismatches
- Frontend expects `/api/dashboard/*` but backend defines `/api/monitoring/dashboard/*`
- Frontend expects `/api/system-alerts` but backend defines `/api/monitoring/alerts`
- Frontend uses `PUT` for coordinates update, backend defines `PATCH`

## Settings Module

### Frontend Files
- `apps/frontend-web/src/features/settings/api/settingsApi.ts`
- `apps/frontend-web/src/features/settings/pages/ApiManagement.tsx`
- `apps/frontend-web/src/features/settings/pages/Devices.tsx`
- `apps/frontend-web/src/features/settings/components/DatabaseStatus.tsx`
- `apps/frontend-web/src/features/settings/components/DatabaseSettings.tsx`
- `apps/frontend-web/src/features/settings/components/PortalConfigCard.tsx`
- `apps/frontend-web/src/features/settings/components/SystemPortalSetup.tsx`
- `apps/frontend-web/src/features/settings/components/TemperatureThresholdSettings.tsx`

### API Calls
- `GET /api/settings` - Used in: ApiManagement, TemperatureThresholdSettings
- `GET /api/settings?category=:category` - Used in: Various settings pages
- `GET /api/settings/thresholds` - Used in: TemperatureThresholdSettings
- `POST /api/settings` - Used in: Settings create/update
- `PUT /api/settings/:id` - Used in: Settings update
- `DELETE /api/settings/:id` - Used in: Settings delete
- `DELETE /api/settings/:category/:keyName` - Used in: settingsApi (NOTE: endpoint does NOT exist in backend)
- `GET /api/database/info` - Used in: DatabaseSettings (NOTE: endpoint does NOT exist in backend)
- `GET /api/database/status` - Used in: DatabaseStatus
- `POST /api/database/performance-test` - Used in: settingsApi (NOTE: endpoint does NOT exist in backend)
- `GET /api/setup-config` - Used in: SystemPortalSetup
- `GET /api/health` - Used in: DatabaseStatus
- `GET /api/status` - Used in: settingsApi (NOTE: endpoint does NOT exist in backend)

### API Mismatches
- `/api/settings/:category/:keyName` (DELETE) does not exist in backend
- `/api/database/info` does not exist in backend
- `/api/database/performance-test` does not exist in backend
- `/api/status` does not exist in backend

## Users Module

### Frontend Files
- `apps/frontend-web/src/features/users/api/usersApi.ts`
- `apps/frontend-web/src/features/users/hooks/useUserData.ts`
- `apps/frontend-web/src/features/users/hooks/useUserMutations.ts`
- `apps/frontend-web/src/features/users/pages/User.tsx`
- `apps/frontend-web/src/features/users/pages/UserSettings.tsx`
- `apps/frontend-web/src/features/users/components/UserSettingsModal.tsx`

### API Calls
- `GET /api/users` - Used in: User page
- `GET /api/users/mandant` - Used in: usersApi (NOTE: endpoint does NOT exist in backend)
- `POST /api/users` - Used in: User create modal
- `PATCH /api/users/:id` - Used in: User edit modal
- `DELETE /api/users/:id` - Used in: User management
- `POST /api/users/:id/change-password` - Used in: UserSettingsModal
- `GET /api/user-profiles` - Used in: User management
- `POST /api/user-profiles` - Used in: Profile creation
- `PUT /api/user-profiles/:id` - Used in: Profile update
- `DELETE /api/user-profiles/:id` - Used in: Profile deletion
- `GET /api/mandants` - Used in: User management
- `POST /api/mandants` - Used in: Mandant creation
- `PATCH /api/mandants/:id` - Used in: Mandant update
- `DELETE /api/mandants/:id` - Used in: Mandant deletion

### API Mismatches
- `/api/users/mandant` (GET) does not exist in backend

## Logbook Module

### Frontend Files
- `apps/frontend-web/src/features/logbook/api/logbook.api.ts`
- `apps/frontend-web/src/features/logbook/hooks/useLogbook.ts`

### API Calls
- `POST /api/logbook` - Used in: Logbook entry creation
- `POST /api/todo-tasks` - Used in: Task creation
- `PUT /api/todo-tasks/:id` - Used in: Task update
- `DELETE /api/todo-tasks/:id` - Used in: Task deletion

### API Mismatches
None identified

## Temperature Module

### Frontend Files
- `apps/frontend-web/src/features/temperature/api/temperatureApi.ts`
- `apps/frontend-web/src/features/temperature/components/TemperatureEfficiencyChart.tsx`
- `apps/frontend-web/src/features/temperature/pages/TemperatureAnalysis.tsx`

### API Calls
- Temperature API file likely exists but not shown in sample
- Uses public weather endpoints from `/api/outdoor-temperatures/*`
- May use `/api/temperature/*` endpoints

## KI Reports Module

### Frontend Files
- `apps/frontend-web/src/features/ki-reports/api/reportsApi.ts`
- `apps/frontend-web/src/features/ki-reports/components/GrafanaReport.tsx`
- `apps/frontend-web/src/features/ki-reports/components/GrafanaDiagramme.tsx`
- `apps/frontend-web/src/features/ki-reports/pages/GrafanaDashboard.tsx`

### API Calls
Likely includes:
- `GET /api/ki-reports/yearly-summary/:objectId`
- Grafana-related API calls through settings

## Admin Dashboard Module

### Frontend Files
- `apps/frontend-web/src/features/admin-dashboard/hooks/useActivityLogs.ts`

### API Calls
- `GET /api/user-logs/activity/:timeRange?` - Used in: Admin dashboard activity logs
- `POST /api/user-logs/activity` - Used in: Activity log creation

## Shared Components

### DatabaseStatusHeader.tsx
- `GET /api/database/status` - Used in: Header component

### DatabaseStatus components
- `GET /api/admin/database/status` - Used in: Admin database status
- `GET /api/database/status` - Used in: Connection pool status

### ExportDialog.tsx
- `POST /api/export/send-email` - Used in: PDF export functionality

### Layout.tsx
- `GET /api/auth/me` - Used in: User session check
- `POST /api/auth/heartbeat` - Used in: Session keepalive

## Summary of API Mismatches

### Missing Backend Endpoints (Called by Frontend)
1. `GET /api/auth/check` - Auth status check
2. `GET /api/heating-systems` - Heating systems list
3. `GET /api/energy-data?systemId=:systemId` - Energy data query
4. `POST /api/energy-data` - Energy data creation
5. `PUT /api/energy-data/:id` - Energy data update
6. `DELETE /api/energy-data/:id` - Energy data deletion
7. `POST /api/energy-balance/:objectId` - Energy balance calculation
8. `GET /api/dashboard/kpis` - Dashboard KPIs (should be /api/monitoring/dashboard/kpis)
9. `GET /api/dashboard/critical-systems` - Critical systems (should be /api/monitoring/systems/critical)
10. `GET /api/system-alerts` - System alerts (should be /api/monitoring/alerts)
11. `DELETE /api/settings/:category/:keyName` - Delete setting by key
12. `GET /api/database/info` - Database info
13. `POST /api/database/performance-test` - Performance test
14. `GET /api/status` - System status
15. `GET /api/users/mandant` - Users by mandant
16. `POST /api/object-mandant` - Object-mandant assignment (should be /api/objects/:id/assignments)
17. `PATCH /api/object-mandant/:objectId` - Update assignment (should be /api/objects/:id/assignments)
18. `DELETE /api/object-mandant/:objectId/:mandantId` - Delete assignment (should be /api/objects/:id/assignments/:role)

### Path Mismatches (Different URL Structure)
1. Frontend: `/api/objects/by-objectid?objectid=:objectid` (query param)
   Backend: `/api/objects/by-objectid/:objectid` (path param)

2. Frontend: `/api/object-mandant/*`
   Backend: `/api/objects/:id/assignments*`

3. Frontend: `/api/dashboard/*`
   Backend: `/api/monitoring/dashboard/*`

### Method Mismatches
1. Frontend uses `PUT /api/objects/:objectId/coordinates`
   Backend defines `PATCH /api/objects/:id/coordinates`

## Recommendations

### High Priority Fixes
1. Add missing monitoring endpoints or redirect frontend to correct paths:
   - Map `/api/dashboard/kpis` to `/api/monitoring/dashboard/kpis`
   - Map `/api/dashboard/critical-systems` to `/api/monitoring/systems/critical`
   - Map `/api/system-alerts` to `/api/monitoring/alerts`

2. Fix object-mandant assignment endpoints:
   - Update frontend to use `/api/objects/:id/assignments*`
   - Or add backend routes for `/api/object-mandant*`

3. Add missing energy data endpoints or update frontend

4. Fix query param vs path param mismatch for object lookup

### Medium Priority Fixes
1. Add `/api/auth/check` endpoint or remove from frontend
2. Add `/api/users/mandant` endpoint or update frontend
3. Standardize HTTP methods (PUT vs PATCH)

### Low Priority Fixes
1. Add missing database info/test endpoints if needed
2. Add system status endpoint if required
3. Implement energy balance calculation endpoint
