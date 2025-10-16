# Archon Deployment Quick Start

Created: 2025-10-16
Last Updated: 2025-10-16

## 5-Minute Quick Reference

Essential commands and access information for daily Archon operations.

## SSH Access

```bash
# Connect to production server
ssh -i ~/.ssh/netzwaechter_deployment root@91.98.156.158

# Server details
# IP: 91.98.156.158
# OS: Ubuntu 22.04 LTS
# Location: /opt/archon
```

## Service URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| Frontend | https://archon.nexorithm.io | None (public) |
| API | https://archon.nexorithm.io/api | API key required |
| Supabase Studio | https://supabase.archon.nexorithm.io | See core/CREDENTIALS.md |
| Arcane (Docker UI) | https://arcane.nexorithm.io | Username: `admin`, Password: See core/CREDENTIALS.md |

## Common Operations

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f archon-server
docker compose logs -f archon-ui
docker compose logs -f archon-mcp

# Nginx logs
tail -f /var/log/nginx/archon-access.log
tail -f /var/log/nginx/archon-error.log
```

### Restart Services
```bash
# All services
docker compose restart

# Specific service
docker compose restart archon-server

# Full rebuild
docker compose down
docker compose up -d --build
```

### Health Checks
```bash
# Check all containers
docker compose ps

# Check service health
curl http://localhost:8181/health    # API
curl http://localhost:8051/health    # MCP
curl http://localhost:3737/          # Frontend

# Check from outside
curl https://archon.nexorithm.io/api/health
```

### Deploy Updates
```bash
# Standard deployment
cd /opt/archon
git pull origin stable
docker compose build
docker compose up -d

# Verify deployment
docker compose ps
docker compose logs -f archon-server
```

## File Locations

| File | Purpose |
|------|---------|
| `/opt/archon/.env` | Environment configuration |
| `/opt/archon/docker-compose.yml` | Container orchestration |
| `/etc/nginx/sites-available/archon` | Nginx config |
| `/opt/archon/migration/` | Database migrations |

## Emergency Contacts

**Documentation**: [README.md](./README.md)
**Server Info**: [core/DEPLOYMENT_SUMMARY.md](./core/DEPLOYMENT_SUMMARY.md)
**Credentials**: [core/CREDENTIALS.md](./core/CREDENTIALS.md)
**Troubleshooting**: [README.md#troubleshooting](./README.md#troubleshooting)

## Quick Troubleshooting

### Service Won't Start
```bash
# Check logs
docker compose logs archon-server

# Restart service
docker compose restart archon-server

# Full rebuild
docker compose down
docker compose up -d --build archon-server
```

### 502 Bad Gateway
```bash
# Check if backend is running
docker compose ps
curl http://localhost:8181/health

# Check Nginx logs
tail -f /var/log/nginx/archon-error.log

# Restart services
docker compose restart
```

### API Authentication Errors
```bash
# Verify API key in database (Supabase Studio)
# Check AUTH_ENABLED setting
cat /opt/archon/.env | grep AUTH_ENABLED

# Test API key
curl -H "Authorization: Bearer YOUR_API_KEY" \
  http://localhost:8181/api/auth/validate
```

## Next Steps

For detailed information, see:
- **Full Deployment Guide**: [README.md](./README.md)
- **Core Configuration**: [core/](./core/)
- **Security**: [security/](./security/)
- **Services**: [services/](./services/)
- **Organization Index**: [INDEX.md](./INDEX.md)
