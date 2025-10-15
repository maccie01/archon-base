# Archon UI Authentication Usage Guide

Date Created: 2025-10-15

## Quick Start

### For Users

1. **Initial Access**
   - Open your browser and navigate to the Archon UI URL
   - You will be automatically redirected to the login page

2. **Logging In**
   - Enter your API key in the password field
   - Click the "Login" button
   - Upon successful authentication, you will be redirected to the Knowledge Base

3. **Using the Application**
   - Navigate freely between pages using the sidebar
   - All your API requests will be automatically authenticated

4. **Logging Out**
   - Click the logout button (door with arrow icon) at the bottom of the navigation sidebar
   - You will be redirected to the login page
   - Your session will be cleared

### For Developers

#### Using the AuthContext

```typescript
import { useAuth } from '@/contexts/AuthContext';

function MyComponent() {
  const { isAuthenticated, login, logout, isLoading, error } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return <div>Please log in</div>;
  }

  return <div>Welcome!</div>;
}
```

#### Making Authenticated API Calls

```typescript
import { apiClient } from '@/lib/apiClient';

// GET request
async function fetchData() {
  try {
    const data = await apiClient.get('/api/knowledge/documents');
    console.log(data);
  } catch (error) {
    console.error('API call failed:', error);
  }
}

// POST request
async function createDocument(documentData) {
  try {
    const result = await apiClient.post('/api/knowledge/documents', documentData);
    return result;
  } catch (error) {
    console.error('Failed to create document:', error);
    throw error;
  }
}

// PUT request
async function updateDocument(id, updates) {
  try {
    const updated = await apiClient.put(`/api/knowledge/documents/${id}`, updates);
    return updated;
  } catch (error) {
    console.error('Failed to update document:', error);
    throw error;
  }
}

// DELETE request
async function deleteDocument(id) {
  try {
    await apiClient.delete(`/api/knowledge/documents/${id}`);
  } catch (error) {
    console.error('Failed to delete document:', error);
    throw error;
  }
}
```

#### Creating Protected Routes

```typescript
import { ProtectedRoute } from '@/components/auth/ProtectedRoute';

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/my-protected-page"
        element={
          <ProtectedRoute>
            <MyProtectedPage />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}
```

#### Handling Logout Programmatically

```typescript
import { useAuth } from '@/contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

function MyComponent() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <button onClick={handleLogout}>
      Log Out
    </button>
  );
}
```

## API Key Management

### Obtaining an API Key

Contact your system administrator to obtain an API key. API keys are generated on the backend and should be kept secure.

### API Key Security

- API keys are stored in browser localStorage
- Keys are automatically included in all API requests via the Authorization header
- Keys are validated on initial page load
- Invalid or expired keys are automatically cleared
- Never share your API key with others
- Never commit API keys to version control

### API Key Format

API keys are sent to the backend in the Authorization header:
```
Authorization: Bearer your-api-key-here
```

## Troubleshooting

### "Invalid API key" Error

**Problem**: You see an error message saying your API key is invalid.

**Solutions**:
1. Double-check that you copied the entire API key
2. Ensure there are no leading or trailing spaces
3. Verify the key hasn't expired
4. Contact your administrator for a new key

### Automatically Logged Out

**Problem**: You were logged out unexpectedly.

**Possible Causes**:
1. Your API key expired
2. Your API key was revoked by an administrator
3. The backend returned a 401 Unauthorized response

**Solution**: Log in again with a valid API key

### Login Page Keeps Redirecting

**Problem**: After logging in, you're immediately redirected back to the login page.

**Possible Causes**:
1. API key validation is failing
2. Backend is not reachable
3. Backend authentication endpoint is not working

**Solutions**:
1. Check browser console for errors
2. Verify backend is running
3. Test API key using curl:
   ```bash
   curl -H "Authorization: Bearer YOUR-API-KEY" http://your-backend-url/api/auth/validate
   ```

### Can't Access Protected Routes

**Problem**: Trying to access a page shows the login screen instead.

**Possible Causes**:
1. You're not logged in
2. Your session expired
3. localStorage was cleared

**Solution**: Log in again with your API key

## Backend Requirements

For the authentication system to work properly, the backend must:

1. **Implement `/api/auth/validate` endpoint**
   - Method: GET
   - Headers: `Authorization: Bearer <api-key>`
   - Response: 200 OK for valid keys, 401 for invalid

2. **Accept Authorization Header**
   - All protected endpoints must accept and validate the Bearer token

3. **Return 401 for Invalid/Expired Keys**
   - Return HTTP 401 status code for authentication failures
   - Frontend will automatically handle logout and redirect

