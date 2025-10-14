# Development Setup

Step-by-step guide to set up the Netzwächter development environment.

Created: 2025-10-13
Last Updated: 2025-10-13

---

## Prerequisites

### Required Software

#### Node.js

**Version:** 20.18.2 or higher
**Download:** https://nodejs.org/

**Verify Installation:**
```bash
node --version
# Should output: v20.18.2 or higher
```

**Installation:**
- macOS: `brew install node@20`
- Windows: Download installer from nodejs.org
- Linux: Use package manager or nvm

#### pnpm

**Version:** 10.2.0 (exact)
**Website:** https://pnpm.io/

**Install:**
```bash
npm install -g pnpm@10.2.0
```

**Verify:**
```bash
pnpm --version
# Should output: 10.2.0
```

#### Git

**Version:** Any recent version
**Download:** https://git-scm.com/

**Verify:**
```bash
git --version
```

### Optional Software

#### Docker

**Purpose:** Containerized deployment
**Download:** https://www.docker.com/
**Usage:** `docker-compose.yml` for production

#### PostgreSQL Client

**Purpose:** Direct database access
**Tools:** psql, pgAdmin, DBeaver
**Usage:** Database inspection, manual queries

---

## Initial Setup

### 1. Clone Repository

```bash
git clone <repository-url> netzwaechter-refactored
cd netzwaechter-refactored
```

### 2. Install Dependencies

```bash
pnpm install
```

**Expected Duration:** 1-3 minutes

**What Happens:**
- Installs all dependencies
- Links workspace packages
- Creates `node_modules/`
- Generates `pnpm-lock.yaml`

**Troubleshooting:**
```bash
# If installation fails, try:
rm -rf node_modules pnpm-lock.yaml
pnpm install

# Or force clean install:
pnpm install --force
```

### 3. Configure Environment Variables

**Copy Template:**
```bash
cp .env.example .env
```

**Edit Configuration:**
```bash
nano .env  # or vim, code, etc.
```

**Required Variables:**

```bash
# Database Connection
DATABASE_URL=postgresql://username:password@host:port/database?sslmode=require

# Session Secret (generate new)
SESSION_SECRET=$(node -e "console.log(require('crypto').randomBytes(64).toString('hex'))")

# Email Service
MAILSERVER_PASSWORD=your-smtp-password

# Environment
NODE_ENV=development

# Server Port
PORT=5000
```

**Generate SESSION_SECRET:**
```bash
node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"
```

**Set File Permissions:**
```bash
chmod 600 .env
```

### 4. Database Setup

**Option A: Use Neon (Recommended)**

1. Create account at https://neon.tech
2. Create new project
3. Copy connection string
4. Update `DATABASE_URL` in `.env`
5. Run migrations:
```bash
pnpm db:push
```

**Option B: Local PostgreSQL**

1. Install PostgreSQL locally
2. Create database:
```bash
createdb netzwaechter_dev
```
3. Update `.env`:
```bash
DATABASE_URL=postgresql://localhost:5432/netzwaechter_dev?sslmode=disable
```
4. Run migrations:
```bash
pnpm db:push
```

**Verify Connection:**
```bash
psql $DATABASE_URL -c "SELECT 1;"
```

### 5. Initial Data (Optional)

**Import Weather Data:**
```bash
pnpm run import:weather
```

**Populate Report Data:**
```bash
pnpm run migrate:reports
```

### 6. Start Development Servers

**Start Both Servers:**
```bash
pnpm run dev
```

**Or Start Individually:**

Terminal 1 (Backend):
```bash
pnpm run dev:backend
```

Terminal 2 (Frontend):
```bash
pnpm run dev:frontend
```

**Verify:**
- Backend: http://localhost:5001
- Frontend: http://localhost:5173
- Health check: http://localhost:5001/api/health

---

## Development Workflow

### Daily Development

**Start Development:**
```bash
pnpm run dev
```

**Run Tests:**
```bash
pnpm test              # All tests
pnpm run test:unit     # Unit tests
pnpm run test:e2e      # E2E tests
```

**Type Checking:**
```bash
pnpm run typecheck
```

**Build:**
```bash
pnpm run build
```

### Code Changes

**Frontend Changes:**
- Edit files in `apps/frontend-web/src/`
- Hot module replacement (HMR) updates automatically
- No server restart needed

**Backend Changes:**
- Edit files in `apps/backend-api/`
- Server restarts automatically (tsx watch)
- Changes reflected immediately

**Shared Package Changes:**
- Edit files in `packages/*/`
- May require manual restart
- Run type check to verify

### Database Changes

