# Research Result: React Component Patterns

# React Component Patterns

A comprehensive guide to essential component patterns in React 18+ with TypeScript, focusing on reusability, maintainability, and type safety.

## Component Composition Patterns

### 1. Basic Composition with Children

Component composition allows you to build complex UIs by combining simpler components. The `children` prop is the foundation of composition in React.

```tsx
interface ContainerProps {
  className?: string;
  children: React.ReactNode;
}

const Container: React.FC<ContainerProps> = ({ className = '', children }) => {
  return (
    
      {children}
    
  );
};

// Usage
const App = () => (
  <Container className="main-container">
    <h1>Welcome</h1>
    <p>This content is composed inside the container.</p>
  </Container>
);
```

### 2. Layout Composition Pattern

Create flexible layouts by composing multiple slot-based components:

```tsx
interface LayoutProps {
  header: React.ReactNode;
  sidebar: React.ReactNode;
  content: React.ReactNode;
  footer?: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ header, sidebar, content, footer }) => {
  return (
    
      <header className="layout-header">{header}</header>
      
        <aside className="layout-sidebar">{sidebar}</aside>
        <main className="layout-content">{content}</main>
      
      {footer && <footer className="layout-footer">{footer}</footer>}
    
  );
};

// Usage
const App = () => (
  <Layout
    header={<Navigation />}
    sidebar={<Sidebar />}
    content={<MainContent />}
    footer={<Footer />}
  />
);
```

## Props vs Children Patterns

### 3. Flexible Component with Both Props and Children

```tsx
interface CardProps {
  title: string;
  variant?: 'default' | 'elevated' | 'outlined';
  actions?: React.ReactNode;
  children: React.ReactNode;
}

const Card: React.FC<CardProps> = ({ 
  title, 
  variant = 'default', 
  actions, 
  children 
}) => {
  const getVariantClass = () => {
    switch (variant) {
      case 'elevated': return 'card-elevated';
      case 'outlined': return 'card-outlined';
      default: return 'card-default';
    }
  };

  return (
    
      
        <h3 className="card-title">{title}</h3>
        {actions && {actions}}
      
      
        {children}
      
    
  );
};
```

## Controlled vs Uncontrolled Components

### 4. Controlled Input Component

Controlled components have their state managed by React, making them predictable and easy to test:

```tsx
interface ControlledInputProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  type?: 'text' | 'email' | 'password';
  error?: string;
}

const ControlledInput: React.FC<ControlledInputProps> = ({
  value,
  onChange,
  placeholder,
  type = 'text',
  error
}) => {
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    onChange(event.target.value);
  };

  return (
    
      <input
        type={type}
        value={value}
        onChange={handleChange}
        placeholder={placeholder}
        className={`input ${error ? 'input-error' : ''}`}
        aria-invalid={!!error}
        aria-describedby={error ? 'input-error' : undefined}
      />
      {error && (
        
          {error}
        
      )}
    
  );
};

// Usage with state management
const FormExample = () => {
  const [email, setEmail] = useState('');
  const [emailError, setEmailError] = useState('');

  const validateEmail = (value: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) {
      setEmailError('Please enter a valid email address');
    } else {
      setEmailError('');
    }
  };

  const handleEmailChange = (value: string) => {
    setEmail(value);
    validateEmail(value);
  };

  return (
    <ControlledInput
      value={email}
      onChange={handleEmailChange}
      type="email"
      placeholder="Enter your email"
      error={emailError}
    />
  );
};
```

### 5. Uncontrolled Component with Refs

Uncontrolled components manage their own state internally:

```tsx
interface UncontrolledInputProps {
  defaultValue?: string;
  onSubmit?: (value: string) => void;
  placeholder?: string;
}

const UncontrolledInput: React.FC<UncontrolledInputProps> = ({
  defaultValue = '',
  onSubmit,
  placeholder
}) => {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (inputRef.current && onSubmit) {
      onSubmit(inputRef.current.value);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        ref={inputRef}
        defaultValue={defaultValue}
        placeholder={placeholder}
        className="input"
      />
      
    </form>
  );
};
```

## Compound Components

### 6. Accordion Compound Component

Compound components work together to form a cohesive interface:

```tsx
interface AccordionContextType {
  openItems: Set<string>;
  toggleItem: (id: string) => void;
  allowMultiple: boolean;
}

const AccordionContext = createContext<AccordionContextType | undefined>(undefined);

interface AccordionProps {
  allowMultiple?: boolean;
  defaultOpenItems?: string[];
  children: React.ReactNode;
}

const Accordion: React.FC<AccordionProps> & {
  Item: React.FC<AccordionItemProps>;
  Header: React.FC<AccordionHeaderProps>;
  Content: React.FC<AccordionContentProps>;
} = ({ allowMultiple = false, defaultOpenItems = [], children }) => {
  const [openItems, setOpenItems] = useState(new Set(defaultOpenItems));

  const toggleItem = useCallback((id: string) => {
    setOpenItems(prev => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        if (!allowMultiple) {
          newSet.clear();
        }
        newSet.add(id);
      }
      return newSet;
    });
  }, [allowMultiple]);

  return (
    <AccordionContext.Provider value={{ openItems, toggleItem, allowMultiple }}>
      
        {children}
      
    </AccordionContext.Provider>
  );
};

interface AccordionItemProps {
  id: string;
  children: React.ReactNode;
}

const AccordionItem: React.FC<AccordionItemProps> = ({ id, children }) => {
  return (
    
      {children}
    
  );
};

interface AccordionHeaderProps {
  children: React.ReactNode;
}

const AccordionHeader: React.FC<AccordionHeaderProps> = ({ children }) => {
  const context = useContext(AccordionContext);
  const itemElement = useRef<HTMLDivElement>(null);
  
  if (!context) {
    throw new Error('AccordionHeader must be used within Accordion');
  }

  const handleClick = () => {
    const itemId = itemElement.current?.closest('[data-item-id]')?.getAttribute('data-item-id');
    if (itemId) {
      context.toggleItem(itemId);
    }
  };

  return (
    
  );
};

interface AccordionContentProps {
  children: React.ReactNode;
}

const AccordionContent: React.FC<AccordionContentProps> = ({ children }) => {
  const context = useContext(AccordionContext);
  const itemElement = useRef<HTMLDivElement>(null);

  if (!context) {
    throw new Error('AccordionContent must be used within Accordion');
  }

  const itemId = itemElement.current?.closest('[data-item-id]')?.getAttribute('data-item-id');
  const isOpen = itemId ? context.openItems.has(itemId) : false;

  return (
    
      {children}
    
  );
};

Accordion.Item = AccordionItem;
Accordion.Header = AccordionHeader;
Accordion.Content = AccordionContent;

// Usage
const AccordionExample = () => (
  <Accordion allowMultiple defaultOpenItems={['item1']}>
    <Accordion.Item id="item1">
      <Accordion.Header>Section 1</Accordion.Header>
      <Accordion.Content>
        <p>Content for section 1</p>
      </Accordion.Content>
    </Accordion.Item>
    <Accordion.Item id="item2">
      <Accordion.Header>Section 2</Accordion.Header>
      <Accordion.Content>
        <p>Content for section 2</p>
      </Accordion.Content>
    </Accordion.Item>
  </Accordion>
);
```

## Render Props Pattern

### 7. Data Fetcher with Render Props

```tsx
interface DataFetcherProps<T> {
  url: string;
  render: (state: {
    data: T | null;
    loading: boolean;
    error: string | null;
    retry: () => void;
  }) => React.ReactNode;
}

function DataFetcher<T>({ url, render }: DataFetcherProps<T>) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return <>{render({ data, loading, error, retry: fetchData })}</>;
}

// Usage
interface User {
  id: number;
  name: string;
  email: string;
}

const UserProfile = () => (
  <DataFetcher<User>
    url="/api/user/1"
    render={({ data, loading, error, retry }) => {
      if (loading) return Loading user...;
      if (error) return (
        
          Error: {error}
          
        
      );
      if (!data) return No user found;
    
      return (
        
          <h2>{data.name}</h2>
          <p>{data.email}</p>
        
      );
    }}
  />
);
```

## Higher-Order Components (HOCs)

### 8. Authentication HOC

```tsx
interface WithAuthProps {
  user: { id: string; name: string } | null;
  isAuthenticated: boolean;
}

function withAuth<P extends object>(
  WrappedComponent: React.ComponentType<P & WithAuthProps>
) {
  return function AuthenticatedComponent(props: P) {
    const [user, setUser] = useState<{ id: string; name: string } | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
      // Simulate auth check
      const checkAuth = async () => {
        try {
          const response = await fetch('/api/auth/me');
          if (response.ok) {
            const userData = await response.json();
            setUser(userData);
          }
        } catch (error) {
          console.error('Auth check failed:', error);
        } finally {
          setLoading(false);
        }
      };

      checkAuth();
    }, []);

    if (loading) {
      return Checking authentication...;
    }

    return (
      <WrappedComponent
        {...props}
        user={user}
        isAuthenticated={!!user}
      />
    );
  };
}

// Usage
interface DashboardProps extends WithAuthProps {
  title: string;
}

const Dashboard: React.FC<DashboardProps> = ({ title, user, isAuthenticated }) => {
  if (!isAuthenticated) {
    return Please log in to access the dashboard.;
  }

  return (
    
      <h1>{title}</h1>
      <p>Welcome, {user?.name}!</p>
    
  );
};

const AuthenticatedDashboard = withAuth(Dashboard);
```

