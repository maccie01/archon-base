# Archon Environment Configuration

**Created**: 2025-10-15
**File Location**: `/opt/archon/.env` (on server)

---

## Complete Production .env File

```bash
# ============================================
# SUPABASE CONFIGURATION (LOCAL)
# ============================================
# Using supabase kong IP address on Docker network
SUPABASE_URL=http://supabase_kong_archon:8000
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU
SUPABASE_JWT_SECRET=super-secret-jwt-token-with-at-least-32-characters-long
SUPABASE_DB_URL=postgresql://postgres:postgres@supabase_db_archon:5432/postgres

# ============================================
# OLLAMA CONFIGURATION
# ============================================
# Ollama is running on host, using Docker network gateway IP
OLLAMA_URL=http://172.18.0.1:11434
OLLAMA_MODEL=llama3.2:3b

# Optional: Set log level for debugging
LOGFIRE_TOKEN=
LOG_LEVEL=INFO

# ============================================
# SERVICE PORTS CONFIGURATION
# ============================================
# Allow remote access by binding to server IP
HOST=0.0.0.0
ARCHON_SERVER_PORT=8181
ARCHON_MCP_PORT=8051
ARCHON_AGENTS_PORT=8052
ARCHON_UI_PORT=3737
ARCHON_DOCS_PORT=3838

# ============================================
# FRONTEND CONFIGURATION
# ============================================
# Allow access from remote hosts
VITE_ALLOWED_HOSTS=archon.nexorithm.io,91.98.156.158,netzwaechter-prod,localhost,127.0.0.1,supabase.archon.nexorithm.io

# Development Tools
VITE_SHOW_DEVTOOLS=false

# ============================================
# PRODUCTION MODE
# ============================================
# Proxy server through UI port for single-port deployment
PROD=false

# ============================================
# AGENTS SERVICE (Optional)
# ============================================
# Set to true to enable AI agents service
AGENTS_ENABLED=false

# ============================================
# AUTHENTICATION CONFIGURATION
# ============================================
AUTH_ENABLED=true
ARCHON_BOOTSTRAP_SECRET=8aJEvaqfNAektfXZ6enA27_XPQ3nf-OjG1z9RhAPu0k
ALLOWED_ORIGINS=https://archon.nexorithm.io
```

---

## Variable Reference

### Supabase Configuration

| Variable | Value | Description |
|----------|-------|-------------|
| `SUPABASE_URL` | `http://supabase_kong_archon:8000` | Internal Docker network URL to Supabase Kong gateway |
| `SUPABASE_ANON_KEY` | JWT token | Public anon key for client-side queries (RLS enforced) |
| `SUPABASE_SERVICE_KEY` | JWT token | Admin service role key (bypasses RLS) - KEEP SECRET |
| `SUPABASE_JWT_SECRET` | Secret string | JWT signing secret (must match Supabase config) |
| `SUPABASE_DB_URL` | PostgreSQL connection string | Direct database connection URL for internal use |

**Notes**:
- Supabase runs as separate Docker containers in the same network
- Kong gateway handles routing and authentication
- Service key has full database access - never expose to client

### Ollama Configuration

| Variable | Value | Description |
|----------|-------|-------------|
| `OLLAMA_URL` | `http://172.18.0.1:11434` | Host machine Ollama service via Docker bridge network |
| `OLLAMA_MODEL` | `llama3.2:3b` | Default local LLM model for embeddings and operations |

**Notes**:
- Ollama runs on host machine (not in Docker)
- Accessible via Docker network gateway IP
- Model downloaded via: `ollama pull llama3.2:3b`

### Service Ports

| Variable | Value | Description |
|----------|-------|-------------|
| `HOST` | `0.0.0.0` | Bind to all network interfaces (allows external access) |
| `ARCHON_SERVER_PORT` | `8181` | FastAPI backend service |
| `ARCHON_MCP_PORT` | `8051` | Model Context Protocol server |
| `ARCHON_AGENTS_PORT` | `8052` | AI agents service (if enabled) |
| `ARCHON_UI_PORT` | `3737` | Frontend React application |
| `ARCHON_DOCS_PORT` | `3838` | Documentation site (if enabled) |

**Port Mapping**:
```
External (via Nginx):
/ → archon-ui (3737)
/api → archon-server (8181)
/mcp → archon-mcp (8051)
```

### Frontend Configuration

| Variable | Value | Description |
|----------|-------|-------------|
| `VITE_ALLOWED_HOSTS` | Comma-separated list | Hosts allowed to access Vite dev server |
| `VITE_SHOW_DEVTOOLS` | `false` | Show React Query DevTools in production |

**Allowed Hosts**:
- `archon.nexorithm.io` - Primary domain
- `91.98.156.158` - Direct IP access
- `localhost, 127.0.0.1` - Local development
- `supabase.archon.nexorithm.io` - Subdomain

### Authentication

| Variable | Value | Description |
|----------|-------|-------------|
| `AUTH_ENABLED` | `true` | Enable API key authentication middleware |
| `ARCHON_BOOTSTRAP_SECRET` | Random secret | One-time secret for creating first API key |
| `ALLOWED_ORIGINS` | `https://archon.nexorithm.io` | CORS allowed origins |

**Security Notes**:
- Bootstrap secret used only once to create first admin API key
- Can be rotated after initial setup
- CORS configured to allow only production domain

### Optional/Debug

| Variable | Default | Description |
|----------|---------|-------------|
| `LOGFIRE_TOKEN` | Empty | Logfire monitoring token (optional) |
| `LOG_LEVEL` | `INFO` | Logging verbosity (DEBUG, INFO, WARNING, ERROR) |
| `PROD` | `false` | Production mode flag |
| `AGENTS_ENABLED` | `false` | Enable AI agents service |

