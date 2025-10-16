# Supabase Domain Configuration Fix Guide

Date: 2025-10-15 19:30 UTC
Server: 91.98.156.158 (netzwaechter-prod)

---

## Current Situation Analysis

### What's Working ✅
- **supabase.archon.nexorithm.io** - Nginx configured, SSL certificate exists, Kong responding (404 is normal)
- Supabase Kong running on **127.0.0.1:54321**
- Nginx proxy properly configured in `/etc/nginx/sites-available/archon`

### What's Broken ❌
1. **supabase.nexorithm.io** - DNS points to wrong server (49.12.201.236 - old server)
2. **Kong 404 error** - "no Route matched" means Supabase API routes not configured yet

### Current DNS Status

```
supabase.nexorithm.io → 49.12.201.236 ❌ (Old server, doesn't exist)
supabase.archon.nexorithm.io → 188.114.97.3 ✅ (Cloudflare, working)
archon.nexorithm.io → 188.114.97.3 ✅ (Cloudflare, working)
```

**Correct server IP:** 91.98.156.158

---

## Part 1: Fix supabase.nexorithm.io DNS (Cloudflare)

### Option A: Point to Cloudflare (Recommended)

**Why?** Your other domains (archon.nexorithm.io, arcane.nexorithm.io) use Cloudflare proxy with benefits:
- DDoS protection
- SSL termination
- CDN caching
- Attack mitigation

**Steps in Cloudflare:**

1. **Log into Cloudflare Dashboard**
   - Go to https://dash.cloudflare.com
   - Select domain: **nexorithm.io**

2. **Navigate to DNS Settings**
   - Click "DNS" in the left sidebar

3. **Find the supabase Record**
   - Look for: `supabase` A record → `49.12.201.236`

4. **Edit the A Record**
   - Click "Edit" on the `supabase` record
   - Change IP: `49.12.201.236` → `91.98.156.158`
   - **Proxy status**: Enable (Orange cloud ☁️) ← IMPORTANT
   - TTL: Auto
   - Click "Save"

5. **Result:**
   ```
   Type: A
   Name: supabase
   IPv4 address: 91.98.156.158
   Proxy status: Proxied (Orange cloud)
   TTL: Auto
   ```

**Wait time:** 1-5 minutes (Cloudflare propagates fast)

---

### Option B: Direct to Server (Not Recommended)

If you don't want Cloudflare proxy:

**Steps in Cloudflare:**
1. Same as Option A, but:
   - **Proxy status**: DNS only (Gray cloud ☁️)

**Cons:**
- No DDoS protection
- No SSL acceleration
- Direct server IP exposed
- Must manage SSL certs on server

---

## Part 2: Create Nginx Configuration (I Will Do This)

### Current Setup

You have **two Supabase access patterns**:

1. **supabase.archon.nexorithm.io** (subdomain)
   - Already configured in `/etc/nginx/sites-available/archon`
   - SSL certificate exists
   - Proxies to 127.0.0.1:54321

2. **supabase.nexorithm.io** (top-level subdomain)
   - NOT configured yet
   - No SSL certificate
   - No Nginx server block

### Decision: Which Domain to Use?

**Option 1: Use supabase.archon.nexorithm.io (Current)**
- ✅ Already working
- ✅ SSL certificate exists
- ✅ Nginx configured
- ⚠️ Longer domain name

**Option 2: Use supabase.nexorithm.io (Shorter)**
- ✅ Shorter, cleaner domain
- ❌ Needs new Nginx config
- ❌ Needs new SSL certificate
- ❌ More DNS records to manage

**Option 3: Use Both (Redirect)**
- supabase.nexorithm.io → redirects to → supabase.archon.nexorithm.io
- ✅ Best of both worlds
- ✅ SEO friendly (301 redirect)

**My Recommendation:** **Option 3** - Use both with redirect

---

## Part 3: Nginx Configuration (I Will Execute)

### Step 1: Create supabase.nexorithm.io Configuration

I will create `/etc/nginx/sites-available/supabase` with:

```nginx
# Supabase Domain Configuration
# Redirects supabase.nexorithm.io → supabase.archon.nexorithm.io

# HTTP: Redirect to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name supabase.nexorithm.io;

    # Redirect to canonical HTTPS domain
    return 301 https://supabase.archon.nexorithm.io$request_uri;
}

# HTTPS: Redirect to canonical domain
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name supabase.nexorithm.io;

    # SSL certificate (will be created by certbot)
    ssl_certificate /etc/letsencrypt/live/supabase.nexorithm.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/supabase.nexorithm.io/privkey.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # Redirect to canonical domain
    return 301 https://supabase.archon.nexorithm.io$request_uri;
}
```

### Step 2: Enable Configuration

```bash
ssh netzwaechter-prod "ln -s /etc/nginx/sites-available/supabase /etc/nginx/sites-enabled/supabase"
ssh netzwaechter-prod "nginx -t"
ssh netzwaechter-prod "systemctl reload nginx"
```

### Step 3: Obtain SSL Certificate

```bash
ssh netzwaechter-prod "certbot --nginx -d supabase.nexorithm.io"
```

---

## Part 4: Fix Kong "no Route matched" Error

### Understanding the Error

```json
{"message":"no Route matched with those values"}
```

**What this means:**
- Kong (Supabase API Gateway) is running ✅
- Nginx proxy is working ✅
- **Kong has no routes configured** ❌

### Why Kong Has No Routes

Supabase Kong acts as an API gateway. It needs to be configured with:
1. **Services** - Backend services (PostgREST, GoTrue, Storage, etc.)
2. **Routes** - URL patterns that map to services

