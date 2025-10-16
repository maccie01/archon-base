# Archon Authentication System

**Created**: 2025-10-15
**Updated**: 2025-10-16 (Kong JWT Flow)
**Version**: 1.3.0
**Status**: ✅ Production Ready

---

## Overview

Archon uses API key-based authentication to secure all endpoints. The system provides:

- ✅ Secure API key generation with bcrypt hashing
- ✅ Bearer token authentication
- ✅ Fine-grained permissions (read, write, admin)
- ✅ Bootstrap mechanism for initial setup
- ✅ Automatic key validation and rotation support
- ✅ Kong Gateway JWT transformation (v1.3.0)

---

## Architecture

```
┌──────────────┐
│   Client     │
│  (Browser/   │
│   API Call)  │
└──────┬───────┘
       │ Authorization: Bearer ak_xxxx...
       ▼
┌──────────────────────────────────┐
│  APIKeyAuthMiddleware            │
│  (middleware/auth_middleware.py) │
├──────────────────────────────────┤
│ 1. Extract Bearer token          │
│ 2. Hash and lookup in database   │
│ 3. Validate is_active             │
│ 4. Check permissions             │
│ 5. Inject into request.state     │
└──────┬──────────────────────────┘
       │ ✅ Valid → Continue
       │ ❌ Invalid → 401
       ▼
┌──────────────────────────────────┐
│   Protected Endpoint             │
│   (requires auth = Depends(...)) │
└──────────────────────────────────┘
```

---

## Kong Gateway JWT Transformation (v1.3.0)

### Overview

In the consolidated architecture, Kong Gateway sits between clients and PostgREST, handling JWT authentication transformation to prevent PGRST301 errors (JWT secret mismatch).

### Authentication Flow

```
Client Request (with Archon API key)
       │
       ▼
┌──────────────────────────────┐
│  APIKeyAuthMiddleware         │
│  (Archon Server)             │
├──────────────────────────────┤
│ 1. Validate Bearer token     │
│ 2. Check bcrypt hash         │
│ 3. Verify is_active          │
│ 4. Check permissions         │
└──────┬───────────────────────┘
       │ ✅ Valid → Continue
       ▼
┌──────────────────────────────┐
│  Supabase Client Request     │
│  (Internal to Kong)          │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Kong Gateway                │
│  (supabase-kong:54321)       │
├──────────────────────────────┤
│ 1. Remove Authorization      │
│    header (if present)       │
│ 2. Add hardcoded service JWT │
│    (configured with correct  │
│     JWT secret)              │
│ 3. Forward to PostgREST      │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  PostgREST                   │
│  (port 3000, internal)       │
├──────────────────────────────┤
│ 1. Validate service JWT      │
│ 2. Execute database query    │
│ 3. Return results            │
└──────────────────────────────┘
```

### Why This Is Needed

**Problem**: PGRST301 errors occur when JWT secret in client request doesn't match database configuration.

**Solution**: Kong Gateway removes any client Authorization headers and adds a hardcoded service JWT that matches the database's JWT secret.

**Configuration**:
- **Database JWT Secret**: `super-secret-jwt-token-with-at-least-32-characters-long`
- **Kong Service JWT**: Hardcoded with same secret
- **Client Authorization**: Removed by Kong before forwarding to PostgREST

### Database JWT Configuration

The PostgreSQL database is configured with the JWT secret:

```sql
-- Database configuration (set at startup)
ALTER DATABASE postgres SET app.settings.jwt_secret TO 'super-secret-jwt-token-with-at-least-32-characters-long';

-- Verify configuration
SHOW app.settings.jwt_secret;
```

This secret **must match**:
1. `SUPABASE_JWT_SECRET` environment variable
2. Kong Gateway service JWT configuration
3. PostgREST JWT secret configuration

---

## Database Schema

### api_keys Table

