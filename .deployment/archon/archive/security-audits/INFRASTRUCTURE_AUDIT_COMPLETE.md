# Infrastructure Security Audit Report
## Archon Deployment at 91.98.156.158

Date Created: 2025-10-15
Timestamp: 12:34:00 CEST

---

## Executive Summary

This security audit examined the production Archon deployment infrastructure focusing on port security, firewall configuration, Docker security, and Nginx hardening. The overall security posture is **GOOD** with proper firewall rules in place blocking external access to sensitive services.

**Key Finding**: All Supabase database ports are properly firewalled and inaccessible from the public internet, which is critical for database security.

---

## 1. Port Security Status

### 1.1 External Port Scan Results

```
PORT      STATE      SERVICE
22/tcp    open       ssh
80/tcp    open       http (Cloudflare proxy)
443/tcp   open       https (Cloudflare proxy)
3737/tcp  filtered   Archon UI (Vite dev server)
8051/tcp  filtered   Archon MCP Server
8181/tcp  filtered   Archon API Server
54321/tcp filtered   Supabase Kong Gateway
54322/tcp filtered   Supabase PostgreSQL Database
54323/tcp filtered   Supabase Studio
54324/tcp filtered   Supabase Inbucket (Email)
54327/tcp filtered   Supabase Analytics
```

**Status**: ✅ SECURE
- All application and database ports are properly filtered by iptables
- Only SSH (22), HTTP (80), and HTTPS (443) are accessible externally
- HTTP/HTTPS traffic is proxied through Cloudflare

### 1.2 Listening Ports Analysis

All services are bound to `0.0.0.0` (all interfaces):
```
0.0.0.0:3737   - Archon UI (docker-proxy)
0.0.0.0:8181   - Archon API Server (docker-proxy)
0.0.0.0:8051   - Archon MCP Server (docker-proxy)
0.0.0.0:54321  - Supabase Kong Gateway (docker-proxy)
0.0.0.0:54322  - Supabase PostgreSQL (docker-proxy)
0.0.0.0:54323  - Supabase Studio (docker-proxy)
0.0.0.0:54324  - Supabase Inbucket (docker-proxy)
0.0.0.0:54327  - Supabase Analytics (docker-proxy)
```

**Status**: ✅ MITIGATED
- While ports are bound to 0.0.0.0, external access is blocked by iptables DOCKER-USER chain
- This is acceptable given the firewall protection

**Note**: 30 packets were dropped on port 54322 (PostgreSQL), indicating external connection attempts were blocked successfully.

---

## 2. Firewall Configuration

### 2.1 iptables DOCKER-USER Chain (Primary Defense)

```
Chain DOCKER-USER (protecting Docker-published ports)
- DROP tcp dpt:54327  (Supabase Analytics)     ✅
- DROP tcp dpt:54324  (Supabase Inbucket)      ✅
- DROP tcp dpt:54323  (Supabase Studio)        ✅
- DROP tcp dpt:54322  (PostgreSQL) - 30 pkts   ✅
- DROP tcp dpt:54321  (Kong Gateway)           ✅
- DROP tcp dpt:11434  (Ollama)                 ✅
- DROP tcp dpt:8181   (Archon API)             ✅
- DROP tcp dpt:8052   (Archon Agents)          ✅
- DROP tcp dpt:8051   (Archon MCP)             ✅
- DROP tcp dpt:5001   (Internal service)       ✅
- DROP tcp dpt:3737   (Archon UI)              ✅
- DROP tcp dpt:3000   (Internal service)       ✅
- RETURN lo           (Loopback allowed)       ✅
```

**Status**: ✅ EXCELLENT
- All critical ports are explicitly blocked on eth0 (external interface)
- Loopback interface is allowed for internal communication
- Rules are processed BEFORE Docker's default ACCEPT rules

### 2.2 UFW Configuration

```
Status: UFW is integrated with iptables
- INPUT chain policy: DROP (with ufw-before-input processing)
- ufw-before-input allows: RELATED,ESTABLISHED connections
- Ollama (11434) accessible from Docker network 172.18.0.0/16
```

