# Deployment Checklist - Netzwächter Production

Created: 2025-10-14

Use this checklist to track deployment progress.

---

## Pre-Deployment Preparation

### Server Setup
- [x] SSH key pair generated
- [x] Deployment documentation created
- [ ] Server IP obtained: `___________________`
- [ ] Domain name configured: `___________________`
- [ ] DNS A record pointing to server IP

### SSH Access
- [ ] Public key added to server
- [ ] SSH connection tested successfully
- [ ] SSH config file updated (optional)
- [ ] Can connect without password: `ssh netzwaechter-prod`

### Information Gathered
- [ ] Database password chosen (strong, 32+ characters)
- [ ] Session secret will be auto-generated
- [ ] Email SMTP credentials (if needed)
- [ ] Domain SSL/TLS email for Let's Encrypt

---

## Phase 1: Server Hardening (30 minutes)

### System Updates
- [ ] System packages updated: `apt update && apt upgrade -y`
- [ ] Automatic security updates enabled
- [ ] Server rebooted if kernel updated

### User Management
- [ ] Non-root user created: `netzwaechter`
- [ ] User added to sudo group
- [ ] Strong password set for non-root user

### Firewall Configuration
- [ ] UFW installed
- [ ] Port 22 (SSH) allowed
- [ ] Port 80 (HTTP) allowed
- [ ] Port 443 (HTTPS) allowed
- [ ] All other ports blocked by default
- [ ] UFW enabled and active

### SSH Hardening
- [ ] Password authentication disabled
- [ ] Root login with password disabled
- [ ] SSH key authentication only
- [ ] SSH config backed up
- [ ] SSH service restarted

### Intrusion Prevention
- [ ] fail2ban installed
- [ ] fail2ban configured for SSH
- [ ] fail2ban service enabled and running
- [ ] fail2ban status verified

---

## Phase 2: Install Dependencies (30 minutes)

### Node.js Environment
- [ ] Node.js 20 LTS installed
- [ ] npm version verified
- [ ] pnpm installed globally
- [ ] Node.js version confirmed: `node --version`

### Database
- [ ] PostgreSQL 16 installed
- [ ] PostgreSQL service running
- [ ] PostgreSQL port 5432 listening (localhost only)

### Process Manager
- [ ] PM2 installed globally
- [ ] PM2 startup script configured
- [ ] PM2 can start on boot

### Web Server
- [ ] Nginx installed
- [ ] Nginx service running
- [ ] Default config backed up
- [ ] Nginx can restart successfully

### SSL/TLS Tools
- [ ] Certbot installed
- [ ] Certbot Nginx plugin installed
- [ ] Certbot version verified

---

## Phase 3: Database Configuration (15 minutes)

### PostgreSQL Setup
- [ ] Database created: `netzwaechter`
- [ ] Database user created: `netzwaechter_user`
- [ ] Strong password set for database user
- [ ] Privileges granted to user
- [ ] Connection verified

### PostgreSQL Optimization
- [ ] `max_connections` set to 100
- [ ] `shared_buffers` set to 256MB
- [ ] Connection pooling configured
- [ ] PostgreSQL restarted with new config

### Connection Test
- [ ] Can connect as netzwaechter_user
- [ ] Can create tables
- [ ] Can query database
- [ ] Connection string tested

---

## Phase 4: Application Deployment (30 minutes)

### Repository Setup
- [ ] Git installed (if needed)
- [ ] Repository cloned to `/opt/netzwaechter`
- [ ] Correct branch checked out (main/production)
- [ ] Git remote verified

### Dependencies Installation
- [ ] pnpm install completed successfully
- [ ] All dependencies downloaded
- [ ] node_modules directory exists
- [ ] Lockfile present

### Environment Configuration
- [ ] .env file created in project root
- [ ] DATABASE_URL configured
- [ ] NODE_ENV set to "production"
- [ ] PORT set to 3000
- [ ] SESSION_SECRET generated (32-char hex)
- [ ] ALLOWED_ORIGIN configured with domain
- [ ] All required env vars present
- [ ] .env file permissions: 600

### Database Migrations
- [ ] Migration scripts verified
- [ ] Migrations ran successfully
- [ ] Database schema created
- [ ] Initial data seeded (if any)

### Application Build
- [ ] Build command ran successfully
- [ ] dist/ or build/ directory created
- [ ] No build errors
- [ ] Static assets built

---

## Phase 5: Process Management (15 minutes)

### PM2 Configuration
- [ ] ecosystem.config.js exists
- [ ] PM2 config file validated
- [ ] Instance count configured
- [ ] Environment variables set

### Application Start
- [ ] Application started with PM2
- [ ] Process shows "online" status
- [ ] No startup errors in logs
- [ ] Application responds on port 3000

### PM2 Persistence
- [ ] PM2 list saved: `pm2 save`
- [ ] PM2 startup command ran
- [ ] Startup script enabled
- [ ] Verified PM2 starts on reboot

### Health Check
- [ ] Application logs show no errors
- [ ] Can curl localhost:3000
- [ ] Health endpoint responds
- [ ] Database connection successful

---

## Phase 6: Nginx Configuration (20 minutes)

### Nginx Setup
- [ ] Nginx config file created in sites-available
- [ ] Server name set to domain
- [ ] Proxy pass to localhost:3000
- [ ] Proxy headers configured
- [ ] Config syntax validated: `nginx -t`

### Enable Site
- [ ] Symlink created in sites-enabled
- [ ] Default site disabled (if desired)
- [ ] Nginx reloaded successfully
- [ ] Can access via domain (HTTP)

