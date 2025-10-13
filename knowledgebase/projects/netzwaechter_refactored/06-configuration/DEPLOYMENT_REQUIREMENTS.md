# Deployment Requirements

Production environment requirements and deployment configuration for the Netzwächter project.

Created: 2025-10-13
Last Updated: 2025-10-13

---

## Overview

This document outlines all requirements, configurations, and best practices for deploying Netzwächter to a production environment.

---

## System Requirements

### Server Specifications

#### Minimum Requirements

**Development/Testing:**
- CPU: 2 cores
- RAM: 4 GB
- Disk: 20 GB SSD
- Network: 100 Mbps

**Production (Small):**
- CPU: 4 cores
- RAM: 8 GB
- Disk: 50 GB SSD
- Network: 1 Gbps

**Production (Medium):**
- CPU: 8 cores
- RAM: 16 GB
- Disk: 100 GB SSD
- Network: 1 Gbps

**Production (Large):**
- CPU: 16+ cores
- RAM: 32+ GB
- Disk: 200+ GB SSD
- Network: 10 Gbps

### Software Requirements

#### Operating System

**Supported:**
- Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+)
- Docker containers (Alpine, Ubuntu)
- Cloud platforms (AWS, GCP, Azure, Digital Ocean)

**Not Recommended:**
- Windows Server (use WSL2 or Docker)
- macOS (development only)

#### Runtime

**Node.js:**
- Version: 20.18.2 or higher
- LTS version recommended
- Installation: nvm, package manager, or Docker

**Package Manager:**
- pnpm 10.2.0 (exact version)
- Global installation required

**Verification:**
```bash
node --version  # v20.18.2+
pnpm --version  # 10.2.0
```

---

## Environment Configuration

### Required Environment Variables

**Production .env Template:**
```bash
# ===================================
# PRODUCTION ENVIRONMENT CONFIGURATION
# ===================================

# Environment Mode
NODE_ENV=production

# Server Configuration
PORT=3000

# Database (PostgreSQL via Neon)
DATABASE_URL=postgresql://username:password@host:port/database?sslmode=require

# Session Security (128+ characters, cryptographically random)
SESSION_SECRET=<STRONG_128_CHAR_SECRET>

# Email Service
MAILSERVER_PASSWORD=<STRONG_EMAIL_PASSWORD>

# Connection Pool (Production Settings)
DB_POOL_MIN=5
DB_POOL_MAX=20
DB_POOL_IDLE_TIMEOUT=30000
DB_CONNECTION_TIMEOUT=5000
```

### Security Checklist

**Before Deployment:**
- [ ] NODE_ENV=production
- [ ] Strong SESSION_SECRET (128+ characters)
- [ ] DATABASE_URL uses sslmode=require
- [ ] Strong database password (12+ characters)
- [ ] Strong email password
- [ ] .env file has 600 permissions
- [ ] .env not committed to git
- [ ] All secrets unique per environment
- [ ] No default/placeholder values

---

## Database Requirements

### PostgreSQL Database

**Provider:** Neon (recommended) or self-hosted PostgreSQL

**Neon Requirements:**
- Pro tier recommended for production
- Compute: Scale based on load
- Storage: Minimum 10 GB, scale as needed
- Connections: 20-50 concurrent (adjust pool size)
- Region: Same as application for low latency

**Self-Hosted Requirements:**
- PostgreSQL 15+
- SSL/TLS enabled
- Automated backups
- Point-in-time recovery
- Monitoring setup

**Connection Pool:**
- Min connections: 5
- Max connections: 20 (adjust based on load)
- Idle timeout: 30s
- Connection timeout: 5s

**Database Size Estimates:**
- Small deployment: 1-5 GB
- Medium deployment: 5-20 GB
- Large deployment: 20-100+ GB

### Database Security

**Required:**
- SSL/TLS encryption (sslmode=require)
- Strong passwords (12+ characters)
- Connection from application only
- Regular backups (automated)
- Access logging enabled

**Optional but Recommended:**
- IP whitelisting
- Certificate verification
- Read replicas (for scaling)
- Connection pooling (PgBouncer)

---

## Network & Connectivity

### Ports

| Service | Port | Protocol | Purpose |
|---------|------|----------|---------|
| HTTP | 80 | TCP | Redirect to HTTPS |
| HTTPS | 443 | TCP | Production traffic |
| Backend API | 3000 | TCP | Internal (behind proxy) |
| PostgreSQL | 5432 | TCP | Database (external) |

**Firewall Rules:**
- Allow inbound: 80, 443
- Deny direct access: 3000 (use reverse proxy)
- Allow outbound: 443, 5432 (database)
- Deny all other inbound

### Domain & DNS

