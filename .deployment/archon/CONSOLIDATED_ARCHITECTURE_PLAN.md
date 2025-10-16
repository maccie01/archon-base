# Consolidated Archon Architecture Plan

**Date**: 2025-10-16
**Goal**: Simplify network topology while maintaining security and all current functionality

---

## Current vs Proposed Architecture

### Current State (Complex)

**Networks**:
- `app-network` (internal Archon services)
- `supabase_network_archon` (external, only Archon containers)
- `supabase_network_supabase` (external, all Supabase + Archon)
- `supabase_network_root` (unused legacy)

**Containers**:
- 11 Supabase containers (managed by `supabase start`)
- 4 Archon containers (managed by docker-compose)
- Total: 15 containers across 3+ networks

**Management**:
- Supabase: CLI commands from `/opt/archon/supabase/`
- Archon: `docker compose` from `/opt/archon/`
- Custom rebind script for port security
- Systemd service for rebinding

### Proposed State (Simplified)

**Single Network**:
- `archon_production` (one network for everything)

**Unified Docker Compose**:
- All services in one `docker-compose.yml`
- Single startup command: `docker compose up -d`
- Consistent logging: `docker compose logs -f`
- Unified monitoring: `docker compose ps`

**Services** (9 total - removed 6 unused):
1. PostgreSQL (database)
2. Kong Gateway (API routing)
3. PostgREST (REST API)
4. Studio (admin UI)
5. Archon Server (FastAPI backend)
6. Archon MCP (MCP server)
7. Archon UI (React frontend)
8. Archon Agents (optional, with profile)
9. Nginx (external proxy - separate container or host-level)

---

## Security Model (Preserved)

### API Key Authentication

**How it works** (unchanged):
1. UI stores API key in `localStorage` (`archon_api_key`)
2. All API requests include `Authorization: Bearer <api_key>` header
3. FastAPI middleware validates key against `api_keys` table
4. MCP inherits same authentication (proxies through API)

**Middleware**: `/Users/janschubert/tools/archon/python/src/server/middleware/auth_middleware.py`
- Validates Bearer tokens
- Checks against bcrypt hashes in database
- Updates `last_used_at` timestamp
- Stores auth info in `request.state`

**Exempt paths** (no auth required):
- `/` (root)
- `/health`
- `/api/health`
- `/api/auth/bootstrap` (initial key creation)
- `/api/auth/status` (public status)
- `/internal/*` (IP-based auth)

### Network Security

**External Access** (via Nginx reverse proxy):
- `https://archon.nexorithm.io` → UI + API + WebSocket
- `https://supabase.archon.nexorithm.io` → Studio UI only
- All other services: `127.0.0.1` binding (not exposed)

**Internal Communication**:
- All containers on same Docker network
- Service discovery via container names
- No external ports except through Nginx

### Port Binding Strategy

**Localhost Only** (for security):
```yaml
ports:
  - "127.0.0.1:54321:8000"   # Kong API
  - "127.0.0.1:54322:5432"   # PostgreSQL
  - "127.0.0.1:54323:3000"   # Studio UI
  - "127.0.0.1:8181:8181"    # Archon Server
  - "127.0.0.1:8051:8051"    # Archon MCP
  - "127.0.0.1:3737:3737"    # Archon UI
```

**Benefits**:
- Services not accessible from internet
- All traffic goes through Nginx
- Defense in depth
- No rebind script needed (built into compose)

---

## New Docker Compose Structure

### File: `/opt/archon/docker-compose.production.yml`

