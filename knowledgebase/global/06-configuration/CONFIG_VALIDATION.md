# Configuration Validation Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Runtime validation patterns, Zod best practices, fail-fast principles

## Overview

Configuration validation ensures your application receives valid configuration values at startup. Fail fast by validating early rather than discovering invalid config during runtime.

## Core Principles

1. **Validate Early** - At application startup
2. **Fail Fast** - Don't start with invalid config
3. **Type Safety** - Generate types from schemas
4. **Clear Errors** - Helpful validation messages
5. **Document Requirements** - Schema serves as documentation

## Validation with Zod

### Basic Schema
```typescript
import { z } from 'zod'

const configSchema = z.object({
  port: z.coerce.number().min(1).max(65535),
  nodeEnv: z.enum(['development', 'staging', 'production']),
  databaseUrl: z.string().url(),
  logLevel: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
})

type Config = z.infer<typeof configSchema>
```

### Advanced Validation
```typescript
const configSchema = z.object({
  // Email validation
  smtpUser: z.string().email(),

  // URL validation
  apiUrl: z.string().url(),

  // String patterns
  apiKey: z.string().regex(/^sk_[a-zA-Z0-9]{32}$/),

  // Number constraints
  maxConnections: z.number().int().positive().max(100),

  // Boolean coercion
  enableFeature: z.coerce.boolean(),

  // Optional with default
  timeout: z.number().optional().default(30000),

  // Conditional validation
  jwtSecret: z.string().min(32).refine(
    (val) => process.env.NODE_ENV !== 'production' || val.length >= 64,
    'JWT secret must be at least 64 characters in production'
  ),
})
```

### Nested Objects
```typescript
// TODO: Add nested config validation
// Database config, SMTP config as nested objects
```

### Array Validation
```typescript
// TODO: Add array validation
// CORS origins, allowed hosts
```

## Validation Strategies

### Strategy 1: Centralized Config Module
```typescript
// config/env.ts
import { z } from 'zod'

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'staging', 'production']),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
})

function validateEnv() {
  const parsed = envSchema.safeParse(process.env)

  if (!parsed.success) {
    console.error('Environment validation failed:')
    console.error(parsed.error.format())
    process.exit(1)
  }

  return parsed.data
}

export const env = validateEnv()
```

### Strategy 2: Lazy Validation
```typescript
// TODO: Add lazy validation pattern
// Validate on first access
```

### Strategy 3: Feature-Based Validation
```typescript
// TODO: Add feature-based config validation
// Separate schemas for database, auth, etc.
```

## Error Handling

### Detailed Error Messages
```typescript
const result = configSchema.safeParse(config)

if (!result.success) {
  const errors = result.error.format()

  // Pretty print errors
  console.error('Configuration validation failed:')
  console.error(JSON.stringify(errors, null, 2))

  // Or format for user
  result.error.issues.forEach(issue => {
    console.error(`${issue.path.join('.')}: ${issue.message}`)
  })

  process.exit(1)
}
```

### Custom Error Messages
```typescript
const schema = z.object({
  apiKey: z.string().min(32, {
    message: 'API key must be at least 32 characters. Generate one at https://example.com/api-keys'
  }),
})
```

## Type Generation

### Infer Types from Schema
```typescript
const configSchema = z.object({
  port: z.number(),
  host: z.string(),
})

// Automatically inferred type
type Config = z.infer<typeof configSchema>
// { port: number; host: string }
```

### Export Types
```typescript
// config/schema.ts
export const configSchema = z.object({...})
export type Config = z.infer<typeof configSchema>

// Usage
import type { Config } from './config/schema'
```

## Default Values

```typescript
const schema = z.object({
  // Simple default
  port: z.number().default(3000),

  // Conditional default
  logLevel: z.string().default(
    process.env.NODE_ENV === 'production' ? 'error' : 'debug'
  ),

  // Computed default
  maxConnections: z.number().default(() => {
    return process.env.NODE_ENV === 'production' ? 100 : 10
  }),
})
```

## Environment-Specific Validation

```typescript
// TODO: Add environment-specific rules
// Stricter validation in production
```

## Testing Configuration

```typescript
// TODO: Add config testing patterns
// Test validation, test defaults, test error cases
```

## Alternative Validation Libraries

### Joi
```typescript
// TODO: Add Joi example
```

### io-ts
```typescript
// TODO: Add io-ts example
```

### class-validator
```typescript
// TODO: Add class-validator example
```

## Best Practices

1. Validate at application startup
2. Fail fast with clear errors
3. Use strong typing
4. Provide sensible defaults
5. Document required vs optional
6. Test validation logic
7. Log validation errors clearly
8. Don't start with invalid config
9. Use schemas as documentation
10. Keep validation logic simple

## Additional Resources

- [ENVIRONMENT_VARIABLES.md](./ENVIRONMENT_VARIABLES.md) - Env var patterns
- [CONFIG_EXTERNALIZATION.md](./CONFIG_EXTERNALIZATION.md) - Config patterns
- [Zod Documentation](https://zod.dev/)