**Update Schema:**
1. Edit `packages/shared-types/schema.ts`
2. Generate migration:
```bash
pnpm drizzle-kit generate
```
3. Apply changes:
```bash
pnpm db:push
```

**Inspect Database:**
```bash
pnpm drizzle-kit studio
```
Opens Drizzle Studio at http://localhost:4983

---

## Project Structure

### Key Directories

```
netzwaechter-refactored/
├── apps/
│   ├── backend-api/          # Express API server
│   │   ├── modules/          # Feature modules
│   │   ├── services/         # Shared services
│   │   ├── utilities/        # Helper utilities
│   │   └── index.ts          # Entry point
│   └── frontend-web/         # React application
│       ├── src/
│       │   ├── components/   # Reusable components
│       │   ├── features/     # Feature modules
│       │   ├── pages/        # Page components
│       │   └── main.tsx      # Entry point
│       └── index.html
├── packages/                 # Shared packages
│   ├── shared-types/        # Types & schemas
│   ├── shared-validation/   # Validation schemas
│   └── shared-utils/        # Utilities
├── config/                  # Configuration files
├── scripts/                 # Build & dev scripts
├── testing/                 # Test results
└── docs/                    # Documentation
```

### Important Files

**Configuration:**
- `.env` - Environment variables (not committed)
- `turbo.json` - Turborepo configuration
- `tsconfig.json` - TypeScript configuration
- `package.json` - Dependencies and scripts

**Build:**
- `config/build/vite.config.ts` - Frontend build
- `config/build/drizzle.config.ts` - Database ORM

**Testing:**
- `config/testing/vitest.config.ts` - Unit tests
- `config/testing/playwright.config.ts` - E2E tests

---

## IDE Setup

### Visual Studio Code

**Recommended Extensions:**

```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "Prisma.prisma",
    "ms-vscode.vscode-typescript-next"
  ]
}
```

**Settings:**
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true
}
```

**Workspace Setup:**
1. Open project root in VS Code
2. Install recommended extensions
3. TypeScript will auto-detect workspace
4. Path aliases will work automatically

### Other IDEs

**JetBrains (WebStorm, IntelliJ):**
- Enable Node.js integration
- Configure TypeScript (workspace version)
- Mark `node_modules` as excluded
- Enable ESLint/Prettier

**Vim/Neovim:**
- Install LSP plugins
- Configure tsserver
- Use coc.nvim or native LSP

---

## Common Development Tasks

### Adding a New Feature Module

**Backend:**
```bash
# Create module directory
mkdir apps/backend-api/modules/my-feature

# Create files
touch apps/backend-api/modules/my-feature/my-feature.controller.ts
touch apps/backend-api/modules/my-feature/my-feature.routes.ts
touch apps/backend-api/modules/my-feature/my-feature.repository.ts
touch apps/backend-api/modules/my-feature/my-feature.service.ts
mkdir apps/backend-api/modules/my-feature/__tests__
```

**Frontend:**
```bash
# Create feature directory
mkdir apps/frontend-web/src/features/my-feature

# Create files
touch apps/frontend-web/src/features/my-feature/index.tsx
touch apps/frontend-web/src/features/my-feature/MyFeature.tsx
```

### Adding a New Database Table

1. **Define Schema:**
```typescript
// packages/shared-types/schema.ts
export const myTable = pgTable("my_table", {
  id: serial("id").primaryKey(),
  name: varchar("name", { length: 255 }).notNull(),
  createdAt: timestamp("created_at").defaultNow()
});
```

2. **Export Types:**
```typescript
export type MyTable = typeof myTable.$inferSelect;
export type InsertMyTable = typeof myTable.$inferInsert;
```

3. **Generate Migration:**
```bash
pnpm drizzle-kit generate
```

4. **Apply Migration:**
```bash
pnpm db:push
```

### Adding a New Page

1. **Create Page Component:**
```typescript
// apps/frontend-web/src/pages/MyPage.tsx
export default function MyPage() {
  return <div>My Page</div>;
}
```

2. **Add Route:**
```typescript
// apps/frontend-web/src/App.tsx
import MyPage from './pages/MyPage';

// Add route
<Route path="/my-page" component={MyPage} />
```

---

## Testing

### Unit Tests

**Run Tests:**
```bash
pnpm run test:unit
```

**Watch Mode:**
```bash
pnpm run test:watch
```

**Coverage:**
```bash
pnpm run test:coverage
```

**Write Tests:**
```typescript
// apps/backend-api/modules/feature/__tests__/feature.test.ts
import { describe, it, expect } from 'vitest';
import { myFunction } from '../feature.service';

