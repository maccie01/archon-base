# Request and Response Schemas

Created: 2025-10-13
Timestamp: 16:48:00

## Common Request Patterns

### Authentication Request
```typescript
// POST /api/auth/login
{
  username: string;
  password: string;
}
```

### Pagination (not currently implemented)
No pagination is currently implemented in the API. All list endpoints return full result sets.

### Date Range Filtering
```typescript
// Query parameters
{
  startDate?: string; // ISO 8601 format
  endDate?: string;   // ISO 8601 format
  timeRange?: 'last-365-days' | '2023' | '2024' | '2025' | 'last-year' | 'last30days';
}
```

### Mandant Filtering
```typescript
// Query parameters
{
  mandantIds?: string; // Comma-separated list: "1,2,3"
}
```

## Common Response Patterns

### Success Response (with data)
```typescript
{
  success?: boolean;
  message?: string;
  data?: any;
  source?: string; // e.g., 'database', 'external_database'
}
```

### Success Response (simple)
```typescript
{
  message: string;
}
```

### Error Response
```typescript
{
  message: string;
  error?: string;
  statusCode?: number;
}
```

### HTTP Status Codes
- `200 OK`: Successful GET/PUT/PATCH/DELETE
- `201 Created`: Successful POST
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Database connection failed

## Authentication Module

### Login Request
```typescript
// POST /api/auth/login
// POST /api/auth/superadmin-login
{
  username: string;
  password: string;
}
```

### Login Response
```typescript
{
  message: string; // "Erfolgreich angemeldet"
  user: {
    id: number;
    username: string;
    email: string;
    role: 'user' | 'admin' | 'superadmin';
    mandantId?: number;
    mandantAccess?: number[];
    // ... additional user fields
  };
}
```

### Current User Response
```typescript
// GET /api/auth/me
{
  id: number;
  username: string;
  email: string;
  role: string;
  mandantId?: number;
  mandantAccess?: number[];
  profile?: {
    firstName?: string;
    lastName?: string;
    phone?: string;
    // ... additional profile fields
  };
}
```

## Objects Module

### Object Schema
```typescript
{
  id: number;
  objectid: bigint | number; // Portal DB bigint ID
  name: string;
  street?: string;
  houseNumber?: string;
  postalCode?: string;
  city?: string;
  country?: string;
  latitude?: number;
  longitude?: number;
  objectType?: string;
  status?: string;
  mandantId?: number;
  parentObjectId?: number;
  meter?: {
    [meterKey: string]: string; // e.g., "Z20541": "123456"
  };
  report?: any; // JSON field
  createdAt?: string;
  updatedAt?: string;
}
```

### Create Object Request
```typescript
// POST /api/objects
{
  name: string; // Required
  objectid: bigint | number; // Required
  mandantId?: number;
  street?: string;
  houseNumber?: string;
  postalCode?: string;
  city?: string;
  objectType?: string;
  status?: string;
  latitude?: number;
  longitude?: number;
  parentObjectId?: number;
  meter?: object;
}
```

### Update Object Request
```typescript
// PUT /api/objects/:id
{
  name?: string;
  street?: string;
  city?: string;
  postalCode?: string;
  objectType?: string;
  status?: string;
  // ... any other object fields (partial update)
}
```

### Object-Mandant Assignment
```typescript
// POST /api/objects/:id/assignments
{
  mandantId: number; // Required
  mandantRole: string; // Required, e.g., 'owner', 'operator'
}
```

## Energy Module

### Day Comp Data Schema
```typescript
{
  id?: number;
  log: number; // objectId
  time: string; // ISO timestamp
  diff_en?: number;
  diff_vol?: number;
  pow_mean?: number;
  flt_mean?: number;
  ret_mean?: number;
  // ... additional energy fields
}
```

### Daily Consumption Response
```typescript
// GET /api/energy/daily-consumption/:objectId
{
  [date: string]: {
    date: string;
    consumption: number;
    avgTemperature?: number;
    avgPower?: number;
  };
}
```

### Monthly Netz Response
```typescript
// GET /api/monthly-netz/:objectId
{
  success: boolean;
  data: {
    objectId: number;
    meterKey: string; // e.g., "Z20541"
    meterId: number;
    timeRange: string;
    monthlyData: Array<{
      date: string; // YYYY-MM-01
      diffEn: number;
      energy: number;
      avgTemp: number;
      avgPower: number;
      returnTemp: number;
      volume: number;
    }>;
    rawRecordsCount: number;
    monthlyAggregatesCount: number;
  };
  source: 'external_database';
  message: string;
}
```

