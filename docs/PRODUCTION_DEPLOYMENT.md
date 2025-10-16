# Archon Production Deployment Guide

**Last Updated**: 2025-10-16
**Architecture**: Consolidated Single-Network
**Status**: Production Ready

## Overview

Archon uses a consolidated Docker Compose architecture with all services running on a single bridge network. This deployment eliminates the complexity of the previous multi-network Supabase setup and provides unified service management.

## Architecture

### Network Topology

```
archon_production (172.21.0.0/16) - Single Bridge Network
├── Supabase Stack
│   ├── postgres:5432 (internal)
│   ├── rest:3000 (internal)
│   ├── kong:8000 → localhost:54321 (external proxy)
│   ├── meta:8080 (internal)
│   └── studio:3000 → localhost:54323 (external proxy)
└── Archon Stack
    ├── archon-server:8181 → localhost:8181
    ├── archon-mcp:8051 → localhost:8051
    └── archon-ui:3737 → localhost:3737
```

### Service Overview

| Service | Purpose | Port Binding | Health Check |
|---------|---------|--------------|--------------|
| **postgres** | PostgreSQL 17 + pgvector | 127.0.0.1:54322:5432 | pg_isready |
| **rest** | PostgREST v13.0.7 | Internal only | TCP check |
| **kong** | API Gateway + JWT transformation | 127.0.0.1:54321:8000 | kong health |
| **meta** | PostgreSQL metadata service | Internal only | TCP check |
| **studio** | Supabase Studio UI | 127.0.0.1:54323:3000 | Node.js HTTP (hostname-aware) |
| **archon-server** | FastAPI backend | 127.0.0.1:8181:8181 | Python HTTP check |
| **archon-mcp** | MCP server | 127.0.0.1:8051:8051 | Python socket check |
| **archon-ui** | React/Vite UI | 127.0.0.1:3737:3737 | curl HTTP check |

## Prerequisites

### Server Requirements

- **OS**: Ubuntu 20.04+ or Debian 11+
- **RAM**: 4GB minimum, 8GB recommended
- **CPU**: 2 cores minimum, 4 cores recommended
- **Disk**: 20GB minimum
- **Docker**: 24.0.0+
- **Docker Compose**: 2.20.0+

### Required Files

```
/opt/archon/
├── docker-compose.yml (from docker-compose.production.yml)
├── .env
├── volumes/
│   ├── api/
│   │   └── kong.yml
│   └── db/
│       └── init/
├── python/
├── archon-ui-main/
└── scripts/
```

## Installation

### 1. Initial Setup

```bash
# Create deployment directory
sudo mkdir -p /opt/archon
cd /opt/archon

# Clone repository (or copy files)
git clone <repository-url> .

# Copy production configuration
cp docker-compose.production.yml docker-compose.yml
```

### 2. Generate Secrets

The deployment uses specific secrets that must match the migrated database:

```bash
# JWT Secret (MUST match database-stored value)
JWT_SECRET="super-secret-jwt-token-with-at-least-32-characters-long"

# Generate other secrets
POSTGRES_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-32)
ARCHON_BOOTSTRAP_SECRET=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-32)
```

### 3. Generate JWT Tokens

JWT tokens must be signed with the database JWT secret:

```bash
# Helper function to generate JWT
generate_jwt() {
  local role=$1
  local secret="super-secret-jwt-token-with-at-least-32-characters-long"

  header='{"alg":"HS256","typ":"JWT"}'
  payload="{\"iss\":\"supabase-demo\",\"role\":\"$role\",\"exp\":1983812996}"

  header_b64=$(echo -n "$header" | openssl base64 -e -A | sed 's/+/-/g; s/\//_/g; s/=//g')
  payload_b64=$(echo -n "$payload" | openssl base64 -e -A | sed 's/+/-/g; s/\//_/g; s/=//g')
  signature=$(echo -n "${header_b64}.${payload_b64}" | openssl dgst -sha256 -hmac "$secret" -binary | openssl base64 -e -A | sed 's/+/-/g; s/\//_/g; s/=//g')

  echo "${header_b64}.${payload_b64}.${signature}"
}

# Generate tokens
SUPABASE_ANON_KEY=$(generate_jwt "anon")
SUPABASE_SERVICE_KEY=$(generate_jwt "service_role")
```

### 4. Create .env File

