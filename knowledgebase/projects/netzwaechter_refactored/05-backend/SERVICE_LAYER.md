# Service Layer Documentation

Created: 2025-10-13

## Overview

The Service Layer implements business logic, validation rules, and orchestrates data operations. It sits between Controllers (HTTP layer) and Repositories (data layer).

## Service Layer Responsibilities

1. **Business Logic**: Implement domain-specific rules and calculations
2. **Validation**: Validate input data against business rules
3. **Orchestration**: Coordinate between multiple repositories
4. **Transformation**: Transform data between layers
5. **Error Handling**: Throw descriptive business errors

## Standard Service Pattern

### Class Structure

```typescript
import { [module]Repository } from "./[module].repository";
import type { [Entity], Insert[Entity] } from "@shared/schema";

/**
 * [Module] Service
 *
 * Business logic layer for [module] operations.
 * Handles validation, business rules, and delegates CRUD to repository.
 */
export class [Module]Service {
  // ============================================================================
  // PUBLIC METHODS - Business Operations
  // ============================================================================

  /**
   * Get all [entities] with validation
   * @returns Array of [Entity] records
   */
  async getAll(): Promise<[Entity][]> {
    return await [module]Repository.getAll();
  }

  /**
   * Create [entity] with validation
   * @param data - Entity data to create
   * @returns Created [Entity] record
   */
  async create(data: Insert[Entity]): Promise<[Entity]> {
    // Validate business rules
    this.validateEntityData(data);

    return await [module]Repository.create(data);
  }

  // ============================================================================
  // PRIVATE METHODS - Validation Helpers
  // ============================================================================

  /**
   * Validate entity data
   * @param data - Entity data to validate
   * @throws Error if validation fails
   */
  private validateEntityData(data: Insert[Entity]): void {
    if (!data.name) {
      throw new Error('Name is required');
    }
    // More validation...
  }
}

// Singleton instance
export const [module]Service = new [Module]Service();
```

## Existing Services Analysis

### Complete Services (7 modules)

#### 1. Settings Service

**File**: `modules/settings/settings.service.ts`

**Complexity**: High - Comprehensive validation

**Key Features**:
- Filter validation (category, user_id, mandant_id)
- Field validation (category regex, key name format)
- Type validation (user ID, mandant ID)
- JSON serialization validation

**Validation Methods**:
```typescript
private validateSettingCategory(category: string): void
private validateSettingKey(keyName: string): void
private validateUserId(userId: string): void
private validateMandantId(mandantId: number): void
private validateSettingId(id: number): void
private validateSettingData(settingData: InsertSettings): void
private validatePartialSettingData(settingData: Partial<InsertSettings>): void
```

**Business Logic**:
- Settings filtering with multiple criteria
- Partial updates with field-level validation
- Clear all settings (superadmin only - validated in controller)

**Dependencies**: settingsRepository

#### 2. Monitoring Service

**File**: `modules/monitoring/monitoring.service.ts`

**Complexity**: Medium - Validation + orchestration

**Key Features**:
- Dashboard KPI aggregation
- Critical systems filtering
- Energy classification
- System alerts management

**Validation Methods**:
```typescript
private validateSystemId(systemId: number): void
private validateAlertId(id: number): void
private validateUserId(userId: string): void
private validateMandantIds(mandantIds: number[]): void
private validateAlertData(alertData: any): void
```

**Business Logic**:
- Mandant-scoped data access
- Alert severity validation
- System classification by energy consumption
- Dashboard metrics calculation

**Dependencies**: monitoringRepository

#### 3. Energy Service

**File**: `modules/energy/energy.service.ts`

**Complexity**: High - Multiple data sources + complex calculations

**Key Features**:
- Day compensation data management
- Daily consumption calculations
- External energy database integration
- Multi-meter data aggregation

**Business Operations**:
```typescript
getDayCompData(objectId: number, startDate?: Date, endDate?: Date)
getLatestDayCompData(objectId: number)
getDailyConsumption(objectId: number, startDate?: Date, endDate?: Date)
getEnergyDataExternal(objectId: number, limit: number)
getEnergyDataForAllMeters(objectId: number, meterData: any, timeRange?: string)
getEnergyDataForSpecificMeter(meterId: number, objectId: number, from: Date | null, to: Date | null)
getEnergyDataForObject(objectId: number, startDate?: string, endDate?: string, timeRange?: string)
getDailyConsumptionData(objectId: number, timeRange: string)
```

**Dependencies**: energyRepository

#### 4. Logbook Service

**File**: `modules/logbook/logbook.service.ts`

**Complexity**: Medium - Validation + filtering

**Key Features**:
- Activity log management
- User action tracking
- Mandant filtering

**Validation Methods**:
```typescript
private validateLogId(id: number): void
private validateUserId(userId: string): void
private validateMandantId(mandantId: number): void
private validateLogData(logData: InsertLogbook): void
```

**Business Logic**:
- Log filtering by user, mandant, date range
- Log entry validation
- Batch log retrieval

