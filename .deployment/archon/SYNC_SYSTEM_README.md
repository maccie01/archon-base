# Documentation Sync System

Created: 2025-10-16

## Overview

This sync system keeps the Archon deployment documentation synchronized with the centralized server documentation folder at `/Users/janschubert/server/servers/archon/`.

## Purpose

- **Single Source of Truth**: Maintain deployment docs in the Archon repository
- **Centralized Access**: Provide easy access to server management docs in one location
- **Version Control**: Track changes in git while keeping server docs updated
- **Archive History**: Preserve old versions when files change

## Structure

### Source (This Repository)
```
/Users/janschubert/tools/archon/.deployment/archon/
├── core/                  # Essential operational docs
├── security/              # Security documentation
├── services/              # Service-specific guides
├── archive/               # Historical documentation
├── README.md              # Main deployment guide
├── QUICK_START.md         # Quick reference
└── SYNC_TO_SERVER_DOCS.sh # This sync script
```

### Target (Server Documentation)
```
/Users/janschubert/server/servers/archon/
├── core/                  # Synced from source
├── security/              # Synced from source
├── services/              # Synced from source
├── archive/               # Timestamped archives of changed files
│   ├── 20251016_083045/  # Archive from sync at this time
│   └── 20251016_140522/  # Another archive
├── 00_START_HERE.md       # Master navigation (generated)
├── QUICK_START.md         # Synced from source
└── DEPLOYMENT_README.md   # Synced from source
```

## How to Use

### Manual Sync

When you update deployment documentation, run:

```bash
cd /Users/janschubert/tools/archon/.deployment/archon
./SYNC_TO_SERVER_DOCS.sh
```

### What Gets Synced

**Always Synced**:
- `core/` directory (credentials, environment, docker config)
- `security/` directory (authentication, security docs)
- `services/` directory (supabase, arcane, mcp guides)
- `README.md` → `DEPLOYMENT_README.md`
- `QUICK_START.md`
- `INDEX.md` → `DOCUMENTATION_INDEX.md`
- Latest status reports (KNOWLEDGE_BASE_STATUS, etc.)

**Never Synced**:
- `archive/` directory (historical docs stay in repo only)
- `ORGANIZATION_PLAN.md` (internal to repo)
- `.git` directory
- Temporary files

### Archiving Behavior

When you run the sync script:

1. **New Files**: Copied directly to target
2. **Changed Files**:
   - Old version archived to `archive/YYYYMMDD_HHMMSS/`
   - New version copied to target
   - Archive includes full directory structure
3. **Unchanged Files**: Left as-is
4. **Empty Archives**: Automatically deleted

Example archive:
```
archive/20251016_083045/
├── ARCHIVE_INDEX.md           # List of what was archived
├── core/
│   └── CREDENTIALS.md         # Old version of credentials
└── security/
    └── AUTHENTICATION.md      # Old version of auth doc
```

### Archive Index

Each non-empty archive contains an `ARCHIVE_INDEX.md` with:
- Timestamp
- List of archived files
- Reason for archiving
- Instructions for restoration

## When to Sync

### Required Sync Triggers

Run sync after:
- ✅ Updating credentials (API keys, passwords)
- ✅ Changing service configurations
- ✅ Modifying deployment procedures
- ✅ Updating security documentation
- ✅ Creating new status reports
- ✅ Major documentation reorganizations

### Optional Sync

Consider syncing after:
- Minor typo fixes in documentation
- Adding clarifications to existing docs
- Updating timestamps or dates

## Workflow Example

### Scenario: New API Key Created

1. **Update Repository**:
   ```bash
   cd /Users/janschubert/tools/archon
   # Edit .deployment/archon/core/CREDENTIALS.md
   git add .deployment/archon/core/CREDENTIALS.md
   git commit -m "docs: update API key credentials"
   ```

2. **Sync to Server Docs**:
   ```bash
   ./deployment/archon/SYNC_TO_SERVER_DOCS.sh
   ```

3. **Verify**:
   ```bash
   cat /Users/janschubert/server/servers/archon/core/CREDENTIALS.md
   # Verify new API key is present
   ```

4. **Check Archive**:
   ```bash
   ls -la /Users/janschubert/server/servers/archon/archive/
   # Old credentials archived with timestamp
   ```

## Automation Options

### Git Hook (Post-Commit)

