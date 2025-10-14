# React Error Handling Patterns

Created: 2025-10-13
Last Research: 2025-10-13
Sources: React Official Docs, Web Research (Medium, Refine, FreeCodeCamp)

## Overview

Error handling in React involves capturing JavaScript errors, managing error boundaries, handling async errors, and providing fallback UIs. React 18+ introduces enhanced error handling with Suspense integration.

## Core Principles

1. **Graceful Degradation**: Show fallback UI instead of crashing
2. **Error Boundaries for Component Trees**: Catch rendering errors
3. **Try-Catch for Async Operations**: Handle async errors in event handlers
4. **User-Friendly Messages**: Display helpful error messages
5. **Error Reporting**: Log errors to monitoring services

## Patterns

### Pattern 1: Error Boundary (Class Component)

**When to use**: To catch JavaScript errors in component tree

**How to implement**: Create class component with componentDidCatch

**Example skeleton**:
```typescript
// TODO: Add example code
import React, { Component, ErrorInfo, ReactNode } from 'react'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error?: Error
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log error to service
    console.error('Error caught by boundary:', error, errorInfo)
    // Send to error reporting service (Sentry, LogRocket, etc.)
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div role="alert">
          <h2>Something went wrong</h2>
          <details>
            <summary>Error details</summary>
            <pre>{this.state.error?.message}</pre>
          </details>
          <button onClick={() => this.setState({ hasError: false })}>
            Try again
          </button>
        </div>
      )
    }

    return this.props.children
  }
}

// Usage:
<ErrorBoundary fallback={<ErrorFallback />}>
  <MyComponent />
</ErrorBoundary>
```

**What Error Boundaries Catch**:
- Rendering errors
- Lifecycle method errors
- Constructor errors

**What They DON'T Catch**:
- Event handlers (use try-catch)
- Async code (setTimeout, promises)
- Server-side rendering errors
- Errors in the error boundary itself

**References**:
- [React Docs - Error Boundaries](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary)

### Pattern 2: react-error-boundary Library

**When to use**: For easier error boundary implementation with hooks

**How to implement**: Use ErrorBoundary component from library

**Example skeleton**:
```typescript
// TODO: Add example code
import { ErrorBoundary, useErrorHandler } from 'react-error-boundary'

// Error fallback component
function ErrorFallback({ error, resetErrorBoundary }: {
  error: Error
  resetErrorBoundary: () => void
}) {
  return (
    <div role="alert">
      <h2>Something went wrong</h2>
      <pre style={{ color: 'red' }}>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  )
}

// Usage:
<ErrorBoundary
  FallbackComponent={ErrorFallback}
  onError={(error, errorInfo) => {
    // Log to error reporting service
    logErrorToService(error, errorInfo)
  }}
  onReset={() => {
    // Reset app state
    resetAppState()
  }}
>
  <MyApp />
</ErrorBoundary>

// Using error handler hook in functional component
function MyComponent() {
  const handleError = useErrorHandler()

  async function fetchData() {
    try {
      const data = await api.getData()
      setData(data)
    } catch (error) {
      handleError(error) // Throws to nearest error boundary
    }
  }

  return <div>...</div>
}
```

