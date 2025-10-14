# Quick Technology Reference

Created: 2025-10-13

This is a quick reference guide for the most commonly used technologies across all projects. For detailed analysis, see [TECHNOLOGY_ANALYSIS.md](./TECHNOLOGY_ANALYSIS.md).

## Most Used Technologies

### Frontend (5+ projects)
- React 18.3.1
- Vite 5.4.19
- Tailwind CSS 3.4+

### Backend (6+ projects)
- Express.js 4.21+
- TypeScript 5.6+
- Node.js (ESM modules)

### Database (3+ projects)
- PostgreSQL
- Drizzle ORM 0.39+

### Testing (2+ projects)
- Vitest 3.2+
- Playwright
- Jest

### UI Libraries (2+ projects)
- Radix UI (headless components)
- Lucide React (icons)
- Framer Motion (animations)

## Standard Tech Stack

### Recommended for New Projects
```
Frontend:
├── React 18
├── Vite 5
├── TypeScript 5.6
├── Tailwind CSS 3.4
├── Radix UI
├── TanStack Query
└── React Hook Form + Zod

Backend:
├── Express.js 4.21
├── TypeScript (ESM)
├── Drizzle ORM
├── PostgreSQL
├── express-session
└── Zod validation

Monorepo:
├── Turborepo
├── pnpm workspaces
└── Shared packages

Testing:
├── Vitest (unit/integration)
├── Playwright (E2E)
└── MSW (API mocking)
```

## Common Patterns

### 1. Authentication
- **Session-based**: express-session + connect-pg-simple
- **Password hashing**: bcrypt/bcryptjs
- **Alternative**: JWT (jsonwebtoken) for older projects

### 2. Database Schema
```typescript
// Using Drizzle ORM
import { pgTable, serial, text, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: text('email').notNull().unique(),
  password: text('password').notNull(),
  createdAt: timestamp('created_at').defaultNow()
});
```

### 3. Validation
```typescript
// Using Zod
import { z } from 'zod';

export const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
});
```

### 4. API Routes
```typescript
// Express.js pattern
import express from 'express';

const router = express.Router();

router.get('/api/users', async (req, res) => {
  // Handler logic
});

export default router;
```

### 5. React Components
```typescript
// Modern React pattern with TypeScript
import { useState } from 'react';
import { Button } from '@/components/ui/button';

interface Props {
  title: string;
}

export function Component({ title }: Props) {
  const [state, setState] = useState('');

  return (
    <div>
      <h1>{title}</h1>
      <Button>Click me</Button>
    </div>
  );
}
```

## File Structure (Monorepo)

```
project-root/
├── apps/
│   ├── frontend-web/
│   │   ├── src/
│   │   ├── package.json
│   │   └── vite.config.ts
│   └── backend-api/
│       ├── modules/
│       ├── package.json
│       └── index.ts
├── packages/
│   ├── shared-types/
│   ├── shared-validation/
│   └── shared-utils/
├── config/
│   ├── build/
│   └── testing/
├── scripts/
├── .env
├── package.json
├── pnpm-workspace.yaml
└── turbo.json
```

## Configuration Files

### package.json (Root)
```json
{
  "name": "project-name",
  "type": "module",
  "packageManager": "pnpm@10.2.0",
  "scripts": {
    "dev": "turbo run dev",
    "build": "turbo run build",
    "test": "turbo run test"
  }
}
```

### pnpm-workspace.yaml
```yaml
packages:
  - "apps/*"
  - "packages/*"
```

### turbo.json
```json
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "test": {
      "dependsOn": ["build"]
    }
  }
}
```

### tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
```

## Common Commands

### Development
```bash
pnpm dev              # Start development server
pnpm build            # Build for production
pnpm test             # Run tests
pnpm typecheck        # Check TypeScript types
pnpm lint             # Lint code
```

### Database
```bash
pnpm db:push          # Push schema changes (Drizzle)
pnpm db:generate      # Generate migrations
pnpm db:migrate       # Run migrations
```

### Testing
```bash
pnpm test:unit        # Unit tests
pnpm test:integration # Integration tests
pnpm test:e2e         # End-to-end tests
pnpm test:coverage    # With coverage report
```

## Environment Variables

### Standard .env Structure
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Session
SESSION_SECRET=your-secret-key

# API Keys
OPENAI_API_KEY=sk-...
SENDGRID_API_KEY=...

# Environment
NODE_ENV=development
PORT=3000
```

## Package Versions Reference

