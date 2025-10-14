# Hetzner Server Setup - Netzwächter Production Deployment

Created: 2025-10-13

## Server Specifications

**Provider**: Hetzner
**Plan**: CX31 (or similar)
**Location**: TBD

### Resources
- **vCPU**: 8 cores
- **RAM**: 16 GB
- **Disk**: 160 GB (local SSD)
- **Traffic**: 20 TB/month included
- **Cost**: 11.99 EUR/month

### Assessment
✅ **Perfect for Netzwächter**
- CPU: 8 vCPU (need 2-4) - 100% headroom
- RAM: 16 GB (need 4-8) - Excellent
- Disk: 160 GB (need 40-60) - Plenty of space
- Traffic: 20 TB (need < 1) - More than sufficient

---

## Server Information

**Operating System**: Ubuntu 22.04 LTS (or 24.04 LTS)

### Server Details
```
Server IP: 91.98.156.158
SSH Port: 22 (default)
Hostname: netzwaechter
Domain Name: TBD
```

**Server Specs (Verified)**:
- OS: Ubuntu 24.04.3 LTS (Noble)
- Architecture: aarch64 (ARM64)
- CPU Cores: 8
- RAM: 16 GB (15 GiB available)
- Disk: 150 GB (143 GB available)
- Swap: 0 (will configure)

### DNS Configuration (TO BE SETUP)
```
A Record:
  netzwaechter.yourdomain.com -> SERVER_IP

OR

Subdomain:
  app.yourdomain.com -> SERVER_IP
```

---

## SSH Key Setup

### Key Information

**Key Name**: `netzwaechter_deployment`
**Key Type**: ED25519 (most secure, modern)
**Purpose**: Claude-assisted deployment and management
**Created**: 2025-10-13

### Key Locations

**Private Key** (KEEP SECRET):
```
/Users/janschubert/.ssh/netzwaechter_deployment
```

**Public Key** (Safe to share):
```
/Users/janschubert/.ssh/netzwaechter_deployment.pub
```

### SSH Config Entry

Add to `~/.ssh/config`:
```
Host netzwaechter-prod
    HostName SERVER_IP_HERE
    User root
    IdentityFile ~/.ssh/netzwaechter_deployment
    Port 22
```

Then connect with: `ssh netzwaechter-prod`

---

## Deployment Strategy

### Phase 1: Initial Setup (1-2 hours)

**Approach**: Direct SSH access by Claude

**Tasks**:
1. ✅ Generate SSH key pair
2. ⏳ Copy public key to server
3. ⏳ Harden server security
4. ⏳ Install dependencies
5. ⏳ Configure database
6. ⏳ Deploy application
7. ⏳ Setup Nginx + SSL
8. ⏳ Configure monitoring

### Phase 2: Application Configuration

**Environment Variables**:
```env
# Database (PostgreSQL 16)
DATABASE_URL=postgresql://netzwaechter_user:PASSWORD@localhost:5432/netzwaechter

# Server
NODE_ENV=production
PORT=3000

# Session
SESSION_SECRET=<generated-32-char-hex>

# CORS
ALLOWED_ORIGIN=https://your-domain.com

# Optional
SMTP_HOST=<email-server>
SMTP_PORT=587
SMTP_USER=<email-user>
SMTP_PASS=<email-password>
```

### Phase 3: SSL/TLS Setup

**Certificate Authority**: Let's Encrypt (via Certbot)
**Auto-renewal**: Yes (certbot renew hook)
**Domains**: TBD

---

## Security Configuration

### Firewall Rules (ufw)
```bash
Port 22   (SSH)     - ALLOW from anywhere
Port 80   (HTTP)    - ALLOW from anywhere (redirect to HTTPS)
Port 443  (HTTPS)   - ALLOW from anywhere
Port 5432 (PostgreSQL) - DENY (localhost only)
Port 3000 (Node.js)    - DENY (localhost only, behind Nginx)
```

### Fail2Ban
- **SSH**: Max 5 attempts, 10 minute ban
- **Nginx**: Rate limiting enabled
- **PostgreSQL**: Connection limits enforced

### User Accounts
```
root - System administration only (SSH key auth only)
netzwaechter - Application user (non-root, limited privileges)
postgres - Database user (system account)
```

### SSH Hardening
```
PasswordAuthentication no
PermitRootLogin prohibit-password
PubkeyAuthentication yes
Port 22 (consider changing to non-standard port)
```

---

## Software Stack

### System Packages
- Ubuntu 22.04/24.04 LTS
- ufw (firewall)
- fail2ban (intrusion prevention)
- unattended-upgrades (automatic security updates)

### Application Runtime
- Node.js 20.x LTS
- pnpm 8.x
- PM2 (process manager)

### Database
- PostgreSQL 16
- Connection pooling: 5-20 connections
- Automatic backups: Daily

### Web Server
- Nginx (reverse proxy)
- Certbot (SSL/TLS)
- HTTP/2 enabled
- Gzip compression

---

## Monitoring & Logging

### PM2 Monitoring
```bash
pm2 status          # Process status
pm2 logs            # View logs
pm2 monit           # Real-time monitoring
pm2 describe app    # Detailed info
```

### PostgreSQL Monitoring
```bash
# Check connections
SELECT count(*) FROM pg_stat_activity;

# Check database size
SELECT pg_size_pretty(pg_database_size('netzwaechter'));

# Check active queries
SELECT * FROM pg_stat_activity WHERE state = 'active';
```

### Nginx Monitoring
```bash
# Access logs
tail -f /var/log/nginx/access.log

# Error logs
tail -f /var/log/nginx/error.log

# Test configuration
nginx -t
```

### System Monitoring
```bash
# CPU and memory
htop

# Disk usage
df -h

# Network
netstat -tuln
```

