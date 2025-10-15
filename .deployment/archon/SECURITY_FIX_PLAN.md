# Security Fix Implementation Plan

**Created**: 2025-10-15
**Priority**: CRITICAL - Must be deployed immediately

---

## Executive Summary

Security audits revealed **11 CRITICAL** authentication gaps and exposed ports that must be fixed before production use:

### Critical Issues Found:
1. **API Endpoints**: 89+ endpoints missing authentication
2. **Exposed Ports**: 5 Supabase ports accessible from internet
3. **Nginx Security**: Missing rate limiting and security headers

---

## Part 1: Fix Authentication on API Endpoints

### Files to Modify

#### 1. knowledge_api.py (CRITICAL - 14 endpoints)

**Lines to modify**:
- Line 233: `GET /api/knowledge-items/sources`
- Line 245: `GET /api/knowledge-items`
- Line 288: `GET /api/knowledge-items/summary`
- Line 319: `GET /api/knowledge-items/{source_id}`
- Line 420: `GET /api/knowledge-items/{source_id}/chunks`
- Line 579: `GET /api/knowledge-items/{source_id}/code-examples`
- Line 1153: `POST /api/knowledge-items/search`
- Line 1167: `POST /api/rag/query`
- Line 1204: `POST /api/rag/code-examples`
- Line 1240: `POST /api/code-examples`
- Line 1247: `GET /api/rag/sources`
- Line 1300: `GET /api/database/metrics`
- Line 190: `GET /api/crawl-progress/{progress_id}` (review needed)

**Change Pattern**:
```python
# BEFORE (vulnerable)
@router.get("/knowledge-items/summary")
async def get_knowledge_items_summary(
    page: int = 1, per_page: int = 20
):

# AFTER (secure)
@router.get("/knowledge-items/summary")
async def get_knowledge_items_summary(
    page: int = 1, per_page: int = 20,
    auth = Depends(require_auth)  # ADD THIS LINE
):
```

#### 2. settings_api.py (CRITICAL - 8 endpoints)

**Lines to modify**:
- Line 46: `GET /api/credentials`
- Line 78: `GET /api/credentials/categories/{category}`
- Line 142: `GET /api/credentials/{key}`
- Line 267: `POST /api/credentials/initialize` (DANGEROUS - returns decrypted values)
- Line 282: `GET /api/database/metrics`
- Line 347: `POST /api/credentials/status-check` (CRITICAL - returns decrypted API keys!)

**Add**: `auth = Depends(require_auth)` to all functions

#### 3. projects_api.py (CRITICAL - 18+ endpoints)

**All project CRUD endpoints need auth**:
- Line 79: `GET /api/projects`
- Line 163: `POST /api/projects`
- Line 339: `GET /api/projects/{project_id}`
- Line 379: `PUT /api/projects/{project_id}`
- Line 490: `DELETE /api/projects/{project_id}`
- All task endpoints (lines 658-916)
- All document endpoints (lines 957-1128)
- All version endpoints (lines 1134-1279)

**Add**: `auth = Depends(require_auth)` to all functions

#### 4. mcp_api.py (HIGH - 5 endpoints)

**Lines to modify**:
- Line 78: `GET /api/mcp/status`
- Line 97: `GET /api/mcp/config`
- Line 142: `GET /api/mcp/clients`
- Line 168: `GET /api/mcp/sessions`

**Add**: `auth = Depends(require_auth)` to all functions

#### 5. ollama_api.py (MEDIUM - 10 endpoints)

**Lines to modify**:
- Line 83: `GET /api/ollama/models`
- Line 142: `GET /api/ollama/instances/health`
- Line 207: `POST /api/ollama/validate`
- Line 257: `POST /api/ollama/embedding/route`
- Line 294: `GET /api/ollama/embedding/routes`
- Line 350: `DELETE /api/ollama/cache` (Can clear caches!)
- Line 411: `POST /api/ollama/models/discover-and-store`
- Line 499: `GET /api/ollama/models/stored`
- Line 957: `POST /api/ollama/models/discover-with-details`
- Line 1231: `POST /api/ollama/models/test-capabilities`

**Add**: `auth = Depends(require_auth)` to all functions