```sql
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key_name TEXT NOT NULL,
    key_hash TEXT NOT NULL UNIQUE,
    key_prefix TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_used_at TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    permissions JSONB DEFAULT '{"read": true, "write": true, "admin": false}'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,

    CONSTRAINT key_name_not_empty CHECK (length(key_name) > 0),
    CONSTRAINT key_hash_not_empty CHECK (length(key_hash) > 0),
    CONSTRAINT key_prefix_format CHECK (key_prefix ~ '^ak_[a-zA-Z0-9]{4}$')
);

CREATE INDEX idx_api_keys_key_hash ON api_keys(key_hash);
CREATE INDEX idx_api_keys_is_active ON api_keys(is_active);
CREATE INDEX idx_api_keys_key_prefix ON api_keys(key_prefix);
CREATE INDEX idx_api_keys_created_at ON api_keys(created_at DESC);
```

**Applied**: 2025-10-15 via `migration/add_api_keys_table.sql`

---

## API Key Format

### Structure

```
ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI
│  │    │
│  │    └─ Random token (43 characters, URL-safe base64)
│  └────── Prefix identifier (4 characters)
└───────── Key type identifier ("ak" = API key)
```

### Components

1. **Type Prefix**: `ak_` - Identifies this as an API key
2. **Random ID**: `597A` - Short unique identifier for key lookup
3. **Separator**: `_` - Separates prefix from token
4. **Token**: `U6Z6POYpv8Sae...` - Cryptographically secure random string

### Security

- **Generation**: `secrets.token_urlsafe(32)` (cryptographically secure)
- **Storage**: Bcrypt hash (never plain text)
- **Prefix**: Stored in plain text for quick lookup
- **Hash**: Used for validation (cost factor 12)

---

## Backend Implementation

### 1. Middleware (`middleware/auth_middleware.py`)

```python
class APIKeyAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Exempt paths (public access)
        if request.url.path in EXEMPT_PATHS:
            return await call_next(request)

        # Extract Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"error": "Authentication required"})

        # Validate API key
        api_key = auth_header.replace("Bearer ", "")
        is_valid, key_info = await api_key_service.validate_api_key(api_key)

        if not is_valid:
            return JSONResponse(status_code=401, content={"error": "Invalid API key"})

        # Inject key info into request
        request.state.api_key_id = key_info["id"]
        request.state.api_key_permissions = key_info["permissions"]

        return await call_next(request)
```

**Exempt Paths** (no authentication required):
- `/` - Root endpoint
- `/health` - Health check
- `/api/health` - API health check
- `/api/auth/bootstrap` - Bootstrap endpoint
- `/api/auth/status` - Bootstrap status check
- `/internal/*` - Internal-only endpoints

### 2. API Key Service (`services/api_key_service.py`)

**Key Functions**:

```python
# Generate new API key
async def create_api_key(name: str, permissions: dict = None) -> tuple[bool, dict]:
    api_key, key_prefix = generate_api_key()
    key_hash = bcrypt.hashpw(api_key.encode('utf-8'), bcrypt.gensalt())
    # Store in database
    return True, {"api_key": api_key, "key_id": result.id}

# Validate API key
async def validate_api_key(api_key: str) -> tuple[bool, dict]:
    # Hash and check against database
    # Update last_used_at
    return is_valid, key_info

# List all keys
async def list_api_keys() -> list[dict]:
    # Return all keys (without full hash)

# Revoke key
async def revoke_api_key(key_id: str) -> bool:
    # Set is_active = false
```

### 3. Auth API (`api_routes/auth_api.py`)

**Endpoints**:

```python
@router.post("/bootstrap")
async def bootstrap_first_api_key(request: BootstrapRequest):
    """Create the first API key using bootstrap secret."""
    # Verify bootstrap secret
    # Check no keys exist
    # Create admin key

@router.get("/status")
async def get_bootstrap_status():
    """Check if bootstrap is available."""
    # Return bootstrap_available: bool

@router.post("/validate")
async def validate_current_key(auth = Depends(require_auth)):
    """Validate the current API key."""
    # Return key info if valid

@router.get("/keys")
async def list_keys(auth = Depends(require_auth)):
    """List all API keys (admin only)."""
    # Return list of keys

@router.post("/keys")
async def create_key(request: CreateKeyRequest, auth = Depends(require_auth)):
    """Create a new API key (admin only)."""
    # Generate and return new key

@router.delete("/keys/{key_id}")
async def revoke_key(key_id: str, auth = Depends(require_auth)):
    """Revoke an API key (admin only)."""
    # Deactivate key
```

