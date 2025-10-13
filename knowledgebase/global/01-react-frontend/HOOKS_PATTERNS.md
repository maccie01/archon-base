# React Hooks Patterns

Created: 2025-10-13
Last Research: 2025-10-13
Sources: React Official Docs, Web Research (LogRocket, Devtrium, Medium)

## Overview

React Hooks enable functional components to have state and side effects. This document covers built-in hooks, custom hooks patterns, and best practices for hooks usage in React 18+.

## Core Principles

1. **Only Call Hooks at Top Level**: Never in loops, conditions, or nested functions
2. **Only Call Hooks from React Functions**: From functional components or custom hooks
3. **Follow Naming Convention**: Always prefix custom hooks with "use"
4. **Complete Dependencies**: Include all dependencies in dependency arrays
5. **Single Responsibility**: Each custom hook should have one focused purpose

## Built-in Hooks Patterns

### Pattern 1: useState - State Management

**When to use**: For component-local state

**How to implement**: Call useState with initial value

**Example skeleton**:
```typescript
// TODO: Add example code
// Basic usage
const [count, setCount] = useState(0)

// With type annotation
const [user, setUser] = useState<User | null>(null)

// Lazy initialization (for expensive computations)
const [state, setState] = useState(() => {
  return expensiveComputation()
})

// Functional updates (when new state depends on previous)
setCount(prevCount => prevCount + 1)
```