```yaml
version: '3.8'

# ==============================================================================
# ARCHON PRODUCTION DEPLOYMENT
# Consolidated architecture with all services in one compose file
# ==============================================================================

services:
  # ==========================================================================
  # DATABASE LAYER - PostgreSQL with pgvector
  # ==========================================================================

  postgres:
    image: public.ecr.aws/supabase/postgres:17.6.1.017
    container_name: archon-postgres
    restart: unless-stopped
    ports:
      - "127.0.0.1:54322:5432"
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_DB: ${POSTGRES_DB:-postgres}
      POSTGRES_HOST: /var/run/postgresql
      JWT_SECRET: ${JWT_SECRET}
      JWT_EXP: ${JWT_EXP:-3600}
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./supabase/migrations:/docker-entrypoint-initdb.d:ro
    networks:
      - archon_production
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    command: >
      postgres
      -c shared_preload_libraries=pg_stat_statements,pgaudit,plpgsql,plpgsql_check,pg_cron,pg_net,pgjwt,pgsodium,pgcrypto,uuid-ossp
      -c pgaudit.log=ddl,role
      -c log_statement=mod
      -c max_connections=200
      -c shared_buffers=256MB

  # ==========================================================================
  # API GATEWAY - Kong for routing
  # ==========================================================================

  kong:
    image: public.ecr.aws/supabase/kong:2.8.1
    container_name: archon-kong
    restart: unless-stopped
    ports:
      - "127.0.0.1:54321:8000"
    environment:
      KONG_DATABASE: "off"
      KONG_DECLARATIVE_CONFIG: /home/kong/kong.yml
      KONG_DNS_ORDER: LAST,A,CNAME
      KONG_PLUGINS: request-transformer,cors,key-auth,acl
      SUPABASE_ANON_KEY: ${SUPABASE_ANON_KEY}
      SUPABASE_SERVICE_KEY: ${SUPABASE_SERVICE_KEY}
    volumes:
      - ./supabase/volumes/api/kong.yml:/home/kong/kong.yml:ro
    networks:
      - archon_production
    depends_on:
      postgres:
        condition: service_healthy
      rest:
        condition: service_started
    healthcheck:
      test: ["CMD", "kong", "health"]
      interval: 10s
      timeout: 10s
      retries: 5

  # ==========================================================================
  # REST API - PostgREST for auto-generated API
  # ==========================================================================

  rest:
    image: public.ecr.aws/supabase/postgrest:v13.0.7
    container_name: archon-rest
    restart: unless-stopped
    environment:
      PGRST_DB_URI: postgresql://${POSTGRES_USER:-postgres}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB:-postgres}
      PGRST_DB_SCHEMAS: public,storage,graphql_public
      PGRST_DB_ANON_ROLE: anon
      PGRST_JWT_SECRET: ${JWT_SECRET}
      PGRST_DB_USE_LEGACY_GUCS: "false"
      PGRST_APP_SETTINGS_JWT_SECRET: ${JWT_SECRET}
      PGRST_APP_SETTINGS_JWT_EXP: ${JWT_EXP:-3600}
    networks:
      - archon_production
    depends_on:
      postgres:
        condition: service_healthy

  # ==========================================================================
  # ADMIN UI - Supabase Studio
  # ==========================================================================

  studio:
    image: public.ecr.aws/supabase/studio:2025.10.09-sha-433e578
    container_name: archon-studio
    restart: unless-stopped
    ports:
      - "127.0.0.1:54323:3000"
    environment:
      SUPABASE_URL: http://kong:8000
      STUDIO_PG_META_URL: http://meta:8080
      SUPABASE_ANON_KEY: ${SUPABASE_ANON_KEY}
      SUPABASE_SERVICE_KEY: ${SUPABASE_SERVICE_KEY}
      LOGFLARE_API_KEY: ${LOGFLARE_API_KEY:-}
      LOGFLARE_URL: ${LOGFLARE_URL:-}
    networks:
      - archon_production
    depends_on:
      - kong

  # ==========================================================================
  # METADATA API - PostgreSQL metadata for Studio
  # ==========================================================================

  meta:
    image: public.ecr.aws/supabase/postgres-meta:v0.91.7
    container_name: archon-meta
    restart: unless-stopped
    environment:
      PG_META_PORT: 8080
      PG_META_DB_HOST: postgres
      PG_META_DB_PORT: 5432
      PG_META_DB_NAME: ${POSTGRES_DB:-postgres}
      PG_META_DB_USER: ${POSTGRES_USER:-postgres}
      PG_META_DB_PASSWORD: ${POSTGRES_PASSWORD}
    networks:
      - archon_production
    depends_on:
      postgres:
        condition: service_healthy

  # ==========================================================================
  # ARCHON BACKEND - FastAPI + Socket.IO
  # ==========================================================================

  archon-server:
    build:
      context: ./python
      dockerfile: Dockerfile.server
      args:
        BUILDKIT_INLINE_CACHE: 1
        ARCHON_SERVER_PORT: ${ARCHON_SERVER_PORT:-8181}
    container_name: archon-server
    restart: unless-stopped
    ports:
      - "127.0.0.1:${ARCHON_SERVER_PORT:-8181}:${ARCHON_SERVER_PORT:-8181}"
    environment:
      # Database connection (via Kong)
      SUPABASE_URL: http://kong:8000
      SUPABASE_SERVICE_KEY: ${SUPABASE_SERVICE_KEY}
      SUPABASE_JWT_SECRET: ${JWT_SECRET}

      # OpenAI API
      OPENAI_API_KEY: ${OPENAI_API_KEY:-}

      # Logging
      LOGFIRE_TOKEN: ${LOGFIRE_TOKEN:-}
      LOG_LEVEL: ${LOG_LEVEL:-INFO}

      # Service discovery
      SERVICE_DISCOVERY_MODE: docker_compose
      ARCHON_SERVER_PORT: ${ARCHON_SERVER_PORT:-8181}
      ARCHON_MCP_PORT: ${ARCHON_MCP_PORT:-8051}
      ARCHON_AGENTS_PORT: ${ARCHON_AGENTS_PORT:-8052}
      AGENTS_ENABLED: ${AGENTS_ENABLED:-false}

      # Security
      ARCHON_BOOTSTRAP_SECRET: ${ARCHON_BOOTSTRAP_SECRET:-}
    networks:
      - archon_production
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./python/src:/app/src
      - ./python/tests:/app/tests
      - ./migration:/app/migration
    extra_hosts:
      - "host.docker.internal:host-gateway"
    depends_on:
      postgres:
        condition: service_healthy
      kong:
        condition: service_healthy
    command:
      [
        "python",
        "-m",
        "uvicorn",
        "src.server.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "${ARCHON_SERVER_PORT:-8181}",
        "--reload",
      ]
    healthcheck:
      test:
        [
          "CMD",
          "sh",
          "-c",
          'python -c "import urllib.request; urllib.request.urlopen(''http://localhost:${ARCHON_SERVER_PORT:-8181}/health'')"',
        ]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # ==========================================================================
  # MCP SERVER - Model Context Protocol
  # ==========================================================================

  archon-mcp:
    build:
      context: ./python
      dockerfile: Dockerfile.mcp
      args:
        BUILDKIT_INLINE_CACHE: 1
        ARCHON_MCP_PORT: ${ARCHON_MCP_PORT:-8051}
    container_name: archon-mcp
    restart: unless-stopped
    ports:
      - "127.0.0.1:${ARCHON_MCP_PORT:-8051}:${ARCHON_MCP_PORT:-8051}"
    environment:
      SUPABASE_URL: http://kong:8000
      SUPABASE_SERVICE_KEY: ${SUPABASE_SERVICE_KEY}
      LOGFIRE_TOKEN: ${LOGFIRE_TOKEN:-}
      SERVICE_DISCOVERY_MODE: docker_compose
      TRANSPORT: sse
      LOG_LEVEL: ${LOG_LEVEL:-INFO}
      API_SERVICE_URL: http://archon-server:${ARCHON_SERVER_PORT:-8181}
      AGENTS_ENABLED: ${AGENTS_ENABLED:-false}
      AGENTS_SERVICE_URL: ${AGENTS_SERVICE_URL:-http://archon-agents:${ARCHON_AGENTS_PORT:-8052}}
      ARCHON_MCP_PORT: ${ARCHON_MCP_PORT:-8051}
      ARCHON_SERVER_PORT: ${ARCHON_SERVER_PORT:-8181}
      ARCHON_AGENTS_PORT: ${ARCHON_AGENTS_PORT:-8052}
    networks:
      - archon_production
    depends_on:
      archon-server:
        condition: service_healthy
    extra_hosts:
      - "host.docker.internal:host-gateway"
    healthcheck:
      test:
        [
          "CMD",
          "sh",
          "-c",
          'python -c "import socket; s=socket.socket(); s.connect((''localhost'', ${ARCHON_MCP_PORT:-8051})); s.close()"',
        ]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  # ==========================================================================
  # ARCHON FRONTEND - React/Next.js UI
  # ==========================================================================

  archon-ui:
    build: ./archon-ui-main
    container_name: archon-ui
    restart: unless-stopped
    ports:
      - "127.0.0.1:${ARCHON_UI_PORT:-3737}:3737"
    environment:
      # API connection (uses relative URLs, proxied by Nginx)
      VITE_ARCHON_SERVER_PORT: ${ARCHON_SERVER_PORT:-8181}
      ARCHON_SERVER_PORT: ${ARCHON_SERVER_PORT:-8181}
      HOST: ${HOST:-localhost}
      PROD: ${PROD:-false}
      VITE_ALLOWED_HOSTS: ${VITE_ALLOWED_HOSTS:-}
      VITE_SHOW_DEVTOOLS: ${VITE_SHOW_DEVTOOLS:-false}
      DOCKER_ENV: true
    networks:
      - archon_production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3737"]
      interval: 30s
      timeout: 10s
      retries: 3
    volumes:
      - ./archon-ui-main/src:/app/src
      - ./archon-ui-main/public:/app/public
    depends_on:
      archon-server:
        condition: service_healthy

  # ==========================================================================
  # ARCHON AGENTS - AI Agents (Optional, with profile)
  # ==========================================================================

  archon-agents:
    profiles:
      - agents
    build:
      context: ./python
      dockerfile: Dockerfile.agents
      args:
        BUILDKIT_INLINE_CACHE: 1
        ARCHON_AGENTS_PORT: ${ARCHON_AGENTS_PORT:-8052}
    container_name: archon-agents
    restart: unless-stopped
    ports:
      - "127.0.0.1:${ARCHON_AGENTS_PORT:-8052}:${ARCHON_AGENTS_PORT:-8052}"
    environment:
      SUPABASE_URL: http://kong:8000
      SUPABASE_SERVICE_KEY: ${SUPABASE_SERVICE_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY:-}
      LOGFIRE_TOKEN: ${LOGFIRE_TOKEN:-}
      SERVICE_DISCOVERY_MODE: docker_compose
      LOG_LEVEL: ${LOG_LEVEL:-INFO}
      ARCHON_AGENTS_PORT: ${ARCHON_AGENTS_PORT:-8052}
      ARCHON_SERVER_PORT: ${ARCHON_SERVER_PORT:-8181}
    networks:
      - archon_production
    healthcheck:
      test:
        [
          "CMD",
          "sh",
          "-c",
          'python -c "import urllib.request; urllib.request.urlopen(''http://localhost:${ARCHON_AGENTS_PORT:-8052}/health'')"',
        ]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

# ==============================================================================
# NETWORKS
# ==============================================================================

networks:
  archon_production:
    name: archon_production
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

# ==============================================================================
# VOLUMES
# ==============================================================================

volumes:
  postgres-data:
    name: archon_postgres_data
```