```bash
cat > /opt/archon/.env << 'EOF'
# PostgreSQL Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<generated-password>
POSTGRES_DB=postgres

# JWT Configuration (MUST match database-stored secret)
JWT_SECRET=super-secret-jwt-token-with-at-least-32-characters-long
JWT_EXP=3600

# Supabase API Keys
SUPABASE_ANON_KEY=<generated-anon-jwt>
SUPABASE_SERVICE_KEY=<generated-service-jwt>

# OpenAI API Key
OPENAI_API_KEY=<your-openai-key>

# Service Ports
ARCHON_SERVER_PORT=8181
ARCHON_MCP_PORT=8051
ARCHON_UI_PORT=3737
ARCHON_AGENTS_PORT=8052

# Features
AGENTS_ENABLED=false
PROD=true

# Logging
LOG_LEVEL=INFO
LOGFIRE_TOKEN=

# Security
ARCHON_BOOTSTRAP_SECRET=<generated-secret>

# Hosts
HOST=archon.nexorithm.io
VITE_ALLOWED_HOSTS=archon.nexorithm.io,supabase.archon.nexorithm.io,91.98.156.158,localhost,127.0.0.1
VITE_SHOW_DEVTOOLS=false
EOF
```

### 5. Configure Kong

Create `/opt/archon/volumes/api/kong.yml`:

```yaml
_format_version: "1.1"

services:
  - name: rest-v1
    _comment: "PostgREST: /rest/v1/* -> http://rest:3000/*"
    url: http://rest:3000/
    routes:
      - name: rest-v1-all
        strip_path: true
        paths:
          - /rest/v1/
    plugins:
      - name: cors
      - name: request-transformer
        config:
          remove:
            headers:
              - Authorization
              - authorization
          add:
            headers:
              - "Authorization: Bearer <SUPABASE_SERVICE_KEY>"

  - name: graphql-v1
    _comment: "PostgREST: /graphql/v1 -> http://rest:3000/rpc/graphql"
    url: http://rest:3000/rpc/graphql
    routes:
      - name: graphql-v1-all
        strip_path: true
        paths:
          - /graphql/v1
    plugins:
      - name: cors
      - name: request-transformer
        config:
          remove:
            headers:
              - Authorization
              - authorization
          add:
            headers:
              - "Content-Profile: graphql_public"
              - "Authorization: Bearer <SUPABASE_SERVICE_KEY>"

consumers: []
```

**Important**: Replace `<SUPABASE_SERVICE_KEY>` with the actual generated JWT token.

### 6. Deploy Services

```bash
cd /opt/archon

# Start all services
docker compose up -d

# Wait for services to become healthy
sleep 60

# Verify all services are healthy
docker compose ps
```

### 7. Configure Nginx Reverse Proxy

Create `/etc/nginx/sites-available/archon`:

```nginx
# Archon UI
server {
    listen 80;
    server_name archon.nexorithm.io;

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name archon.nexorithm.io;

    ssl_certificate /etc/letsencrypt/live/archon.nexorithm.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/archon.nexorithm.io/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:3737;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8181/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Supabase Studio
server {
    listen 80;
    server_name supabase.archon.nexorithm.io;

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name supabase.archon.nexorithm.io;

    ssl_certificate /etc/letsencrypt/live/archon.nexorithm.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/archon.nexorithm.io/privkey.pem;

    auth_basic "Supabase Studio Access";
    auth_basic_user_file /etc/nginx/.htpasswd-supabase;

    location / {
        proxy_pass http://127.0.0.1:54323;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the configuration:

```bash
sudo ln -s /etc/nginx/sites-available/archon /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Authentication Flow

### Kong JWT Transformation

Kong handles authentication by transforming requests:

1. **Client Request** → Kong receives request with any Authorization header
2. **Header Removal** → Kong removes incoming Authorization header
3. **JWT Injection** → Kong adds hardcoded service role JWT token
4. **PostgREST Validation** → PostgREST validates JWT against database secret
5. **Database Access** → Query executed with service_role permissions

This ensures all internal requests use the service role, while Archon implements its own API key authentication layer on top.

### Database JWT Secret

The JWT secret is stored at the database level in PostgreSQL's GUC settings:

```sql
-- View current JWT secret
SELECT current_setting('app.settings.jwt_secret');

-- Update JWT secret (requires superuser)
ALTER DATABASE postgres SET app.settings.jwt_secret = 'your-secret-here';
```

**Critical**: JWT tokens must be signed with the database-stored secret. Mismatches cause `PGRST301` errors.

## Management

### Service Operations