**References**:
- [React Docs - useState](https://react.dev/reference/react/useState)

### Pattern 2: useEffect - Side Effects

**When to use**: For side effects like data fetching, subscriptions, DOM manipulation

**How to implement**: Pass effect function and dependency array

**Example skeleton**:
```typescript
// TODO: Add example code
// Run once on mount
useEffect(() => {
  fetchData()
}, [])

// Run when dependencies change
useEffect(() => {
  document.title = `Count: ${count}`
}, [count])

// Cleanup function
useEffect(() => {
  const subscription = subscribe()
  return () => subscription.unsubscribe()
}, [])

// Multiple effects for separation of concerns
useEffect(() => {
  // Effect 1: Document title
  document.title = title
}, [title])

useEffect(() => {
  // Effect 2: API call
  fetchData()
}, [id])
```

**Common mistakes**:
- Missing dependencies (use ESLint plugin to catch)
- Including objects/functions in dependencies without memoization
- Using useEffect for state transformations (use useMemo instead)

**References**:
- [React Docs - useEffect](https://react.dev/reference/react/useEffect)

### Pattern 3: useContext - Context Consumption

**When to use**: To access Context values without prop drilling

**How to implement**: Call useContext with Context object

**Example skeleton**:
```typescript
// TODO: Add example code
// Define context
const ThemeContext = createContext<'light' | 'dark'>('light')

// Provider
const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState('light')
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

// Consumer with useContext
const ThemedButton = () => {
  const { theme, setTheme } = useContext(ThemeContext)
  return <button className={theme}>Click me</button>
}
```

**References**:
- [React Docs - useContext](https://react.dev/reference/react/useContext)

### Pattern 4: useMemo - Expensive Computation Memoization

**When to use**: To memoize expensive calculations that don't need to run on every render

**How to implement**: Pass computation function and dependency array

**Example skeleton**:
```typescript
// TODO: Add example code
const ExpensiveComponent = ({ items, filter }) => {
  // Memoize expensive filtering operation
  const filteredItems = useMemo(() => {
    return items.filter(item => item.matches(filter))
  }, [items, filter])

  return <List items={filteredItems} />
}

// Memoize object/array to prevent reference changes
const config = useMemo(() => ({
  theme: 'dark',
  locale: 'en'
}), [])
```

**When NOT to use**:
- For cheap calculations (overhead may not be worth it)
- Before profiling shows a performance issue

**References**:
- [React Docs - useMemo](https://react.dev/reference/react/useMemo)

### Pattern 5: useCallback - Function Memoization

**When to use**: To memoize callback functions, especially when passed to child components

**How to implement**: Pass callback function and dependency array

**Example skeleton**:
```typescript
// TODO: Add example code
const ParentComponent = () => {
  const [count, setCount] = useState(0)

  // Memoize callback to prevent child re-renders
  const handleClick = useCallback(() => {
    setCount(prev => prev + 1)
  }, [])

  return <MemoizedChild onClick={handleClick} />
}

// In TypeScript, specify parameter types
const handleSubmit = useCallback((data: FormData) => {
  submitForm(data)
}, [])
```

**References**:
- [React Docs - useCallback](https://react.dev/reference/react/useCallback)

### Pattern 6: useReducer - Complex State Logic

**When to use**: When state logic is complex or involves multiple sub-values

**How to implement**: Define reducer function, initial state, and dispatch actions

**Example skeleton**:
```typescript
// TODO: Add example code
type State = { count: number; step: number }
type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'set_step'; step: number }

const reducer = (state: State, action: Action): State => {
  switch (action.type) {
    case 'increment':
      return { ...state, count: state.count + state.step }
    case 'decrement':
      return { ...state, count: state.count - state.step }
    case 'set_step':
      return { ...state, step: action.step }
    default:
      return state
  }
}

const Counter = () => {
  const [state, dispatch] = useReducer(reducer, { count: 0, step: 1 })

  return (
    <>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
    </>
  )
}
```

**References**:
- [React Docs - useReducer](https://react.dev/reference/react/useReducer)

### Pattern 7: useRef - Mutable References

**When to use**: For accessing DOM elements or storing mutable values that don't trigger re-renders

**How to implement**: Call useRef with initial value

**Example skeleton**:
```typescript
// TODO: Add example code
// DOM reference
const InputComponent = () => {
  const inputRef = useRef<HTMLInputElement>(null)

  const focusInput = () => {
    inputRef.current?.focus()
  }

  return <input ref={inputRef} />
}

// Mutable value (doesn't trigger re-render)
const Timer = () => {
  const intervalRef = useRef<number>()

  useEffect(() => {
    intervalRef.current = window.setInterval(() => {
      console.log('tick')
    }, 1000)

    return () => clearInterval(intervalRef.current)
  }, [])
}
```

**References**:
- [React Docs - useRef](https://react.dev/reference/react/useRef)

### Pattern 8: React 18+ Hooks

**useTransition**: Mark state updates as non-urgent
```typescript
// TODO: Add example code
const [isPending, startTransition] = useTransition()

startTransition(() => {
  setSearchQuery(input) // Non-urgent update
})
```

**useDeferredValue**: Defer re-rendering for non-critical parts
```typescript
// TODO: Add example code
const deferredQuery = useDeferredValue(searchQuery)
```

**useId**: Generate unique IDs for accessibility
```typescript
// TODO: Add example code
const id = useId()
return <><label htmlFor={id}>Name</label><input id={id} /></>
```

**References**:
- [React Docs - useTransition](https://react.dev/reference/react/useTransition)
- [React Docs - useDeferredValue](https://react.dev/reference/react/useDeferredValue)
- [React Docs - useId](https://react.dev/reference/react/useId)

## Custom Hooks Patterns

### Pattern 1: Data Fetching Hook

**When to use**: To encapsulate data fetching logic

**Example skeleton**:
```typescript
// TODO: Add example code
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(url)
        const json = await response.json()
        setData(json)
      } catch (err) {
        setError(err as Error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()
  }, [url])

  return { data, isLoading, error }
}

// Usage:
const { data, isLoading, error } = useFetch<User[]>('/api/users')
```

### Pattern 2: Local Storage Hook

**When to use**: To sync state with localStorage

**Example skeleton**:
```typescript
// TODO: Add example code
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      return initialValue
    }
  })

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value
      setStoredValue(valueToStore)
      window.localStorage.setItem(key, JSON.stringify(valueToStore))
    } catch (error) {
      console.error(error)
    }
  }

  return [storedValue, setValue] as const
}
```

### Pattern 3: Media Query Hook

**When to use**: To respond to media query changes

**Example skeleton**:
```typescript
// TODO: Add example code
function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(() => window.matchMedia(query).matches)

  useEffect(() => {
    const mediaQuery = window.matchMedia(query)
    const handler = (e: MediaQueryListEvent) => setMatches(e.matches)

    mediaQuery.addEventListener('change', handler)
    return () => mediaQuery.removeEventListener('change', handler)
  }, [query])

  return matches
}

// Usage:
const isMobile = useMediaQuery('(max-width: 768px)')
```

### Pattern 4: Debounced Value Hook

**When to use**: To debounce rapidly changing values (e.g., search input)

**Example skeleton**:
```typescript
// TODO: Add example code
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => clearTimeout(handler)
  }, [value, delay])

  return debouncedValue
}

// Usage:
const [searchTerm, setSearchTerm] = useState('')
const debouncedSearch = useDebounce(searchTerm, 500)
```

### Pattern 5: Previous Value Hook

**When to use**: To access previous value of state/prop

**Example skeleton**:
```typescript
// TODO: Add example code
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>()

  useEffect(() => {
    ref.current = value
  }, [value])

  return ref.current
}

// Usage:
const [count, setCount] = useState(0)
const previousCount = usePrevious(count)
```

## Custom Hooks Best Practices

1. **Naming**: Always start with "use"
2. **Single Responsibility**: One hook, one purpose
3. **Return Tuples or Objects**: Consistently use one pattern
4. **Include All Dependencies**: No missing dependencies
5. **Document Complex Hooks**: Add JSDoc comments
6. **Test Independently**: Write unit tests for custom hooks
7. **Keep Hooks Focused**: Break down complex hooks into smaller ones

## Common Mistakes

1. **Conditional Hook Calls**: Never call hooks inside if statements
2. **Missing Dependencies**: Always include all dependencies in arrays
3. **Object/Function Dependencies**: Can cause infinite loops without memoization
4. **useEffect for Derived State**: Use useMemo or compute during render
5. **Premature Optimization**: Don't use useMemo/useCallback without profiling
6. **Stale Closures**: Not updating dependencies can lead to stale values
7. **Not Cleaning Up**: Forgetting cleanup functions in useEffect

## React 19 Hooks Updates

With React 19's compiler:
- Automatic memoization reduces need for useMemo/useCallback
- Manual memoization still useful for expensive operations
- Focus on correct dependencies, compiler handles optimization

## Tools and Libraries

- **eslint-plugin-react-hooks**: Catches hooks mistakes
- **@tanstack/react-query**: Advanced data fetching hooks
- **usehooks-ts**: Collection of common hooks
- **react-use**: Large collection of reusable hooks

## Additional Resources

- [React Docs - Hooks API Reference](https://react.dev/reference/react)
- [React Hooks Cheat Sheet (LogRocket)](https://blog.logrocket.com/react-hooks-cheat-sheet-solutions-common-problems/)
- [React TypeScript - How to Type Hooks (Devtrium)](https://devtrium.com/posts/react-typescript-how-to-type-hooks)
- [Custom Hooks Best Practices](https://react.dev/learn/reusing-logic-with-custom-hooks)

## Next Steps

- Review [STATE_MANAGEMENT.md](./STATE_MANAGEMENT.md) for global state patterns
- See [PERFORMANCE.md](./PERFORMANCE.md) for memoization strategies
- Check [ANTIPATTERNS.md](./ANTIPATTERNS.md) for hooks anti-patterns
