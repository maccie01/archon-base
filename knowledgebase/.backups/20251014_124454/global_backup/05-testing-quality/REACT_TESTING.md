# React Testing Library Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Testing Library docs, Kent C. Dodds best practices, React testing patterns

## Overview

React Testing Library helps you test React components in a way that resembles how users interact with your application. It encourages good testing practices by focusing on user behavior rather than implementation details.

## Core Principles

1. **Test User Behavior** - Test how users interact with components
2. **Avoid Implementation Details** - Don't test state, props, or component internals
3. **Accessibility First** - Use accessible queries to find elements
4. **User-Centric** - Think from the user's perspective
5. **Confidence Over Coverage** - Focus on critical user paths

## Setup

### Installation
```bash
npm install -D @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

### Setup File
```typescript
// src/test/setup.ts
import { expect, afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'
import * as matchers from '@testing-library/jest-dom/matchers'

expect.extend(matchers)

afterEach(() => {
  cleanup()
})
```

### Test Utils
```typescript
// TODO: Add renderWithProviders utility
// Include Router, Redux, Theme providers
```

## Querying Elements

### Query Priority (Use in This Order)

1. **Accessible to Everyone**
   - `getByRole` - Best for most elements
   - `getByLabelText` - Form elements
   - `getByPlaceholderText` - Alternative for inputs
   - `getByText` - Non-interactive elements
   - `getByDisplayValue` - Current value of form elements

2. **Semantic Queries**
   - `getByAltText` - Images
   - `getByTitle` - Elements with title attribute

3. **Test IDs (Last Resort)**
   - `getByTestId` - When no better option exists

### Query Variants

**getBy*** - Returns element, throws if not found or multiple found
```typescript
const button = screen.getByRole('button', { name: /submit/i })
```

**queryBy*** - Returns element or null, doesn't throw
```typescript
const error = screen.queryByText(/error/i)
expect(error).not.toBeInTheDocument()
```

**findBy*** - Returns promise, waits for element to appear
```typescript
const heading = await screen.findByText(/welcome/i)
```

**getAllBy***, **queryAllBy***, **findAllBy*** - Return arrays
```typescript
const items = screen.getAllByRole('listitem')
```

## Basic Component Testing

### Simple Component
```typescript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { Button } from './Button'

describe('Button', () => {
  it('should render with text', () => {
    render(<Button>Click me</Button>)

    expect(screen.getByRole('button', { name: /click me/i }))
      .toBeInTheDocument()
  })

  it('should be disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>)

    expect(screen.getByRole('button')).toBeDisabled()
  })
})
```

### Component with Props
```typescript
// TODO: Add component with various props testing
```

## User Interactions

### User Event (Preferred)
```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

it('should handle click', async () => {
  const user = userEvent.setup()
  const handleClick = vi.fn()

  render(<Button onClick={handleClick}>Click</Button>)

  await user.click(screen.getByRole('button'))

  expect(handleClick).toHaveBeenCalledTimes(1)
})
```

### Common User Actions
```typescript
// TODO: Add examples for:
// - Typing in input
// - Selecting from dropdown
// - Checking checkbox
// - Hovering
// - Double click
// - Keyboard navigation
```

### FireEvent (Legacy, Avoid When Possible)
```typescript
// Only use if userEvent doesn't support the interaction
import { fireEvent } from '@testing-library/react'

fireEvent.click(button)
```

## Testing Forms

### Form Submission
```typescript
// TODO: Add complete form testing example
// Input, validation, submission, error handling
```

### Form Validation
```typescript
// TODO: Add validation testing
// Required fields, format validation, async validation
```

### Controlled Components
```typescript
// TODO: Add controlled input testing
```

## Testing Async Components

### Loading States
```typescript
it('should show loading state', async () => {
  render(<AsyncComponent />)

  expect(screen.getByText(/loading/i)).toBeInTheDocument()

  await waitForElementToBeRemoved(() => screen.queryByText(/loading/i))

  expect(screen.getByText(/loaded data/i)).toBeInTheDocument()
})
```

### API Data Fetching
```typescript
// TODO: Add MSW + React Testing Library example
```

### Error States
```typescript
// TODO: Add error state testing
```

## Testing Hooks

### Custom Hooks
```typescript
import { renderHook, waitFor } from '@testing-library/react'

