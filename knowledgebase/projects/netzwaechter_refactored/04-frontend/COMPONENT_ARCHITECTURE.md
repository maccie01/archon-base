# Component Architecture Patterns

**Created:** 2025-10-13
**Last Updated:** 2025-10-13

## Overview
Netzwächter uses a feature-based architecture with shared components. This document describes the patterns, organization, and component composition strategies used throughout the application.

## Directory Structure

### Feature-Based Organization
```
src/
├── features/
│   ├── admin-dashboard/
│   │   ├── api/              # API client functions
│   │   ├── components/       # Feature components
│   │   ├── pages/           # Route components
│   │   └── types/           # TypeScript types
│   │
│   ├── auth/
│   │   ├── api/
│   │   ├── components/
│   │   │   ├── LoginModal.tsx
│   │   │   └── SessionWarning.tsx
│   │   ├── hooks/
│   │   │   └── useAuth.ts
│   │   ├── pages/
│   │   │   ├── Login.tsx
│   │   │   ├── LoginStrawa.tsx
│   │   │   ├── LayoutStrawa.tsx
│   │   │   └── SuperadminLogin.tsx
│   │   └── types/
│   │
│   ├── energy/
│   │   ├── api/
│   │   ├── components/
│   │   │   ├── shared/      # Shared within feature
│   │   │   ├── KI_energy.tsx
│   │   │   ├── KI_energy_jahr.tsx
│   │   │   └── EfficiencyDistributionCard.tsx
│   │   ├── pages/
│   │   │   ├── EnergyData.tsx
│   │   │   ├── EfficiencyAnalysis.tsx
│   │   │   └── DbEnergyDataConfig.tsx
│   │   └── types/
│   │
│   ├── ki-reports/
│   ├── logbook/
│   ├── monitoring/
│   ├── objects/
│   ├── settings/
│   ├── temperature/
│   └── users/
│
├── components/           # Shared components
│   ├── ui/              # shadcn/ui components
│   ├── Layout.tsx
│   ├── DatabaseStatusHeader.tsx
│   ├── ExportDialog.tsx
│   └── SystemSchemaView.tsx
│
├── hooks/               # Shared hooks
│   ├── use-toast.ts
│   └── useUIMode.ts
│
└── lib/                 # Utilities
    ├── queryClient.ts
    └── utils.ts
```

## Component Patterns

### 1. Page Components
**Location**: `features/*/pages/`
**Purpose**: Route-level components that compose features
**Pattern**:

```tsx
// features/monitoring/pages/Dashboard.tsx
export default function Dashboard() {
  // 1. Hooks
  const { user } = useAuth();
  const [filters, setFilters] = useState(...);

  // 2. Data fetching
  const { data: kpis, isLoading } = useQuery({
    queryKey: ['/api/dashboard/kpis'],
  });

  // 3. Computed values
  const filteredData = useMemo(() => {
    return processData(data, filters);
  }, [data, filters]);

  // 4. Event handlers
  const handleFilterChange = (filter) => {
    setFilters(filter);
  };

  // 5. Render
  return (
    <div className="p-6">
      <KPICards data={kpis} />
      <DataTable data={filteredData} />
    </div>
  );
}
```

**Characteristics**:
- Default exports
- Handle routing logic
- Compose feature components
- Manage page-level state
- Coordinate data fetching
- Usually 200-900 lines (too large)

---

### 2. Feature Components
**Location**: `features/*/components/`
**Purpose**: Feature-specific reusable components
**Pattern**:

```tsx
// features/logbook/components/LogbookTaskForm.tsx
interface LogbookTaskFormProps {
  task?: Task;
  onSubmit: (data: TaskFormData) => void;
  onCancel: () => void;
}

export function LogbookTaskForm({ task, onSubmit, onCancel }: Props) {
  const form = useForm<TaskFormData>({
    defaultValues: task || defaultValues,
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        {/* Form fields */}
        <DialogFooter>
          <Button variant="outline" onClick={onCancel}>Cancel</Button>
          <Button type="submit">Save</Button>
        </DialogFooter>
      </form>
    </Form>
  );
}
```

**Characteristics**:
- Named exports
- TypeScript interfaces for props
- Focused on single responsibility
- Reusable within feature
- Usually 50-200 lines

---

### 3. Shared Components
**Location**: `components/`
**Purpose**: Components used across multiple features
**Examples**:

#### Layout Components
```tsx
// components/Layout.tsx
export function Layout({ children }: { children: ReactNode }) {
  // Sidebar + header + content wrapper
  // Used by: All cockpit mode routes
}

// features/auth/pages/LayoutStrawa.tsx
export default function LayoutStrawaTabs() {
  // Alternative layout for Strawa mode
  // Used by: All non-cockpit routes
}
```

