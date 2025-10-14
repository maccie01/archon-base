# React State Management Patterns

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Web Research (TanStack Query docs, Zustand docs, Medium, TkDodo's blog)

## Overview

State management in React has evolved significantly. This document covers when to use different state management solutions: Context API, TanStack Query, Zustand, and when to use each.

## Core Principles

1. **Separate Server and Client State**: Different tools for different state types
2. **Colocate State**: Keep state as close to where it's used as possible
3. **Lift State Up**: Only when multiple components need shared state
4. **Avoid Global State Overuse**: Not everything needs to be global
5. **Choose the Right Tool**: Match the tool to the state type

## State Types

### 1. Server State (Remote Data)
- Data fetched from APIs
- Cached data
- Synchronized with backend
- Best tool: **TanStack Query** (React Query)

### 2. Client State (UI State)
- Form inputs
- UI toggles (modals, dropdowns)
- Local preferences
- Best tools: **useState**, **useReducer**, **Zustand** (for global)

### 3. URL State
- Current route
- Query parameters
- Route params
- Best tool: **React Router** or **Wouter**

### 4. Shared State
- State needed by multiple unrelated components
- Theme, language, auth status
- Best tools: **Context API**, **Zustand**

## When to Use Each Solution

### Use Context API When:
- Simple dependency injection
- Theme or locale settings
- Auth status (with server state from TanStack Query)
- Small to medium apps with minimal state needs
- State updates are infrequent

### Use TanStack Query When:
- Fetching data from APIs
- Caching server responses
- Background data synchronization
- Optimistic updates
- Pagination, infinite scroll
- Mutations with automatic cache updates

### Use Zustand When:
- Complex client-side state
- Global state across many components
- State that changes frequently
- Need devtools integration
- Want minimal boilerplate

### Use useState/useReducer When:
- Local component state
- State only used in one component or its children
- Simple state transitions

## Patterns

### Pattern 1: Context API for Dependency Injection

**When to use**: For passing down configuration or rarely changing values

**How to implement**: Create context, provider, and custom hook

**Example skeleton**:
```typescript
// TODO: Add example code
// Define context
interface ThemeContextType {
  theme: 'light' | 'dark'
  toggleTheme: () => void
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

// Provider component
export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light')

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

// Custom hook for consuming context
export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}

// Usage:
const Component = () => {
  const { theme, toggleTheme } = useTheme()
  return <button onClick={toggleTheme}>{theme}</button>
}
```

**References**:
- [React Docs - Context](https://react.dev/reference/react/useContext)

### Pattern 2: TanStack Query for Server State

**When to use**: For all API data fetching and caching

**How to implement**: Use useQuery for reads, useMutation for writes

**Example skeleton**:
```typescript
// TODO: Add example code
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

// Queries (GET requests)
const UsersList = () => {
  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const response = await fetch('/api/users')
      return response.json()
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 30 * 60 * 1000,   // 30 minutes (formerly cacheTime)
  })

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return <ul>{data.map(user => <li key={user.id}>{user.name}</li>)}</ul>
}

// Mutations (POST/PUT/DELETE requests)
const CreateUser = () => {
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: async (newUser: User) => {
      const response = await fetch('/api/users', {
        method: 'POST',
        body: JSON.stringify(newUser),
      })
      return response.json()
    },
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })

  return (
    <button onClick={() => mutation.mutate({ name: 'New User' })}>
      Create User
    </button>
  )
}
```

**Key Features**:
- Automatic caching and background refetching
- Stale-while-revalidate strategy
- Request deduplication
- Optimistic updates
- Pagination and infinite scroll support

**References**:
- [TanStack Query Docs](https://tanstack.com/query/latest)
- [TkDodo's Blog - React Query Tips](https://tkdodo.eu/blog/practical-react-query)

### Pattern 3: Zustand for Client State

**When to use**: For complex global client state that changes frequently

**How to implement**: Create store with create function

**Example skeleton**:
```typescript
// TODO: Add example code
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

interface BearStore {
  bears: number
  increase: () => void
  decrease: () => void
}

// Basic store
const useBearStore = create<BearStore>((set) => ({
  bears: 0,
  increase: () => set((state) => ({ bears: state.bears + 1 })),
  decrease: () => set((state) => ({ bears: state.bears - 1 })),
}))

// With devtools and persistence
const useBearStore = create<BearStore>()(
  devtools(
    persist(
      (set) => ({
        bears: 0,
        increase: () => set((state) => ({ bears: state.bears + 1 })),
        decrease: () => set((state) => ({ bears: state.bears - 1 })),
      }),
      { name: 'bear-storage' }
    )
  )
)

// Usage:
const Component = () => {
  const bears = useBearStore((state) => state.bears)
  const increase = useBearStore((state) => state.increase)

  return (
    <>
      <p>Bears: {bears}</p>
      <button onClick={increase}>Add Bear</button>
    </>
  )
}

// Selecting nested state to prevent unnecessary re-renders
const Component = () => {
  const bearCount = useBearStore((state) => state.bears)
  // Component only re-renders when bears count changes
}
```

**Key Features**:
- Minimal boilerplate
- No providers needed
- Built-in devtools support
- Middleware for persistence, immer, etc.
- Excellent TypeScript support

**References**:
- [Zustand GitHub](https://github.com/pmndrs/zustand)
- [Zustand Documentation](https://docs.pmnd.rs/zustand)

### Pattern 4: Combining TanStack Query + Zustand

**When to use**: TanStack Query for server state, Zustand for complex client state

**How to implement**: Use both libraries for their strengths

**Example skeleton**:
```typescript
// TODO: Add example code
// Zustand store for UI state
const useUIStore = create<UIStore>((set) => ({
  sidebarOpen: true,
  theme: 'light',
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setTheme: (theme) => set({ theme }),
}))

// TanStack Query for server state
const UserDashboard = () => {
  // Server state from React Query
  const { data: users } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  })

  // Client state from Zustand
  const sidebarOpen = useUIStore((state) => state.sidebarOpen)
  const toggleSidebar = useUIStore((state) => state.toggleSidebar)

  return (
    <div>
      <Sidebar isOpen={sidebarOpen} onToggle={toggleSidebar} />
      <UserList users={users} />
    </div>
  )
}
```

**This is the recommended modern approach**:
- TanStack Query handles ALL server/async state
- Zustand handles complex client state
- Context API for simple dependency injection

**References**:
- [Zustand + React Query Pattern](https://tkdodo.eu/blog/zustand-and-react-context)
- [Modern State Management](https://medium.com/@freeyeon96/zustand-react-query-new-state-management-7aad6090af56)

### Pattern 5: Context + TanStack Query for Auth

**When to use**: For authentication state that combines server and client concerns

**Example skeleton**:
```typescript
// TODO: Add example code
interface AuthContextType {
  user: User | null
  isLoading: boolean
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const queryClient = useQueryClient()

  // Server state from React Query
  const { data: user, isLoading } = useQuery({
    queryKey: ['auth', 'me'],
    queryFn: async () => {
      const response = await fetch('/api/auth/me')
      if (!response.ok) return null
      return response.json()
    },
    retry: false,
    staleTime: 5 * 60 * 1000,
  })

  const logout = async () => {
    await fetch('/api/auth/logout', { method: 'POST' })
    queryClient.clear()
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
```

## State Management Decision Tree

```
Is it server data (from API)?
├─ YES → Use TanStack Query
└─ NO → Is it global client state?
    ├─ YES → Is it complex with many actions?
    │   ├─ YES → Use Zustand
    │   └─ NO → Use Context API
    └─ NO → Use useState/useReducer
```

## Common Mistakes

1. **Using Context for Everything**: Context causes all consumers to re-render
2. **Not Separating Server and Client State**: Mixing API data with UI state
3. **Redux for Everything**: Modern React doesn't need Redux for most cases
4. **Prop Drilling Instead of Context**: Passing props through 5+ components
5. **Global State for Local State**: Making everything global when it's only used locally
6. **Not Using TanStack Query**: Rolling your own data fetching when TanStack Query solves it

## Migration Strategies

### From Redux to Modern Stack

1. **Server State**: Move to TanStack Query
2. **Simple Client State**: Move to Context API
3. **Complex Client State**: Move to Zustand
4. **Result**: Significantly less boilerplate

### When Redux Still Makes Sense

- Very large applications with complex state
- Teams already invested in Redux
- Need for Redux DevTools time-travel debugging
- Existing Redux middleware/tooling

## Tools and Libraries

### Server State
- **TanStack Query** (React Query): Industry standard for server state

### Client State
- **Zustand**: Minimal, fast, scalable
- **Jotai**: Atomic state management
- **Valtio**: Proxy-based state management
- **Redux Toolkit**: Modernized Redux (if you need Redux)

### Context Enhancement
- **use-context-selector**: Prevent unnecessary re-renders

## Additional Resources

- [TanStack Query Documentation](https://tanstack.com/query/latest)
- [Zustand Documentation](https://docs.pmnd.rs/zustand)
- [TkDodo - React Query Blog Series](https://tkdodo.eu/blog/practical-react-query)
- [State Management Comparison 2024](https://results.stateofreactnative.com/en-US/state-management/)
- [Does TanStack Query Replace Redux?](https://tanstack.com/query/v4/docs/framework/react/guides/does-this-replace-client-state)

## Next Steps

- Review [HOOKS_PATTERNS.md](./HOOKS_PATTERNS.md) for useState/useReducer patterns
- See [PERFORMANCE.md](./PERFORMANCE.md) for optimization with memoization
- Check [TYPESCRIPT_REACT.md](./TYPESCRIPT_REACT.md) for typing state