describe('Feature Service', () => {
  it('should do something', () => {
    expect(myFunction()).toBe('expected');
  });
});
```

### Integration Tests

**Run Tests:**
```bash
pnpm run test:integration
```

**Write Tests:**
```typescript
// Test with database
import { db } from '../db';
import { users } from '@shared';

describe('User Repository', () => {
  it('should create user', async () => {
    const user = await db.insert(users).values({...});
    expect(user).toBeDefined();
  });
});
```

### E2E Tests

**Run Tests:**
```bash
pnpm run test:e2e
```

**Watch Mode:**
```bash
pnpm run test:e2e:ui
```

**Write Tests:**
```typescript
// testing/e2e/feature.spec.ts
import { test, expect } from '@playwright/test';

test('user can login', async ({ page }) => {
  await page.goto('http://localhost:5173');
  await page.fill('[name="username"]', 'testuser');
  await page.fill('[name="password"]', 'password');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});
```

---

## Debugging

### Backend Debugging

**VS Code Launch Config:**
```json
{
  "type": "node",
  "request": "launch",
  "name": "Debug Backend",
  "runtimeExecutable": "pnpm",
  "runtimeArgs": ["run", "dev:backend"],
  "console": "integratedTerminal"
}
```

**Console Logging:**
```typescript
console.log('Debug:', variable);
console.error('Error:', error);
```

**Debugger:**
```typescript
debugger; // Set breakpoint
```

### Frontend Debugging

**Browser DevTools:**
- Chrome DevTools
- React DevTools extension
- Network tab for API calls
- Console for errors

**VS Code Debugger:**
```json
{
  "type": "chrome",
  "request": "launch",
  "name": "Debug Frontend",
  "url": "http://localhost:5173",
  "webRoot": "${workspaceFolder}/apps/frontend-web"
}
```

---

## Troubleshooting

### Port Already in Use

**Symptom:** `Error: listen EADDRINUSE: address already in use :::5000`

**Solution:**
```bash
# Find process using port
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port
PORT=5001 pnpm run dev:backend
```

### Module Not Found

**Symptom:** `Cannot find module '@shared'`

**Solution:**
```bash
# Reinstall dependencies
pnpm install

# Verify TypeScript paths
cat tsconfig.json | grep -A 10 paths

# Restart IDE
```

### Database Connection Failed

**Symptom:** `Error: connect ECONNREFUSED`

**Solutions:**
1. Verify DATABASE_URL in .env
2. Check database server running
3. Test connection:
```bash
psql $DATABASE_URL -c "SELECT 1;"
```
4. Check firewall/network

### Build Errors

**Symptom:** `Build failed with errors`

**Solutions:**
```bash
# Clear cache
rm -rf node_modules .turbo dist
pnpm install

# Check TypeScript errors
pnpm run typecheck

# Check for syntax errors
pnpm run lint
```

---

## Development Scripts Reference

### Core Commands

```bash
pnpm run dev              # Start both servers
pnpm run dev:frontend     # Frontend only
pnpm run dev:backend      # Backend only
pnpm run build            # Production build
pnpm start                # Start production server
```

### Testing

```bash
pnpm test                 # All tests
pnpm run test:unit        # Unit tests
pnpm run test:integration # Integration tests
pnpm run test:e2e         # E2E tests
pnpm run test:watch       # Watch mode
pnpm run test:coverage    # With coverage
pnpm run test:ui          # Test UI
```

### Database

```bash
pnpm db:push              # Apply schema changes
pnpm drizzle-kit generate # Generate migration
pnpm drizzle-kit studio   # Database GUI
pnpm run import:weather   # Import weather data
```

### Type Checking

```bash
pnpm run typecheck        # All packages
pnpm run typecheck:frontend  # Frontend only
pnpm run typecheck:backend   # Backend only
```

### Build Analysis

```bash
pnpm run analyze          # Bundle analysis
```

---

## Next Steps

After completing setup:

1. **Explore Codebase:**
   - Read `docs/` documentation
   - Review backend modules
   - Understand frontend structure

2. **Make First Change:**
   - Add a console.log
   - Verify HMR works
   - Commit change

3. **Run Tests:**
   - Ensure all tests pass
   - Understand test structure

4. **Read Documentation:**
   - Architecture docs
   - API documentation
   - Database schema

---

## References

### Internal Documentation
- `README.md` - Project overview
- `CONFIGURATION_OVERVIEW.md` - Configuration details
- `ENVIRONMENT_VARIABLES.md` - Environment vars
- `BUILD_CONFIGURATION.md` - Build system

### External Resources
- [Node.js](https://nodejs.org/docs)
- [pnpm](https://pnpm.io/)
- [Turborepo](https://turbo.build/repo/docs)
- [Vite](https://vitejs.dev/guide/)
- [React](https://react.dev/)
