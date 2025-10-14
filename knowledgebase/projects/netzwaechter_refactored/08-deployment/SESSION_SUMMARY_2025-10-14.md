# Netzwächter Deployment & Bug Fix Session

**Date**: October 14, 2025
**Server**: https://netzwaechter.nexorithm.io (91.98.156.158)
**Status**: Production Deployment Successful & Critical Bugs Fixed

---

## Overview

This session accomplished a complete production deployment of the Netzwächter monitoring application and resolved critical bugs that were preventing the application from functioning correctly.

---

## 1. Initial Deployment

### Server Setup
- **Provider**: Hetzner Cloud
- **Specifications**: 8 vCPU, 16 GB RAM, 160 GB Disk
- **OS**: Ubuntu 24.04.3 LTS (ARM64)
- **IP Address**: 91.98.156.158
- **Domain**: netzwaechter.nexorithm.io

### Components Installed
- Node.js 20.19.5
- PostgreSQL client tools
- Nginx (reverse proxy and static file server)
- PM2 (process manager, cluster mode with 2 instances)
- Certbot (Let's Encrypt SSL/TLS)
- UFW Firewall + fail2ban

### Security Measures
- SSH key-based authentication only (password auth disabled)
- UFW firewall configured (ports 22, 80, 443 open)
- fail2ban active with SSH jail (3 malicious IPs banned)
- Let's Encrypt SSL certificate with automatic renewal
- Nginx security headers configured

---

## 2. Critical Bugs Identified & Fixed

### Bug #1: Temperature API 404 Errors

**Symptom**: All temperature efficiency chart requests returning 404

**Root Cause**: Frontend calling wrong API endpoint
- Frontend: `/api/energy-data/temperature-efficiency-chart/{objectId}`
- Backend: `/api/temperature/efficiency/{objectId}`

**Fix Applied**:
- Updated `apps/frontend-web/src/features/temperature/api/temperatureApi.ts` line 76
- Changed endpoint to match backend route

**File Modified**:
```typescript
// apps/frontend-web/src/features/temperature/api/temperatureApi.ts:76
return apiClient.get(`/api/temperature/efficiency/${objectId}`, {
  timeRange: timeRangeMap[timeRange]
});
```

---

### Bug #2: Time Range Parameter Validation Errors

**Symptom**: API returning 500 errors with message:
```
Invalid time range for efficiency. Must be one of: last30days, 365days, 2023, 2024, 2025
```

**Root Cause**: Frontend/backend parameter mismatch
- Frontend sends: `'last-year'`, `'last-365-days'`, `'last-2year'`
- Backend expects: `'2024'`, `'365days'`, `'2023'`

**Fix Applied**:
- Added time range mapping in `temperatureApi.ts` lines 70-74

```typescript
const timeRangeMap = {
  'last-year': '2024',
  'last-365-days': '365days',
  'last-2year': '2023'
};
```

---

### Bug #3: All Objects Showing as Offline (CRITICAL)

**Symptom**: All 25 objects displayed as "Offline" in the UI despite having valid recent temperature data

**Root Cause**: `/api/settings/thresholds` endpoint returning incorrect data format
- **Expected**: Array of threshold configuration objects with `keyName: 'netzwaechter_0'`
- **Actual**: Single object `{"warning":25,"critical":30,"unit":"°C"}`

**Investigation Process**:
1. Checked frontend offline detection logic in `Maps.tsx` lines 226-274
2. Discovered frontend expects `Array.isArray(thresholds)` with items containing `keyName` property
3. When format check fails at line 227, function returns `{status: 'offline'}` for ALL objects
4. Verified database had correct threshold data with `netzwaechter_0`, `netzwaechter_1`, `netzwaechter_2`
5. Realized running backend was outdated (PM2 running old bundle)

**Fix Applied**:
1. Synced updated backend source to server:
   ```bash
   rsync -avz apps/backend-api/ netzwaechter-prod:/opt/netzwaechter-backend-source/
   ```

2. Copied updated modules to deployment location:
   ```bash
   ssh netzwaechter-prod 'cp -r /opt/netzwaechter-backend-source/modules/ /opt/netzwaechter/apps/backend-api/'
   ```

3. **Critical Step**: Rebuilt backend bundle (PM2 runs bundled code, not source):
   ```bash
   ssh netzwaechter-prod 'cd /opt/netzwaechter && npx esbuild apps/backend-api/index.ts --platform=node --packages=external --bundle --format=esm --outdir=dist'
   ```

4. Restarted PM2:
   ```bash
   ssh netzwaechter-prod 'pm2 restart all'
   ```

**Verification**: API now returns correct array format:
```json
[
  {
    "id": 142,
    "category": "thresholds",
    "key_name": "netzwaechter_0",
    "keyName": "netzwaechter_0",
    "value": {
      "label": "Global",
      "thresholds": {
        "normal": {"vlValue": 55, "rlValue": 45},
        "warning": {"vlValue": 53, "rlValue": 52},
        "critical": {"vlValue": 49, "rlValue": 56}
      }
    }
  }
]
```

---

## 3. Results After Fixes

### Object Status Distribution
- **Critical**: 3 objects (temperature thresholds violated)
  - Garkenburgstr 52 (207315002)
  - Grimmstr. 2 (207315013)
  - Röntgenstr. 9 (272605197)
- **Warning**: 1 object (approaching thresholds)
  - Guts-Muths-Straße 10 (272605178)
- **Normal**: 15 objects (operating within parameters)
- **Offline**: 6 objects (no recent temperature data)

### Verified Working Features
- Temperature efficiency API returning valid data
- Object classification based on temperature thresholds
- Real-time temperature monitoring
- Critical/warning alerts functioning
- Netzwächter dashboard displaying correct statistics
- Objekt Monitor showing proper object statuses

---

## 4. Documentation Created

Created comprehensive production documentation using parallel task agents:

### `.deployment/SERVER_INFRASTRUCTURE.md` (13 KB)
- Complete server specifications and configuration
- Network setup (firewall, ports, SSL/TLS)
- Nginx reverse proxy configuration
- Security measures (SSH, fail2ban, UFW)
- Maintenance procedures
- System monitoring and health checks

### `.deployment/APPLICATION_ARCHITECTURE.md` (20 KB, 790 lines)
- Application structure at `/opt/netzwaechter/`
- Backend architecture (Node.js/Express, PM2 cluster)
- Frontend architecture (React/Vite build)
- Database configuration (PostgreSQL Neon)
- Process management (PM2)
- Build process and deployment
- Architecture diagrams (Mermaid)
- Complete database schema documentation

### `.deployment/DEPLOYMENT_PROCEDURES.md`
- Initial deployment reference
- Code deployment from GitHub
- Update/hotfix procedures (backend and frontend)
- Rollback procedures (3 methods documented)
- Health checks and monitoring commands
- Comprehensive troubleshooting guide
- Recent fixes documentation

### Additional Documentation
- `HETZNER_SETUP.md` - Initial server setup
- `SSH_KEY_SETUP.md` - SSH configuration
- `DEPLOYMENT_CHECKLIST.md` - Step-by-step checklist
- `QUICK_START.md` - 5-minute reference
- `README.md` - Navigation guide

---

## 5. Git Commits Pushed

All fixes and documentation committed to GitHub repository:
- Repository: https://github.com/maccie01/monitoring_portal.git
- Branch: main

### Commits:
1. **fix(frontend): correct temperature API endpoint and add time range mapping**
   - Fixed temperature API 404 and 500 errors
   - Commit: 0646699

2. **docs(deployment): add initial deployment documentation**
   - Added SSH setup and deployment guides
   - Commit: 6e5e222

3. **docs(deployment): add comprehensive production documentation**
   - Added server infrastructure, architecture, and procedures docs
   - Commit: f89d633

---

## 6. Key Learnings

### Backend Deployment Requirement
**CRITICAL**: When updating backend code on production:
1. Source code changes are NOT enough
2. Backend must be REBUILT with esbuild to create new bundle
3. PM2 runs `/opt/netzwaechter/dist/index.js` (bundled), not source files
4. Always run: `npx esbuild apps/backend-api/index.ts --platform=node --packages=external --bundle --format=esm --outdir=dist`
5. Then restart PM2: `pm2 restart all`

### Frontend vs Backend Deployment
- **Frontend**: Static files, no rebuild needed on server (rsync dist/ is sufficient)
- **Backend**: Requires bundle rebuild on server before PM2 restart

### Threshold Configuration
- Database stores correct threshold data
- API must return as array, not single object
- Frontend checks `Array.isArray()` before processing
- Missing `netzwaechter_0` config causes all objects to show offline

---

## 7. Server Access Information

### SSH Access
```bash
ssh netzwaechter-prod
# or
ssh root@91.98.156.158
```

### Key Locations
- **Application**: `/opt/netzwaechter/`
- **Backend Bundle**: `/opt/netzwaechter/dist/index.js`
- **Frontend Build**: `/opt/netzwaechter/apps/frontend-web/dist/`
- **Environment**: `/opt/netzwaechter/.env`
- **Nginx Config**: `/etc/nginx/sites-available/netzwaechter`
- **SSL Certificates**: `/etc/letsencrypt/live/netzwaechter.nexorithm.io/`
- **PM2 Logs**: `/root/.pm2/logs/`

### Important Commands
```bash
# Check application status
pm2 status
pm2 logs netzwaechter

# Check Nginx
sudo systemctl status nginx
sudo nginx -t

# Check SSL certificate
sudo certbot certificates

# Check firewall
sudo ufw status numbered

# Check fail2ban
sudo fail2ban-client status sshd

# Application health
curl http://localhost:3000/api/health
curl https://netzwaechter.nexorithm.io/api/health
```

---

## 8. Database Configuration

### Connection Details
- **Type**: PostgreSQL (Neon Serverless)
- **Host**: 23.88.40.91
- **Port**: 50184
- **Database**: 20251001_neu_neondb
- **User**: postgres
- **Connection String**: In `/opt/netzwaechter/.env` as `DATABASE_URL`

### Schema
- 15+ core tables documented in APPLICATION_ARCHITECTURE.md
- Key tables: objects, users, settings, logbook_entries, todo_tasks
- JSONB columns for flexible data: fltemp, rttemp, meter, objdata

---

## 9. Production URLs

- **Application**: https://netzwaechter.nexorithm.io
- **Health Check**: https://netzwaechter.nexorithm.io/api/health
- **API Base**: https://netzwaechter.nexorithm.io/api
- **WebSocket**: wss://netzwaechter.nexorithm.io/ws

---

## 10. Next Steps & Recommendations

### Immediate
- ✅ All critical bugs fixed
- ✅ Documentation complete
- ✅ Code pushed to GitHub
- ✅ Production verified working

### Short Term
1. Set up automated deployment pipeline (GitHub Actions)
2. Configure database backups (currently manual)
3. Add monitoring/alerting (Uptime Robot, Grafana)
4. Consider CI/CD for automated testing before deployment

### Long Term
1. Implement blue-green deployment for zero-downtime updates
2. Add comprehensive logging (structured logs, log aggregation)
3. Set up staging environment for testing
4. Document disaster recovery procedures
5. Implement automated rollback on health check failure

---

## 11. Contact & Support

### Repository
- **GitHub**: https://github.com/maccie01/monitoring_portal.git
- **Issues**: Create GitHub issues for bug reports

### Server
- **Provider**: Hetzner Cloud
- **IP**: 91.98.156.158
- **SSH Key**: ~/.ssh/netzwaechter_deployment

### Documentation
- All deployment documentation in `.deployment/` directory
- Start with `.deployment/README.md` for navigation

---

## Summary

This session successfully:
1. ✅ Deployed Netzwächter application to production server
2. ✅ Configured SSL/TLS, Nginx, PM2, security measures
3. ✅ Fixed 3 critical bugs preventing application functionality
4. ✅ Created comprehensive documentation (3 major docs, 4000+ lines)
5. ✅ Committed all changes to GitHub
6. ✅ Verified production application is fully functional

**Application Status**: ✅ PRODUCTION READY & WORKING

**URL**: https://netzwaechter.nexorithm.io

---

*Generated: October 14, 2025*
*Session Duration: ~3 hours*
*Lines of Documentation: 4,000+*
*Bugs Fixed: 3 (2 frontend, 1 backend)*
*Git Commits: 3*