**References**:
- [react-error-boundary GitHub](https://github.com/bvaughn/react-error-boundary)

### Pattern 3: Error Boundary with Suspense (React 18+)

**When to use**: For handling errors in Suspense boundaries

**How to implement**: Wrap Suspense with ErrorBoundary

**Example skeleton**:
```typescript
// TODO: Add example code
import { Suspense, lazy } from 'react'
import { ErrorBoundary } from 'react-error-boundary'

const LazyComponent = lazy(() => import('./LazyComponent'))

function App() {
  return (
    <ErrorBoundary fallback={<ErrorFallback />}>
      <Suspense fallback={<LoadingSpinner />}>
        <LazyComponent />
      </Suspense>
    </ErrorBoundary>
  )
}

// Nested boundaries for granular error handling
function FeatureSection() {
  return (
    <ErrorBoundary fallback={<FeatureError />}>
      <Suspense fallback={<FeatureLoading />}>
        <FeatureComponent />
      </Suspense>
    </ErrorBoundary>
  )
}
```

**References**:
- [React Docs - Suspense](https://react.dev/reference/react/Suspense)

### Pattern 4: Async Error Handling in Event Handlers

**When to use**: For errors in event handlers and async operations

**How to implement**: Use try-catch blocks

**Example skeleton**:
```typescript
// TODO: Add example code
function FormComponent() {
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setIsLoading(true)

    try {
      await api.submitForm(formData)
      // Success handling
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message)
      } else {
        setError('An unexpected error occurred')
      }
      // Optionally log to error service
      logError(err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {error && (
        <div role="alert" className="error">
          {error}
        </div>
      )}
      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  )
}
```

### Pattern 5: Error Handling with TanStack Query

**When to use**: For API call error handling with React Query

**How to implement**: Use error property from useQuery/useMutation

**Example skeleton**:
```typescript
// TODO: Add example code
import { useQuery, useMutation } from '@tanstack/react-query'

function UserList() {
  const { data, error, isError, isLoading, refetch } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
    retry: 3,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  })

  if (isLoading) return <LoadingSpinner />

  if (isError) {
    return (
      <div role="alert">
        <h2>Failed to load users</h2>
        <p>{error.message}</p>
        <button onClick={() => refetch()}>Try again</button>
      </div>
    )
  }

  return <ul>{data.map(user => <li key={user.id}>{user.name}</li>)}</ul>
}

// Mutation error handling
function CreateUser() {
  const mutation = useMutation({
    mutationFn: createUser,
    onError: (error) => {
      toast.error(`Failed to create user: ${error.message}`)
    },
    onSuccess: () => {
      toast.success('User created successfully')
    },
  })

  const handleSubmit = (data: UserData) => {
    mutation.mutate(data)
  }

  return (
    <form onSubmit={handleSubmit}>
      {mutation.isError && (
        <div role="alert">{mutation.error.message}</div>
      )}
      <button type="submit" disabled={mutation.isPending}>
        Create User
      </button>
    </form>
  )
}
```

**References**:
- [TanStack Query - Error Handling](https://tanstack.com/query/latest/docs/framework/react/guides/query-functions)

### Pattern 6: Global Error Handler

**When to use**: To catch all unhandled errors

**How to implement**: Add event listeners for unhandled errors

**Example skeleton**:
```typescript
// TODO: Add example code
// src/errorHandler.ts
export function setupGlobalErrorHandlers() {
  // Catch unhandled promise rejections
  window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason)
    // Log to error service
    logErrorToService(event.reason)
    event.preventDefault()
  })

  // Catch global errors
  window.addEventListener('error', (event) => {
    console.error('Global error:', event.error)
    logErrorToService(event.error)
  })
}

// In main.tsx/index.tsx
import { setupGlobalErrorHandlers } from './errorHandler'

setupGlobalErrorHandlers()
```

### Pattern 7: Custom Error Hook

**When to use**: To standardize error handling across components

**Example skeleton**:
```typescript
// TODO: Add example code
import { useState, useCallback } from 'react'

interface UseErrorReturn {
  error: Error | null
  setError: (error: Error | null) => void
  clearError: () => void
  withErrorHandling: <T>(
    fn: () => Promise<T>
  ) => Promise<T | undefined>
}

function useError(): UseErrorReturn {
  const [error, setError] = useState<Error | null>(null)

  const clearError = useCallback(() => setError(null), [])

  const withErrorHandling = useCallback(
    async <T,>(fn: () => Promise<T>): Promise<T | undefined> => {
      try {
        clearError()
        return await fn()
      } catch (err) {
        const error = err instanceof Error ? err : new Error('Unknown error')
        setError(error)
        logErrorToService(error)
        return undefined
      }
    },
    [clearError]
  )

  return { error, setError, clearError, withErrorHandling }
}

// Usage:
function MyComponent() {
  const { error, withErrorHandling } = useError()

  const fetchData = () => withErrorHandling(async () => {
    const data = await api.getData()
    setData(data)
  })

  return (
    <>
      {error && <ErrorMessage error={error} />}
      <button onClick={fetchData}>Load Data</button>
    </>
  )
}
```

## Error Reporting Services

### Popular Services
- **Sentry**: Most popular, comprehensive error tracking
- **LogRocket**: Error tracking + session replay
- **Bugsnag**: Real-time error monitoring
- **Rollbar**: Error monitoring and crash reporting

### Sentry Integration Example
```typescript
// TODO: Add example code
import * as Sentry from '@sentry/react'

Sentry.init({
  dsn: 'your-sentry-dsn',
  integrations: [
    new Sentry.BrowserTracing(),
    new Sentry.Replay(),
  ],
  tracesSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
})

// Wrap app with Sentry ErrorBoundary
<Sentry.ErrorBoundary fallback={<ErrorFallback />}>
  <App />
</Sentry.ErrorBoundary>
```

## Error Types and Handling

### Network Errors
```typescript
if (error.name === 'NetworkError') {
  return 'Please check your internet connection'
}
```

### Validation Errors
```typescript
if (error.status === 400) {
  return error.response.data.errors
}
```

### Authentication Errors
```typescript
if (error.status === 401) {
  redirectToLogin()
}
```

### Server Errors
```typescript
if (error.status >= 500) {
  return 'Server error. Please try again later.'
}
```

## Best Practices

1. **Multiple Error Boundaries**: Place boundaries at different levels for granular handling
2. **User-Friendly Messages**: Show helpful messages, not technical stack traces
3. **Reset Functionality**: Allow users to recover from errors
4. **Log All Errors**: Send errors to monitoring service
5. **Development vs Production**: Show detailed errors in dev, generic in production
6. **Retry Logic**: Implement automatic retry for transient failures
7. **Fallback UI**: Always provide meaningful fallback content

## Common Mistakes

1. **Single Error Boundary**: Only at root level, crashes entire app
2. **Not Handling Async Errors**: Forgetting try-catch in event handlers
3. **Exposing Stack Traces**: Showing technical details to users in production
4. **No Error Logging**: Not sending errors to monitoring service
5. **Ignoring Error State**: Not showing errors to users
6. **No Recovery Path**: Not providing way to retry or recover

## Development Tools

### React DevTools
- View error boundary state
- Track error origins

### Sentry Browser Extension
- View errors in real-time
- Link to Sentry dashboard

## Additional Resources

- [React Docs - Error Boundaries](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary)
- [react-error-boundary GitHub](https://github.com/bvaughn/react-error-boundary)
- [Suspense and Error Boundaries Explained](https://reetesh.in/blog/suspense-and-error-boundary-in-react-explained)
- [Error Handling in React (FreeCodeCamp)](https://www.freecodecamp.org/news/react-suspense/)
- [Next.js 15 Error Boundaries (Medium)](https://medium.com/@sureshdotariya/leveraging-suspense-and-error-boundaries-in-next-js-034aff10df4f)

## Next Steps

- Review [TESTING_REACT.md](./TESTING_REACT.md) for testing error states
- See [ACCESSIBILITY.md](./ACCESSIBILITY.md) for accessible error messages
- Check [ANTIPATTERNS.md](./ANTIPATTERNS.md) for error handling anti-patterns