#### Utility Components
```tsx
// components/ExportDialog.tsx
interface ExportDialogProps {
  data: any[];
  filename: string;
  title: string;
  userEmail?: string;
  filterInfo?: FilterInfo;
}

export default function ExportDialog(props: ExportDialogProps) {
  // Handles CSV/Excel export with email delivery
  // Used by: Dashboard, TemperatureAnalysis, Logbook
}

// components/DatabaseStatusHeader.tsx
export default function DatabaseStatusHeader() {
  // Shows current database connection
  // Used by: All authenticated routes
}
```

---

### 4. UI Components (shadcn/ui)
**Location**: `components/ui/`
**Purpose**: Base UI building blocks
**Pattern**: See UI_COMPONENT_INVENTORY.md

**Usage Pattern**:
```tsx
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Dialog, DialogContent, DialogHeader } from "@/components/ui/dialog";

// Use in any component
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>
    <Button>Action</Button>
  </CardContent>
</Card>
```

---

## Composition Patterns

### 1. Card Composition
**Pattern**: Nest related content in cards

```tsx
<Card>
  <CardHeader>
    <div className="flex items-center justify-between">
      <CardTitle>Portfolio Objekte</CardTitle>
      <div className="flex items-center space-x-3">
        <ExportDialog {...} />
        <Input placeholder="Search..." />
        <Select>...</Select>
      </div>
    </div>
  </CardHeader>
  <CardContent>
    <Table>...</Table>
  </CardContent>
</Card>
```

**Used In**: Dashboard, UserManagement, Settings, Logbook

---

### 2. Tab Composition
**Pattern**: Organize related views in tabs

```tsx
<Card>
  <CardHeader className="p-0">
    <Tabs defaultValue="users">
      <TabsList>
        <TabsTrigger value="users">
          <UsersIcon className="h-4 w-4 mr-2" />
          Benutzer
        </TabsTrigger>
        <TabsTrigger value="mandates">
          <ShieldCheckIcon className="h-4 w-4 mr-2" />
          Mandanten
        </TabsTrigger>
      </TabsList>

      <TabsContent value="users">
        <UserTable />
      </TabsContent>
      <TabsContent value="mandates">
        <MandateTable />
      </TabsContent>
    </Tabs>
  </CardHeader>
</Card>
```

**Used In**: UserManagement, Logbook

---

### 3. Form Composition
**Pattern**: Dialog + Form + Fields

```tsx
<Dialog open={open} onOpenChange={setOpen}>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Create User</DialogTitle>
      <DialogDescription>Enter user details</DialogDescription>
    </DialogHeader>

    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <div className="space-y-4">
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <Input type="email" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          {/* More fields */}
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={close}>Cancel</Button>
          <Button type="submit">Save</Button>
        </DialogFooter>
      </form>
    </Form>
  </DialogContent>
</Dialog>
```

**Used In**: UserForm, MandateForm, ObjectGroupForm, ProfileForm, LogbookTaskForm

---

### 4. Table Composition
**Pattern**: Card + Filters + Table

```tsx
<Card>
  <CardHeader>
    <div className="flex items-center justify-between">
      <CardTitle>Data Table</CardTitle>
      <div className="flex space-x-3">
        <Input placeholder="Search..." />
        <Select>...</Select>
        <Button>Add New</Button>
      </div>
    </div>
  </CardHeader>

  <CardContent>
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Column 1</TableHead>
          <TableHead>Column 2</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {data.map(item => (
          <TableRow key={item.id}>
            <TableCell>{item.name}</TableCell>
            <TableCell>{item.value}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </CardContent>
</Card>
```

**Used In**: UserTable, MandateTable, ObjectGroupTable, ProfileTable, LogbookTables

---

## State Management Patterns

### 1. Server State (TanStack Query)
**Pattern**: Query hooks for data fetching

```tsx
// Custom query hook
export function useUsers() {
  return useQuery({
    queryKey: ['/api/users'],
    staleTime: 5 * 60 * 1000,
  });
}

// Usage in component
function UserManagement() {
  const { data: users, isLoading, error } = useUsers();

  if (isLoading) return <LoadingState />;
  if (error) return <ErrorState />;

  return <UserTable users={users} />;
}
```

**Examples**:
- `features/users/hooks/useUserData.ts`: useUsers, useUserProfiles, useMandants
- `features/settings/hooks/useSettingsQueries.ts`: useSettings, useThresholds
- `features/logbook/hooks/useLogbookQueries.ts`: useTasks, useEntries