---

## Frontend Implementation

### 1. Auth Context (`contexts/AuthContext.tsx`)

```typescript
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [apiKey, setApiKey] = useState<string | null>(() => {
    return localStorage.getItem('archon_api_key');
  });
  const [isValidating, setIsValidating] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const validateKey = async () => {
      if (!apiKey) {
        setIsAuthenticated(false);
        setIsValidating(false);
        return;
      }

      try {
        const response = await fetch('/api/auth/validate', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
          }
        });
        setIsAuthenticated(response.ok);
      } catch (error) {
        setIsAuthenticated(false);
      }

      setIsValidating(false);
    };

    validateKey();
  }, [apiKey]);

  const login = async (key: string) => {
    const response = await fetch('/api/auth/validate', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${key}` }
    });

    if (!response.ok) throw new Error('Invalid API key');

    localStorage.setItem('archon_api_key', key);
    setApiKey(key);
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem('archon_api_key');
    setApiKey(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, isValidating, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
```

### 2. Protected Routes (`components/auth/ProtectedRoute.tsx`)

```typescript
export const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isValidating } = useAuth();
  const location = useLocation();

  if (isValidating) {
    return <LoadingScreen />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
};
```

### 3. API Client (`features/shared/api/apiClient.ts`)

```typescript
export async function callAPIWithETag<T = unknown>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    ...((options.headers as Record<string, string>) || {}),
  };

  // Add Authorization header if API key exists in localStorage
  const apiKey = localStorage.getItem('archon_api_key');
  if (apiKey) {
    headers['Authorization'] = `Bearer ${apiKey}`;
  }

  const response = await fetch(fullUrl, {
    ...options,
    headers,
  });

  // Handle 401 Unauthorized - clear stored API key and redirect to login
  if (response.status === 401) {
    localStorage.removeItem('archon_api_key');
    if (window.location.pathname !== '/login') {
      window.location.href = '/login';
    }
    throw new APIServiceError('Authentication required', 'AUTH_ERROR', 401);
  }

  // ... rest of error handling
}
```

### 4. Login Page (`features/auth/LoginPage.tsx`)

```typescript
export const LoginPage: React.FC = () => {
  const [apiKey, setApiKey] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login(apiKey);
      navigate('/knowledge');
    } catch (err) {
      setError('Invalid API key. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8">
        <h2>Welcome to Archon</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="Enter your API key"
          />
          <button type="submit" disabled={!apiKey || isLoading}>
            {isLoading ? 'Validating...' : 'Login'}
          </button>
          {error && <p className="text-red-600">{error}</p>}
        </form>
      </div>
    </div>
  );
};
```

---

## Bootstrap Process

### Initial Setup (First API Key)

**Prerequisites**:
1. Database migration applied (`add_api_keys_table.sql`)
2. `ARCHON_BOOTSTRAP_SECRET` set in `.env`
3. No existing API keys in database

**Process**:

1. **Generate Bootstrap Secret** (if not set):
   ```bash
   openssl rand -base64 32
   # Add to .env: ARCHON_BOOTSTRAP_SECRET=<generated_secret>
   ```

2. **Run Bootstrap Script**:
   ```bash
   cd /opt/archon/migration
   python3 bootstrap_api_key.py
   ```

3. **Script Workflow**:
   - Prompts for server URL (default: http://localhost:8181)
   - Checks if bootstrap is available
   - Generates or uses existing bootstrap secret
   - Prompts for key name
   - Creates admin API key
   - Displays key (ONLY TIME IT'S SHOWN)

4. **Save API Key**:
   ```bash
   # Add to .env
   ARCHON_API_KEY=ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI

   # Or store in password manager
   ```

**Example Output**:
```
============================================================
SUCCESS! API Key Created
============================================================

Key Name: Production Admin Key
Key ID: 3a5c4b2d-1e8f-4a9b-b5c6-7d8e9f0a1b2c