## Logbook Module

### Logbook Entry Schema
```typescript
{
  id?: number;
  title: string; // Required
  entryType: string; // Required, e.g., 'maintenance', 'incident'
  description?: string;
  objectId?: number;
  status?: string; // e.g., 'open', 'in_progress', 'closed'
  priority?: string; // e.g., 'low', 'medium', 'high', 'critical'
  createdBy?: number;
  assignedTo?: number;
  createdAt?: string;
  updatedAt?: string;
  resolvedAt?: string;
}
```

### Create Logbook Entry Request
```typescript
// POST /api/logbook
{
  title: string; // Required
  entryType: string; // Required
  description?: string;
  objectId?: number;
  status?: string;
  priority?: string;
  assignedTo?: number;
}
```

## Todo Tasks Module

### Todo Task Schema
```typescript
{
  id?: number;
  title: string; // Required
  description?: string;
  objectId?: number;
  logbookEntryId?: number;
  dueDate?: string; // ISO date
  priority?: string; // 'low', 'medium', 'high', 'critical'
  assignedTo?: number; // User ID
  status?: string; // 'pending', 'in_progress', 'completed'
  createdBy?: number;
  createdAt?: string;
  updatedAt?: string;
  completedAt?: string;
}
```

### Create Task Request
```typescript
// POST /api/todo-tasks
{
  title: string; // Required
  description?: string;
  objectId?: number;
  logbookEntryId?: number;
  dueDate?: string;
  priority?: string;
  assignedTo?: number;
  status?: string;
}
```

## Monitoring Module

### Dashboard KPIs Response
```typescript
// GET /api/monitoring/dashboard/kpis
{
  criticalSystems: number;
  totalFacilities: number;
  totalMandants: number;
  activeUsers: number;
  systemHealth: 'optimal' | 'warning' | 'critical';
  lastUpdate: string; // ISO timestamp
}
```

### System Alert Schema
```typescript
{
  id?: number;
  message: string; // Required
  alertType: string; // Required, e.g., 'temperature', 'consumption', 'system'
  severity: string; // Required, e.g., 'info', 'warning', 'critical'
  objectId?: number;
  systemId?: string;
  metadata?: object; // JSON field
  resolved?: boolean;
  resolvedAt?: string;
  resolvedBy?: number;
  createdAt?: string;
}
```

### Create Alert Request
```typescript
// POST /api/monitoring/alerts
{
  message: string; // Required
  alertType: string; // Required
  severity: string; // Required
  objectId?: number;
  metadata?: object;
}
```

## Users Module

### User Schema
```typescript
{
  id?: number;
  username: string; // Required, unique
  email: string; // Required, unique
  password?: string; // Hashed, never returned in responses
  role: 'user' | 'admin' | 'superadmin'; // Required
  mandantId?: number;
  mandantAccess?: number[]; // Array of additional mandant IDs
  isActive?: boolean;
  lastLogin?: string;
  createdAt?: string;
  updatedAt?: string;
  profile?: UserProfile;
}
```

### Create User Request
```typescript
// POST /api/users
{
  username: string; // Required
  email: string; // Required
  password: string; // Required
  role: 'user' | 'admin' | 'superadmin'; // Required
  mandantId?: number;
  mandantAccess?: number[];
}
```

### Update User Request
```typescript
// PATCH /api/users/:id
{
  email?: string;
  role?: string;
  mandantId?: number;
  mandantAccess?: number[];
  isActive?: boolean;
  // password is NOT updated via this endpoint
}
```

### Change Password Request
```typescript
// POST /api/users/:id/change-password
{
  currentPassword: string; // Required
  newPassword: string; // Required
}
```

## Settings Module

### Setting Schema
```typescript
{
  id?: number;
  category: string; // Required, e.g., 'data', 'ui', 'system'
  keyName: string; // Required, snake_case
  value: any; // JSON value, can be string, number, object, array
  userId?: number;
  mandantId?: number;
  createdAt?: string;
  updatedAt?: string;
}
```

### Create/Update Setting Request
```typescript
// POST /api/settings
// PUT /api/settings/:id
{
  category: string; // Required
  keyName: string; // Required (snake_case)
  value: any; // Required
  userId?: number;
  mandantId?: number;
}
```

### Settings Query
```typescript
// GET /api/settings
// Query parameters
{
  category?: string; // Filter by category
  userId?: number; // Filter by user
  mandantId?: number; // Filter by mandant
}
```

## Temperature Module

