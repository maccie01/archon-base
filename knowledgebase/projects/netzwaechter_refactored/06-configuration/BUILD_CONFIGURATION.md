# Build Configuration

Comprehensive documentation of all build tools, configurations, and processes for the Netzwächter project.

Created: 2025-10-13
Last Updated: 2025-10-13

---

## Overview

The Netzwächter project uses a modern monorepo build system with Turborepo for task orchestration, Vite for frontend bundling, esbuild for backend compilation, and TypeScript for type safety across all packages.

---

## Turborepo Configuration

### Overview

**File:** `turbo.json`
**Purpose:** Monorepo task orchestration and caching
**Version:** Managed via turbo package

### Configuration Structure

```json
{
  "$schema": "https://turbo.build/schema.json",
  "cacheDir": "config/turbo/cache",
  "globalDependencies": [
    ".env",
    "tsconfig.json",
    "vite.config.ts",
    "vitest.config.ts"
  ],
  "tasks": {
    "build": { /* ... */ },
    "test": { /* ... */ },
    "typecheck": { /* ... */ }
  }
}
```

### Cache Configuration

**Cache Directory:** `config/turbo/cache/`

**Benefits:**
- Faster builds (skip unchanged packages)
- Shared cache across team (optional)
- Remote caching support (optional)
- Incremental builds

**Cache Invalidation:**
- Changes to source files
- Changes to dependencies
- Changes to global dependencies (.env, configs)

### Task Pipeline

#### build

**Purpose:** Build all packages in dependency order

**Configuration:**
```json
{
  "dependsOn": ["^build"],
  "outputs": ["dist/**", ".next/**", "build/**"]
}
```

**Features:**
- Topological ordering (dependencies built first)
- Parallel execution where possible
- Output caching

**Execution:**
```bash
pnpm run build
# or
turbo run build
```

#### test

**Purpose:** Run all tests

**Configuration:**
```json
{
  "dependsOn": ["build"],
  "outputs": ["coverage/**"]
}
```

**Features:**
- Runs after build completes
- Coverage reports cached
- Parallel test execution

#### typecheck

**Purpose:** TypeScript type checking

**Configuration:**
```json
{
  "dependsOn": []
}
```

**Features:**
- No dependencies (can run immediately)
- Fast execution
- No outputs (pure validation)

#### dev

**Purpose:** Development servers

**Configuration:**
```json
{
  "cache": false,
  "persistent": true
}
```

**Features:**
- No caching (always run fresh)
- Persistent process
- Hot module replacement

### Task Execution

**Single Task:**
```bash
turbo run build
```

**Multiple Tasks:**
```bash
turbo run build test typecheck
```

**Specific Package:**
```bash
turbo run build --filter=@netzwaechter/shared-types
```

**Force Rebuild:**
```bash
turbo run build --force
```

---

## Vite Configuration

### Overview

**File:** `config/build/vite.config.ts`
**Purpose:** Frontend build tool and dev server
**Version:** 5.4.19+

### Configuration

```typescript
export default defineConfig({
  plugins: [
    react(),
    visualizer({
      filename: "./dist/bundle-analysis.html",
      open: false,
      gzipSize: true,
      brotliSize: true,
      template: "treemap"
    })
  ],
  resolve: {
    alias: {
      "@": "apps/frontend-web/src",
      "@shared": "packages/shared-types",
      "@netzwaechter/shared-validation": "packages/shared-validation/src",
      "@assets": "attached_assets"
    }
  },
  root: "apps/frontend-web",
  build: {
    outDir: "dist/public",
    emptyOutDir: true
  },
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:5001",
        changeOrigin: true,
        secure: false
      }
    },
    fs: {
      strict: true,
      deny: ["**/.*"]
    }
  }
});
```

### Plugins

#### @vitejs/plugin-react

**Purpose:** React support (JSX, Fast Refresh)
**Features:**
- JSX transformation
- Fast refresh (HMR)
- React dev tools integration

#### rollup-plugin-visualizer

**Purpose:** Bundle analysis
**Output:** `dist/bundle-analysis.html`
**Features:**
- Treemap visualization
- Gzip/Brotli size analysis
- Dependency analysis
- Performance insights

