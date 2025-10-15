# Frontend Authentication Deployment Instructions

**Created**: 2025-10-15

## Overview

This document provides manual deployment instructions for the authentication-enabled frontend build.

## Current Status

- ✅ Backend authentication implemented and working
- ✅ Frontend production build created with auth components
- ✅ Database migration applied
- ✅ API key created and tested
- ⏳ Frontend deployment to production server needed

## Files to Deploy

**Source**: `/Users/janschubert/tools/archon/archon-ui-main/dist/`
**Target**: `root@91.98.156.158:/opt/archon/archon-ui-main/dist/`

## Manual Deployment Steps

### Option 1: Using SCP (if you have SSH access)

```bash
# From your local machine with SSH access
cd /Users/janschubert/tools/archon/archon-ui-main
scp -r dist/* root@91.98.156.158:/opt/archon/archon-ui-main/dist/

# Restart the container
ssh root@91.98.156.158 "cd /opt/archon && docker compose restart archon-ui"
```

### Option 2: Using tar.gz Archive

```bash
# Create archive
cd /Users/janschubert/tools/archon/archon-ui-main
tar -czf archon-ui-auth-build.tar.gz dist/

# Transfer via your preferred method (scp, sftp, web upload, etc.)
# Then on the server:
cd /opt/archon/archon-ui-main
rm -rf dist/*
tar -xzf archon-ui-auth-build.tar.gz
docker compose restart archon-ui
```

### Option 3: Direct Server Build

```bash
# SSH to server
ssh root@91.98.156.158

# Navigate to UI directory
cd /opt/archon/archon-ui-main

# Pull latest code
git fetch origin
git checkout stable
git pull origin stable

# Install dependencies and build
npm install
npm run build

# Restart container
docker compose restart archon-ui
```

## Verification Steps

After deployment, test the authentication flow:

1. **Visit** https://archon.nexorithm.io
2. **Expected**: Redirect to `/login` page
3. **Enter API key**: `ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI`
4. **Expected**: Redirect to `/knowledge` dashboard
5. **Test protected endpoint**: Navigate to Knowledge Inspector
6. **Expected**: Data loads successfully with auth header

## Testing Checklist

- [ ] Site redirects unauthenticated users to /login
- [ ] Login page displays correctly
- [ ] Valid API key allows login
- [ ] Invalid API key shows error message
- [ ] After login, dashboard loads properly
- [ ] API calls include Authorization header
- [ ] Protected endpoints return data (not 401)
- [ ] Logout clears session and redirects to login

## Rollback Plan

If issues occur:

```bash
# On server
cd /opt/archon/archon-ui-main
git checkout [previous-commit-hash]
npm run build
docker compose restart archon-ui
```

## API Key Information

**Production API Key**: `ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI`
**Permissions**: Full admin access (read, write, admin)
**Created**: 2025-10-15

Store this key securely. It cannot be retrieved again.

## Architecture Notes

### Frontend Components
- **AuthContext** (`src/contexts/AuthContext.tsx`): Manages authentication state
- **LoginPage** (`src/features/auth/LoginPage.tsx`): API key entry UI
- **ProtectedRoute** (`src/components/auth/ProtectedRoute.tsx`): Route guards
- **apiClient** (`src/lib/apiClient.ts`): Centralized API client with auth headers

### Backend Components
- **APIKeyAuthMiddleware** (`python/src/server/middleware/auth_middleware.py`): Request authentication
- **auth_api** (`python/src/server/api_routes/auth_api.py`): Auth endpoints
- **api_key_service** (`python/src/server/services/api_key_service.py`): Key management

### Exempt Endpoints (No Auth Required)
- `/` - Root
- `/health` - Health check
- `/api/health` - API health check
- `/api/auth/bootstrap` - Initial key creation
- `/api/auth/status` - Bootstrap availability status
- `/internal/*` - Internal endpoints

## Troubleshooting

### Issue: Still seeing 401 errors after deployment

**Solution**: Check that:
1. Production build includes auth code (check `dist/assets/*.js` for "AuthContext")
2. Container restarted after deployment
3. Browser cache cleared (Ctrl+Shift+R)

### Issue: Login page not showing

**Solution**:
1. Check browser console for errors
2. Verify `dist/index.html` has correct asset paths
3. Check CORS configuration allows `https://archon.nexorithm.io`

### Issue: API calls missing Authorization header

**Solution**:
1. Check that apiClient.ts is being used (not raw fetch)
2. Verify localStorage has `archon_api_key` after login
3. Update components to use apiClient instead of direct fetch

## Contact

For deployment assistance, contact the system administrator with SSH access to root@91.98.156.158.