it('should return data from hook', () => {
  const { result } = renderHook(() => useCustomHook())

  expect(result.current.data).toBe(null)

  await waitFor(() => {
    expect(result.current.data).not.toBe(null)
  })
})
```

### Hook with Props
```typescript
// TODO: Add hook with props example
```

### Hook Rerendering
```typescript
// TODO: Add hook rerender example
```

## Testing Context

### Component with Context
```typescript
// TODO: Add context provider testing
// Custom render with providers
```

### Multiple Contexts
```typescript
// TODO: Add multiple context providers example
```

## Testing Router

### Component with React Router
```typescript
// TODO: Add Router testing example
// Mock routes, navigation, params
```

### Testing Navigation
```typescript
// TODO: Add navigation testing
```

## Testing Redux/State Management

### Component with Redux
```typescript
// TODO: Add Redux + RTL example
// Mock store, dispatch testing
```

### Testing Actions
```typescript
// TODO: Add action testing
```

## Accessibility Testing

### Aria Roles
```typescript
it('should be accessible', () => {
  render(<Component />)

  const button = screen.getByRole('button', { name: /submit/i })
  expect(button).toHaveAccessibleName('Submit')
})
```

### Keyboard Navigation
```typescript
// TODO: Add keyboard navigation testing
// Tab, Enter, Escape, Arrow keys
```

### Screen Reader Testing
```typescript
// TODO: Add screen reader accessibility testing
```

## Custom Matchers

### Common jest-dom Matchers
```typescript
expect(element).toBeInTheDocument()
expect(element).toBeVisible()
expect(element).toBeDisabled()
expect(element).toHaveClass('active')
expect(element).toHaveAttribute('href', '/path')
expect(element).toHaveTextContent('Hello')
expect(element).toHaveValue('input value')
```

### Custom Matcher
```typescript
// TODO: Add custom matcher example
```

## Mocking

### Mocking Child Components
```typescript
vi.mock('./ChildComponent', () => ({
  ChildComponent: () => <div>Mocked Child</div>
}))
```

### Mocking API Calls
```typescript
// TODO: Add MSW integration example
```

### Mocking External Libraries
```typescript
// TODO: Add external library mocking
// react-router, react-query, etc.
```

## Snapshot Testing

### Component Snapshots
```typescript
it('should match snapshot', () => {
  const { container } = render(<Component />)
  expect(container).toMatchSnapshot()
})
```

### When to Use Snapshots
- Complex UI structures
- Generated markup
- Regression detection

### When NOT to Use Snapshots
- Simple components (use explicit assertions)
- Frequently changing UI
- Dynamic content

## Performance Testing

### Render Performance
```typescript
// TODO: Add performance testing example
// React.memo, useMemo, useCallback testing
```

### Unnecessary Rerenders
```typescript
// TODO: Add rerender detection testing
```

## Common Patterns

### Pattern 1: Testing Modal Dialogs
```typescript
// TODO: Add modal testing pattern
// Open, close, interactions, backdrop
```

### Pattern 2: Testing Dropdown/Select
```typescript
// TODO: Add dropdown testing
```

### Pattern 3: Testing Lists with Actions
```typescript
// TODO: Add list testing
// Filter, sort, pagination, item actions
```

### Pattern 4: Testing File Upload
```typescript
// TODO: Add file upload testing
```

## Best Practices

1. **Use Semantic HTML** - Proper roles make testing easier
2. **Query by Role First** - Most accessible and robust
3. **Use User Event** - More realistic than fireEvent
4. **Avoid Test IDs** - Use only when no semantic option exists
5. **Test User Workflows** - Not implementation details
6. **Don't Test Third-Party Code** - Trust libraries work
7. **Keep Tests Simple** - Easy to understand and maintain
8. **Use Data-testid Sparingly** - Last resort for queries
9. **Mock External Dependencies** - APIs, third-party services
10. **Cleanup Automatically** - Use afterEach cleanup

## Anti-Patterns to Avoid

### 1. Testing Implementation Details
```typescript
// Bad - accessing state
expect(wrapper.state('count')).toBe(1)

// Good - testing user-visible behavior
expect(screen.getByText('Count: 1')).toBeInTheDocument()
```

### 2. Using Container Queries
```typescript
// Bad - querying container
const { container } = render(<Component />)
container.querySelector('.class-name')

// Good - using screen queries
screen.getByRole('button')
```

### 3. Waiting with Act Warnings
```typescript
// Bad - not properly handling async
render(<AsyncComponent />)
expect(screen.getByText('data')).toBeInTheDocument()

// Good - waiting for async operations
await screen.findByText('data')
```

## Testing Component Libraries

### Testing Shadcn/UI Components
```typescript
// TODO: Add Radix UI/Shadcn testing patterns
```

### Testing Material-UI Components
```typescript
// TODO: Add MUI testing patterns
```

## Debugging Tests

### Screen Debug
```typescript
import { render, screen } from '@testing-library/react'

it('test', () => {
  render(<Component />)
  screen.debug() // Prints DOM to console
})
```

### Debug Specific Element
```typescript
screen.debug(screen.getByRole('button'))
```

### Loggy Testing Playground
```typescript
import { logRoles } from '@testing-library/react'

const { container } = render(<Component />)
logRoles(container)
```

## Tools and Extensions

### Recommended Tools
- Testing Library Playground (testing-playground.com)
- React DevTools
- VS Code Testing Library snippets

### Browser Extensions
- Testing Playground Chrome extension

## Troubleshooting

### Common Errors

**Unable to find element**
- Check if element rendered
- Verify query is correct
- Check if async (use findBy)
- Use screen.debug()

**Act Warnings**
- Wrap state updates in act()
- Wait for async operations
- Use findBy* queries

**Multiple Elements Found**
- Make query more specific
- Use getAllBy* if intentional

## Additional Resources

- [TESTING_STRATEGY.md](./TESTING_STRATEGY.md) - Overall testing approach
- [VITEST_PATTERNS.md](./VITEST_PATTERNS.md) - Vitest configuration
- [E2E_TESTING.md](./E2E_TESTING.md) - End-to-end testing
- [Testing Library Documentation](https://testing-library.com/react)
- [Common Mistakes](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
