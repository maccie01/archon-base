# Deployment Procedures - Netzwächter Production

Created: 2025-10-14

This document provides comprehensive deployment procedures for the Netzwächter application, including initial deployment, code updates, hotfixes, rollback procedures, and troubleshooting.

---

## Table of Contents

1. [Initial Deployment](#initial-deployment)
2. [Code Deployment Process](#code-deployment-process)
3. [Update and Hotfix Procedures](#update-and-hotfix-procedures)
4. [Rollback Procedure](#rollback-procedure)
5. [Health Checks](#health-checks)
6. [Troubleshooting](#troubleshooting)
7. [Recent Fixes Applied](#recent-fixes-applied)

---

## Initial Deployment

### Overview

The initial deployment sets up the production environment from scratch. This is a one-time process that configures the server, installs dependencies, and deploys the application.

### Prerequisites

- Hetzner server with Ubuntu 22.04/24.04 LTS
- SSH key pair generated (see `SSH_KEY_SETUP.md`)
- Domain name configured and pointing to server IP
- Database password prepared (32+ characters)

### Server Information

```
Server IP: 91.98.156.158
Domain: netzwaechter.nexorithm.io (or your domain)
OS: Ubuntu 24.04.3 LTS
Architecture: ARM64 (aarch64)
Resources: 8 vCPU, 16 GB RAM, 150 GB Disk
```

### 1. Server Setup and Hardening

**Duration**: 30 minutes

```bash
# Connect to server
ssh -i ~/.ssh/netzwaechter_deployment root@91.98.156.158

# Update system packages
apt update && apt upgrade -y

# Create non-root user
adduser netzwaechter
usermod -aG sudo netzwaechter

# Configure firewall
apt install -y ufw
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# Install fail2ban
apt install -y fail2ban
systemctl enable fail2ban
systemctl start fail2ban

# Harden SSH
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/#PermitRootLogin yes/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
systemctl restart sshd

# Enable automatic security updates
apt install -y unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades
```

### 2. Install Dependencies

**Duration**: 30 minutes

```bash
# Install Node.js 20 LTS
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
apt install -y nodejs

# Install pnpm
npm install -g pnpm@10.2.0

# Install PM2
npm install -g pm2

# Install PostgreSQL 16
apt install -y postgresql postgresql-contrib

# Install Nginx
apt install -y nginx

# Install Certbot for SSL
apt install -y certbot python3-certbot-nginx

# Verify installations
node --version    # Should show v20.x.x
pnpm --version    # Should show 10.2.0
pm2 --version     # Should show latest
psql --version    # Should show 16.x
nginx -v          # Should show latest
certbot --version # Should show latest
```

### 3. Configure PostgreSQL

**Duration**: 15 minutes

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE netzwaechter;
CREATE USER netzwaechter_user WITH PASSWORD 'YOUR_STRONG_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE netzwaechter TO netzwaechter_user;

# Grant schema permissions
\c netzwaechter
GRANT ALL ON SCHEMA public TO netzwaechter_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO netzwaechter_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO netzwaechter_user;

# Exit psql
\q

# Test connection
psql -U netzwaechter_user -d netzwaechter -h localhost -W
```

### 4. Deploy Application

**Duration**: 30 minutes

```bash
# Create application directory
mkdir -p /opt/netzwaechter
cd /opt/netzwaechter

# Clone repository
git clone https://github.com/maccie01/monitoring_portal.git .

# Install dependencies
pnpm install

# Create .env file
cat > .env << 'EOF'
# Database
DATABASE_URL=postgresql://netzwaechter_user:YOUR_PASSWORD@localhost:5432/netzwaechter

# Server
NODE_ENV=production
PORT=3000

# Session (generate with: openssl rand -hex 32)
SESSION_SECRET=YOUR_GENERATED_32_CHAR_HEX

# CORS
ALLOWED_ORIGIN=https://netzwaechter.nexorithm.io

# Optional: Email configuration
# SMTP_HOST=
# SMTP_PORT=587
# SMTP_USER=
# SMTP_PASS=
EOF

# Set proper permissions
chmod 600 .env

# Run database migrations
pnpm run db:push

# Build application
pnpm run build:packages
pnpm run build:frontend
pnpm run build:backend
```

### 5. Configure PM2

**Duration**: 15 minutes

```bash
# Start application with PM2
cd /opt/netzwaechter
pm2 start dist/index.js --name netzwaechter --env production

# Save PM2 configuration
pm2 save

# Configure PM2 to start on boot
pm2 startup systemd
# Follow the command output and run the suggested command

# Verify application is running
pm2 status
pm2 logs netzwaechter --lines 50
```

### 6. Configure Nginx

**Duration**: 20 minutes

```bash
# Create Nginx configuration
cat > /etc/nginx/sites-available/netzwaechter << 'EOF'
server {
    listen 80;
    server_name netzwaechter.nexorithm.io;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Proxy to Node.js application
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Static files
    location /assets {
        alias /opt/netzwaechter/apps/frontend-web/dist/assets;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable site
ln -s /etc/nginx/sites-available/netzwaechter /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test configuration
nginx -t

# Restart Nginx
systemctl restart nginx
```

### 7. Configure SSL/TLS

**Duration**: 10 minutes

```bash
# Obtain SSL certificate
certbot --nginx -d netzwaechter.nexorithm.io

# Certificate will auto-renew via cron
# Test renewal
certbot renew --dry-run

# Verify HTTPS works
curl -I https://netzwaechter.nexorithm.io
```

### 8. Configure Backups

**Duration**: 10 minutes

```bash
# Create backup directory
mkdir -p /backups/postgres

# Create backup script
cat > /opt/netzwaechter/scripts/backup-db.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/netzwaechter_$TIMESTAMP.sql"

# Create backup
pg_dump -U netzwaechter_user -h localhost netzwaechter > "$BACKUP_FILE"

# Compress backup
gzip "$BACKUP_FILE"

# Delete backups older than 30 days
find "$BACKUP_DIR" -name "netzwaechter_*.sql.gz" -mtime +30 -delete

echo "Backup completed: ${BACKUP_FILE}.gz"
EOF

chmod +x /opt/netzwaechter/scripts/backup-db.sh

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/netzwaechter/scripts/backup-db.sh") | crontab -
```

---

## Code Deployment Process

### Git Repository

**Repository**: https://github.com/maccie01/monitoring_portal.git
**Branch**: main (production)
**Location**: /opt/netzwaechter

### Standard Deployment Flow

```
Developer pushes to GitHub
    ↓
SSH to production server
    ↓
Pull latest code
    ↓
Install dependencies (if changed)
    ↓
Run database migrations (if any)
    ↓
Build application
    ↓
Restart PM2
    ↓
Verify deployment
```

### Full Deployment Command Sequence

```bash
# 1. Connect to server
ssh -i ~/.ssh/netzwaechter_deployment root@91.98.156.158

# 2. Navigate to application directory
cd /opt/netzwaechter

# 3. Create database backup (IMPORTANT)
pg_dump -U netzwaechter_user -h localhost netzwaechter > /backups/postgres/pre_deploy_$(date +%Y%m%d_%H%M%S).sql

# 4. Save current git commit (for rollback)
git rev-parse HEAD > /tmp/last_deploy.txt

# 5. Pull latest code
git pull origin main

# 6. Install dependencies (if package.json changed)
pnpm install

# 7. Run database migrations (if schema changed)
pnpm run db:push

# 8. Build packages
pnpm run build:packages

# 9. Build frontend
pnpm run build:frontend

# 10. Build backend
pnpm run build:backend

# 11. Restart application
pm2 restart netzwaechter

# 12. Verify deployment
pm2 logs netzwaechter --lines 50
pm2 status

# 13. Test application
curl https://netzwaechter.nexorithm.io/api/health
```

### Build Commands Explained

```bash
# Build all packages (shared libraries)
pnpm run build:packages
# Uses: turbo run build
# Builds: @netzwaechter/database, @netzwaechter/shared, etc.

# Build frontend
pnpm run build:frontend
# Uses: vite build
# Output: apps/frontend-web/dist/
# Contains: HTML, CSS, JS, assets

# Build backend
pnpm run build:backend
# Uses: esbuild apps/backend-api/index.ts --platform=node --packages=external --bundle --format=esm --outdir=dist
# Output: dist/index.js
# Single bundled file for Node.js execution
```

---

## Update and Hotfix Procedures

### Backend Code Updates

When only backend code changes (no dependencies or schema changes):

```bash
# 1. SSH to server
ssh -i ~/.ssh/netzwaechter_deployment root@91.98.156.158

# 2. Navigate to app directory
cd /opt/netzwaechter

# 3. Pull latest code
git pull origin main

# 4. Rebuild backend bundle (CRITICAL STEP)
pnpm run build:backend
# Or manually:
# npx esbuild apps/backend-api/index.ts --platform=node --packages=external --bundle --format=esm --outdir=dist

# 5. Restart PM2
pm2 restart netzwaechter

# 6. Verify
pm2 logs netzwaechter --lines 30
curl https://netzwaechter.nexorithm.io/api/health
```

**Important**: Backend changes MUST be bundled with esbuild. The `dist/index.js` file is what PM2 runs, not the source files.

### Alternative: Rsync Backend Files

For rapid hotfixes without full git pull:

```bash
# From local machine
rsync -avz --exclude='node_modules' \
  apps/backend-api/ \
  root@91.98.156.158:/opt/netzwaechter/apps/backend-api/

# On server
ssh -i ~/.ssh/netzwaechter_deployment root@91.98.156.158
cd /opt/netzwaechter
pnpm run build:backend
pm2 restart netzwaechter
```

### Frontend Code Updates

When only frontend code changes:

```bash
# Option A: Build on server (slower)
ssh -i ~/.ssh/netzwaechter_deployment root@91.98.156.158
cd /opt/netzwaechter
git pull origin main
pnpm run build:frontend
# No restart needed - static files

# Option B: Build locally and sync (faster)
# On local machine
cd /Users/janschubert/code-projects/monitoring_firma/netzwaechter-refactored
pnpm run build:frontend

# Sync dist folder to server
rsync -avz apps/frontend-web/dist/ \
  root@91.98.156.158:/opt/netzwaechter/apps/frontend-web/dist/

# No restart needed - Nginx serves static files
```

### Full Stack Updates

When both frontend and backend change:

```bash
ssh -i ~/.ssh/netzwaechter_deployment root@91.98.156.158
cd /opt/netzwaechter

# Backup database
pg_dump -U netzwaechter_user -h localhost netzwaechter > /backups/postgres/backup_$(date +%Y%m%d_%H%M%S).sql

# Pull code
git pull origin main

# Install new dependencies (if any)
pnpm install

# Run migrations (if any)
pnpm run db:push

# Build everything
pnpm run build:packages
pnpm run build:frontend
pnpm run build:backend

# Restart
pm2 restart netzwaechter

# Verify
pm2 logs netzwaechter --lines 50
curl https://netzwaechter.nexorithm.io/api/health
```

### Database Schema Updates

When database schema changes:

```bash
ssh -i ~/.ssh/netzwaechter_deployment root@91.98.156.158
cd /opt/netzwaechter

# IMPORTANT: Backup database first
pg_dump -U netzwaechter_user -h localhost netzwaechter > /backups/postgres/pre_migration_$(date +%Y%m%d_%H%M%S).sql

# Pull code with schema changes
git pull origin main

# Install dependencies
pnpm install

# Review migration (if using drizzle-kit migrate)
# pnpm run db:migrate --dry-run

# Apply migration
pnpm run db:push

# Rebuild and restart
pnpm run build:packages
pnpm run build:backend
pm2 restart netzwaechter

# Verify database
psql -U netzwaechter_user -d netzwaechter -h localhost
# Check tables, verify data
```

### Emergency Hotfix Procedure

For critical production issues requiring immediate fix:

```bash
# 1. Create emergency branch locally
git checkout -b hotfix/critical-issue
# Make fix
git add .
git commit -m "hotfix: describe critical fix"
git push origin hotfix/critical-issue

# 2. SSH to server
ssh -i ~/.ssh/netzwaechter_deployment root@91.98.156.158
cd /opt/netzwaechter

# 3. Backup current state
git rev-parse HEAD > /tmp/pre_hotfix_$(date +%Y%m%d_%H%M%S).txt
pg_dump -U netzwaechter_user -h localhost netzwaechter > /backups/postgres/pre_hotfix_$(date +%Y%m%d_%H%M%S).sql

# 4. Fetch and checkout hotfix
git fetch origin
git checkout hotfix/critical-issue

# 5. Build and deploy
pnpm run build:backend  # or build:frontend depending on fix
pm2 restart netzwaechter

# 6. Verify fix
pm2 logs netzwaechter --lines 50
curl https://netzwaechter.nexorithm.io/api/health

# 7. Merge hotfix to main when verified
git checkout main
git merge hotfix/critical-issue
git push origin main
```

---

## Rollback Procedure

### Quick Rollback to Previous Git Commit

```bash
# 1. SSH to server
ssh -i ~/.ssh/netzwaechter_deployment root@91.98.156.158
cd /opt/netzwaechter

# 2. Stop application
pm2 stop netzwaechter

# 3. Get previous commit hash
cat /tmp/last_deploy.txt
# Or check git log
git log --oneline -10

# 4. Checkout previous version
git checkout PREVIOUS_COMMIT_HASH

# 5. Rebuild (if needed)
pnpm run build:backend  # or full build if major changes

# 6. Restart
pm2 restart netzwaechter

# 7. Verify
pm2 logs netzwaechter --lines 50
curl https://netzwaechter.nexorithm.io/api/health
```

### Database Rollback

If migration needs to be rolled back:

```bash
# 1. Stop application
pm2 stop netzwaechter

# 2. Restore database from backup
psql -U netzwaechter_user -d netzwaechter -h localhost < /backups/postgres/BACKUP_FILE.sql

# 3. Verify database restored
psql -U netzwaechter_user -d netzwaechter -h localhost
\dt  # List tables
SELECT COUNT(*) FROM users;  # Verify data

# 4. Checkout matching code version
git checkout MATCHING_COMMIT_HASH

# 5. Rebuild and restart
pnpm run build:backend
pm2 restart netzwaechter
```

### Full Server Rollback (Hetzner Snapshot)

If complete rollback needed:

```bash
# 1. Access Hetzner Cloud Console
# https://console.hetzner.cloud/

# 2. Navigate to your server
# Select "Netzwächter Production Server"

# 3. Go to "Snapshots" tab

# 4. Select snapshot before deployment
# Click "Restore"

# 5. Confirm and wait for restore (5-10 minutes)

# 6. Reconnect and verify
ssh -i ~/.ssh/netzwaechter_deployment root@91.98.156.158
pm2 status
curl https://netzwaechter.nexorithm.io/api/health
```

### Rollback Decision Matrix

| Scenario | Rollback Method | Time | Data Loss |
|----------|----------------|------|-----------|
| Backend bug, no DB changes | Git checkout previous commit | 2 min | None |
| Frontend bug | Git checkout + rebuild frontend | 3 min | None |
| Bad migration, no user data affected | DB restore + git checkout | 5 min | Since backup |
| Critical system failure | Hetzner snapshot restore | 10 min | Since snapshot |

---

## Health Checks

### Application Health Endpoint

```bash
# Primary health check
curl https://netzwaechter.nexorithm.io/api/health

# Expected response:
{
  "status": "ok",
  "timestamp": "2025-10-14T10:30:00.000Z"
}
```

### PM2 Status Check

```bash
# Check PM2 process status
pm2 status

# Expected output:
┌─────┬────────────────┬─────────────┬─────────┬─────────┬──────────┐
│ id  │ name           │ mode        │ ↺       │ status  │ cpu      │
├─────┼────────────────┼─────────────┼─────────┼─────────┼──────────┤
│ 0   │ netzwaechter   │ fork        │ 0       │ online  │ 0%       │
└─────┴────────────────┴─────────────┴─────────┴─────────┴──────────┘

# View real-time logs
pm2 logs netzwaechter

# View last 100 lines
pm2 logs netzwaechter --lines 100

# Monitor resources
pm2 monit
```

### Database Connection Test

```bash
# Test PostgreSQL connection
psql -U netzwaechter_user -d netzwaechter -h localhost -c "SELECT 1;"

# Check active connections
psql -U netzwaechter_user -d netzwaechter -h localhost -c "SELECT count(*) FROM pg_stat_activity;"

# Check database size
psql -U netzwaechter_user -d netzwaechter -h localhost -c "SELECT pg_size_pretty(pg_database_size('netzwaechter'));"
```

### Nginx Status Check

```bash
# Check Nginx status
systemctl status nginx

# Test configuration
nginx -t

# Check access logs for errors
tail -f /var/log/nginx/access.log

# Check error logs
tail -f /var/log/nginx/error.log
```

### SSL Certificate Check

```bash
# Check certificate expiry
certbot certificates

# Expected output shows:
# - Certificate Name
# - Domains
# - Expiry Date (should be > 60 days)
# - Certificate Path

# Test SSL with curl
curl -vI https://netzwaechter.nexorithm.io 2>&1 | grep "expire"
```

### System Resource Check

```bash
# CPU and memory usage
htop

# Or use simple commands:
top -bn1 | head -20

# Disk usage
df -h

# Check application directory size
du -sh /opt/netzwaechter

# Memory usage
free -h

# Network connections
netstat -tuln | grep -E ':(3000|5432|80|443)'
```

### Comprehensive Health Check Script

Create `/opt/netzwaechter/scripts/health-check.sh`:

```bash
#!/bin/bash

echo "=== Netzwächter Health Check ==="
echo "Time: $(date)"
echo ""

echo "--- PM2 Status ---"
pm2 status

echo ""
echo "--- Application Health ---"
curl -s https://netzwaechter.nexorithm.io/api/health | jq .

echo ""
echo "--- Database Connection ---"
psql -U netzwaechter_user -d netzwaechter -h localhost -c "SELECT 1;" > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "✓ Database: Connected"
else
  echo "✗ Database: Connection Failed"
fi

echo ""
echo "--- Nginx Status ---"
systemctl is-active nginx > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "✓ Nginx: Running"
else
  echo "✗ Nginx: Not Running"
fi

echo ""
echo "--- SSL Certificate ---"
certbot certificates 2>&1 | grep "Expiry Date"

echo ""
echo "--- Disk Usage ---"
df -h | grep -E '(Filesystem|/dev/sda|/dev/vda)'

echo ""
echo "--- Memory Usage ---"
free -h | grep -E '(total|Mem)'

echo ""
echo "=== Health Check Complete ==="
```

Make executable: `chmod +x /opt/netzwaechter/scripts/health-check.sh`

Run: `/opt/netzwaechter/scripts/health-check.sh`

---

## Troubleshooting

### Backend Not Responding

**Symptoms**: API returns 502 Bad Gateway or connection refused

**Diagnosis**:
```bash
# Check if PM2 process is running
pm2 status

# Check application logs
pm2 logs netzwaechter --lines 100

# Check if port 3000 is listening
netstat -tuln | grep 3000
```

**Solutions**:

1. **PM2 process crashed**:
```bash
# Check error logs
pm2 logs netzwaechter --err --lines 50

# Restart application
pm2 restart netzwaechter

# If restart fails, delete and recreate
pm2 delete netzwaechter
cd /opt/netzwaechter
pm2 start dist/index.js --name netzwaechter --env production
pm2 save
```

2. **Backend not bundled**:
```bash
# Rebuild backend bundle
cd /opt/netzwaechter
pnpm run build:backend

# Restart PM2
pm2 restart netzwaechter
```

3. **Environment variables missing**:
```bash
# Check .env file exists
ls -la /opt/netzwaechter/.env

# Verify required variables
cat /opt/netzwaechter/.env | grep -E '(DATABASE_URL|NODE_ENV|PORT|SESSION_SECRET)'

# Restart after fixing .env
pm2 restart netzwaechter
```

4. **Port conflict**:
```bash
# Check what's using port 3000
lsof -i :3000

# If another process is using it, kill it or change app port in .env
```

### Database Connection Issues

**Symptoms**: Application logs show database connection errors

**Diagnosis**:
```bash
# Check PostgreSQL is running
systemctl status postgresql

# Check PostgreSQL logs
tail -f /var/log/postgresql/postgresql-16-main.log

# Test connection manually
psql -U netzwaechter_user -d netzwaechter -h localhost
```

**Solutions**:

1. **PostgreSQL not running**:
```bash
# Start PostgreSQL
systemctl start postgresql

# Enable on boot
systemctl enable postgresql

# Restart application
pm2 restart netzwaechter
```

2. **Connection refused**:
```bash
# Check PostgreSQL is listening
netstat -tuln | grep 5432

# Check pg_hba.conf allows local connections
sudo cat /etc/postgresql/16/main/pg_hba.conf | grep local

# Should have line:
# local   all   all   peer
# host    all   all   127.0.0.1/32   md5

# Restart PostgreSQL after changes
systemctl restart postgresql
```

3. **Authentication failed**:
```bash
# Verify database user exists
sudo -u postgres psql -c "\du"

# Reset password if needed
sudo -u postgres psql
ALTER USER netzwaechter_user WITH PASSWORD 'new_password';
\q

# Update .env with new password
nano /opt/netzwaechter/.env
# Update DATABASE_URL

pm2 restart netzwaechter
```

4. **Too many connections**:
```bash
# Check current connections
psql -U netzwaechter_user -d netzwaechter -h localhost -c "SELECT count(*) FROM pg_stat_activity;"

# Check max connections
psql -U netzwaechter_user -d netzwaechter -h localhost -c "SHOW max_connections;"

# Increase if needed
sudo nano /etc/postgresql/16/main/postgresql.conf
# Set: max_connections = 200
sudo systemctl restart postgresql
```

### SSL Certificate Problems

**Symptoms**: HTTPS not working, browser shows certificate error

**Diagnosis**:
```bash
# Check certificate status
certbot certificates

# Check Nginx SSL configuration
cat /etc/nginx/sites-available/netzwaechter | grep ssl

# Test SSL with openssl
openssl s_client -connect netzwaechter.nexorithm.io:443
```

**Solutions**:

1. **Certificate expired**:
```bash
# Renew certificate
certbot renew

# Restart Nginx
systemctl restart nginx
```

2. **Certificate not found**:
```bash
# Re-obtain certificate
certbot --nginx -d netzwaechter.nexorithm.io

# Follow prompts
# Restart Nginx
systemctl restart nginx
```

3. **Auto-renewal not working**:
```bash
# Test renewal
certbot renew --dry-run

# Check cron job
systemctl status certbot.timer

# Enable timer if disabled
systemctl enable certbot.timer
systemctl start certbot.timer
```

### PM2 Restart Issues

**Symptoms**: PM2 restart fails or process keeps restarting

**Diagnosis**:
```bash
# Check PM2 logs
pm2 logs netzwaechter --lines 100 --err

# Check if process is in error state
pm2 status
```

**Solutions**:

1. **Startup error**:
```bash
# Check application logs for errors
pm2 logs netzwaechter --lines 200

# Common issues:
# - Missing dist/index.js: Run pnpm run build:backend
# - Missing .env: Create .env file
# - Port in use: Change PORT in .env or kill conflicting process
```

2. **Process keeps restarting (crash loop)**:
```bash
# Delete and recreate with detailed error logging
pm2 delete netzwaechter
cd /opt/netzwaechter

# Try running directly first to see error
NODE_ENV=production node dist/index.js

# Fix error, then start with PM2
pm2 start dist/index.js --name netzwaechter --env production
pm2 save
```

3. **PM2 not starting on boot**:
```bash
# Reconfigure startup
pm2 unstartup
pm2 startup systemd
# Run the suggested command

# Save PM2 list
pm2 save

# Test reboot
reboot
# After reboot, check PM2
pm2 status
```

### High CPU or Memory Usage

**Symptoms**: Server slow, application unresponsive

**Diagnosis**:
```bash
# Check resource usage
htop

# Check PM2 resource usage
pm2 monit

# Check specific process
ps aux | grep node
```

**Solutions**:

1. **Memory leak**:
```bash
# Restart application
pm2 restart netzwaechter

# Monitor memory over time
watch -n 5 'pm2 info netzwaechter | grep "memory"'

# If leak persists, check application code for memory issues
```

2. **Too many PM2 instances**:
```bash
# Check PM2 processes
pm2 status

# If multiple instances running, delete all and restart
pm2 delete all
cd /opt/netzwaechter
pm2 start dist/index.js --name netzwaechter --env production
pm2 save
```

3. **Database queries slow**:
```bash
# Check slow queries
psql -U netzwaechter_user -d netzwaechter -h localhost
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY duration DESC;

# Consider adding indexes or optimizing queries
```

### Frontend Not Loading

**Symptoms**: Blank page, 404 errors for assets

**Diagnosis**:
```bash
# Check if dist directory exists
ls -la /opt/netzwaechter/apps/frontend-web/dist/

# Check Nginx configuration
cat /etc/nginx/sites-available/netzwaechter

# Check Nginx error logs
tail -f /var/log/nginx/error.log
```

**Solutions**:

1. **Frontend not built**:
```bash
# Build frontend
cd /opt/netzwaechter
pnpm run build:frontend

# Verify dist exists
ls -la apps/frontend-web/dist/
```

2. **Nginx configuration issue**:
```bash
# Test Nginx config
nginx -t

# Check static file location in config
# Should match actual dist directory

# Restart Nginx
systemctl restart nginx
```

3. **Permissions issue**:
```bash
# Fix permissions
cd /opt/netzwaechter
chmod -R 755 apps/frontend-web/dist/
```

---

## Recent Fixes Applied

### Fix 1: Temperature API Endpoint Correction (Oct 14, 2025)

**Issue**: Temperature efficiency API returning 404 errors

**Root Cause**:
- Frontend was calling `/api/energy-data/temperature-efficiency-chart/`
- Backend only had `/api/temperature/efficiency/` endpoint registered

**Fix Applied**:
```typescript
// Changed in: apps/frontend-web/src/features/temperature/api/temperatureApi.ts
const response = await api.get<TemperatureEfficiencyResponse>(
  `/api/temperature/efficiency/`,  // Corrected endpoint
  { params: { object_id: objectId, time_range: backendTimeRange } }
);
```

**Commit**: `0646699`

### Fix 2: Time Range Parameter Mapping (Oct 14, 2025)

**Issue**: Backend returning 500 validation errors for time range parameter

**Root Cause**:
- Frontend sends: `'last-year'`, `'last-365-days'`, `'last-2year'`
- Backend expects: `'2024'`, `'365days'`, `'2023'`
- Parameter format mismatch causing validation failures

**Fix Applied**:
```typescript
// Added in: apps/frontend-web/src/features/temperature/api/temperatureApi.ts
const timeRangeMap: Record<string, string> = {
  'last-year': '2024',
  'last-365-days': '365days',
  'last-2year': '2023',
};

const backendTimeRange = timeRangeMap[timeRange] || timeRange;
```

**Commit**: `0646699`

### Fix 3: Backend Bundle Rebuild Requirement (Oct 14, 2025)

**Issue**: Object offline status showing incorrectly, threshold API changes not reflected

**Root Cause**:
- Backend code changes were made but not bundled with esbuild
- PM2 was running old `dist/index.js` bundle
- New API endpoints and logic not included in running code

**Fix Applied**:
```bash
# On server
cd /opt/netzwaechter
pnpm run build:backend
# Or: npx esbuild apps/backend-api/index.ts --platform=node --packages=external --bundle --format=esm --outdir=dist
pm2 restart netzwaechter
```

**Critical Lesson**:
Backend changes MUST be bundled before PM2 restart. The build step is not optional.

**Updated Deployment Procedure**:
All backend deployments now include explicit rebuild step:
1. Pull/sync code
2. **Build backend bundle** (critical)
3. Restart PM2

---

## Deployment Checklist

Use this quick checklist for deployments:

### Pre-Deployment
- [ ] Database backup created
- [ ] Current git commit saved for rollback
- [ ] Changes tested locally
- [ ] Dependencies updated (if needed)

### Deployment
- [ ] Code pulled/synced to server
- [ ] Dependencies installed (if package.json changed)
- [ ] Database migrations run (if schema changed)
- [ ] Packages built (if shared code changed)
- [ ] Frontend built (if frontend changed)
- [ ] Backend bundled (if backend changed) - **CRITICAL**
- [ ] PM2 restarted

### Post-Deployment
- [ ] PM2 status shows "online"
- [ ] PM2 logs show no errors
- [ ] Health endpoint responds
- [ ] Database queries work
- [ ] Frontend loads correctly
- [ ] Key features tested manually

### Rollback Ready
- [ ] Previous commit hash recorded
- [ ] Database backup accessible
- [ ] Rollback procedure tested (if major change)

---

## Deployment Scripts Reference

### Available Scripts (package.json)

```bash
# Development
pnpm dev              # Start dev servers (frontend + backend)
pnpm dev:frontend     # Start frontend only
pnpm dev:backend      # Start backend only

# Building
pnpm build            # Build everything (packages + frontend + backend)
pnpm build:packages   # Build shared packages
pnpm build:frontend   # Build frontend only
pnpm build:backend    # Build backend only

# Database
pnpm db:push          # Apply database schema changes

# Testing
pnpm test             # Run all tests
pnpm typecheck        # TypeScript type checking
```

### Custom Deployment Scripts

Location: `/opt/netzwaechter/scripts/`

- `deploy.sh` - Automated deployment script
- `backup-db.sh` - Database backup script
- `health-check.sh` - Comprehensive health check

---

## Monitoring and Maintenance

### Daily Tasks
- Check PM2 status: `pm2 status`
- Review application logs: `pm2 logs netzwaechter --lines 100`
- Verify health endpoint: `curl https://netzwaechter.nexorithm.io/api/health`

### Weekly Tasks
- Review system resources: `htop`, `df -h`
- Check database size and performance
- Review Nginx logs for anomalies
- Verify automated backups are running

### Monthly Tasks
- Update system packages: `apt update && apt upgrade`
- Test SSL certificate renewal: `certbot renew --dry-run`
- Review and clean old backups
- Performance optimization review

---

## Emergency Contacts and Resources

### Server Access
- **SSH Key**: `~/.ssh/netzwaechter_deployment`
- **Server IP**: `91.98.156.158`
- **Domain**: `netzwaechter.nexorithm.io`

### Important Locations
- **Application**: `/opt/netzwaechter`
- **Backups**: `/backups/postgres/`
- **Nginx Config**: `/etc/nginx/sites-available/netzwaechter`
- **PM2 Logs**: `~/.pm2/logs/`

### Documentation
- This file: `.deployment/DEPLOYMENT_PROCEDURES.md`
- Initial Setup: `.deployment/HETZNER_SETUP.md`
- SSH Setup: `.deployment/SSH_KEY_SETUP.md`
- Deployment Checklist: `.deployment/DEPLOYMENT_CHECKLIST.md`

---

**Created**: 2025-10-14
**Last Updated**: 2025-10-14
**Status**: Current and Active
**Maintained By**: Development Team
