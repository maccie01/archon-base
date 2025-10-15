# Quick Deploy Instructions

## The Problem
The production site is running Vite dev server instead of the production build, so auth code isn't loaded.

## The Fix (2 minutes)

### Option A: Automated Script (Easiest)
```bash
cd /Users/janschubert/tools/archon/archon-ui-main
./deploy-auth-fix.sh
```

### Option B: Manual Commands
```bash
# 1. Sync the built files
cd /Users/janschubert/tools/archon/archon-ui-main
rsync -avz --delete dist/ root@91.98.156.158:/opt/archon/archon-ui-main/dist/

# 2. Restart the container
ssh root@91.98.156.158 "cd /opt/archon/archon-ui-main && docker compose restart archon-ui"
```

## Verify It Works
1. Open: https://archon.nexorithm.io
2. Should redirect to /login ✓
3. Enter API key: `ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI`
4. Should see the knowledge base ✓

## What Changed
- Built production bundle with auth code
- Ready to deploy to server
- Will replace dev server with production build

## Files Ready for Deployment
- `/Users/janschubert/tools/archon/archon-ui-main/dist/` - Production bundle (built)
- All auth code included in bundle
- File size: 1.4 MB (383 KB gzipped)

Created: 2025-10-15 | Timestamp: 11:05:00
