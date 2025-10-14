# React Component Patterns

Created: 2025-10-13
Last Research: 2025-10-13
Sources: React Official Docs, Web Research (UXPin, Telerik, Medium)

## Overview

Component patterns are the building blocks of React applications. This document covers composition strategies, prop patterns, and component architecture approaches for building maintainable, reusable components.

## Core Principles

1. **Composition over Inheritance**: Build complex components from simpler ones
2. **Single Responsibility**: Each component should do one thing well
3. **Prop Drilling Avoidance**: Use composition, Context, or state management to avoid deep prop chains
4. **Separation of Concerns**: Separate presentation from business logic
5. **Reusability**: Design components to be used in multiple contexts

## Patterns

### Pattern 1: Container/Presentational Pattern

**When to use**: To separate data fetching/business logic from UI rendering

**How to implement**: Split components into "smart" containers and "dumb" presentational components

**Example skeleton**:
```typescript
// TODO: Add example code
// Container (smart component with logic)
const UserListContainer = () => {
  const { data: users, isLoading } = useQuery('/api/users')

  if (isLoading) return <LoadingSpinner />

  return <UserList users={users} />
}

// Presentational (dumb component, just UI)
interface UserListProps {
  users: User[]
}

const UserList: React.FC<UserListProps> = ({ users }) => (
  <ul>
    {users.map(user => (
      <li key={user.id}>{user.name}</li>
    ))}
  </ul>
)
```