**Status**: ✅ SECURE
- Default deny policy with explicit allows
- Established connections properly allowed
- Internal Docker network connectivity maintained

---

## 3. Docker Security

### 3.1 Port Binding Configuration

All services use default port binding in docker-compose.yml:
```yaml
archon-server:
  ports:
    - "${ARCHON_SERVER_PORT:-8181}:8181"

archon-mcp:
  ports:
    - "${ARCHON_MCP_PORT:-8051}:8051"

archon-ui:
  ports:
    - "${ARCHON_UI_PORT:-3737}:3737"

Supabase services:
  - "54321:8000"  (Kong)
  - "54322:5432"  (PostgreSQL)
  - "54323:3000"  (Studio)
  - "54324:8025"  (Inbucket)
  - "54327:4000"  (Analytics)
```

**Status**: ⚠️ MEDIUM - Could be improved
- Current: `"8181:8181"` binds to 0.0.0.0 (all interfaces)
- Best practice: `"127.0.0.1:8181:8181"` (localhost only)
- Mitigated by iptables rules, but defense in depth suggests explicit localhost binding

### 3.2 Docker Networks

```
archon_app-network        - Bridge network for Archon services
supabase_network_archon   - Bridge network for Supabase services
```

**Status**: ✅ GOOD
- Services are properly isolated in separate bridge networks
- Internal service communication is possible within networks

### 3.3 Container Port Mappings

Internal services (not exposed externally):
```
supabase_pg_meta_archon:       8080/tcp  (internal only)
supabase_edge_runtime_archon:  8081/tcp  (internal only)
supabase_storage_archon:       5000/tcp  (internal only)
supabase_rest_archon:          3000/tcp  (internal only)
supabase_realtime_archon:      4000/tcp  (internal only)
supabase_auth_archon:          9999/tcp  (internal only)
supabase_kong_archon:          8001/tcp, 8088/tcp, 8443-8444/tcp (internal)
```

**Status**: ✅ EXCELLENT
- Most Supabase microservices are not exposed to host
- Only Kong gateway is exposed as single entry point
- Follows microservices security best practices

---

## 4. Nginx Security

### 4.1 TLS/SSL Configuration

**Main Domain (archon.nexorithm.io)**:
```
Status: HTTP only (port 80)
- Behind Cloudflare proxy
- Cloudflare handles SSL termination
- X-Forwarded-Proto header trusted from Cloudflare
```

**Subdomain (supabase.archon.nexorithm.io)**:
```
SSL Certificate: Let's Encrypt
ssl_protocols: TLSv1.2 TLSv1.3
ssl_ciphers: Modern ECDHE ciphers
ssl_prefer_server_ciphers: off
ssl_session_timeout: 1d
ssl_session_cache: shared:SSL:50m
ssl_session_tickets: off
```

**Status**: ✅ EXCELLENT (subdomain) / ✅ ACCEPTABLE (main domain)
- Subdomain has strong TLS 1.2+ only configuration
- Modern cipher suite (no weak ciphers)
- TLS 1.0/1.1 connection test failed (expected - these are disabled)
- Main domain relies on Cloudflare for SSL (common pattern)

### 4.2 Security Headers

**Implemented Headers**:
```
X-Frame-Options: SAMEORIGIN                      ✅
X-Content-Type-Options: nosniff                  ✅
X-XSS-Protection: 1; mode=block                  ✅
Referrer-Policy: no-referrer-when-downgrade      ✅
```

**Missing Headers**:
```
Strict-Transport-Security (HSTS)                 ❌ HIGH
Content-Security-Policy (CSP)                    ❌ MEDIUM
Permissions-Policy                               ❌ LOW
```

**Status**: ⚠️ HIGH - Missing critical HSTS header
- Basic security headers are present
- Missing HSTS exposes users to SSL stripping attacks
- Missing CSP increases XSS attack surface

### 4.3 Rate Limiting

**Status**: ❌ MEDIUM - No rate limiting configured
- No `limit_req_zone` or `limit_conn_zone` directives found
- API endpoints are vulnerable to brute force attacks
- Recommendation: Implement rate limiting on /api/ endpoints

### 4.4 Server Information Disclosure

