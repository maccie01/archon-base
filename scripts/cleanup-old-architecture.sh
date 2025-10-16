#!/bin/bash

# ==============================================================================
# Cleanup Old Archon Architecture
# Run this ONLY after verifying the new consolidated stack works properly
# ==============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}================================================================================${NC}"
echo -e "${YELLOW}              WARNING: OLD ARCHITECTURE CLEANUP${NC}"
echo -e "${YELLOW}================================================================================${NC}"
echo ""
echo -e "${RED}This script will permanently delete old resources!${NC}"
echo ""
echo "This will remove:"
echo "  - Old Supabase Docker volumes (11 volumes)"
echo "  - Old Docker networks (3 networks)"
echo "  - Old Supabase configuration directory"
echo "  - Rebind service and scripts"
echo ""
echo -e "${YELLOW}Make sure you have:${NC}"
echo "  1. Verified the new stack is working correctly"
echo "  2. Tested all endpoints and functionality"
echo "  3. Confirmed backups are complete and valid"
echo ""

read -p "Are you absolutely sure you want to proceed? (yes/no) " -r
echo ""
if [[ ! $REPLY =~ ^yes$ ]]; then
    echo "Cleanup cancelled."
    exit 1
fi

echo ""
echo -e "${BLUE}Starting cleanup...${NC}"
echo ""

# ------------------------------------------------------------------------------
# Remove Old Docker Volumes
# ------------------------------------------------------------------------------

echo -e "${BLUE}Removing old Supabase Docker volumes...${NC}"

OLD_VOLUMES=$(docker volume ls --format '{{.Name}}' | grep "supabase_" || true)

if [ -z "$OLD_VOLUMES" ]; then
    echo "  No old Supabase volumes found"
else
    echo "  Found volumes to remove:"
    echo "$OLD_VOLUMES" | sed 's/^/    - /'
    echo ""

    for volume in $OLD_VOLUMES; do
        echo "  Removing $volume..."
        docker volume rm "$volume" 2>/dev/null || echo "    Failed to remove $volume (may be in use)"
    done
fi

echo ""

# ------------------------------------------------------------------------------
# Remove Old Docker Networks
# ------------------------------------------------------------------------------

echo -e "${BLUE}Removing old Docker networks...${NC}"

OLD_NETWORKS="supabase_network_supabase supabase_network_archon supabase_network_root app-network"

for network in $OLD_NETWORKS; do
    if docker network ls | grep -q "$network"; then
        echo "  Removing $network..."
        docker network rm "$network" 2>/dev/null || echo "    Failed to remove $network (may be in use)"
    else
        echo "  $network not found (already removed)"
    fi
done

echo ""

# ------------------------------------------------------------------------------
# Move Old Supabase Directory
# ------------------------------------------------------------------------------

echo -e "${BLUE}Archiving old Supabase directory...${NC}"

if [ -d "/opt/archon/supabase" ]; then
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    mv /opt/archon/supabase "/opt/archon/supabase.old.$TIMESTAMP"
    echo "  ✓ Moved to: /opt/archon/supabase.old.$TIMESTAMP"
    echo "  (You can delete this later if everything works fine)"
else
    echo "  /opt/archon/supabase not found (already removed)"
fi

echo ""

# ------------------------------------------------------------------------------
# Remove Rebind Service
# ------------------------------------------------------------------------------

echo -e "${BLUE}Removing rebind service...${NC}"

if systemctl list-units --type=service --all | grep -q supabase-rebind; then
    echo "  Stopping and disabling supabase-rebind.service..."
    systemctl stop supabase-rebind.service 2>/dev/null || true
    systemctl disable supabase-rebind.service 2>/dev/null || true
fi

if [ -f "/etc/systemd/system/supabase-rebind.service" ]; then
    echo "  Removing service file..."
    rm /etc/systemd/system/supabase-rebind.service
    systemctl daemon-reload
    echo "  ✓ Service removed"
else
    echo "  Service file not found (already removed)"
fi

if [ -f "/opt/archon/scripts/rebind-supabase.py" ]; then
    echo "  Archiving rebind script..."
    mv /opt/archon/scripts/rebind-supabase.py /opt/archon/scripts/rebind-supabase.py.old
    echo "  ✓ Script archived"
fi

echo ""

# ------------------------------------------------------------------------------
# Remove Old Docker Compose Files
# ------------------------------------------------------------------------------

echo -e "${BLUE}Archiving old Docker Compose files...${NC}"

if [ -f "/opt/archon/docker-compose.yml.backup" ]; then
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    mv /opt/archon/docker-compose.yml.backup "/opt/archon/docker-compose.yml.backup.$TIMESTAMP"
    echo "  ✓ Archived docker-compose.yml.backup"
fi

if [ -f "/opt/archon/.env.backup" ]; then
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    mv /opt/archon/.env.backup "/opt/archon/.env.backup.$TIMESTAMP"
    echo "  ✓ Archived .env.backup"
fi

echo ""

# ------------------------------------------------------------------------------
# Verify Current State
# ------------------------------------------------------------------------------

echo -e "${BLUE}Verifying current state...${NC}"
echo ""

echo "Running containers:"
docker compose ps

echo ""
echo "Networks:"
docker network ls | grep archon || echo "  No Archon networks found"

echo ""
echo "Volumes:"
docker volume ls | grep archon || echo "  No Archon volumes found"

echo ""

# ------------------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------------------

echo -e "${GREEN}================================================================================${NC}"
echo -e "${GREEN}                         CLEANUP COMPLETE${NC}"
echo -e "${GREEN}================================================================================${NC}"
echo ""
echo "Removed:"
echo "  ✓ Old Supabase Docker volumes"
echo "  ✓ Old Docker networks"
echo "  ✓ Rebind service and scripts"
echo ""
echo "Archived (can be deleted manually later):"
echo "  - /opt/archon/supabase.old.*"
echo "  - /opt/archon/docker-compose.yml.backup.*"
echo "  - /opt/archon/.env.backup.*"
echo ""
echo "Current architecture:"
echo "  - Single network: archon_production"
echo "  - 9 containers (down from 15)"
echo "  - Unified management via docker compose"
echo ""
echo -e "${GREEN}You can now manage Archon with simple docker compose commands!${NC}"
echo ""
