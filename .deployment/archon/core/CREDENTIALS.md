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
ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI
```

**Key Details**:
- **Name**: Production Master Key
- **Key Prefix**: `ak_597A`
- **Created**: 2025-10-15
- **Permissions**: Full admin access (read, write, admin)
- **Status**: Active
- **Last Used**: Check via `/api/auth/validate`

**Usage Example**:
```bash
curl -H "Authorization: Bearer ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI" \
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
| Supabase Studio | https://supabase.archon.nexorithm.io | Database admin (protected) |

---

## Supabase (Self-Hosted Database)

**Architecture**: Self-hosted Supabase stack running in Docker on single network (archon_production)

### Connection Details

**Internal Docker Network**:
- **Kong Gateway**: http://kong:8000 (internal) → http://localhost:54321 (host)
- **PostgreSQL**: postgres:5432 (internal) → localhost:54322 (host)
- **Studio UI**: studio:3000 (internal) → localhost:54323 (host)

**External Access**:
- **Studio UI**: https://supabase.archon.nexorithm.io (protected by HTTP Basic Auth)
- **API Gateway**: Accessed through archon-server (not exposed externally)

### JWT Secret

**Critical Configuration**:
```
JWT_SECRET=super-secret-jwt-token-with-at-least-32-characters-long
```

**⚠️ CRITICAL**: This JWT secret MUST match the value stored in the database's `app.settings.jwt_secret` configuration. Mismatches cause PGRST301 JWT validation errors.

**Stored In**:
- `.env` file: `JWT_SECRET` variable
- Database: `app.settings.jwt_secret` GUC parameter
- Kong config: Used to generate JWT tokens

### API Keys (JWT Tokens)

**Anon Key** (Generated from JWT_SECRET):
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
```
- **Purpose**: Client-side queries with RLS
- **Permissions**: Row Level Security enforced
- **JWT Claims**: `role: "anon"`, `iss: "supabase-demo"`, `exp: 1983812996`
- **Usage**: Frontend database queries (if needed)

**Service Role Key** (Server-side only, NEVER expose):
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU
```
- **Purpose**: Server-side admin operations
- **Permissions**: Bypasses RLS, full access
- **JWT Claims**: `role: "service_role"`, `iss: "supabase-demo"`, `exp: 1983812996`
- **Security**: ⚠️ KEEP SECRET - Has full database access
- **Used By**: archon-server, Kong Gateway (hardcoded in kong.yml)

### Kong Gateway Configuration

**JWT Transformation**:
Kong removes all incoming `Authorization` headers and adds a hardcoded service role JWT token. This ensures all PostgREST requests use the service role, regardless of client authentication.

**Location**: `volumes/api/kong.yml`
```yaml
plugins:
  - name: request-transformer
    config:
      remove:
        headers:
          - Authorization
          - authorization
      add:
        headers:
          - "Authorization: Bearer eyJhbGci..."
```

### Database Direct Access

**From Host Machine**:
```bash
psql -h localhost -p 54322 -U postgres -d postgres
```

**Password**: `SUcWRRb52CMUPMzLA2OBhKI2spOuqOEq` (from `.env`)

**From Docker Container**:
```bash
docker exec -it archon-postgres psql -U postgres -d postgres
```

**Connection String**:
```
postgresql://postgres:SUcWRRb52CMUPMzLA2OBhKI2spOuqOEq@localhost:54322/postgres
```

### Supabase Studio Access

**URL**: https://supabase.archon.nexorithm.io
**Protected By**: Nginx HTTP Basic Authentication
**Username**: Check `.htpasswd-supabase` file or Nginx config
**Password**: Set during Nginx configuration

**Alternative Local Access** (from server):
```bash
# Access Studio without Basic Auth
curl http://localhost:54323
```

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

**Last Updated**: 2025-10-16 (Consolidated Architecture v1.3.0)
**Review Needed**: 2026-01-16 (Quarterly review)
**Responsible**: DevOps Team

### Recent Changes (v1.3.0 - 2025-10-16)

- ✅ Migrated to self-hosted Supabase on single Docker network
- ✅ Updated JWT secret to match database-stored value
- ✅ Documented Kong JWT transformation configuration
- ✅ Updated database connection details for Docker deployment
- ✅ Consolidated from cloud-hosted to self-hosted architecture

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
