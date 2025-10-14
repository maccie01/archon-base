# Global Shared Knowledge Base

Created: 2025-10-13

This directory contains cross-project technology documentation, patterns, and best practices that apply to all projects in `/Users/janschubert/code-projects/`.

## Purpose

The global knowledge base serves to:
1. Document technologies used across multiple projects
2. Establish consistent patterns and best practices
3. Reduce duplication of documentation
4. Speed up onboarding for new projects
5. Provide quick reference for common tasks

## Documentation Structure

```
.global-shared-knowledge/
├── README.md (this file)
├── TECHNOLOGY_ANALYSIS.md (comprehensive analysis)
├── QUICK_REFERENCE.md (quick lookup guide)
├── DOCUMENTATION_PRIORITIES.md (documentation roadmap)
├── 01-react-frontend/ (React, Vite, Tailwind, etc.)
├── 02-nodejs-backend/ (Express, TypeScript, etc.)
├── 03-database-orm/ (PostgreSQL, Drizzle, etc.)
├── 04-security-auth/ (Authentication, security)
├── 05-testing-quality/ (Vitest, Playwright, etc.)
└── 06-configuration/ (Monorepo, build tools, etc.)
```

## Quick Navigation

### Start Here
- **New to the codebase?** → Start with [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)
- **Understanding the tech stack?** → Read [TECHNOLOGY_ANALYSIS.md](./TECHNOLOGY_ANALYSIS.md)
- **Contributing documentation?** → Check [DOCUMENTATION_PRIORITIES.md](./DOCUMENTATION_PRIORITIES.md)

### By Technology

#### Frontend (React)
📁 **Location**: `01-react-frontend/`
- React 18 patterns and best practices
- Vite configuration and optimization
- Tailwind CSS setup and utilities
- Radix UI component patterns
- TanStack Query (React Query)
- React Hook Form + Zod validation
- Framer Motion animations

#### Backend (Node.js)
📁 **Location**: `02-nodejs-backend/`
- Express.js setup and patterns
- TypeScript configuration (ESM)
- API design and structure
- Middleware patterns
- Error handling strategies
- Session management
- Zod validation
- File uploads and processing
- WebSocket patterns

#### Database & ORM
📁 **Location**: `03-database-orm/`
- PostgreSQL setup and patterns
- Drizzle ORM configuration
- Schema design patterns
- Migration strategies
- Query optimization
- Connection pooling

#### Security & Authentication
📁 **Location**: `04-security-auth/`
- Session-based authentication
- Password hashing (bcrypt)
- JWT patterns (legacy)
- Security headers (helmet)
- Rate limiting
- CSRF protection
- CORS configuration

#### Testing & Quality
📁 **Location**: `05-testing-quality/`
- Vitest setup and patterns
- Playwright E2E testing
- MSW (Mock Service Worker)
- Unit test patterns
- Integration test patterns
- Coverage strategies
- CI/CD integration

#### Configuration & Build
📁 **Location**: `06-configuration/`
- Monorepo setup (Turborepo)
- pnpm workspaces
- Shared packages
- Environment variables
- TypeScript configuration
- Build optimization

## Technology Index

### Most Frequently Used

| Technology | Category | Projects Using | Documentation Status |
|-----------|----------|----------------|---------------------|
| React 18 | Frontend | 5 projects | ⬜ Planned |
| Express.js | Backend | 6 projects | ⬜ Planned |
| TypeScript | Language | 8 projects | ⬜ Planned |
| Tailwind CSS | Styling | 5 projects | ⬜ Planned |
| Drizzle ORM | Database | 3 projects | ⬜ Planned |
| PostgreSQL | Database | 3 projects | ⬜ Planned |
| Vite | Build Tool | 3 projects | ⬜ Planned |
| Vitest | Testing | 2 projects | ⬜ Planned |
| Zod | Validation | 6 projects | ⬜ Planned |
| Next.js | Framework | 3 projects | ⬜ Planned |