```bash
cd /opt/archon

# View service status
docker compose ps

# View logs for all services
docker compose logs -f

# View logs for specific service
docker compose logs -f archon-server

# Restart specific service
docker compose restart archon-server

# Restart all services
docker compose restart

# Stop all services
docker compose down

# Start all services
docker compose up -d

# Rebuild and restart specific service
docker compose up -d --build archon-server
```

### Health Monitoring

```bash
# Check all service health
docker compose ps --format 'table {{.Service}}\t{{.Status}}'

# Test Archon API health
curl http://localhost:8181/health

# Test PostgREST via Kong
curl 'http://localhost:54321/rest/v1/archon_settings?select=*&limit=1'

# Test external URLs
curl -k https://archon.nexorithm.io/api/health
curl -I -k https://archon.nexorithm.io
```

### Database Operations

```bash
# Connect to PostgreSQL
docker exec -it archon-postgres psql -U postgres -d postgres

# View running queries
docker exec -it archon-postgres psql -U postgres -d postgres -c "SELECT pid, usename, application_name, client_addr, state, query FROM pg_stat_activity WHERE state != 'idle';"

# Backup database
docker exec archon-postgres pg_dump -U postgres postgres > backup-$(date +%Y%m%d).sql

# Restore database
cat backup.sql | docker exec -i archon-postgres psql -U postgres -d postgres
```

## Troubleshooting

### Service Won't Start

**Symptom**: Container exits immediately or crashes on startup

**Common Causes**:
1. **Port already in use**: Check with `sudo lsof -i :<port>`
2. **Missing environment variables**: Verify `.env` file
3. **Network conflicts**: Check `docker network ls` for overlapping subnets

**Solution**:
```bash
# Check logs
docker compose logs <service-name>

# Rebuild container
docker compose up -d --build <service-name>

# Verify environment
docker compose config
```

### PGRST301 JWT Errors

**Symptom**: PostgREST returns `{"code":"PGRST301","message":"JWT cryptographic operation failed"}`

**Cause**: JWT tokens don't match database-stored secret

**Solution**:
1. Check database JWT secret: `docker exec archon-postgres psql -U postgres -c "SELECT current_setting('app.settings.jwt_secret');"`
2. Verify JWT_SECRET in `.env` matches database value
3. Regenerate JWT tokens using correct secret
4. Update Kong configuration with new tokens
5. Restart Kong: `docker compose restart kong`

### Healthcheck Failures

**Studio (unhealthy)**:
- **Cause**: Next.js binds to container hostname, not 127.0.0.1
- **Solution**: Healthcheck uses `os.hostname()` to resolve dynamically
- **Verify**: `docker exec archon-studio node -e "require('http').get('http://'+require('os').hostname()+':3000', r => console.log(r.statusCode))"`

**UI (unhealthy)**:
- **Cause**: Alpine container lacks bash
- **Solution**: Use curl instead of bash TCP check
- **Verify**: `docker exec archon-ui curl -f http://127.0.0.1:3737`

### Network Issues

**Symptom**: Services can't communicate

**Solution**:
```bash
# Verify network exists
docker network ls | grep archon_production

# Inspect network
docker network inspect archon_production

# Recreate network
docker compose down
docker network prune -f
docker compose up -d
```

### Kong Configuration Errors

**Symptom**: Kong container restarts repeatedly with config errors

**Common Issues**:
1. Invalid YAML syntax in `kong.yml`
2. Wrong format version (must be "1.1" for Kong 2.8.1)
3. Invalid JWT tokens in headers

**Solution**:
```bash
# Validate Kong config
docker compose config | grep -A 50 kong

# Check Kong logs
docker logs archon-kong

# Test Kong declarative config
docker exec archon-kong kong config parse /var/lib/kong/kong.yml
```

## Monitoring

### Metrics

Monitor these key indicators:

- **Container Health**: All services should show "healthy" status
- **Response Times**: API endpoints should respond < 200ms
- **Database Connections**: Monitor with `pg_stat_activity`
- **Memory Usage**: Check with `docker stats`

### Log Aggregation

```bash
# Stream all logs
docker compose logs -f --tail=100

# Search logs
docker compose logs | grep ERROR

# Export logs
docker compose logs > archon-logs-$(date +%Y%m%d).log
```

## Backup and Recovery

### Full Backup

