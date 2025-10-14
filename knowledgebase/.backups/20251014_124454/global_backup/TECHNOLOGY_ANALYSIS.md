# Technology Analysis Across All Projects

Created: 2025-10-13

## Summary Statistics
- Total projects analyzed: 12
- JavaScript/TypeScript projects: 8
- Python projects: 4
- Primary focus: Web applications (monitoring, AI search, forecasting)

## Technology Usage Matrix

| Project Name | Frontend | Backend | Database | ORM/Query Builder | Testing | Build Tools | Auth Pattern | Notable Features |
|-------------|----------|---------|----------|-------------------|---------|-------------|--------------|------------------|
| netzwaechter-refactored | React + Vite | Express.js | PostgreSQL (Neon) | Drizzle ORM | Vitest, Playwright, MSW | Vite, Turborepo, esbuild | Session-based (express-session) | Monorepo (pnpm workspaces), Radix UI, TanStack Query |
| app-version-4_netzwächter | React + Vite | Express.js | PostgreSQL | Drizzle ORM | Vitest | Vite, esbuild | Session-based | Radix UI, Python agents |
| moni (monitoring-app) | N/A (API) | Express.js | MySQL | Sequelize | Jest | N/A | JWT + bcrypt | Legacy monitoring |
| ws_energieservice | N/A (API) | Express.js | PostgreSQL | Sequelize | Jest | N/A | JWT + bcrypt | Multi-tenant monitoring |
| Nexorithm-website | Next.js 15 | Next.js API | Supabase | Supabase client | N/A | Next.js | Supabase Auth | React 19, Framer Motion |
| Perplexica (backend) | N/A | Express.js | SQLite | Drizzle ORM | Jest | TypeScript | N/A | LangChain, AI embeddings |
| Perplexica (ui) | Next.js 14 | Next.js API | N/A | N/A | N/A | Next.js | N/A | AI search interface |
| Perplexica-old-revised | Next.js | Express.js | SQLite | Drizzle ORM | N/A | TypeScript | N/A | MLX service (Python) |
| dhbw-tp-forecasting | N/A | N/A | CSV files | Pandas | Pytest | N/A | N/A | Time series forecasting (Darts, Prophet) |
| ai-presentation | HTML/CSS | Node.js | N/A | N/A | N/A | Custom build | N/A | Modular CSS components |
| Data_security | N/A | Python | N/A | N/A | N/A | N/A | N/A | Security analysis scripts |
| software_eng2 | N/A | Python | N/A | N/A | N/A | N/A | N/A | Educational projects |

## Shared Technologies (Used in 2+ Projects)

### Frontend Frameworks (Priority Order)
1. **React** - used in 5 projects (netzwaechter-refactored, app-version-4, Nexorithm-website, Perplexica, Perplexica-old)
2. **Next.js** - used in 3 projects (Nexorithm-website, Perplexica ui, Perplexica-old-revised)
3. **Vite** - used in 3 projects (netzwaechter-refactored, app-version-4, build tool)

### Backend Frameworks (Priority Order)
1. **Express.js** - used in 6 projects (netzwaechter-refactored, app-version-4, moni, ws_energieservice, Perplexica backend, Perplexica-old-revised)
2. **Next.js API Routes** - used in 2 projects (Nexorithm-website, Perplexica ui)

### Database & ORM (Priority Order)
1. **PostgreSQL** - used in 3 projects (netzwaechter-refactored, app-version-4, ws_energieservice)
2. **Drizzle ORM** - used in 3 projects (netzwaechter-refactored, app-version-4, Perplexica)
3. **Sequelize** - used in 2 projects (moni, ws_energieservice)
4. **SQLite** - used in 2 projects (Perplexica backend, Perplexica-old-revised)
5. **MySQL** - used in 1 project (moni)
6. **Supabase** - used in 1 project (Nexorithm-website)

### UI Libraries & Styling (Priority Order)
1. **Tailwind CSS** - used in 5 projects (netzwaechter-refactored, app-version-4, Nexorithm-website, Perplexica ui, Perplexica-old)
2. **Radix UI** - used in 2 projects (netzwaechter-refactored, app-version-4)
3. **Lucide React** - used in 3 projects (netzwaechter-refactored, Nexorithm-website, Perplexica ui)
4. **Framer Motion** - used in 2 projects (netzwaechter-refactored, Nexorithm-website)