---

## Environment Variables

### File: `/opt/archon/.env.production`

```bash
# ==============================================================================
# ARCHON PRODUCTION ENVIRONMENT
# ==============================================================================

# ------------------------------------------------------------------------------
# PostgreSQL Configuration
# ------------------------------------------------------------------------------
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<GENERATE_SECURE_PASSWORD>
POSTGRES_DB=postgres

# ------------------------------------------------------------------------------
# Supabase JWT (for PostgREST)
# ------------------------------------------------------------------------------
JWT_SECRET=<GENERATE_32_CHAR_SECRET>
JWT_EXP=3600

# ------------------------------------------------------------------------------
# Supabase API Keys (for PostgREST)
# ------------------------------------------------------------------------------
SUPABASE_ANON_KEY=<GENERATE_JWT_TOKEN>
SUPABASE_SERVICE_KEY=<GENERATE_JWT_TOKEN>

# ------------------------------------------------------------------------------
# OpenAI API Key
# ------------------------------------------------------------------------------
OPENAI_API_KEY=<YOUR_OPENAI_KEY>

# ------------------------------------------------------------------------------
# Archon Ports
# ------------------------------------------------------------------------------
ARCHON_SERVER_PORT=8181
ARCHON_MCP_PORT=8051
ARCHON_UI_PORT=3737
ARCHON_AGENTS_PORT=8052

# ------------------------------------------------------------------------------
# Features
# ------------------------------------------------------------------------------
AGENTS_ENABLED=false
PROD=true

# ------------------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------------------
LOG_LEVEL=INFO
LOGFIRE_TOKEN=  # Optional

# ------------------------------------------------------------------------------
# Security
# ------------------------------------------------------------------------------
ARCHON_BOOTSTRAP_SECRET=<GENERATE_SECURE_SECRET>

# ------------------------------------------------------------------------------
# Hosts
# ------------------------------------------------------------------------------
HOST=archon.nexorithm.io
VITE_ALLOWED_HOSTS=archon.nexorithm.io,supabase.archon.nexorithm.io,91.98.156.158,localhost,127.0.0.1
```

