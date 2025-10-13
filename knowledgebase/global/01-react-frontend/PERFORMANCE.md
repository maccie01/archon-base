# React Performance Optimization

Created: 2025-10-13
Last Research: 2025-10-13
Sources: React Official Docs, Web Research (Medium, Saeloun, LogRocket, ContentFul)

## Overview

Performance optimization in React involves preventing unnecessary re-renders, optimizing expensive computations, and implementing code splitting. With React 19's compiler, many manual optimizations become automatic, but understanding these patterns remains crucial.

## Core Principles

1. **Profile Before Optimizing**: Use React DevTools Profiler to identify actual bottlenecks
2. **Premature Optimization is Evil**: Don't optimize until you have a measured problem
3. **Memoization is Not Free**: Has overhead; only use when profiling shows benefit
4. **Code Splitting**: Load code when needed, not upfront
5. **React 19 Compiler**: Handles most memoization automatically

## Patterns

### Pattern 1: React.memo - Component Memoization

**When to use**: To prevent re-renders when props haven't changed

**How to implement**: Wrap component with React.memo

**Example skeleton**:
```typescript
// TODO: Add example code
const ExpensiveComponent = React.memo<Props>(({ data, onUpdate }) => {
  // Expensive rendering logic
  return <div>{data}</div>
})

// With custom comparison function
const MemoizedComponent = React.memo(
  Component,
  (prevProps, nextProps) => {
    // Return true if passing nextProps would render same result
    return prevProps.id === nextProps.id
  }
)
```

**When NOT to use**:
- Component renders quickly (< 1ms)
- Props change on every render
- Before profiling shows a problem