### State Management (Priority Order)
1. **TanStack Query (React Query)** - used in 1 project (netzwaechter-refactored)
2. **Wouter** (routing) - used in 1 project (netzwaechter-refactored)

### Testing Frameworks (Priority Order)
1. **Vitest** - used in 2 projects (netzwaechter-refactored, app-version-4)
2. **Jest** - used in 2 projects (moni, ws_energieservice, Perplexica)
3. **Playwright** - used in 1 project (netzwaechter-refactored)
4. **Pytest** - used in 1 project (dhbw-tp-forecasting)
5. **MSW (Mock Service Worker)** - used in 1 project (netzwaechter-refactored)

### Build Tools (Priority Order)
1. **Vite** - used in 3 projects (netzwaechter-refactored, app-version-4, multiple monitoring apps)
2. **esbuild** - used in 3 projects (netzwaechter-refactored, app-version-4, bundling)
3. **Turborepo** - used in 1 project (netzwaechter-refactored)
4. **TypeScript** - used in 6+ projects (nearly all JS/TS projects)
5. **Next.js** - used in 3 projects (as build tool)

### Authentication Patterns (Priority Order)
1. **Session-based (express-session)** - used in 2 projects (netzwaechter-refactored, app-version-4)
2. **JWT (jsonwebtoken)** - used in 2 projects (moni, ws_energieservice)
3. **bcrypt/bcryptjs** - used in 4 projects (all Express-based projects)
4. **Supabase Auth** - used in 1 project (Nexorithm-website)

### Python Data Science Stack (Priority Order)
1. **Pandas** - used in 1 project (dhbw-tp-forecasting)
2. **NumPy** - used in 1 project (dhbw-tp-forecasting)
3. **Darts** - used in 1 project (dhbw-tp-forecasting)
4. **Prophet** - used in 1 project (dhbw-tp-forecasting)
5. **Statsmodels** - used in 1 project (dhbw-tp-forecasting)
6. **Scikit-learn** - used in 1 project (dhbw-tp-forecasting)

## Shared Patterns Identified

### 1. Monorepo Pattern
- **Tool**: Turborepo + pnpm workspaces
- **Usage**: netzwaechter-refactored
- **Structure**:
  - apps/ (frontend-web, backend-api)
  - packages/ (shared-types, shared-validation, shared-utils)
- **Benefits**: Shared code, unified build system, type safety across apps

### 2. Database Migration Pattern
- **Drizzle Kit**: Used for schema management and migrations
- **Projects**: netzwaechter-refactored, app-version-4, Perplexica
- **Command**: `drizzle-kit push` for schema synchronization

### 3. Session Storage Pattern
- **PostgreSQL Session Store**: connect-pg-simple
- **Usage**: netzwaechter-refactored
- **Alternative**: memorystore for development

### 4. Environment Configuration
- **Tool**: dotenv
- **Pattern**: .env files at project root
- **Usage**: All JavaScript/TypeScript projects
- **Security**: .env files in .gitignore

### 5. Type-Safe Validation
- **Tool**: Zod
- **Usage**: All modern TypeScript projects
- **Integration**: @hookform/resolvers for form validation
- **Pattern**: Shared validation schemas in monorepo

### 6. API Patterns
- **REST API**: All Express.js projects
- **Next.js API Routes**: Nexorithm-website, Perplexica ui
- **WebSocket**: netzwaechter-refactored (ws package)

### 7. Rate Limiting & Security
- **express-rate-limit**: Used in 4 projects
- **helmet**: Used in 3 projects (security headers)
- **cors**: Used in all Express projects

### 8. Logging Pattern
- **winston**: Used in 3 projects (Perplexica, moni, ws_energieservice)
- **Pattern**: Structured logging with log levels

### 9. File Upload Pattern
- **multer**: Used in 2 projects (netzwaechter-refactored, Perplexica)
- **@uppy**: Used in 1 project (netzwaechter-refactored) for UI