**Dependencies**: logbookRepository

#### 5. Users Service

**File**: `modules/users/users.service.ts`

**Complexity**: Medium - User management + validation

**Key Features**:
- User CRUD operations
- Password validation (if implemented)
- Role validation

**Dependencies**: usersRepository

#### 6. Objects Service

**File**: `modules/objects/objects.service.ts`

**Complexity**: Medium - Object management + mandant rules

**Key Features**:
- Object CRUD operations
- Mandant access validation
- Object status management

**Dependencies**: objectsRepository

#### 7. Auth Service

**File**: `modules/auth/auth.service.ts`

**Complexity**: High - Authentication logic

**Key Features**:
- User authentication
- Session management
- Password hashing/verification
- Token generation (if used)

**Dependencies**: authRepository

## Service Layer Patterns

### Pattern 1: Simple Pass-Through

**When to use**: No business logic needed, just delegation

```typescript
async getAll(): Promise<Entity[]> {
  return await entityRepository.getAll();
}
```

**Modules using this**: health, database (would use if service existed)

### Pattern 2: Validation Before Delegation

**When to use**: Input validation required before data access

```typescript
async create(data: InsertEntity): Promise<Entity> {
  // Validate
  this.validateEntityData(data);

  // Delegate
  return await entityRepository.create(data);
}
```

**Modules using this**: settings, logbook, monitoring

### Pattern 3: Orchestration Between Multiple Repositories

**When to use**: Operation requires data from multiple sources

```typescript
async getCompleteObjectData(objectId: number): Promise<CompleteObject> {
  // Get from multiple repositories
  const object = await objectsRepository.getById(objectId);
  const energy = await energyRepository.getForObject(objectId);
  const logs = await logbookRepository.getForObject(objectId);

  // Combine and return
  return {
    ...object,
    energyData: energy,
    recentLogs: logs
  };
}
```

**Modules using this**: energy (partially), objects (could use)

### Pattern 4: Business Calculations

**When to use**: Complex calculations based on retrieved data

```typescript
async calculateEfficiency(objectId: number, timeRange: string): Promise<Efficiency> {
  // Get data
  const object = await objectsRepository.getById(objectId);
  const energyData = await energyRepository.getEnergyData(objectId, timeRange);

  // Calculate
  const area = this.extractArea(object);
  const consumption = this.sumConsumption(energyData);
  const efficiency = consumption / area;

  return {
    objectId,
    area,
    consumption,
    efficiency,
    unit: 'kWh/m²/Jahr'
  };
}
```

**Modules needing this**: efficiency (currently in controller!)

### Pattern 5: Mandant-Scoped Access Control

**When to use**: Multi-tenant data isolation required

```typescript
async getForUser(userId: string, filters: Filters): Promise<Entity[]> {
  // Get user's mandant IDs
  const user = await usersRepository.getById(userId);

  // Add mandant filter
  const scopedFilters = {
    ...filters,
    mandantIds: user.mandantIds
  };

  return await entityRepository.getWithFilters(scopedFilters);
}
```

**Modules using this**: monitoring, objects (partially)

## Validation Patterns

### Basic Field Validation

```typescript
private validateEntityName(name: string): void {
  if (!name || typeof name !== 'string') {
    throw new Error('Name is required and must be a string');
  }

  if (name.length > 255) {
    throw new Error('Name must not exceed 255 characters');
  }

  if (name.length < 3) {
    throw new Error('Name must be at least 3 characters');
  }
}
```

### Regex Validation

```typescript
private validateCategory(category: string): void {
  const categoryRegex = /^[a-zA-Z0-9_-]+$/;
  if (!categoryRegex.test(category)) {
    throw new Error('Category must contain only alphanumeric characters, underscores, and hyphens');
  }
}
```

### ID Validation

```typescript
private validateId(id: number): void {
  if (!Number.isInteger(id) || id <= 0) {
    throw new Error('ID must be a positive integer');
  }
}
```

### Complex Object Validation

```typescript
private validateSettingData(data: InsertSettings): void {
  // Required fields
  if (!data.category) throw new Error('Category is required');
  if (!data.key_name) throw new Error('Key name is required');
  if (data.value === undefined) throw new Error('Value is required');

  // Field validation
  this.validateCategory(data.category);
  this.validateKeyName(data.key_name);

  // Optional field validation
  if (data.user_id) this.validateUserId(data.user_id);
  if (data.mandant_id) this.validateMandantId(data.mandant_id);

  // JSON serialization check
  try {
    JSON.stringify(data.value);
  } catch (error) {
    throw new Error('Value must be JSON-serializable');
  }
}
```

## Service Dependencies

### Typical Imports

```typescript
import { [module]Repository } from "./[module].repository";
import type { [Entity], Insert[Entity] } from "@shared/schema";
import type { [Module]Filters } from "./[module].types";
```

### Cross-Module Dependencies

Some services may depend on repositories from other modules:

```typescript
// Example: Efficiency service needs energy repository
import { energyRepository } from "../energy/energy.repository";
import { objectsRepository } from "../objects/objects.repository";
```

**Current cross-module dependencies**:
- efficiency → energy (for external DB settings)
- efficiency → objects (for object data)
- monitoring → objects (for mandant filtering)

## Shared Service Utilities

### None Currently

There are no shared service utilities or base classes. Each service is independent.

**Opportunity**: Create a `BaseService` class with common validation methods:
```typescript
export abstract class BaseService {
  protected validateId(id: number): void {
    if (!Number.isInteger(id) || id <= 0) {
      throw new Error('ID must be a positive integer');
    }
  }

  protected validateString(value: string, fieldName: string, maxLength: number = 255): void {
    if (!value || typeof value !== 'string') {
      throw new Error(`${fieldName} is required and must be a string`);
    }
    if (value.length > maxLength) {
      throw new Error(`${fieldName} must not exceed ${maxLength} characters`);
    }
  }

  // More common validators...
}
```

## Service Testing Patterns

Services should be tested in isolation with mocked repositories:

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { settingsService } from './settings.service';
import { settingsRepository } from './settings.repository';

// Mock repository
vi.mock('./settings.repository', () => ({
  settingsRepository: {
    getSettings: vi.fn(),
    createSetting: vi.fn(),
  }
}));

describe('SettingsService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('getSettings', () => {
    it('should validate category and call repository', async () => {
      const mockSettings = [{ id: 1, category: 'test', key_name: 'key', value: 'val' }];
      vi.mocked(settingsRepository.getSettings).mockResolvedValue(mockSettings);

      const result = await settingsService.getSettings({ category: 'test' });

      expect(settingsRepository.getSettings).toHaveBeenCalledWith({ category: 'test' });
      expect(result).toEqual(mockSettings);
    });

    it('should throw error for invalid category', async () => {
      await expect(
        settingsService.getSettings({ category: 'invalid@category' })
      ).rejects.toThrow('Category must contain only alphanumeric characters');
    });
  });
});
```

## Missing Services - Refactoring Candidates

### High Priority

**efficiency module** - Currently 380 lines in controller
```typescript
// Needs: EfficiencyService
export class EfficiencyService {
  async getEfficiencyAnalysis(objectId: number, timeRange: string, resolution: string, user: User) {
    // Validate access
    // Get object and meter data
    // Get external energy data
    // Calculate efficiency
  }

  private validateUserAccess(user: User, object: Object): void
  private extractNetMeterId(object: Object): number
  private calculateArea(object: Object): number
  private calculateEfficiency(energyData: any[], area: number): EfficiencyData
}
```

**ki-reports module** - Currently 280 lines in controller
```typescript
// Needs: KiReportsService
export class KiReportsService {
  async generateReport(objectId: number, reportType: string) {
    // Validate inputs
    // Get object data
    // Generate report
  }
}
```

### Medium Priority

**temperature module**
```typescript
export class TemperatureService {
  async getTemperatureData(objectId: number, startDate: Date, endDate: Date) {
    this.validateDateRange(startDate, endDate);
    return await temperatureRepository.getForObject(objectId, startDate, endDate);
  }
}
```

**weather module**
```typescript
export class WeatherService {
  async getWeatherData(location: string, date: Date) {
    this.validateLocation(location);
    return await weatherRepository.getForLocation(location, date);
  }
}
```

**todo-tasks module**
```typescript
export class TodoTasksService {
  async createTask(taskData: InsertTask, userId: string) {
    this.validateTaskData(taskData);
    taskData.userId = userId;
    return await todoTasksRepository.create(taskData);
  }
}
```

**admin module**
```typescript
export class AdminService {
  async getAllUsers(adminUser: User) {
    this.validateAdminAccess(adminUser);
    return await adminRepository.getAllUsers();
  }
}
```

## Service Layer Best Practices

### DO:
1. ✅ Validate all input data
2. ✅ Use private methods for validation helpers
3. ✅ Throw descriptive errors
4. ✅ Include JSDoc comments
5. ✅ Export as singleton instance
6. ✅ Use TypeScript types from @shared/schema
7. ✅ Keep methods focused and single-purpose
8. ✅ Test services in isolation

### DON'T:
1. ❌ Access HTTP req/res objects
2. ❌ Execute direct database queries
3. ❌ Handle HTTP status codes
4. ❌ Include presentation logic
5. ❌ Mix concerns between methods
6. ❌ Use console.log for errors (throw instead)
7. ❌ Skip validation "for performance"
8. ❌ Return raw database errors to caller

## Conclusion

The service layer is well-implemented in 7 out of 23 modules (30%). The pattern is solid and should be extended to all remaining modules. The `settings` and `monitoring` services are exemplary implementations that should be used as templates for creating missing services.

**Key recommendation**: Extract business logic from fat controllers (efficiency, ki-reports) into dedicated service classes following the established patterns.