#### 6. Other Files (Review and Fix)

- `knowledge_folders_api.py`: All 5 endpoints
- `knowledge_tags_api.py`: All 4 endpoints
- `pages_api.py`: All 3 endpoints
- `providers_api.py`: Line 99
- `progress_api.py`: Lines 22, 100
- `agent_chat_api.py`: All 4 endpoints
- `migration_api.py`: All 3 endpoints (expose schema info!)
- `bug_report_api.py`: All 2 endpoints

---

## Part 2: Block Exposed Supabase Ports

### Immediate Action: iptables Rules

```bash
ssh -i ~/.ssh/netzwaechter_deployment root@91.98.156.158

# Block Supabase ports from external access
iptables -I DOCKER-USER -i eth0 -p tcp --dport 54321 -j DROP
iptables -I DOCKER-USER -i eth0 -p tcp --dport 54322 -j DROP
iptables -I DOCKER-USER -i eth0 -p tcp --dport 54323 -j DROP
iptables -I DOCKER-USER -i eth0 -p tcp --dport 54324 -j DROP
iptables -I DOCKER-USER -i eth0 -p tcp --dport 54327 -j DROP

# Save rules
iptables-save > /etc/iptables/rules.v4

# Verify blocked
iptables -L DOCKER-USER -n -v | grep 543
```

### Permanent Fix: Update docker-compose.yml

Find Supabase services and change port bindings:

```yaml
# BEFORE (exposed)
ports:
  - "0.0.0.0:54321:8000"

# AFTER (localhost only)
ports:
  - "127.0.0.1:54321:8000"
```

Apply to all Supabase services (54321-54324, 54327).

---

## Part 3: Nginx Security Hardening

### File: /etc/nginx/nginx.conf

```nginx
http {
    # Hide server version
    server_tokens off;

    # Request size limits
    client_body_buffer_size 1k;
    client_header_buffer_size 1k;
    client_max_body_size 10M;
    large_client_header_buffers 2 1k;

    # Timeouts
    client_body_timeout 12s;
    client_header_timeout 12s;
    keepalive_timeout 15s;
    send_timeout 10s;

    # Rate limiting zones
    limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=api:10m rate=30r/m;
    limit_req_zone $binary_remote_addr zone=auth:10m rate=5r/m;
    limit_conn_zone $binary_remote_addr zone=conn_limit:10m;
    limit_conn conn_limit 10;

    # SSL/TLS - Only TLS 1.2 and 1.3
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
}
```

### File: /etc/nginx/sites-enabled/archon

Add to HTTPS server block:

```nginx
# Security headers
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

# Rate limiting
location / {
    limit_req zone=general burst=20 nodelay;
    # ... existing config
}

location /api/ {
    limit_req zone=api burst=5 nodelay;
    # ... existing config
}

location /db/ {
    limit_req zone=auth burst=3 nodelay;
    # ... existing config
}
```

---

## Implementation Steps

### Step 1: Fix Authentication (CODE CHANGES)

**Estimated Time**: 2-3 hours

1. **Backup current code**:
   ```bash
   cd /Users/janschubert/tools/archon
   git checkout -b security-fix-authentication
   ```

2. **Apply authentication fixes** to all vulnerable endpoints

3. **Test locally**:
   ```bash
   # Start services
   docker compose up -d

   # Test without auth (should fail)
   curl http://localhost:8181/api/knowledge-items/summary
   # Expected: 401 Unauthorized

   # Test with auth (should succeed)
   curl -H "Authorization: Bearer ak_597A..." \
     http://localhost:8181/api/knowledge-items/summary
   # Expected: 200 OK with data
   ```

4. **Commit and push**:
   ```bash
   git add python/src/server/api_routes/
   git commit -m "fix(security): add authentication to all sensitive API endpoints"
   git push origin security-fix-authentication
   ```

### Step 2: Block Exposed Ports (INFRASTRUCTURE)

**Estimated Time**: 30 minutes

1. **Apply iptables rules** (see Part 2)

2. **Update docker-compose** for Supabase services

3. **Restart services**:
   ```bash
   cd /opt/archon
   docker compose down
   docker compose up -d
   ```