**References**:
- [React Docs - memo](https://react.dev/reference/react/memo)
- [React Memo Performance Guide](https://www.contentful.com/blog/react-memo-improve-performance/)

### Pattern 2: useMemo - Value Memoization

**When to use**: To cache expensive calculations

**How to implement**: Wrap computation in useMemo with dependencies

**Example skeleton**:
```typescript
// TODO: Add example code
const Component = ({ items, filter }) => {
  // Memoize expensive filtering
  const filteredItems = useMemo(() => {
    return items
      .filter(item => item.includes(filter))
      .sort((a, b) => a.localeCompare(b))
  }, [items, filter])

  // Memoize object/array creation
  const config = useMemo(() => ({
    theme: 'dark',
    settings: complexCalculation()
  }), [])

  return <List items={filteredItems} config={config} />
}
```

**References**:
- [React Docs - useMemo](https://react.dev/reference/react/useMemo)
- [Mastering useMemo Guide](https://www.technicalexplore.com/tech/mastering-usememo-in-react-a-comprehensive-guide-to-performance-optimization)

### Pattern 3: useCallback - Function Memoization

**When to use**: To memoize callback functions, especially when passed to memoized children

**How to implement**: Wrap function in useCallback with dependencies

**Example skeleton**:
```typescript
// TODO: Add example code
const ParentComponent = () => {
  const [count, setCount] = useState(0)

  // Memoize callback
  const handleClick = useCallback(() => {
    setCount(prev => prev + 1)
  }, [])

  // Memoize with dependencies
  const handleUpdate = useCallback((id: number) => {
    updateItem(id, count)
  }, [count])

  return <MemoizedChild onClick={handleClick} onUpdate={handleUpdate} />
}

const MemoizedChild = React.memo(({ onClick, onUpdate }) => {
  // Won't re-render unless onClick/onUpdate reference changes
  return <button onClick={onClick}>Click</button>
})
```

**References**:
- [React Docs - useCallback](https://react.dev/reference/react/useCallback)

### Pattern 4: Code Splitting with React.lazy

**When to use**: For routes, heavy components, or features not immediately needed

**How to implement**: Use React.lazy and Suspense

**Example skeleton**:
```typescript
// TODO: Add example code
import { lazy, Suspense } from 'react'

// Lazy load route components
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Settings = lazy(() => import('./pages/Settings'))

// With fallback UI
const App = () => (
  <Suspense fallback={<LoadingSpinner />}>
    <Routes>
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/settings" element={<Settings />} />
    </Routes>
  </Suspense>
)

// Preload on hover
const link = document.querySelector('a[href="/dashboard"]')
link.addEventListener('mouseenter', () => {
  import('./pages/Dashboard')
})
```

**References**:
- [React Docs - lazy](https://react.dev/reference/react/lazy)

### Pattern 5: List Virtualization

**When to use**: For long lists (100+ items) or tables

**How to implement**: Use react-window or react-virtual

**Example skeleton**:
```typescript
// TODO: Add example code
import { FixedSizeList } from 'react-window'

const VirtualizedList = ({ items }) => (
  <FixedSizeList
    height={600}
    itemCount={items.length}
    itemSize={50}
    width="100%"
  >
    {({ index, style }) => (
      <div style={style}>
        {items[index].name}
      </div>
    )}
  </FixedSizeList>
)
```

**Libraries**:
- react-window: Lightweight virtualization
- @tanstack/react-virtual: Modern, framework-agnostic

**References**:
- [react-window Documentation](https://github.com/bvaughn/react-window)

### Pattern 6: useTransition - Non-Urgent Updates

**When to use**: For updates that can be deferred (React 18+)

**How to implement**: Wrap state updates in startTransition

**Example skeleton**:
```typescript
// TODO: Add example code
const SearchComponent = () => {
  const [query, setQuery] = useState('')
  const [isPending, startTransition] = useTransition()

  const handleChange = (e) => {
    // Urgent: update input immediately
    setQuery(e.target.value)

    // Non-urgent: update search results
    startTransition(() => {
      setSearchResults(search(e.target.value))
    })
  }

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending && <Spinner />}
      <Results data={searchResults} />
    </>
  )
}
```

**References**:
- [React Docs - useTransition](https://react.dev/reference/react/useTransition)

### Pattern 7: useDeferredValue - Deferred Rendering

**When to use**: To defer re-rendering of non-critical UI

**How to implement**: Wrap value with useDeferredValue

**Example skeleton**:
```typescript
// TODO: Add example code
const SearchPage = () => {
  const [query, setQuery] = useState('')
  const deferredQuery = useDeferredValue(query)

  // Results update with deferred value
  const results = useMemo(
    () => search(deferredQuery),
    [deferredQuery]
  )

  return (
    <>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <Results query={deferredQuery} results={results} />
    </>
  )
}
```

**References**:
- [React Docs - useDeferredValue](https://react.dev/reference/react/useDeferredValue)

### Pattern 8: Dynamic Import for Heavy Libraries

**When to use**: For large third-party libraries

**How to implement**: Import only when needed

**Example skeleton**:
```typescript
// TODO: Add example code
const ChartComponent = () => {
  const [Chart, setChart] = useState(null)

  useEffect(() => {
    // Load chart library only when component mounts
    import('chart.js').then((module) => {
      setChart(() => module.Chart)
    })
  }, [])

  if (!Chart) return <Skeleton />

  return <Chart {...chartProps} />
}
```

## React 19 Performance Features

### 1. React Compiler (Automatic Memoization)
- Automatically optimizes components
- Reduces need for manual React.memo, useMemo, useCallback
- Still useful to understand memoization concepts

### 2. Server Components
- Run on server, send HTML to client
- Reduce bundle size
- Better initial load performance

**Example skeleton**:
```typescript
// TODO: Add example code
// app/posts/page.tsx (Server Component by default)
async function PostsList() {
  const posts = await db.posts.findMany()
  return (
    <ul>
      {posts.map(post => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

## Profiling and Measurement

### React DevTools Profiler

**How to use**:
1. Install React DevTools browser extension
2. Open DevTools > Profiler tab
3. Click record, interact with app, stop recording
4. Review flame graph and ranked chart
5. Identify slow components

**Example skeleton**:
```typescript
// TODO: Add example code
import { Profiler } from 'react'

<Profiler
  id="Navigation"
  onRender={(id, phase, actualDuration) => {
    console.log(`${id} took ${actualDuration}ms to render`)
  }}
>
  <Navigation />
</Profiler>
```

### Browser Performance Tools

- Chrome DevTools Performance tab
- Lighthouse for Core Web Vitals
- React DevTools Profiler

## Bundle Size Optimization

### 1. Tree Shaking
- Import only what you need: `import { Button } from 'lib'` not `import * as Lib from 'lib'`
- Use ES modules

### 2. Bundle Analysis
```bash
# Vite
npm run build
npx vite-bundle-visualizer

# Webpack
npx webpack-bundle-analyzer dist/stats.json
```

### 3. Dynamic Imports
- Split code by route
- Load heavy features on demand

## Common Mistakes

1. **Premature Optimization**: Memoizing everything without profiling
2. **Missing Dependencies**: Incomplete dependency arrays in useMemo/useCallback
3. **Memoizing Cheap Operations**: Overhead exceeds benefit
4. **Not Using Keys**: Missing or unstable keys in lists
5. **Inline Functions/Objects as Props**: Creates new references on every render
6. **Not Code Splitting**: Loading entire app upfront
7. **Ignoring Bundle Size**: Not analyzing what's in the bundle

## Performance Checklist

- [ ] Use React DevTools Profiler to identify bottlenecks
- [ ] Implement code splitting for routes
- [ ] Virtualize long lists (100+ items)
- [ ] Memoize expensive computations with useMemo
- [ ] Memoize callbacks passed to memoized children
- [ ] Use lazy loading for images
- [ ] Optimize bundle size with tree shaking
- [ ] Use production build for deployment
- [ ] Monitor Core Web Vitals (LCP, FID, CLS)
- [ ] Consider Server Components (React 19 / Next.js)

## Tools and Libraries

### Performance Analysis
- React DevTools Profiler
- Chrome DevTools Performance
- Lighthouse
- Web Vitals library

### Optimization Libraries
- react-window / @tanstack/react-virtual (list virtualization)
- react-lazyload (lazy loading)
- bundle-analyzer (Vite/Webpack)

### Monitoring
- Sentry Performance Monitoring
- New Relic
- DataDog

## Additional Resources

- [React Docs - Performance Optimization](https://react.dev/learn/render-and-commit)
- [React Performance Optimization Techniques (Medium)](https://rajeshdhiman.medium.com/react-performance-optimization-techniques-memoization-lazy-loading-and-more-d1d9ddefca84)
- [React Memo vs useMemo (Saeloun)](https://blog.saeloun.com/2024/02/15/memo-vs-usememo-when-to-use-each-for-better-react-performance/)
- [Beyond React.memo (GitHub)](https://cekrem.github.io/posts/beyond-react-memo-smarter-performance-optimization/)
- [React 19 Memoization Changes](https://dev.to/joodi/react-19-memoization-is-usememo-usecallback-no-longer-necessary-3ifn)

## Next Steps

- Review [HOOKS_PATTERNS.md](./HOOKS_PATTERNS.md) for useMemo/useCallback details
- See [TESTING_REACT.md](./TESTING_REACT.md) for performance testing
- Check [ANTIPATTERNS.md](./ANTIPATTERNS.md) for performance anti-patterns
