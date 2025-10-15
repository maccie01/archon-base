# Archon Docker Setup

**Created**: 2025-10-15
**Docker Compose Version**: 2.x
**Status**: Production Ready

---

## Docker Compose Configuration

### File Location

`/opt/archon/docker-compose.yml`

### Services Overview

```yaml
services:
  archon-server:      # FastAPI backend
  archon-mcp:         # Model Context Protocol server
  archon-frontend:    # React UI (production build with nginx)
```

---

## Service Details

### 1. archon-server (Backend)

**Image**: Built from `python/Dockerfile.server`
**Port**: 8181 (internal and external)
**Purpose**: Main FastAPI backend API

**Configuration**:
```yaml
archon-server:
  build:
    context: ./python
    dockerfile: Dockerfile.server
    args:
      BUILDKIT_INLINE_CACHE: 1
      ARCHON_SERVER_PORT: ${ARCHON_SERVER_PORT:-8181}
  container_name: archon-server
  ports:
    - "${ARCHON_SERVER_PORT:-8181}:8181"
  environment:
    - SUPABASE_URL=${SUPABASE_URL}
    - SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
    - SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}
    - ARCHON_SERVER_PORT=${ARCHON_SERVER_PORT:-8181}
    - AUTH_ENABLED=${AUTH_ENABLED:-false}
    - ARCHON_BOOTSTRAP_SECRET=${ARCHON_BOOTSTRAP_SECRET}
    - ALLOWED_ORIGINS=${ALLOWED_ORIGINS:-*}
  networks:
    - default
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8181/health"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 40s
  restart: unless-stopped
```

**Health Check**:
- Endpoint: `http://localhost:8181/health`
- Interval: Every 30 seconds
- Timeout: 10 seconds
- Healthy when returns 200 OK

### 2. archon-mcp (MCP Server)

**Image**: Built from `python/Dockerfile.mcp`
**Port**: 8051 (internal and external)
**Purpose**: Model Context Protocol server for AI integrations

**Configuration**:
```yaml
archon-mcp:
  build:
    context: ./python
    dockerfile: Dockerfile.mcp
  container_name: archon-mcp
  ports:
    - "${ARCHON_MCP_PORT:-8051}:8051"
  environment:
    - ARCHON_MCP_PORT=${ARCHON_MCP_PORT:-8051}
  networks:
    - default
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8051/health"]
    interval: 30s
    timeout: 10s
    retries: 3
  restart: unless-stopped
```

### 3. archon-frontend (React UI - Production)

**Image**: Built from `archon-ui-main/Dockerfile.prod` (multi-stage with nginx)
**Port**: 3737 (internal and external)
**Purpose**: Serve production React application

**Configuration**:
```yaml
archon-frontend:
  build:
    context: ./archon-ui-main
    dockerfile: Dockerfile.prod
  container_name: archon-ui
  ports:
    - "${ARCHON_UI_PORT:-3737}:3737"
  environment:
    # Not needed for production build (compiled at build time)
    - VITE_ARCHON_SERVER_PORT=${ARCHON_SERVER_PORT:-8181}
  networks:
    - default
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:3737/"]
    interval: 30s
    timeout: 10s
    retries: 3
  restart: unless-stopped
  depends_on:
    archon-server:
      condition: service_healthy
```

**Notes**:
- Uses multi-stage Dockerfile (build → nginx serve)
- Nginx serves static files from `/usr/share/nginx/html`
- API requests proxied to archon-server via Nginx config
- No Vite dev server in production

---

## Dockerfiles

### Backend Dockerfile (`python/Dockerfile.server`)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY pyproject.toml poetry.lock* ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy application code
COPY . .

# Expose port
EXPOSE ${ARCHON_SERVER_PORT:-8181}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:${ARCHON_SERVER_PORT:-8181}/health || exit 1

# Start server
CMD ["python", "-m", "uvicorn", "src.server.main:app", "--host", "0.0.0.0", "--port", "8181"]
```

### MCP Dockerfile (`python/Dockerfile.mcp`)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY . .

EXPOSE ${ARCHON_MCP_PORT:-8051}

CMD ["python", "-m", "src.mcp_server.main"]
```

### Frontend Dockerfile - Production (`archon-ui-main/Dockerfile.prod`)

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache python3 make g++ git

# Install npm dependencies
COPY package*.json ./
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3737

CMD ["nginx", "-g", "daemon off;"]
```

---

## Docker Networks

### Default Bridge Network

**Name**: `archon_default` (auto-created by Docker Compose)
**Type**: bridge
**Services**: All three containers

**Service DNS Resolution**:
- `archon-server` → resolves to backend container
- `archon-mcp` → resolves to MCP container
- `archon-ui` → resolves to frontend container

**Example**:
```bash
# From within archon-ui container
curl http://archon-server:8181/health
```

---

## Volume Management

### Current Setup

No persistent volumes defined (stateless containers)

**Data Storage**:
- Database: External Supabase (not in Docker)
- Uploads: Could add volume if needed
- Logs: Container logs via `docker compose logs`

### Adding Volumes (If Needed)

```yaml
volumes:
  archon-data:
    driver: local

services:
  archon-server:
    volumes:
      - archon-data:/app/data
```

---

## Common Operations

### Build Services

```bash
# Build all services
docker compose build

# Build specific service
docker compose build archon-server

