# Environment Variables Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: 12-factor app methodology, environment variable security, Node.js best practices

## Overview

Environment variables externalize configuration from code, enabling the same codebase to run in different environments (development, staging, production) with different settings.

## Core Principles

1. **Separate Config from Code** - Never hardcode configuration
2. **Type Safety** - Validate and type environment variables
3. **Security** - Never commit secrets to version control
4. **Fail Fast** - Validate at application startup
5. **Documentation** - Document all required variables

## Basic Setup

### .env File (Development)
```bash
# Database
DATABASE_URL=postgresql://localhost:5432/myapp_dev
DATABASE_POOL_SIZE=10

# Server
PORT=3000
NODE_ENV=development
API_BASE_URL=http://localhost:3000

# Authentication
JWT_SECRET=your-dev-secret-key
SESSION_SECRET=your-session-secret

# External Services
SMTP_HOST=localhost
SMTP_PORT=1025
```

### .env.example (Template)
```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database
DATABASE_POOL_SIZE=10

# Server Configuration
PORT=3000
NODE_ENV=development|staging|production

# Authentication (Generate secure values for production)
JWT_SECRET=
SESSION_SECRET=

# External Services
SMTP_HOST=
SMTP_PORT=
```

### .gitignore
```
.env
.env.local
.env.*.local
```

## Loading Environment Variables

### Node.js with dotenv
```typescript
import 'dotenv/config'

// Or with explicit configuration
import dotenv from 'dotenv'
dotenv.config({ path: '.env' })
```

### Vite
```typescript
// vite.config.ts - Exposes VITE_ prefixed variables
export default defineConfig({
  define: {
    'process.env.VITE_API_URL': JSON.stringify(process.env.VITE_API_URL)
  }
})

// Usage in frontend
const apiUrl = import.meta.env.VITE_API_URL
```

### Next.js
```javascript
// TODO: Add Next.js env var patterns
// NEXT_PUBLIC_ prefix for client-side
```

## Type-Safe Environment Variables

### Validation with Zod
```typescript
import { z } from 'zod'

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'staging', 'production']),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  SMTP_HOST: z.string(),
  SMTP_PORT: z.coerce.number(),
  API_BASE_URL: z.string().url(),
})

export type Env = z.infer<typeof envSchema>

export function loadEnv(): Env {
  const result = envSchema.safeParse(process.env)

  if (!result.success) {
    console.error('Invalid environment variables:', result.error.format())
    throw new Error('Environment validation failed')
  }

  return result.data
}

// Usage
export const env = loadEnv()
```

### Type Declaration
```typescript
// env.d.ts
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      NODE_ENV: 'development' | 'staging' | 'production'
      PORT: string
      DATABASE_URL: string
      JWT_SECRET: string
      SMTP_HOST: string
      SMTP_PORT: string
    }
  }
}

export {}
```

## Environment-Specific Configuration

### Development (.env.development)
```bash
NODE_ENV=development
API_BASE_URL=http://localhost:3000
LOG_LEVEL=debug
```

### Staging (.env.staging)
```bash
NODE_ENV=staging
API_BASE_URL=https://staging-api.example.com
LOG_LEVEL=info
```

### Production (.env.production)
```bash
NODE_ENV=production
API_BASE_URL=https://api.example.com
LOG_LEVEL=error
```

## Naming Conventions

### Standard Naming
```bash
# Good: Clear, descriptive, consistent
DATABASE_URL=postgresql://localhost/db
REDIS_HOST=localhost
SMTP_PORT=587

# Bad: Inconsistent, unclear
db=postgresql://localhost/db
redis_host=localhost
SmtpPort=587
```

### Grouping by Service
```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USER=postgres
DB_PASSWORD=secret

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=noreply@example.com
SMTP_PASSWORD=secret
```

## Security Best Practices

### 1. Never Commit Secrets
```bash
# Always in .gitignore
.env
.env.local
.env.production
```

### 2. Use Secrets Manager in Production
```typescript
// TODO: Add AWS Secrets Manager example
// TODO: Add Azure Key Vault example
// TODO: Add HashiCorp Vault example
```

### 3. Rotate Secrets Regularly
Schedule regular rotation of:
- API keys
- Database passwords
- JWT secrets
- Encryption keys

### 4. Limit Secret Exposure
```typescript
// Don't log secrets
console.log(process.env.DATABASE_URL) // Bad!

// Don't expose in error messages
throw new Error(`Failed to connect to ${process.env.DATABASE_URL}`) // Bad!

// Sanitize before logging
const sanitizedUrl = process.env.DATABASE_URL?.replace(/:\/\/.*@/, '://***@')
console.log(`Database: ${sanitizedUrl}`)
```

