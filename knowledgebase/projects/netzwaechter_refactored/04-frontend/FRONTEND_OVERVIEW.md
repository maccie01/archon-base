# Frontend Overview - Netzwächter React Application

**Created:** 2025-10-13
**Last Updated:** 2025-10-13

## Technology Stack

### Core Framework
- **React 18** - Modern React with hooks and concurrent features
- **TypeScript** - Full type safety across the application
- **Vite** - Fast development server and build tool

### Routing
- **Wouter** - Lightweight routing library (~1.2KB)
  - Location: `/Apps/frontend-web/src/App.tsx`
  - Pattern: File-based routing with URL parameters
  - Features:
    - Protected routes with auth guards
    - Dynamic UI mode switching (cockpit vs. Strawa layout)
    - URL parameter-based navigation

### State Management
- **TanStack Query (React Query)** - Server state management
  - Configuration: `/Apps/frontend-web/src/lib/queryClient.ts`
  - Used for:
    - API data fetching and caching
    - Mutations with optimistic updates
    - Real-time data synchronization
  - Query keys follow REST endpoint patterns: `['/api/endpoint']`

### UI Component Libraries
- **Radix UI** - Headless accessible components
- **shadcn/ui** - Pre-styled Radix components with Tailwind
- **Tailwind CSS** - Utility-first CSS framework
- **Heroicons** - Icon library (24/outline)
- **Lucide React** - Modern icon library

## Application Architecture

### Entry Point
```typescript
// src/main.tsx
- React root initialization
- Axe-core accessibility testing (dev only)
- Error boundary setup
```

### Main App Component
```typescript
// src/App.tsx
- QueryClientProvider setup
- TooltipProvider for global tooltips
- Toaster for notifications
- SessionWarning component
- RouterMain with authentication guards
```

## Routing Structure

### Authentication Flow
1. **Loading State**: Shows spinner while checking auth status
2. **Superadmin Routes**: Special routes for superadmin users
3. **Unauthenticated Routes**: Login pages only
4. **Authenticated Routes**: Full application access

### UI Mode System
The application has two distinct UI modes controlled by `useUIMode` hook:

#### 1. Strawa Mode (Default)
- **Trigger**: Any URL without `ui=cockpit` parameter
- **Layout**: `LayoutStrawaTabs` component
- **Features**:
  - Vertical sidebar with Strawa branding
  - Tab-based navigation (4 main tabs)
  - Integrated dashboard view
  - Mobile-responsive collapsible sidebar

#### 2. Cockpit Mode
- **Trigger**: URL with `?ui=cockpit` parameter
- **Layout**: `Layout` component with full sidebar
- **Features**:
  - Full navigation sidebar
  - Traditional page routing
  - Admin dashboard access
  - Extended menu options

### Protected Routes
All routes require authentication except login pages. Routes are organized by feature:

- **Monitoring**: `/dashboard`, `/maps`, `/network-monitor`, `/performance-test`
- **KI Reports**: `/grafana-dashboards`, `/grafana-dashboard`
- **Energy**: `/energy-data`, `/efficiency`, `/db-energy-config`
- **Temperature**: `/temperature-analysis`, `/temperatur-analyse`
- **Objects**: `/objects`, `/objektverwaltung`
- **Users**: `/users`, `/user-management`, `/user`, `/user-settings`
- **Settings**: `/system-setup`, `/setup`, `/api-management`, `/modbus-config`, `/devices`, `/geraeteverwaltung`
- **Admin**: `/admin-dashboard`, `/logbook`

## Feature-Based Architecture

### Directory Structure
```
src/
├── features/
│   ├── admin-dashboard/
│   ├── auth/
│   ├── energy/
│   ├── ki-reports/
│   ├── logbook/
│   ├── monitoring/
│   ├── objects/
│   ├── settings/
│   ├── temperature/
│   └── users/
├── components/       # Shared components
├── hooks/           # Custom hooks
├── lib/            # Utilities and configs
├── pages/          # Legacy pages (minimal)
└── styles/         # Global styles
```

