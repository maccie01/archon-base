# Netzwächter Knowledge Base

Created: 2025-10-13

Complete knowledge base documentation for the Netzwächter Energy Monitoring System, prepared for Archon integration.

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Documentation Structure](#documentation-structure)
4. [Key Statistics](#key-statistics)
5. [Critical Findings](#critical-findings)
6. [For Different Roles](#for-different-roles)
7. [How to Use This Knowledge Base](#how-to-use-this-knowledge-base)
8. [Next Steps](#next-steps)

---

## Overview

This knowledge base contains comprehensive documentation of the Netzwächter project across 7 major domains:

- **Database**: PostgreSQL schemas, 20+ tables, relationships, indexes
- **API**: 120+ endpoints across 22 modules
- **Authentication**: Session-based auth, role system, security features
- **Frontend**: React architecture, UI components, design system
- **Backend**: Module patterns, service layer, data access
- **Configuration**: Environment setup, dependencies, deployment
- **Standards**: Coding standards, required patterns, security practices (NEW)

**Total Documentation**: 49 files, ~450 KB, created by 6 specialized agents

---

## Quick Start

### New Developer Onboarding

**Day 1: Setup**
1. Read: `06-configuration/DEVELOPMENT_SETUP.md`
2. Configure environment: `06-configuration/ENVIRONMENT_VARIABLES.md`
3. Setup database: `01-database/DATABASE_OVERVIEW.md`

**Day 2: Architecture**
4. Backend overview: `05-backend/BACKEND_OVERVIEW.md`
5. Frontend overview: `04-frontend/FRONTEND_OVERVIEW.md`
6. API catalog: `02-api-endpoints/ENDPOINTS_BY_MODULE.md`

**Day 3: Patterns**
7. Module pattern: `05-backend/MODULE_PATTERN_STANDARD.md`
8. Component patterns: `04-frontend/COMPONENT_ARCHITECTURE.md`
9. Auth flow: `03-authentication/AUTH_FLOW.md`

### Need Something Specific?

- **Database schema?** → `01-database/SCHEMA_TABLES.md`
- **API endpoint?** → `02-api-endpoints/ENDPOINTS_ALPHABETICAL.md`
- **How to authenticate?** → `03-authentication/AUTH_OVERVIEW.md`
- **UI component?** → `04-frontend/UI_COMPONENT_INVENTORY.md`
- **Code pattern?** → `05-backend/MODULE_PATTERN_STANDARD.md`
- **Environment variable?** → `06-configuration/ENVIRONMENT_VARIABLES.md`

---

## Documentation Structure

### 01-database/ (5 files, 66 KB)

Complete PostgreSQL database documentation:

- `README.md` - Navigation and quick reference
- `DATABASE_OVERVIEW.md` - PostgreSQL setup, connection pool, Drizzle ORM
- `SCHEMA_TABLES.md` - All 20 tables documented (677 lines)
- `RELATIONSHIPS.md` - 30+ foreign keys, relationship diagrams
- `INDEXES_CONSTRAINTS.md` - 72+ indexes, performance optimization

**Key Stats**: 20 tables, 200+ columns, 72+ indexes, 30+ relationships

### 02-api-endpoints/ (6 files, ~85 KB)

Complete API endpoint catalog:

- `README.md` - Documentation index
- `API_OVERVIEW.md` - Base URL, authentication, middleware
- `ENDPOINTS_BY_MODULE.md` - 120+ endpoints by functional area
- `ENDPOINTS_ALPHABETICAL.md` - Quick reference A-Z
- `REQUEST_RESPONSE_SCHEMAS.md` - All request/response formats
- `FRONTEND_USAGE_MAP.md` - Frontend-backend integration, mismatches

**Key Stats**: 120+ endpoints, 22 modules, 18 API mismatches identified

### 03-authentication/ (5 files, ~55 KB)

Complete authentication and security architecture:

- `AUTH_OVERVIEW.md` - Session-based authentication strategy
- `AUTH_FLOW.md` - Login, session validation, logout flows
- `AUTHORIZATION.md` - Role system, permissions, middleware
- `SECURITY_FEATURES.md` - Password security, rate limiting, vulnerabilities
- `PROTECTED_ROUTES.md` - All 90+ protected endpoints cataloged

**Key Stats**: 3 roles, 90+ protected endpoints, 8 rate-limited endpoints

### 04-frontend/ (8 files, ~95 KB)

Complete frontend architecture and UI documentation:

- `README.md` - Navigation hub for all frontend docs
- `FRONTEND_OVERVIEW.md` - React 18, TypeScript, Vite, TanStack Query
- `UI_COMPONENT_INVENTORY.md` - 24 shadcn/ui components
- `DESIGN_SYSTEM_CURRENT.md` - Colors, typography, spacing
- `LAYOUT_PATTERNS.md` - Two layout modes (Strawa vs Cockpit)
- `UI_INCONSISTENCIES.md` - 200+ documented UI problems
- `COMPONENT_ARCHITECTURE.md` - Feature-based organization
- `UI_REDESIGN_NEEDS.md` - 6-phase redesign plan (12 weeks)

**Key Stats**: 24 shadcn/ui components, 11 features, 30+ routes, 2 layout modes

### 05-backend/ (8 files, ~111 KB)

Complete backend architecture documentation:

- `README.md` - Navigation guide, code review checklist
- `BACKEND_OVERVIEW.md` - 23 modules, Express setup, middleware
- `MODULE_PATTERN_STANDARD.md` - 4-layer pattern definition
- `ARCHITECTURE_CONSISTENCY.md` - Pattern adherence analysis (26%)
- `SERVICE_LAYER.md` - Business logic patterns, 7 services
- `DATA_ACCESS_LAYER.md` - Drizzle ORM, repository pattern
- `MIDDLEWARE_STACK.md` - Auth, error handling, rate limiting
- `ARCHITECTURE_ASSESSMENT.md` - Technical debt: 6.5/10, refactor plan

**Key Stats**: 23 modules, 120+ endpoints, 26% pattern adherence, 6-8 week refactor

### 06-configuration/ (8 files, ~111 KB)

Complete configuration and environment documentation:

- `CONFIGURATION_OVERVIEW.md` - Monorepo structure, Turborepo
- `ENVIRONMENT_VARIABLES.md` - All 11 env vars documented
- `DATABASES.md` - PostgreSQL/Neon, connection pool, SSL
- `EXTERNAL_SERVICES.md` - Neon, Nodemailer, Bright Sky API, OpenAI
- `BUILD_CONFIGURATION.md` - Vite, esbuild, TypeScript, Drizzle
- `DEPENDENCIES.md` - 170 packages categorized
- `DEVELOPMENT_SETUP.md` - Setup instructions, IDE config
- `DEPLOYMENT_REQUIREMENTS.md` - Production setup, Docker, PM2

**Key Stats**: 11 env vars, 4 external services, 170 dependencies

### 07-standards/ (7 files, ~100 KB) ⚠️ CRITICAL

**Project coding standards and required patterns:**

- `README.md` - Standards overview and quick reference
- `LEGACY_PATTERNS_TO_AVOID.md` - Deprecated patterns (NEVER use)
- `BACKEND_PATTERNS.md` - Required 4-layer architecture
- `FRONTEND_PATTERNS.md` - Required React patterns
- `TESTING_PATTERNS.md` - Testing requirements (80%+ coverage)
- `SECURITY_PATTERNS.md` - Non-negotiable security requirements
- `CODING_STANDARDS.md` - Style guide, naming conventions

**Key Stats**: 6 critical standards, P0 priority, AI guidance source

**Why Critical**: These documents define what patterns to use vs avoid. AI agents MUST reference these when suggesting code.

---

## Key Statistics

### Project Scale

- **Total LOC**: 81,129 lines (57.9% dead code identified)
- **Active Code**: 34,162 lines (after cleanup)
- **Backend**: 23 modules, 120+ endpoints
- **Frontend**: 11 features, 30+ routes, 24 UI components
- **Database**: 20 tables, 200+ columns, 72+ indexes
- **Tests**: 1,094 passing tests (75%+ coverage)

### Technology Stack

**Backend:**
- Node.js 20+, Express.js, TypeScript 5.6
- PostgreSQL 16+ with Neon
- Drizzle ORM
- express-session, bcrypt

**Frontend:**
- React 18.3, TypeScript
- TanStack Query (React Query)
- Radix UI (shadcn/ui)
- Tailwind CSS, Vite

**Infrastructure:**
- Monorepo: Turborepo + pnpm
- Testing: Vitest, Playwright
- Database: Neon (Serverless PostgreSQL)

### Documentation Coverage

- **49 files** created
- **~450 KB** total documentation
- **100% coverage** across all 7 domains
- Created by **6 specialized agents**
- **Dated**: 2025-10-13
- **Standards**: 7 critical files for AI guidance

---

## Critical Findings

### Strengths

1. **Excellent Architecture Design**: 4-layer pattern is sound (9/10)
2. **Zero Circular Dependencies**: Clean module boundaries
3. **Good Testing**: 1,094 tests passing (97.4% pass rate)
4. **Modern Stack**: React 18, TypeScript, TanStack Query
5. **Well-Organized**: Feature-based frontend, module-based backend

### Critical Issues

#### 1. Dead Code (57.9% of codebase)

- 46,967 LOC dead code identified
- Phase 1 cleanup can remove 40,055 LOC in 5 minutes
- See: `.dead-code-analysis-reports/MASTER_REPORT.md`

#### 2. API Mismatches (18 identified)

**High Priority:**
- Monitoring routes mismatch
- Object-mandant assignments mismatch
- 7 missing energy endpoints
- Auth check endpoint missing

See: `02-api-endpoints/FRONTEND_USAGE_MAP.md`

#### 3. Backend Pattern Inconsistency (74% deviation)

- Only 6 of 23 modules follow standard pattern
- efficiency module: 383-line controller (needs refactor)
- ki-reports module: 280-line controller (needs refactor)

See: `05-backend/ARCHITECTURE_CONSISTENCY.md`

#### 4. UI Inconsistencies (200+ issues)

**Critical:**
- Dialog overlay transparency bug (global CSS hack)
- Toast opacity bug (global CSS hack)
- 3 different table implementations
- 3 gray scales, 5 blues (no unified design system)
- Two completely different layouts (Strawa vs Cockpit)

See: `04-frontend/UI_INCONSISTENCIES.md`

#### 5. Security Vulnerabilities

**Critical:**
- SSL disabled on database connection
- No CSRF token validation
- Weak session secrets allowed in dev
- Superadmin plain text passwords
- Missing security headers

See: `03-authentication/SECURITY_FEATURES.md`

---

## For Different Roles

### Backend Developers

**Start Here:**
1. `05-backend/BACKEND_OVERVIEW.md`
2. `05-backend/MODULE_PATTERN_STANDARD.md`
3. `01-database/SCHEMA_TABLES.md`
4. `02-api-endpoints/ENDPOINTS_BY_MODULE.md`

**When Adding Features:**
- Use `settings` module as reference implementation
- Follow 4-layer pattern: Routes → Controller → Service → Repository
- Check `05-backend/MODULE_PATTERN_STANDARD.md` for examples
- Use code review checklist in `05-backend/README.md`

**Common Tasks:**
- Add endpoint: See `02-api-endpoints/REQUEST_RESPONSE_SCHEMAS.md`
- Add table: See `01-database/SCHEMA_TABLES.md`
- Add auth: See `03-authentication/PROTECTED_ROUTES.md`

### Frontend Developers

**Start Here:**
1. `04-frontend/FRONTEND_OVERVIEW.md`
2. `04-frontend/UI_COMPONENT_INVENTORY.md`
3. `04-frontend/COMPONENT_ARCHITECTURE.md`
4. `02-api-endpoints/ENDPOINTS_ALPHABETICAL.md`

**When Adding Features:**
- Check `04-frontend/DESIGN_SYSTEM_CURRENT.md` for colors/spacing
- Use shadcn/ui components (see inventory)
- Follow feature-based organization pattern
- Use TanStack Query for API calls

**Common Tasks:**
- Add page: See `04-frontend/LAYOUT_PATTERNS.md`
- Add API call: See `02-api-endpoints/FRONTEND_USAGE_MAP.md`
- Style component: See `04-frontend/DESIGN_SYSTEM_CURRENT.md`

### DevOps / SRE

**Start Here:**
1. `06-configuration/DEPLOYMENT_REQUIREMENTS.md`
2. `06-configuration/ENVIRONMENT_VARIABLES.md`
3. `01-database/DATABASE_OVERVIEW.md`
4. `06-configuration/EXTERNAL_SERVICES.md`

**For Deployment:**
- Production setup: `06-configuration/DEPLOYMENT_REQUIREMENTS.md`
- Environment config: `06-configuration/ENVIRONMENT_VARIABLES.md`
- Database setup: `01-database/DATABASE_OVERVIEW.md`
- Monitoring: `05-backend/BACKEND_OVERVIEW.md` (health endpoints)

**For Troubleshooting:**
- Connection issues: `01-database/DATABASE_OVERVIEW.md`
- Auth problems: `03-authentication/AUTH_FLOW.md`
- API errors: `02-api-endpoints/API_OVERVIEW.md`

### Security Auditors

**Start Here:**
1. `03-authentication/SECURITY_FEATURES.md`
2. `03-authentication/PROTECTED_ROUTES.md`
3. `01-database/DATABASE_OVERVIEW.md`
4. `06-configuration/ENVIRONMENT_VARIABLES.md`

**Critical Vulnerabilities:**
- See full vulnerability assessment in `03-authentication/SECURITY_FEATURES.md`
- Database SSL: `01-database/DATABASE_OVERVIEW.md`
- Rate limiting: `03-authentication/SECURITY_FEATURES.md`
- Session security: `03-authentication/AUTH_OVERVIEW.md`

### Product Managers / Designers

**Start Here:**
1. `04-frontend/UI_INCONSISTENCIES.md`
2. `04-frontend/UI_REDESIGN_NEEDS.md`
3. `02-api-endpoints/ENDPOINTS_BY_MODULE.md`
4. `05-backend/BACKEND_OVERVIEW.md`

**For Planning:**
- UI redesign: `04-frontend/UI_REDESIGN_NEEDS.md` (12-week plan)
- Backend refactor: `05-backend/ARCHITECTURE_ASSESSMENT.md` (6-8 weeks)
- Dead code cleanup: `.dead-code-analysis-reports/MASTER_REPORT.md` (4-5 weeks)
- API fixes: `02-api-endpoints/FRONTEND_USAGE_MAP.md` (1-2 weeks)

---

## How to Use This Knowledge Base

### For Archon Integration

This knowledge base is structured for optimal Archon integration:

**1. Document Chunking**
- Each markdown file is self-contained
- Cross-references use relative paths
- Consistent heading hierarchy
- Code examples included

**2. RAG Optimization**
- Clear table of contents in each file
- Consistent formatting
- Keyword-rich headings
- Proper metadata (dates, creation timestamps)

**3. Context Retrieval**
- README files provide navigation
- Cross-referenced documents
- Alphabetical indexes for quick lookup
- Categorized by domain

**4. Import to Archon**
```bash
# Archon will index all markdown files in this directory
archon knowledge import .archon-knowledge-base/
```

### For Manual Reference

**Search by Domain:**
```bash
# Database questions
cd 01-database/

# API questions
cd 02-api-endpoints/

# Auth questions
cd 03-authentication/

# Frontend questions
cd 04-frontend/

# Backend questions
cd 05-backend/

# Config questions
cd 06-configuration/

# Standards questions (CRITICAL for AI)
cd 07-standards/
```

**Search by Keyword:**
```bash
# Find all mentions of "session"
grep -r "session" .archon-knowledge-base/

# Find all API endpoints
grep -r "GET /api" .archon-knowledge-base/

# Find security issues
grep -r "CRITICAL" .archon-knowledge-base/
```

### For IDE Integration

**VS Code:**
1. Install "Markdown All in One" extension
2. Open `.archon-knowledge-base/` folder
3. Use "Markdown: Open Preview" for navigation
4. Search across all files with Cmd/Ctrl+Shift+F

**JetBrains IDEs:**
1. Open `.archon-knowledge-base/` as folder
2. Use built-in markdown preview
3. Search across files with Shift+Shift

---

## Next Steps

### Immediate (This Week)

**1. Review Documentation**
- Read through all README files in each domain
- Verify accuracy of documented patterns
- Check for any missing information

**2. Fix Critical Issues**
- Phase 1 dead code cleanup (5 minutes, zero risk)
- Fix 18 API mismatches (1-2 weeks)
- Fix critical UI bugs (dialogs, toasts - 1 day)
- Enable SSL on database connection (1 hour)

**3. Setup Archon**
- Install Archon following `ARCHON_CAPABILITIES_REFERENCE.md`
- Import this knowledge base
- Configure project/task management
- Test RAG retrieval with sample queries

### Short-term (Next Month)

**4. Backend Refactoring (6-8 weeks)**
- Refactor efficiency and ki-reports modules (HIGH PRIORITY)
- Add service layers to 4 modules
- Migrate to Drizzle pattern consistently
- Follow plan in `05-backend/ARCHITECTURE_ASSESSMENT.md`

**5. UI Redesign (12 weeks)**
- Fix critical bugs (week 1)
- Build unified components (weeks 2-4)
- Mobile responsiveness (weeks 5-8)
- Accessibility (weeks 9-12)
- Follow plan in `04-frontend/UI_REDESIGN_NEEDS.md`

**6. Dead Code Cleanup (4-5 weeks)**
- Phase 1: Archives, backups (5 minutes)
- Phase 2: Backend dead code (1 week)
- Phase 3: Frontend dead code (1-2 weeks)
- Phase 4: Import cleanup (1 week)
- Phase 5: Duplicate consolidation (2-3 weeks)
- Follow plan in `.dead-code-analysis-reports/MASTER_REPORT.md`

### Long-term (Ongoing)

**7. Maintain Documentation**
- Update knowledge base when patterns change
- Document new features as added
- Keep API catalog current
- Update security assessments

**8. Enforce Standards**
- Use code review checklists in `05-backend/README.md`
- Enforce module pattern from `05-backend/MODULE_PATTERN_STANDARD.md`
- Follow UI guidelines from `04-frontend/DESIGN_SYSTEM_CURRENT.md`
- Run monthly dead code audits

**9. Security Hardening**
- Address all vulnerabilities in `03-authentication/SECURITY_FEATURES.md`
- Implement security headers
- Add CSRF protection
- Regular security audits

---

## Maintenance

### Keeping Documentation Current

**When Adding Features:**
1. Update relevant markdown files in knowledge base
2. Add new endpoints to `02-api-endpoints/`
3. Document new tables in `01-database/`
4. Update component inventory in `04-frontend/`

**When Refactoring:**
1. Update pattern documentation
2. Mark deprecated patterns clearly
3. Update consistency analysis
4. Re-run dead code analysis

**When Deploying:**
1. Update deployment requirements
2. Document new environment variables
3. Update external services list
4. Review security features

### Documentation Standards

All documentation follows these standards:
- No emojis in content
- Dated and timestamped
- Clear table of contents
- Code examples included
- Cross-referenced
- Consistent formatting
- Factual (no opinions)

---

## Questions?

For specific information:
- **Database**: Check `01-database/README.md`
- **API**: Check `02-api-endpoints/README.md`
- **Auth**: Check `03-authentication/AUTH_OVERVIEW.md`
- **Frontend**: Check `04-frontend/README.md`
- **Backend**: Check `05-backend/README.md`
- **Config**: Check `06-configuration/CONFIGURATION_OVERVIEW.md`
- **Standards**: Check `07-standards/README.md` ⚠️ CRITICAL for AI

For general questions:
- Review this README
- Check individual domain README files
- Search across all markdown files
- Consult Archon with RAG queries (once setup)

---

**Knowledge Base Created**: 2025-10-13
**Total Documentation**: 49 files, ~623 KB
**Coverage**: 100% across all 7 domains + critical standards
**Created By**: 6 specialized documentation agents
**Standards Added**: 2025-10-13 (7 critical pattern files)
**Status**: Complete and ready for Archon integration

---

## Summary Statistics

| Domain | Files | Size | Key Metrics |
|--------|-------|------|-------------|
| **Database** | 5 | 66 KB | 20 tables, 72+ indexes, 30+ relationships |
| **API Endpoints** | 6 | 85 KB | 120+ endpoints, 22 modules, 18 mismatches |
| **Authentication** | 5 | 55 KB | 3 roles, 90+ protected routes, 8 rate-limited |
| **Frontend** | 8 | 95 KB | 24 components, 11 features, 200+ UI issues |
| **Backend** | 8 | 111 KB | 23 modules, 26% pattern adherence |
| **Configuration** | 8 | 111 KB | 11 env vars, 4 services, 170 dependencies |
| **Standards** ⚠️ | 7 | 100 KB | 6 critical patterns, P0 priority, AI guidance |
| **TOTAL** | **49** | **~623 KB** | **100% coverage + standards** |

---

**Ready for Production Enhancement with Archon**