See [TECHNOLOGY_ANALYSIS.md](./TECHNOLOGY_ANALYSIS.md) for complete technology breakdown.

## Project Reference Map

Each project uses a different combination of technologies. Use this map to find examples:

### Modern Full-Stack (Recommended Reference)
**Project**: `monitoring_firma/netzwaechter-refactored`
- **Stack**: React + Vite + Express + PostgreSQL + Drizzle ORM
- **Architecture**: Turborepo monorepo with shared packages
- **Testing**: Vitest + Playwright + MSW
- **Use for**: Reference architecture for new projects

### Next.js + Supabase
**Project**: `Nexorithm-website`
- **Stack**: Next.js 15 + React 19 + Supabase
- **Architecture**: Jamstack
- **Use for**: Marketing sites, rapid prototyping

### AI/LangChain Integration
**Project**: `Perplexica`
- **Stack**: Next.js + Express + SQLite + LangChain
- **Architecture**: Microservices
- **Use for**: AI/LLM integration patterns

### Data Science/ML
**Project**: `tawian/dhbw-tp-forecasting`
- **Stack**: Python + Pandas + Darts + Prophet
- **Architecture**: Jupyter notebooks + pipelines
- **Use for**: Time series forecasting, data analysis

### Legacy Patterns
**Projects**: `monitoring_firma/moni`, `monitoring_firma/ws_energieservice`
- **Stack**: Express + Sequelize + MySQL/PostgreSQL
- **Use for**: Migration reference, legacy pattern understanding

## Common Patterns

### Authentication
```
Session-based (Recommended):
  express-session + connect-pg-simple + bcrypt

JWT (Legacy):
  jsonwebtoken + bcrypt
```

### Database Access
```
Modern:
  Drizzle ORM + PostgreSQL

Legacy:
  Sequelize + MySQL/PostgreSQL
```

### Frontend State
```
Server State:
  TanStack Query

Client State:
  React useState/useReducer

Routing:
  Wouter (SPA) or Next.js (SSR)
```

### Form Handling
```
React Hook Form + Zod + @hookform/resolvers
```

### Styling
```
Tailwind CSS + Radix UI + clsx/tailwind-merge
```

### Testing
```
Unit/Integration: Vitest + @testing-library/react
E2E: Playwright
Mocking: MSW
```

## Quick Snippets

### Start New Project
```bash
# Clone reference architecture
cp -r monitoring_firma/netzwaechter-refactored my-new-project
cd my-new-project

# Install dependencies
pnpm install

# Setup environment
cp .env.example .env

# Start development
pnpm dev
```

### Common Commands
```bash
# Development
pnpm dev              # Start all apps
pnpm dev:frontend     # Start frontend only
pnpm dev:backend      # Start backend only

# Building
pnpm build            # Build all
pnpm typecheck        # Check types

# Testing
pnpm test             # Run all tests
pnpm test:unit        # Unit tests
pnpm test:e2e         # E2E tests

# Database
pnpm db:push          # Push schema changes
```

## Getting Started Checklist

### For New Developers
- [ ] Read [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)
- [ ] Review [TECHNOLOGY_ANALYSIS.md](./TECHNOLOGY_ANALYSIS.md)
- [ ] Clone reference project: `monitoring_firma/netzwaechter-refactored`
- [ ] Review project-specific README
- [ ] Check documentation in relevant directories

### For New Projects
- [ ] Choose tech stack from [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)
- [ ] Use reference project as template
- [ ] Follow patterns from documentation
- [ ] Add project to [TECHNOLOGY_ANALYSIS.md](./TECHNOLOGY_ANALYSIS.md)

### For Contributing
- [ ] Check [DOCUMENTATION_PRIORITIES.md](./DOCUMENTATION_PRIORITIES.md)
- [ ] Follow documentation template
- [ ] Use examples from real projects
- [ ] Submit for review

## Documentation Standards

