# Supabase Service Documentation

Created: 2025-10-16
Last Updated: 2025-10-16

## Overview

Supabase provides PostgreSQL database with REST API, authentication, real-time subscriptions, and admin interface for the Archon platform.

## Service Configuration

**Domain**: https://supabase.archon.nexorithm.io
**Backend**: Self-hosted Supabase (Docker)
**Database**: PostgreSQL 15 with pgvector extension

### Ports

| Service | Internal Port | External Access |
|---------|--------------|-----------------|
| Kong Gateway (API) | 54321 | Via Nginx at `/rest/v1/`, `/auth/v1/`, etc. |
| Studio UI | 54323 | Via Nginx at `/` (root path) |
| PostgreSQL | 5432 | Localhost only |

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

**Base URL**: https://supabase.archon.nexorithm.io

**Endpoints** (no HTTP Basic Auth - use API keys):
- `/rest/v1/` - Database REST API (PostgREST)
- `/auth/v1/` - Authentication API (GoTrue)
- `/storage/v1/` - File storage API
- `/realtime/v1/` - WebSocket real-time subscriptions

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
psql -h 127.0.0.1 -p 5432 -U postgres -d postgres

# Connection string
postgresql://postgres:YOUR_POSTGRES_PASSWORD@127.0.0.1:5432/postgres
```

## Common Operations

### View Logs
```bash
# Studio UI logs
ssh netzwaechter-prod "docker logs -f supabase_studio_supabase"

# Kong Gateway logs
ssh netzwaechter-prod "docker logs -f supabase_kong_supabase"

# PostgreSQL logs
ssh netzwaechter-prod "docker logs -f supabase_db_supabase"
```

### Restart Services
```bash
# Restart all Supabase services
ssh netzwaechter-prod "cd /opt/supabase && docker compose restart"

# Restart specific service
ssh netzwaechter-prod "cd /opt/supabase && docker compose restart studio"
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
ssh netzwaechter-prod "docker ps | grep studio"
ssh netzwaechter-prod "docker logs supabase_studio_supabase"

# Check Nginx proxy
ssh netzwaechter-prod "tail -f /var/log/nginx/supabase-archon-ssl-error.log"

# Restart Studio
ssh netzwaechter-prod "cd /opt/supabase && docker compose restart studio"
```

### API Returning Errors
```bash
# Check Kong Gateway
ssh netzwaechter-prod "docker logs supabase_kong_supabase | tail -50"

# Test API directly
curl -H "apikey: YOUR_SUPABASE_ANON_KEY" \
  "https://supabase.archon.nexorithm.io/rest/v1/"

# Restart Kong
ssh netzwaechter-prod "cd /opt/supabase && docker compose restart kong"
```

### Database Connection Issues
```bash
# Check PostgreSQL
ssh netzwaechter-prod "docker ps | grep db_supabase"
ssh netzwaechter-prod "docker logs supabase_db_supabase | tail -50"

# Test connection
ssh netzwaechter-prod "docker exec supabase_db_supabase psql -U postgres -c 'SELECT version();'"

# Restart database (WARNING: Will disconnect all clients)
ssh netzwaechter-prod "cd /opt/supabase && docker compose restart db"
```

### Authentication Not Working
```bash
# Check auth service
ssh netzwaechter-prod "docker logs supabase_auth_supabase | tail -50"

# Verify JWT secret configured
ssh netzwaechter-prod "cd /opt/supabase && cat .env | grep JWT_SECRET"

# Restart auth service
ssh netzwaechter-prod "cd /opt/supabase && docker compose restart auth"
```

## Configuration Files

| File | Purpose |
|------|---------|
| `/opt/supabase/docker-compose.yml` | Service orchestration |
| `/opt/supabase/.env` | Environment variables |
| `/etc/nginx/sites-available/archon` | Nginx proxy config |
| `/etc/nginx/.htpasswd-supabase` | HTTP Basic Auth credentials |

## Security Notes

- Studio UI protected by HTTP Basic Authentication
- API endpoints use Supabase API keys (no HTTP Basic Auth)
- PostgreSQL bound to localhost only (127.0.0.1)
- All external traffic through Nginx reverse proxy
- Rate limiting: 30 req/min per IP (exceptions for static assets)
- SSL/TLS via Cloudflare + Let's Encrypt

## Issue Resolution History

All critical Supabase issues resolved on 2025-10-15:

1. DNS configuration fixed
2. Browser access enabled (Studio UI)
3. CSS/JavaScript loading fixed
4. Authentication implemented (HTTP Basic Auth)
5. Rate limiting optimized

See [SUPABASE_ALL_ISSUES_RESOLVED.md](./SUPABASE_ALL_ISSUES_RESOLVED.md) for complete details.

## Resources

**Official Documentation**:
- Supabase Docs: https://supabase.com/docs
- PostgREST: https://postgrest.org
- Kong Gateway: https://docs.konghq.com

**Internal Documentation**:
- [SUPABASE_ALL_ISSUES_RESOLVED.md](./SUPABASE_ALL_ISSUES_RESOLVED.md) - Complete fix documentation
- [../../core/CREDENTIALS.md](../../core/CREDENTIALS.md) - Access credentials
- [../../archive/supabase-fixes/](../../archive/supabase-fixes/) - Historical fix documentation