### Critical Dependencies
```json
{
  "dependencies": {
    "react": "^18.3.1",
    "express": "^4.21.2",
    "drizzle-orm": "^0.39.1",
    "zod": "^3.25.76",
    "@tanstack/react-query": "^5.60.5",
    "pg": "^8.16.3"
  },
  "devDependencies": {
    "typescript": "5.6.3",
    "vite": "^5.4.19",
    "vitest": "^3.2.4",
    "@playwright/test": "^1.56.0",
    "tailwindcss": "^3.4.17"
  }
}
```

## Security Checklist

- [ ] Use express-helmet for security headers
- [ ] Implement rate limiting (express-rate-limit)
- [ ] Hash passwords with bcrypt (cost factor 10+)
- [ ] Use parameterized queries (Drizzle ORM handles this)
- [ ] Validate all inputs with Zod
- [ ] Enable CORS only for specific origins
- [ ] Use HTTPS in production
- [ ] Store secrets in environment variables
- [ ] Implement CSRF protection for session-based auth
- [ ] Keep dependencies updated

## Performance Checklist

- [ ] Use Vite for fast HMR in development
- [ ] Enable build-time optimizations (tree-shaking, minification)
- [ ] Implement code splitting
- [ ] Use TanStack Query for data fetching and caching
- [ ] Optimize images and assets
- [ ] Enable gzip/brotli compression
- [ ] Use connection pooling for database
- [ ] Implement pagination for large datasets
- [ ] Cache static assets with long TTL
- [ ] Monitor bundle size

## Testing Strategy

### Unit Tests (Vitest)
- Test business logic in isolation
- Mock external dependencies
- Aim for 80%+ coverage of critical paths

### Integration Tests (Vitest + MSW)
- Test API endpoints with mocked HTTP requests
- Test database interactions with test database
- Test authentication flows

### E2E Tests (Playwright)
- Test critical user journeys
- Test across different browsers
- Run in CI/CD pipeline before deployment

## Documentation Structure

### In-Code Documentation
```typescript
/**
 * Authenticates user and creates session
 * @param email - User email address
 * @param password - Plain text password
 * @returns User object without password
 * @throws {Error} If credentials are invalid
 */
async function login(email: string, password: string) {
  // Implementation
}
```

### API Documentation
Consider using:
- OpenAPI/Swagger for REST APIs
- JSDoc for internal functions
- README.md for setup and usage

## Common Pitfalls

1. **ESM vs CommonJS**: Use `"type": "module"` in package.json
2. **Path aliases**: Configure in both tsconfig.json and vite.config.ts
3. **Environment variables**: Use `--env-file=.env` with tsx in development
4. **Database connections**: Always close connections properly
5. **Session storage**: Use connect-pg-simple for PostgreSQL, not memory store
6. **Type imports**: Use `import type` for type-only imports
7. **Build output**: Clean dist/ before building
8. **Dependencies**: Keep shared packages in sync across monorepo

## Upgrade Path from Legacy Projects

### From Sequelize to Drizzle ORM
1. Keep both ORMs temporarily
2. Create Drizzle schema matching Sequelize models
3. Migrate routes one by one
4. Remove Sequelize when complete

### From Jest to Vitest
1. Install Vitest and @vitest/ui
2. Update test scripts in package.json
3. Minimal changes to test files needed
4. Update mocking syntax if needed

### From Webpack to Vite
1. Remove webpack config
2. Add vite.config.ts
3. Update imports (no need for `require`)
4. Use `import.meta.env` instead of `process.env`

## Resources

### Official Documentation
- React: https://react.dev
- Vite: https://vitejs.dev
- Drizzle ORM: https://orm.drizzle.team
- Vitest: https://vitest.dev
- Playwright: https://playwright.dev
- Tailwind CSS: https://tailwindcss.com
- Radix UI: https://www.radix-ui.com
- TanStack Query: https://tanstack.com/query

### Project References
- **Modern full-stack**: /monitoring_firma/netzwaechter-refactored
- **Next.js + Supabase**: /Nexorithm-website
- **AI/LangChain**: /Perplexica
- **Data science**: /tawian/dhbw-tp-forecasting

## Getting Help

1. Check [TECHNOLOGY_ANALYSIS.md](./TECHNOLOGY_ANALYSIS.md) for detailed patterns
2. Review reference project implementations
3. Consult official documentation
4. Check GitHub issues for known problems
5. Use TypeScript types for inline documentation

---

Last updated: 2025-10-13
Next review: When new projects are added or major versions change
