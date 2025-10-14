# Deployment Documentation

Created: 2025-10-14

This directory contains all documentation and scripts for deploying Netzwächter to production.

---

## Quick Navigation

### 🚀 New to Deployment?
**Start here**: [`QUICK_START.md`](./QUICK_START.md)
- Your SSH public key (ready to copy)
- 4-step setup process
- 5 minute overview

### 📖 Complete Setup Guide
**Full documentation**: [`HETZNER_SETUP.md`](./HETZNER_SETUP.md)
- Server specifications and assessment
- Complete deployment strategy
- Security configuration
- Monitoring and maintenance
- Troubleshooting guide

### 🔑 SSH Key Details
**SSH configuration**: [`SSH_KEY_SETUP.md`](./SSH_KEY_SETUP.md)
- Key information and locations
- How to add key to server
- Connection testing
- Troubleshooting SSH issues
- Key management and security

---

## Current Status

### Server Information
- **Provider**: Hetzner
- **Server IP**: `___________________` (TO BE FILLED)
- **Domain**: `___________________` (TO BE FILLED)
- **OS**: Ubuntu 22.04/24.04 LTS

### Deployment Progress
- [x] SSH key pair generated
- [x] Deployment documentation created
- [ ] SSH key added to server
- [ ] SSH connection tested
- [ ] Server hardening complete
- [ ] Dependencies installed
- [ ] Database configured
- [ ] Application deployed
- [ ] SSL/TLS configured
- [ ] Monitoring setup

---

## Files in This Directory

| File | Purpose | Status |
|------|---------|--------|
| `README.md` | This file - navigation and overview | ✅ Complete |
| `QUICK_START.md` | 5-minute quick start guide | ✅ Complete |
| `HETZNER_SETUP.md` | Complete server setup documentation | ✅ Complete |
| `SSH_KEY_SETUP.md` | SSH key configuration and troubleshooting | ✅ Complete |

---

## SSH Key Information

**Private Key**: `~/.ssh/netzwaechter_deployment` (KEEP SECRET)
**Public Key**: `~/.ssh/netzwaechter_deployment.pub`
**Fingerprint**: `SHA256:7tVzuYLSTnjuQuxsNL2dw5QqNjBAsNMVaZJvPZmAm0w`

**Your public key**:
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICdyyWO2xYQbC2Gn4efgFk8l60LACLpuY9Lg3Wpb3phJ netzwaechter-deployment-20251014
```

---

## Quick Commands

### Connect to Server
```bash
# If SSH config setup:
ssh netzwaechter-prod

# Or full command:
ssh -i ~/.ssh/netzwaechter_deployment root@YOUR_SERVER_IP
```

### Copy File to Server
```bash
scp -i ~/.ssh/netzwaechter_deployment file.txt root@YOUR_SERVER_IP:/path/
```

### Run Command on Server
```bash
ssh -i ~/.ssh/netzwaechter_deployment root@YOUR_SERVER_IP "command"
```

---

## Deployment Methods

### Option A: Direct SSH (Recommended)
Claude SSH's directly to server and:
- Installs all dependencies
- Configures security
- Deploys application
- Sets up SSL/TLS
- Configures monitoring

**Time**: 1-2 hours
**Interaction**: Minimal

### Option B: Guided Setup
Claude provides commands, you execute:
- More control over each step
- Learn deployment process
- Can pause at any step

**Time**: 2-3 hours
**Interaction**: Continuous

---

## What Gets Installed

### System Packages
- ufw (firewall)
- fail2ban (intrusion prevention)
- unattended-upgrades (security updates)

### Application Stack
- Node.js 20 LTS
- pnpm 8.x
- PM2 (process manager)
- PostgreSQL 16
- Nginx (reverse proxy)
- Certbot (SSL/TLS)

### Security
- Firewall: Ports 22, 80, 443 only
- SSH: Key-only authentication
- Fail2ban: Brute force protection
- SSL/TLS: Let's Encrypt certificates
- Auto-updates: Security patches

---

## Server Specifications

**Your Hetzner Server**:
- 8 vCPU
- 16 GB RAM
- 160 GB Disk
- 20 TB Traffic
- 11.99 EUR/month

**Netzwächter Requirements**:
- 2-4 vCPU (need)
- 4-8 GB RAM (need)
- 40-60 GB Disk (need)
- < 1 TB Traffic (typical)

**Assessment**: ✅ Perfect! You have 2-4x the required resources.

---

## Next Steps

1. **Add SSH key to server** (see QUICK_START.md)
2. **Test SSH connection**
3. **Provide server IP and domain**
4. **Choose deployment method** (A or B)
5. **Begin deployment**

---

## Support & Troubleshooting

### SSH Issues
See: [`SSH_KEY_SETUP.md`](./SSH_KEY_SETUP.md) - Troubleshooting section

### Server Issues
See: [`HETZNER_SETUP.md`](./HETZNER_SETUP.md) - Troubleshooting section

### Application Issues
Will be documented during deployment

---

## Security Notes

### SSH Key Security
- ✅ Private key: 600 permissions (owner only)
- ✅ Never share private key
- ✅ Backup private key securely
- ✅ Use unique key per server

### Server Security
Once deployed:
- ✅ Firewall active (only ports 22, 80, 443)
- ✅ SSH key authentication only
- ✅ Fail2ban protecting against brute force
- ✅ Automatic security updates
- ✅ SSL/TLS enforced

---

## Maintenance

### After Deployment
- **Daily**: Check PM2 status, application logs
- **Weekly**: Review resource usage, create snapshot
- **Monthly**: Update packages, security audit
- **Quarterly**: Full security review, test backups

### Backup Strategy
- **Database**: Daily automated backups (30-day retention)
- **Code**: Git repository (source of truth)
- **Server**: Weekly Hetzner snapshots (4-week retention)

---

## Cost Summary

**Monthly Costs**:
- Server: 11.99 EUR
- Domain: ~0.83 EUR (10 EUR/year)
- SSL: Free (Let's Encrypt)
- **Total**: ~13 EUR/month

**One-time Costs**:
- Domain registration: ~10 EUR/year
- Setup: Free (Claude-assisted)

---

## Resources

### Official Documentation
- [Hetzner Cloud](https://docs.hetzner.com/cloud/)
- [Ubuntu Server](https://ubuntu.com/server/docs)
- [Node.js](https://nodejs.org/en/docs/)
- [PostgreSQL](https://www.postgresql.org/docs/16/)
- [PM2](https://pm2.keymetrics.io/docs/)
- [Nginx](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)

### Project Documentation
- Project Standards: `../.archon-knowledge-base/07-standards/`
- Security Patterns: `../.archon-knowledge-base/07-standards/SECURITY_PATTERNS.md`
- Backend Patterns: `../.archon-knowledge-base/07-standards/BACKEND_PATTERNS.md`

---

**Created**: 2025-10-14
**Last Updated**: 2025-10-14
**Status**: Ready for deployment
**Next Action**: Add SSH key to server
