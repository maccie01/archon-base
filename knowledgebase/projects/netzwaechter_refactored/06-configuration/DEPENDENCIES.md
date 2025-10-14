# Dependencies

Comprehensive documentation of all key packages, their versions, and purposes in the Netzwächter project.

Created: 2025-10-13
Last Updated: 2025-10-13

---

## Overview

The Netzwächter project uses a curated set of dependencies to provide database access, UI components, authentication, testing, and build tools. This document categorizes and explains each major dependency.

**Package Manager:** pnpm 10.2.0
**Node Version:** 20.18.2+
**Total Dependencies:** 144 production + 26 development

---

## Core Framework Dependencies

### Backend Framework

#### express@4.21.2
**Purpose:** Web application framework
**Category:** Core
**Usage:** HTTP server, routing, middleware

**Features:**
- HTTP request handling
- Route management
- Middleware pipeline
- Static file serving

#### express-session@1.18.1
**Purpose:** Session management middleware
**Category:** Authentication
**Usage:** User session storage

**Related:**
- `connect-pg-simple@10.0.0` - PostgreSQL session store
- Session table in database

#### express-rate-limit@8.1.0
**Purpose:** Rate limiting middleware
**Category:** Security
**Usage:** API rate limiting, DDoS protection

**Configuration:**
- Window: 15 minutes
- Max requests: 100 per window
- Applied to /api routes

### Frontend Framework

#### react@18.3.1
**Purpose:** UI library
**Category:** Core
**Usage:** Component-based UI

**Features:**
- Component composition
- State management
- Hooks API
- Virtual DOM

#### react-dom@18.3.1
**Purpose:** React DOM renderer
**Category:** Core
**Usage:** Browser rendering

**Related:**
- react@18.3.1
- Browser DOM APIs

---

## Database & ORM

### Database Drivers

#### @neondatabase/serverless@0.10.4
**Purpose:** Neon PostgreSQL driver
**Category:** Database
**Usage:** Serverless PostgreSQL connections

**Features:**
- Edge-compatible
- WebSocket support
- Connection pooling
- Low latency

#### pg@8.16.3
**Purpose:** PostgreSQL client
**Category:** Database
**Usage:** Connection pool, query execution

**Features:**
- Connection pooling
- Prepared statements
- Transaction support
- SSL/TLS connections

### ORM & Schema

#### drizzle-orm@0.39.1
**Purpose:** TypeScript ORM
**Category:** Database
**Usage:** Type-safe database queries

**Features:**
- Type-safe queries
- Schema definition
- Relation mapping
- Migration support

**Development:**
- `drizzle-kit@0.30.4` - Migration tool

#### drizzle-zod@0.7.0
**Purpose:** Zod schema generation
**Category:** Validation
**Usage:** Auto-generate Zod schemas from Drizzle

---

## Validation & Type Safety

### Schema Validation

#### zod@3.25.76
**Purpose:** TypeScript-first schema validation
**Category:** Validation
**Usage:** Input validation, API schemas, form validation

**Features:**
- Type inference
- Runtime validation
- Composable schemas
- Error messages

**Related:**
- `zod-validation-error@3.4.0` - Human-readable errors

### TypeScript

#### typescript@5.6.3
**Purpose:** TypeScript compiler
**Category:** Development
**Usage:** Type checking, compilation

**Features:**
- Static typing
- Type inference
- IDE support
- Strict mode

---

## UI Components & Styling

### Component Library

#### Radix UI (@radix-ui/*)
**Purpose:** Unstyled accessible components
**Category:** UI
**Count:** 23 packages
**Version:** Various (1.x - 2.x)

**Key Components:**
- Dialog, Dropdown, Popover
- Select, Checkbox, Switch
- Tabs, Accordion, Collapsible
- Toast, Tooltip, Avatar
- And more...

**Features:**
- Accessibility (ARIA)
- Keyboard navigation
- Focus management
- Unstyled (customizable)

### Styling

#### tailwindcss@3.4.17
**Purpose:** Utility-first CSS framework
**Category:** Styling
**Usage:** Component styling, layout

**Features:**
- Utility classes
- Responsive design
- Dark mode
- JIT compilation