## Frontend Environment Variables

### Vite
```bash
# Only VITE_ prefixed vars are exposed to client
VITE_API_URL=http://localhost:3000
VITE_ENABLE_ANALYTICS=true
VITE_APP_VERSION=1.0.0
```

```typescript
// Usage
const apiUrl = import.meta.env.VITE_API_URL
const isDev = import.meta.env.DEV
const isProd = import.meta.env.PROD
```

### Next.js
```bash
# NEXT_PUBLIC_ prefix for client-side
NEXT_PUBLIC_API_URL=http://localhost:3000
NEXT_PUBLIC_ANALYTICS_ID=G-XXXXXXXXXX

# Server-only (no prefix)
DATABASE_URL=postgresql://localhost/db
SECRET_KEY=server-only-secret
```

## Validation Strategies

### Early Validation (Recommended)
```typescript
// Validate at app startup
import { env } from './config/env'

async function bootstrap() {
  // env validation happens during import
  const app = createApp()
  await app.listen(env.PORT)
}

bootstrap()
```

### Lazy Validation
```typescript
// Validate on first access
class Config {
  private _validated = false

  get DATABASE_URL() {
    this.validate()
    return process.env.DATABASE_URL!
  }

  private validate() {
    if (this._validated) return
    // Validation logic
    this._validated = true
  }
}
```

## Default Values

```typescript
// Using Zod defaults
const envSchema = z.object({
  PORT: z.coerce.number().default(3000),
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
  ENABLE_CORS: z.coerce.boolean().default(false),
})

// Using fallback
const port = process.env.PORT || 3000
const logLevel = process.env.LOG_LEVEL || 'info'
```

## Common Patterns

### Pattern 1: Centralized Config Module
```typescript
// config/index.ts
// TODO: Add centralized config pattern
// Single source of truth for all config
```

### Pattern 2: Config by Feature
```typescript
// config/database.ts, config/auth.ts, etc.
// TODO: Add feature-based config organization
```

### Pattern 3: Config Factory
```typescript
// TODO: Add config factory pattern
// Different configs for different environments
```

## Testing with Environment Variables

### Override in Tests
```typescript
import { beforeEach, afterEach } from 'vitest'

let originalEnv: NodeJS.ProcessEnv

beforeEach(() => {
  originalEnv = { ...process.env }
  process.env.DATABASE_URL = 'postgresql://localhost/test_db'
  process.env.NODE_ENV = 'test'
})

afterEach(() => {
  process.env = originalEnv
})
```

### Test Configuration
```bash
# .env.test
NODE_ENV=test
DATABASE_URL=postgresql://localhost/test_db
LOG_LEVEL=silent
```

## CI/CD Configuration

### GitHub Actions
```yaml
env:
  NODE_ENV: production
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  JWT_SECRET: ${{ secrets.JWT_SECRET }}
```

### Docker
```dockerfile
# Pass env vars at runtime
docker run -e DATABASE_URL=... -e JWT_SECRET=... myapp
```

## Common Mistakes

### 1. Committing .env Files
```bash
# Bad: .env is committed
# Good: .env in .gitignore, .env.example committed
```

### 2. No Validation
```typescript
// Bad: Using env vars without validation
const port = process.env.PORT

// Good: Validated and typed
const port = env.PORT // Type-safe after validation
```

### 3. Exposing Secrets in Frontend
```bash
# Bad: Secrets in frontend env vars
VITE_DATABASE_PASSWORD=secret

# Good: Only public values
VITE_API_URL=https://api.example.com
```

## Tools and Libraries

### Loading
- dotenv - Load .env files
- dotenv-expand - Variable expansion
- dotenv-cli - CLI tool

### Validation
- Zod - Schema validation
- envalid - Env validation library
- joi - Alternative validator

### Management
- direnv - Auto-load env vars
- doppler - Secrets management
- infisical - Open source secrets

## Best Practices Checklist

- [ ] .env files in .gitignore
- [ ] .env.example committed
- [ ] All env vars validated at startup
- [ ] Type-safe env var access
- [ ] Secrets never logged
- [ ] Different configs per environment
- [ ] Fail fast on invalid config
- [ ] Document required variables
- [ ] Use secrets manager in production
- [ ] Regular secret rotation

## Additional Resources

- [CONFIG_VALIDATION.md](./CONFIG_VALIDATION.md) - Validation patterns
- [SECRETS_MANAGEMENT.md](./SECRETS_MANAGEMENT.md) - Secret storage
- [CI_CD_PATTERNS.md](./CI_CD_PATTERNS.md) - CI/CD configuration
- [12-Factor App Config](https://12factor.net/config)
