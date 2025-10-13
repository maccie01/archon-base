# TypeScript with React Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: React Official Docs, React TypeScript Cheatsheet, Web Research (SitePoint, Medium, Kodaps)

## Overview

TypeScript provides static typing for React applications, catching errors at compile-time and improving developer experience. This document covers typing components, props, hooks, and advanced patterns.

## Core Principles

1. **Type Over Interface for Props**: Use `type` for consistency and better unions
2. **Avoid `any`**: Use `unknown` or proper types instead
3. **Leverage Type Inference**: Let TypeScript infer when obvious
4. **Use Generics for Reusability**: Create flexible, type-safe components
5. **Enable Strict Mode**: Use `strict: true` in tsconfig.json

## Patterns

### Pattern 1: Typing Component Props

**When to use**: For all components with props

**How to implement**: Define type/interface for props

**Example skeleton**:
```typescript
// TODO: Add example code
// Using type (recommended)
type ButtonProps = {
  label: string
  onClick: () => void
  variant?: 'primary' | 'secondary'
  disabled?: boolean
}

const Button = ({ label, onClick, variant = 'primary', disabled = false }: ButtonProps) => {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  )
}

// With children
type CardProps = {
  title: string
  children: React.ReactNode
}

const Card = ({ title, children }: CardProps) => (
  <div>
    <h2>{title}</h2>
    <div>{children}</div>
  </div>
)

// Extending HTML attributes
type InputProps = React.InputHTMLAttributes<HTMLInputElement> & {
  label: string
  error?: string
}

const Input = ({ label, error, ...props }: InputProps) => (
  <div>
    <label>{label}</label>
    <input {...props} />
    {error && <span>{error}</span>}
  </div>
)
```

