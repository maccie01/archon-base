# Arcane Docker Management Interface

Created: 2025-10-16
Last Updated: 2025-10-16

## Overview

Arcane is a lightweight, web-based Docker container management and monitoring interface deployed on the Archon production server. It provides a modern UI for managing all Docker containers, images, and resources.

**Access URL**: https://arcane.nexorithm.io
**Container**: `ghcr.io/ofkm/arcane:latest`

## Quick Access

**URL**: https://arcane.nexorithm.io

**Default Credentials** (change after first login):
- Username: `arcane`
- Password: `arcane-admin`

See [../../core/CREDENTIALS.md](../../core/CREDENTIALS.md) for current credentials.

## Features

### Container Management
- View all running and stopped containers
- Start/stop/restart containers
- View container logs in real-time
- Execute commands in containers
- Monitor resource usage (CPU, memory, network)
- View container details and configuration

### Image Management
- List all Docker images
- Pull new images from registries
- Remove unused images
- View image details and layers

### System Monitoring
- Docker system stats
- Container health monitoring
- Resource usage dashboards

## Configuration

### Container Details
| Setting | Value |
|---------|-------|
| Port | 127.0.0.1:3552 (localhost only) |
| Restart Policy | unless-stopped |
| Docker Socket | /var/run/docker.sock (read/write) |
| Data Volume | arcane-data |
| User | root (0:0) |

### Environment Variables
| Variable | Purpose |
|----------|---------|
| APP_URL | https://arcane.nexorithm.io |
| ENCRYPTION_KEY | Data encryption |
| JWT_SECRET | JWT token security |

See docker-compose.yml for full configuration.

### Network Configuration
- Bound to localhost only (127.0.0.1:3552)
- External access via Nginx reverse proxy
- Rate limiting: 100 req/min per IP
- WebSocket support enabled for real-time updates
- SSL/TLS via Cloudflare

## Common Operations

### View Logs
```bash
ssh netzwaechter-prod "docker logs arcane --tail 100 -f"
```

### Restart Arcane
```bash
ssh netzwaechter-prod "cd /opt/arcane && docker compose restart"
```

### Update Arcane
```bash
ssh netzwaechter-prod "cd /opt/arcane && docker compose pull && docker compose up -d"
```

### Check Status
```bash
ssh netzwaechter-prod "docker ps | grep arcane"
curl https://arcane.nexorithm.io/health
```

## Managed Containers

Arcane can monitor and control all containers on the server:

### Archon Stack
- archon-server (API server)
- archon-ui (Frontend)
- archon-mcp (MCP server)

### Supabase Stack
- supabase_db_archon (PostgreSQL)
- supabase_kong_archon (API Gateway)
- supabase_auth_archon (Authentication)
- supabase_rest_archon (PostgREST)
- supabase_storage_archon (File storage)
- supabase_realtime_archon (Realtime)
- supabase_studio_archon (Admin UI)
- And more...

### Arcane
- arcane (self-monitoring)

## Security

### Authentication
- Built-in user authentication
- JWT token-based sessions
- Secure cookie storage
- **IMPORTANT**: Change default password after first login

### Network Security
- Localhost binding (127.0.0.1:3552)
- All external access via Nginx reverse proxy
- Cloudflare SSL termination and DDoS protection
- Rate limiting: 100 req/min per IP

### Data Security
- Encryption key for sensitive data
- JWT secret for token security
- Secure credential storage

### Docker Socket Access
Arcane has full Docker daemon access, allowing it to:
- Monitor all containers
- Start/stop/restart containers
- Execute commands in containers
- Pull images and create containers
- **WARNING**: This is powerful - protect credentials

## Troubleshooting

### Cannot Access Arcane
**Symptoms**: https://arcane.nexorithm.io not reachable

**Solutions**:
```bash
# Check container is running
ssh netzwaechter-prod "docker ps | grep arcane"

# Check if responds locally
ssh netzwaechter-prod "curl http://127.0.0.1:3552"

# Check Nginx logs
ssh netzwaechter-prod "tail -f /var/log/nginx/arcane-error.log"

# Restart Arcane
ssh netzwaechter-prod "cd /opt/arcane && docker compose restart"
```