**Plugins:**
- `tailwindcss-animate@1.0.7` - Animations
- `@tailwindcss/typography@0.5.15` - Prose styling

**Utilities:**
- `tailwind-merge@2.6.0` - Class merging
- `class-variance-authority@0.7.1` - Variant management
- `clsx@2.1.1` - Class name helper

### Icons

#### lucide-react@0.453.0
**Purpose:** Icon library
**Category:** UI
**Usage:** Icons throughout application

**Features:**
- 1000+ icons
- Tree-shakeable
- Customizable
- Consistent design

#### react-icons@5.4.0
**Purpose:** Additional icon library
**Category:** UI
**Usage:** Supplementary icons

---

## Data Visualization

### Charts & Graphs

#### recharts@2.15.4
**Purpose:** React charting library
**Category:** Visualization
**Usage:** Energy consumption charts, efficiency graphs

**Features:**
- Responsive charts
- Customizable
- Animation support
- Multiple chart types

### Maps

#### leaflet@1.9.4
**Purpose:** Interactive maps library
**Category:** Mapping
**Usage:** Object location visualization

**Features:**
- Interactive maps
- Tile layers
- Markers & popups
- Zoom controls

#### react-leaflet@4.2.1
**Purpose:** React wrapper for Leaflet
**Category:** Mapping
**Usage:** React integration for maps

**Types:** `@types/leaflet@1.9.20`

---

## Forms & Input

### Form Management

#### react-hook-form@7.55.0
**Purpose:** Form state management
**Category:** Forms
**Usage:** Form handling, validation

**Features:**
- Performance (uncontrolled)
- Validation integration
- TypeScript support
- Error handling

#### @hookform/resolvers@3.10.0
**Purpose:** Validation resolvers
**Category:** Forms
**Usage:** Zod integration with react-hook-form

### Date Pickers

#### react-day-picker@8.10.1
**Purpose:** Date picker component
**Category:** UI
**Usage:** Date selection in forms

**Related:**
- `date-fns@3.6.0` - Date utilities

### File Upload

#### @uppy/core@4.5.2 + plugins
**Purpose:** File upload framework
**Category:** File Upload
**Usage:** Logbook attachments, file management

**Plugins:**
- `@uppy/react@4.5.2` - React integration
- `@uppy/dashboard@4.4.3` - UI dashboard
- `@uppy/aws-s3@4.3.2` - S3 upload
- `@uppy/drag-drop@4.2.2` - Drag & drop
- `@uppy/file-input@4.2.2` - File input
- `@uppy/progress-bar@4.3.2` - Progress bar

---

## Authentication & Security

### Password Hashing

#### bcrypt@6.0.0
**Purpose:** Password hashing
**Category:** Security
**Usage:** User password storage

**Features:**
- Salted hashing
- Configurable rounds
- Secure comparison

**Alternative:** `bcryptjs@3.0.2` - Pure JavaScript implementation

### Unique IDs

#### nanoid@5.1.5
**Purpose:** Unique ID generation
**Category:** Utility
**Usage:** Session IDs, unique identifiers

#### uuid@13.0.0
**Purpose:** UUID generation
**Category:** Utility
**Usage:** Standard UUID format

---

## Email & Communication

### Email

#### nodemailer@7.0.6
**Purpose:** Email sending
**Category:** Email
**Usage:** Password resets, notifications

**Features:**
- SMTP transport
- HTML emails
- Attachments
- Template support

**Alternative:** `@sendgrid/mail@8.1.5` - SendGrid integration (available)

---

## Data Processing

### CSV Processing

#### csv-parser@3.2.0
**Purpose:** CSV parsing
**Category:** Data Processing
**Usage:** Import energy data

#### fast-csv@5.0.5
**Purpose:** Fast CSV reading/writing
**Category:** Data Processing
**Usage:** Data export, import

### PDF Generation

#### jspdf@3.0.2
**Purpose:** PDF generation
**Category:** PDF
**Usage:** Report generation

#### jspdf-autotable@5.0.2
**Purpose:** Table generation for jsPDF
**Category:** PDF
**Usage:** Tabular data in PDFs

### Canvas

#### html2canvas@1.4.1
**Purpose:** HTML to canvas rendering
**Category:** Export
**Usage:** Screenshot/export functionality