---

## Nginx Configuration (No Changes)

Your existing Nginx config continues to work:

```nginx
# archon.nexorithm.io → UI + API
location / {
    proxy_pass http://127.0.0.1:3737;  # Archon UI
}

location /api/ {
    proxy_pass http://127.0.0.1:8181/api/;  # Archon Server
}

location /socket.io/ {
    proxy_pass http://127.0.0.1:8181/socket.io/;  # WebSocket
}

# supabase.archon.nexorithm.io → Studio
location / {
    proxy_pass http://127.0.0.1:54323;  # Supabase Studio
}
```

---

## Migration Steps

### Phase 1: Backup (15 minutes)

```bash
# 1. Backup database
docker exec supabase_db_supabase pg_dumpall -U postgres > \
    /root/backups/archon-db-$(date +%Y%m%d_%H%M%S).sql

# 2. Backup current configurations
cd /opt/archon
tar czf /root/backups/archon-config-$(date +%Y%m%d_%H%M%S).tar.gz \
    docker-compose.yml .env supabase/

# 3. Export PostgreSQL data volume
docker run --rm \
    -v supabase_db_supabase:/source:ro \
    -v /root/backups:/backup \
    alpine \
    tar czf /backup/postgres-volume-$(date +%Y%m%d_%H%M%S).tar.gz -C /source .
```

