# Archon UI Authentication Code Examples

Date Created: 2025-10-15

## Complete Implementation Overview

This document provides code examples and explanations for the authentication implementation.

## 1. AuthContext Implementation

**File:** `/Users/janschubert/tools/archon/archon-ui-main/src/contexts/AuthContext.tsx`

```typescript
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { getApiUrl } from '../config/api';

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (apiKey: string) => Promise<void>;
  logout: () => void;
  getApiKey: () => string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);
const API_KEY_STORAGE_KEY = 'archon_api_key';

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Get API key from localStorage
  const getApiKey = useCallback(() => {
    return localStorage.getItem(API_KEY_STORAGE_KEY);
  }, []);

  // Validate API key with backend
  const validateApiKey = useCallback(async (apiKey: string): Promise<boolean> => {
    try {
      const baseUrl = getApiUrl();
      const response = await fetch(`${baseUrl}/api/auth/validate`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
      });

      return response.ok;
    } catch (error) {
      console.error('API key validation error:', error);
      throw error;
    }
  }, []);

  // Login function
  const login = useCallback(async (apiKey: string) => {
    setError(null);
    setIsLoading(true);

    try {
      const isValid = await validateApiKey(apiKey);

      if (isValid) {
        localStorage.setItem(API_KEY_STORAGE_KEY, apiKey);
        setIsAuthenticated(true);
      } else {
        setError('Invalid API key. Please check your key and try again.');
        throw new Error('Invalid API key');
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Authentication failed';
      setError(errorMessage);
      setIsAuthenticated(false);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [validateApiKey]);

  // Logout function
  const logout = useCallback(() => {
    localStorage.removeItem(API_KEY_STORAGE_KEY);
    setIsAuthenticated(false);
    setError(null);
  }, []);

  // Validate stored key on mount
  useEffect(() => {
    const initAuth = async () => {
      const storedKey = getApiKey();

      if (!storedKey) {
        setIsAuthenticated(false);
        setIsLoading(false);
        return;
      }

      try {
        const isValid = await validateApiKey(storedKey);
        setIsAuthenticated(isValid);

        if (!isValid) {
          localStorage.removeItem(API_KEY_STORAGE_KEY);
        }
      } catch (error) {
        console.error('Failed to validate stored API key:', error);
        setIsAuthenticated(false);
        localStorage.removeItem(API_KEY_STORAGE_KEY);
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, [getApiKey, validateApiKey]);

  const value: AuthContextType = {
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    getApiKey,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
```

**Key Features:**
- Validates API key on mount
- Stores key in localStorage
- Provides loading states
- Error handling
- Clean API for components

---

## 2. Login Page Component

**File:** `/Users/janschubert/tools/archon/archon-ui-main/src/features/auth/LoginPage.tsx`

### Key Parts Explained

**State Management:**
```typescript
const [apiKey, setApiKey] = useState('');
const [isSubmitting, setIsSubmitting] = useState(false);
const [localError, setLocalError] = useState<string | null>(null);
const { login, isAuthenticated, error: authError } = useAuth();
```

**Form Submission:**
```typescript
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  setLocalError(null);

  if (!apiKey.trim()) {
    setLocalError('Please enter an API key');
    return;
  }

  setIsSubmitting(true);

  try {
    await login(apiKey);
    // On success, ProtectedRoute will handle redirect
  } catch (error) {
    console.error('Login failed:', error);
    // Error shown via authError state
  } finally {
    setIsSubmitting(false);
  }
};
```

**Redirect After Login:**
```typescript
useEffect(() => {
  if (isAuthenticated) {
    navigate(from, { replace: true });
  }
}, [isAuthenticated, navigate, from]);
```

**UI Structure:**
```typescript
<Card blur="md" transparency="light" size="lg">
  {/* Logo */}
  <img src="/logo-neon.png" alt="Archon" />

  {/* Form */}
  <form onSubmit={handleSubmit}>
    <Input
      type="password"
      value={apiKey}
      onChange={(e) => setApiKey(e.target.value)}
    />

    {/* Error Display */}
    {errorMessage && (
      <div className="error">
        <AlertCircle />
        <p>{errorMessage}</p>
      </div>
    )}

    {/* Submit Button */}
    <Button type="submit" loading={isSubmitting}>
      Login
    </Button>
  </form>
</Card>
```

---

## 3. Protected Route Component

**File:** `/Users/janschubert/tools/archon/archon-ui-main/src/components/auth/ProtectedRoute.tsx`

```typescript
import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  // Show loading screen while checking auth
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <img src="/logo-neon.png" alt="Loading" className="animate-pulse" />
          <p>Verifying authentication</p>
        </div>
      </div>
    );
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Render protected content
  return <>{children}</>;
}
```

