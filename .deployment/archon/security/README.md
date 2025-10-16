# Security Documentation

Created: 2025-10-16

## Overview

Archon security documentation including authentication, audits, and security configurations.

## Current Security Posture

Status: Production-Ready
Last Audit: 2025-10-15
All Critical Issues: Resolved

## Authentication Methods

### 1. API Key Authentication
**Used by**: Archon API endpoints
**Configuration**: See [AUTHENTICATION.md](./AUTHENTICATION.md)
**Management**: Stored in Supabase `api_keys` table

**Quick Test**:
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://archon.nexorithm.io/api/auth/validate
```

### 2. HTTP Basic Authentication
**Used by**: Supabase Studio, Arcane UI
**Configuration**: Nginx `.htpasswd` files
**Credentials**: See [../core/CREDENTIALS.md](../core/CREDENTIALS.md)

### 3. Supabase RLS (Row Level Security)
**Used by**: Database access control
**Configuration**: Supabase Dashboard → Authentication → Policies

## Security Features Implemented

- [x] API key authentication on all 79 API endpoints
- [x] HTTP Basic Auth on admin interfaces (Supabase Studio, Arcane)
- [x] Nginx rate limiting (30 req/min per IP)
- [x] Localhost binding for internal services
- [x] Firewall configuration (UFW)
- [x] SSL/TLS via Cloudflare + Let's Encrypt
- [x] Security headers (HSTS, CSP, X-Frame-Options)
- [x] Docker network isolation

## Quick Security Checks

```bash
# Check authentication is working
curl -I https://archon.nexorithm.io/api/knowledge-items/summary
# Should return 401 Unauthorized without API key

# Check Supabase Studio requires auth
curl -I https://supabase.archon.nexorithm.io/
# Should return 401 Unauthorized

# Check services bound to localhost
ssh netzwaechter-prod "netstat -tlnp | grep -E '8181|8051|54321'"
# Should show 127.0.0.1, not 0.0.0.0

# Check firewall status
ssh netzwaechter-prod "ufw status"
```

## Security Audit History

Comprehensive security audits completed on 2025-10-15. See archive for details:

- **Comprehensive Audit**: [../archive/security-audits/COMPREHENSIVE_SECURITY_AUDIT_2025-10-15.md](../archive/security-audits/COMPREHENSIVE_SECURITY_AUDIT_2025-10-15.md)
- **Final Report**: [../archive/security-audits/SECURITY_DEPLOYMENT_FINAL_REPORT.md](../archive/security-audits/SECURITY_DEPLOYMENT_FINAL_REPORT.md)
- **Authentication Audit**: [../archive/security-audits/AUTHENTICATION_AUDIT_COMPLETE.md](../archive/security-audits/AUTHENTICATION_AUDIT_COMPLETE.md)
- **Infrastructure Audit**: [../archive/security-audits/INFRASTRUCTURE_AUDIT_COMPLETE.md](../archive/security-audits/INFRASTRUCTURE_AUDIT_COMPLETE.md)
- **Nginx Hardening**: [../archive/security-audits/NGINX_SECURITY_HARDENING_COMPLETE.md](../archive/security-audits/NGINX_SECURITY_HARDENING_COMPLETE.md)

## Credential Management

All production credentials documented in:
- [../core/CREDENTIALS.md](../core/CREDENTIALS.md)

Includes:
- API keys
- Database credentials
- SSH keys
- Admin passwords
- Service tokens

## Incident Response

If security issue detected:

1. **Immediate**: Disable compromised credentials
2. **Assess**: Check logs for suspicious activity
3. **Rotate**: Generate new credentials
4. **Document**: Update security documentation
5. **Review**: Audit related systems

## Security Maintenance Schedule

| Task | Frequency | Last Done |
|------|-----------|-----------|
| Credential rotation | Quarterly | 2025-10-15 |
| Security audit | Annually | 2025-10-15 |
| Dependency updates | Monthly | - |
| Log review | Weekly | - |
| Access audit | Quarterly | 2025-10-15 |

## Resources

**External Documentation**:
- Nginx Security: https://nginx.org/en/docs/http/configuring_https_servers.html
- Docker Security: https://docs.docker.com/engine/security/
- Supabase Security: https://supabase.com/docs/guides/platform/going-into-prod

**Internal Documentation**:
- [AUTHENTICATION.md](./AUTHENTICATION.md) - Complete authentication guide
- [../README.md](../README.md) - Main deployment documentation
- [../core/](../core/) - Core configuration files
