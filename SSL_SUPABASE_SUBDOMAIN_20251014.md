# SSL Certificate Implementation for Supabase Subdomain

**Date**: 2025-10-14 22:20 UTC
**Server**: netzwaechter (91.98.156.158)
**Domain**: supabase.archon.nexorithm.io
**Status**: ✅ COMPLETED AND OPERATIONAL

---

## Problem

Cloudflare SSL certificate did not cover the subdomain `supabase.archon.nexorithm.io`, causing SSL handshake failures:

```
curl: (35) OpenSSL/3.0.13: error:0A000410:SSL routines::sslv3 alert handshake failure
```

**Error in Cloudflare**: "Dieser Hostname wird nicht von einem Zertifikat abgedeckt" (This hostname is not covered by a certificate)

---

## Solution Implemented

Implemented **Let's Encrypt SSL certificate** directly on nginx, bypassing Cloudflare SSL limitations.

### Approach Chosen

**Option**: Disable Cloudflare Proxy + Use Let's Encrypt on Nginx

**Why This Approach**:
- No cost (free Let's Encrypt certificate)
- Full control over SSL configuration
- Auto-renewal built-in via certbot
- No dependency on Cloudflare paid features

---

## Implementation Steps

### 1. Disabled Cloudflare Proxy

Changed DNS record in Cloudflare:
- Record: `supabase.archon.nexorithm.io`
- Type: A
- Value: `91.98.156.158`
- Proxy status: DNS-only (grey cloud) ← Changed from proxied (orange cloud)

### 2. Installed Certbot

```bash
apt update && apt install -y certbot python3-certbot-nginx
```

**Status**: Already installed on server

### 3. Obtained SSL Certificate

```bash
certbot certonly --nginx --non-interactive --agree-tos \
  --email admin@nexorithm.io \
  -d supabase.archon.nexorithm.io
```

**Result**:
- Certificate: `/etc/letsencrypt/live/supabase.archon.nexorithm.io/fullchain.pem`
- Private Key: `/etc/letsencrypt/live/supabase.archon.nexorithm.io/privkey.pem`
- Expiry: 2026-01-12 (90 days from issue)
- Auto-renewal: Enabled via certbot systemd timer

### 4. Updated Nginx Configuration

**File**: `/etc/nginx/sites-available/archon`

**Changes**:
1. HTTP server block (port 80) - Redirect to HTTPS:
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name supabase.archon.nexorithm.io;

    # Redirect all HTTP to HTTPS
    return 301 https://$host$request_uri;
}
```

2. HTTPS server block (port 443) - SSL configuration:
```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name supabase.archon.nexorithm.io;

    # SSL certificate from Let's Encrypt
    ssl_certificate /etc/letsencrypt/live/supabase.archon.nexorithm.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/supabase.archon.nexorithm.io/privkey.pem;

    # SSL configuration - Mozilla Intermediate profile
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Proxy to Supabase API (port 54321)
    location / {
        proxy_pass http://127.0.0.1:54321;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
}
```

**Backup Created**: `/etc/nginx/sites-available/archon.backup-before-ssl`

### 5. Reloaded Nginx

```bash
nginx -t  # Test configuration
systemctl reload nginx  # Apply changes
```

**Result**: Configuration valid, nginx reloaded successfully

---

## Verification Results

### ✅ HTTPS Access

```bash
curl -I https://supabase.archon.nexorithm.io/rest/v1/
# HTTP/2 200
# server: nginx/1.24.0 (Ubuntu)
# ✅ Working perfectly
```

### ✅ HTTP Redirect

```bash
curl -I http://supabase.archon.nexorithm.io
# HTTP/1.1 301 Moved Permanently
# Location: https://supabase.archon.nexorithm.io/
# ✅ Redirects correctly
```

### ✅ SSL Certificate Valid

```bash
openssl s_client -servername supabase.archon.nexorithm.io -connect localhost:443
# Certificate:
#   Subject: CN = supabase.archon.nexorithm.io
#   Issuer: C = US, O = Let's Encrypt, CN = E8
#   Valid from: Oct 14 19:19:08 2025 GMT
#   Valid until: Jan 12 19:19:07 2026 GMT
# ✅ Valid Let's Encrypt certificate
```

---

## Certificate Auto-Renewal

### Certbot Timer

Certbot automatically installs a systemd timer for certificate renewal:

```bash
systemctl list-timers | grep certbot
# certbot.timer will run renewal twice daily
```

### Manual Renewal (if needed)

```bash
certbot renew --dry-run  # Test renewal
certbot renew            # Force renewal
```

### Renewal Process

1. Certbot checks certificates twice daily
2. Renews certificates 30 days before expiry
3. Automatically reloads nginx after renewal
4. No manual intervention required

---

## Cloudflare Configuration

### DNS Record

**Current Configuration**:
- Name: `supabase.archon.nexorithm.io`
- Type: A
- Value: `91.98.156.158`
- TTL: Auto
- Proxy status: DNS-only (grey cloud) ✅

**Important**: Must remain in DNS-only mode for Let's Encrypt to work

### Main Domain (archon.nexorithm.io)

**Still proxied through Cloudflare**:
- Proxy status: Proxied (orange cloud) ✅
- Cloudflare handles SSL for main domain
- nginx handles SSL for supabase subdomain

---

## Service Endpoints Status

| Endpoint | SSL Provider | Status |
|----------|--------------|--------|
| `https://archon.nexorithm.io` | Cloudflare | ✅ Working |
| `https://archon.nexorithm.io/api` | Cloudflare | ✅ Working |
| `https://archon.nexorithm.io/mcp` | Cloudflare | ✅ Working |
| `https://archon.nexorithm.io/db` | Cloudflare | ✅ Working |
| `https://supabase.archon.nexorithm.io` | Let's Encrypt | ✅ Working |

