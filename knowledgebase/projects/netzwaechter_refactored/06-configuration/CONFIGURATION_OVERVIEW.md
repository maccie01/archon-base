# Configuration Overview

## Project Information

**Project Name:** Netzwächter (Network Guardian)
**Type:** Energy Monitoring & Management Portal
**Architecture:** Monorepo (Turborepo)
**Package Manager:** pnpm 10.2.0
**License:** MIT

Created: 2025-10-13
Last Updated: 2025-10-13

---

## Monorepo Structure

### Root Level
```
netzwaechter-refactored/
├── apps/                    # Application packages
│   ├── backend-api/        # Express.js REST API server
│   └── frontend-web/       # React + Vite frontend
├── packages/               # Shared packages
│   ├── shared-types/      # TypeScript types & Drizzle schemas
│   ├── shared-validation/ # Zod validation schemas
│   └── shared-utils/      # Utility functions
├── config/                # Configuration files
│   ├── build/            # Build configs (Vite, Drizzle)
│   ├── docker/           # Docker & deployment configs
│   ├── testing/          # Test configs (Vitest, Playwright)
│   ├── tooling/          # Tool configs (Tailwind, PostCSS)
│   └── turbo/            # Turborepo cache
├── db/                   # Database migrations
├── docs/                 # Documentation
├── scripts/             # Build & development scripts
└── testing/             # Test results & coverage
```

### Application Packages

#### Backend API (apps/backend-api)
- **Technology:** Node.js 20+ with Express.js
- **Language:** TypeScript (ESM)
- **Purpose:** REST API server for energy monitoring
- **Structure:** Modular architecture with feature-based organization
- **Modules:**
  - `admin/` - Admin management
  - `auth/` - Authentication & authorization
  - `database/` - Database utilities
  - `efficiency/` - Efficiency calculations
  - `energy/` - Energy data management
  - `export/` - Data export functionality
  - `health/` - Health checks & monitoring
  - `ki-reports/` - AI-powered reports
  - `logbook/` - Maintenance logbook
  - `mandants/` - Multi-tenancy management
  - `monitoring/` - Real-time monitoring
  - `object-groups/` - Object grouping
  - `objects/` - Object management
  - `settings/` - System settings
  - `setup/` - Initial setup
  - `weather/` - Weather data integration

#### Frontend Web (apps/frontend-web)
- **Technology:** React 18 + Vite
- **Language:** TypeScript
- **Purpose:** Web-based user interface
- **UI Framework:** Radix UI + Tailwind CSS
- **Features:**
  - Dashboard & monitoring views
  - Energy data visualization (Recharts)
  - Interactive maps (Leaflet)
  - Real-time updates (WebSocket)
  - Multi-tenancy support
  - Role-based access control

### Shared Packages

#### @netzwaechter/shared-types
- **Purpose:** Shared TypeScript types and database schemas
- **Technology:** Drizzle ORM
- **Contents:**
  - Database schema definitions
  - TypeScript type exports
  - Zod insert schemas
- **Main Files:**
  - `schema.ts` - Complete database schema
  - `index.ts` - Type exports

#### @netzwaechter/shared-validation
- **Purpose:** Validation schemas for API requests
- **Technology:** Zod
- **Contents:**
  - Input validation schemas
  - Form validation schemas
  - API request/response schemas

#### @netzwaechter/shared-utils
- **Purpose:** Shared utility functions
- **Technology:** TypeScript
- **Contents:**
  - Date/time utilities (date-fns)
  - Common helper functions
  - Formatting utilities

---

## Build System

### Turborepo Configuration

**File:** `turbo.json`

**Key Features:**
- Task orchestration
- Incremental builds
- Shared caching
- Parallel execution

**Tasks:**
- `build` - Build all packages
- `test` - Run all tests
- `typecheck` - TypeScript validation
- `lint` - Code linting
- `dev` - Development servers

**Cache Directory:** `config/turbo/cache/`

**Global Dependencies:**
- `.env`
- `tsconfig.json`
- `vite.config.ts`
- `vitest.config.ts`

### Package Scripts

#### Root Package Scripts
```json
"dev": "pnpm run dev:backend & sleep 2 && pnpm run dev:frontend"
"dev:start": "bash scripts/development/start-dev.sh"
"dev:stop": "bash scripts/development/stop-dev.sh"
"build": "turbo run build && vite build && esbuild..."
"test": "turbo run test"
"test:unit": "vitest run --coverage"
"test:integration": "vitest run --coverage"
"test:e2e": "playwright test"
```

#### Development Workflow
1. **Setup:** `pnpm run setup` - Initial project setup
2. **Development:** `pnpm run dev` - Start both servers
3. **Testing:** `pnpm run test` - Run all tests
4. **Build:** `pnpm run build` - Production build
5. **Start:** `pnpm start` - Start production server

---

## Port Configuration

### Default Ports

| Service | Port | Environment | Configurable |
|---------|------|-------------|--------------|
| Backend API | 5001 | Development | Yes (PORT) |
| Backend API | 3000 | Production | Yes (PORT) |
| Frontend Dev Server | 5173 | Development | Via Vite config |
| Frontend Proxy | /api → 5001 | Development | Via Vite config |
| PostgreSQL | 5432 | All | Via DATABASE_URL |

### Port Configuration Files
- Backend: Set via `PORT` environment variable
- Frontend: `config/build/vite.config.ts` (server.port)
- API Proxy: `config/build/vite.config.ts` (server.proxy)

---

## Environment Modes

### NODE_ENV Values

#### development
- Relaxed security settings
- Verbose logging
- Stack traces in errors
- Hot module replacement
- SSL verification: relaxed
- Session cookie: secure=false