**Usage in Routes:**
```typescript
<Route
  path="/knowledge"
  element={
    <ProtectedRoute>
      <KnowledgeBasePage />
    </ProtectedRoute>
  }
/>
```

---

## 4. API Client with Authentication

**File:** `/Users/janschubert/tools/archon/archon-ui-main/src/lib/apiClient.ts`

### Core Functions

**Get Auth Headers:**
```typescript
function getAuthHeaders(): HeadersInit {
  const apiKey = localStorage.getItem('archon_api_key');

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };

  if (apiKey) {
    headers['Authorization'] = `Bearer ${apiKey}`;
  }

  return headers;
}
```

**API Request with 401 Handling:**
```typescript
export async function apiRequest<T = any>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const baseUrl = getApiUrl();
  const url = `${baseUrl}${endpoint}`;

  const headers = {
    ...getAuthHeaders(),
    ...options.headers,
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  // Handle 401 Unauthorized
  if (response.status === 401) {
    localStorage.removeItem('archon_api_key');

    if (unauthorizedCallback) {
      unauthorizedCallback(); // Redirect to login
    }

    throw new Error('Unauthorized: Invalid or expired API key');
  }

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`HTTP ${response.status}: ${errorText}`);
  }

  return await response.json();
}
```

**Convenience Methods:**
```typescript
export const apiClient = {
  get: <T = any>(endpoint: string) =>
    apiRequest<T>(endpoint, { method: 'GET' }),

  post: <T = any>(endpoint: string, data?: any) =>
    apiRequest<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  put: <T = any>(endpoint: string, data?: any) =>
    apiRequest<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  delete: <T = any>(endpoint: string) =>
    apiRequest<T>(endpoint, { method: 'DELETE' }),
};
```

**Usage Examples:**
```typescript
// GET request
const documents = await apiClient.get('/api/knowledge/documents');

// POST request
const newDoc = await apiClient.post('/api/knowledge/documents', {
  title: 'My Document',
  content: 'Content here',
});

// PUT request
const updated = await apiClient.put(`/api/knowledge/documents/${id}`, {
  title: 'Updated Title',
});

// DELETE request
await apiClient.delete(`/api/knowledge/documents/${id}`);
```

---

## 5. App.tsx Integration

**File:** `/Users/janschubert/tools/archon/archon-ui-main/src/App.tsx`

### Provider Hierarchy

```typescript
export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <AuthProvider>          {/* Auth context at high level */}
          <ToastProvider>
            <TooltipProvider>
              <SettingsProvider>
                <AppContent />
              </SettingsProvider>
            </TooltipProvider>
          </ToastProvider>
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}
```

### API Client Configuration

```typescript
const ApiClientConfigurator = () => {
  const navigate = useNavigate();

  useEffect(() => {
    configureApiClient({
      onUnauthorized: () => {
        navigate('/login', { replace: true });
      },
    });
  }, [navigate]);

  return null;
};
```

### Route Configuration

```typescript
const AppRoutes = () => {
  return (
    <Routes>
      {/* Public route - no protection */}
      <Route path="/login" element={<LoginPage />} />

      {/* Protected routes - wrapped in ProtectedRoute */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Navigate to="/knowledge" replace />
          </ProtectedRoute>
        }
      />

      <Route
        path="/knowledge"
        element={
          <ProtectedRoute>
            <KnowledgeBasePage />
          </ProtectedRoute>
        }
      />

      {/* ... more protected routes */}
    </Routes>
  );
};
```

---

## 6. Navigation with Logout

**File:** `/Users/janschubert/tools/archon/archon-ui-main/src/components/layout/Navigation.tsx`

### Logout Handler

```typescript
export function Navigation({ className }: NavigationProps) {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav>
      {/* ... navigation items ... */}

      {/* Separator */}
      <div className="separator" />

      {/* Logout Button */}
      <Tooltip>
        <TooltipTrigger asChild>
          <button
            onClick={handleLogout}
            className={cn(
              "logout-button",
              "hover:text-red-600",
              "hover:bg-red-50/10"
            )}
          >
            <LogOut className="h-5 w-5" />
          </button>
        </TooltipTrigger>
        <TooltipContent>
          <p>Logout</p>
        </TooltipContent>
      </Tooltip>
    </nav>
  );
}
```

---

## 7. Usage Patterns

### Pattern 1: Check Auth in Component

```typescript
import { useAuth } from '@/contexts/AuthContext';

function MyComponent() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!isAuthenticated) {
    return <div>Please log in to continue</div>;
  }

  return <div>Authenticated content</div>;
}
```

### Pattern 2: Conditional Rendering

```typescript
function Header() {
  const { isAuthenticated, logout } = useAuth();

  return (
    <header>
      <h1>My App</h1>
      {isAuthenticated && (
        <button onClick={logout}>
          Logout
        </button>
      )}
    </header>
  );
}
```

