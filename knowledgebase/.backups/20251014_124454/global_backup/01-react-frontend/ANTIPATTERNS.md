# React Anti-Patterns to Avoid

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Web Research (Persson Dennis, Talent500, Medium, OOZOU, Java Code Geeks)

## Overview

Anti-patterns are common mistakes that lead to bugs, performance issues, and unmaintainable code. This document catalogs the most common React anti-patterns and how to avoid them.

## Core Principles to Remember

1. **Don't Mutate State**: Always create new objects/arrays
2. **Include All Dependencies**: In useEffect, useMemo, useCallback
3. **Use Stable Keys**: Never use array index as key
4. **Avoid Prop Drilling**: Use Context or state management
5. **Keep Components Focused**: Single responsibility principle

## Anti-Patterns

### Anti-Pattern 1: Mutating State Directly

**Problem**: React doesn't detect state changes

**Example of BAD code**:
```typescript
// ❌ BAD: Mutating state
const [user, setUser] = useState({ name: 'John', age: 25 })
user.age = 26 // Won't trigger re-render
setUser(user) // Still won't work (same reference)

const [items, setItems] = useState([1, 2, 3])
items.push(4) // Mutates array
setItems(items) // Won't trigger re-render
```

**Solution**:
```typescript
// ✅ GOOD: Create new objects/arrays
setUser({ ...user, age: 26 })
// Or
setUser(prev => ({ ...prev, age: 26 }))

setItems([...items, 4])
// Or
setItems(prev => [...prev, 4])
```

**Why it's bad**: React relies on immutability to detect changes. Mutations don't trigger re-renders.