============================================================
YOUR API KEY (save this securely!):
ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI
============================================================

WARNING: This is the ONLY time you will see this API key!
Store it securely in your password manager or .env file.

Test your API key:
curl -H "Authorization: Bearer ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI" \
  http://localhost:8181/api/auth/validate
```

---

## Usage Examples

### Backend (Python)

**Protecting an endpoint**:
```python
from fastapi import Depends
from ..auth.dependencies import require_auth

@router.get("/protected-resource")
async def get_protected_resource(auth = Depends(require_auth)):
    """This endpoint requires authentication."""
    # auth.api_key_id - Current API key ID
    # auth.api_key_permissions - Permissions dict
    return {"message": "Access granted", "key_id": auth.api_key_id}
```

**Admin-only endpoint**:
```python
@router.delete("/admin-only")
async def admin_only_operation(auth = Depends(require_admin)):
    """This endpoint requires admin permissions."""
    # Check permissions
    if not auth.api_key_permissions.get("admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"message": "Admin operation successful"}
```

### Frontend (TypeScript/React)

**Using authenticated API**:
```typescript
import { apiClient } from '@/features/shared/api/apiClient';

// API client automatically includes Authorization header
const data = await apiClient.get<KnowledgeItem[]>('/api/knowledge-items/summary');

// Or use callAPIWithETag directly
const result = await callAPIWithETag<Response>('/api/endpoint');
```

**Manual fetch with auth**:
```typescript
const apiKey = localStorage.getItem('archon_api_key');

const response = await fetch('/api/endpoint', {
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  }
});
```

### curl Examples

**Validate API key**:
```bash
curl -X POST https://archon.nexorithm.io/api/auth/validate \
  -H "Authorization: Bearer ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI"
```

**List knowledge items**:
```bash
curl https://archon.nexorithm.io/api/knowledge-items/summary?page=1&per_page=10 \
  -H "Authorization: Bearer ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI"
```

**Create new API key** (admin only):
```bash
curl -X POST https://archon.nexorithm.io/api/auth/keys \
  -H "Authorization: Bearer ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI" \
  -H "Content-Type: application/json" \
  -d '{
    "key_name": "Development Key",
    "permissions": {"read": true, "write": false, "admin": false}
  }'
```

---

## Key Management

### Creating Additional Keys

**Via API**:
```bash
curl -X POST https://archon.nexorithm.io/api/auth/keys \
  -H "Authorization: Bearer <admin_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "key_name": "Mobile App Key",
    "permissions": {"read": true, "write": true, "admin": false},
    "metadata": {"created_for": "mobile_app_v1.0"}
  }'
```

**Via Database** (emergency):
```sql
-- Insert pre-hashed key (bcrypt hash of actual key)
INSERT INTO api_keys (key_name, key_hash, key_prefix, permissions)
VALUES (
  'Emergency Key',
  '$2b$12$...', -- Bcrypt hash
  'ak_EMRG',
  '{"read": true, "write": true, "admin": true}'::jsonb
);
```

### Listing Keys

```bash
curl https://archon.nexorithm.io/api/auth/keys \
  -H "Authorization: Bearer <admin_key>"
```

**Response**:
```json
{
  "keys": [
    {
      "id": "uuid",
      "key_name": "Production Admin Key",
      "key_prefix": "ak_597A",
      "created_at": "2025-10-15T08:30:00Z",
      "last_used_at": "2025-10-15T09:45:00Z",
      "is_active": true,
      "permissions": {"read": true, "write": true, "admin": true}
    }
  ]
}
```

### Revoking Keys

**Via API**:
```bash
curl -X DELETE https://archon.nexorithm.io/api/auth/keys/<key_id> \
  -H "Authorization: Bearer <admin_key>"
```

**Via Database**:
```sql
-- Soft delete (recommended)
UPDATE api_keys SET is_active = false WHERE id = 'uuid';