### Path Aliases

| Alias | Path | Usage |
|-------|------|-------|
| `@/*` | `apps/frontend-web/src/*` | Components, pages, hooks |
| `@shared` | `packages/shared-types` | Database types, schemas |
| `@netzwaechter/shared-validation` | `packages/shared-validation/src` | Zod schemas |
| `@assets` | `attached_assets` | Static assets |

### Build Settings

**Output Directory:** `dist/public/`
**Root Directory:** `apps/frontend-web/`

**Build Optimizations:**
- Code splitting
- Tree shaking
- Minification
- Asset optimization

**Production Build:**
```bash
pnpm run build:frontend
# or
vite build
```

### Dev Server

**Port:** 5173 (default Vite port)
**HMR:** Enabled
**Proxy:** `/api` → `http://localhost:5001`

**Features:**
- Hot module replacement
- Fast startup
- API proxy to backend
- File system restrictions

**Security:**
```typescript
fs: {
  strict: true,        // Restrict access outside root
  deny: ["**/.*"]      // Deny dotfiles
}
```

### Bundle Analysis

**Generate Analysis:**
```bash
pnpm run analyze
# or
vite build --mode analyze
```

**Output:** `dist/bundle-analysis.html`

**Insights:**
- Largest dependencies
- Duplicate dependencies
- Unused code
- Optimization opportunities

---

## esbuild Configuration

### Overview

**Purpose:** Backend compilation and bundling
**Version:** 0.25.0+
**Command:** Inline in package.json

### Configuration

```bash
esbuild apps/backend-api/index.ts \
  --platform=node \
  --packages=external \
  --bundle \
  --format=esm \
  --outdir=dist
```

### Options

| Option | Value | Purpose |
|--------|-------|---------|
| `--platform` | node | Target Node.js |
| `--packages` | external | Keep node_modules external |
| `--bundle` | true | Bundle application code |
| `--format` | esm | ES Modules output |
| `--outdir` | dist | Output directory |

### Features

**Fast Compilation:**
- Written in Go (very fast)
- Parallel processing
- Minimal overhead

**Output:**
- Single bundle file
- ES Module format
- External dependencies
- Source maps (development)

**Execution:**
```bash
pnpm run build:backend
```

**Output:** `dist/index.js`

---

## TypeScript Configuration

### Root Configuration

**File:** `tsconfig.json`
**Extends:** None (base config)

```json
{
  "compilerOptions": {
    "incremental": true,
    "tsBuildInfoFile": "./node_modules/typescript/tsbuildinfo",
    "noEmit": true,
    "module": "ESNext",
    "strict": true,
    "lib": ["esnext", "dom", "dom.iterable"],
    "jsx": "preserve",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "allowImportingTsExtensions": true,
    "moduleResolution": "bundler",
    "baseUrl": ".",
    "types": ["node", "vite/client"],
    "paths": { /* aliases */ }
  }
}
```

### Key Settings

#### Strict Mode

**Enabled Checks:**
- `strictNullChecks` - Null/undefined handling
- `strictFunctionTypes` - Function type checking
- `strictBindCallApply` - Call/bind/apply typing
- `strictPropertyInitialization` - Class property init
- `noImplicitThis` - This type checking
- `alwaysStrict` - Strict mode in output

#### Module System

**Settings:**
- `module: "ESNext"` - Modern ES modules
- `moduleResolution: "bundler"` - Bundler-specific resolution
- `esModuleInterop: true` - CommonJS compatibility
- `allowImportingTsExtensions: true` - .ts imports allowed

#### Performance

**Optimizations:**
- `incremental: true` - Faster rebuilds
- `skipLibCheck: true` - Skip node_modules type checking
- `noEmit: true` - No JS output (handled by bundlers)

### Package-Specific Configs

#### Backend API

**File:** `apps/backend-api/tsconfig.json`

**Extends:** Root config
**Target:** Node.js
**Specific settings:** Server-side types

#### Frontend Web

**File:** `apps/frontend-web/tsconfig.json`

**Extends:** Root config
**Target:** Browser
**Specific settings:** React types, DOM APIs

#### Shared Packages

**Files:**
- `packages/shared-types/tsconfig.json`
- `packages/shared-validation/tsconfig.json`
- `packages/shared-utils/tsconfig.json`

