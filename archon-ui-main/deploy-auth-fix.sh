#!/bin/bash

# Deploy Authentication Fix Script
# Created: 2025-10-15

set -e

SERVER="root@91.98.156.158"
REMOTE_PATH="/opt/archon/archon-ui-main"
LOCAL_DIST="dist"

echo "Starting deployment of authentication fix..."
echo ""

# Check if dist folder exists
if [ ! -d "$LOCAL_DIST" ]; then
    echo "Error: dist folder not found. Running build..."
    npm run build
fi

echo "Step 1: Syncing dist folder to server..."
rsync -avz --delete "$LOCAL_DIST/" "$SERVER:$REMOTE_PATH/dist/"

if [ $? -eq 0 ]; then
    echo "✓ Files synced successfully"
else
    echo "✗ Failed to sync files"
    exit 1
fi

echo ""
echo "Step 2: Restarting archon-ui container..."
ssh "$SERVER" "cd $REMOTE_PATH && docker compose restart archon-ui"

if [ $? -eq 0 ]; then
    echo "✓ Container restarted successfully"
else
    echo "✗ Failed to restart container"
    exit 1
fi

echo ""
echo "Deployment completed successfully!"
echo ""
echo "Please verify at: https://archon.nexorithm.io"
echo "Expected: Should redirect to /login page"
echo ""
echo "Test API key: ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI"