### Feature Module Pattern
Each feature follows this structure:
```
feature-name/
├── api/              # API client functions
├── components/       # Feature-specific components
├── hooks/           # Feature-specific hooks
├── pages/           # Route components
├── types/           # TypeScript types
└── utils/           # Feature utilities
```

## State Management Patterns

### Server State (TanStack Query)
```typescript
// Query pattern
const { data, isLoading, error } = useQuery({
  queryKey: ['/api/endpoint'],
  staleTime: 5 * 60 * 1000,  // 5 minutes
  gcTime: 10 * 60 * 1000,    // 10 minutes
});

// Mutation pattern
const mutation = useMutation({
  mutationFn: (data) => apiRequest('POST', '/api/endpoint', data),
  onSuccess: () => {
    queryClient.invalidateQueries(['/api/endpoint']);
    toast({ title: 'Success' });
  },
});
```

### Local State (React Hooks)
- `useState` for component-level state
- `useEffect` for side effects
- Custom hooks for shared logic (e.g., `useAuth`, `useUIMode`)

### Authentication State
Managed by `useAuth` hook:
- User data cached in React Query
- Automatic refetch on focus
- Logout clears all cached data
- Session warning for expiring tokens

## Data Fetching Patterns

### API Client
```typescript
// lib/queryClient.ts
export const apiRequest = async (method, url, data?) => {
  // Automatic authentication
  // Error handling
  // JSON serialization
};
```

### Common Query Patterns
1. **Dashboard KPIs**: Aggregate data with 5-minute cache
2. **Object Lists**: Full object data with invalidation on updates
3. **Settings**: Long-lived cache (10 minutes)
4. **Real-time Data**: Short cache (30 seconds) with refetch on focus

## Performance Optimizations

### Code Splitting
- Route-based lazy loading
- Feature module bundling
- Dynamic imports for heavy components

### Caching Strategy
- Aggressive caching for static data (settings, configurations)
- Short cache for real-time data (temperatures, status)
- Background refetch for stale data
- Optimistic updates for mutations

### Render Optimization
- React.memo for expensive components
- useMemo for computed values
- useCallback for event handlers
- Virtual scrolling for large lists (planned)

## Build Configuration

### Vite Config
- TypeScript compilation
- Path aliases (@/ → src/)
- CSS processing with PostCSS
- Production optimizations

### Environment Variables
```typescript
import.meta.env.MODE      // development | production
import.meta.env.DEV       // boolean
```

## Testing Setup

### Testing Library
- Vitest for unit/integration tests
- React Testing Library for component tests
- MSW (Mock Service Worker) for API mocking

### Test Files
- Located in `__tests__` directories
- Pattern: `*.test.tsx`
- Setup: `src/test/setup.ts`
- Mocks: `src/test/mocks/`

## Accessibility

### Features
- Axe-core integration in development
- ARIA labels on interactive elements
- Keyboard navigation support
- Screen reader compatibility
- Color contrast compliance

### Tools
- @axe-core/react for automated testing
- Semantic HTML structure
- Focus management for modals/dialogs

## Key Dependencies

### Production
- react, react-dom: ^18.x
- @tanstack/react-query: Latest
- wouter: Latest
- @radix-ui/* components
- tailwindcss: ^3.x
- lucide-react: Icons
- date-fns: Date utilities

### Development
- vite: ^5.x
- vitest: Testing framework
- typescript: ^5.x
- @testing-library/react: Component testing
- tailwindcss-animate: Animation utilities

## Browser Support
- Modern browsers (ES2020+)
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- No IE11 support

## Mobile Responsiveness
- Tailwind breakpoints: sm, md, lg, xl, 2xl
- Collapsible sidebar for mobile
- Touch-optimized controls
- Responsive tables with horizontal scroll
- Mobile-first design approach