**Purpose:** Type-only packages (no emit)

### Type Checking

**Check All:**
```bash
pnpm run typecheck
```

**Check Specific:**
```bash
pnpm run typecheck:frontend
pnpm run typecheck:backend
```

**Integration:**
- Pre-commit hooks
- CI/CD pipeline
- IDE integration

---

## Drizzle Configuration

### Overview

**File:** `config/build/drizzle.config.ts`
**Purpose:** Database ORM and migrations
**Version:** 0.30.4 (drizzle-kit)

### Configuration

```typescript
export default defineConfig({
  out: "./db/migrations",
  schema: "./packages/shared-types/schema.ts",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL
  }
});
```

### Settings

| Setting | Value | Purpose |
|---------|-------|---------|
| `out` | `./db/migrations` | Migration output directory |
| `schema` | `packages/shared-types/schema.ts` | Schema definition file |
| `dialect` | `postgresql` | Database type |
| `dbCredentials.url` | `DATABASE_URL` env var | Connection string |

### Commands

**Generate Migration:**
```bash
pnpm drizzle-kit generate
```

**Push Schema:**
```bash
pnpm db:push
```

**Introspect Database:**
```bash
pnpm drizzle-kit introspect
```

**Studio (GUI):**
```bash
pnpm drizzle-kit studio
```

### Migration Files

**Location:** `db/migrations/`
**Format:** SQL files
**Naming:** Timestamp-based

**Example:**
```
db/migrations/
├── 0000_initial_schema.sql
├── 0001_add_agents_table.sql
└── meta/
    └── _journal.json
```

---

## Tailwind CSS Configuration

### Overview

**File:** `config/tooling/tailwind.config.ts`
**Purpose:** Utility-first CSS framework
**Version:** 3.4.17+

### Configuration

```typescript
export default {
  darkMode: ["class"],
  content: [
    "./apps/frontend-web/index.html",
    "./apps/frontend-web/src/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      borderRadius: { /* ... */ },
      colors: { /* ... */ },
      keyframes: { /* ... */ },
      animation: { /* ... */ }
    }
  },
  plugins: [
    require("tailwindcss-animate"),
    require("@tailwindcss/typography")
  ]
}
```

### Features

**Dark Mode:**
- Class-based toggle
- Persistent preference
- Component support

**Content Sources:**
- Frontend HTML
- All React components
- TypeScript files

**Plugins:**
- `tailwindcss-animate` - Animation utilities
- `@tailwindcss/typography` - Prose styling

**Custom Theme:**
- CSS variables for colors
- Custom animations
- Extended utilities

### Build Process

**Development:**
- JIT compilation
- Fast rebuilds
- Full utility availability

**Production:**
- Unused CSS purged
- Minified output
- Optimized for size

---

## PostCSS Configuration

### Overview

**File:** `config/tooling/postcss.config.js`
**Purpose:** CSS processing pipeline

### Minimal Configuration

```javascript
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {}
  }
}
```

### Plugins

**tailwindcss:**
- Processes Tailwind utilities
- Applies theme configuration
- Generates CSS

**autoprefixer:**
- Adds vendor prefixes
- Browser compatibility
- Automatic prefix detection

---

## Build Scripts

### Package.json Scripts

**Full Build:**
```bash
pnpm run build
# Runs: turbo run build && vite build && esbuild backend
```

**Package Builds:**
```bash
pnpm run build:packages   # Shared packages only
pnpm run build:frontend   # Frontend only
pnpm run build:backend    # Backend only
```

**Development:**
```bash
pnpm run dev              # Start both servers
pnpm run dev:frontend     # Frontend only
pnpm run dev:backend      # Backend only
```

**Production:**
```bash
pnpm start                # Start production server
# Runs: NODE_ENV=production node dist/index.js
```

### Build Process Flow

1. **Clean:**
   - Clear dist directory
   - Remove old builds
   - Reset cache (if forced)

2. **Shared Packages:**
   - Type checking
   - No compilation (type-only)

3. **Frontend:**
   - Vite build
   - Bundle optimization
   - Asset processing
   - Output to dist/public/