## Error Boundaries

### 9. Error Boundary Implementation

```tsx
interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
  errorInfo?: ErrorInfo;
}

interface ErrorBoundaryProps {
  fallback?: React.ComponentType<{ error: Error; resetError: () => void }>;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
  children: React.ReactNode;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.setState({ errorInfo });
  
    // Log error to monitoring service
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }
  
    console.error('Error caught by boundary:', error, errorInfo);
  }

  resetError = () => {
    this.setState({ hasError: false, error: undefined, errorInfo: undefined });
  };

  render() {
    if (this.state.hasError) {
      const FallbackComponent = this.props.fallback || DefaultErrorFallback;
      return (
        <FallbackComponent
          error={this.state.error!}
          resetError={this.resetError}
        />
      );
    }

    return this.props.children;
  }
}

const DefaultErrorFallback: React.FC<{ error: Error; resetError: () => void }> = ({
  error,
  resetError
}) => (
  
    <h2>Something went wrong</h2>
    <p>{error.message}</p>
    
  
);

// Usage
const App = () => (
  <ErrorBoundary
    fallback={CustomErrorFallback}
    onError={(error, errorInfo) => {
      // Send to monitoring service
      console.error('Application error:', { error, errorInfo });
    }}
  >
    <Header />
    <MainContent />
    <Footer />
  </ErrorBoundary>
);
```

## Suspense and Lazy Loading

### 10. Lazy Loading with Suspense

```tsx
// Lazy load components
const Dashboard = lazy(() => import('./components/Dashboard'));
const Profile = lazy(() => import('./components/Profile'));
const Settings = lazy(() => import('./components/Settings'));

// Loading component
const LoadingSpinner: React.FC = () => (
  
    
    <p>Loading...</p>
  
);

// Route-based code splitting
const App: React.FC = () => {
  return (
    <Router>
      <ErrorBoundary>
        <Navigation />
        <Suspense fallback={<LoadingSpinner />}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Suspense>
      </ErrorBoundary>
    </Router>
  );
};

// Component-level lazy loading
interface LazyImageProps {
  src: string;
  alt: string;
  className?: string;
}

const LazyImage: React.FC<LazyImageProps> = ({ src, alt, className }) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [isInView, setIsInView] = useState(false);
  const imgRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsInView(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    
      {isInView && (
        <>
          <img
            src={src}
            alt={alt}
            onLoad={() => setIsLoaded(true)}
            style={{ opacity: isLoaded ? 1 : 0 }}
            className="lazy-image"
          />
          {!isLoaded && Loading...}
        </>
      )}
    
  );
};
```

## Portal Usage

### 11. Modal with Portal

```tsx
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, title, children }) => {
  const [portalContainer, setPortalContainer] = useState<HTMLElement | null>(null);

  useEffect(() => {
    // Create or get portal container
    let container = document.getElementById('modal-portal');
    if (!container) {
      container = document.createElement('div');
      container.id = 'modal-portal';
      document.body.appendChild(container);
    }
    setPortalContainer(container);

    return () => {
      // Cleanup on unmount if container is empty
      if (container && !container.hasChildNodes()) {
        document.body.removeChild(container);
      }
    };
  }, []);

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  // Handle escape key
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isOpen, onClose]);

  if (!isOpen || !portalContainer) return null;

  return createPortal(
    
       e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-labelledby={title ? 'modal-title' : undefined}
      >
        
          {title && <h2 id="modal-title">{title}</h2>}
          
        
        
          {children}
        
      
    ,
    portalContainer
  );
};

// Usage
const ModalExample = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    
      

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Example Modal"
      >
        <p>This modal is rendered using React Portal!</p>
        
      </Modal>
    
  );
};
```

## Ref Forwarding

### 12. Input Component with Ref Forwarding

