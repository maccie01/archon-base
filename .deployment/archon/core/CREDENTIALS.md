# Archon Production Credentials

**Created**: 2025-10-15
**Classification**: CONFIDENTIAL - DO NOT COMMIT TO PUBLIC REPOS

---

## ⚠️ Security Notice

This file contains sensitive credentials for production systems. Handle with care:

- ✅ Store in password manager (1Password, Bitwarden, etc.)
- ✅ Encrypt if storing in version control
- ✅ Use `.gitignore` to exclude from commits
- ✅ Rotate keys regularly (quarterly recommended)
- ❌ Never share via email or chat
- ❌ Never commit to public repositories
- ❌ Never expose in client-side code

---

## Server Access

### SSH Credentials

**Server IP**: `91.98.156.158`
**Username**: `root`
**Authentication**: SSH key-based

**Private Key Location**: `~/.ssh/netzwaechter_deployment`
**Public Key Fingerprint**: `SHA256:7tVzuYLSTnjuQuxsNL2dw5QqNjBAsNMVaZJvPZmAm0w`

**Connection Command**:
```bash
ssh -i ~/.ssh/netzwaechter_deployment root@91.98.156.158
```

**SSH Config Entry** (`~/.ssh/config`):
```
Host archon-prod
    HostName 91.98.156.158
    User root
    IdentityFile ~/.ssh/netzwaechter_deployment
    Port 22
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

Then connect with: `ssh archon-prod`

---

## Archon Application

### API Authentication

**Production API Key** (Admin):
```
ak_266E_qxiSRg309qhky6v_9MB5EYQ_bQWSpKch8RoJTntfhpQ
```

**Key Details**:
- **Name**: Production Master Key 2025-10-16
- **Key ID**: `6e1a653b-aa3a-4df1-a2df-5b4d8683d58e`
- **Key Prefix**: `ak_266E`
- **Created**: 2025-10-16
- **Permissions**: Full admin access (read, write, admin)
- **Status**: Active
- **Last Used**: Check via `/api/auth/validate`

**Usage Example**:
```bash
curl -H "Authorization: Bearer ak_266E_qxiSRg309qhky6v_9MB5EYQ_bQWSpKch8RoJTntfhpQ" \
  https://archon.nexorithm.io/api/auth/validate
```

**⚠️ Security Note**: This is the ONLY copy of this API key. Store it securely in a password manager immediately!

**Bootstrap Secret**:
```
8aJEvaqfNAektfXZ6enA27_XPQ3nf-OjG1z9RhAPu0k
```
- **Purpose**: One-time secret for creating first API key
- **Status**: Already used (can be rotated)
- **Location**: `ARCHON_BOOTSTRAP_SECRET` in `.env`

### Application URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | https://archon.nexorithm.io | Main application |
| Backend API | https://archon.nexorithm.io/api | REST API |
| MCP Server | https://archon.nexorithm.io/mcp | Model Context Protocol |
| Supabase Studio | https://archon.nexorithm.io/db | Database admin (protected) |

---

## Supabase (Database)

### Connection Details

**Project URL**:
```
https://[PROJECT_ID].supabase.co
```

**Connection String** (from `.env`):
```
postgresql://postgres.[PROJECT_ID]:[PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres
```

### API Keys

**Anon Key** (Client-side, safe to expose):
```
[SUPABASE_ANON_KEY from .env]
```
- **Purpose**: Client-side queries with RLS
- **Permissions**: Row Level Security enforced
- **Usage**: Frontend database queries

**Service Role Key** (Server-side only, NEVER expose):
```
[SUPABASE_SERVICE_ROLE_KEY from .env]
```
- **Purpose**: Server-side admin operations
- **Permissions**: Bypasses RLS, full access
- **Security**: ⚠️ KEEP SECRET - Has full database access

### Database Direct Access

**Host**: `aws-0-[region].pooler.supabase.com`
**Port**: `6543` (Supavisor pooler) or `5432` (direct)
**Database**: `postgres`
**User**: `postgres.[PROJECT_ID]`
**Password**: [From connection string]

**Connection via psql**:
```bash
psql "postgresql://postgres.[PROJECT_ID]:[PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres"
```

### Supabase Studio Access

**URL**: https://archon.nexorithm.io/db
**Username**: Configured via `.htpasswd-supabase`
**Password**: [Set during nginx basic auth setup]

**Note**: Protected by Nginx basic authentication

---

## Domain & DNS

### Cloudflare

**Email**: [Your Cloudflare account email]
**Domain**: nexorithm.io

**DNS Records**:
```
Type: A
Name: archon
Content: 91.98.156.158
Proxy: Enabled (Orange cloud)
TTL: Auto