Add to `.git/hooks/post-commit`:
```bash
#!/bin/bash
# Auto-sync deployment docs after commit

CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD | grep "^\.deployment/archon/")

if [ -n "$CHANGED_FILES" ]; then
    echo "Deployment docs changed, syncing..."
    cd .deployment/archon
    ./SYNC_TO_SERVER_DOCS.sh
fi
```

### Cron Job (Scheduled)

Add to crontab for daily sync:
```bash
# Sync Archon docs daily at 2 AM
0 2 * * * cd /Users/janschubert/tools/archon/.deployment/archon && ./SYNC_TO_SERVER_DOCS.sh >> /tmp/archon_sync.log 2>&1
```

### Manual Reminder

Create an alias in `~/.zshrc` or `~/.bashrc`:
```bash
alias sync-archon-docs='cd /Users/janschubert/tools/archon/.deployment/archon && ./SYNC_TO_SERVER_DOCS.sh'
```

## Archive Management

### Viewing Archives

```bash
# List all archives
ls -la /Users/janschubert/server/servers/archon/archive/

# View specific archive index
cat /Users/janschubert/server/servers/archon/archive/20251016_083045/ARCHIVE_INDEX.md

# View archived file
cat /Users/janschubert/server/servers/archon/archive/20251016_083045/core/CREDENTIALS.md
```

### Restoring from Archive

To restore an archived file:
```bash
# Copy archived version back to current location
cp /Users/janschubert/server/servers/archon/archive/20251016_083045/core/CREDENTIALS.md \
   /Users/janschubert/server/servers/archon/core/CREDENTIALS.md
```

### Cleaning Old Archives

Archive directories are kept indefinitely. To clean old archives:

```bash
# Remove archives older than 90 days
find /Users/janschubert/server/servers/archon/archive/ \
  -maxdepth 1 -type d -mtime +90 -exec rm -rf {} \;

# Or keep only last 10 archives
cd /Users/janschubert/server/servers/archon/archive/
ls -t | tail -n +11 | xargs rm -rf
```

## Troubleshooting

### Script Fails with Permission Error

```bash
# Make script executable
chmod +x /Users/janschubert/tools/archon/.deployment/archon/SYNC_TO_SERVER_DOCS.sh
```

### Files Not Syncing

Check if directories exist:
```bash
ls -la /Users/janschubert/tools/archon/.deployment/archon/
ls -la /Users/janschubert/server/servers/archon/
```

### Archive Growing Too Large

```bash
# Check archive size
du -sh /Users/janschubert/server/servers/archon/archive/

# Clean old archives (keep last 5)
cd /Users/janschubert/server/servers/archon/archive/
ls -t | tail -n +6 | xargs rm -rf
```

## Best Practices

1. **Commit Before Sync**: Always commit changes to git before syncing
2. **Review Changes**: Check what files changed after sync
3. **Keep Archives**: Don't delete archives immediately - keep for 90+ days
4. **Document Changes**: Add comments in commits about why docs changed
5. **Test First**: If making major changes, test sync on a copy first

## Script Maintenance

### Adding New Directories

Edit `SYNC_TO_SERVER_DOCS.sh` to add new directories:

```bash
# Add after existing syncs
echo "📦 Syncing new directory..."
archive_directory "$SERVER_DOCS_DIR/new_directory" "new_directory"
rsync -av --delete \
    "$DEPLOYMENT_DIR/new_directory/" \
    "$SERVER_DOCS_DIR/new_directory/"
```

### Excluding Files

To exclude specific files from sync:

```bash
rsync -av --delete --exclude='SECRET_FILE.md' \
    "$DEPLOYMENT_DIR/core/" \
    "$SERVER_DOCS_DIR/core/"
```

## Related Documentation

- [README.md](./README.md) - Main deployment documentation
- [INDEX.md](./INDEX.md) - Documentation index
- [ORGANIZATION_PLAN.md](./ORGANIZATION_PLAN.md) - Documentation reorganization details

## Support

If you encounter issues with the sync system:

1. Check script output for errors
2. Verify both source and target directories exist
3. Ensure you have write permissions
4. Check disk space in archive directory
5. Review recent git commits for conflicts

---

**Created**: 2025-10-16
**Script Location**: `/Users/janschubert/tools/archon/.deployment/archon/SYNC_TO_SERVER_DOCS.sh`
**Target Location**: `/Users/janschubert/server/servers/archon/`
**Maintainer**: Jan Schubert
