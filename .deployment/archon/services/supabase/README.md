# Supabase Service Documentation

Created: 2025-10-16
Last Updated: 2025-10-16 (Consolidated Architecture)

## Overview

Supabase provides PostgreSQL database with REST API and admin interface for the Archon platform. This is a **consolidated single-network architecture** with 5 core Supabase services.

## Service Configuration

**Architecture**: Consolidated Single-Network (archon_production 172.21.0.0/16)
**Domain**: https://supabase.archon.nexorithm.io
**Backend**: Self-hosted Supabase (Docker Compose)
**Database**: PostgreSQL 17.6 with pgvector extension
**Management**: Simple `docker compose` commands (no Supabase CLI)

### Services

| Service | Container | Port | Purpose |
|---------|-----------|------|---------|
| PostgreSQL | supabase-db | 54322 | Primary database with pgvector |
| Kong Gateway | supabase-kong | 54321 | API gateway with JWT transformation |
| PostgREST | supabase-rest | 3000 (internal) | Automatic REST API generation |
| pg_meta | supabase-meta | Internal | PostgreSQL metadata service |
| Studio UI | supabase-studio | 54323 | Web-based database admin |

**Removed Services** (from v1.3.0 consolidation):
- ❌ GoTrue (Auth) - Not used (custom API keys)
- ❌ Storage API - Not used (no file storage)
- ❌ Realtime - Not used (HTTP polling instead)
- ❌ Analytics - Optional monitoring
- ❌ Inbucket - Dev tool only

## Access Methods

### 1. Browser Access (Studio UI)

**URL**: https://supabase.archon.nexorithm.io/

**Authentication**: HTTP Basic Auth
- Username: `admin`
- Password: See [../../core/CREDENTIALS.md](../../core/CREDENTIALS.md)

**Features**:
- Table Editor
- SQL Editor
- Authentication management
- Storage browser
- API documentation
- Real-time logs

### 2. API Access (Your Application)

**Internal URL** (from Archon containers): `http://supabase-kong:54321`
**External URL**: https://supabase.archon.nexorithm.io (if exposed via Nginx)

**Endpoints** (no HTTP Basic Auth):
- `/rest/v1/` - Database REST API (PostgREST)

**Note**: Auth, Storage, and Realtime endpoints are NOT available in consolidated architecture.

### Kong Gateway Configuration

**Critical Feature**: JWT Transformation
- **Removes** Authorization headers from client requests
- **Adds** hardcoded service JWT for PostgREST authentication
- **Prevents** PGRST301 errors (JWT secret mismatch)

**Flow**:
```
Client Request → Kong Gateway
  ├─ Remove: Authorization header
  ├─ Add: Hardcoded service JWT
  └─ Forward → PostgREST (port 3000)
```

**Example (JavaScript)**:
```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'https://supabase.archon.nexorithm.io',
  'YOUR_SUPABASE_ANON_KEY' // See core/CREDENTIALS.md
)

// Query data
const { data, error } = await supabase
  .from('your_table')
  .select('*')
```

**Example (Python)**:
```python
from supabase import create_client, Client

url = "https://supabase.archon.nexorithm.io"
key = "YOUR_SUPABASE_ANON_KEY"  # See core/CREDENTIALS.md
supabase: Client = create_client(url, key)

# Query data
response = supabase.table("your_table").select("*").execute()
```

### 3. Direct PostgreSQL Access

```bash
# From server (localhost)
psql -h 127.0.0.1 -p 54322 -U postgres -d postgres

# Connection string (consolidated architecture)
postgresql://postgres:postgres@supabase-db:5432/postgres  # Internal
postgresql://postgres:postgres@127.0.0.1:54322/postgres   # External

# JWT Secret (must match PostgREST configuration)
JWT_SECRET=super-secret-jwt-token-with-at-least-32-characters-long
```

## Common Operations

### View Logs
```bash
# All Supabase services (consolidated architecture)
docker compose logs -f supabase-db supabase-kong supabase-rest supabase-meta supabase-studio

# Specific service
docker compose logs -f supabase-kong
docker compose logs -f supabase-db
docker compose logs -f supabase-studio
```

### Restart Services
```bash
# Restart all services (from /opt/archon)
cd /opt/archon
docker compose restart

# Restart specific Supabase service
docker compose restart supabase-kong
docker compose restart supabase-db
docker compose restart supabase-studio
```

### Database Backup
```bash
# Manual backup via Studio UI
# 1. Login to Studio
# 2. Navigate to Database → Backups
# 3. Click "Create backup"

# Or use pg_dump
ssh netzwaechter-prod "docker exec supabase_db_supabase pg_dump -U postgres postgres > backup_$(date +%Y%m%d).sql"
```

### Run Migrations
```bash
# Apply migration via Studio UI
# 1. Login to Studio
# 2. Navigate to SQL Editor
# 3. Paste migration SQL
# 4. Click "Run"

# Or via psql
ssh netzwaechter-prod "docker exec -i supabase_db_supabase psql -U postgres -d postgres < migration.sql"
```

## Troubleshooting