All documentation in this knowledge base should:
1. Use Markdown format
2. Include creation date and last updated date
3. Provide real-world examples from projects
4. Follow the standard template structure
5. Be technology-focused, not project-specific
6. Include troubleshooting sections
7. Link to official documentation

## Maintenance

### Review Schedule
- **Weekly**: During initial documentation phase
- **Monthly**: Review P0 (critical) documentation
- **Quarterly**: Review P1 (high priority) documentation
- **Semi-annually**: Full review of all documentation

### Update Process
1. Identify outdated or missing documentation
2. Create/update documentation following template
3. Add real examples from projects
4. Review and test code examples
5. Update version numbers and dates
6. Link from relevant index files

## Contributing

### Adding Documentation
1. Check [DOCUMENTATION_PRIORITIES.md](./DOCUMENTATION_PRIORITIES.md) for priorities
2. Use the standard template structure
3. Include practical examples from real projects
4. Ensure code examples are tested and working
5. Update this README if adding new categories

### Reporting Issues
- Missing documentation for a technology
- Outdated or incorrect information
- Better pattern discovered
- Security vulnerability in documented pattern

## Statistics

### Coverage
- **Total technologies identified**: 50+
- **Projects analyzed**: 12
- **Documentation files created**: 4 (foundation)
- **Documentation files planned**: 40+
- **Estimated completion time**: 65-93 hours

### Usage Distribution
- **JavaScript/TypeScript**: 67% of projects (8/12)
- **Python**: 33% of projects (4/12)
- **Frontend frameworks**: React (5), Next.js (3)
- **Backend frameworks**: Express (6), Next.js API (2)
- **Databases**: PostgreSQL (3), MySQL (1), SQLite (2)

## Version History

### 2025-10-13 - Initial Creation
- Created global knowledge base structure
- Completed comprehensive technology analysis
- Created quick reference guide
- Defined documentation priorities
- Analyzed 12 projects across all categories
- Identified 50+ technologies in use
- Mapped common patterns and best practices

## Next Steps

### Immediate (This Week)
1. Create React best practices documentation
2. Create Express.js patterns documentation
3. Create TypeScript configuration guide
4. Create Tailwind CSS setup guide

### Short-term (Next 2 Weeks)
1. Complete all P0 (critical) documentation
2. Begin P1 (high priority) documentation
3. Create documentation navigation/search
4. Gather feedback from team

### Medium-term (Next Month)
1. Complete P1 documentation
2. Begin P2 (medium priority) documentation
3. Create video tutorials for complex topics
4. Add interactive examples

### Long-term (Next Quarter)
1. Complete all planned documentation
2. Build automated documentation system
3. Create onboarding tutorials
4. Implement documentation feedback loop

## Resources

### Official Documentation Links
- [React](https://react.dev)
- [Express.js](https://expressjs.com)
- [TypeScript](https://www.typescriptlang.org)
- [Vite](https://vitejs.dev)
- [Vitest](https://vitest.dev)
- [Playwright](https://playwright.dev)
- [Drizzle ORM](https://orm.drizzle.team)
- [Tailwind CSS](https://tailwindcss.com)
- [Radix UI](https://www.radix-ui.com)
- [TanStack Query](https://tanstack.com/query)
- [Next.js](https://nextjs.org)

### Internal Resources
- Project codebases in `/Users/janschubert/code-projects/`
- Reference architecture: `monitoring_firma/netzwaechter-refactored`
- Technology analysis: [TECHNOLOGY_ANALYSIS.md](./TECHNOLOGY_ANALYSIS.md)

## Contact & Support

For questions about:
- **General documentation**: Check [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)
- **Specific technologies**: Check relevant directory
- **Documentation gaps**: See [DOCUMENTATION_PRIORITIES.md](./DOCUMENTATION_PRIORITIES.md)
- **Project references**: See [TECHNOLOGY_ANALYSIS.md](./TECHNOLOGY_ANALYSIS.md)

---

**Last Updated**: 2025-10-13
**Status**: Foundation Complete, Documentation In Progress
**Next Review**: Weekly during initial documentation phase