**References**:
- [React TypeScript Cheatsheet - Props](https://react-typescript-cheatsheet.netlify.app/docs/basic/getting-started/basic_type_example/)

### Pattern 2: React.FC vs Function Declaration

**When to use**: Prefer function declarations in modern React

**Example skeleton**:
```typescript
// TODO: Add example code
// ❌ Not recommended: React.FC is verbose and has issues
const Component: React.FC<Props> = ({ children }) => {
  return <div>{children}</div>
}

// ✅ Recommended: Direct function declaration
type ComponentProps = {
  title: string
  children: React.ReactNode
}

const Component = ({ title, children }: ComponentProps) => {
  return (
    <div>
      <h1>{title}</h1>
      {children}
    </div>
  )
}

// Or with explicit return type
const Component = ({ title, children }: ComponentProps): JSX.Element => {
  return <div>{title}</div>
}
```

**Why avoid React.FC?**:
- Implicit children (confusing)
- More verbose
- Community moving away from it

### Pattern 3: Typing Hooks

**useState**:
```typescript
// TODO: Add example code
// Type inference works
const [count, setCount] = useState(0) // number
const [name, setName] = useState('') // string

// Explicit type with union or complex types
const [user, setUser] = useState<User | null>(null)

// With interface
interface User {
  id: number
  name: string
}
const [user, setUser] = useState<User | null>(null)
```

**useRef**:
```typescript
// TODO: Add example code
// DOM reference
const inputRef = useRef<HTMLInputElement>(null)
inputRef.current?.focus()

// Mutable value
const countRef = useRef<number>(0)
countRef.current = 5
```

**useEffect**:
```typescript
// TODO: Add example code
useEffect(() => {
  // Cleanup function is inferred
  const subscription = subscribe()
  return () => subscription.unsubscribe()
}, [])
```

**useCallback**:
```typescript
// TODO: Add example code
// Specify parameter types
const handleClick = useCallback((id: number) => {
  console.log(id)
}, [])

// With event handlers
const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
  setValue(e.target.value)
}, [])
```

**useReducer**:
```typescript
// TODO: Add example code
type State = { count: number }
type Action = { type: 'increment' } | { type: 'decrement' } | { type: 'reset' }

const reducer = (state: State, action: Action): State => {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 }
    case 'decrement':
      return { count: state.count - 1 }
    case 'reset':
      return { count: 0 }
  }
}

const [state, dispatch] = useReducer(reducer, { count: 0 })
```

**References**:
- [React TypeScript - How to Type Hooks](https://devtrium.com/posts/react-typescript-how-to-type-hooks)

### Pattern 4: Event Handlers

**When to use**: For all event handlers

**Example skeleton**:
```typescript
// TODO: Add example code
// Form events
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault()
}

const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setValue(e.target.value)
}

// Mouse events
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
  console.log(e.currentTarget)
}

// Keyboard events
const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
  if (e.key === 'Enter') {
    submit()
  }
}

// Generic event handler
const handleEvent = (e: React.SyntheticEvent) => {
  e.preventDefault()
}
```

**Common Event Types**:
- `React.FormEvent<HTMLFormElement>` - form submit
- `React.ChangeEvent<HTMLInputElement>` - input change
- `React.MouseEvent<HTMLButtonElement>` - click events
- `React.KeyboardEvent<HTMLInputElement>` - keyboard events
- `React.FocusEvent<HTMLInputElement>` - focus/blur

### Pattern 5: Generic Components

**When to use**: For reusable components that work with multiple types

**Example skeleton**:
```typescript
// TODO: Add example code
// Generic list component
type ListProps<T> = {
  items: T[]
  renderItem: (item: T) => React.ReactNode
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={index}>{renderItem(item)}</li>
      ))}
    </ul>
  )
}

// Usage with type inference
<List
  items={users}
  renderItem={(user) => <span>{user.name}</span>}
/>

// Generic select component
type SelectProps<T> = {
  options: T[]
  getLabel: (option: T) => string
  getValue: (option: T) => string
  onChange: (value: T) => void
}

function Select<T>({ options, getLabel, getValue, onChange }: SelectProps<T>) {
  return (
    <select onChange={(e) => {
      const option = options.find(o => getValue(o) === e.target.value)
      if (option) onChange(option)
    }}>
      {options.map((option) => (
        <option key={getValue(option)} value={getValue(option)}>
          {getLabel(option)}
        </option>
      ))}
    </select>
  )
}
```

**References**:
- [TypeScript Generics for React Developers](https://www.developerway.com/posts/typescript-generics-for-react-developers)

### Pattern 6: Typing Context

**When to use**: For all Context usage

**Example skeleton**:
```typescript
// TODO: Add example code
type ThemeContextType = {
  theme: 'light' | 'dark'
  toggleTheme: () => void
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

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

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (context === undefined) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}
```

### Pattern 7: Utility Types

**ComponentProps**: Extract props from existing component
```typescript
// TODO: Add example code
type ButtonProps = React.ComponentProps<'button'>
type CustomButtonProps = React.ComponentProps<typeof CustomButton>
```

**PropsWithChildren**: Add children automatically
```typescript
// TODO: Add example code
type CardProps = React.PropsWithChildren<{
  title: string
}>
```

**Omit/Pick**: Modify existing types
```typescript
// TODO: Add example code
type UserFormProps = Omit<User, 'id' | 'createdAt'>
type UserPreview = Pick<User, 'id' | 'name' | 'email'>
```

**Partial/Required**: Make all fields optional/required
```typescript
// TODO: Add example code
type PartialUser = Partial<User>
type RequiredUser = Required<User>
```

### Pattern 8: Typing Custom Hooks

**When to use**: For all custom hooks

**Example skeleton**:
```typescript
// TODO: Add example code
// Return tuple
function useToggle(initialValue: boolean): [boolean, () => void] {
  const [value, setValue] = useState(initialValue)
  const toggle = useCallback(() => setValue(v => !v), [])
  return [value, toggle]
}

// Return object
function useFetch<T>(url: string): {
  data: T | null
  isLoading: boolean
  error: Error | null
} {
  const [data, setData] = useState<T | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    // fetch logic
  }, [url])

  return { data, isLoading, error }
}

// Usage with type inference
const { data, isLoading } = useFetch<User[]>('/api/users')
```

## TypeScript Configuration

**tsconfig.json for React**:
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

## Common Mistakes

1. **Using `any`**: Defeats purpose of TypeScript; use `unknown` instead
2. **Not Using Strict Mode**: Missing many type-safety benefits
3. **Over-typing**: TypeScript can infer many types
4. **Using `React.FC`**: Community has moved away from it
5. **Not Typing Event Handlers**: Use specific React event types
6. **Forgetting `children` Type**: Use `React.ReactNode`
7. **Type Assertions Overuse**: Use type guards instead of `as`

## Type vs Interface

**Use `type` for**:
- Component props
- Union types
- Intersection types
- Consistency across codebase

**Use `interface` for**:
- API contracts
- When you need declaration merging
- Object-oriented patterns

**In React, prefer `type`** for props and most use cases.

## Additional Resources

- [React Official TypeScript Documentation](https://react.dev/learn/typescript)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- [TypeScript with React Best Practices (SitePoint)](https://www.sitepoint.com/react-with-typescript-best-practices/)
- [Best Practices for TypeScript with React (Medium)](https://medium.com/@mkare/best-practices-for-using-typescript-with-react-bad13d851143)
- [React TypeScript Guide (Kodaps)](https://www.kodaps.dev/en/blog/using-react-with-typescript-a-comprehensive-guide)

## Next Steps

- Review [FORMS_VALIDATION.md](./FORMS_VALIDATION.md) for form typing with Zod
- See [HOOKS_PATTERNS.md](./HOOKS_PATTERNS.md) for typing hooks
- Check [COMPONENT_PATTERNS.md](./COMPONENT_PATTERNS.md) for typed component patterns