---

## HTTP & Networking

### HTTP Client

#### axios@1.12.2
**Purpose:** HTTP client
**Category:** HTTP
**Usage:** External API calls, weather data

**Features:**
- Promise-based
- Request/response interceptors
- Timeout support
- Browser & Node.js

### WebSocket

#### ws@8.18.0
**Purpose:** WebSocket implementation
**Category:** Real-time
**Usage:** Real-time updates, monitoring

**Types:** `@types/ws@8.5.13`

---

## State Management & Data Fetching

### React Query

#### @tanstack/react-query@5.60.5
**Purpose:** Server state management
**Category:** State Management
**Usage:** API data fetching, caching

**Features:**
- Automatic caching
- Background refetching
- Optimistic updates
- Pagination support

---

## Routing

### Client-Side Routing

#### wouter@3.3.5
**Purpose:** Lightweight React router
**Category:** Routing
**Usage:** Frontend navigation

**Features:**
- Small bundle size (~1.5kb)
- Hooks-based API
- Browser history
- Pattern matching

---

## Animation & UI Enhancements

### Animation

#### framer-motion@11.13.1
**Purpose:** Animation library
**Category:** Animation
**Usage:** Component animations, transitions

**Features:**
- Declarative animations
- Gesture support
- Layout animations
- Spring physics

#### canvas-confetti@1.9.3
**Purpose:** Confetti effects
**Category:** UI
**Usage:** Celebration animations

**Types:** `@types/canvas-confetti@1.9.0`

### UI Enhancements

#### embla-carousel-react@8.6.0
**Purpose:** Carousel component
**Category:** UI
**Usage:** Image/content carousels

#### next-themes@0.4.6
**Purpose:** Theme management
**Category:** UI
**Usage:** Dark/light mode switching

#### vaul@1.1.2
**Purpose:** Drawer component
**Category:** UI
**Usage:** Mobile drawer UI

---

## Testing

### Test Runners

#### vitest@3.2.4
**Purpose:** Unit test framework
**Category:** Testing
**Usage:** Unit and integration tests

**Features:**
- Vite-powered
- Fast execution
- ESM support
- Snapshot testing

**Plugins:**
- `@vitest/ui@3.2.4` - Test UI
- `@vitest/coverage-v8@3.2.4` - Coverage reports

#### @playwright/test@1.56.0
**Purpose:** E2E testing framework
**Category:** Testing
**Usage:** End-to-end browser tests

**Features:**
- Cross-browser testing
- Auto-waiting
- Screenshots/videos
- Network interception

### Testing Libraries

#### @testing-library/react@16.3.0
**Purpose:** React testing utilities
**Category:** Testing
**Usage:** Component testing

**Features:**
- User-centric queries
- Accessibility testing
- Async utilities

**Related:**
- `@testing-library/jest-dom@6.9.1` - Custom matchers
- `@testing-library/user-event@14.6.1` - User interactions

#### jsdom@27.0.0
**Purpose:** DOM implementation
**Category:** Testing
**Usage:** Browser environment for tests

#### msw@2.11.3
**Purpose:** API mocking
**Category:** Testing
**Usage:** Mock HTTP requests in tests

---

## AI & External APIs

### OpenAI

#### openai@5.23.1
**Purpose:** OpenAI API client
**Category:** AI
**Usage:** AI-powered reports (optional)

**Status:** Installed but not actively used

### Google Cloud

#### @google-cloud/storage@7.16.0
**Purpose:** Google Cloud Storage
**Category:** Storage
**Usage:** File storage (potential)

**Status:** Installed, usage unclear

#### google-auth-library@10.2.1
**Purpose:** Google authentication
**Category:** Auth
**Usage:** OAuth or service accounts

---

## Utilities

### Date/Time

#### date-fns@3.6.0
**Purpose:** Date utilities
**Category:** Utility
**Usage:** Date formatting, manipulation

**Features:**
- Immutable
- Tree-shakeable
- TypeScript support
- i18n support

### Caching

#### memoizee@0.4.17
**Purpose:** Function memoization
**Category:** Performance
**Usage:** Cache expensive computations

**Types:** `@types/memoizee@0.4.12`

### Session Storage