---

## Configuration Files Location

### Server

**Primary Config**: `/opt/archon/.env`

**Backups**:
- `/opt/archon/.env.backup-YYYYMMDD-HHMMSS` (automatic on changes)
- `/opt/archon/.env.example` (template)

### Docker Compose

**File**: `/opt/archon/docker-compose.yml`

**Service Environment Injection**:
```yaml
services:
  archon-server:
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - AUTH_ENABLED=${AUTH_ENABLED:-false}
      # ... etc
```

---

## Environment Setup Process

### New Server Setup

1. **Copy Example**:
   ```bash
   cd /opt/archon
   cp .env.example .env
   ```

2. **Generate Secrets**:
   ```bash
   # Generate bootstrap secret
   openssl rand -base64 32

   # Generate JWT secret (if needed)
   openssl rand -hex 32
   ```

3. **Configure Supabase**:
   - Set up Supabase instance (or use local)
   - Copy connection details to `.env`
   - Test connection:
     ```bash
     curl -H "apikey: $SUPABASE_ANON_KEY" "$SUPABASE_URL/rest/v1/"
     ```

4. **Configure Ollama**:
   - Install Ollama on host: `curl -fsSL https://ollama.com/install.sh | sh`
   - Pull model: `ollama pull llama3.2:3b`
   - Verify accessible: `curl http://localhost:11434/api/tags`

5. **Set Permissions**:
   ```bash
   chmod 600 /opt/archon/.env
   chown root:root /opt/archon/.env
   ```

6. **Validate**:
   ```bash
   # Source the file to check for syntax errors
   set -a && source /opt/archon/.env && set +a

   # Check required variables
   env | grep -E '(SUPABASE|OLLAMA|ARCHON|AUTH)'
   ```

---

## Environment Variable Best Practices

### Security

✅ **DO**:
- Store production `.env` in secure location
- Use strong, random secrets (minimum 32 characters)
- Rotate secrets regularly
- Keep `.env` in `.gitignore`
- Back up encrypted copy to password manager
- Use restrictive file permissions (600)

❌ **DON'T**:
- Commit `.env` to version control
- Share `.env` via email or chat
- Use default/example secrets in production
- Store API keys in plain text
- Give group/world read access

### Maintenance

**Monthly**:
- Review and audit active variables
- Remove unused variables
- Update comments for clarity

**Quarterly**:
- Rotate authentication secrets
- Review CORS and allowed hosts
- Update API keys if needed

**Annually**:
- Full security audit of all credentials
- Update database passwords
- Regenerate JWT secrets

---

## Environment Validation Script

```bash
#!/bin/bash
# validate-env.sh - Check environment configuration

set -e

echo "🔍 Validating Archon environment configuration..."

# Check file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found"
    exit 1
fi

# Check permissions
PERMS=$(stat -c "%a" .env 2>/dev/null || stat -f "%OLp" .env 2>/dev/null)
if [ "$PERMS" != "600" ]; then
    echo "⚠️  Warning: .env permissions should be 600 (currently $PERMS)"
fi

# Load environment
set -a
source .env
set +a

# Required variables
REQUIRED=(
    "SUPABASE_URL"
    "SUPABASE_SERVICE_KEY"
    "AUTH_ENABLED"
    "ARCHON_BOOTSTRAP_SECRET"
    "ARCHON_SERVER_PORT"
    "ARCHON_UI_PORT"
)

MISSING=()
for var in "${REQUIRED[@]}"; do
    if [ -z "${!var}" ]; then
        MISSING+=("$var")
    fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
    echo "❌ Missing required variables:"
    printf '   - %s\n' "${MISSING[@]}"
    exit 1
fi

# Test Supabase connection
echo "🔗 Testing Supabase connection..."
if curl -sf -H "apikey: $SUPABASE_ANON_KEY" "$SUPABASE_URL/rest/v1/" > /dev/null; then
    echo "✅ Supabase connection OK"
else
    echo "❌ Supabase connection failed"
fi

# Test Ollama connection
echo "🔗 Testing Ollama connection..."
if curl -sf "$OLLAMA_URL/api/tags" > /dev/null; then
    echo "✅ Ollama connection OK"
else
    echo "⚠️  Ollama connection failed (may not be required)"
fi

echo ""
echo "✅ Environment configuration valid!"
```

Usage:
```bash
cd /opt/archon
bash .deployment/archon/scripts/validate-env.sh
```

---

## Troubleshooting

### Issue: Services can't connect to Supabase

**Check**:
```bash
# Verify Supabase URL is accessible from container
docker compose exec archon-server curl -H "apikey: $SUPABASE_ANON_KEY" "$SUPABASE_URL/rest/v1/"

# Check Docker network
docker network inspect archon_default | grep supabase
```

**Solution**:
- Ensure Supabase containers are on same network
- Verify SUPABASE_URL points to Docker service name
- Check Supabase containers are running: `docker compose ps`

### Issue: Ollama not accessible

**Check**:
```bash
# Test from host
curl http://localhost:11434/api/tags

# Test from container
docker compose exec archon-server curl http://172.18.0.1:11434/api/tags
```

**Solution**:
- Verify Ollama is running: `systemctl status ollama`
- Check Docker network gateway IP: `docker network inspect archon_default | grep Gateway`
- Update OLLAMA_URL if gateway IP changed

### Issue: CORS errors

**Symptoms**: Browser console shows CORS policy errors

**Check**:
```bash
# Verify ALLOWED_ORIGINS
cat /opt/archon/.env | grep ALLOWED_ORIGINS
```

**Solution**:
- Add missing domain to ALLOWED_ORIGINS
- Restart services: `docker compose restart archon-server`
- Clear browser cache

---

**Last Updated**: 2025-10-15
**Review Schedule**: Monthly