---

### 2. Mutation Pattern
**Pattern**: Mutation hooks for data updates

```tsx
// Custom mutation hook
export function useCreateUser() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (data: UserFormData) =>
      apiRequest('POST', '/api/users', data),
    onSuccess: () => {
      queryClient.invalidateQueries(['/api/users']);
      toast({ title: 'User created successfully' });
    },
    onError: (error) => {
      toast({
        title: 'Error',
        description: error.message,
        variant: 'destructive',
      });
    },
  });
}

// Usage
function UserForm() {
  const createUser = useCreateUser();

  const onSubmit = (data: UserFormData) => {
    createUser.mutate(data);
  };

  return <Form onSubmit={onSubmit}>...</Form>;
}
```

**Examples**:
- `features/users/hooks/useUserMutations.ts`
- `features/settings/hooks/useSettingsMutations.ts`
- `features/logbook/hooks/useLogbookMutations.ts`

---

### 3. Local State Pattern
**Pattern**: useState for component-level state

```tsx
function Dashboard() {
  // Simple state
  const [searchTerm, setSearchTerm] = useState("");
  const [filter, setFilter] = useState("all");

  // Complex state
  const [sortConfig, setSortConfig] = useState<SortConfig | null>(null);

  // Derived state
  const filteredData = useMemo(() => {
    return data
      .filter(item => item.name.includes(searchTerm))
      .filter(item => filter === "all" || item.type === filter);
  }, [data, searchTerm, filter]);

  return <DataTable data={filteredData} />;
}
```

**Used For**:
- Form state (react-hook-form handles internally)
- UI state (modals, filters, sort)
- Temporary state (search, selections)

---

### 4. Global State Pattern
**Pattern**: Context + hooks for cross-cutting concerns

```tsx
// hooks/useAuth.ts
export function useAuth() {
  const { data: user, isLoading } = useQuery({
    queryKey: ['/api/auth/me'],
    retry: false,
  });

  return {
    user,
    isLoading,
    isAuthenticated: !!user,
    isSuperadmin: user?.role === 'superadmin',
  };
}

// hooks/useUIMode.ts
export function useUIMode() {
  const [location] = useLocation();
  const searchParams = new URLSearchParams(location.split('?')[1]);

  return {
    shouldUseStrawa: searchParams.get('ui') !== 'cockpit',
  };
}

// Usage: Available in any component
const { user, isAuthenticated } = useAuth();
const { shouldUseStrawa } = useUIMode();
```

---

## Data Fetching Patterns

### 1. API Client Pattern
**Location**: `lib/queryClient.ts`

```tsx
export const apiRequest = async (
  method: string,
  url: string,
  data?: any
) => {
  const response = await fetch(url, {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
    body: data ? JSON.stringify(data) : undefined,
  });

  if (!response.ok) {
    throw new Error('Request failed');
  }

  return response.json();
};
```

---

### 2. Feature API Pattern
**Location**: `features/*/api/`

```tsx
// features/users/api/usersApi.ts
export const usersApi = {
  getUsers: () => apiRequest('GET', '/api/users'),

  createUser: (data: UserFormData) =>
    apiRequest('POST', '/api/users', data),

  updateUser: (id: number, data: UserFormData) =>
    apiRequest('PUT', `/api/users/${id}`, data),

  deleteUser: (id: number) =>
    apiRequest('DELETE', `/api/users/${id}`),
};
```

---

### 3. Query Hook Pattern
**Location**: `features/*/hooks/`

```tsx
// features/users/hooks/useUserData.ts
export function useUsers() {
  return useQuery({
    queryKey: ['/api/users'],
    staleTime: 5 * 60 * 1000,
    gcTime: 10 * 60 * 1000,
  });
}

export function useUserProfiles() {
  return useQuery({
    queryKey: ['/api/users/profiles'],
    staleTime: 10 * 60 * 1000,
  });
}
```

---

## Component Communication Patterns

### 1. Props Down
**Pattern**: Parent passes data to children

```tsx
function ParentComponent() {
  const { data } = useQuery(['/api/data']);

  return (
    <ChildComponent
      data={data}
      onAction={handleAction}
    />
  );
}

function ChildComponent({ data, onAction }: Props) {
  return <Button onClick={onAction}>{data.label}</Button>;
}
```

---

### 2. Events Up
**Pattern**: Children emit events, parents handle

