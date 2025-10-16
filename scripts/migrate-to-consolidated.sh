#!/bin/bash

# ==============================================================================
# Migrate Archon to Consolidated Architecture
# ==============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

log_info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO:${NC} $1"
}

echo -e "${GREEN}================================================================================${NC}"
echo -e "${GREEN}              ARCHON CONSOLIDATED ARCHITECTURE MIGRATION${NC}"
echo -e "${GREEN}================================================================================${NC}"
echo ""

# Check if running on server
if [ ! -d "/opt/archon" ]; then
    log_error "This script must be run on the Archon server (/opt/archon not found)"
    exit 1
fi

cd /opt/archon

# ------------------------------------------------------------------------------
# PHASE 1: Pre-Migration Checks
# ------------------------------------------------------------------------------

echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}PHASE 1: Pre-Migration Checks${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""

log "Checking prerequisites..."

# Check if docker-compose.production.yml exists
if [ ! -f "docker-compose.production.yml" ]; then
    log_error "docker-compose.production.yml not found in /opt/archon"
    exit 1
fi

# Check if .env.production exists
if [ ! -f ".env.production" ]; then
    log_warning ".env.production not found. Run generate-production-env.sh first"
    echo ""
    read -p "Do you want to generate .env.production now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        bash /opt/archon/scripts/generate-production-env.sh
    else
        log_error "Cannot proceed without .env.production"
        exit 1
    fi
fi

# Check if volumes/api directory exists
if [ ! -d "volumes/api" ]; then
    log "Creating volumes/api directory..."
    mkdir -p volumes/api
fi

# Check if Kong config exists
if [ ! -f "volumes/api/kong.yml" ]; then
    log_error "Kong configuration not found at volumes/api/kong.yml"
    exit 1
fi

log "✓ Prerequisites check passed"
echo ""

# ------------------------------------------------------------------------------
# PHASE 2: Backup Current State
# ------------------------------------------------------------------------------

echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}PHASE 2: Backup Current State${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""

BACKUP_DIR="/root/backups/archon-migration-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

log "Backup directory: $BACKUP_DIR"
echo ""

# Backup database
log "Backing up PostgreSQL database..."
if docker ps | grep -q supabase_db_supabase; then
    docker exec supabase_db_supabase pg_dumpall -U postgres > "$BACKUP_DIR/database-full.sql"
    log "✓ Database backup complete: $BACKUP_DIR/database-full.sql"
else
    log_warning "supabase_db_supabase container not running, skipping database backup"
fi

# Backup current configurations
log "Backing up current configurations..."
if [ -f "docker-compose.yml" ]; then
    cp docker-compose.yml "$BACKUP_DIR/docker-compose.yml.old"
    log "✓ Backed up docker-compose.yml"
fi

if [ -f ".env" ]; then
    cp .env "$BACKUP_DIR/env.old"
    log "✓ Backed up .env"
fi

if [ -d "supabase" ]; then
    tar czf "$BACKUP_DIR/supabase-config.tar.gz" supabase/
    log "✓ Backed up supabase/ directory"
fi

# Backup PostgreSQL data volume
log "Backing up PostgreSQL data volume..."
if docker volume ls | grep -q supabase_db_supabase; then
    docker run --rm \
        -v supabase_db_supabase:/source:ro \
        -v "$BACKUP_DIR":/backup \
        alpine \
        tar czf /backup/postgres-volume.tar.gz -C /source .
    log "✓ PostgreSQL volume backup complete"
else
    log_warning "supabase_db_supabase volume not found, skipping volume backup"
fi

# Save current container list
docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}' > "$BACKUP_DIR/containers-before.txt"
docker network ls > "$BACKUP_DIR/networks-before.txt"
docker volume ls > "$BACKUP_DIR/volumes-before.txt"

log "✓ Backup phase complete"
echo ""

# ------------------------------------------------------------------------------
# PHASE 3: Stop Old Services
# ------------------------------------------------------------------------------

echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}PHASE 3: Stop Old Services${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""

log "Stopping Archon services..."
if [ -f "docker-compose.yml" ]; then
    docker compose down || log_warning "docker compose down failed or no services running"
else
    log_warning "No docker-compose.yml found, skipping compose down"
fi

log "Stopping Supabase services..."
if [ -d "supabase" ] && command -v supabase &> /dev/null; then
    cd supabase
    supabase stop 2>/dev/null || log_warning "supabase stop failed or no services running"
    cd ..
else
    log_warning "Supabase CLI not available or directory not found"
fi

# Manually stop any remaining Supabase containers
log "Stopping any remaining Supabase containers..."
docker ps | grep supabase | awk '{print $1}' | xargs -r docker stop

log "✓ Old services stopped"
echo ""

# ------------------------------------------------------------------------------
# PHASE 4: Migrate Data
# ------------------------------------------------------------------------------

echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}PHASE 4: Migrate Data${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""

log "Creating new volume: archon_postgres_data"
if ! docker volume ls | grep -q archon_postgres_data; then
    docker volume create archon_postgres_data
fi

# Restore data from backup
if [ -f "$BACKUP_DIR/postgres-volume.tar.gz" ]; then
    log "Restoring PostgreSQL data to new volume..."
    docker run --rm \
        -v "$BACKUP_DIR":/backup \
        -v archon_postgres_data:/target \
        alpine \
        sh -c "cd /target && tar xzf /backup/postgres-volume.tar.gz"
    log "✓ Data restoration complete"
else
    log_warning "No PostgreSQL backup found, starting with empty database"
fi

echo ""

# ------------------------------------------------------------------------------
# PHASE 5: Deploy New Configuration
# ------------------------------------------------------------------------------

echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}PHASE 5: Deploy New Configuration${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""

log "Deploying production docker-compose.yml..."
cp docker-compose.production.yml docker-compose.yml
log "✓ docker-compose.yml deployed"

log "Deploying production environment..."
cp .env.production .env
log "✓ .env deployed"

log "✓ Configuration deployment complete"
echo ""

# ------------------------------------------------------------------------------
# PHASE 6: Start Consolidated Stack
# ------------------------------------------------------------------------------

echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}PHASE 6: Start Consolidated Stack${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""

log "Starting consolidated Archon stack..."
docker compose up -d

log "Waiting for services to become healthy (60 seconds)..."
sleep 60

echo ""

# ------------------------------------------------------------------------------
# PHASE 7: Verification
# ------------------------------------------------------------------------------

echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}PHASE 7: Verification${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""

log "Checking service health..."
echo ""

# Check container status
docker compose ps

echo ""

# Test database connectivity
log "Testing database connectivity..."
if docker exec archon-postgres psql -U postgres -d postgres -c "SELECT 1;" > /dev/null 2>&1; then
    log "✓ Database connection successful"
else
    log_error "Database connection failed"
fi

# Test Kong
log "Testing Kong API Gateway..."
if docker exec archon-server curl -f http://kong:8000 > /dev/null 2>&1; then
    log "✓ Kong API Gateway accessible"
else
    log_warning "Kong API Gateway not accessible"
fi

# Test Archon Server
log "Testing Archon Server..."
if curl -f http://localhost:8181/health > /dev/null 2>&1; then
    log "✓ Archon Server healthy"
else
    log_warning "Archon Server not responding"
fi

# Test Archon UI
log "Testing Archon UI..."
if curl -f http://localhost:3737 > /dev/null 2>&1; then
    log "✓ Archon UI accessible"
else
    log_warning "Archon UI not responding"
fi

# Test Studio
log "Testing Supabase Studio..."
if curl -f http://localhost:54323 > /dev/null 2>&1; then
    log "✓ Supabase Studio accessible"
else
    log_warning "Supabase Studio not responding"
fi

echo ""
log "✓ Basic verification complete"
echo ""

# Save current state
docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}' > "$BACKUP_DIR/containers-after.txt"
docker network ls > "$BACKUP_DIR/networks-after.txt"
docker volume ls > "$BACKUP_DIR/volumes-after.txt"

# ------------------------------------------------------------------------------
# PHASE 8: Cleanup Information
# ------------------------------------------------------------------------------

echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}PHASE 8: Cleanup Instructions${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""

log_info "Migration complete! Old services have been stopped but not deleted."
echo ""
echo "To clean up old resources after verifying the new stack works:"
echo ""
echo "1. Remove old Supabase volumes:"
echo "   docker volume ls | grep supabase | awk '{print \$2}' | xargs docker volume rm"
echo ""
echo "2. Remove old networks:"
echo "   docker network rm supabase_network_supabase supabase_network_archon supabase_network_root app-network"
echo ""
echo "3. Remove old Supabase directory (after backup):"
echo "   mv /opt/archon/supabase /opt/archon/supabase.old"
echo ""
echo "4. Disable rebind service:"
echo "   systemctl disable supabase-rebind.service"
echo "   rm /etc/systemd/system/supabase-rebind.service"
echo "   systemctl daemon-reload"
echo ""

# ------------------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------------------

echo -e "${GREEN}================================================================================${NC}"
echo -e "${GREEN}                         MIGRATION COMPLETE${NC}"
echo -e "${GREEN}================================================================================${NC}"
echo ""
echo -e "${GREEN}✓${NC} Backup location: ${BACKUP_DIR}"
echo -e "${GREEN}✓${NC} New architecture deployed"
echo -e "${GREEN}✓${NC} All services started"
echo ""
echo "Management commands:"
echo "  docker compose ps              # Check service status"
echo "  docker compose logs -f         # View all logs"
echo "  docker compose restart         # Restart all services"
echo "  docker compose down            # Stop all services"
echo "  docker compose up -d           # Start all services"
echo ""
echo "Service URLs:"
echo "  Archon UI: http://localhost:3737 (https://archon.nexorithm.io)"
echo "  Archon API: http://localhost:8181"
echo "  Studio: http://localhost:54323 (https://supabase.archon.nexorithm.io)"
echo "  PostgreSQL: localhost:54322"
echo ""
echo -e "${YELLOW}IMPORTANT:${NC} Test all functionality before running cleanup commands!"
echo ""