```bash
#!/bin/bash
BACKUP_DIR="/root/backups/archon-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Database
docker exec archon-postgres pg_dumpall -U postgres > "$BACKUP_DIR/database.sql"

# Volumes
docker run --rm -v archon_postgres_data:/source:ro -v "$BACKUP_DIR":/backup alpine tar czf /backup/postgres-volume.tar.gz -C /source .

# Configuration
cp /opt/archon/.env "$BACKUP_DIR/env"
cp /opt/archon/docker-compose.yml "$BACKUP_DIR/"
cp -r /opt/archon/volumes "$BACKUP_DIR/"

echo "Backup complete: $BACKUP_DIR"
```

### Restore from Backup

```bash
BACKUP_DIR="/root/backups/archon-20251016_092340"

# Stop services
cd /opt/archon
docker compose down

# Restore database volume
docker volume rm archon_postgres_data
docker volume create archon_postgres_data
docker run --rm -v "$BACKUP_DIR":/backup -v archon_postgres_data:/target alpine sh -c "cd /target && tar xzf /backup/postgres-volume.tar.gz"

# Restore configuration
cp "$BACKUP_DIR/env" /opt/archon/.env
cp "$BACKUP_DIR/docker-compose.yml" /opt/archon/
cp -r "$BACKUP_DIR/volumes" /opt/archon/

# Start services
docker compose up -d
```

## Security Considerations

### Network Security

- All services bind to `127.0.0.1` only
- External access only through Nginx reverse proxy
- Supabase Studio protected with HTTP Basic Auth
- Cloudflare provides DDoS protection

### Secrets Management

- Never commit `.env` files to git
- Rotate secrets regularly (especially `ARCHON_BOOTSTRAP_SECRET`)
- Use different JWT secrets per environment
- Store backups encrypted

### Access Control

- Archon implements API key authentication
- Each user gets unique API key stored in database
- Bootstrap endpoint for initial setup only
- Regular audit of API key usage

## Performance Tuning

### PostgreSQL

Current settings (in `docker-compose.yml`):

```yaml
-c max_connections=200
-c shared_buffers=256MB
-c effective_cache_size=768MB
-c maintenance_work_mem=64MB
-c work_mem=1310kB
```

Adjust based on available RAM:

```bash
# For 8GB RAM server
shared_buffers=2GB
effective_cache_size=6GB
maintenance_work_mem=512MB
work_mem=10MB
```

### Docker Resource Limits

Add to `docker-compose.yml`:

```yaml
services:
  archon-server:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

## Updates and Maintenance

### Updating Services

```bash
cd /opt/archon

# Pull latest changes
git pull

# Rebuild specific service
docker compose up -d --build archon-server

# Or rebuild all
docker compose up -d --build
```

### Database Migrations

```bash
# Run migrations
docker exec -it archon-server python -m alembic upgrade head

# Create new migration
docker exec -it archon-server python -m alembic revision -m "description"
```

### Cleanup

```bash
# Remove unused Docker resources
docker system prune -a --volumes -f

# Remove old images
docker images | grep archon | awk '{print $3}' | xargs docker rmi -f
```

## Migration from Old Architecture

If migrating from the previous multi-network Supabase setup:

1. **Backup everything** (database, volumes, configs)
2. **Stop old services**: `cd /opt/archon/supabase && supabase stop`
3. **Deploy new stack**: Follow installation steps above
4. **Migrate data**: Restore database from backup
5. **Verify services**: Check all healthchecks pass
6. **Test functionality**: Verify API, UI, and Studio access
7. **Clean up**: Run `/opt/archon/scripts/cleanup-old-architecture.sh`

## Support

For issues:
1. Check this documentation
2. Review logs: `docker compose logs -f`
3. Verify configuration: `docker compose config`
4. Check network: `docker network inspect archon_production`

## Appendix

### Port Reference

| Port | Service | Access |
|------|---------|--------|
| 54321 | Kong (Supabase API) | localhost only |
| 54322 | PostgreSQL | localhost only |
| 54323 | Supabase Studio | localhost only (Nginx proxy) |
| 8181 | Archon Backend API | localhost only (Nginx proxy) |
| 8051 | Archon MCP Server | localhost only |
| 3737 | Archon UI | localhost only (Nginx proxy) |

### Environment Variable Reference

See `.env.example` in repository for complete list with descriptions.

### Health Check Commands

```bash
# All services
docker compose ps --format 'table {{.Service}}\t{{.Status}}'

# Individual checks
curl http://localhost:8181/health                              # Archon API
curl http://localhost:54321/rest/v1/archon_settings?limit=1   # PostgREST via Kong
curl http://localhost:3737                                     # UI
curl http://localhost:54323                                    # Studio
```
