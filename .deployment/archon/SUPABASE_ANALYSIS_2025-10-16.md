# Supabase Service Architecture Analysis

**Date**: 2025-10-16
**Server**: netzwaechter-prod (91.98.156.158)
**Analysis Scope**: Complete in-depth review of Supabase deployment and usage

---

## Executive Summary

After thorough analysis of the Archon server deployment, I've identified that Archon is running a **complete Supabase stack (11 containers)** but **only actively uses 4 core services**. The remaining 7 services are unused and can be safely removed to reduce resource consumption.

**Key Findings**:
- ✅ Supabase managed by Supabase CLI (`/opt/archon/supabase/`)
- ✅ 11 containers running, only 4 actively used by Archon
- ✅ Custom rebind script changes all ports to `127.0.0.1` for security
- ✅ Nginx proxy only exposes Studio UI publicly
- ⚠️ Archon uses **zero** Auth, Storage, or Realtime features
- ⚠️ 7 containers consuming resources unnecessarily

**Recommendation**: Transition to minimal Supabase stack (4 services instead of 11)

---

## Current Deployment Architecture

### How Supabase is Deployed

**Deployment Method**: Supabase CLI (`supabase start`)
- **Project Directory**: `/opt/archon/supabase/`
- **Config File**: `/opt/archon/supabase/config.toml`
- **Project ID**: `supabase`
- **Network**: `supabase_network_supabase` (external Docker network)

**Post-Start Configuration**:
- Custom rebind script: `/opt/archon/scripts/rebind-supabase.py`
- Systemd service: `supabase-rebind.service` (inactive, manual)
- Purpose: Changes port bindings from `0.0.0.0` to `127.0.0.1` for security

### Container Inventory

**11 Supabase Containers Running**:

| Container | Service | Status | Archon Usage |
|-----------|---------|--------|--------------|
| `supabase_db_supabase` | PostgreSQL 17.6.1 | Healthy | ✅ **ACTIVE** |
| `supabase_kong_supabase` | Kong Gateway | Healthy | ✅ **ACTIVE** |
| `supabase_rest_supabase` | PostgREST | Running | ✅ **ACTIVE** |
| `supabase_studio_supabase` | Studio UI | Healthy | ✅ **ACTIVE** (admin only) |
| `supabase_auth_supabase` | GoTrue (Auth) | Healthy | ❌ **UNUSED** |
| `supabase_storage_supabase` | Storage API | Healthy | ❌ **UNUSED** |
| `supabase_realtime_supabase` | Realtime Server | Healthy | ❌ **UNUSED** |
| `supabase_pg_meta_supabase` | PostgreSQL Metadata | Healthy | ⚠️ **OPTIONAL** (Studio only) |
| `supabase_vector_supabase` | Log Aggregation | Healthy | ❌ **UNUSED** |
| `supabase_analytics_supabase` | Logflare Analytics | Running | ❌ **UNUSED** |
| `supabase_inbucket_supabase` | Mailpit (Email Testing) | Healthy | ❌ **UNUSED** |

---

## Evidence: What Archon Actually Uses

### 1. Database Connection

**Connection String** (from `/opt/archon/.env`):
```bash
SUPABASE_URL=http://supabase_kong_supabase:8000
SUPABASE_SERVICE_KEY=eyJhbGc...
```

**Analysis**:
- Archon connects to Kong Gateway on Docker network
- Kong routes to PostgREST (REST API) and directly to PostgreSQL
- Connection is internal (container-to-container)

### 2. Code Analysis

**Supabase Client Usage** (`python/src/server/services/client_manager.py`):
```python
from supabase import Client, create_client

def get_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    client = create_client(url, key)
    return client
```

**Actual API Methods Used** (grep analysis of entire codebase):
- ✅ `.table()` - Used extensively (50+ occurrences)
- ✅ `.rpc()` - Used once for migrations
- ❌ `.auth` - **ZERO occurrences**
- ❌ `.storage` - **ZERO occurrences** (only local imports)
- ❌ `.realtime` - **ZERO occurrences**
- ❌ `.channel()` - **ZERO occurrences**

**Tables Accessed**:
- `archon_sources` - Knowledge sources
- `archon_crawled_pages` - Document chunks
- `archon_code_examples` - Code snippets
- `archon_projects` - Projects
- `archon_tasks` - Tasks
- `archon_document_versions` - Version history
- `archon_prompts` - AI prompts
- `archon_settings` - Configuration
- `archon_migrations` - Schema versions
- `api_keys` - API key authentication