### 10. AI/ML Integration
- **OpenAI API**: netzwaechter-refactored
- **LangChain**: Perplexica projects
- **Anthropic Claude**: app-version-4 (agents)
- **Time Series**: dhbw-tp-forecasting (Darts, Prophet)

### 11. CSS Utility Pattern
- **Tailwind CSS**: Dominant styling approach
- **Utilities**: clsx, tailwind-merge (cn function)
- **Animations**: tailwindcss-animate

### 12. Testing Strategy
- **Unit Tests**: Vitest/Jest
- **Integration Tests**: Vitest with MSW
- **E2E Tests**: Playwright
- **Coverage**: @vitest/coverage-v8

## Technology Trends & Insights

### Modern vs Legacy Stack
**Modern Stack (2024-2025):**
- React + Vite
- Drizzle ORM
- Vitest + Playwright
- TypeScript ESM modules
- Radix UI + Tailwind CSS
- TanStack Query
- pnpm + Turborepo

**Legacy Stack (2023):**
- Express standalone
- Sequelize ORM
- Jest
- MySQL/PostgreSQL
- Traditional JWT auth

### Migration Patterns Observed
1. **Sequelize → Drizzle ORM**: Type-safe, lightweight alternative
2. **Jest → Vitest**: Faster, better ESM support
3. **Webpack → Vite**: Faster dev server, better DX
4. **npm → pnpm**: Disk efficiency, monorepo support
5. **Material UI → Radix UI**: Headless components, more control

### Architecture Patterns
1. **Full-stack Monorepo**: netzwaechter-refactored
2. **Microservices**: Perplexica (backend + ui + ocr service)
3. **Monolithic API**: moni, ws_energieservice
4. **Jamstack**: Nexorithm-website (Next.js + Supabase)
5. **Data Pipeline**: dhbw-tp-forecasting (Python notebooks)

## Recommendations for Global Knowledge Base

### Critical Priority (Document First)
These technologies appear in 50%+ of projects and are actively used:

1. **React** - Core frontend library
   - Hooks patterns
   - Component composition
   - Performance optimization

2. **Express.js** - Core backend framework
   - Middleware patterns
   - Error handling
   - Security best practices

3. **TypeScript** - Type system
   - Configuration patterns
   - Type inference
   - Module resolution (ESM)

4. **Tailwind CSS** - Styling approach
   - Configuration
   - Custom utilities
   - Component patterns

5. **Drizzle ORM** - Modern database toolkit
   - Schema definition
   - Migrations
   - Query patterns
   - Type safety

### High Priority (Document Second)
These technologies appear in multiple projects:

1. **Vite** - Build tool and dev server
2. **PostgreSQL** - Primary database
3. **Vitest** - Testing framework
4. **Zod** - Runtime validation
5. **Radix UI** - Component primitives
6. **Next.js** - Full-stack framework

### Medium Priority (Document Third)
Specialized but important:

1. **Playwright** - E2E testing
2. **TanStack Query** - Server state management
3. **Turborepo** - Monorepo orchestration
4. **bcrypt** - Password hashing
5. **express-session** - Session management

### Low Priority (Document as Needed)
Project-specific or rarely used:

1. **LangChain** - AI/LLM framework
2. **Sequelize** - Legacy ORM
3. **Supabase** - BaaS platform
4. **Python Data Science Stack** - Specialized use case

## Technology Stack Recommendations

### For New Full-Stack Projects
```
Frontend:
- React 18
- Vite 5
- Tailwind CSS 3
- Radix UI
- TanStack Query
- Wouter (routing)
- React Hook Form + Zod

Backend:
- Express.js
- TypeScript (ESM)
- Drizzle ORM
- PostgreSQL
- express-session (auth)
- zod (validation)

Testing:
- Vitest (unit/integration)
- Playwright (E2E)
- MSW (API mocking)

Build:
- Turborepo (monorepo)
- pnpm (package manager)
- esbuild (bundling)
```

### For Static Sites/Marketing
```
- Next.js 15
- Tailwind CSS
- Framer Motion
- Supabase (if backend needed)
```

### For Data Science/ML Projects
```
- Python 3.10+
- Pandas
- NumPy
- Darts (time series)
- Prophet
- Statsmodels
- Jupyter notebooks
```