#### production
- Strict security settings
- Minimal logging
- No stack traces
- Optimized builds
- SSL verification: strict
- Session cookie: secure=true

#### test
- Test-specific configurations
- Mock services
- In-memory data
- Fast execution

### Mode-Specific Behavior

| Feature | Development | Production |
|---------|-------------|------------|
| SSL Mode | prefer/disable | require |
| Cookie Secure | false | true |
| Cookie SameSite | lax | strict |
| Error Details | Full stack | Minimal |
| Logging | Verbose | Essential |
| Source Maps | Yes | No |
| HMR | Yes | No |

---

## Module Resolution

### TypeScript Path Aliases

**File:** `tsconfig.json`

```json
{
  "@/*": ["./apps/frontend-web/src/*"],
  "@shared": ["./packages/shared-types"],
  "@shared/*": ["./packages/shared-types/*"],
  "@netzwaechter/shared-validation": ["./packages/shared-validation/src"],
  "@netzwaechter/shared-validation/*": ["./packages/shared-validation/src/*"]
}
```

### Vite Aliases

**File:** `config/build/vite.config.ts`

```javascript
{
  "@": "apps/frontend-web/src",
  "@shared": "packages/shared-types",
  "@netzwaechter/shared-validation": "packages/shared-validation/src",
  "@assets": "attached_assets"
}
```

### Module System
- **Type:** ESM (ECMAScript Modules)
- **Import Style:** `import`/`export`
- **Extension:** `.ts`, `.tsx`
- **Transpilation:** esbuild (backend), Vite (frontend)

---

## File Organization

### Backend Structure
```
apps/backend-api/
├── modules/              # Feature modules
│   └── [feature]/
│       ├── [feature].controller.ts
│       ├── [feature].routes.ts
│       ├── [feature].repository.ts
│       ├── [feature].service.ts
│       └── __tests__/
├── services/            # Shared services
├── utilities/           # Helper utilities
├── connection-pool.ts   # Database pool
├── auth.ts             # Authentication
└── index.ts            # Application entry
```

### Frontend Structure
```
apps/frontend-web/
├── src/
│   ├── components/     # Reusable components
│   ├── features/       # Feature-specific code
│   ├── hooks/          # Custom React hooks
│   ├── lib/            # Utilities & helpers
│   ├── pages/          # Page components
│   ├── styles/         # Global styles
│   └── main.tsx        # Application entry
├── public/             # Static assets
└── index.html          # HTML template
```

---

## Configuration Files

### Build & Bundling
- `config/build/vite.config.ts` - Vite bundler config
- `config/build/drizzle.config.ts` - Database ORM config
- `config/build/tsconfig.json` - TypeScript config

### Testing
- `config/testing/vitest.config.ts` - Unit tests
- `config/testing/vitest.integration.config.ts` - Integration tests
- `config/testing/playwright.config.ts` - E2E tests

### Styling
- `config/tooling/tailwind.config.ts` - Tailwind CSS
- `config/tooling/postcss.config.js` - PostCSS

### Deployment
- `config/docker/docker-compose.yml` - Docker orchestration
- `config/docker/Dockerfile.backend` - Backend container
- `config/docker/Dockerfile.frontend` - Frontend container
- `config/docker/.env.example` - Docker environment template

---

## Code Quality

### TypeScript Configuration
- **Strict Mode:** Enabled
- **Target:** ESNext
- **Module:** ESNext
- **JSX:** preserve (frontend)
- **Skip Lib Check:** true
- **ES Module Interop:** true

### Type Checking
```bash
pnpm run typecheck           # All packages
pnpm run typecheck:frontend  # Frontend only
pnpm run typecheck:backend   # Backend only
```

### Linting
- Configuration: Per-package
- Command: `pnpm run lint`

---

## Development Tools

### Package Manager: pnpm
- **Version:** 10.2.0
- **Workspace:** Enabled
- **Store:** Global (hardlinked)
- **Benefits:**
  - Disk space efficiency
  - Fast installation
  - Strict dependency resolution

### Build Tools
- **Frontend:** Vite 5.4+
- **Backend:** esbuild 0.25+
- **Type Checking:** TypeScript 5.6.3
- **Bundler Analysis:** rollup-plugin-visualizer

### Development Scripts
- `scripts/development/setup-dev.sh` - Initial setup
- `scripts/development/start-dev.sh` - Start servers
- `scripts/development/stop-dev.sh` - Stop servers

---

## Security Considerations

### Configuration Security
1. Never commit `.env` files
2. Use strong secrets (128+ characters)
3. Rotate secrets regularly (90 days)
4. Different secrets per environment
5. File permissions: `chmod 600 .env`

### SSL/TLS Requirements
- **Development:** Optional (`sslmode=prefer`)
- **Production:** Required (`sslmode=require`)
- **Database:** SSL enforced in production
- **Email:** TLS 1.2+ required

### Session Security
- HTTP-only cookies
- Secure flag in production
- SameSite: strict (production)
- 128+ character secret
- 2-hour inactivity timeout
- 24-hour absolute timeout

---

## References

### Documentation
- Project docs: `docs/`
- Backend docs: `apps/backend-api/*.md`
- Knowledge base: `.archon-knowledge-base/`

### Configuration Files
- Environment: `.env.example`
- TypeScript: `tsconfig.json`
- Turborepo: `turbo.json`
- Package: `package.json`

### External Documentation
- Turborepo: https://turbo.build/repo/docs
- Vite: https://vitejs.dev/guide/
- Drizzle ORM: https://orm.drizzle.team/
- pnpm: https://pnpm.io/
