# React Best Practices (2024-2025)

Created: 2025-10-13
Last Research: 2025-10-13
Sources: React Official Docs, Web Research (Telerik, UXPin, GeeksforGeeks, Medium)

## Overview

This document outlines fundamental best practices for React development based on React 18+ features and modern development standards. These patterns are framework-agnostic and applicable to any React project.

## Core Principles

1. **Function Components Over Class Components**: Use functional components with hooks as the default approach
2. **Component Composition**: Build complex UIs from smaller, focused components
3. **Single Responsibility**: Each component should have one clear purpose
4. **Immutable State**: Never mutate state directly; always use setState functions
5. **Code Splitting**: Use lazy loading and dynamic imports for optimal bundle sizes

## Patterns

### Pattern 1: Functional Components as Default

**When to use**: For all new components (99% of use cases)

**How to implement**: Use arrow functions or function declarations with hooks

**Example skeleton**:
```typescript
// TODO: Add example code
// Preferred pattern:
const MyComponent = () => {
  // Component logic
  return <div>Component content</div>
}

// Or with props typing:
interface MyComponentProps {
  // prop types
}

const MyComponent: React.FC<MyComponentProps> = (props) => {
  // Component logic
  return <div>{props.children}</div>
}
```

**References**:
- [React Docs - Function Components](https://react.dev/learn)
- Web research indicates functional components are now the de facto standard

### Pattern 2: Custom Hooks for Reusable Logic

**When to use**: When the same stateful logic appears in multiple components

**How to implement**: Extract logic into functions prefixed with "use"

**Example skeleton**:
```typescript
// TODO: Add example code
// Custom hook pattern:
function useCustomLogic() {
  const [state, setState] = useState(initialValue)

  useEffect(() => {
    // Side effects
  }, [dependencies])

  return { state, setState }
}

// Usage in component:
const MyComponent = () => {
  const { state, setState } = useCustomLogic()
  return <div>{state}</div>
}
```

**References**:
- [React Docs - Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks)
- Web research: Custom hooks are one of the most powerful patterns in modern React

### Pattern 3: Component Composition

**When to use**: To build complex UIs from simpler components

**How to implement**: Use props.children and composition instead of inheritance

**Example skeleton**:
```typescript
// TODO: Add example code
// Composition pattern:
const Card = ({ children }) => (
  <div className="card">{children}</div>
)

const CardHeader = ({ children }) => (
  <div className="card-header">{children}</div>
)

// Usage:
<Card>
  <CardHeader>Title</CardHeader>
  <div>Content</div>
</Card>
```

**References**:
- [React Docs - Composition vs Inheritance](https://react.dev/learn/passing-props-to-a-component)

### Pattern 4: Code Splitting with React.lazy

**When to use**: For large components or routes that aren't immediately needed

**How to implement**: Use React.lazy with Suspense boundaries

**Example skeleton**:
```typescript
// TODO: Add example code
const HeavyComponent = React.lazy(() => import('./HeavyComponent'))

const App = () => (
  <Suspense fallback={<div>Loading...</div>}>
    <HeavyComponent />
  </Suspense>
)
```

**References**:
- [React Docs - Code Splitting](https://react.dev/reference/react/lazy)

### Pattern 5: Controlled Components for Forms

**When to use**: For form inputs that need React state management

**How to implement**: Connect input value to state and update via onChange

**Example skeleton**:
```typescript
// TODO: Add example code
const FormComponent = () => {
  const [value, setValue] = useState('')

  return (
    <input
      value={value}
      onChange={(e) => setValue(e.target.value)}
    />
  )
}
```

**References**:
- [React Docs - Controlled Components](https://react.dev/reference/react-dom/components/input)

### Pattern 6: Key Props for Lists

**When to use**: When rendering arrays of elements

**How to implement**: Always provide stable, unique keys (never use array index)

**Example skeleton**:
```typescript
// TODO: Add example code
const ListComponent = ({ items }) => (
  <ul>
    {items.map(item => (
      <li key={item.id}>{item.name}</li>
    ))}
  </ul>
)
```

**References**:
- [React Docs - Lists and Keys](https://react.dev/learn/rendering-lists)

### Pattern 7: Prop Validation with TypeScript

**When to use**: Always, in TypeScript projects

**How to implement**: Define interfaces/types for component props

**Example skeleton**:
```typescript
// TODO: Add example code
interface ButtonProps {
  label: string
  onClick: () => void
  variant?: 'primary' | 'secondary'
}

const Button: React.FC<ButtonProps> = ({ label, onClick, variant = 'primary' }) => {
  return <button onClick={onClick}>{label}</button>
}
```

**References**:
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)

## Common Mistakes

1. **Mutating State Directly**: Never do `state.value = newValue`; always use setState
2. **Missing Dependencies in Hooks**: Always include all dependencies in useEffect/useCallback arrays
3. **Using Index as Key**: Avoid `key={index}` in lists; use stable unique identifiers
4. **Prop Drilling**: Don't pass props through many intermediate components; use Context or state management
5. **Massive Components**: Break down large components into smaller, focused ones
6. **Not Using Code Splitting**: Load all code upfront instead of lazy loading routes/components

## Tools and Libraries

### Essential Tools
- **Vite**: Modern build tool with fast HMR
- **TypeScript**: Static typing for better development experience
- **ESLint**: Code linting with react-hooks/recommended rules
- **Prettier**: Code formatting

### Recommended Libraries (by category)
- **Routing**: React Router, Wouter
- **State Management**: TanStack Query (server state), Zustand (client state)
- **Forms**: React Hook Form
- **UI Components**: shadcn/ui, Radix UI, Headless UI
- **Testing**: Vitest, React Testing Library

## React 18+ Features to Use

1. **Automatic Batching**: Multiple state updates are batched automatically
2. **Transitions**: Use `useTransition` for non-urgent updates
3. **Suspense for Data Fetching**: Wrap async components in Suspense boundaries
4. **useDeferredValue**: Defer rendering of non-critical UI parts
5. **useId**: Generate unique IDs for accessibility attributes

## React 19 Features (Stable Late 2024)

1. **React Compiler**: Automatic memoization (reduces need for useMemo/useCallback)
2. **Server Components**: Better performance for server-rendered content
3. **Actions**: Simplified form handling with server actions
4. **Enhanced use() Hook**: Simpler data fetching patterns

## Framework Recommendations

For new projects in 2025, consider these frameworks:
1. **Next.js**: Full-featured framework with SSR, SSG, and app router
2. **Remix**: Modern routing and data loading patterns
3. **Vite + React Router**: Lightweight SPA with fast development

## Additional Resources

- [React Official Documentation](https://react.dev)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- [Patterns.dev - React Patterns](https://www.patterns.dev/react)
- [React Best Practices 2024 (Telerik)](https://www.telerik.com/blogs/react-design-patterns-best-practices)
- [React Architecture Patterns (GeeksforGeeks)](https://www.geeksforgeeks.org/reactjs/react-architecture-pattern-and-best-practices/)

## Next Steps

- Review [COMPONENT_PATTERNS.md](./COMPONENT_PATTERNS.md) for detailed composition strategies
- See [HOOKS_PATTERNS.md](./HOOKS_PATTERNS.md) for advanced hook usage
- Check [ANTIPATTERNS.md](./ANTIPATTERNS.md) for common mistakes to avoid