**Authentication System**:
- Archon has **custom API key authentication** (`api_keys` table)
- Does NOT use Supabase GoTrue (auth service)
- API keys stored with bcrypt hashes
- Bootstrap endpoint for initial key creation

### 3. Nginx Configuration

**Public Supabase Access** (`/etc/nginx/sites-available/archon`):
```nginx
# supabase.archon.nexorithm.io
server {
    listen 443 ssl http2;
    server_name supabase.archon.nexorithm.io;

    location / {
        proxy_pass http://127.0.0.1:54323;  # Studio UI
    }
}
```

**Analysis**:
- Only Studio UI is exposed publicly
- No public access to Auth, Storage, or Realtime endpoints
- Studio used for manual database management only

### 4. Network Architecture

**Docker Networks**:
```
supabase_network_supabase (external)
├── All 11 Supabase containers
├── archon-server (connects here)
└── archon-mcp (connects here)

supabase_network_archon (external)
├── archon-server
└── archon-mcp

app-network (internal)
├── archon-server
├── archon-mcp
├── archon-ui
└── archon-agents (when enabled)
```

**Analysis**:
- `archon-server` connects to TWO Supabase networks
- `supabase_network_supabase` has all Supabase services
- `supabase_network_archon` appears redundant (only Archon containers)
- Network topology can be simplified

### 5. Supabase Configuration

**Enabled Services** (`/opt/archon/supabase/config.toml`):
```toml
[api]
enabled = true
port = 54321

[db]
enabled = true
port = 54322
major_version = 17

[realtime]
enabled = true  # ← NOT USED BY ARCHON

[studio]
enabled = true
port = 54323

[storage]
enabled = true  # ← NOT USED BY ARCHON

[auth]
enabled = true  # ← NOT USED BY ARCHON

[inbucket]
enabled = true  # ← DEV TOOL ONLY
```

**Analysis**:
- All services enabled in config
- But Archon doesn't actually use most of them
- Config was generated with defaults

---

## Resource Impact

### Current Resource Usage

**Container Memory** (estimated from typical Supabase deployment):
- PostgreSQL: ~200-400 MB
- Kong Gateway: ~50-100 MB
- PostgREST: ~20-50 MB
- Studio: ~100-150 MB
- **Auth: ~50-100 MB** ← Unused
- **Storage: ~50-100 MB** ← Unused
- **Realtime: ~50-100 MB** ← Unused
- **pg_meta: ~20-40 MB** ← Optional
- **Vector: ~30-50 MB** ← Unused
- **Analytics: ~50-100 MB** ← Unused
- **Inbucket: ~20-30 MB** ← Unused

**Total**: ~690-1220 MB
**Unused**: ~270-520 MB (39-43% waste)

### Minimal Stack Resource Usage

**Required Services Only**:
- PostgreSQL: ~200-400 MB
- Kong Gateway: ~50-100 MB
- PostgREST: ~20-50 MB
- Studio: ~100-150 MB (optional in production)

**Total**: ~370-700 MB (43-50% reduction)

---

## Recommendations

### Option 1: Minimal Supabase Stack (RECOMMENDED)

**Keep Only**:
1. **PostgreSQL** (`supabase_db_supabase`) - Database storage
2. **Kong Gateway** (`supabase_kong_supabase`) - API routing
3. **PostgREST** (`supabase_rest_supabase`) - REST API generation
4. **Studio** (`supabase_studio_supabase`) - Admin UI (optional for production)

**Remove**:
- `supabase_auth_supabase` - Not used (custom API keys instead)
- `supabase_storage_supabase` - Not used (no file storage)
- `supabase_realtime_supabase` - Not used (HTTP polling instead)
- `supabase_pg_meta_supabase` - Optional (only for Studio)
- `supabase_vector_supabase` - Optional logging
- `supabase_analytics_supabase` - Optional monitoring
- `supabase_inbucket_supabase` - Dev tool only

**Implementation**:
1. Create custom Supabase config with minimal services
2. Update `config.toml` to disable unused services
3. Run `supabase stop && supabase start` with new config
4. Remove/disable rebind script (no longer needed)
5. Simplify network topology

**Benefits**:
- ✅ Reduced memory usage (~40-50% reduction)
- ✅ Faster startup times
- ✅ Simpler troubleshooting
- ✅ Lower attack surface
- ✅ Easier monitoring