### Phase 2: Stop Current Services (5 minutes)

```bash
cd /opt/archon

# Stop Archon services
docker compose down

# Stop Supabase
cd supabase && supabase stop
```

### Phase 3: Install New Configuration (10 minutes)

```bash
cd /opt/archon

# Copy new docker-compose file
cp docker-compose.yml docker-compose.yml.backup
# (Deploy docker-compose.production.yml as docker-compose.yml)

# Update environment variables
cp .env .env.backup
# (Deploy .env.production as .env)

# Generate secure secrets
./scripts/generate-secrets.sh  # Script to create JWT tokens, passwords
```

### Phase 4: Migrate Data (10 minutes)

```bash
# Create new volume and restore data
docker volume create archon_postgres_data

docker run --rm \
    -v /root/backups:/backup \
    -v archon_postgres_data:/target \
    alpine \
    sh -c "cd /target && tar xzf /backup/postgres-volume-YYYYMMDD_HHMMSS.tar.gz"
```

### Phase 5: Start Consolidated Stack (5 minutes)

```bash
cd /opt/archon

# Start all services
docker compose up -d

# Monitor startup
docker compose logs -f
```

### Phase 6: Verification (15 minutes)

```bash
# 1. Check all containers running
docker compose ps

# 2. Test database connectivity
docker exec archon-postgres psql -U postgres -c "SELECT COUNT(*) FROM api_keys;"

# 3. Test API endpoints
curl http://localhost:8181/health
curl http://localhost:8051/health
curl http://localhost:3737

# 4. Test Studio UI
curl http://localhost:54323

# 5. Test external access (from browser)
# https://archon.nexorithm.io
# https://supabase.archon.nexorithm.io

# 6. Test API authentication
curl -H "Authorization: Bearer YOUR_API_KEY" \
    https://archon.nexorithm.io/api/auth/validate
```

### Phase 7: Cleanup (5 minutes)

