# Archon Deployment Documentation Index

**Created**: 2025-10-15
**Last Updated**: 2025-10-16
**Status**: Complete ✅ - Reorganized and Consolidated

---

## Quick Start

### For Deployment

1. 📖 Start with [README.md](./README.md) for deployment overview
2. ⚡ See [QUICK_START.md](./QUICK_START.md) for common operations (5-minute guide)
3. 🔐 Review [core/CREDENTIALS.md](./core/CREDENTIALS.md) for all access credentials
4. ⚙️ Check [core/ENVIRONMENT.md](./core/ENVIRONMENT.md) for configuration details
5. 🔒 Read [security/AUTHENTICATION.md](./security/AUTHENTICATION.md) for auth system
6. 🐳 See [core/DOCKER_SETUP.md](./core/DOCKER_SETUP.md) for container management

### For Security

1. ⭐ Start with [security/README.md](./security/README.md) for security overview
2. 🔐 Review [security/AUTHENTICATION.md](./security/AUTHENTICATION.md) for authentication details
3. 📋 See [archive/security-audits/](./archive/security-audits/) for complete audit history

---

## Documentation Structure

```
.deployment/archon/
├── README.md                    # Main deployment guide
├── QUICK_START.md               # 5-minute quick reference
├── INDEX.md                     # This file
├── ORGANIZATION_PLAN.md         # Reorganization details
│
├── core/                        # Essential operational docs
│   ├── CREDENTIALS.md
│   ├── ENVIRONMENT.md
│   ├── DOCKER_SETUP.md
│   └── DEPLOYMENT_SUMMARY.md
│
├── security/                    # Security documentation
│   ├── README.md
│   └── AUTHENTICATION.md
│
├── services/                    # Service-specific guides
│   ├── supabase/
│   │   ├── README.md
│   │   └── SUPABASE_ALL_ISSUES_RESOLVED.md
│   ├── arcane/
│   │   ├── README.md
│   │   ├── ARCANE_DEPLOYMENT_COMPLETE.md
│   │   ├── ARCANE_CLOUDFLARE_DNS_SETUP.md
│   │   └── ARCANE_WEBSOCKET_FIX.md
│   └── mcp/
│       ├── MCP_SETUP_GUIDE.md
│       └── MCP_SETUP_TEST_RESULTS.md
│
└── archive/                     # Historical documentation
    ├── cleanup/                 # Cleanup phase reports
    ├── security-audits/         # Security audit history
    ├── agent-work/              # Agent coordination docs
    └── supabase-fixes/          # Supabase fix history
```

### Core Documentation

| File | Description | When to Use |
|------|-------------|-------------|
| [README.md](./README.md) | Main deployment guide with architecture, setup, and maintenance | Starting point for all deployment tasks |
| [QUICK_START.md](./QUICK_START.md) | 5-minute quick reference guide | Common operations and quick access |
| [core/CREDENTIALS.md](./core/CREDENTIALS.md) | All passwords, API keys, and access credentials | Need credentials for any service |
| [core/ENVIRONMENT.md](./core/ENVIRONMENT.md) | Complete .env file reference and configuration | Setting up or troubleshooting environment |
| [security/AUTHENTICATION.md](./security/AUTHENTICATION.md) | API key authentication system guide | Managing API keys, troubleshooting auth |
| [core/DOCKER_SETUP.md](./core/DOCKER_SETUP.md) | Docker Compose and container management | Working with containers and services |

---

## Documentation by Task

### Initial Setup

**Setting up a new server**:
1. [README.md](./README.md) → "Initial Setup" section
2. [ENVIRONMENT.md](./ENVIRONMENT.md) → "Environment Setup Process"
3. [DOCKER_SETUP.md](./DOCKER_SETUP.md) → "Build Process"
4. [AUTHENTICATION.md](./AUTHENTICATION.md) → "Bootstrap Process"

**Creating first API key**:
1. [AUTHENTICATION.md](./AUTHENTICATION.md) → "Bootstrap Process"
2. [CREDENTIALS.md](./CREDENTIALS.md) → Save generated key

### Daily Operations

**Deploying updates**:
- [README.md](./README.md) → "Deployment Updates" section
- [DOCKER_SETUP.md](./DOCKER_SETUP.md) → "Build Process"

**Viewing logs**:
- [README.md](./README.md) → "Log Access" section
- [DOCKER_SETUP.md](./DOCKER_SETUP.md) → "View Logs"

**Health checks**:
- [README.md](./README.md) → "Health Checks" section
- [DOCKER_SETUP.md](./DOCKER_SETUP.md) → "Check Status"

### Security & Access

**Managing API keys**:
- [AUTHENTICATION.md](./AUTHENTICATION.md) → "Key Management"
- [CREDENTIALS.md](./CREDENTIALS.md) → Store new keys

**SSH access**:
- [CREDENTIALS.md](./CREDENTIALS.md) → "SSH Credentials"
- [README.md](./README.md) → "Server Infrastructure"