**Problem:** Your Supabase deployment may not have services registered in Kong.

### Solution: Check Supabase Configuration

```bash
# Check if Supabase services are running
ssh netzwaechter-prod "docker ps | grep supabase"

# Check Kong configuration
ssh netzwaechter-prod "curl http://127.0.0.1:54321/ 2>&1"

# Check if PostgREST is accessible
ssh netzwaechter-prod "curl -I http://127.0.0.1:54323"

# Check Supabase Studio (admin panel)
ssh netzwaechter-prod "curl -I http://127.0.0.1:54323"
```

### Expected Supabase Routes

Supabase Kong should have these routes:
- `/rest/v1/*` → PostgREST (54323)
- `/auth/v1/*` → GoTrue (54325)
- `/storage/v1/*` → Storage API (54326)
- `/realtime/v1/*` → Realtime (54324)

### Fix: Reconfigure Supabase

**Option A: Restart Supabase Stack**
```bash
ssh netzwaechter-prod "cd /opt/archon && docker compose restart supabase_kong_supabase"
```

**Option B: Check Supabase Environment Variables**
```bash
ssh netzwaechter-prod "docker logs supabase_kong_supabase | tail -50"
```

**Option C: Verify Docker Compose Configuration**
```bash
ssh netzwaechter-prod "cat /opt/archon/docker-compose.yml | grep -A30 'supabase_kong'"
```

---

## Part 5: Alternative - Direct Service Access

If Kong routing is complex, you can expose services directly via Nginx:

### Create Individual Nginx Routes

In `/etc/nginx/sites-available/archon`, add to `supabase.archon.nexorithm.io` server block:

```nginx
server {
    listen 443 ssl http2;
    server_name supabase.archon.nexorithm.io;

    # ... existing SSL config ...

    # PostgREST API
    location /rest/v1/ {
        proxy_pass http://127.0.0.1:54323/;  # PostgREST port
        # ... proxy headers ...
    }

    # Auth API
    location /auth/v1/ {
        proxy_pass http://127.0.0.1:9999/;  # GoTrue port
        # ... proxy headers ...
    }

    # Storage API
    location /storage/v1/ {
        proxy_pass http://127.0.0.1:5000/;  # Storage port
        # ... proxy headers ...
    }

    # Realtime
    location /realtime/v1/ {
        proxy_pass http://127.0.0.1:4000/;  # Realtime port
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        # ... proxy headers ...
    }

    # Default to Kong
    location / {
        proxy_pass http://127.0.0.1:54321;
        # ... existing config ...
    }
}
```

---

## Summary: What You Need to Do

### In Cloudflare (Your Action Required):

1. **Navigate to DNS settings** for nexorithm.io
2. **Find `supabase` A record**
3. **Change IP:** `49.12.201.236` → `91.98.156.158`
4. **Enable proxy** (Orange cloud ☁️)
5. **Save**

**Expected result:**
- DNS propagates in 1-5 minutes
- supabase.nexorithm.io will point to correct server

### What I Will Do (Automated):

1. **Create Nginx configuration** for supabase.nexorithm.io
2. **Set up 301 redirect** to supabase.archon.nexorithm.io
3. **Obtain SSL certificate** with certbot
4. **Test and verify** configuration
5. **Investigate Kong routing** issue

---

## Verification Steps

### After DNS Change (Your Action):

Wait 5 minutes, then test:
```bash
dig supabase.nexorithm.io A +short
# Should show: 188.114.97.3 or 188.114.96.3 (Cloudflare IPs)
```

### After Nginx Configuration (My Action):

Test access:
```bash
curl -I https://supabase.nexorithm.io
# Should get: HTTP/2 301 (redirect to supabase.archon.nexorithm.io)

curl -I https://supabase.archon.nexorithm.io
# Should get: HTTP/2 404 (Kong responding, but no routes configured)
```

### After Kong Fix (Collaborative):

Test Supabase API:
```bash
curl https://supabase.archon.nexorithm.io/rest/v1/
# Should return: Supabase API response (not 404)
```

---

## Timeline

1. **You:** Update DNS in Cloudflare → **5 minutes**
2. **Me:** Create Nginx config and SSL cert → **5 minutes**
3. **Wait:** DNS propagation → **5-10 minutes**
4. **Me:** Investigate Kong routing → **10-15 minutes**
5. **Test:** Verify everything works → **5 minutes**

**Total:** ~30-40 minutes

---

## Next Steps

### Immediate (Now):

1. ✅ You: Fix DNS in Cloudflare (change IP to 91.98.156.158)
2. ⏳ Me: Create Nginx configuration for supabase.nexorithm.io
3. ⏳ Me: Obtain SSL certificate
4. ⏳ Me: Investigate and fix Kong routing

### After DNS Fixed:

5. Test redirect: supabase.nexorithm.io → supabase.archon.nexorithm.io
6. Debug Kong "no Route matched" error
7. Configure Kong routes or bypass Kong with direct service access

### Optional (Future):

- Set up Supabase API keys for authentication
- Configure Supabase database connection
- Test PostgREST, GoTrue, Storage APIs
- Set up Supabase Studio access at /db/ endpoint

---

**Ready to proceed?**

Once you update the DNS in Cloudflare, let me know and I'll execute the Nginx configuration steps immediately.

---

**Created:** 2025-10-15 19:30 UTC
**Server:** netzwaechter-prod (91.98.156.158)
**Status:** Waiting for DNS update