```tsx
function ParentComponent() {
  const handleSubmit = (formData: FormData) => {
    // Handle submission
    mutation.mutate(formData);
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent>
        <ChildForm onSubmit={handleSubmit} />
      </DialogContent>
    </Dialog>
  );
}

function ChildForm({ onSubmit }: Props) {
  return (
    <Form>
      <Button onClick={() => onSubmit(data)}>
        Submit
      </Button>
    </Form>
  );
}
```

---

### 3. Query Invalidation
**Pattern**: Components trigger refetch via invalidation

```tsx
function UserForm() {
  const queryClient = useQueryClient();

  const createUser = useMutation({
    mutationFn: (data) => apiRequest('POST', '/api/users', data),
    onSuccess: () => {
      // Invalidate users list
      queryClient.invalidateQueries(['/api/users']);

      // Close form
      onClose();

      // Show toast
      toast({ title: 'User created' });
    },
  });
}

// UserTable automatically refetches when invalidated
function UserTable() {
  const { data: users } = useQuery(['/api/users']);
  return <Table data={users} />;
}
```

---

## Styling Patterns

### 1. Utility-First (Tailwind)
**Pattern**: Compose styles with utility classes

```tsx
<div className="flex items-center space-x-4 p-6">
  <Avatar className="h-12 w-12" />
  <div className="flex-1">
    <h3 className="text-lg font-semibold">Title</h3>
    <p className="text-sm text-muted-foreground">Description</p>
  </div>
  <Button variant="outline" size="sm">Action</Button>
</div>
```

**Pros**:
- Fast to write
- No context switching
- Easy to understand
- Consistent spacing

**Cons**:
- Long className strings
- Repetitive patterns
- Hard to extract patterns

---

### 2. Component Variants (CVA)
**Pattern**: shadcn/ui uses class-variance-authority

```tsx
// components/ui/button.tsx
const buttonVariants = cva(
  "inline-flex items-center justify-center...", // base
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground...",
        destructive: "bg-destructive text-destructive-foreground...",
        outline: "border border-input...",
        // ...
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 px-3",
        lg: "h-11 px-8",
        // ...
      },
    },
  }
);
```

**Usage**:
```tsx
<Button variant="outline" size="sm">Click</Button>
```

---

### 3. CSS Modules (Not Used)
**Pattern**: NOT currently used in the project
**Alternative**: Tailwind + CSS custom properties

---

### 4. Global CSS (index.css)
**Pattern**: Global styles for special cases
**Issues**: See UI_INCONSISTENCIES.md

```css
/* Custom animations */
@keyframes pulse-red { ... }

/* Feature-specific styles */
.temp-analysis-table { ... }
.grafana-container { ... }

/* Theme colors */
:root { --primary: ...; }
```

**When to Use**:
- CSS animations
- Theme variables
- Print styles
- Global resets

**When NOT to Use**:
- Component-specific styles
- Feature styles
- Layout styles

---

## Testing Patterns

### 1. Component Tests
**Pattern**: Test user interactions

```tsx
// components/ui/__tests__/button.test.tsx
describe('Button', () => {
  it('renders with correct variant', () => {
    render(<Button variant="destructive">Delete</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('bg-destructive');
  });

  it('handles click events', async () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);

    await userEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledOnce();
  });
});
```

---

### 2. Hook Tests
**Pattern**: Test custom hooks

```tsx
// hooks/__tests__/useAuth.test.ts
describe('useAuth', () => {
  it('returns user data when authenticated', async () => {
    const { result } = renderHook(() => useAuth());

    await waitFor(() => {
      expect(result.current.isAuthenticated).toBe(true);
      expect(result.current.user).toBeDefined();
    });
  });
});
```

---

### 3. Integration Tests
**Pattern**: Test feature workflows

```tsx
// features/logbook/__tests__/LogbookTaskForm.test.tsx
describe('LogbookTaskForm', () => {
  it('creates new task', async () => {
    render(<LogbookTaskForm onSubmit={handleSubmit} />);

    await userEvent.type(
      screen.getByLabelText('Title'),
      'New Task'
    );
    await userEvent.click(screen.getByRole('button', { name: 'Save' }));

    expect(handleSubmit).toHaveBeenCalledWith(
      expect.objectContaining({ title: 'New Task' })
    );
  });
});
```

---

## Performance Patterns

### 1. React Query Caching
```tsx
const { data } = useQuery({
  queryKey: ['/api/data'],
  staleTime: 5 * 60 * 1000,  // 5 minutes
  gcTime: 10 * 60 * 1000,    // 10 minutes
});
```

### 2. Memoization
```tsx
const filteredData = useMemo(() => {
  return data.filter(item => item.active);
}, [data]);

const handleClick = useCallback(() => {
  // ...
}, [dependency]);
```

