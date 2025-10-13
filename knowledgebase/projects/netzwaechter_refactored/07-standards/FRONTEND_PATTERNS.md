# Frontend Patterns - Netzwächter Project Standards

Created: 2025-10-13

This document defines the **REQUIRED frontend patterns** for the Netzwächter project. All new frontend code MUST follow these patterns.

---

## Data Fetching Pattern

### Use TanStack Query for ALL Server State

**NEVER use**:
- ❌ `fetch()` directly in components
- ❌ `axios` directly in components
- ❌ `apiClient.ts` or `api-utils.ts`
- ❌ `useState` + `useEffect` for API calls

**ALWAYS use**:
- ✅ TanStack Query hooks from `src/features/shared/hooks/api/`

### Query Pattern (GET requests)

```typescript
// src/features/shared/hooks/api/useSettings.ts
import { useQuery } from '@tanstack/react-query'

export function useSettings() {
  return useQuery({
    queryKey: ['settings'],
    queryFn: async () => {
      const response = await fetch('/api/settings', {
        credentials: 'include' // Include session cookie
      })

      if (!response.ok) {
        throw new Error('Failed to fetch settings')
      }

      return response.json()
    }
  })
}

// Usage in component:
import { useSettings } from '@/features/shared/hooks/api/useSettings'

function SettingsPage() {
  const { data: settings, isLoading, error } = useSettings()

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return <div>{/* Render settings */}</div>
}
```

### Mutation Pattern (POST/PUT/DELETE)

```typescript
// src/features/shared/hooks/api/useSettings.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'

export function useUpdateSetting() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: { id: string; value: string }) => {
      const response = await fetch(`/api/settings/${data.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ value: data.value })
      })

      if (!response.ok) {
        throw new Error('Failed to update setting')
      }

      return response.json()
    },
    onSuccess: () => {
      // Invalidate and refetch settings
      queryClient.invalidateQueries({ queryKey: ['settings'] })
    }
  })
}