### Studio UI Not Loading
```bash
# Check Studio container
docker ps | grep supabase-studio
docker logs supabase-studio

# Check Nginx proxy
tail -f /var/log/nginx/supabase-archon-ssl-error.log

# Restart Studio
docker compose restart supabase-studio
```

### PGRST301 Error (JWT Secret Mismatch)

**Symptoms**: PostgREST returns PGRST301 error

**Cause**: JWT secret mismatch between database and PostgREST

**Solution**:
```bash
# 1. Verify JWT_SECRET in environment
cat /opt/archon/.env | grep SUPABASE_JWT_SECRET
# Should be: super-secret-jwt-token-with-at-least-32-characters-long

# 2. Verify database JWT secret matches
docker exec supabase-db psql -U postgres -c \
  "SHOW app.settings.jwt_secret;"

# 3. If mismatch, update database configuration
# (Restart required for changes to take effect)

# 4. Restart services
docker compose restart supabase-db supabase-rest supabase-kong
```

**Kong Gateway Fix**:
- Kong removes Authorization headers to prevent client JWT conflicts
- Kong adds hardcoded service JWT configured with correct secret
- This prevents PGRST301 errors from client-side JWT tokens

### API Returning Errors
```bash
# Check Kong Gateway
docker logs supabase-kong | tail -50

# Test API directly (internal)
docker exec archon-server curl -H "apikey: $SUPABASE_ANON_KEY" \
  "http://supabase-kong:54321/rest/v1/"

# Restart Kong
docker compose restart supabase-kong
```

### Database Connection Issues
```bash
# Check PostgreSQL
docker ps | grep supabase-db
docker logs supabase-db | tail -50

# Test connection
docker exec supabase-db psql -U postgres -c 'SELECT version();'

# Restart database (WARNING: Will disconnect all clients)
docker compose restart supabase-db
```

### Healthcheck Failures

**Studio Healthcheck** (uses Node.js with os.hostname()):
```bash
# Check Studio health manually
docker exec supabase-studio node -e "console.log(require('os').hostname())"

# If failing, check container network
docker inspect supabase-studio | grep NetworkMode
```

**UI Healthcheck** (uses curl):
```bash
# Check UI health manually
docker exec archon-ui curl -f http://localhost:3737

# If failing, check nginx configuration
docker exec archon-ui cat /etc/nginx/conf.d/default.conf
```

## Configuration Files

**Consolidated Architecture** (v1.3.0):

| File | Purpose |
|------|---------|
| `/opt/archon/docker-compose.yml` | Single compose file for all services |
| `/opt/archon/.env` | Environment variables for all services |
| `/etc/nginx/sites-available/archon` | Nginx proxy config |
| `/etc/nginx/.htpasswd-supabase` | HTTP Basic Auth credentials |

**Removed** (from consolidation):
- `/opt/supabase/` directory - No longer needed (Supabase CLI removed)
- Rebind scripts - Port binding now handled by Docker Compose
- External network definitions - Single network architecture

## Security Notes

- Studio UI protected by HTTP Basic Authentication
- API endpoints use Supabase API keys (no HTTP Basic Auth)
- PostgreSQL accessible on port 54322 (internal network and localhost)
- All services on single isolated network (172.21.0.0/16)
- Kong Gateway handles JWT transformation (prevents PGRST301 errors)
- All external traffic through Nginx reverse proxy
- Rate limiting: 30 req/min per IP (exceptions for static assets)
- SSL/TLS via Cloudflare + Let's Encrypt

**JWT Secret Security**:
- Hardcoded in database configuration: `super-secret-jwt-token-with-at-least-32-characters-long`
- Must match across all services (database, PostgREST, Kong)
- Kong removes client Authorization headers to prevent conflicts
- Kong adds service JWT for internal authentication

## Migration History

### v1.3.0 Consolidation (2025-10-16)

**Changes**:
- Migrated from multi-network (11 containers) to single-network (5 containers)
- Removed unused services: Auth, Storage, Realtime, Analytics, Inbucket
- Cleaned up supabase volumes and rebind scripts
- Standardized JWT secret across all services
- Fixed Kong Gateway JWT transformation
- All healthchecks now passing

**Benefits**:
- 40-50% memory reduction
- Simpler network topology
- Faster startup times
- Cleaner troubleshooting
- No external network dependencies

### v1.2.0 and Earlier (2025-10-15)

See archived documentation:
- [SUPABASE_ALL_ISSUES_RESOLVED.md](./SUPABASE_ALL_ISSUES_RESOLVED.md) - DNS and access fixes
- [../../archive/supabase-fixes/](../../archive/supabase-fixes/) - Historical fixes

## Resources

**Official Documentation**:
- Supabase Docs: https://supabase.com/docs
- PostgREST: https://postgrest.org
- Kong Gateway: https://docs.konghq.com

**Internal Documentation**:
- [SUPABASE_ALL_ISSUES_RESOLVED.md](./SUPABASE_ALL_ISSUES_RESOLVED.md) - Complete fix documentation
- [../../core/CREDENTIALS.md](../../core/CREDENTIALS.md) - Access credentials
- [../../archive/supabase-fixes/](../../archive/supabase-fixes/) - Historical fix documentation