```
server_tokens: off (commented out in nginx.conf)
```

**Status**: ⚠️ LOW
- Server tokens should be explicitly disabled
- Currently relying on default (may expose Nginx version)

### 4.5 Authentication

**Supabase Studio (/db/)**:
```
auth_basic: "Supabase Studio Access"
auth_basic_user_file: /etc/nginx/.htpasswd-supabase
Status: ✅ Configured and active
```

**Status**: ✅ EXCELLENT
- HTTP Basic Auth protects Supabase Studio
- Additional layer of defense for database management interface

### 4.6 Proxy Configuration

**Strengths**:
- Proper timeout configuration (300s read, 75s connect)
- X-Real-IP and X-Forwarded-For headers set correctly
- HTTP/1.1 with Connection upgrade for WebSockets
- Keepalive configured for Vite dev server (fixes 502 errors)

**Status**: ✅ EXCELLENT

---

## 5. Critical Findings Summary

### 5.1 CRITICAL Issues (Immediate Action Required)

**NONE** - No critical vulnerabilities found

### 5.2 HIGH Priority Issues

1. **Missing HSTS Header**
   - Risk: Users vulnerable to SSL stripping attacks
   - Impact: High - affects all HTTPS connections
   - Recommendation: Add HSTS header with long max-age

### 5.3 MEDIUM Priority Issues

1. **No Rate Limiting**
   - Risk: Brute force attacks on API endpoints
   - Impact: Medium - could lead to resource exhaustion
   - Recommendation: Implement rate limiting

2. **Docker Port Binding to 0.0.0.0**
   - Risk: Relies solely on iptables for protection
   - Impact: Medium - defense in depth concern
   - Recommendation: Bind to 127.0.0.1 where possible

3. **Missing Content-Security-Policy**
   - Risk: Increased XSS attack surface
   - Impact: Medium - depends on application code
   - Recommendation: Implement strict CSP

### 5.4 LOW Priority Issues

1. **Server Tokens Not Disabled**
   - Risk: Information disclosure
   - Impact: Low - minor security hygiene
   - Recommendation: Uncomment `server_tokens off;`

---

## 6. Recommendations

### 6.1 Immediate Actions (High Priority)

#### Add HSTS Header
```nginx
# In both server blocks
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
```

#### Implement Rate Limiting
```nginx
# In http block of nginx.conf
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/m;

# In server block
location /api/ {
    limit_req zone=api_limit burst=20 nodelay;
    # ... existing proxy config
}

location /api/auth/ {
    limit_req zone=auth_limit burst=5 nodelay;
    # ... existing proxy config
}
```

### 6.2 Short-term Improvements (Medium Priority)

#### Bind Docker Ports to Localhost
Update docker-compose.yml:
```yaml
services:
  archon-server:
    ports:
      - "127.0.0.1:${ARCHON_SERVER_PORT:-8181}:8181"

  archon-mcp:
    ports:
      - "127.0.0.1:${ARCHON_MCP_PORT:-8051}:8051"

  archon-ui:
    ports:
      - "127.0.0.1:${ARCHON_UI_PORT:-3737}:3737"

  # Supabase services
  supabase_kong:
    ports:
      - "127.0.0.1:54321:8000"

  supabase_db:
    ports:
      - "127.0.0.1:54322:5432"
```

**Note**: After this change, iptables DOCKER-USER rules can be removed since ports won't be accessible from eth0.

#### Add Content-Security-Policy
```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://supabase.archon.nexorithm.io;" always;
```

**Note**: CSP requires testing with your application to avoid breaking functionality.

#### Disable Server Tokens
```nginx
# Uncomment in nginx.conf
server_tokens off;
```

### 6.3 Long-term Enhancements (Low Priority)

1. **Implement Fail2ban**
   - Protect SSH from brute force attacks
   - Monitor Nginx logs for suspicious activity

2. **Add Permissions-Policy Header**
   ```nginx
   add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
   ```

3. **Consider WAF Integration**
   - ModSecurity or similar for application-layer protection
   - May be overkill for current deployment scale

4. **Regular Security Audits**
   - Run automated security scans (nmap, nikto)
   - Review logs for suspicious activity
   - Keep Docker images and Nginx updated