### 502 Bad Gateway
**Symptoms**: Nginx returns 502 error

**Solutions**:
```bash
# Verify Arcane is running
ssh netzwaechter-prod "docker ps | grep arcane"

# Check Arcane logs
ssh netzwaechter-prod "docker logs arcane --tail 50"

# Restart Arcane
ssh netzwaechter-prod "cd /opt/arcane && docker compose restart"
```

### Rate Limited (429)
**Symptoms**: 429 Too Many Requests

**Solution**: Wait 1 minute. Rate limit is 100 req/min with burst of 30.

### WebSocket Issues
If real-time updates not working, see [ARCANE_WEBSOCKET_FIX.md](./ARCANE_WEBSOCKET_FIX.md).

### Cannot See Containers
**Symptoms**: Arcane shows no containers

**Solutions**:
```bash
# Check Docker socket permissions
ssh netzwaechter-prod "ls -la /var/run/docker.sock"

# Verify socket is mounted
ssh netzwaechter-prod "docker inspect arcane | grep docker.sock"

# Restart Arcane
ssh netzwaechter-prod "cd /opt/arcane && docker compose restart"
```

## File Locations

### On Server
| Path | Purpose |
|------|---------|
| `/opt/arcane/docker-compose.yml` | Container configuration |
| `/etc/nginx/sites-available/arcane` | Nginx proxy config |
| `/var/log/nginx/arcane-access.log` | Access logs |
| `/var/log/nginx/arcane-error.log` | Error logs |
| `arcane-data` (volume) | Persistent data |

## Use Cases

### Monitor Archon Services
- Check if archon-server, archon-ui, archon-mcp are running
- View resource usage
- Check logs for errors

### Restart Services
- Quickly restart any container
- No SSH needed
- View restart logs in real-time

### Troubleshoot Issues
- View container logs from web UI
- Execute diagnostic commands
- Check container health status

### Resource Monitoring
- Monitor CPU and memory usage
- Identify resource bottlenecks
- Track performance over time

## Maintenance

### Update Schedule
| Task | Frequency |
|------|-----------|
| Check logs | Weekly |
| Update image | Monthly |
| Backup data | Weekly |
| Review access logs | Weekly |
| Security audit | Quarterly |

### Backup Arcane Data
```bash
ssh netzwaechter-prod "docker run --rm -v arcane_arcane-data:/data -v /root/backups:/backup alpine tar czf /backup/arcane-data-$(date +%Y%m%d).tar.gz -C /data ."
```

## Comparison with Alternatives

### vs. Portainer
**Arcane Advantages**: Lightweight, simple, fast, modern UI
**Portainer Advantages**: More features, multi-host, RBAC

### vs. Docker CLI
**Arcane Advantages**: Web-based, visual, no SSH needed
**Docker CLI Advantages**: More powerful, scriptable

**Recommendation**: Use both - Arcane for quick tasks, CLI for advanced ops.

## Resources

**Official Documentation**:
- Arcane GitHub: https://github.com/ofkm/arcane

**Internal Documentation**:
- [ARCANE_DEPLOYMENT_COMPLETE.md](./ARCANE_DEPLOYMENT_COMPLETE.md) - Full deployment details
- [ARCANE_CLOUDFLARE_DNS_SETUP.md](./ARCANE_CLOUDFLARE_DNS_SETUP.md) - DNS configuration
- [ARCANE_WEBSOCKET_FIX.md](./ARCANE_WEBSOCKET_FIX.md) - WebSocket troubleshooting
- [../../core/CREDENTIALS.md](../../core/CREDENTIALS.md) - Access credentials

## Known Issues

### Analytics Heartbeat Error
**Error**: `analytics heartbeat failed: request failed with status: 429`
**Impact**: None - telemetry feature
**Solution**: Can be ignored

## Deployment Status

**Deployed**: 2025-10-15
**Status**: Operational
**Version**: Latest (ghcr.io/ofkm/arcane:latest)
