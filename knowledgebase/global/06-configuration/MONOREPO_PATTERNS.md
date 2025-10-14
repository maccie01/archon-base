# Monorepo Patterns Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Turborepo, Nx, monorepo architecture patterns

## Overview

A monorepo contains multiple related projects in a single repository, sharing code, tooling, and workflows. This enables better code reuse and consistent development practices.

## Core Principles

1. **Workspace Management** - Organize multiple packages
2. **Code Sharing** - Shared packages and utilities
3. **Task Orchestration** - Efficient build and test
4. **Caching** - Speed up repeated operations
5. **Consistent Tooling** - Same tools across packages

## Monorepo Structure

### Typical Layout
```
monorepo/
├── apps/
│   ├── frontend-web/
│   ├── frontend-mobile/
│   └── backend-api/
├── packages/
│   ├── shared-types/
│   ├── shared-utils/
│   ├── shared-validation/
│   └── ui-components/
├── config/
│   ├── eslint/
│   ├── typescript/
│   └── testing/
├── docs/
├── scripts/
├── package.json
└── turbo.json
```

## Turborepo (Recommended)

### Setup
```bash
npm install -D turbo
```

### turbo.json
```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    },
    "lint": {
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

### Running Tasks
```bash
# Run in all packages
turbo run build
turbo run test
turbo run lint

# Run in specific package
turbo run build --filter=frontend-web

# Run with dependencies
turbo run build --filter=...frontend-web
```

## Package Management

### Root package.json
```json
{
  "name": "monorepo",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "dev": "turbo run dev",
    "build": "turbo run build",
    "test": "turbo run test",
    "lint": "turbo run lint"
  }
}
```

### Package package.json
```json
{
  "name": "@myapp/shared-types",
  "version": "1.0.0",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch"
  }
}
```

## Shared Packages

### Shared Types
```typescript
// packages/shared-types/src/index.ts
export interface User {
  id: string
  email: string
  name: string
}

export interface ApiResponse<T> {
  data: T
  error?: string
}
```

### Shared Utils
```typescript
// packages/shared-utils/src/index.ts
export function formatDate(date: Date): string {
  return date.toISOString()
}

export function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}
```

## TypeScript Configuration

### Root tsconfig.json
```json
{
  "files": [],
  "references": [
    { "path": "./apps/frontend-web" },
    { "path": "./apps/backend-api" },
    { "path": "./packages/shared-types" }
  ]
}
```

### Package tsconfig.json
```json
{
  "extends": "../../config/typescript/base.json",
  "compilerOptions": {
    "composite": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src"],
  "references": [
    { "path": "../shared-types" }
  ]
}
```

## Dependency Management

### Internal Dependencies
```json
{
  "dependencies": {
    "@myapp/shared-types": "workspace:*",
    "@myapp/shared-utils": "workspace:*"
  }
}
```

### Version Management
```bash
# Update all packages
npm update --workspaces

# Update specific workspace
npm update --workspace=apps/frontend-web
```

## Build Optimization

### Turborepo Caching
```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"],
      "cache": true
    }
  }
}
```

### Parallel Execution
```bash
# Run in parallel
turbo run build --parallel

# Limit concurrency
turbo run build --concurrency=4
```

## Testing in Monorepo

### Shared Test Config
```typescript
// config/testing/vitest.config.ts
export default defineConfig({
  test: {
    globals: true,
    environment: 'node'
  }
})
```

### Package Test Config
```typescript
// apps/backend-api/vitest.config.ts
import baseConfig from '../../config/testing/vitest.config'

export default defineConfig({
  ...baseConfig,
  test: {
    ...baseConfig.test,
    include: ['**/*.test.ts']
  }
})
```

## Shared Configuration

### ESLint
```javascript
// config/eslint/base.js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended'
  ],
  parser: '@typescript-eslint/parser'
}
```

### Prettier
```json
// config/prettier/base.json
{
  "semi": true,
  "singleQuote": true,
  "printWidth": 100
}
```

## CI/CD for Monorepo

```yaml
# TODO: Add Turborepo CI example
# Selective testing, caching, affected detection
```

## Best Practices

1. Use Turborepo for task orchestration
2. Share configuration across packages
3. Leverage caching for speed
4. Use TypeScript project references
5. Version internal packages consistently
6. Document package dependencies
7. Keep shared packages focused
8. Use workspace protocol for internal deps
9. Run tasks selectively
10. Monitor build times

## Common Patterns

### Pattern 1: App + Packages
```
apps/       - Deployable applications
packages/   - Shared libraries
```

### Pattern 2: Feature Packages
```
packages/
  - feature-auth/
  - feature-dashboard/
  - feature-reports/
```

### Pattern 3: Layer-Based
```
packages/
  - domain/      - Business logic
  - application/ - Use cases
  - infrastructure/ - Implementation
```

## Tools Comparison

### Turborepo
- Fast
- Simple
- Great caching
- Good for most projects

### Nx
- Powerful
- Feature-rich
- Steeper learning curve
- Better for large projects

### Lerna (Legacy)
- Older tool
- More configuration
- Consider Turborepo instead

## Additional Resources

- [BUILD_CONFIGURATION.md](./BUILD_CONFIGURATION.md) - Build setup
- [CI_CD_PATTERNS.md](./CI_CD_PATTERNS.md) - CI/CD
- [Turborepo Documentation](https://turbo.build/)