**Rotating credentials**:
- [CREDENTIALS.md](./CREDENTIALS.md) → "Credential Rotation Schedule"
- [AUTHENTICATION.md](./AUTHENTICATION.md) → "Rotating Keys"

### Troubleshooting

**Authentication issues**:
- [AUTHENTICATION.md](./AUTHENTICATION.md) → "Troubleshooting"
- [ENVIRONMENT.md](./ENVIRONMENT.md) → "Troubleshooting"

**Container issues**:
- [DOCKER_SETUP.md](./DOCKER_SETUP.md) → "Debugging"
- [README.md](./README.md) → "Troubleshooting"

**Environment problems**:
- [ENVIRONMENT.md](./ENVIRONMENT.md) → "Troubleshooting"
- [README.md](./README.md) → "Troubleshooting"

---

## Quick Reference

### Essential Commands

```bash
# SSH to server
ssh -i ~/.ssh/netzwaechter_deployment root@91.98.156.158

# View logs
docker compose logs -f archon-server

# Restart services
docker compose restart

# Deploy updates
cd /opt/archon
git pull origin stable
docker compose build
docker compose up -d

# Health check
curl http://localhost:8181/health
```

### Important URLs

| Service | URL | Documentation |
|---------|-----|---------------|
| Frontend | https://archon.nexorithm.io | [README.md](./README.md) |
| API | https://archon.nexorithm.io/api | [AUTHENTICATION.md](./AUTHENTICATION.md) |
| Supabase Studio | https://archon.nexorithm.io/db | [CREDENTIALS.md](./CREDENTIALS.md) |

### Key Files on Server

| Path | Purpose | Documentation |
|------|---------|---------------|
| `/opt/archon/.env` | Environment configuration | [ENVIRONMENT.md](./ENVIRONMENT.md) |
| `/opt/archon/docker-compose.yml` | Container orchestration | [DOCKER_SETUP.md](./DOCKER_SETUP.md) |
| `/etc/nginx/sites-enabled/archon` | Nginx reverse proxy | [README.md](./README.md) |
| `/opt/archon/migration/` | Database migrations | [AUTHENTICATION.md](./AUTHENTICATION.md) |

---

## Documentation Standards

### Updating Documentation

**When to update**:
- After any significant deployment change
- When credentials are rotated
- After troubleshooting new issues
- When adding new features

**How to update**:
1. Edit the relevant markdown file
2. Update "Last Updated" date
3. Add entry to [README.md](./README.md) "Deployment History"
4. Commit changes to git

### Markdown Conventions

- Use `**Bold**` for important terms
- Use `code blocks` for commands
- Use tables for structured data
- Include examples where helpful
- Cross-reference other docs with relative links

---

## Getting Help

### Internal Resources

1. Check this documentation first
2. Review Git history for similar changes
3. Check Docker/Nginx logs

### External Resources

- **Archon GitHub**: https://github.com/maccie01/archon-base
- **Docker Docs**: https://docs.docker.com
- **Nginx Docs**: https://nginx.org/en/docs/
- **Supabase Docs**: https://supabase.com/docs

### Emergency Contacts

See [README.md](./README.md) → "Emergency Contacts & Resources"

---

## Documentation Coverage

### ✅ Covered

- [x] Initial setup and deployment
- [x] Environment configuration
- [x] Authentication system
- [x] Docker container management
- [x] Security and credentials
- [x] Daily operations
- [x] Troubleshooting common issues
- [x] SSH and server access

### ✅ Security Documentation (Added 2025-10-15)

- [x] Security deployment final report (SECURITY_DEPLOYMENT_FINAL_REPORT.md)
- [x] Security deployment summary (SECURITY_DEPLOYMENT_COMPLETE.md)
- [x] Final security summary (FINAL_SECURITY_SUMMARY.md)
- [x] Authentication audit (AUTHENTICATION_AUDIT_COMPLETE.md)
- [x] Infrastructure audit (INFRASTRUCTURE_AUDIT_COMPLETE.md)
- [x] Nginx security hardening (NGINX_SECURITY_HARDENING_COMPLETE.md)
- [x] Docker port binding analysis (DOCKER_PORT_BINDING_ANALYSIS.md)
- [x] Security fix plan (SECURITY_FIX_PLAN.md)

### 🔄 Future Documentation

- [ ] API endpoint reference (API_REFERENCE.md)
- [ ] Monitoring and alerting setup
- [ ] Backup and disaster recovery procedures
- [ ] Performance tuning guide
- [ ] CI/CD pipeline documentation

---

## Document Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-10-15 | 1.0.0 | Initial documentation set created |

---

## Maintenance Schedule

| Task | Frequency | Responsible |
|------|-----------|-------------|
| Review documentation accuracy | Monthly | DevOps Team |
| Update credentials | Quarterly | Security Team |
| Audit access logs | Monthly | Security Team |
| Update deployment history | After each deploy | DevOps Team |
| Review and archive old docs | Annually | Documentation Team |

---

**Created**: 2025-10-15
**Maintained By**: Development Team
**Contact**: See [README.md](./README.md) for support channels
