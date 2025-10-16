# Archon Production Deployment Documentation

**Created**: 2025-10-15
**Updated**: 2025-10-16 (Consolidated Architecture)
**Server**: Hetzner Cloud (91.98.156.158)
**Domain**: archon.nexorithm.io
**Status**: ✅ Production Ready
**Architecture**: v1.3.0 (Single-Network Consolidated)

---

## Table of Contents

1. [Overview](#overview)
2. [Server Infrastructure](#server-infrastructure)
3. [Architecture](#architecture)
4. [Deployment Process](#deployment-process)
5. [Credentials & Access](#credentials--access)
6. [Maintenance](#maintenance)
7. [Troubleshooting](#troubleshooting)

---

## Overview

Archon is a knowledge management and AI automation platform deployed on Hetzner Cloud infrastructure using a **consolidated single-network architecture** (v1.3.0).

### Core Services (8 containers)

**Archon Application** (3 services):
- **archon-server**: FastAPI backend (Python)
- **archon-mcp**: MCP (Model Context Protocol) server
- **archon-ui**: React frontend (TypeScript)

**Supabase Self-Hosted** (5 services):
- **supabase-db**: PostgreSQL 17.6 with pgvector
- **supabase-kong**: Kong API Gateway (JWT transformation)
- **supabase-rest**: PostgREST automatic REST API
- **supabase-meta**: PostgreSQL metadata service
- **supabase-studio**: Web-based database admin

**Architecture**:
- Single Docker network: `archon_production` (172.21.0.0/16)
- Single docker-compose.yml for all services
- No Supabase CLI (direct Docker Compose management)
- All healthchecks passing
- 40-50% resource reduction vs. previous multi-network architecture

---

## Server Infrastructure

### Server Details

- **Provider**: Hetzner Cloud
- **IP Address**: 91.98.156.158
- **OS**: Ubuntu 22.04 LTS
- **Region**: Germany
- **RAM**: 16GB
- **CPU**: 4 vCPU
- **Storage**: 160GB SSD

### Domain & SSL

- **Primary Domain**: archon.nexorithm.io
- **Subdomain**: supabase.archon.nexorithm.io
- **CDN**: Cloudflare (proxy enabled)
- **SSL**: Cloudflare Universal SSL + Let's Encrypt for subdomain

### SSH Access

**Key File**: `~/.ssh/netzwaechter_deployment`

```bash
# Connect to server
ssh -i ~/.ssh/netzwaechter_deployment root@91.98.156.158

# Or if SSH config is set up
ssh netzwaechter-prod
```

**SSH Public Key Fingerprint**: `SHA256:7tVzuYLSTnjuQuxsNL2dw5QqNjBAsNMVaZJvPZmAm0w`

---

## Architecture

### System Components (Consolidated Architecture v1.3.0)

```
┌─────────────────────────────────────────────────────────────┐
│                     Cloudflare CDN                           │
│         archon.nexorithm.io + supabase.archon.nexorithm.io  │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   Nginx Reverse Proxy (80, 443)              │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ / → 3737     │ /api → 8181  │ /mcp → 8051  │subdomain→54323 │
└──────┬───────┴──────┬───────┴──────┬───────┴──────┬─────────┘
       │              │               │              │
       │              │               │              │
       │    ┌─────────┴───────────────┴──────────────┴─────────┐
       │    │  archon_production network (172.21.0.0/16)       │
       │    │  Single Docker Compose (8 containers)            │
       │    └──────────────────────────────────────────────────┘
       │              │               │              │
       ▼              ▼               ▼              ▼
┌─────────────┐ ┌──────────┐  ┌──────────┐  ┌───────────────┐
│ archon-ui   │ │ archon-  │  │ archon-  │  │ supabase-     │
│ (React)     │ │ server   │  │ mcp      │  │ studio        │
│ Port: 3737  │ │ (FastAPI)│  │ Port:8051│  │ Port: 54323   │
└─────────────┘ └─────┬────┘  └──────────┘  └───────────────┘
                      │
       ┌──────────────┴─────────────────────┐
       │    Supabase Services (5 containers) │
       │    Single Network (no external)     │
       └──────────────┬─────────────────────┘
                      │
       ┌──────────────┴─────────────────────┐
       │                                     │
       ▼                                     ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ supabase-db  │  │ supabase-    │  │ supabase-    │
│ PostgreSQL   │  │ kong         │  │ rest         │
│ Port: 54322  │  │ (Gateway)    │  │ (PostgREST)  │
│              │  │ Port: 54321  │  │ Port: 3000   │
└──────────────┘  └──────────────┘  └──────────────┘
                         │
                         ├─ Removes Authorization headers
                         ├─ Adds service JWT (hardcoded)
                         └─ Prevents PGRST301 errors
```

### Port Mapping (Consolidated Architecture)

**Archon Services**:
| Service | Internal Port | External Access | Purpose |
|---------|--------------|-----------------|---------|
| archon-ui | 3737 | via Nginx (/) | Frontend application |
| archon-server | 8181 | via Nginx (/api) | Backend API |
| archon-mcp | 8051 | via Nginx (/mcp) | MCP server |

**Supabase Services**:
| Service | Internal Port | External Access | Purpose |
|---------|--------------|-----------------|---------|
| supabase-kong | 54321 | Internal only | API Gateway (JWT transform) |
| supabase-db | 54322 | Internal + localhost | PostgreSQL database |
| supabase-rest | 3000 | via Kong only | PostgREST API |
| supabase-meta | Internal | Internal only | Metadata service |
| supabase-studio | 54323 | via Nginx (subdomain) | Database admin UI |

### Docker Network (Consolidated)

- **Network Name**: `archon_production`
- **Type**: Bridge network
- **Subnet**: 172.21.0.0/16
- **Services**: All 8 containers on same network
- **Internal DNS**: Services resolve by container name
- **Benefits**:
  - Single network topology (no external networks)
  - Simplified service discovery
  - Easier troubleshooting
  - Better isolation

---

## Deployment Process

### Initial Setup (One-Time)

1. **Server Provisioning**
   ```bash
   # Update system
   apt update && apt upgrade -y

   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh

   # Install Docker Compose
   apt install docker-compose-plugin -y

   # Install Nginx
   apt install nginx -y
   ```

2. **Clone Repository**
   ```bash
   cd /opt
   git clone https://github.com/maccie01/archon-base.git archon
   cd archon
   git checkout stable
   ```

3. **Configure Environment**
   ```bash
   # Copy example and configure
   cp .env.example .env
   nano .env  # Edit with actual credentials
   ```

4. **Configure Nginx**
   ```bash
   # Copy Nginx config
   cp /opt/archon/.deployment/archon/nginx/archon.conf /etc/nginx/sites-available/archon
   ln -s /etc/nginx/sites-available/archon /etc/nginx/sites-enabled/archon

   # Test and reload
   nginx -t
   systemctl reload nginx
   ```

5. **Initial Database Setup**
   ```bash
   # Apply migrations via Supabase Dashboard
   # SQL Editor → Run migration files in order:
   # 1. migration/add_source_url_display_name.sql
   # 2. migration/add_api_keys_table.sql
   ```

6. **Build and Start Services**
   ```bash
   cd /opt/archon
   docker compose build
   docker compose up -d
   ```

### Deployment Updates

**Standard Deployment Process**:

```bash
# 1. SSH to server
ssh -i ~/.ssh/netzwaechter_deployment root@91.98.156.158

# 2. Navigate to project
cd /opt/archon

# 3. Pull latest changes
git fetch origin
git checkout stable
git pull origin stable

# 4. Check for environment changes
git diff HEAD@{1} .env.example
# If changed, update .env accordingly

# 5. Rebuild services (if code changed)
docker compose build archon-server archon-mcp archon-frontend

# 6. Restart services
docker compose up -d

# 7. Verify health
docker compose ps
curl http://localhost:8181/health
curl http://localhost:3737/
```

**Quick Restart** (no code changes):
```bash
cd /opt/archon
docker compose restart
```

**Full Rebuild** (major changes):
```bash
cd /opt/archon
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Database Migrations

```bash
# 1. Create migration file locally
# migration/new_migration_YYYYMMDD.sql

# 2. Commit and push
git add migration/new_migration_YYYYMMDD.sql
git commit -m "feat(db): add new migration"
git push origin stable

# 3. Apply on server via Supabase Dashboard
# - Login to Supabase dashboard
# - Navigate to SQL Editor
# - Copy migration content
# - Execute SQL

# 4. Verify migration
# Check that new tables/columns exist
```

---

## Credentials & Access

See detailed credentials in:
- [CREDENTIALS.md](./CREDENTIALS.md) - All API keys, passwords, tokens
- [ENVIRONMENT.md](./ENVIRONMENT.md) - Complete .env file reference

### Quick Reference

**Production URLs**:
- Frontend: https://archon.nexorithm.io
- API: https://archon.nexorithm.io/api
- MCP: https://archon.nexorithm.io/mcp
- Supabase Studio: https://archon.nexorithm.io/db

**API Authentication**:
```bash
# Test API with authentication
curl -H "Authorization: Bearer ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI" \
  https://archon.nexorithm.io/api/knowledge-items/summary?page=1&per_page=10
```

---

## Maintenance

### Log Access

```bash
# View all container logs
docker compose logs -f

# View specific service logs
docker compose logs -f archon-server
docker compose logs -f archon-ui
docker compose logs -f archon-mcp

# View Nginx logs
tail -f /var/log/nginx/archon-access.log
tail -f /var/log/nginx/archon-error.log
```

### Health Checks

```bash
# Check container status
docker compose ps

# Check service health
curl http://localhost:8181/health
curl http://localhost:8051/health
curl http://localhost:3737/

# Check Nginx status
systemctl status nginx

# Check disk space
df -h

# Check memory usage
free -h

# Check Docker resource usage
docker stats --no-stream
```

### Backup Procedures

**Database Backup**:
```bash
# Supabase provides automatic backups
# Manual backup via Supabase Dashboard:
# Database → Backups → Create backup

# Or use pg_dump (if direct access configured)
```

**Application Backup**:
```bash
# Backup environment and configurations
cd /opt/archon
tar -czf /root/backups/archon-config-$(date +%Y%m%d).tar.gz \
  .env docker-compose.yml /etc/nginx/sites-available/archon
```

**Git Backup**:
```bash
# Ensure all changes are committed
cd /opt/archon
git status
git add .
git commit -m "chore: backup server state"
git push origin stable
```

### Updates & Security

**System Updates**:
```bash
# Monthly security updates
apt update
apt upgrade -y
apt autoremove -y

# Reboot if kernel updated
reboot
```

**Docker Updates**:
```bash
# Update Docker images
cd /opt/archon
docker compose pull
docker compose up -d
```

**Certificate Renewal** (Let's Encrypt for subdomain):
```bash
# Automatic renewal via cron
# Check status:
certbot certificates

# Manual renewal if needed:
certbot renew
systemctl reload nginx
```

---

## Troubleshooting

### Common Issues

#### 1. Service Not Starting

```bash
# Check container logs
docker compose logs archon-server

# Check if port is in use
netstat -tulpn | grep 8181

# Restart service
docker compose restart archon-server

# Full rebuild if needed
docker compose build --no-cache archon-server
docker compose up -d archon-server
```

#### 2. 502 Bad Gateway

**Symptoms**: Nginx returns 502 error

**Causes & Solutions**:
```bash
# Check if backend is running
docker compose ps
curl http://localhost:8181/health

# Check Nginx error logs
tail -f /var/log/nginx/archon-error.log

# Restart services
docker compose restart

# Check Docker network
docker network inspect archon_default
```

#### 3. Authentication Errors (401)

**Symptoms**: API returns 401 Unauthorized

**Solutions**:
```bash
# Verify API key is valid
# Check database:
# Supabase Dashboard → Table Editor → api_keys

# Check if AUTH_ENABLED in .env
cat /opt/archon/.env | grep AUTH_ENABLED

# Test API directly
curl -H "Authorization: Bearer YOUR_API_KEY" \
  http://localhost:8181/api/auth/validate
```

#### 4. Database Connection Issues

**Symptoms**: "Could not connect to database"

**Solutions**:
```bash
# Check Supabase credentials in .env
cat /opt/archon/.env | grep SUPABASE

# Test connection
curl -H "apikey: YOUR_SUPABASE_ANON_KEY" \
  "https://YOUR_PROJECT.supabase.co/rest/v1/"

# Restart services
docker compose restart
```

#### 5. Frontend Not Loading

**Symptoms**: Blank page or 404 errors

**Solutions**:
```bash
# Check if nginx is serving files
docker compose exec archon-ui ls -la /usr/share/nginx/html

# Check Nginx config
nginx -t
cat /etc/nginx/sites-enabled/archon

# Rebuild frontend
cd /opt/archon
docker compose build --no-cache archon-frontend
docker compose up -d archon-frontend

# Clear Cloudflare cache
# Cloudflare Dashboard → Caching → Purge Everything
```

#### 6. Disk Space Full

```bash
# Check disk usage
df -h

# Clean Docker
docker system prune -a --volumes
# WARNING: This removes unused images, containers, and volumes

# Clean logs
journalctl --vacuum-time=7d
rm -f /var/log/nginx/*.log.*.gz
```

### Emergency Contacts & Resources

**Documentation**:
- Archon GitHub: https://github.com/maccie01/archon-base
- Hetzner Docs: https://docs.hetzner.com
- Docker Docs: https://docs.docker.com
- Nginx Docs: https://nginx.org/en/docs/

**Support Channels**:
- GitHub Issues: https://github.com/maccie01/archon-base/issues
- Hetzner Support: https://console.hetzner.cloud/

**Monitoring**:
- Cloudflare Analytics: https://dash.cloudflare.com
- Supabase Dashboard: https://supabase.com/dashboard

---

## Deployment History

| Date | Version | Changes | By |
|------|---------|---------|-----|
| 2025-10-16 | v1.3.0 | Consolidated single-network architecture (8 services) | Claude Code |
| 2025-10-16 | v1.3.0 | Removed unused Supabase services (11→5 containers) | Claude Code |
| 2025-10-16 | v1.3.0 | Kong JWT transformation configured | Claude Code |
| 2025-10-15 | v1.2.0 | Deployed production build with Nginx | Claude Code |
| 2025-10-15 | v1.1.1 | Fixed Authorization header in API client | Claude Code |
| 2025-10-15 | v1.1.0 | Implemented API key authentication system | Claude Code |
| 2025-10-14 | v1.0.0 | Initial production deployment | Team |

---

## Additional Documentation

- [CREDENTIALS.md](./CREDENTIALS.md) - Complete credentials reference
- [ENVIRONMENT.md](./ENVIRONMENT.md) - Environment variables documentation
- [NGINX_CONFIG.md](./NGINX_CONFIG.md) - Nginx configuration reference
- [DOCKER_SETUP.md](./DOCKER_SETUP.md) - Docker Compose configuration
- [AUTHENTICATION.md](./AUTHENTICATION.md) - Authentication system guide
- [API_REFERENCE.md](./API_REFERENCE.md) - API endpoints documentation

---

**Last Updated**: 2025-10-15
**Maintained By**: Development Team
**Review Schedule**: Monthly