---

## 7. Compliance Status

### 7.1 OWASP Top 10 Considerations

1. **A01:2021 - Broken Access Control**: ✅ GOOD
   - Authentication on admin interfaces
   - Database not directly accessible

2. **A02:2021 - Cryptographic Failures**: ✅ GOOD
   - Strong TLS configuration
   - Modern ciphers only

3. **A03:2021 - Injection**: ⚠️ Depends on application code
   - Not auditable at infrastructure level

4. **A05:2021 - Security Misconfiguration**: ⚠️ MEDIUM
   - Missing some security headers
   - Server tokens potentially exposed

5. **A07:2021 - Identification and Authentication Failures**: ✅ GOOD
   - Basic auth on admin interfaces
   - No rate limiting (concern)

### 7.2 CIS Docker Benchmark

- ✅ Ports properly firewalled
- ✅ Services in isolated networks
- ⚠️ Ports bound to 0.0.0.0 (should be 127.0.0.1)
- ✅ No privileged containers detected

---

## 8. Testing Validation

### 8.1 Port Security Tests

```bash
# External port scan confirmed filtering
nmap -sT -p 3737,8181,8051,54321-54324,54327 91.98.156.158
Result: All ports filtered ✅

# PostgreSQL connection attempt from external
Result: 30 packets dropped by iptables ✅

# Internal connectivity
Result: Services can communicate within Docker networks ✅
```

### 8.2 SSL/TLS Tests

```bash
# TLS 1.0/1.1 connection attempt
openssl s_client -connect supabase.archon.nexorithm.io:443 -tls1_1
Result: Connection failed (expected) ✅

# TLS 1.2+ connection
Result: Success with strong ciphers ✅
```

### 8.3 Security Headers Tests

```bash
curl -I https://supabase.archon.nexorithm.io
Result: Basic headers present, HSTS missing ⚠️
```

---

## 9. Deployment Architecture

```
Internet
    |
    v
[Cloudflare Proxy] (SSL termination for main domain)
    |
    v
[Server: 91.98.156.158]
    |
    +-- [Nginx] (Port 80/443)
    |     |
    |     +-- / -> 127.0.0.1:3737 (Archon UI)
    |     +-- /api/ -> 127.0.0.1:8181 (Archon API)
    |     +-- /mcp/ -> 127.0.0.1:8051 (Archon MCP)
    |     +-- /db/ -> 127.0.0.1:54323 (Supabase Studio) [Basic Auth]
    |     +-- https://supabase.* -> 127.0.0.1:54321 (Kong Gateway)
    |
    +-- [iptables DOCKER-USER]
    |     |
    |     +-- DROP external access to all application ports
    |     +-- ALLOW loopback
    |     +-- ALLOW established connections
    |
    +-- [Docker]
          |
          +-- [archon_app-network]
          |     +-- archon-ui (3737)
          |     +-- archon-server (8181)
          |     +-- archon-mcp (8051)
          |
          +-- [supabase_network_archon]
                +-- Kong Gateway (54321)
                +-- PostgreSQL (54322)
                +-- Studio (54323)
                +-- Auth, Storage, Realtime, etc. (internal only)
```

---

## 10. Conclusion

The Archon infrastructure deployment demonstrates **good security practices** with a robust firewall configuration that effectively protects critical services. The iptables DOCKER-USER chain successfully blocks all external access to application and database ports.

**Overall Security Rating: B+ (Good)**

**Strengths**:
- Excellent firewall configuration
- Strong TLS setup on subdomain
- Proper service isolation
- Basic authentication on admin interfaces
- No critical vulnerabilities

**Areas for Improvement**:
- Add HSTS header (HIGH)
- Implement rate limiting (MEDIUM)
- Bind Docker ports to localhost (MEDIUM)
- Add missing security headers (MEDIUM)

The infrastructure is production-ready with the current configuration. Implementing the HIGH priority recommendations would elevate the security posture to excellent (A rating).

---

**Audit Completed**: 2025-10-15 12:34:00 CEST
**Auditor**: Claude Code Infrastructure Security Audit
**Next Review Date**: 2025-11-15