**References**:
- [Medium - Presentational vs Container Components](https://medium.com/@dan_abramov/smart-and-dumb-components-7ca2f9a7c7d0)

### Pattern 2: Compound Components Pattern

**When to use**: When components work together and share implicit state

**How to implement**: Use Context to share state between parent and children

**Example skeleton**:
```typescript
// TODO: Add example code
// Parent component with context
const TabsContext = createContext(null)

const Tabs = ({ children, defaultValue }) => {
  const [activeTab, setActiveTab] = useState(defaultValue)

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  )
}

// Child components consume context
const TabList = ({ children }) => <div className="tab-list">{children}</div>
const TabTrigger = ({ value, children }) => {
  const { activeTab, setActiveTab } = useContext(TabsContext)
  return (
    <button
      className={activeTab === value ? 'active' : ''}
      onClick={() => setActiveTab(value)}
    >
      {children}
    </button>
  )
}

// Usage:
<Tabs defaultValue="tab1">
  <TabList>
    <TabTrigger value="tab1">Tab 1</TabTrigger>
    <TabTrigger value="tab2">Tab 2</TabTrigger>
  </TabList>
</Tabs>
```

**References**:
- [Kent C. Dodds - Compound Components](https://kentcdodds.com/blog/compound-components-with-react-hooks)

### Pattern 3: Render Props Pattern

**When to use**: To share code between components using a prop whose value is a function

**How to implement**: Pass a function as a prop that returns React elements

**Example skeleton**:
```typescript
// TODO: Add example code
interface MouseTrackerProps {
  render: (position: { x: number, y: number }) => React.ReactNode
}

const MouseTracker: React.FC<MouseTrackerProps> = ({ render }) => {
  const [position, setPosition] = useState({ x: 0, y: 0 })

  const handleMouseMove = (e: MouseEvent) => {
    setPosition({ x: e.clientX, y: e.clientY })
  }

  useEffect(() => {
    window.addEventListener('mousemove', handleMouseMove)
    return () => window.removeEventListener('mousemove', handleMouseMove)
  }, [])

  return <>{render(position)}</>
}

// Usage:
<MouseTracker render={({ x, y }) => <div>Mouse at {x}, {y}</div>} />
```

**References**:
- [React Docs - Render Props](https://legacy.reactjs.org/docs/render-props.html)

### Pattern 4: Higher-Order Components (HOC)

**When to use**: To reuse component logic (Note: Custom hooks are often preferred in modern React)

**How to implement**: Function that takes a component and returns a new component

**Example skeleton**:
```typescript
// TODO: Add example code
// HOC that adds loading state
function withLoading<P extends object>(
  Component: React.ComponentType<P>
) {
  return function WithLoadingComponent(props: P & { isLoading: boolean }) {
    const { isLoading, ...restProps } = props

    if (isLoading) return <LoadingSpinner />

    return <Component {...(restProps as P)} />
  }
}

// Usage:
const UserListWithLoading = withLoading(UserList)
<UserListWithLoading users={users} isLoading={isLoading} />
```

**References**:
- [React Docs - Higher-Order Components](https://legacy.reactjs.org/docs/higher-order-components.html)
- Note: Modern React prefers custom hooks over HOCs

### Pattern 5: Children as Function Pattern

**When to use**: Similar to render props but using children prop

**How to implement**: Accept a function as children and call it with data

**Example skeleton**:
```typescript
// TODO: Add example code
interface DataProviderProps {
  children: (data: any, isLoading: boolean) => React.ReactNode
}

const DataProvider: React.FC<DataProviderProps> = ({ children }) => {
  const { data, isLoading } = useQuery('/api/data')
  return <>{children(data, isLoading)}</>
}

// Usage:
<DataProvider>
  {(data, isLoading) => (
    isLoading ? <Spinner /> : <DataDisplay data={data} />
  )}
</DataProvider>
```

### Pattern 6: Slots Pattern

**When to use**: When you need multiple named insertion points in a component

**How to implement**: Accept multiple children via separate props

**Example skeleton**:
```typescript
// TODO: Add example code
interface CardProps {
  header?: React.ReactNode
  footer?: React.ReactNode
  children: React.ReactNode
}

const Card: React.FC<CardProps> = ({ header, footer, children }) => (
  <div className="card">
    {header && <div className="card-header">{header}</div>}
    <div className="card-body">{children}</div>
    {footer && <div className="card-footer">{footer}</div>}
  </div>
)

// Usage:
<Card
  header={<h2>Title</h2>}
  footer={<button>Action</button>}
>
  <p>Content</p>
</Card>
```

### Pattern 7: Controlled vs Uncontrolled Components

**When to use**:
- Controlled: When React state should be source of truth
- Uncontrolled: For simple forms or integrating with non-React code

**How to implement**:

**Example skeleton**:
```typescript
// TODO: Add example code
// Controlled input
const ControlledInput = () => {
  const [value, setValue] = useState('')
  return <input value={value} onChange={(e) => setValue(e.target.value)} />
}

// Uncontrolled input
const UncontrolledInput = () => {
  const inputRef = useRef<HTMLInputElement>(null)
  const handleSubmit = () => {
    console.log(inputRef.current?.value)
  }
  return <input ref={inputRef} defaultValue="" />
}
```

**References**:
- [React Docs - Controlled Components](https://react.dev/reference/react-dom/components/input#controlling-an-input-with-a-state-variable)

### Pattern 8: Component Composition with Dot Notation

**When to use**: For related components that belong together as a family

**How to implement**: Attach child components as properties of parent

**Example skeleton**:
```typescript
// TODO: Add example code
const Card = ({ children }: { children: React.ReactNode }) => (
  <div className="card">{children}</div>
)

Card.Header = ({ children }: { children: React.ReactNode }) => (
  <div className="card-header">{children}</div>
)

Card.Body = ({ children }: { children: React.ReactNode }) => (
  <div className="card-body">{children}</div>
)

Card.Footer = ({ children }: { children: React.ReactNode }) => (
  <div className="card-footer">{children}</div>
)

// Usage:
<Card>
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
  <Card.Footer>Actions</Card.Footer>
</Card>
```

## Common Mistakes

1. **Over-Composition**: Breaking components into too many tiny pieces
2. **Prop Drilling**: Passing props through many layers instead of using Context
3. **Tight Coupling**: Making components depend on specific parent/child structure
4. **God Components**: Single component doing too many things
5. **Premature Abstraction**: Creating reusable components before patterns emerge

## Component Organization Strategies

### By Feature (Recommended)
```
features/
  users/
    components/
      UserList.tsx
      UserCard.tsx
    hooks/
      useUsers.ts
    types/
      user.types.ts
```

### By Type
```
components/
  UserList.tsx
  ProductCard.tsx
hooks/
  useUsers.ts
  useProducts.ts
types/
  user.types.ts
  product.types.ts
```

## Tools and Libraries

- **Radix UI**: Unstyled accessible components
- **shadcn/ui**: Copy-paste component library built on Radix
- **Headless UI**: Unstyled, accessible UI components
- **React Aria**: Accessible component primitives from Adobe

## Additional Resources

- [React Docs - Composition vs Inheritance](https://react.dev/learn/passing-props-to-a-component)
- [Patterns.dev - React Component Patterns](https://www.patterns.dev/react)
- [UXPin - React Design Patterns](https://www.uxpin.com/studio/blog/react-design-patterns/)
- [Kent C. Dodds - Advanced React Patterns](https://kentcdodds.com/blog/advanced-react-component-patterns)

## Next Steps

- See [HOOKS_PATTERNS.md](./HOOKS_PATTERNS.md) for custom hook patterns
- Review [TYPESCRIPT_REACT.md](./TYPESCRIPT_REACT.md) for typing component props
- Check [ANTIPATTERNS.md](./ANTIPATTERNS.md) for component anti-patterns