---

## Backup Strategy

### Database Backups
```bash
# Daily automated backup
pg_dump -U netzwaechter_user netzwaechter > backup_$(date +%Y%m%d).sql

# Retention: 30 days
# Location: /backups/postgres/
```

### Application Backups
```bash
# Git repository (source of truth)
# .env file (encrypted storage)
# uploads/ directory (if any)
```

### Hetzner Snapshots
- **Frequency**: Weekly
- **Retention**: 4 weeks
- **Before**: Major updates

---

## Deployment Workflow

### Initial Deployment
```bash
# 1. Clone repository
git clone REPO_URL /opt/netzwaechter

# 2. Install dependencies
cd /opt/netzwaechter
pnpm install

# 3. Setup environment
cp .env.example .env
# Edit .env with production values

# 4. Run migrations
pnpm run db:migrate

# 5. Build application
pnpm run build

# 6. Start with PM2
pm2 start ecosystem.config.js --name netzwaechter
pm2 save
```

### Update Deployment
```bash
# 1. Pull latest code
cd /opt/netzwaechter
git pull origin main

# 2. Install new dependencies
pnpm install

# 3. Run migrations (if any)
pnpm run db:migrate

# 4. Rebuild
pnpm run build

# 5. Restart application
pm2 restart netzwaechter

# 6. Verify
pm2 logs netzwaechter --lines 50
```

---

## Troubleshooting

### Application Won't Start
```bash
# Check PM2 status
pm2 status

# View logs
pm2 logs netzwaechter --lines 100

# Check environment variables
pm2 env 0

# Restart
pm2 restart netzwaechter
```

### Database Connection Issues
```bash
# Check PostgreSQL is running
systemctl status postgresql

# Check connections
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity;"

# Test connection
psql -U netzwaechter_user -d netzwaechter -h localhost
```

### SSL Certificate Issues
```bash
# Check certificate status
certbot certificates

# Renew manually
certbot renew

# Test renewal
certbot renew --dry-run
```

### Nginx Issues
```bash
# Test configuration
nginx -t

# Reload configuration
systemctl reload nginx

# Check status
systemctl status nginx

# View error logs
tail -f /var/log/nginx/error.log
```

---

## Maintenance Tasks

### Daily
- ✅ Monitor PM2 status
- ✅ Check application logs for errors
- ✅ Verify backup completion

### Weekly
- ✅ Review system resource usage (CPU, RAM, Disk)
- ✅ Check PostgreSQL performance
- ✅ Review Nginx access logs for anomalies
- ✅ Create Hetzner snapshot

### Monthly
- ✅ Update system packages: `apt update && apt upgrade`
- ✅ Review security logs (fail2ban, auth.log)
- ✅ Test SSL certificate renewal
- ✅ Clean up old backups
- ✅ Performance optimization review

### Quarterly
- ✅ Security audit
- ✅ Database vacuum and analyze
- ✅ Review and update documentation
- ✅ Test disaster recovery procedure

---

## Emergency Contacts & Procedures

### Rollback Procedure
```bash
# 1. Stop application
pm2 stop netzwaechter

# 2. Checkout previous version
cd /opt/netzwaechter
git checkout PREVIOUS_COMMIT_HASH

# 3. Restore database (if needed)
psql -U netzwaechter_user netzwaechter < backup_YYYYMMDD.sql

# 4. Restart
pm2 restart netzwaechter
```

### Server Recovery
1. Access Hetzner Console
2. Restore from snapshot (if needed)
3. Verify DNS settings
4. Test application functionality

---

## Cost Optimization

### Current Setup
- Server: 11.99 EUR/month
- Domain: ~10 EUR/year
- SSL: Free (Let's Encrypt)
- **Total**: ~13 EUR/month

### Scaling Options
If needed later:
- **More CPU/RAM**: Upgrade Hetzner plan
- **Database**: Separate database server
- **CDN**: Cloudflare (free tier)
- **Load Balancer**: If traffic increases significantly

---

## Next Steps

### Immediate (Today)
1. ✅ Generate SSH key pair
2. ⏳ Add public key to Hetzner server
3. ⏳ Test SSH connection
4. ⏳ Begin server hardening

### Phase 1 (This Week)
5. ⏳ Install all dependencies
6. ⏳ Configure PostgreSQL
7. ⏳ Deploy application
8. ⏳ Setup Nginx + SSL
9. ⏳ Configure monitoring

### Phase 2 (Next Week)
10. ⏳ Setup automated backups
11. ⏳ Configure CI/CD (optional)
12. ⏳ Performance testing
13. ⏳ Documentation completion

---

## Resources & Documentation

### Official Docs
- [Hetzner Cloud Docs](https://docs.hetzner.com/cloud/)
- [Ubuntu Server Guide](https://ubuntu.com/server/docs)
- [PostgreSQL 16 Docs](https://www.postgresql.org/docs/16/)
- [Node.js Deployment](https://nodejs.org/en/docs/guides/nodejs-docker-webapp/)
- [PM2 Documentation](https://pm2.keymetrics.io/docs/usage/quick-start/)
- [Nginx Guide](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/getting-started/)

### Project-Specific
- Project README: `/Users/janschubert/code-projects/monitoring_firma/netzwaechter-refactored/README.md`
- Standards: `/Users/janschubert/code-projects/monitoring_firma/netzwaechter-refactored/.archon-knowledge-base/07-standards/`
- Security: `/Users/janschubert/code-projects/monitoring_firma/netzwaechter-refactored/.archon-knowledge-base/07-standards/SECURITY_PATTERNS.md`

---

**Document Created**: 2025-10-13
**Last Updated**: 2025-10-13
**Status**: In Progress - SSH Key Generation
**Next Action**: Copy public key to server