#### memorystore@1.6.7
**Purpose:** In-memory session store
**Category:** Sessions
**Usage:** Development session storage (alternative)

---

## Development Tools

### Build Tools

#### vite@5.4.19
**Purpose:** Frontend build tool
**Category:** Build
**Usage:** Frontend bundling, dev server

**Features:**
- Fast HMR
- ESM-based
- Plugin system
- Optimized builds

#### esbuild@0.25.0
**Purpose:** JavaScript bundler
**Category:** Build
**Usage:** Backend compilation

**Features:**
- Extremely fast
- ES6 modules
- Tree shaking
- Minification

#### tsx@4.19.1
**Purpose:** TypeScript execution
**Category:** Development
**Usage:** Run TypeScript directly

**Features:**
- No compilation step
- Watch mode
- Fast execution

### Linting & Formatting

**Note:** Linting configuration not centralized in root package.json, may be per-package.

### Type Definitions

**Major @types packages:**
- `@types/node@20.16.11` - Node.js
- `@types/react@18.3.11` - React
- `@types/react-dom@18.3.1` - React DOM
- `@types/express@4.17.21` - Express
- `@types/express-session@1.18.0` - Express sessions
- `@types/pg@8.15.5` - PostgreSQL client
- `@types/bcrypt@6.0.0` - Bcrypt
- `@types/multer@2.0.0` - File uploads
- `@types/nodemailer@7.0.1` - Email

---

## Optional Dependencies

### bufferutil@4.0.8
**Purpose:** WebSocket performance
**Category:** Performance
**Usage:** Faster WebSocket operations

**Note:** Optional dependency for ws package

---

## Dependency Management

### Installation

**Install All:**
```bash
pnpm install
```

**Add Dependency:**
```bash
pnpm add package-name
```

**Add Dev Dependency:**
```bash
pnpm add -D package-name
```

**Update Dependencies:**
```bash
pnpm update
```

### Workspaces

**Structure:**
```
node_modules/              # Shared dependencies
apps/*/node_modules/       # App-specific (if any)
packages/*/node_modules/   # Package-specific (if any)
```

**Benefits:**
- Shared dependencies (disk space savings)
- Consistent versions
- Fast installation (hard links)

---

## Security Considerations

### Vulnerability Scanning

**Check Vulnerabilities:**
```bash
pnpm audit
```

**Fix Vulnerabilities:**
```bash
pnpm audit --fix
```

### Updates

**Check Outdated:**
```bash
pnpm outdated
```

**Update Specific:**
```bash
pnpm update package-name
```

**Update All:**
```bash
pnpm update -r
```

### Best Practices

1. Regular updates (monthly)
2. Security patches immediately
3. Test after updates
4. Review breaking changes
5. Pin critical versions

---

## Dependency Categories Summary

| Category | Count | Examples |
|----------|-------|----------|
| Core Framework | 5 | express, react, react-dom |
| Database | 5 | pg, drizzle-orm, @neondatabase/serverless |
| UI Components | 25+ | @radix-ui/*, lucide-react |
| Styling | 6 | tailwindcss, tailwind-merge |
| Forms | 4 | react-hook-form, react-day-picker |
| Data Viz | 3 | recharts, leaflet, react-leaflet |
| Testing | 8 | vitest, playwright, testing-library |
| Build Tools | 5 | vite, esbuild, tsx, turbo |
| Security | 3 | bcrypt, express-rate-limit |
| Utilities | 10+ | date-fns, axios, zod, nanoid |

---

## Version Pinning Strategy

### Exact Versions
**Used for:** Critical dependencies
**Format:** `"package": "1.2.3"`

### Caret Ranges
**Used for:** Most dependencies
**Format:** `"package": "^1.2.3"`
**Allows:** 1.2.x, 1.x.x (not 2.0.0)

### Tilde Ranges
**Rarely used**
**Format:** `"package": "~1.2.3"`
**Allows:** 1.2.x only

---

## References

### Package Information
- `package.json` - Root dependencies
- `pnpm-lock.yaml` - Lock file
- `node_modules/` - Installed packages

### External Resources
- [npm Registry](https://www.npmjs.com/)
- [pnpm Documentation](https://pnpm.io/)
- [Package Diff Tool](https://diff.intrinsic.com/)