### SSL/TLS Certificate
- [ ] DNS propagation verified
- [ ] Certbot ran for domain
- [ ] Certificate obtained successfully
- [ ] Auto-renewal configured
- [ ] HTTPS redirect enabled
- [ ] SSL certificate verified

### Final Nginx Checks
- [ ] HTTP redirects to HTTPS
- [ ] HTTPS works correctly
- [ ] SSL certificate valid
- [ ] Security headers present

---

## Phase 7: Monitoring & Logging (10 minutes)

### PM2 Monitoring
- [ ] PM2 logs accessible
- [ ] Log rotation configured
- [ ] Can view real-time logs: `pm2 logs`
- [ ] PM2 monitoring works: `pm2 monit`

### System Logs
- [ ] Nginx access logs accessible
- [ ] Nginx error logs accessible
- [ ] PostgreSQL logs accessible
- [ ] System logs reviewed (no errors)

### Health Checks
- [ ] Application responds to health endpoint
- [ ] Database queries successful
- [ ] API endpoints working
- [ ] Frontend loads correctly

---

## Phase 8: Security Verification (15 minutes)

### Firewall
- [ ] Only ports 22, 80, 443 open
- [ ] PostgreSQL not accessible externally
- [ ] Application port not accessible externally
- [ ] UFW status verified

### SSL/TLS
- [ ] SSL certificate valid
- [ ] Certificate expiry date > 60 days
- [ ] TLS 1.2+ enforced
- [ ] Weak ciphers disabled
- [ ] SSL Labs test passed (A rating)

### Application Security
- [ ] Environment secrets not in logs
- [ ] .env file has proper permissions (600)
- [ ] No sensitive data exposed in responses
- [ ] CORS configured correctly
- [ ] Rate limiting works (if configured)

### SSH Security
- [ ] Root login with password disabled
- [ ] SSH key authentication only
- [ ] fail2ban protecting SSH
- [ ] No failed login attempts

---

## Phase 9: Backup Configuration (10 minutes)

### Database Backups
- [ ] Backup script created
- [ ] Backup directory created: `/backups/postgres/`
- [ ] Backup cron job configured
- [ ] First backup ran successfully
- [ ] Backup file verified

### Hetzner Snapshots
- [ ] First snapshot created
- [ ] Snapshot schedule configured (weekly)
- [ ] Snapshot retention set (4 weeks)
- [ ] Snapshot verified in Hetzner console

### Application Backups
- [ ] Git repository is backup (source code)
- [ ] .env file backed up securely (encrypted)
- [ ] Upload directory backed up (if exists)

---

## Phase 10: Final Verification (15 minutes)

### Functionality Testing
- [ ] Homepage loads
- [ ] Can login
- [ ] Can logout
- [ ] Dashboard loads
- [ ] API endpoints respond
- [ ] Database queries work
- [ ] Forms submit correctly
- [ ] No console errors

### Performance Testing
- [ ] Page load time acceptable (< 3 seconds)
- [ ] API response time acceptable (< 500ms)
- [ ] Database queries fast (< 100ms)
- [ ] No memory leaks
- [ ] CPU usage normal

### Browser Testing
- [ ] Works in Chrome
- [ ] Works in Firefox
- [ ] Works in Safari
- [ ] Responsive on mobile
- [ ] No SSL warnings

### Error Testing
- [ ] 404 page works
- [ ] 500 error handled gracefully
- [ ] Invalid login shows error
- [ ] Network errors handled
- [ ] Database errors logged

---

## Post-Deployment Tasks

### Documentation
- [ ] Server IP documented
- [ ] Domain documented
- [ ] Database credentials stored securely
- [ ] Deployment date recorded
- [ ] SSH key backed up

### Monitoring Setup
- [ ] PM2 monitoring configured
- [ ] Log monitoring setup
- [ ] Alert notifications configured (optional)
- [ ] Uptime monitoring (optional)

### Team Access
- [ ] Team members added (if needed)
- [ ] SSH keys added for team
- [ ] Access permissions configured
- [ ] Documentation shared

### Maintenance Schedule
- [ ] Daily tasks documented
- [ ] Weekly tasks documented
- [ ] Monthly tasks documented
- [ ] Quarterly tasks documented

---

## Rollback Plan (If Needed)

### Before Major Changes
- [ ] Create Hetzner snapshot
- [ ] Backup database
- [ ] Note current git commit hash
- [ ] Document current PM2 processes

### If Rollback Needed
- [ ] Stop PM2 processes
- [ ] Restore database backup
- [ ] Checkout previous git commit
- [ ] Restart PM2 processes
- [ ] Verify application works

---

## Success Criteria

### All Green ✅
- [ ] Application accessible via HTTPS
- [ ] No errors in logs
- [ ] All tests passing
- [ ] Performance acceptable
- [ ] Security hardened
- [ ] Backups configured
- [ ] Monitoring active
- [ ] Documentation complete

### Ready for Production
- [ ] Deployment checklist 100% complete
- [ ] All team members notified
- [ ] Support procedures documented
- [ ] Maintenance schedule active

---

## Completion

**Deployment Date**: `___________________`
**Deployed By**: `___________________`
**Time Taken**: `___________________`
**Server IP**: `___________________`
**Domain**: `___________________`

**Status**:
- [ ] In Progress
- [ ] Complete
- [ ] Issues (document below)

**Issues/Notes**:
```
___________________
___________________
___________________
```

---

**Created**: 2025-10-14
**Status**: Ready for deployment
**Estimated Time**: 2-3 hours total