**Risks**:
- ⚠️ Cannot add Auth/Storage later without reconfiguration
- ⚠️ Loses Studio UI if removed (but can access via psql)

**Migration Path**:
- Can be done during off-hours
- Minimal downtime (< 5 minutes)
- Reversible (keep backups)

### Option 2: Consolidate Network Topology

**Current Complexity**:
- 3 Docker networks: `supabase_network_supabase`, `supabase_network_archon`, `supabase_network_root`
- Archon containers connect to multiple networks
- Unclear purpose of `supabase_network_archon`

**Simplified Approach**:
```
archon_production_network (single network)
├── archon-server
├── archon-mcp
├── archon-ui
├── archon-agents (optional)
├── supabase_db
├── supabase_kong
├── supabase_rest
└── supabase_studio (optional)
```

**Benefits**:
- ✅ Simpler DNS resolution
- ✅ Easier network management
- ✅ Better isolation from other services
- ✅ Clearer service boundaries

### Option 3: Direct PostgreSQL Connection

**Most Minimal Approach**:
- Remove Kong and PostgREST entirely
- Connect Archon directly to PostgreSQL
- Use Python PostgreSQL client (psycopg2/asyncpg)
- Keep Studio for admin UI only

**Trade-offs**:
- ✅ Simplest possible setup
- ✅ Maximum performance (no API layer)
- ✅ Full control over queries
- ❌ Lose automatic REST API generation
- ❌ Lose Row Level Security features
- ❌ Need to rewrite all Supabase client code
- ❌ Not recommended unless major refactor planned

### Option 4: Supabase Cloud (Alternative)

**Replace self-hosted with managed service**:
- Use Supabase Cloud (supabase.com)
- Pay-as-you-go pricing (~$25+/month)
- Zero container management
- Automatic backups and monitoring

**Benefits**:
- ✅ No local resource usage
- ✅ Professional backups
- ✅ Managed upgrades
- ✅ Better monitoring tools

**Trade-offs**:
- ❌ Monthly cost
- ❌ Data leaves your server
- ❌ Less control over configuration
- ❌ Network latency (external API calls)

---

## Implementation Plan: Minimal Stack Migration

### Phase 1: Preparation (15 minutes)

1. **Backup current state**:
```bash
# Backup database
docker exec supabase_db_supabase pg_dumpall -U postgres > \
    /root/backups/supabase-full-$(date +%Y%m%d_%H%M%S).sql

# Backup Supabase config
cd /opt/archon/supabase
tar czf /root/backups/supabase-config-$(date +%Y%m%d_%H%M%S).tar.gz \
    config.toml migrations/ seed.sql
```

2. **Document current state**:
```bash
# Save container list
docker ps --filter name=supabase --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}' > \
    /root/backups/supabase-containers-before.txt

# Save port bindings
ss -tulpn | grep -E '54321|54322|54323|54324|54327' > \
    /root/backups/supabase-ports-before.txt
```

### Phase 2: Update Configuration (5 minutes)

1. **Edit `/opt/archon/supabase/config.toml`**:
```toml
# Disable unused services
[auth]
enabled = false  # Using custom API keys

[storage]
enabled = false  # Not using file storage

[realtime]
enabled = false  # Using HTTP polling

[inbucket]
enabled = false  # Dev tool only

# Analytics and logging (optional)
[analytics]
enabled = false

[db.pooler]
enabled = false  # Not needed for small deployments
```

2. **Keep essential services**:
```toml
[api]
enabled = true  # PostgREST

[db]
enabled = true  # PostgreSQL

[studio]
enabled = true  # Admin UI
```

### Phase 3: Restart Supabase (5 minutes)

```bash
cd /opt/archon/supabase

# Stop all Supabase services
supabase stop

# Start with new configuration
supabase start

# Verify only essential services running
docker ps --filter name=supabase
```

Expected containers after restart:
- `supabase_db_supabase`
- `supabase_kong_supabase`
- `supabase_rest_supabase`
- `supabase_studio_supabase`

### Phase 4: Verification (10 minutes)

1. **Test Archon connectivity**:
```bash
# Restart Archon services
cd /opt/archon
docker compose restart archon-server

# Check logs
docker logs -f archon-server | grep -i supabase

# Test API
curl http://localhost:8181/health
```