### 3. Lazy Loading (Future)
```tsx
const HeavyComponent = lazy(() => import('./HeavyComponent'));

<Suspense fallback={<Loading />}>
  <HeavyComponent />
</Suspense>
```

---

## Component Naming Conventions

### File Names
- **Pages**: PascalCase (Dashboard.tsx, UserManagement.tsx)
- **Components**: PascalCase (UserTable.tsx, LogbookTaskForm.tsx)
- **Hooks**: camelCase (useAuth.ts, useUserData.ts)
- **Utils**: camelCase (utils.ts, authUtils.ts)
- **Types**: PascalCase or camelCase.types.ts

### Component Names
- **Pages**: Default export, PascalCase
  ```tsx
  export default function Dashboard() { }
  ```

- **Feature Components**: Named export, PascalCase
  ```tsx
  export function UserTable(props: UserTableProps) { }
  ```

- **UI Components**: Named export, PascalCase
  ```tsx
  export function Button({ variant, ...props }: ButtonProps) { }
  ```

### Props Types
```tsx
interface ComponentNameProps {
  // Required props first
  data: Data[];
  onSubmit: (data: FormData) => void;

  // Optional props second
  className?: string;
  disabled?: boolean;
}
```

---

## Anti-Patterns to Avoid

### 1. Inline Styles
**BAD**:
```tsx
<div style={{ color: '#1e40af', padding: '10px' }}>
```

**GOOD**:
```tsx
<div className="text-blue-600 p-[10px]">
```

---

### 2. Inline CSS in Components
**BAD**:
```tsx
function Component() {
  return (
    <>
      <style>{`
        .custom-class {
          background: red !important;
        }
      `}</style>
      <div className="custom-class">...</div>
    </>
  );
}
```

**GOOD**:
```tsx
function Component() {
  return (
    <div className="bg-red-500">...</div>
  );
}
```

---

### 3. Prop Drilling
**BAD**:
```tsx
<Parent>
  <Child1 data={data}>
    <Child2 data={data}>
      <Child3 data={data}>
        <Child4 data={data} />
      </Child3>
    </Child2>
  </Child1>
</Parent>
```

**GOOD**:
```tsx
// Use query hooks at leaf components
function Child4() {
  const { data } = useQuery(['/api/data']);
  return <div>{data}</div>;
}
```

---

## Best Practices

### 1. Component Size
- **Pages**: 200-500 lines max (extract when larger)
- **Feature Components**: 50-200 lines
- **UI Components**: 50-150 lines
- Extract when component does too much

### 2. Props Interface
- Always define TypeScript interface
- Document complex props
- Use semantic prop names
- Group related props

### 3. State Management
- Use React Query for server state
- Use useState for UI state
- Use useMemo for expensive computations
- Use useCallback for event handlers

### 4. Error Handling
- Use error boundaries
- Handle query errors
- Show user-friendly messages
- Log errors for debugging

### 5. Accessibility
- Use semantic HTML
- Add ARIA labels
- Support keyboard navigation
- Test with screen readers

### 6. Testing
- Test user interactions
- Test error states
- Test loading states
- Test edge cases

---

## Recommended Refactorings

### 1. Extract Shared Table Component
Currently have 3 different table implementations. Create unified:
```tsx
<DataTable
  data={data}
  columns={columns}
  sortable
  filterable
  paginated
/>
```

### 2. Extract Form Components
Many forms repeat same patterns. Create:
```tsx
<FormDialog
  title="Create User"
  fields={userFields}
  onSubmit={handleSubmit}
/>
```

### 3. Extract Card Patterns
Standardize card layouts:
```tsx
<DataCard
  title="Portfolio Objects"
  actions={<ExportButton />}
  filters={<TableFilters />}
>
  <Table />
</DataCard>
```

### 4. Consolidate Tab Styling
Create unified tab component:
```tsx
<StyledTabs
  variant="strawa" // or "default"
  tabs={[
    { label: 'Users', icon: UsersIcon, content: <Users /> },
    { label: 'Profiles', icon: Settings, content: <Profiles /> },
  ]}
/>
```

---

## Summary

### Strengths
- Clear feature-based organization
- Good use of TypeScript
- Consistent query hooks pattern
- shadcn/ui provides solid foundation

### Weaknesses
- Too much duplication (tables, tabs, forms)
- Inconsistent component patterns
- Large page components (need extraction)
- Global CSS instead of components
- Inline styles in some places

### Next Steps
1. Extract shared patterns into components
2. Consolidate duplicate implementations
3. Create component library documentation
4. Establish component guidelines
5. Refactor large page components