-- Hard delete (not recommended)
DELETE FROM api_keys WHERE id = 'uuid';
```

### Rotating Keys

1. **Create new key** with same permissions
2. **Update applications** to use new key
3. **Test** new key works
4. **Revoke old key**
5. **Verify** old key no longer works

---

## Security Best Practices

### Key Storage

✅ **DO**:
- Store in environment variables
- Use password managers
- Encrypt in configuration management tools
- Rotate regularly (quarterly recommended)

❌ **DON'T**:
- Commit to version control
- Share via email/chat
- Embed in client-side code
- Log in plain text

### Permissions

**Principle of Least Privilege**:
- Grant minimum permissions needed
- Use read-only keys for dashboards
- Reserve admin keys for automation/ops

**Permission Levels**:
- `read: true` - Can query data
- `write: true` - Can create/update/delete data
- `admin: true` - Can manage API keys and system settings

### Monitoring

Track:
- `last_used_at` - Detect unused keys
- API call patterns - Detect anomalies
- Failed auth attempts - Detect attacks
- Key creation/deletion - Audit trail

**Example Query**:
```sql
-- Find unused keys (over 30 days)
SELECT key_name, key_prefix, created_at, last_used_at
FROM api_keys
WHERE is_active = true
  AND (last_used_at IS NULL OR last_used_at < NOW() - INTERVAL '30 days');
```

---

## Troubleshooting

### Issue: 401 Unauthorized

**Symptoms**: All API calls return 401

**Checks**:
1. Verify API key format: `ak_XXXX_...`
2. Check Authorization header: `Bearer <key>`
3. Verify key is active in database
4. Test with curl to isolate issue

**Solutions**:
```bash
# Test key validity
curl -v -X POST http://localhost:8181/api/auth/validate \
  -H "Authorization: Bearer <your_key>"

# Check database
SELECT key_prefix, is_active FROM api_keys WHERE key_prefix = 'ak_597A';

# Enable debugging
export LOG_LEVEL=DEBUG
docker compose restart archon-server
```

### Issue: Bootstrap Not Available

**Symptoms**: Bootstrap endpoint returns 403

**Cause**: API keys already exist in database

**Solution**:
```bash
# Check existing keys
SELECT COUNT(*) FROM api_keys;

# If you need to re-bootstrap (DANGEROUS - deletes all keys):
TRUNCATE api_keys CASCADE;
# Then run bootstrap script again
```

### Issue: Frontend Not Sending Auth Header

**Symptoms**: Frontend gets 401 but key is valid

**Checks**:
1. Check localStorage has key: `localStorage.getItem('archon_api_key')`
2. Check Network tab for Authorization header
3. Verify apiClient is being used

**Solution**:
```typescript
// Debug API calls
console.log('API Key:', localStorage.getItem('archon_api_key'));

// Check if header is added
const headers = new Headers();
const apiKey = localStorage.getItem('archon_api_key');
if (apiKey) {
  headers.append('Authorization', `Bearer ${apiKey}`);
}
console.log('Headers:', Object.fromEntries(headers.entries()));
```

---

## Migration Guide

### From No Auth to Auth

1. **Apply Database Migration**:
   ```bash
   # Via Supabase Dashboard SQL Editor
   # Run: migration/add_api_keys_table.sql
   ```

2. **Update .env**:
   ```bash
   AUTH_ENABLED=true
   ARCHON_BOOTSTRAP_SECRET=<generate_random>
   ALLOWED_ORIGINS=https://archon.nexorithm.io
   ```

3. **Restart Services**:
   ```bash
   docker compose restart
   ```

4. **Create First API Key**:
   ```bash
   cd /opt/archon/migration
   python3 bootstrap_api_key.py
   ```

5. **Update Frontend** (if needed):
   - Ensure AuthContext wraps app
   - Ensure ProtectedRoute wraps routes
   - Ensure apiClient includes auth headers

6. **Test**:
   ```bash
   # Should work
   curl -H "Authorization: Bearer <key>" http://localhost:8181/api/health

   # Should fail (401)
   curl http://localhost:8181/api/knowledge-items/summary
   ```

---

**Last Updated**: 2025-10-15
**Version**: 1.1.0
**Status**: Production Ready