# Build without cache
docker compose build --no-cache

# Build with progress
docker compose build --progress=plain
```

### Start Services

```bash
# Start all services
docker compose up -d

# Start specific service
docker compose up -d archon-server

# Start with logs
docker compose up

# Start and rebuild
docker compose up -d --build
```

### Stop Services

```bash
# Stop all services
docker compose stop

# Stop specific service
docker compose stop archon-ui

# Stop and remove containers
docker compose down

# Stop and remove everything (including volumes)
docker compose down -v
```

### Restart Services

```bash
# Restart all
docker compose restart

# Restart specific service
docker compose restart archon-server

# Restart with rebuild
docker compose up -d --force-recreate archon-server
```

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f archon-server

# Last 100 lines
docker compose logs --tail=100 archon-server

# Since timestamp
docker compose logs --since 2025-10-15T10:00:00

# JSON format
docker compose logs --json
```

### Check Status

```bash
# List running containers
docker compose ps

# Show service details
docker compose ps -a

# Show resource usage
docker compose stats
```

### Execute Commands

```bash
# Open shell in container
docker compose exec archon-server bash

# Run one-off command
docker compose exec archon-server curl http://localhost:8181/health

# Run as root
docker compose exec -u root archon-server bash
```

---

## Build Process

### Production Build Workflow

1. **Pull Latest Code**:
   ```bash
   cd /opt/archon
   git pull origin stable
   ```

2. **Update Environment** (if needed):
   ```bash
   nano .env
   ```

3. **Build Services**:
   ```bash
   # Backend
   docker compose build --no-cache archon-server

   # MCP
   docker compose build --no-cache archon-mcp

   # Frontend
   docker compose build --no-cache archon-frontend
   ```

4. **Start Services**:
   ```bash
   docker compose up -d
   ```

5. **Verify Health**:
   ```bash
   docker compose ps
   curl http://localhost:8181/health
   curl http://localhost:3737/
   ```

### Development Build

For local development, use `Dockerfile` (dev server) instead of `Dockerfile.prod`:

```yaml
# In docker-compose.yml (or docker-compose.dev.yml)
archon-frontend:
  build:
    context: ./archon-ui-main
    dockerfile: Dockerfile  # Dev server, not nginx
```

---

## Debugging

### Container Issues

**Container Won't Start**:
```bash
# Check logs
docker compose logs archon-server

# Check events
docker events --since 10m

# Inspect container
docker inspect archon-server

# Check resource limits
docker stats archon-server
```

**Health Check Failing**:
```bash
# Test health check manually
docker compose exec archon-server curl -f http://localhost:8181/health

# Check health status
docker inspect archon-server | grep -A 10 Health
```

**Network Issues**:
```bash
# Inspect network
docker network inspect archon_default

# Test connectivity between containers
docker compose exec archon-ui curl http://archon-server:8181/health
```

### Build Issues

**Build Failing**:
```bash
# Build with verbose output
docker compose build --progress=plain archon-server

# Check Dockerfile syntax
docker compose config

# Clear build cache
docker builder prune -a
```

**Slow Builds**:
```bash
# Use BuildKit
export DOCKER_BUILDKIT=1
docker compose build

# Use layer caching
# Already configured with BUILDKIT_INLINE_CACHE
```

---

## Performance Optimization

### Resource Limits

Add resource constraints to prevent container overuse:

```yaml
services:
  archon-server:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

### Image Size Optimization

**Current Sizes**:
- archon-server: ~500MB (Python + dependencies)
- archon-mcp: ~450MB (Python + dependencies)
- archon-frontend: ~25MB (nginx alpine + static files)

**Optimization Tips**:
- ✅ Multi-stage builds (already used for frontend)
- ✅ Alpine base images where possible
- ✅ .dockerignore to exclude unnecessary files
- ✅ Layer caching for faster rebuilds

### Build Cache

**.dockerignore** (already configured):
```
node_modules
.git
.env
*.log
dist
coverage
.pytest_cache
__pycache__
```

---

## Security

### Image Scanning

```bash
# Scan for vulnerabilities
docker scout cves archon-archon-server
docker scout recommendations archon-archon-server

# Or use Trivy
trivy image archon-archon-server
```

### Non-Root Users

Consider running containers as non-root:

```dockerfile
# In Dockerfile
RUN useradd -m -u 1000 archon
USER archon
```

### Secrets Management

**Current**: Environment variables via `.env`

**Better**: Docker secrets (for sensitive data):
```yaml
secrets:
  supabase_key:
    file: ./secrets/supabase_key.txt

services:
  archon-server:
    secrets:
      - supabase_key
```

---

## Monitoring

### Container Metrics

```bash
# Real-time stats
docker stats --no-stream archon-server archon-mcp archon-ui

# Resource usage over time
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### Logs

**Centralized Logging** (optional):

```yaml
services:
  archon-server:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## Backup & Restore

### Backup Containers

```bash
# Export container state
docker commit archon-server archon-server-backup:$(date +%Y%m%d)

# Save image
docker save archon-server-backup:20251015 | gzip > archon-server-backup.tar.gz
```

### Restore from Backup

```bash
# Load image
docker load < archon-server-backup.tar.gz

# Run container
docker run -d --name archon-server archon-server-backup:20251015
```

---

**Last Updated**: 2025-10-15
**Review Schedule**: Quarterly