**Requirements:**
- Domain name (e.g., monitoring.example.com)
- DNS A record pointing to server IP
- SSL certificate (Let's Encrypt recommended)

**Example DNS:**
```
monitoring.example.com.  IN  A  <SERVER_IP>
```

### Reverse Proxy

**Recommended:** Nginx or Caddy

**Purpose:**
- SSL/TLS termination
- Static file serving
- API proxy to backend
- Load balancing (if multiple instances)
- Security headers
- Rate limiting

**Nginx Configuration Example:**
```nginx
server {
    listen 443 ssl http2;
    server_name monitoring.example.com;

    ssl_certificate /etc/letsencrypt/live/monitoring.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/monitoring.example.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    # Static files (frontend)
    location / {
        root /var/www/netzwaechter/dist/public;
        try_files $uri $uri/ /index.html;
    }

    # API proxy
    location /api {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name monitoring.example.com;
    return 301 https://$server_name$request_uri;
}
```

---

## SSL/TLS Requirements

### Certificate

**Options:**
1. **Let's Encrypt (Free):**
   - Automated renewal
   - Trusted by all browsers
   - Easy setup with certbot

2. **Commercial Certificate:**
   - Extended validation
   - Wildcard support
   - Organization validation

**Installation (Let's Encrypt):**
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d monitoring.example.com

# Auto-renewal (already configured by certbot)
sudo systemctl status certbot.timer
```

### SSL Configuration

**Minimum TLS Version:** 1.2
**Recommended:** 1.3

**Strong Cipher Suites:**
```
TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
TLS_DHE_RSA_WITH_AES_256_GCM_SHA384
```

**Nginx SSL Config:**
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
```

---

## Application Deployment

### Build Process

**1. Prepare Environment:**
```bash
export NODE_ENV=production
```

**2. Install Dependencies:**
```bash
pnpm install --prod --frozen-lockfile
```

**3. Build Application:**
```bash
pnpm run build
```

**4. Verify Build:**
```bash
ls -la dist/
# Should contain:
# - index.js (backend bundle)
# - public/ (frontend build)
```

### Deployment Methods

#### Method 1: Direct Deployment

**Steps:**
1. Build on CI/CD or locally
2. Copy `dist/` to server
3. Copy `node_modules/` to server
4. Copy `.env` to server
5. Start application

**Directory Structure:**
```
/var/www/netzwaechter/
├── dist/
│   ├── index.js
│   └── public/
├── node_modules/
├── .env
└── package.json
```

**Start Command:**
```bash
NODE_ENV=production node dist/index.js
```

#### Method 2: Docker Deployment

**Dockerfile:**
```dockerfile
# See config/docker/Dockerfile.backend
# See config/docker/Dockerfile.frontend
```

**Docker Compose:**
```yaml
# See config/docker/docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./config/docker/Dockerfile.backend
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - SESSION_SECRET=${SESSION_SECRET}
    ports:
      - "3000:3000"

  frontend:
    build: ./config/docker/Dockerfile.frontend
    ports:
      - "80:80"
```

**Deploy:**
```bash
docker-compose -f config/docker/docker-compose.yml up -d
```

#### Method 3: PM2 Process Manager

**Install PM2:**
```bash
npm install -g pm2
```

**PM2 Ecosystem File:**
```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'netzwaechter',
    script: 'dist/index.js',
    instances: 2,
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    }
  }]
};
```

**Start:**
```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

---

## Process Management

### Systemd Service

**Service File:** `/etc/systemd/system/netzwaechter.service`

```ini
[Unit]
Description=Netzwächter Monitoring Portal
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/netzwaechter
EnvironmentFile=/var/www/netzwaechter/.env
ExecStart=/usr/bin/node dist/index.js
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Commands:**
```bash
sudo systemctl enable netzwaechter
sudo systemctl start netzwaechter
sudo systemctl status netzwaechter
sudo systemctl restart netzwaechter
```

---

## Monitoring & Logging

### Application Logs

**Log Locations:**
- Application logs: `/var/log/netzwaechter/app.log`
- Error logs: `/var/log/netzwaechter/error.log`
- Access logs: `/var/log/nginx/access.log`
- Error logs: `/var/log/nginx/error.log`

**Log Rotation:**
```bash
# /etc/logrotate.d/netzwaechter
/var/log/netzwaechter/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0644 www-data www-data
}
```

### Health Checks

**Endpoint:** `/api/health`

**Check Script:**
```bash
#!/bin/bash
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/health)
if [ "$response" != "200" ]; then
    echo "Health check failed: $response"
    exit 1
fi
```

**Monitoring Tools:**
- Uptime monitoring (UptimeRobot, Pingdom)
- Application monitoring (New Relic, DataDog)
- Server monitoring (Prometheus, Grafana)
- Error tracking (Sentry)

### Metrics

**Track:**
- Response times
- Error rates
- Database connection pool stats
- Memory usage
- CPU usage
- Disk usage
- Active users

---

## Backup Strategy

### Database Backups

**Automated (Neon):**
- Point-in-time recovery
- Automatic snapshots
- Retention: 7-30 days (plan dependent)

**Manual Backups:**
```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_$DATE.sql"

pg_dump $DATABASE_URL > /backups/$BACKUP_FILE
gzip /backups/$BACKUP_FILE

# Keep last 30 days
find /backups -type f -mtime +30 -delete
```

**Backup Schedule:**
- Daily: Keep 30 days
- Weekly: Keep 12 weeks
- Monthly: Keep 12 months

### Application Backups

**Files to Backup:**
- `.env` file (encrypted storage)
- Configuration files
- Uploaded files (if any)
- Database settings

**Not to Backup:**
- `node_modules/` (reproducible)
- `dist/` (build artifacts)
- Log files (archived separately)

---

## Scaling Considerations

### Horizontal Scaling

**Load Balancer:**
- Nginx, HAProxy, or cloud load balancer
- Session affinity or shared session store
- Health checks for instances

**Multiple Instances:**
```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      replicas: 3
```

**Session Storage:**
- Use PostgreSQL (current setup)
- Or Redis for better performance

### Vertical Scaling

**When to Scale:**
- CPU usage > 70% sustained
- Memory usage > 80%
- Response times increasing
- Database connections maxed

**How to Scale:**
1. Increase server resources
2. Optimize database queries
3. Add caching layer (Redis)
4. Optimize frontend bundle
5. Use CDN for static assets

---

## Security Hardening

### Server Security

**Operating System:**
- Keep system updated
- Disable root SSH login
- Use SSH keys (no passwords)
- Configure firewall (ufw, iptables)
- Install fail2ban (brute force protection)

**Application Security:**
- Run as non-root user
- Use environment variables (no hardcoded secrets)
- Enable rate limiting
- Implement CORS properly
- Use security headers

**Security Headers:**
```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
```

### Regular Updates

**Schedule:**
- Security patches: Immediately
- Minor updates: Monthly
- Major updates: Quarterly (with testing)

**Update Process:**
1. Test in staging environment
2. Backup production
3. Schedule maintenance window
4. Apply updates
5. Verify functionality
6. Monitor for issues

---

## Deployment Checklist

### Pre-Deployment

**Infrastructure:**
- [ ] Server provisioned (CPU, RAM, disk)
- [ ] Operating system installed & updated
- [ ] Node.js 20+ installed
- [ ] pnpm 10.2.0 installed
- [ ] Firewall configured
- [ ] Domain DNS configured
- [ ] SSL certificate installed

**Database:**
- [ ] PostgreSQL database created
- [ ] Connection string obtained
- [ ] SSL enabled
- [ ] Backups configured
- [ ] Monitoring enabled

**Application:**
- [ ] Code repository accessible
- [ ] .env file created (production values)
- [ ] All secrets generated (strong)
- [ ] Environment variables validated
- [ ] File permissions set (chmod 600 .env)

### Deployment

**Build:**
- [ ] Dependencies installed (pnpm install)
- [ ] Application built (pnpm run build)
- [ ] Build artifacts verified (dist/)
- [ ] No build errors

**Deploy:**
- [ ] Application files copied to server
- [ ] Process manager configured (PM2/systemd)
- [ ] Application started
- [ ] Health check passes
- [ ] Logs show no errors

**Proxy:**
- [ ] Reverse proxy configured (Nginx)
- [ ] SSL termination working
- [ ] Static files served
- [ ] API proxy working
- [ ] Security headers set

### Post-Deployment

**Verification:**
- [ ] Application accessible via HTTPS
- [ ] Login working
- [ ] Database queries working
- [ ] API endpoints responding
- [ ] Frontend loading correctly
- [ ] No console errors
- [ ] SSL certificate valid

**Monitoring:**
- [ ] Health checks configured
- [ ] Uptime monitoring enabled
- [ ] Log rotation configured
- [ ] Backup jobs scheduled
- [ ] Alerts configured

**Documentation:**
- [ ] Deployment documented
- [ ] Access credentials stored securely
- [ ] Runbook created
- [ ] Emergency contacts listed

---

## Rollback Procedure

### Quick Rollback

**If Deployment Fails:**

1. **Stop New Version:**
```bash
pm2 stop netzwaechter
# or
sudo systemctl stop netzwaechter
```

2. **Restore Previous Version:**
```bash
cd /var/www/netzwaechter
rm -rf dist
cp -r dist.backup dist
```

3. **Restart:**
```bash
pm2 start netzwaechter
# or
sudo systemctl start netzwaechter
```

4. **Verify:**
```bash
curl http://localhost:3000/api/health
```

### Database Rollback

**If Migration Fails:**

1. **Restore from backup:**
```bash
psql $DATABASE_URL < backup_latest.sql
```

2. **Or use Neon point-in-time recovery**

---

## References

### Internal Documentation
- `.env.example` - Environment template
- `config/docker/` - Docker configurations
- `CONFIGURATION_OVERVIEW.md` - Project structure
- `ENVIRONMENT_VARIABLES.md` - Environment vars

### External Resources
- [Node.js Deployment](https://nodejs.org/en/docs/guides/simple-profiling/)
- [PM2 Documentation](https://pm2.keymetrics.io/docs/)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/docs/)
- [Neon Documentation](https://neon.tech/docs)
