# Configuration Externalization Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: 12-Factor App methodology, configuration management patterns

## Overview

Configuration externalization separates configuration from code, following the 12-Factor App principle: "Store config in the environment". This enables the same codebase to run in multiple environments.

## Core Principles

1. **Strict Separation** - Config never in code
2. **Environment-Specific** - Different values per environment
3. **No Defaults for Secrets** - Require explicit values
4. **Fail Fast** - Validate at startup
5. **Centralized** - Single source of truth

## The 12-Factor Config Principle

### What is Configuration?
Anything that varies between environments:
- Database credentials
- API endpoints
- Feature flags
- Service URLs
- Resource limits
- Third-party credentials

### What is NOT Configuration?
Internal application structure:
- Routes
- Database schema
- Business logic
- UI components

## Configuration Patterns

### Pattern 1: Environment Variables
```bash
# Development
DATABASE_URL=postgresql://localhost/myapp_dev
API_URL=http://localhost:3000

# Production
DATABASE_URL=postgresql://prod-server/myapp_prod
API_URL=https://api.example.com
```

### Pattern 2: Config Files (Anti-pattern for Secrets)
```typescript
// config/development.ts
export default {
  apiUrl: 'http://localhost:3000',
  logLevel: 'debug',
  // Never put secrets here!
}
```

### Pattern 3: Config Service
```typescript
// TODO: Add config service pattern
// Centralized config management, feature flags
```

## Environment-Specific Configuration

### Development
```bash
NODE_ENV=development
DATABASE_URL=postgresql://localhost/myapp_dev
LOG_LEVEL=debug
ENABLE_DEBUG_TOOLS=true
CACHE_ENABLED=false
```

### Staging
```bash
NODE_ENV=staging
DATABASE_URL=postgresql://staging-db/myapp_staging
LOG_LEVEL=info
ENABLE_DEBUG_TOOLS=false
CACHE_ENABLED=true
```

### Production
```bash
NODE_ENV=production
DATABASE_URL=postgresql://prod-db/myapp_prod
LOG_LEVEL=error
ENABLE_DEBUG_TOOLS=false
CACHE_ENABLED=true
RATE_LIMIT_ENABLED=true
```

## Configuration Hierarchy

### Priority Order (highest to lowest)
1. Command-line arguments
2. Environment variables
3. Config files (.env)
4. Default values

```typescript
const port =
  process.argv.port ||           // CLI args
  process.env.PORT ||            // Env vars
  config.port ||                 // Config file
  3000                           // Default
```

## Feature Flags

### Environment-Based
```bash
FEATURE_NEW_UI=true
FEATURE_BETA_API=false
```

### Config Service
```typescript
// TODO: Add feature flag service
// LaunchDarkly, Unleash, custom service
```

## Configuration Validation

### Startup Validation
```typescript
import { z } from 'zod'

const configSchema = z.object({
  nodeEnv: z.enum(['development', 'staging', 'production']),
  databaseUrl: z.string().url(),
  apiUrl: z.string().url(),
  port: z.coerce.number(),
})

function loadConfig() {
  const result = configSchema.safeParse(process.env)

  if (!result.success) {
    console.error('Configuration validation failed')
    process.exit(1)
  }

  return result.data
}

export const config = loadConfig()
```

## Best Practices

1. Never commit secrets to version control
2. Use environment variables for all config
3. Validate configuration at startup
4. Provide .env.example template
5. Document all required variables
6. Use different configs per environment
7. Fail fast on invalid configuration
8. Keep configuration simple
9. Use type-safe configuration
10. Test with different configurations

## Anti-Patterns

### 1. Config in Code
```typescript
// Bad
const apiUrl = 'https://api.example.com'

// Good
const apiUrl = process.env.API_URL
```

### 2. Environment-Specific Code
```typescript
// Bad
if (process.env.NODE_ENV === 'production') {
  // Production-specific logic
}

// Good - use config
if (config.enableFeature) {
  // Feature logic
}
```

### 3. Default Secrets
```typescript
// Bad
const secret = process.env.JWT_SECRET || 'default_secret'

// Good
const secret = process.env.JWT_SECRET
if (!secret) {
  throw new Error('JWT_SECRET is required')
}
```

## Configuration Documentation

### README.md
```markdown
## Environment Variables

Required variables:
- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET` - Secret for JWT signing (min 32 chars)
- `API_URL` - Base URL for API

Optional variables:
- `PORT` - Server port (default: 3000)
- `LOG_LEVEL` - Logging level (default: info)
```

### .env.example
```bash
# Required
DATABASE_URL=
JWT_SECRET=
API_URL=

# Optional
PORT=3000
LOG_LEVEL=info
```

## Additional Resources

- [ENVIRONMENT_VARIABLES.md](./ENVIRONMENT_VARIABLES.md) - Env var patterns
- [CONFIG_VALIDATION.md](./CONFIG_VALIDATION.md) - Validation
- [SECRETS_MANAGEMENT.md](./SECRETS_MANAGEMENT.md) - Secrets
- [12-Factor App](https://12factor.net/config)