## Testing Authentication

### Manual Testing

1. **Test Invalid Login**
```bash
# This should fail
curl -X GET http://localhost:3737/api/auth/validate \
  -H "Authorization: Bearer invalid-key"
```

2. **Test Valid Login**
```bash
# This should succeed (replace with your actual key)
curl -X GET http://localhost:3737/api/auth/validate \
  -H "Authorization: Bearer your-actual-api-key"
```

3. **Test Protected Endpoint**
```bash
# Test that API calls include the auth header
curl -X GET http://localhost:3737/api/knowledge/documents \
  -H "Authorization: Bearer your-actual-api-key"
```

### Browser Testing

1. Open browser DevTools (F12)
2. Go to Application > Local Storage
3. Find key `archon_api_key`
4. Verify it contains your API key
5. Go to Network tab
6. Make an API request
7. Check the request headers include `Authorization: Bearer <key>`

## Security Best Practices

### For Users

1. **Never share your API key**
   - Treat it like a password
   - Each user should have their own key

2. **Log out when finished**
   - Especially on shared computers
   - Logging out clears your session

3. **Report compromised keys immediately**
   - If you think your key was exposed, contact your administrator
   - Request a new key and have the old one revoked

### For Developers

1. **Never log API keys**
   - Don't console.log keys
   - Don't include keys in error messages

2. **Don't store keys in code**
   - Keys should only be entered by users
   - Never commit keys to git

3. **Use HTTPS in production**
   - API keys should only be transmitted over secure connections
   - Configure your deployment to use HTTPS

4. **Implement rate limiting**
   - Protect against brute force attacks
   - Limit failed login attempts

## Common Patterns

### Checking Authentication Status

```typescript
import { useAuth } from '@/contexts/AuthContext';

function MyComponent() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!isAuthenticated) {
    return <LoginPrompt />;
  }

  return <AuthenticatedContent />;
}
```

### Conditional Rendering Based on Auth

```typescript
import { useAuth } from '@/contexts/AuthContext';

function Navigation() {
  const { isAuthenticated } = useAuth();

  return (
    <nav>
      {isAuthenticated ? (
        <>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/settings">Settings</Link>
          <LogoutButton />
        </>
      ) : (
        <Link to="/login">Login</Link>
      )}
    </nav>
  );
}
```

### Handling Login Errors

```typescript
import { useAuth } from '@/contexts/AuthContext';
import { useState } from 'react';

function LoginForm() {
  const { login, error } = useAuth();
  const [apiKey, setApiKey] = useState('');
  const [localError, setLocalError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLocalError('');

    if (!apiKey.trim()) {
      setLocalError('Please enter an API key');
      return;
    }

    try {
      await login(apiKey);
      // Success - will redirect automatically
    } catch (err) {
      // Error is available via the error property
      console.error('Login failed:', err);
    }
  };

  const displayError = localError || error;

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="password"
        value={apiKey}
        onChange={(e) => setApiKey(e.target.value)}
        placeholder="Enter API key"
      />
      {displayError && <div className="error">{displayError}</div>}
      <button type="submit">Login</button>
    </form>
  );
}
```

## Architecture Decisions

### Why localStorage?

We use localStorage instead of sessionStorage because:
- Users expect to remain logged in after closing the browser
- Provides better user experience for daily usage
- Can be easily changed to sessionStorage if needed

### Why Context API?

We use React Context instead of Redux because:
- Authentication state is simple (logged in/out)
- No complex state updates needed
- Reduces bundle size
- Easier to understand and maintain

### Why Bearer Tokens?

We use Bearer token authentication because:
- Industry standard for API authentication
- Simple to implement
- Works with any backend
- Easy to debug (visible in network tab)

## Future Enhancements

Potential improvements to consider:

1. **Token Refresh**
   - Automatically refresh expired tokens
   - Silent renewal before expiration

2. **Multi-Factor Authentication**
   - Add second factor after API key entry
   - SMS or authenticator app codes

3. **Session Timeout**
   - Automatic logout after inactivity
   - Configurable timeout period

4. **Remember Me Option**
   - Let users choose localStorage vs sessionStorage
   - Toggle between persistent and session-only login

5. **Password Manager Integration**
   - Better support for password managers
   - Autocomplete attributes

6. **Biometric Authentication**
   - WebAuthn support for fingerprint/face unlock
   - Store encrypted keys in browser

## Support

For issues or questions:
1. Check this guide first
2. Review the AUTH_IMPLEMENTATION_REPORT.md
3. Check browser console for errors
4. Contact your system administrator
5. Open an issue in the project repository
