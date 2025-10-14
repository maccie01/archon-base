# Quick Start - Netzwächter Deployment

Created: 2025-10-14

## Your SSH Public Key

**Copy this ENTIRE line to your server**:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICdyyWO2xYQbC2Gn4efgFk8l60LACLpuY9Lg3Wpb3phJ netzwaechter-deployment-20251014
```

---

## Step 1: Add Key to Server

### Easiest Method (if password enabled):
```bash
ssh-copy-id -i ~/.ssh/netzwaechter_deployment.pub root@YOUR_SERVER_IP
```

### Via Hetzner Console:
✅ **ALREADY DONE** - SSH key is configured and working!

---

## Step 2: Test Connection

```bash
ssh netzwaechter-prod
```

✅ **CONNECTION WORKS!** Server is ready for deployment!

---

## Step 3: Setup SSH Config (Optional)

```bash
cat >> ~/.ssh/config << 'EOF'

Host netzwaechter-prod
    HostName YOUR_SERVER_IP
    User root
    IdentityFile ~/.ssh/netzwaechter_deployment
    Port 22
EOF

chmod 600 ~/.ssh/config
```

Then connect with: `ssh netzwaechter-prod`

---

## Step 4: Give Claude Access

Once SSH works, choose:

**Option A - Direct Access (Fastest)**:
Let Claude SSH directly to setup everything

**Option B - Guided (You execute)**:
Claude provides commands, you run them

---

## What We'll Setup

1. ✅ Security (firewall, fail2ban, SSH hardening)
2. ✅ Dependencies (Node.js 20, PostgreSQL 16, PM2, Nginx)
3. ✅ Database (create user, database, migrations)
4. ✅ Application (deploy, build, start)
5. ✅ SSL/TLS (Let's Encrypt certificate)
6. ✅ Monitoring (PM2, logs, health checks)

**Time**: 1-2 hours total

---

## Server Information

1. **Server IP**: `91.98.156.158` ✅
2. **Hostname**: `netzwaechter` ✅
3. **SSH works**: YES ✅
4. **OS**: Ubuntu 24.04.3 LTS ✅
5. **Domain**: TBD
6. **Deployment method**: Choose A (direct) or B (guided)

---

**Files Created**:
- `.deployment/HETZNER_SETUP.md` - Complete setup documentation
- `.deployment/SSH_KEY_SETUP.md` - Detailed SSH key guide
- `.deployment/QUICK_START.md` - This file

**SSH Keys**:
- Private: `~/.ssh/netzwaechter_deployment` (KEEP SECRET)
- Public: `~/.ssh/netzwaechter_deployment.pub`

**Status**: Ready for deployment! 🚀