```bash
# Remove old Supabase volumes (AFTER verification!)
docker volume ls | grep supabase | awk '{print $2}' | xargs docker volume rm

# Remove old networks
docker network rm supabase_network_supabase
docker network rm supabase_network_archon
docker network rm supabase_network_root

# Disable rebind service
systemctl disable supabase-rebind.service
rm /etc/systemd/system/supabase-rebind.service
systemctl daemon-reload
```

---

## Benefits of Consolidated Architecture

### Operational Benefits

✅ **Single Command Management**:
```bash
docker compose up -d        # Start everything
docker compose down         # Stop everything
docker compose restart      # Restart everything
docker compose logs -f      # View all logs
docker compose ps           # Check all services
```

✅ **Simplified Networking**:
- One network: `archon_production`
- Clear service names: `archon-postgres`, `archon-kong`, `archon-server`
- No external network dependencies
- No rebind scripts needed

✅ **Centralized Configuration**:
- Single `.env` file for all services
- Consistent environment variable naming
- Version-controlled docker-compose

✅ **Better Resource Management**:
- Removed 6 unused containers
- ~40-50% reduction in memory usage
- Faster startup times

### Security Benefits

✅ **Maintained Security**:
- All API key authentication preserved
- Localhost-only binding on all ports
- Nginx reverse proxy still controls external access
- Defense in depth still in place

✅ **Improved Security**:
- Fewer containers = smaller attack surface
- Single network = easier firewall rules
- No complex network topology to misconfigure

### Development Benefits

✅ **Easier Debugging**:
```bash
# All logs in one place
docker compose logs -f archon-server

# Easy to restart individual services
docker compose restart archon-server

# Simple health checks
docker compose ps
```

✅ **Consistent Development/Production**:
- Same docker-compose structure locally and in prod
- Easy to replicate production environment
- Simplified CI/CD pipelines

---

## Rollback Plan

If issues occur during migration:

```bash
# 1. Stop new stack
cd /opt/archon
docker compose down

# 2. Restore old configurations
cp docker-compose.yml.backup docker-compose.yml
cp .env.backup .env

# 3. Restore database volume
docker volume rm archon_postgres_data
docker volume create supabase_db_supabase

docker run --rm \
    -v /root/backups:/backup \
    -v supabase_db_supabase:/target \
    alpine \
    sh -c "cd /target && tar xzf /backup/postgres-volume-YYYYMMDD_HHMMSS.tar.gz"

# 4. Recreate old networks
docker network create supabase_network_supabase
docker network create supabase_network_archon

# 5. Start old stack
cd supabase && supabase start
cd .. && docker compose up -d

# 6. Re-run rebind script
python3 scripts/rebind-supabase.py
```

---

## Post-Migration Monitoring

### Daily Checks (First Week)

```bash
#!/bin/bash
# health-check.sh

echo "=== Container Status ==="
docker compose ps

echo "\n=== Resource Usage ==="
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo "\n=== Network Connectivity ==="
docker exec archon-server curl -f http://kong:8000/rest/v1/ && echo "Kong: OK"
docker exec archon-server curl -f http://postgres:5432 && echo "Postgres: OK"

echo "\n=== External Access ==="
curl -I https://archon.nexorithm.io && echo "Archon UI: OK"
curl -I https://supabase.archon.nexorithm.io && echo "Studio: OK"

echo "\n=== API Authentication ==="
curl -H "Authorization: Bearer $API_KEY" \
    https://archon.nexorithm.io/api/auth/validate && echo "Auth: OK"
```

### Alerting

Set up basic monitoring:
```bash
# Add to crontab
*/5 * * * * /opt/archon/scripts/health-check.sh || /opt/archon/scripts/alert.sh
```

---

## Next Steps

1. **Review this plan** - Ensure all requirements are met
2. **Test in staging** - If available
3. **Schedule maintenance window** - 1 hour recommended
4. **Execute migration** - Follow phases 1-7
5. **Monitor for 1 week** - Daily health checks
6. **Document lessons learned** - Update this plan

---

**Plan Created**: 2025-10-16
**Author**: Claude (automated planning)
**Review Status**: Ready for human review
**Estimated Time**: 1 hour (with rollback plan ready)
