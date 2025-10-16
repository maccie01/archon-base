#!/bin/bash

# Archon Deployment Documentation Sync Script
# Syncs deployment documentation to centralized server documentation folder
# Usage: ./SYNC_TO_SERVER_DOCS.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paths
DEPLOYMENT_DIR="/Users/janschubert/tools/archon/.deployment/archon"
SERVER_DOCS_DIR="/Users/janschubert/server/servers/archon"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Archon Documentation Sync${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if server docs directory exists
if [ ! -d "$SERVER_DOCS_DIR" ]; then
    echo -e "${RED}Error: Server docs directory does not exist: $SERVER_DOCS_DIR${NC}"
    exit 1
fi

# Check if deployment directory exists
if [ ! -d "$DEPLOYMENT_DIR" ]; then
    echo -e "${RED}Error: Deployment directory does not exist: $DEPLOYMENT_DIR${NC}"
    exit 1
fi

echo -e "${YELLOW}Source:${NC} $DEPLOYMENT_DIR"
echo -e "${YELLOW}Target:${NC} $SERVER_DOCS_DIR"
echo ""

# Create subdirectories in server docs if they don't exist
mkdir -p "$SERVER_DOCS_DIR/core"
mkdir -p "$SERVER_DOCS_DIR/security"
mkdir -p "$SERVER_DOCS_DIR/services"
mkdir -p "$SERVER_DOCS_DIR/archive"

# Create archive directory with timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ARCHIVE_DIR="$SERVER_DOCS_DIR/archive/$TIMESTAMP"
mkdir -p "$ARCHIVE_DIR"

echo -e "${GREEN}Syncing documentation...${NC}"
echo -e "${YELLOW}Archive location:${NC} $ARCHIVE_DIR"
echo ""

# Function to archive file if it exists and differs from source
archive_if_different() {
    local source=$1
    local target=$2
    local archive_path=$3

    if [ -f "$target" ]; then
        # Check if files differ
        if ! cmp -s "$source" "$target"; then
            # Files are different, archive the old version
            local relative_path=$(echo "$target" | sed "s|$SERVER_DOCS_DIR/||")
            local archive_file="$archive_path/$relative_path"
            mkdir -p "$(dirname "$archive_file")"
            cp "$target" "$archive_file"
            echo -e "  ${YELLOW}→${NC} Archived: $relative_path"
        fi
    fi
}

# Function to archive entire directory before sync
archive_directory() {
    local target_dir=$1
    local archive_subdir=$2

    if [ -d "$target_dir" ]; then
        # Archive all existing files in directory
        find "$target_dir" -type f | while read -r file; do
            local relative_path=$(echo "$file" | sed "s|$SERVER_DOCS_DIR/||")
            local archive_file="$ARCHIVE_DIR/$archive_subdir/$relative_path"
            mkdir -p "$(dirname "$archive_file")"
            cp "$file" "$archive_file"
        done
    fi
}

# Sync core operational files (always current)
echo "📄 Syncing core documentation..."
archive_directory "$SERVER_DOCS_DIR/core" "core"
rsync -av --delete \
    "$DEPLOYMENT_DIR/core/" \
    "$SERVER_DOCS_DIR/core/"

# Sync security documentation
echo "🔒 Syncing security documentation..."
archive_directory "$SERVER_DOCS_DIR/security" "security"
rsync -av --delete \
    "$DEPLOYMENT_DIR/security/" \
    "$SERVER_DOCS_DIR/security/"

# Sync service-specific documentation
echo "⚙️  Syncing service documentation..."
archive_directory "$SERVER_DOCS_DIR/services" "services"
rsync -av --delete \
    "$DEPLOYMENT_DIR/services/" \
    "$SERVER_DOCS_DIR/services/"

# Sync root-level essential files
echo "📋 Syncing root-level files..."
archive_if_different "$DEPLOYMENT_DIR/README.md" "$SERVER_DOCS_DIR/DEPLOYMENT_README.md" "$ARCHIVE_DIR"
cp "$DEPLOYMENT_DIR/README.md" "$SERVER_DOCS_DIR/DEPLOYMENT_README.md"

archive_if_different "$DEPLOYMENT_DIR/QUICK_START.md" "$SERVER_DOCS_DIR/QUICK_START.md" "$ARCHIVE_DIR"
cp "$DEPLOYMENT_DIR/QUICK_START.md" "$SERVER_DOCS_DIR/QUICK_START.md"

archive_if_different "$DEPLOYMENT_DIR/INDEX.md" "$SERVER_DOCS_DIR/DOCUMENTATION_INDEX.md" "$ARCHIVE_DIR"
cp "$DEPLOYMENT_DIR/INDEX.md" "$SERVER_DOCS_DIR/DOCUMENTATION_INDEX.md"

# Sync latest status reports
echo "📊 Syncing status reports..."
if [ -f "$DEPLOYMENT_DIR/KNOWLEDGE_BASE_STATUS_2025-10-16.md" ]; then
    archive_if_different "$DEPLOYMENT_DIR/KNOWLEDGE_BASE_STATUS_2025-10-16.md" "$SERVER_DOCS_DIR/KNOWLEDGE_BASE_STATUS_2025-10-16.md" "$ARCHIVE_DIR"
    cp "$DEPLOYMENT_DIR/KNOWLEDGE_BASE_STATUS_2025-10-16.md" "$SERVER_DOCS_DIR/"
fi

if [ -f "$DEPLOYMENT_DIR/REORGANIZATION_SUMMARY.md" ]; then
    archive_if_different "$DEPLOYMENT_DIR/REORGANIZATION_SUMMARY.md" "$SERVER_DOCS_DIR/REORGANIZATION_SUMMARY.md" "$ARCHIVE_DIR"
    cp "$DEPLOYMENT_DIR/REORGANIZATION_SUMMARY.md" "$SERVER_DOCS_DIR/"
fi

# Create index file in server docs
echo "📑 Creating master index..."
cat > "$SERVER_DOCS_DIR/00_START_HERE.md" << 'EOF'
# Archon Server Documentation

**Last Synced**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Server**: netzwaechter-prod (91.98.156.158)
**Domain**: https://archon.nexorithm.io

---

## Quick Navigation

### 🚀 Getting Started
- [QUICK_START.md](./QUICK_START.md) - 5-minute quick reference
- [DEPLOYMENT_README.md](./DEPLOYMENT_README.md) - Complete deployment guide
- [DOCUMENTATION_INDEX.md](./DOCUMENTATION_INDEX.md) - Full documentation index

### 🔐 Access & Security
- [core/CREDENTIALS.md](./core/CREDENTIALS.md) - All credentials (API keys, SSH, passwords)
- [security/AUTHENTICATION.md](./security/AUTHENTICATION.md) - Authentication system
- [security/README.md](./security/README.md) - Security overview

### ⚙️ Configuration
- [core/ENVIRONMENT.md](./core/ENVIRONMENT.md) - Environment variables
- [core/DOCKER_SETUP.md](./core/DOCKER_SETUP.md) - Docker configuration
- [core/DEPLOYMENT_SUMMARY.md](./core/DEPLOYMENT_SUMMARY.md) - Deployment details

### 🛠️ Services
- [services/supabase/README.md](./services/supabase/README.md) - Supabase (database)
- [services/arcane/README.md](./services/arcane/README.md) - Arcane (Docker UI)
- [services/mcp/MCP_SETUP_GUIDE.md](./services/mcp/MCP_SETUP_GUIDE.md) - MCP server

### 📊 Current Status
- [KNOWLEDGE_BASE_STATUS_2025-10-16.md](./KNOWLEDGE_BASE_STATUS_2025-10-16.md) - KB status

---

## Documentation Structure

This folder is automatically synchronized from the Archon repository deployment documentation.

**Source**: `/Users/janschubert/tools/archon/.deployment/archon/`
**Sync Script**: Run `./SYNC_TO_SERVER_DOCS.sh` in source directory

### Folder Structure

```
archon/
├── 00_START_HERE.md              # This file
├── QUICK_START.md                # Quick reference
├── DEPLOYMENT_README.md          # Main deployment guide
├── DOCUMENTATION_INDEX.md        # Complete index
│
├── core/                         # Essential operational docs
│   ├── CREDENTIALS.md            # ⚠️ SENSITIVE
│   ├── ENVIRONMENT.md
│   ├── DOCKER_SETUP.md
│   └── DEPLOYMENT_SUMMARY.md
│
├── security/                     # Security documentation
│   ├── README.md
│   └── AUTHENTICATION.md
│
└── services/                     # Service-specific guides
    ├── supabase/
    ├── arcane/
    └── mcp/
```

---

## Quick Commands

### SSH Access
```bash
ssh -i ~/.ssh/netzwaechter_deployment root@91.98.156.158
```

### Health Checks
```bash
# All containers
docker ps | grep -E 'archon|supabase'

# API health
curl http://localhost:8181/health
```

### View Logs
```bash
docker logs -f archon-server
docker logs -f archon-ui
```

### Restart Services
```bash
cd /opt/archon && docker compose restart
```

---

## Important Notes

⚠️ **CREDENTIALS**: The `core/CREDENTIALS.md` file contains sensitive information. Handle with extreme care.

🔄 **Sync Status**: This documentation is synchronized from the main repository. To update:
1. Make changes in `/Users/janschubert/tools/archon/.deployment/archon/`
2. Run sync script
3. Or manually copy updated files

📝 **Archive**: Historical documentation is available in the source repository under `archive/` but not synced here to keep this folder focused on current operations.

---

**Maintainer**: Jan Schubert
**Repository**: https://github.com/maccie01/archon-base
**Branch**: stable
EOF

# Update timestamp in index
sed -i '' "s/\$(date -u +\"%Y-%m-%d %H:%M:%S UTC\")/$(date -u +"%Y-%m-%d %H:%M:%S UTC")/" "$SERVER_DOCS_DIR/00_START_HERE.md"

# Clean up archive directory if empty
ARCHIVED_FILES=$(find "$ARCHIVE_DIR" -type f | wc -l | tr -d ' ')
if [ "$ARCHIVED_FILES" -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓${NC} No files were changed - archive directory removed"
    rm -rf "$ARCHIVE_DIR"
else
    echo ""
    echo -e "${YELLOW}📦 Archived $ARCHIVED_FILES changed file(s) to:${NC}"
    echo "   $ARCHIVE_DIR"

    # Create archive index
    cat > "$ARCHIVE_DIR/ARCHIVE_INDEX.md" << EOF
# Archive: $TIMESTAMP

**Date**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Total Files Archived**: $ARCHIVED_FILES

## Archived Files

\`\`\`
$(find "$ARCHIVE_DIR" -type f ! -name "ARCHIVE_INDEX.md" | sed "s|$ARCHIVE_DIR/||" | sort)
\`\`\`

## Why These Files Were Archived

These files were archived because they were modified or replaced during a documentation sync from the Archon repository.

**Source**: /Users/janschubert/tools/archon/.deployment/archon/
**Target**: $SERVER_DOCS_DIR

To restore a file, simply copy it from this archive back to its original location.

---

**Created**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
EOF
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Sync Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Documentation synced to: ${YELLOW}$SERVER_DOCS_DIR${NC}"
echo ""

if [ "$ARCHIVED_FILES" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Changed files archived to:${NC}"
    echo "   $ARCHIVE_DIR"
    echo ""
fi

echo "Quick Access:"
echo "  • Navigation: $SERVER_DOCS_DIR/00_START_HERE.md"
echo "  • Quick Start: $SERVER_DOCS_DIR/QUICK_START.md"
echo "  • Credentials: $SERVER_DOCS_DIR/core/CREDENTIALS.md"
echo ""
echo "Next steps:"
echo "  1. Review synced files in $SERVER_DOCS_DIR"
echo "  2. Check 00_START_HERE.md for navigation"
echo "  3. Verify credentials are up to date"
echo ""
