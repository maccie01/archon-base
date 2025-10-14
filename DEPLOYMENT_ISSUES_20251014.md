# Archon Server Deployment Issues - 2025-10-14

**Server**: netzwaechter (91.98.156.158)
**Domain**: archon.nexorithm.io
**Status**: Deployed but with configuration issues

---

## Critical Issues Found

### 1. ❌ Hardcoded Docker IP Addresses in .env

**Problem**: The `.env` file uses hardcoded Docker container IP addresses which will break when containers restart or network changes.

**Current Configuration** (in `/opt/archon/.env`):
```bash
SUPABASE_URL=http://172.18.0.5:8000
SUPABASE_DB_URL=postgresql://postgres:postgres@172.18.0.2:5432/postgres
OLLAMA_URL=http://172.18.0.1:11434
```

**Issue**:
- Docker assigns IP addresses dynamically
- IP `172.18.0.5` (Kong) and `172.18.0.2` (Postgres) can change on restart
- Services will fail to communicate if IPs change

**Impact**: HIGH - Services will fail after Docker restarts

**Solution**: Use Docker service names instead:
```bash
SUPABASE_URL=http://supabase_kong_archon:8000
SUPABASE_DB_URL=postgresql://postgres:postgres@supabase_db_archon:5432/postgres
OLLAMA_URL=http://host.docker.internal:11434  # Ollama runs on host
```

---

### 2. ❌ Port Bindings Restrict Access to Localhost Only

**Problem**: All Archon services are bound to `127.0.0.1` in docker-compose.yml, making them inaccessible from nginx reverse proxy.

**Current Configuration** (in `/opt/archon/docker-compose.yml`):
```yaml
archon-server:
  ports:
    - "127.0.0.1:8181:8181"  # Only accessible from localhost

archon-mcp:
  ports:
    - "127.0.0.1:8051:8051"  # Only accessible from localhost

archon-frontend:
  ports:
    - "127.0.0.1:3737:3737"  # Only accessible from localhost
```

**Issue**:
- Nginx running on host can access these ports
- But if we want to expose ports directly or use different network configs, this limits flexibility
- Not technically broken (nginx works) but not best practice for production

**Impact**: MEDIUM - Works but inflexible

**Recommendation**: Either:
1. Keep `127.0.0.1` bindings (current setup) - Services only accessible via nginx ✅
2. OR use Docker networks without port mapping (more secure)

---

### 3. ⚠️ Supabase Services Not on Same Docker Network

**Problem**: Supabase containers and Archon containers are on different Docker networks, requiring manual IP configuration.

**Current Networks**:
- **Supabase**: `supabase_network_archon`
- **Archon**: `app-network`

**Issue**:
- Services can't communicate using Docker service names
- Requires hardcoded IPs (see Issue #1)
- No automatic service discovery

**Impact**: HIGH - Creates dependency on Issue #1

**Solution**: Connect Archon containers to Supabase network:
```yaml
# In docker-compose.yml
networks:
  supabase_network_archon:
    external: true
  app-network:
    driver: bridge

services:
  archon-server:
    networks:
      - app-network
      - supabase_network_archon  # Add this
```

---

### 4. ✅ Nginx Configuration is Correct

**Status**: WORKING

The nginx configuration at `/etc/nginx/sites-available/archon` is properly configured:
- Main domain: `archon.nexorithm.io`
- Routes configured for: `/`, `/api/`, `/mcp/`, `/db/`
- Supabase subdomain: `supabase.archon.nexorithm.io`
- Proxying to correct localhost ports

**No action needed** ✅

---

### 5. ✅ Services Are Running

**Status**: ALL HEALTHY

```bash
CONTAINER        STATUS
archon-server    Up 36 minutes (healthy)
archon-mcp       Up 36 minutes (healthy)
archon-ui        Up 36 minutes (healthy)
supabase_*       Up 29 minutes (12 containers, all healthy)
```

**No action needed** ✅

---

## Recommended Fixes (Priority Order)

### Priority 1: Fix Hardcoded IPs and Network Configuration

**Steps**:

1. **Stop Archon services**:
```bash
cd /opt/archon
docker compose down
```

2. **Update .env file**:
```bash
# Replace hardcoded IPs with service names
sed -i 's|http://172.18.0.5:8000|http://supabase_kong_archon:8000|g' .env
sed -i 's|172.18.0.2:5432|supabase_db_archon:5432|g' .env
sed -i 's|http://172.18.0.1:11434|http://host.docker.internal:11434|g' .env
```

3. **Update docker-compose.yml to use Supabase network**:
```yaml
networks:
  supabase_network_archon:
    external: true
  app-network:
    driver: bridge

services:
  archon-server:
    networks:
      - app-network
      - supabase_network_archon

  archon-mcp:
    networks:
      - app-network
      - supabase_network_archon

  archon-frontend:
    networks:
      - app-network
      - supabase_network_archon
```

4. **Restart services**:
```bash
docker compose up -d
```

---

### Priority 2: Verify Access

**Test each service**:
```bash
# Frontend
curl -I http://localhost:3737

# Backend API
curl http://localhost:8181/health

# MCP Server
curl http://localhost:8051/health

# Supabase API
curl http://localhost:54321/

# Supabase Studio
curl -I http://localhost:54323
```

**Test through nginx**:
```bash
# From local machine
curl -I https://archon.nexorithm.io
curl https://archon.nexorithm.io/api/health
curl https://archon.nexorithm.io/mcp/health
```

---

## Current State Summary

| Component | Status | Issue |
|-----------|--------|-------|
| Archon Server | ✅ Running | ⚠️ Hardcoded IPs |
| Archon MCP | ✅ Running | ⚠️ Hardcoded IPs |
| Archon UI | ✅ Running | ✅ OK |
| Supabase (12 services) | ✅ Running | ✅ OK |
| Nginx Config | ✅ Correct | ✅ OK |
| SSL/TLS | ✅ Active | ✅ OK |
| Port Bindings | ⚠️ Localhost only | ⚠️ Acceptable |
| Docker Networks | ❌ Separated | ❌ Needs fix |

---

## Post-Fix Verification Checklist

- [ ] Archon containers on supabase network
- [ ] Services use Docker service names instead of IPs
- [ ] All containers restart successfully
- [ ] Frontend accessible at https://archon.nexorithm.io
- [ ] Backend API responding at https://archon.nexorithm.io/api/health
- [ ] MCP server accessible at https://archon.nexorithm.io/mcp/
- [ ] Supabase Studio accessible at https://archon.nexorithm.io/db/ (with auth)
- [ ] Supabase API accessible at https://supabase.archon.nexorithm.io
- [ ] Services survive docker compose restart
- [ ] Services survive server reboot

---

**Created**: 2025-10-14 22:10
**Server**: netzwaechter (91.98.156.158)
**Analyst**: Claude Code