// Usage in component:
function SettingsForm() {
  const mutation = useUpdateSetting()

  const handleSubmit = (values: FormData) => {
    mutation.mutate({
      id: values.id,
      value: values.value
    }, {
      onSuccess: () => {
        toast.success('Setting updated!')
      },
      onError: (error) => {
        toast.error(error.message)
      }
    })
  }

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? 'Saving...' : 'Save'}
      </button>
    </form>
  )
}
```

### Advanced Query Patterns

#### Query with Parameters

```typescript
export function useSettingById(id: string) {
  return useQuery({
    queryKey: ['settings', id], // Include params in key
    queryFn: async () => {
      const response = await fetch(`/api/settings/${id}`, {
        credentials: 'include'
      })

      if (!response.ok) {
        throw new Error('Setting not found')
      }

      return response.json()
    },
    enabled: !!id // Only fetch if id exists
  })
}
```

#### Query with Dependent Data

```typescript
export function useUserSettings(userId: string) {
  // First fetch user
  const { data: user } = useUser(userId)

  // Then fetch their settings (only when user is loaded)
  return useQuery({
    queryKey: ['users', userId, 'settings'],
    queryFn: async () => {
      const response = await fetch(`/api/users/${userId}/settings`, {
        credentials: 'include'
      })
      return response.json()
    },
    enabled: !!user // Wait for user before fetching settings
  })
}
```

#### Optimistic Updates

```typescript
export function useUpdateSetting() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: UpdateSettingData) => {
      const response = await fetch(`/api/settings/${data.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(data)
      })
      return response.json()
    },
    onMutate: async (newData) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['settings'] })

      // Snapshot previous value
      const previousSettings = queryClient.getQueryData(['settings'])

      // Optimistically update to new value
      queryClient.setQueryData(['settings'], (old: any[]) =>
        old.map(s => s.id === newData.id ? { ...s, ...newData } : s)
      )

      // Return snapshot for rollback
      return { previousSettings }
    },
    onError: (err, newData, context) => {
      // Rollback on error
      queryClient.setQueryData(['settings'], context.previousSettings)
    },
    onSettled: () => {
      // Refetch to ensure sync
      queryClient.invalidateQueries({ queryKey: ['settings'] })
    }
  })
}
```

---

## Form Pattern

### Use React Hook Form + Zod for ALL Forms

**NEVER use**:
- ❌ Manual `useState` for each field
- ❌ Manual validation with if/else
- ❌ Forms without schema validation

**ALWAYS use**:
- ✅ React Hook Form + Zod schema

### Basic Form Pattern

```typescript
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

// 1. Define Zod schema
const settingFormSchema = z.object({
  key: z.string().min(1, 'Key is required'),
  value: z.string().min(1, 'Value is required'),
  description: z.string().optional()
})

type SettingFormData = z.infer<typeof settingFormSchema>

// 2. Create form component
function SettingForm() {
  const mutation = useCreateSetting()

  const form = useForm<SettingFormData>({
    resolver: zodResolver(settingFormSchema),
    defaultValues: {
      key: '',
      value: '',
      description: ''
    }
  })

  const onSubmit = (data: SettingFormData) => {
    mutation.mutate(data, {
      onSuccess: () => {
        form.reset()
        toast.success('Setting created!')
      }
    })
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="key">Key</label>
        <input
          id="key"
          {...form.register('key')}
        />
        {form.formState.errors.key && (
          <span className="text-red-500">
            {form.formState.errors.key.message}
          </span>
        )}
      </div>

      <div>
        <label htmlFor="value">Value</label>
        <input
          id="value"
          {...form.register('value')}
        />
        {form.formState.errors.value && (
          <span className="text-red-500">
            {form.formState.errors.value.message}
          </span>
        )}
      </div>

      <div>
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          {...form.register('description')}
        />
      </div>

      <button
        type="submit"
        disabled={mutation.isPending || !form.formState.isValid}
      >
        {mutation.isPending ? 'Saving...' : 'Save'}
      </button>
    </form>
  )
}
```

### Form with Custom Validation

```typescript
const userFormSchema = z.object({
  username: z.string()
    .min(3, 'Username must be at least 3 characters')
    .max(20, 'Username must be at most 20 characters')
    .regex(/^[a-zA-Z0-9_]+$/, 'Username can only contain letters, numbers, and underscores'),

  email: z.string()
    .email('Invalid email address'),

  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
    .regex(/[0-9]/, 'Password must contain at least one number'),

  confirmPassword: z.string()
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword']
})
```

### Form with Dependent Fields

```typescript
const settingFormSchema = z.object({
  key: z.string().min(1),
  isSecret: z.boolean(),
  value: z.string().min(1)
}).refine(
  data => {
    // If isSecret is true, value must be at least 16 characters
    if (data.isSecret && data.value.length < 16) {
      return false
    }
    return true
  },
  {
    message: 'Secret values must be at least 16 characters',
    path: ['value']
  }
)
```

---

## State Management Pattern

### Decision Tree

Use the **right tool** for each type of state:

```typescript
// 1. Server State (data from API) → TanStack Query
const { data: users } = useUsers()

// 2. Complex Client State (shared across many components) → Zustand
const { theme, setTheme } = useThemeStore()

// 3. Simple Local State (single component) → useState
const [isOpen, setIsOpen] = useState(false)

// 4. Shared Context (auth, user session) → React Context
const { user, isAuthenticated } = useAuth()
```

### Zustand Pattern (Complex Client State)

```typescript
// src/features/shared/store/themeStore.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface ThemeState {
  theme: 'light' | 'dark'
  setTheme: (theme: 'light' | 'dark') => void
  toggleTheme: () => void
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set) => ({
      theme: 'light',
      setTheme: (theme) => set({ theme }),
      toggleTheme: () =>
        set((state) => ({
          theme: state.theme === 'light' ? 'dark' : 'light'
        }))
    }),
    {
      name: 'theme-storage' // localStorage key
    }
  )
)

// Usage in component:
function ThemeToggle() {
  const { theme, toggleTheme } = useThemeStore()

  return (
    <button onClick={toggleTheme}>
      Current: {theme}
    </button>
  )
}
```

### React Context Pattern (Shared Context)

```typescript
// src/features/auth/context/AuthContext.tsx
import { createContext, useContext, ReactNode } from 'react'

interface AuthContextValue {
  user: User | null
  isAuthenticated: boolean
  login: (username: string, password: string) => Promise<void>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const { data: user, isLoading } = useCurrentUser()
  const loginMutation = useLogin()
  const logoutMutation = useLogout()

  const value: AuthContextValue = {
    user: user || null,
    isAuthenticated: !!user,
    login: async (username, password) => {
      await loginMutation.mutateAsync({ username, password })
    },
    logout: async () => {
      await logoutMutation.mutateAsync()
    }
  }

  if (isLoading) {
    return <div>Loading...</div>
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

// Usage:
function Header() {
  const { user, logout } = useAuth()

  return (
    <header>
      {user ? (
        <>
          <span>Welcome, {user.username}</span>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <Link to="/login">Login</Link>
      )}
    </header>
  )
}
```

---

## Component Patterns

### Component Composition

**NEVER use**:
- ❌ Large monolithic components (500+ lines)
- ❌ Props drilling through 3+ levels
- ❌ Components with multiple responsibilities

**ALWAYS use**:
- ✅ Small, focused components (< 200 lines)
- ✅ Composition over configuration
- ✅ Single responsibility principle

### Example: Good Component Composition

```typescript
// ❌ BAD: Monolithic component
function SettingsPage() {
  const { data: settings } = useSettings()
  const mutation = useUpdateSetting()
  const form = useForm()

  // 500+ lines of JSX with forms, cards, modals, etc.
  return (
    <div>
      {/* Everything in one component */}
    </div>
  )
}

// ✅ GOOD: Composed components
function SettingsPage() {
  const { data: settings, isLoading } = useSettings()

  if (isLoading) return <LoadingSpinner />

  return (
    <div className="container">
      <PageHeader title="Settings" />
      <SettingsList settings={settings} />
    </div>
  )
}

function SettingsList({ settings }: { settings: Setting[] }) {
  return (
    <div className="grid gap-4">
      {settings.map(setting => (
        <SettingCard key={setting.id} setting={setting} />
      ))}
    </div>
  )
}

function SettingCard({ setting }: { setting: Setting }) {
  const [isEditing, setIsEditing] = useState(false)

  return (
    <Card>
      <CardHeader>
        <CardTitle>{setting.key}</CardTitle>
      </CardHeader>
      <CardContent>
        {isEditing ? (
          <SettingEditForm
            setting={setting}
            onCancel={() => setIsEditing(false)}
          />
        ) : (
          <SettingDisplay
            setting={setting}
            onEdit={() => setIsEditing(true)}
          />
        )}
      </CardContent>
    </Card>
  )
}
```

### Custom Hooks Pattern

Extract complex logic into custom hooks:

```typescript
// src/features/settings/hooks/useSettingForm.ts
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useUpdateSetting } from '@/features/shared/hooks/api/useSettings'
import { settingFormSchema } from '../schemas/settingSchema'

export function useSettingForm(setting: Setting) {
  const mutation = useUpdateSetting()

  const form = useForm({
    resolver: zodResolver(settingFormSchema),
    defaultValues: {
      key: setting.key,
      value: setting.value,
      description: setting.description
    }
  })

  const onSubmit = (data: SettingFormData) => {
    mutation.mutate(
      { id: setting.id, ...data },
      {
        onSuccess: () => {
          toast.success('Setting updated!')
        },
        onError: (error) => {
          toast.error(error.message)
        }
      }
    )
  }

  return {
    form,
    onSubmit: form.handleSubmit(onSubmit),
    isSubmitting: mutation.isPending
  }
}

// Usage in component:
function SettingEditForm({ setting }: { setting: Setting }) {
  const { form, onSubmit, isSubmitting } = useSettingForm(setting)

  return (
    <form onSubmit={onSubmit}>
      {/* Form fields using form.register */}
    </form>
  )
}
```

---

## File Structure Pattern

### Feature-Based Organization

```
apps/frontend-web/src/features/
  ├── settings/
  │   ├── components/
  │   │   ├── SettingsCard.tsx
  │   │   ├── SettingEditForm.tsx
  │   │   └── SettingDisplay.tsx
  │   ├── hooks/
  │   │   └── useSettingForm.ts
  │   ├── pages/
  │   │   └── SettingsPage.tsx
  │   ├── schemas/
  │   │   └── settingSchema.ts
  │   └── types/
  │       └── settings.types.ts
  │
  ├── shared/
  │   ├── components/
  │   │   ├── ui/         # Radix UI components
  │   │   │   ├── button.tsx
  │   │   │   ├── card.tsx
  │   │   │   └── input.tsx
  │   │   └── layout/
  │   │       ├── Header.tsx
  │   │       ├── Sidebar.tsx
  │   │       └── PageLayout.tsx
  │   ├── hooks/
  │   │   └── api/        # TanStack Query hooks
  │   │       ├── useSettings.ts
  │   │       ├── useUsers.ts
  │   │       └── useAuth.ts
  │   └── store/          # Zustand stores
  │       └── themeStore.ts
```

---

## Styling Pattern

### Use Tailwind CSS Classes

**NEVER use**:
- ❌ Inline styles (`style={{ color: 'red' }}`)
- ❌ CSS modules
- ❌ Styled-components

**ALWAYS use**:
- ✅ Tailwind utility classes
- ✅ Component variants with `cva` (class-variance-authority)

### Example: Component with Tailwind

```typescript
import { cn } from '@/lib/utils'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'destructive' | 'outline'
  size?: 'sm' | 'md' | 'lg'
}

function Button({
  variant = 'default',
  size = 'md',
  className,
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        // Base styles
        'inline-flex items-center justify-center rounded-md font-medium transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
        'disabled:pointer-events-none disabled:opacity-50',

        // Variant styles
        variant === 'default' && 'bg-primary text-primary-foreground hover:bg-primary/90',
        variant === 'destructive' && 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        variant === 'outline' && 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',

        // Size styles
        size === 'sm' && 'h-9 px-3 text-sm',
        size === 'md' && 'h-10 px-4 py-2',
        size === 'lg' && 'h-11 px-8 text-lg',

        // Allow override
        className
      )}
      {...props}
    >
      {children}
    </button>
  )
}
```

---

## Accessibility Pattern

### ALWAYS Follow WCAG 2.1 AA Standards

**Required for all components**:
- ✅ Semantic HTML (`<button>` not `<div onClick>`)
- ✅ Keyboard navigation (Tab, Enter, Escape, Arrow keys)
- ✅ ARIA labels and roles
- ✅ Focus indicators
- ✅ Color contrast (4.5:1 for text)

### Example: Accessible Modal

```typescript
import * as Dialog from '@radix-ui/react-dialog'

function SettingsModal({ open, onClose }: SettingsModalProps) {
  return (
    <Dialog.Root open={open} onOpenChange={onClose}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50" />
        <Dialog.Content
          className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-lg p-6"
          aria-describedby="settings-description"
        >
          <Dialog.Title className="text-lg font-semibold">
            Settings
          </Dialog.Title>
          <Dialog.Description id="settings-description" className="text-sm text-gray-600">
            Manage your application settings
          </Dialog.Description>

          <SettingsForm />

          <Dialog.Close asChild>
            <button
              className="absolute top-4 right-4"
              aria-label="Close settings"
            >
              <XIcon />
            </button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  )
}
```

---

## Error Handling Pattern

### Always Handle Loading and Error States

```typescript
function SettingsPage() {
  const { data: settings, isLoading, error } = useSettings()

  // Loading state
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <LoadingSpinner />
      </div>
    )
  }

  // Error state
  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <ErrorMessage
          title="Failed to load settings"
          message={error.message}
          onRetry={() => queryClient.invalidateQueries(['settings'])}
        />
      </div>
    )
  }

  // Empty state
  if (!settings || settings.length === 0) {
    return (
      <EmptyState
        title="No settings found"
        description="Create your first setting to get started"
        action={<Button>Create Setting</Button>}
      />
    )
  }

  // Success state
  return <SettingsList settings={settings} />
}
```

---

## Quick Reference

### Data Fetching Decision Tree

```
Need data from API?
├─ Read data (GET) → useQuery
├─ Write data (POST/PUT/DELETE) → useMutation
└─ Real-time data → useQuery with refetchInterval
```

### State Management Decision Tree

```
What type of state?
├─ Server data (API) → TanStack Query
├─ Complex client state (global) → Zustand
├─ Simple local state → useState
├─ Shared context (auth, theme) → React Context
└─ URL state (filters, pagination) → React Router + URLSearchParams
```

### Form Validation Decision Tree

```
Need form validation?
├─ Simple validation → React Hook Form + Zod
├─ Complex cross-field validation → Zod .refine()
├─ Async validation (check username) → Zod .superRefine()
└─ No form → Don't validate manually, always use Zod
```

---

Created: 2025-10-13
Last Updated: 2025-10-13
Status: Active - Required for all new frontend code
Reference: See `LEGACY_PATTERNS_TO_AVOID.md` for anti-patterns