### Pattern 3: Protected Action

```typescript
function DeleteButton({ documentId }) {
  const { isAuthenticated } = useAuth();

  const handleDelete = async () => {
    if (!isAuthenticated) {
      alert('Please log in');
      return;
    }

    await apiClient.delete(`/api/documents/${documentId}`);
  };

  return (
    <button onClick={handleDelete} disabled={!isAuthenticated}>
      Delete
    </button>
  );
}
```

### Pattern 4: Handle Auth Errors

```typescript
function MyApiComponent() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const result = await apiClient.get('/api/data');
        setData(result);
      } catch (err) {
        if (err.message.includes('Unauthorized')) {
          // Will auto-redirect to login via apiClient
          setError('Session expired. Redirecting...');
        } else {
          setError('Failed to load data');
        }
      }
    }

    fetchData();
  }, []);

  if (error) return <div>Error: {error}</div>;
  if (!data) return <div>Loading...</div>;

  return <div>{JSON.stringify(data)}</div>;
}
```

### Pattern 5: Login Form with Validation

```typescript
function LoginForm() {
  const { login, error } = useAuth();
  const [apiKey, setApiKey] = useState('');
  const [localError, setLocalError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateApiKey = (key: string) => {
    if (!key) return 'API key is required';
    if (key.length < 10) return 'API key seems too short';
    return null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const validationError = validateApiKey(apiKey);
    if (validationError) {
      setLocalError(validationError);
      return;
    }

    setLocalError('');
    setIsSubmitting(true);

    try {
      await login(apiKey);
      // Success - will redirect automatically
    } catch (err) {
      // Error already in context error state
    } finally {
      setIsSubmitting(false);
    }
  };

  const displayError = localError || error;

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="password"
        value={apiKey}
        onChange={(e) => setApiKey(e.target.value)}
        placeholder="API Key"
      />

      {displayError && (
        <div className="error">{displayError}</div>
      )}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}
```

---

## 8. Testing Utilities

### Test Auth Context

```typescript
import { render, screen } from '@testing-library/react';
import { AuthProvider } from '@/contexts/AuthContext';

const wrapper = ({ children }) => (
  <AuthProvider>
    {children}
  </AuthProvider>
);

test('auth context provides expected values', () => {
  render(<MyComponent />, { wrapper });
  // ... test assertions
});
```

### Mock API Client

```typescript
import { apiClient } from '@/lib/apiClient';

jest.mock('@/lib/apiClient', () => ({
  apiClient: {
    get: jest.fn(),
    post: jest.fn(),
    put: jest.fn(),
    delete: jest.fn(),
  },
}));

test('makes authenticated API call', async () => {
  (apiClient.get as jest.Mock).mockResolvedValue({ data: 'test' });

  // ... test component that uses apiClient

  expect(apiClient.get).toHaveBeenCalledWith('/api/endpoint');
});
```

---

## 9. Environment Configuration

### Development (.env.development)
```bash
# Use Vite proxy - relative URLs
# No VITE_API_URL needed
```

### Production (.env.production)
```bash
# If backend is on different domain
VITE_API_URL=https://api.archon.example.com
```

### Docker Compose
```yaml
services:
  frontend:
    environment:
      - VITE_API_URL=http://backend:8000
```

---

## 10. Migration Guide

### Migrating Existing Services

**Before (credentialsService.ts):**
```typescript
async getAllCredentials(): Promise<Credential[]> {
  const response = await fetch(`${this.baseUrl}/api/credentials`);
  if (!response.ok) {
    throw new Error("Failed to fetch credentials");
  }
  return response.json();
}
```

**After (with apiClient):**
```typescript
import { apiClient } from '../lib/apiClient';

async getAllCredentials(): Promise<Credential[]> {
  try {
    return await apiClient.get('/api/credentials');
  } catch (error) {
    throw new Error("Failed to fetch credentials");
  }
}
```

**Benefits:**
- Automatic authentication headers
- Automatic 401 handling
- Consistent error handling
- Less boilerplate code

---

## Summary

This authentication system provides:

1. **Secure Authentication**
   - API key stored in localStorage
   - Automatic validation on mount
   - Bearer token authentication

2. **User Experience**
   - Persistent sessions
   - Automatic redirects
   - Clear error messages
   - Loading states

3. **Developer Experience**
   - Simple API with useAuth hook
   - Automatic API authentication
   - Easy to integrate
   - Type-safe with TypeScript

4. **Production Ready**
   - Error handling
   - 401 auto-logout
   - Build successful
   - No dependencies added

The implementation follows React best practices and integrates seamlessly with the existing Archon UI architecture.