## Next Steps

### Phase 1: Core Documentation (Week 1)
1. Create React best practices guide
2. Document Express.js patterns
3. Write TypeScript configuration guide
4. Document Tailwind CSS setup and patterns

### Phase 2: Database & Backend (Week 2)
1. Drizzle ORM complete guide
2. PostgreSQL setup and patterns
3. Session management guide
4. API design patterns

### Phase 3: Testing & Quality (Week 3)
1. Vitest testing patterns
2. Playwright E2E guide
3. MSW mocking guide
4. Coverage strategies

### Phase 4: Build & Deploy (Week 4)
1. Vite configuration guide
2. Turborepo monorepo setup
3. pnpm workspaces guide
4. Production deployment checklist

### Phase 5: UI & UX (Week 5)
1. Radix UI component library
2. Form handling (React Hook Form + Zod)
3. Animation patterns (Framer Motion)
4. Accessibility guidelines

## Project-Specific Notes

### netzwaechter-refactored
- **Status**: Most modern, reference architecture
- **Use as template for**: New full-stack projects
- **Notable**: Complete testing setup, monorepo, type safety

### Perplexica
- **Status**: AI-focused, microservices
- **Use as reference for**: AI/LLM integration, multi-language services
- **Notable**: LangChain integration, embeddings, vector search

### dhbw-tp-forecasting
- **Status**: Data science project
- **Use as reference for**: Time series analysis, scientific computing
- **Notable**: Comprehensive ML pipeline, academic paper workflow

### Nexorithm-website
- **Status**: Modern Jamstack
- **Use as reference for**: Marketing sites, Supabase integration
- **Notable**: React 19, Next.js 15 early adoption

### Legacy Monitoring Apps (moni, ws_energieservice)
- **Status**: Legacy, maintenance mode
- **Use as reference for**: Migration planning
- **Notable**: Sequelize ORM patterns, JWT auth

## Technology Version Tracking

### Current Versions (as of Oct 2025)
- React: 18.3.1 (stable), 19.0.0 (adopted by Nexorithm)
- Next.js: 14.1.4 → 15.1.7
- TypeScript: 5.4.3 → 5.6.3
- Vite: 5.4.19
- Vitest: 3.2.4
- Drizzle ORM: 0.31.2 → 0.39.1
- Tailwind CSS: 3.3.0 → 3.4.17
- Express: 4.18.2 → 4.21.2
- PostgreSQL: 8.11.3 → 8.16.3 (node-postgres)

## Knowledge Gaps Identified

### Areas Needing Documentation
1. **Deployment strategies**: No clear deployment patterns documented
2. **Docker/containerization**: Not consistently used across projects
3. **CI/CD pipelines**: GitHub Actions patterns need documentation
4. **Monitoring/observability**: No standard logging/monitoring setup
5. **Error handling**: Inconsistent patterns across projects
6. **API documentation**: No standard (Swagger/OpenAPI) used
7. **State management**: Beyond TanStack Query, no patterns documented
8. **Internationalization**: No i18n patterns established
9. **Performance monitoring**: No APM/RUM tools documented
10. **Security scanning**: No automated security testing documented

## Conclusion

The technology landscape across all projects shows a clear evolution toward modern, type-safe, and performant tools. The dominant pattern is React + Express + PostgreSQL + Drizzle ORM with TypeScript throughout. The netzwaechter-refactored project represents the current best practices and should serve as the reference architecture for future projects.

Key takeaways:
1. **Type safety is critical**: TypeScript + Zod + Drizzle ORM provide end-to-end type safety
2. **Modern tooling wins**: Vite, Vitest, and Drizzle are replacing older tools
3. **Monorepo pattern**: Emerging as preferred structure for complex projects
4. **Testing is improving**: More comprehensive testing in newer projects
5. **UI libraries**: Moving toward headless components (Radix UI) + Tailwind CSS
6. **Performance matters**: Vite, esbuild, and pnpm chosen for speed
7. **Security baseline**: express-session, helmet, rate-limiting are standard

This analysis should guide the creation of global shared knowledge documentation, prioritizing the most frequently used and most critical technologies first.