```tsx
interface InputProps {
  label?: string;
  error?: string;
  className?: string;
}

type InputRef = HTMLInputElement;

const Input = forwardRef<InputRef, InputProps & React.InputHTMLAttributes<HTMLInputElement>>(
  ({ label, error, className = '', ...inputProps }, ref) => {
    const inputId = useId();
    const errorId = useId();

    return (
      
        {label && (
          <label htmlFor={inputId} className="input-label">
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          className={`input ${error ? 'input-error' : ''}`}
          aria-invalid={!!error}
          aria-describedby={error ? errorId : undefined}
          {...inputProps}
        />
        {error && (
          
            {error}
          
        )}
      
    );
  }
);

Input.displayName = 'Input';

// Usage with imperative methods
const FormWithImperativeInput = () => {
  const inputRef = useRef<HTMLInputElement>(null);

  const focusInput = () => {
    inputRef.current?.focus();
  };

  const clearInput = () => {
    if (inputRef.current) {
      inputRef.current.value = '';
    }
  };

  return (
    <form>
      <Input
        ref={inputRef}
        label="Username"
        placeholder="Enter username"
      />
      
        
        
      
    </form>
  );
};
```

## Performance Considerations

### 13. Memoization Patterns

```tsx
interface ExpensiveListProps {
  items: Array<{ id: string; name: string; value: number }>;
  onItemClick: (id: string) => void;
}

// Memoized list item component
interface ListItemProps {
  item: { id: string; name: string; value: number };
  onItemClick: (id: string) => void;
}

const ListItem = memo<ListItemProps>(({ item, onItemClick }) => {
  console.log(`Rendering item: ${item.id}`);
  
  const handleClick = useCallback(() => {
    onItemClick(item.id);
  }, [item.id, onItemClick]);

  return (
    
      <h3>{item.name}</h3>
      ${item.value}
    
  );
});

ListItem.displayName = 'ListItem';

// Memoized list component
const ExpensiveList = memo<ExpensiveListProps>(({ items, onItemClick }) => {
  return (
    
      {items.map(item => (
        <ListItem
          key={item.id}
          item={item}
          onItemClick={onItemClick}
        />
      ))}
    
  );
});

ExpensiveList.displayName = 'ExpensiveList';
```

## Testing Examples

### 14. Component Testing with React Testing Library

```tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ControlledInput } from './ControlledInput';

describe('ControlledInput', () => {
  it('renders with initial value', () => {
    render(
      <ControlledInput
        value="test value"
        onChange={() => {}}
        placeholder="Enter text"
      />
    );

    expect(screen.getByDisplayValue('test value')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter text')).toBeInTheDocument();
  });

  it('calls onChange when user types', async () => {
    const user = userEvent.setup();
    const mockOnChange = jest.fn();

    render(
      <ControlledInput
        value=""
        onChange={mockOnChange}
        placeholder="Enter text"
      />
    );

    const input = screen.getByRole('textbox');
    await user.type(input, 'hello');

    expect(mockOnChange).toHaveBeenCalledTimes(5);
    expect(mockOnChange).toHaveBeenLastCalledWith('hello');
  });

  it('displays error message', () => {
    render(
      <ControlledInput
        value=""
        onChange={() => {}}
        error="This field is required"
      />
    );

    const errorMessage = screen.getByRole('alert');
    expect(errorMessage).toHaveTextContent('This field is required');
    expect(screen.getByRole('textbox')).toHaveAttribute('aria-invalid', 'true');
  });
});

describe('Modal', () => {
  it('renders when open', () => {
    render(
      <Modal isOpen={true} onClose={() => {}} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    expect(screen.getByRole('dialog')).toBeInTheDocument();
    expect(screen.getByText('Test Modal')).toBeInTheDocument();
    expect(screen.getByText('Modal content')).toBeInTheDocument();
  });

  it('does not render when closed', () => {
    render(
      <Modal isOpen={false} onClose={() => {}} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });

  it('calls onClose when close button is clicked', async () => {
    const user = userEvent.setup();
    const mockOnClose = jest.fn();

    render(
      <Modal isOpen={true} onClose={mockOnClose} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    const closeButton = screen.getByLabelText('Close modal');
    await user.click(closeButton);

    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });
});
```

## Summary

These React component patterns provide a solid foundation for building maintainable and scalable applications:

- **Composition patterns** enable flexible UI construction
- **Controlled/uncontrolled components** offer different state management approaches
- **Compound components** create cohesive, reusable UI elements
- **Render props and HOCs** enable code sharing and logic reuse
- **Error boundaries** provide graceful error handling
- **Suspense and lazy loading** improve performance through code splitting
- **Portals** enable rendering outside component hierarchy
- **Ref forwarding** allows direct DOM access when needed
- **Memoization** optimizes rendering performance
- **Comprehensive testing** ensures reliability and maintainability

Choose the appropriate pattern based on your specific use case, keeping in mind factors like reusability, performance, type safety, and testing requirements.