### Daily Outdoor Temperature Schema
```typescript
{
  id?: number;
  postalCode: string; // Required
  date: string; // Required, ISO date
  temperature: number; // Required, Celsius
  minTemperature?: number;
  maxTemperature?: number;
  avgTemperature?: number;
  resolution?: string; // 'daily', 'hourly'
  source?: string; // Data source
  createdAt?: string;
  updatedAt?: string;
}
```

### Temperature Efficiency Response
```typescript
// GET /api/temperature/efficiency/:objectId
{
  objectId: number;
  timeRange: string;
  data: Array<{
    date: string;
    outdoorTemp: number;
    consumption: number;
    efficiency: number; // Calculated metric
  }>;
}
```

## Health Module

### Health Check Response
```typescript
// GET /api/health
{
  status: 'healthy' | 'unhealthy';
  database: 'connected' | 'disconnected';
  timestamp: string; // ISO timestamp
  version: string; // e.g., '1.0.0'
  pool: {
    activeConnections: number;
    errorRate: number;
  };
}
```

### Connection Pool Stats Response
```typescript
// GET /api/health/pool
{
  timestamp: string;
  pool: {
    totalConnections: number;
    idleConnections: number;
    activeConnections: number;
    waitingClients: number;
    health: {
      healthy: boolean;
      errorRate: number;
      lastCheck: string;
    };
  };
}
```

## Admin Module

### Database Status Response
```typescript
// GET /api/admin/database/status
{
  settingdbOnline: boolean;
  settingdbError: string | null;
  portalDbOnline: boolean;
  portalDbError: string | null;
  usingFallback: boolean;
  dbSource: string; // 'environment_database_url', 'setup_app_json', etc.
  timestamp: string;
}
```

### Portal Config Response
```typescript
// GET /api/admin/portal/config
{
  settingdb_app: {
    ssl: boolean;
    host: string;
    port: number;
    table: string;
    schema: string;
    database: string;
    hasCredentials: boolean;
    source: string;
    connectionTimeout: number;
  };
}
```

### Test Connection Request
```typescript
// POST /api/admin/portal/test-connection
{
  host: string; // Required
  port: number; // Required
  database: string; // Required
  username: string; // Required
  password: string; // Required
  connectionTimeout?: number;
}
```

### Test Connection Response
```typescript
{
  success: boolean;
  message: string;
  details?: {
    host: string;
    port: number;
    database: string;
  };
}
```

## Mandants Module

### Mandant Schema
```typescript
{
  id?: number;
  name: string; // Required
  description?: string;
  contactPerson?: string;
  contactEmail?: string;
  contactPhone?: string;
  address?: string;
  city?: string;
  postalCode?: string;
  country?: string;
  isActive?: boolean;
  createdAt?: string;
  updatedAt?: string;
}
```

### Create/Update Mandant Request
```typescript
// POST /api/mandants
// PATCH /api/mandants/:id
{
  name: string; // Required for POST
  description?: string;
  contactPerson?: string;
  contactEmail?: string;
  contactPhone?: string;
  isActive?: boolean;
}
```

## Export Module

### Email Export Request
```typescript
// POST /api/export/send-email
{
  to: string | string[]; // Email recipient(s)
  subject: string;
  body?: string;
  pdfData: string; // Base64 encoded PDF
  filename?: string;
  cc?: string | string[];
  bcc?: string | string[];
}
```

## Validation Schemas

Validation is performed using Zod schemas in DTO files:
- `createUserSchema`: apps/backend-api/modules/users/dto/create-user.dto.ts
- `updateUserSchema`: apps/backend-api/modules/users/dto/update-user.dto.ts
- `createObjectSchema`: apps/backend-api/modules/objects/dto/create-object.dto.ts
- `updateObjectSchema`: apps/backend-api/modules/objects/dto/update-object.dto.ts
- `loginSchema`: apps/backend-api/modules/auth/dto/login.dto.ts

## BigInt Handling

JavaScript BigInt values are automatically converted to Number in JSON responses via global prototype modification:
```typescript
(BigInt.prototype as any).toJSON = function() { return Number(this); };
```

This ensures proper serialization of PostgreSQL bigint fields (like objectid).

## Date Handling

All dates are in ISO 8601 format:
- Request dates: `"2024-01-15T10:30:00.000Z"` or `"2024-01-15"`
- Response dates: `"2024-01-15T10:30:00.000Z"`

## JSON Fields

Several database fields store JSON data:
- `objects.meter`: `{ [meterKey: string]: string }`
- `objects.report`: `any`
- `settings.value`: `any`
- `monitoring_alerts.metadata`: `object`
- `users.mandantAccess`: `number[]`
