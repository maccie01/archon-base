# Arcane Cloudflare DNS Configuration

Date: 2025-10-15
Domain: arcane.nexorithm.io
Server: 91.98.156.158

---

## Required DNS Configuration

### A Record for arcane.nexorithm.io

Log in to Cloudflare dashboard and add the following DNS record:

**Type**: A
**Name**: arcane
**IPv4 address**: 91.98.156.158
**Proxy status**: Proxied (orange cloud icon)
**TTL**: Auto

### Configuration Steps

1. Go to https://dash.cloudflare.com
2. Select the `nexorithm.io` domain
3. Navigate to **DNS** → **Records**
4. Click **Add record**
5. Fill in the details:
   - **Type**: A
   - **Name**: arcane
   - **IPv4 address**: 91.98.156.158
   - **Proxy status**: ✅ Proxied (click the cloud icon to make it orange)
   - **TTL**: Auto
6. Click **Save**

### Verify DNS Propagation

After adding the record, wait 1-5 minutes and verify:

```bash
# Check DNS resolution
dig arcane.nexorithm.io

# Should show Cloudflare IP addresses (proxied)
# Example output:
# arcane.nexorithm.io.  300  IN  A  104.21.x.x
# arcane.nexorithm.io.  300  IN  A  172.67.x.x
```

---

## Cloudflare SSL/TLS Settings

### SSL/TLS Encryption Mode

**Navigate to**: SSL/TLS → Overview

**Setting**: Full (strict)
**Why**: Encrypts traffic between Cloudflare and origin server with valid certificate

### Edge Certificates

**Navigate to**: SSL/TLS → Edge Certificates

**Settings to Enable**:
- ✅ Always Use HTTPS: ON
- ✅ HTTP Strict Transport Security (HSTS): Enable (if not already enabled)
  - Max Age: 12 months (31536000 seconds)
  - Include subdomains: ON
  - Preload: ON
- ✅ Minimum TLS Version: TLS 1.2
- ✅ Opportunistic Encryption: ON
- ✅ TLS 1.3: ON
- ✅ Automatic HTTPS Rewrites: ON

---

## Cloudflare Firewall Rules (Optional but Recommended)

### Navigate to: Security → WAF

**Recommended Rules**:

1. **Block non-HTTPS**: Already handled by "Always Use HTTPS"
2. **Rate Limiting**: Already handled by Nginx (30 req/min per IP)
3. **Country Restrictions** (optional): Block specific countries if needed

---

## Cloudflare Page Rules (Optional)

### Navigate to: Rules → Page Rules

**Optional Rule for Enhanced Security**:

**URL Pattern**: `arcane.nexorithm.io/*`
**Settings**:
- Security Level: High
- Cache Level: Bypass (Arcane is dynamic application)

---

## Verification After DNS Setup

Once DNS is configured, test the following:

### 1. DNS Resolution
```bash
dig arcane.nexorithm.io +short
```
Should return Cloudflare IP addresses.

### 2. HTTPS Access
```bash
curl -I https://arcane.nexorithm.io
```
Should return:
- `HTTP/1.1 200 OK` or `HTTP/2 200`
- `Strict-Transport-Security` header
- `X-Frame-Options` header
- `X-Content-Type-Options` header

### 3. HTTP to HTTPS Redirect
```bash
curl -I http://arcane.nexorithm.io
```
Should redirect to https:// (301 or 302).

### 4. Access from Browser
```
https://arcane.nexorithm.io
```
Should load Arcane interface with valid HTTPS certificate.

---

## Security Headers Verification

Expected headers (check via browser DevTools or curl):

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Referrer-Policy: no-referrer-when-downgrade
Content-Security-Policy: default-src 'self'; ...
```

---

## Troubleshooting

### DNS Not Resolving

**Issue**: `dig arcane.nexorithm.io` returns NXDOMAIN

**Solutions**:
1. Wait 5 minutes for DNS propagation
2. Verify A record was created correctly in Cloudflare
3. Check domain is active in Cloudflare
4. Clear local DNS cache: `sudo dscacheutil -flushcache` (macOS)

### 502 Bad Gateway

**Issue**: Cloudflare shows 502 error

**Solutions**:
1. Check Arcane container is running: `docker ps | grep arcane`
2. Check Nginx is running: `systemctl status nginx`
3. Check Nginx proxy_pass points to correct port (127.0.0.1:3552)
4. Check Arcane logs: `docker logs arcane`

### SSL Certificate Error

**Issue**: Browser shows SSL certificate warning

**Solutions**:
1. Verify SSL/TLS mode is "Full (strict)" in Cloudflare
2. Wait 5 minutes for Cloudflare SSL provisioning
3. Check "Always Use HTTPS" is enabled
4. Verify Nginx is serving on port 80 (Cloudflare connects to origin via HTTP, then encrypts)

### Connection Timeout

**Issue**: Request times out

**Solutions**:
1. Verify firewall allows port 80 on server
2. Check Nginx error logs: `tail -f /var/log/nginx/arcane-error.log`
3. Verify Cloudflare proxy is enabled (orange cloud)
4. Check server IP is correct: 91.98.156.158

---

## Current Configuration Summary

**Server**: 91.98.156.158
**Domain**: arcane.nexorithm.io
**Container**: arcane (port 3552)
**Nginx**: Reverse proxy on port 80 → 127.0.0.1:3552
**Cloudflare**: Proxied (SSL termination)
**Rate Limiting**: 30 requests/minute per IP
**SSL**: Full (strict) with HSTS enabled

---

**Created**: 2025-10-15
**Status**: Waiting for DNS configuration