Type: A
Name: supabase.archon
Content: 91.98.156.158
Proxy: Disabled (Grey cloud - for SSL)
TTL: Auto
```

**SSL/TLS Mode**: Full (strict)
**Cloudflare API Token**: [If using API for cache purging]

### Let's Encrypt (Subdomain SSL)

**Domain**: supabase.archon.nexorithm.io
**Certificate Path**: `/etc/letsencrypt/live/supabase.archon.nexorithm.io/`
**Renewal**: Automatic via certbot cron

**Manual Renewal**:
```bash
certbot renew
systemctl reload nginx
```

---

## AI Provider Keys

### Anthropic (Claude)

**API Key**: [From `.env` - ANTHROPIC_API_KEY]
**Usage**: Backend AI operations, MCP
**Limits**: Check at https://console.anthropic.com/

### OpenAI (Optional)

**API Key**: [From `.env` - OPENAI_API_KEY if configured]
**Usage**: Alternative AI provider
**Limits**: Check at https://platform.openai.com/

### OpenRouter (Optional)

**API Key**: [From `.env` - OPENROUTER_API_KEY if configured]
**Usage**: Multi-model access
**Limits**: Check at https://openrouter.ai/

### Google AI (Optional)

**API Key**: [From `.env` - GOOGLE_AI_API_KEY if configured]
**Usage**: Gemini models
**Limits**: Check at https://makersuite.google.com/

---

## Monitoring & Observability

### Logfire (Optional)

**Token**: [From `.env` - LOGFIRE_TOKEN if configured]
**Purpose**: Application monitoring and logging
**Dashboard**: https://logfire.pydantic.dev/

---

## Docker Registry (If Using Private)

**Registry URL**: [If applicable]
**Username**: [If applicable]
**Password/Token**: [If applicable]

---

## Environment Variables Reference

Complete `.env` file is documented in [ENVIRONMENT.md](./ENVIRONMENT.md)

**Critical Variables**:
- `AUTH_ENABLED=true`
- `ARCHON_BOOTSTRAP_SECRET`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `ANTHROPIC_API_KEY`
- `ALLOWED_ORIGINS`

---

## Backup Locations

### Git Repository

**Remote**: https://github.com/maccie01/archon-base.git
**Branch**: `stable` (production)
**Access**: SSH key or personal access token

### Server Backups

**Location**: `/root/backups/`
**Schedule**: Manual (recommended: weekly)
**Contents**: Configuration files, environment files

---

## Emergency Access

### If SSH Key Lost

1. Access Hetzner Cloud Console: https://console.hetzner.cloud/
2. Navigate to server
3. Use "Console" feature (browser-based terminal)
4. Add new SSH key to `/root/.ssh/authorized_keys`

### If API Key Compromised

1. SSH to server
2. Connect to Supabase:
   ```bash
   # Via psql or Supabase Dashboard
   ```
3. Disable compromised key:
   ```sql
   UPDATE api_keys SET is_active = false WHERE key_prefix = 'ak_597A';
   ```
4. Create new key:
   ```bash
   cd /opt/archon/migration
   python3 bootstrap_api_key.py
   ```

### If Database Credentials Compromised

1. Login to Supabase Dashboard
2. Settings → Database → Reset database password
3. Update `.env` on server with new credentials
4. Restart services:
   ```bash
   cd /opt/archon
   docker compose restart
   ```

---

## Credential Rotation Schedule

| Credential Type | Recommended Frequency | Last Rotated | Next Due |
|----------------|---------------------|-------------|---------|
| API Keys | Quarterly | 2025-10-16 | 2026-01-16 |
| Database Password | Annually | [Check Supabase] | [+1 year] |
| SSH Keys | Annually | 2025-10-14 | 2026-10-14 |
| AI Provider Keys | As needed | [Check provider] | [As needed] |
| Supabase Studio Password | Quarterly | [When set] | [+3 months] |

---

## Password Storage Recommendations

### Recommended Tools

1. **1Password** (Teams/Business)
   - Shared vaults for team access
   - Secure notes for SSH keys
   - Integration with CLI tools

2. **Bitwarden** (Open source alternative)
   - Self-hosted option available
   - Team sharing features
   - Good API for automation

3. **HashiCorp Vault** (Enterprise)
   - Dynamic secrets
   - Audit logging
   - Advanced access control

### What to Store

- ✅ All passwords and API keys
- ✅ SSH private keys (encrypted)
- ✅ Database connection strings
- ✅ Backup of `.env` file (encrypted)
- ✅ Emergency access procedures

### What NOT to Store

- ❌ Plain text files in repositories
- ❌ Unencrypted notes files
- ❌ Slack/email conversations
- ❌ Screenshots of credentials

---

## Additional Security Measures

### Two-Factor Authentication (2FA)

Enable 2FA on:
- [x] Cloudflare account
- [x] Supabase account
- [x] GitHub account
- [x] Hetzner Cloud account
- [ ] AI provider accounts (Anthropic, OpenAI, etc.)

### IP Whitelisting (Optional)

Consider restricting access to:
- Supabase Studio (via Nginx)
- SSH (via firewall rules)
- Admin API endpoints

### Audit Logging

Monitor:
- API key usage (`api_keys.last_used_at`)
- SSH login attempts (`/var/log/auth.log`)
- Nginx access logs
- Docker container logs

---

**Last Updated**: 2025-10-15
**Review Needed**: 2026-01-15 (Quarterly review)
**Responsible**: DevOps Team

---

## Quick Access Checklist

Before granting access to new team member:

- [ ] Create SSH key pair for them
- [ ] Add their public key to server
- [ ] Create dedicated API key for them
- [ ] Share relevant credentials via password manager
- [ ] Add them to GitHub repository
- [ ] Add them to Cloudflare account (if needed)
- [ ] Brief them on security protocols
- [ ] Document their access level