4. **Backend:**
   - esbuild compilation
   - Bundle creation
   - Output to dist/index.js

5. **Verification:**
   - Type checking
   - Build artifacts exist
   - No errors

### Build Outputs

```
dist/
├── index.js              # Backend bundle
├── public/               # Frontend build
│   ├── index.html
│   ├── assets/
│   │   ├── index-[hash].js
│   │   ├── index-[hash].css
│   │   └── vendor-[hash].js
│   └── favicon.ico
└── bundle-analysis.html  # Bundle analysis
```

---

## Development Server Setup

### Backend Server

**Port:** 5001 (development), 5000 (default)
**Runtime:** Node.js with tsx (TypeScript execution)
**Watch Mode:** Enabled

**Command:**
```bash
NODE_ENV=development tsx watch --env-file=../../.env index.ts
```

**Features:**
- Auto-restart on changes
- Environment variable loading
- Source map support
- Fast compilation (esbuild)

### Frontend Server

**Port:** 5173 (Vite default)
**Framework:** React 18
**HMR:** Enabled

**Command:**
```bash
vite
```

**Features:**
- Fast refresh
- Hot module replacement
- API proxy to backend
- Instant updates

### Concurrent Development

**Start Both:**
```bash
pnpm run dev
```

**Process:**
1. Start backend (port 5001)
2. Wait 2 seconds
3. Start frontend (port 5173)
4. Frontend proxies /api to backend

---

## Build Optimizations

### Production Optimizations

**Frontend:**
- Code splitting (route-based)
- Tree shaking (unused code removal)
- Minification (Terser)
- Asset optimization (images, fonts)
- Lazy loading (components, routes)

**Backend:**
- Bundle size reduction
- External dependencies (not bundled)
- ES module format
- Fast startup

### Performance Monitoring

**Tools:**
- Bundle analyzer (visualizer plugin)
- Lighthouse (frontend performance)
- Node.js profiler (backend performance)

**Metrics:**
- Bundle size
- Load time
- Time to interactive
- Memory usage

---

## Build Troubleshooting

### Issue: Build Fails

**Checks:**
1. Node version (20+)
2. Dependencies installed (pnpm install)
3. Environment variables set
4. TypeScript errors
5. Disk space

**Solutions:**
```bash
# Clean install
rm -rf node_modules pnpm-lock.yaml
pnpm install

# Clear cache
rm -rf config/turbo/cache

# Force rebuild
turbo run build --force
```

### Issue: Type Errors

**Checks:**
1. TypeScript version consistent
2. Type definitions installed
3. Path aliases configured
4. tsconfig.json syntax

**Solutions:**
```bash
# Check types
pnpm run typecheck

# Install types
pnpm install -D @types/node @types/react

# Verify config
cat tsconfig.json | jq .
```

### Issue: Slow Builds

**Optimizations:**
1. Enable Turbo cache
2. Use incremental TypeScript
3. Optimize imports
4. Reduce bundle size
5. Use production mode

**Analysis:**
```bash
# Analyze bundle
pnpm run analyze

# Profile build
time pnpm run build

# Check cache usage
turbo run build --summarize
```

---

## CI/CD Build Configuration

### GitHub Actions (Example)

```yaml
name: Build
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: pnpm/action-setup@v2
        with:
          version: 10.2.0
      - uses: actions/setup-node@v3
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install
      - run: pnpm run typecheck
      - run: pnpm run build
      - run: pnpm test
```

### Build Environment

**Requirements:**
- Node.js 20+
- pnpm 10.2.0
- Environment variables
- Database access (for migrations)

---

## References

### Configuration Files
- `turbo.json` - Turborepo config
- `config/build/vite.config.ts` - Vite config
- `tsconfig.json` - TypeScript config
- `config/build/drizzle.config.ts` - Drizzle config
- `config/tooling/tailwind.config.ts` - Tailwind config

### External Documentation
- [Turborepo](https://turbo.build/repo/docs)
- [Vite](https://vitejs.dev)
- [esbuild](https://esbuild.github.io)
- [TypeScript](https://www.typescriptlang.org/docs)
- [Drizzle](https://orm.drizzle.team)
- [Tailwind CSS](https://tailwindcss.com/docs)
