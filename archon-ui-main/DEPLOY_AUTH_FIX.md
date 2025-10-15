# Deploy Authentication Fix

## Issue Identified
The production deployment is running Vite dev server instead of the production build, which means the authentication code (AuthContext, ProtectedRoute, LoginPage) is not being loaded properly.

## Root Cause
- Frontend was never rebuilt after adding authentication features
- Production server is serving dev mode, not the production build from /dist

## Solution
Deploy the newly built production bundle that includes all authentication code.

## Deployment Steps

### Option 1: Manual Deployment via SSH

```bash
# 1. Copy the built files to the server
scp -r dist/* root@91.98.156.158:/opt/archon/archon-ui-main/dist/

# 2. SSH into the server and restart the container
ssh root@91.98.156.158
cd /opt/archon/archon-ui-main
docker compose restart archon-ui
```

### Option 2: Full Rebuild on Server

```bash
ssh root@91.98.156.158 << 'EOF'
cd /opt/archon/archon-ui-main
git pull origin main
npm run build
docker compose restart archon-ui
EOF
```

### Option 3: Using rsync (Recommended)

```bash
# Sync only the dist folder to the server
rsync -avz --delete dist/ root@91.98.156.158:/opt/archon/archon-ui-main/dist/

# Restart the container
ssh root@91.98.156.158 "cd /opt/archon/archon-ui-main && docker compose restart archon-ui"
```

## Verification Steps

After deployment, verify the fix worked:

1. Navigate to https://archon.nexorithm.io
2. Should redirect to /login
3. Enter API key: `ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI`
4. Should see authenticated app
5. Navigate to /knowledge - should load data
6. Check browser console - no 401 errors on initial load
7. Logout should work and redirect back to /login

## Expected Behavior After Fix

- Unauthenticated users redirected to /login
- Login page displays API key input
- After successful login, redirected to /knowledge
- API calls include Authorization header
- 401 responses trigger redirect to /login
- Logout clears credentials and redirects to /login

## Build Details

- Build completed: 2025-10-15
- Build time: 14.54s
- Bundle size: 1,394.89 kB (383.01 kB gzipped)
- Auth code verified in bundle

Created: 2025-10-15 | Timestamp: 10:59:00