4. **Verify**:
   ```bash
   # From external machine
   nmap -p 54321-54327 91.98.156.158
   # Expected: All ports filtered/closed
   ```

### Step 3: Nginx Security Hardening (INFRASTRUCTURE)

**Estimated Time**: 1 hour

1. **Backup current config**:
   ```bash
   cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup
   cp /etc/nginx/sites-enabled/archon /etc/nginx/sites-enabled/archon.backup
   ```

2. **Apply security changes** (see Part 3)

3. **Test configuration**:
   ```bash
   nginx -t
   ```

4. **Reload Nginx**:
   ```bash
   systemctl reload nginx
   ```

5. **Verify**:
   ```bash
   curl -I https://archon.nexorithm.io | grep -i "strict-transport"
   # Expected: Strict-Transport-Security header present
   ```

### Step 4: Deploy to Production

**Estimated Time**: 30 minutes

1. **Merge security fixes**:
   ```bash
   cd /Users/janschubert/tools/archon
   git checkout stable
   git merge security-fix-authentication
   git push origin stable
   ```

2. **Deploy on server**:
   ```bash
   ssh -i ~/.ssh/netzwaechter_deployment root@91.98.156.158
   cd /opt/archon
   git pull origin stable
   docker compose build
   docker compose up -d
   ```

3. **Verify all fixes**:
   - Test authentication on all endpoints
   - Verify ports are blocked
   - Check Nginx security headers

---

## Testing Checklist

### Authentication Testing

```bash
# Test knowledge endpoints (should require auth)
curl http://91.98.156.158:8181/api/knowledge-items/summary
# Expected: 401 Unauthorized

curl -H "Authorization: Bearer ak_597A..." \
  http://91.98.156.158:8181/api/knowledge-items/summary
# Expected: 200 OK

# Test settings endpoints (should require auth)
curl http://91.98.156.158:8181/api/credentials
# Expected: 401 Unauthorized

curl -H "Authorization: Bearer ak_597A..." \
  http://91.98.156.158:8181/api/credentials
# Expected: 200 OK

# Test projects endpoints (should require auth)
curl http://91.98.156.158:8181/api/projects
# Expected: 401 Unauthorized

curl -H "Authorization: Bearer ak_597A..." \
  http://91.98.156.158:8181/api/projects
# Expected: 200 OK
```

### Port Security Testing

```bash
# From external machine (should all be blocked/filtered)
nmap -sS -p 3737,8181,8051,54321-54324,54327 91.98.156.158
# Expected: All ports filtered or closed (not open)

# Only these should be open:
# 22 (SSH), 80 (HTTP), 443 (HTTPS)
```

### Nginx Security Testing

```bash
# Test security headers
curl -I https://archon.nexorithm.io

# Should see:
# Strict-Transport-Security: max-age=31536000...
# Content-Security-Policy: ...
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff

# Test rate limiting
for i in {1..50}; do curl -I https://archon.nexorithm.io/api/ 2>&1 | grep "HTTP/"; done
# Should see: 429 Too Many Requests after ~30 requests

# Test server version hidden
curl -I https://archon.nexorithm.io | grep -i server
# Should NOT show version number
```

---

## Rollback Plan

If issues occur after deployment:

```bash
# Rollback code
cd /opt/archon
git reset --hard HEAD~1
docker compose build
docker compose up -d

# Rollback iptables
iptables -D DOCKER-USER -i eth0 -p tcp --dport 54321 -j DROP
# Repeat for other ports

# Rollback Nginx
cp /etc/nginx/nginx.conf.backup /etc/nginx/nginx.conf
cp /etc/nginx/sites-enabled/archon.backup /etc/nginx/sites-enabled/archon
systemctl reload nginx
```

---

## Success Criteria

- [ ] All API endpoints require authentication
- [ ] Supabase ports blocked from external access
- [ ] Nginx security headers present
- [ ] Rate limiting functional
- [ ] Server version hidden
- [ ] No unauthorized data access possible
- [ ] All tests passing

---

**Estimated Total Time**: 4-5 hours
**Risk Level**: CRITICAL - Must be completed immediately
**Impact**: HIGH - Prevents data breaches and unauthorized access

**Next Steps**: Use task agents to automatically apply fixes and test