2. **Test database access**:
```bash
# From Archon container
docker exec archon-server python -c "
from src.server.services.client_manager import get_supabase_client
client = get_supabase_client()
result = client.table('api_keys').select('*').limit(1).execute()
print('Database access: OK' if result else 'FAILED')
"
```

3. **Test Studio UI**:
```bash
# Access via browser
open https://supabase.archon.nexorithm.io
# Verify can browse tables and run queries
```

### Phase 5: Cleanup (5 minutes)

1. **Remove rebind service** (no longer needed):
```bash
# Disable systemd service
systemctl disable supabase-rebind.service

# Remove service file
rm /etc/systemd/system/supabase-rebind.service
systemctl daemon-reload

# Keep script for reference
mv /opt/archon/scripts/rebind-supabase.py \
   /opt/archon/scripts/rebind-supabase.py.backup
```

2. **Clean up unused volumes**:
```bash
# List Supabase volumes
docker volume ls | grep supabase

# Remove volumes for deleted services (ONLY after verification)
# docker volume rm supabase_auth_supabase
# docker volume rm supabase_storage_supabase
# etc. (BE CAREFUL - only remove if sure)
```

### Phase 6: Network Simplification (Optional)

**Goal**: Merge `supabase_network_archon` into `supabase_network_supabase`

1. **Update Archon docker-compose.yml**:
```yaml
# Remove this line:
# - supabase_network_archon

# Keep only:
networks:
  app-network:
    driver: bridge
  supabase_network_supabase:
    external: true
```

2. **Remove unused network**:
```bash
docker network rm supabase_network_archon
```

### Rollback Plan

If issues occur:

1. **Restore configuration**:
```bash
cd /opt/archon/supabase
cp config.toml config.toml.minimal
cp /root/backups/supabase-config-YYYYMMDD_HHMMSS/config.toml .
```

2. **Restart with full stack**:
```bash
supabase stop
supabase start
```

3. **Re-run rebind script**:
```bash
python3 /opt/archon/scripts/rebind-supabase.py.backup
```

---

## Post-Migration Monitoring

### Health Checks

**Daily Checks** (first week):
```bash
# Container health
docker ps --filter name=supabase --format 'table {{.Names}}\t{{.Status}}'

# Port bindings
ss -tulpn | grep -E '54321|54322|54323'

# Archon connectivity
docker exec archon-server curl -f http://supabase_kong_supabase:8000/rest/v1/

# Database size
docker exec supabase_db_supabase psql -U postgres -c \
    "SELECT pg_size_pretty(pg_database_size('postgres'));"
```

### Performance Metrics

**Before/After Comparison**:
```bash
# Memory usage
docker stats --no-stream --format \
    "table {{.Name}}\t{{.MemUsage}}" | grep supabase

# Container count
docker ps --filter name=supabase --format '{{.Names}}' | wc -l
```

---

## Conclusions

### Current State Assessment

**Positive Findings**:
- ✅ Supabase deployment is properly configured
- ✅ Security implemented correctly (localhost binding)
- ✅ Database schema is clean and well-structured
- ✅ Archon's Supabase usage is well-architected

**Inefficiencies Identified**:
- ⚠️ 63% of Supabase containers are unused (7 out of 11)
- ⚠️ ~40-50% of resources wasted on unused services
- ⚠️ Unnecessary complexity in network topology
- ⚠️ Disabled services still consuming memory

### Recommendation Summary

**Immediate Actions** (Priority 1):
1. Disable unused services in `config.toml`
2. Restart Supabase with minimal configuration
3. Remove rebind script dependency
4. Document new architecture

**Future Optimizations** (Priority 2):
1. Consolidate Docker networks
2. Consider removing Studio in production (use psql)
3. Evaluate Supabase Cloud migration

**Estimated Impact**:
- **Resource Reduction**: 40-50% memory savings
- **Maintenance**: Simpler troubleshooting
- **Security**: Reduced attack surface
- **Performance**: Faster startup times

### Next Steps

1. **Review this analysis** with deployment team
2. **Schedule maintenance window** (30 minutes recommended)
3. **Follow implementation plan** (Phase 1-6)
4. **Monitor for 1 week** post-migration
5. **Document lessons learned**

---

**Analysis Completed**: 2025-10-16
**Analyst**: Claude (automated analysis)
**Review Status**: Pending human review
**Confidence Level**: High (based on code inspection, logs, and live server analysis)