---

## Security Considerations

### SSL Configuration

- **Protocols**: TLS 1.2 and 1.3 only
- **Ciphers**: Modern secure ciphers (ECDHE-ECDSA, ECDHE-RSA)
- **Session**: 1-day timeout, 50MB cache
- **HSTS**: Not enabled (optional, can be added)

### Headers

All security headers applied:
- `X-Frame-Options: SAMEORIGIN`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: no-referrer-when-downgrade`

### Access

- **Supabase API** (port 54321): Direct access via subdomain
- **Supabase Studio** (port 54323): Still protected via `/db/` path with basic auth

---

## Files Modified

### Nginx Configuration

**File**: `/etc/nginx/sites-available/archon`
**Backup**: `/etc/nginx/sites-available/archon.backup-before-ssl`
**Changes**:
- Added HTTPS server block for subdomain
- Updated HTTP block to redirect to HTTPS
- Configured SSL certificates and security settings

### Let's Encrypt Certificates

**Location**: `/etc/letsencrypt/live/supabase.archon.nexorithm.io/`
**Files**:
- `fullchain.pem` - Full certificate chain
- `privkey.pem` - Private key
- `cert.pem` - Certificate only
- `chain.pem` - Intermediate certificates

---

## Troubleshooting

### If SSL Certificate Expires

```bash
# Check certificate status
certbot certificates

# Renew manually
certbot renew

# Reload nginx
systemctl reload nginx
```

### If HTTPS Stops Working

1. Check certificate validity:
```bash
openssl x509 -in /etc/letsencrypt/live/supabase.archon.nexorithm.io/fullchain.pem -noout -dates
```

2. Check nginx configuration:
```bash
nginx -t
```

3. Check nginx logs:
```bash
tail -f /var/log/nginx/supabase-archon-ssl-error.log
```

### If Renewal Fails

**Common cause**: Cloudflare proxy re-enabled

**Solution**: Ensure DNS record is in DNS-only mode (grey cloud)

---

## Rollback Instructions

If you need to revert to Cloudflare SSL:

1. **Enable Cloudflare Proxy**:
   - Go to Cloudflare DNS settings
   - Change `supabase.archon.nexorithm.io` to proxied (orange cloud)

2. **Restore Old Nginx Config**:
```bash
cp /etc/nginx/sites-available/archon.backup-before-ssl /etc/nginx/sites-available/archon
systemctl reload nginx
```

3. **Remove HTTPS Server Block**:
   - Keep only HTTP server block with Cloudflare X-Forwarded-Proto support

---

## Future Maintenance

### Certificate Renewal

- **Automatic**: Certbot timer handles renewal
- **Check**: `certbot certificates` to see expiry dates
- **Monitor**: Set up alerts 14 days before expiry

### Monitoring Recommendations

1. **SSL Certificate Expiry**: Monitor via Uptime Robot or similar
2. **HTTPS Availability**: Check endpoint every 5 minutes
3. **Nginx Logs**: Set up log rotation and alerts

### Optional Improvements

1. **HSTS Header**: Add if you want to enforce HTTPS permanently
2. **OCSP Stapling**: Improve SSL performance
3. **Rate Limiting**: Protect against abuse
4. **IP Whitelisting**: Restrict access to known IPs

---

## Summary

**Problem Solved**: ✅ SSL handshake failure on `supabase.archon.nexorithm.io`

**Solution Applied**: Let's Encrypt SSL certificate with nginx

**Results**:
- ✅ HTTPS working perfectly
- ✅ HTTP redirects to HTTPS
- ✅ Valid SSL certificate (90-day validity)
- ✅ Auto-renewal configured
- ✅ Security headers applied
- ✅ Zero cost solution

**Completion Time**: ~20 minutes
**Downtime**: None (services continued on main domain)

**Status**: PRODUCTION READY ✅

---

**Created**: 2025-10-14 22:20 UTC
**Server**: netzwaechter (91.98.156.158)
**Engineer**: Claude Code
**Project**: Archon Knowledge Base System