**References**:
- [Anti-Patterns in React (Talent500)](https://talent500.com/blog/anti-patterns-in-react-that-you-should-avoid/)

### Anti-Pattern 2: Using Array Index as Key

**Problem**: Can cause bugs with reordering and unnecessary re-renders

**Example of BAD code**:
```typescript
// ❌ BAD: Using index as key
{items.map((item, index) => (
  <ListItem key={index} item={item} />
))}
```

**Solution**:
```typescript
// ✅ GOOD: Use stable unique identifiers
{items.map((item) => (
  <ListItem key={item.id} item={item} />
))}

// If no unique ID exists, generate one
import { nanoid } from 'nanoid'

const [items, setItems] = useState(
  data.map(item => ({ ...item, id: nanoid() }))
)
```

**Why it's bad**:
- Items can't be properly tracked when list changes
- State can get mixed up
- Performance issues with re-renders

**References**:
- [10 React Anti-Patterns (Medium)](https://yosua-halim.medium.com/10-react-anti-patterns-you-should-know-300256bfb007)

### Anti-Pattern 3: Prop Drilling

**Problem**: Passing props through many intermediate components

**Example of BAD code**:
```typescript
// ❌ BAD: Prop drilling through 5 levels
function App() {
  const [user, setUser] = useState(null)
  return <Layout user={user} setUser={setUser} />
}

function Layout({ user, setUser }) {
  return <Sidebar user={user} setUser={setUser} />
}

function Sidebar({ user, setUser }) {
  return <Menu user={user} setUser={setUser} />
}

function Menu({ user, setUser }) {
  return <UserInfo user={user} setUser={setUser} />
}

function UserInfo({ user, setUser }) {
  return <div>{user.name}</div>
}
```

**Solution**:
```typescript
// ✅ GOOD: Use Context API
const UserContext = createContext()

function App() {
  const [user, setUser] = useState(null)
  return (
    <UserContext.Provider value={{ user, setUser }}>
      <Layout />
    </UserContext.Provider>
  )
}

function UserInfo() {
  const { user } = useContext(UserContext)
  return <div>{user.name}</div>
}

// Or use state management (Zustand, Redux, etc.)
```

**Why it's bad**:
- Hard to maintain
- Intermediate components need to know about props they don't use
- Difficult to refactor

**References**:
- [6 React Anti-Patterns (OOZOU)](https://oozou.com/blog/6-react-anti-patterns-to-avoid-206)

### Anti-Pattern 4: Missing Dependencies in Hooks

**Problem**: Stale closures and bugs from outdated values

**Example of BAD code**:
```typescript
// ❌ BAD: Missing dependencies
function Component({ userId }) {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetchData(userId).then(setData)
  }, []) // Missing userId dependency!

  const handleClick = useCallback(() => {
    updateData(userId) // Stale userId
  }, []) // Missing userId!
}
```

**Solution**:
```typescript
// ✅ GOOD: Include all dependencies
useEffect(() => {
  fetchData(userId).then(setData)
}, [userId])

const handleClick = useCallback(() => {
  updateData(userId)
}, [userId])

// Use ESLint plugin to catch missing dependencies
```

**Why it's bad**:
- Stale values lead to bugs
- Effect doesn't run when it should
- Hard to debug

**Enable ESLint rule**:
```json
{
  "rules": {
    "react-hooks/exhaustive-deps": "error"
  }
}
```

**References**:
- [React Anti-Patterns (Persson Dennis)](https://www.perssondennis.com/articles/react-anti-patterns-and-best-practices-dos-and-donts)

### Anti-Pattern 5: Not Storing State Properly

**Problem**: Using plain variables instead of useState

**Example of BAD code**:
```typescript
// ❌ BAD: Plain variable won't trigger re-render
function Component() {
  let count = 0

  const increment = () => {
    count++ // Won't trigger re-render!
    console.log(count) // Shows updated value
  }

  return <div>{count}</div> // Never updates UI
}
```

**Solution**:
```typescript
// ✅ GOOD: Use useState
function Component() {
  const [count, setCount] = useState(0)

  const increment = () => {
    setCount(prev => prev + 1)
  }

  return <div>{count}</div>
}
```

**References**:
- [React Anti-Patterns (Medium)](https://medium.com/@shriharim006/react-anti-patterns-to-void-5dbc930a714a)

### Anti-Pattern 6: Creating Massive Components

**Problem**: God components that do everything

**Example of BAD code**:
```typescript
// ❌ BAD: 500+ line component
function UserDashboard() {
  // 50 useState hooks
  // 20 useEffect hooks
  // Complex business logic
  // API calls
  // UI rendering
  // Form handling
  // All in one component
}
```

**Solution**:
```typescript
// ✅ GOOD: Break into smaller components
function UserDashboard() {
  return (
    <>
      <UserHeader />
      <UserStats />
      <UserActivity />
      <UserSettings />
    </>
  )
}

// Each component handles one concern
function UserStats() {
  const { data } = useUserStats()
  return <StatsDisplay data={data} />
}
```

**Why it's bad**:
- Hard to understand
- Difficult to test
- Can't reuse parts
- Performance issues

**References**:
- [5 React Anti-Patterns (Java Code Geeks)](https://www.javacodegeeks.com/2024/07/avoiding-5-react-anti-patterns-for-a-cleaner-codebase.html)

### Anti-Pattern 7: Inline Object/Array in Props

**Problem**: Creates new reference on every render, breaking memoization

**Example of BAD code**:
```typescript
// ❌ BAD: New object/array every render
function Parent() {
  return (
    <>
      <ChildComponent config={{ theme: 'dark' }} />
      <ChildComponent items={[1, 2, 3]} />
    </>
  )
}

// Even if ChildComponent is memoized, it re-renders every time!
const ChildComponent = React.memo(({ config, items }) => {
  return <div>...</div>
})
```

**Solution**:
```typescript
// ✅ GOOD: Memoize or move outside
const CONFIG = { theme: 'dark' }
const ITEMS = [1, 2, 3]

function Parent() {
  return (
    <>
      <ChildComponent config={CONFIG} />
      <ChildComponent items={ITEMS} />
    </>
  )
}

// Or use useMemo for dynamic values
function Parent() {
  const config = useMemo(() => ({ theme: 'dark' }), [])

  return <ChildComponent config={config} />
}
```

### Anti-Pattern 8: Using useEffect for Derived State

**Problem**: Unnecessary complexity and potential bugs

**Example of BAD code**:
```typescript
// ❌ BAD: Using useEffect for derived state
function Component({ items }) {
  const [count, setCount] = useState(0)

  useEffect(() => {
    setCount(items.length)
  }, [items])

  return <div>Count: {count}</div>
}
```

**Solution**:
```typescript
// ✅ GOOD: Calculate during render
function Component({ items }) {
  const count = items.length

  return <div>Count: {count}</div>
}

// Or use useMemo for expensive calculations
function Component({ items }) {
  const filteredCount = useMemo(() => {
    return items.filter(item => item.active).length
  }, [items])

  return <div>Count: {filteredCount}</div>
}
```

**Why it's bad**:
- Extra re-render
- More complex
- Can cause timing bugs

### Anti-Pattern 9: Ignoring Key Warnings

**Problem**: "Each child should have a unique key prop" warning

**Example of BAD code**:
```typescript
// ❌ BAD: Ignoring or suppressing warnings
{items.map(item => (
  <div>{item.name}</div> // No key!
))}

// Or worse, using index
{items.map((item, i) => (
  <div key={i}>{item.name}</div>
))}
```

**Solution**:
```typescript
// ✅ GOOD: Use proper unique keys
{items.map(item => (
  <div key={item.id}>{item.name}</div>
))}
```

### Anti-Pattern 10: Conditional Hook Calls

**Problem**: Breaks rules of hooks

**Example of BAD code**:
```typescript
// ❌ BAD: Conditional hooks
function Component({ shouldFetch }) {
  const [data, setData] = useState(null)

  if (shouldFetch) {
    useEffect(() => {
      fetchData().then(setData)
    }, []) // ERROR: Hook in conditional!
  }

  return <div>{data}</div>
}
```

**Solution**:
```typescript
// ✅ GOOD: Condition inside hook
function Component({ shouldFetch }) {
  const [data, setData] = useState(null)

  useEffect(() => {
    if (shouldFetch) {
      fetchData().then(setData)
    }
  }, [shouldFetch])

  return <div>{data}</div>
}
```

**Why it's bad**:
- Breaks React's internal hook tracking
- Causes crashes
- Unpredictable behavior

### Anti-Pattern 11: Skipping Tests

**Problem**: No test coverage leads to bugs

**Solution**:
- Write tests for critical user flows
- Test error states
- Use React Testing Library
- Aim for 80%+ coverage on critical paths

**References**:
- [3 React Anti-Patterns (Caktus Group)](https://www.caktusgroup.com/blog/2023/02/02/3-react-anti-patterns-and-how-fix-them/)

### Anti-Pattern 12: Over-Optimizing Too Early

**Problem**: Using useMemo/useCallback everywhere without profiling

**Example of BAD code**:
```typescript
// ❌ BAD: Memoizing everything
function Component() {
  const value = useMemo(() => 5, []) // Pointless
  const greeting = useMemo(() => 'Hello', []) // Pointless

  const handleClick = useCallback(() => {
    console.log('clicked')
  }, []) // Probably unnecessary

  return <div>{greeting}</div>
}
```

**Solution**:
```typescript
// ✅ GOOD: Optimize when needed
function Component() {
  // Simple values don't need memoization
  const value = 5
  const greeting = 'Hello'

  // Only memoize when:
  // 1. Profiling shows performance issue
  // 2. Expensive calculation
  // 3. Passed to memoized child

  return <div>{greeting}</div>
}
```

**Why it's bad**:
- Adds overhead
- Makes code harder to read
- No benefit without actual performance issue

## Quick Reference: Do's and Don'ts

### Do's
- ✅ Use semantic HTML
- ✅ Keep components small and focused
- ✅ Use TypeScript for type safety
- ✅ Write tests for critical flows
- ✅ Profile before optimizing
- ✅ Use stable unique keys
- ✅ Include all dependencies in hooks
- ✅ Use Context/state management to avoid prop drilling

### Don'ts
- ❌ Mutate state directly
- ❌ Use array index as key
- ❌ Skip tests
- ❌ Create massive components
- ❌ Ignore ESLint warnings
- ❌ Forget dependencies in hooks
- ❌ Use useEffect for derived state
- ❌ Over-optimize prematurely

## Tools to Prevent Anti-Patterns

### ESLint
```json
{
  "extends": [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended"
  ],
  "rules": {
    "react-hooks/rules-of-hooks": "error",
    "react-hooks/exhaustive-deps": "error"
  }
}
```

### TypeScript
- Catches type errors at compile-time
- Prevents many runtime bugs
- Improves developer experience

### React DevTools
- Profile components
- Identify unnecessary re-renders
- Debug state and props

## Additional Resources

- [React Anti-Patterns (Persson Dennis)](https://www.perssondennis.com/articles/react-anti-patterns-and-best-practices-dos-and-donts)
- [Anti-Patterns in React (Talent500)](https://talent500.com/blog/anti-patterns-in-react-that-you-should-avoid/)
- [10 React Anti-Patterns (Medium)](https://yosua-halim.medium.com/10-react-anti-patterns-you-should-know-300256bfb007)
- [6 React Anti-Patterns (OOZOU)](https://oozou.com/blog/6-react-anti-patterns-to-avoid-206)
- [Avoiding React Anti-Patterns (Java Code Geeks)](https://www.javacodegeeks.com/2024/07/avoiding-5-react-anti-patterns-for-a-cleaner-codebase.html)
- [React Patterns and Anti-Patterns (InnovationM)](https://innovationm.com/blog/react-patterns-and-anti-patterns-common-mistakes-to-avoid/)

## Next Steps

- Review [REACT_BEST_PRACTICES.md](./REACT_BEST_PRACTICES.md) for correct patterns
- See [HOOKS_PATTERNS.md](./HOOKS_PATTERNS.md) for proper hook usage
- Check [PERFORMANCE.md](./PERFORMANCE.md) for optimization strategies
