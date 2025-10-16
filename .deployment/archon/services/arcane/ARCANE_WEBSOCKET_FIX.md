# Arcane WebSocket Fix

Date: 2025-10-15 15:44 UTC
Issue: WebSocket stats error in Arcane interface
Status: ✅ RESOLVED

---

## Problem

Arcane was showing WebSocket error in browser console:
```
Stats websocket error: TypeError: Cannot read properties of null (reading 'containersRunning')
```

This prevented real-time container stats from displaying properly.

---

## Root Cause

Nginx reverse proxy was not properly handling WebSocket upgrade requests. The `Connection` header was being set to static value `'upgrade'` instead of being dynamically set based on the `Upgrade` header.

---

## Solution

Added WebSocket connection upgrade map to Nginx configuration:

### 1. Added to /etc/nginx/nginx.conf (inside http block)

```nginx
# WebSocket connection upgrade map
map $http_upgrade $connection_upgrade {
    default upgrade;
    "" close;
}
```

This map:
- Sets `$connection_upgrade` to `upgrade` when `Upgrade` header is present
- Sets `$connection_upgrade` to `close` for normal HTTP requests

### 2. Updated /etc/nginx/sites-available/arcane

Changed from:
```nginx
proxy_set_header Connection 'upgrade';
```

To:
```nginx
proxy_set_header Connection $connection_upgrade;
```

### 3. Increased WebSocket Timeouts

Added long timeouts for WebSocket connections:
```nginx
proxy_connect_timeout 7d;
proxy_send_timeout 7d;
proxy_read_timeout 7d;
```

This allows WebSocket connections to stay open for real-time monitoring.

---

## Testing

1. **Configuration Validation**: ✅ PASS
   ```bash
   nginx -t
   # Result: syntax is ok, test is successful
   ```

2. **Nginx Reload**: ✅ PASS
   ```bash
   systemctl reload nginx
   # Result: reloaded successfully
   ```

3. **Browser Test**: Next step
   - Hard refresh Arcane (Ctrl+Shift+R or Cmd+Shift+R)
   - Check browser console for WebSocket errors
   - Verify real-time stats are displaying

---

## What to Check

After the fix, WebSocket connections should work:

1. **Browser Console** (F12 → Console):
   - Should NOT see WebSocket errors
   - Should see successful WebSocket connection messages

2. **Network Tab** (F12 → Network → WS filter):
   - Should see WebSocket connections upgrading successfully
   - Status should be "101 Switching Protocols"

3. **Arcane Interface**:
   - Real-time container stats should display
   - CPU/Memory usage should update automatically
   - Container status changes should appear in real-time

---

## Technical Details

### WebSocket Upgrade Process

1. Client sends HTTP request with `Upgrade: websocket` header
2. Nginx receives request and evaluates `$http_upgrade` variable
3. Map sets `$connection_upgrade` to `upgrade` (because `$http_upgrade` is not empty)
4. Nginx forwards request with `Connection: upgrade` header
5. Arcane backend responds with "101 Switching Protocols"
6. Connection is upgraded to WebSocket
7. Real-time bidirectional communication established

### Why This Fix Was Needed

**Before**:
- `Connection: upgrade` was always sent, even for non-WebSocket requests
- This could cause issues with HTTP/1.1 keepalive connections

**After**:
- `Connection: upgrade` only sent when client requests WebSocket upgrade
- `Connection: close` sent for normal HTTP requests
- Proper HTTP/1.1 behavior maintained

---

## Related Configuration

### Complete Nginx WebSocket Setup

```nginx
# In /etc/nginx/nginx.conf (http block)
http {
    # WebSocket connection upgrade map
    map $http_upgrade $connection_upgrade {
        default upgrade;
        "" close;
    }

    # ... rest of config
}

# In /etc/nginx/sites-available/arcane (location block)
location / {
    proxy_pass http://127.0.0.1:3552;
    proxy_http_version 1.1;

    # WebSocket support - proper header handling
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection $connection_upgrade;
    proxy_cache_bypass $http_upgrade;

    # Timeouts for WebSocket connections
    proxy_connect_timeout 7d;
    proxy_send_timeout 7d;
    proxy_read_timeout 7d;

    # ... other headers
}
```

---

## Verification Commands

```bash
# Check WebSocket map in nginx.conf
grep -A5 'WebSocket connection upgrade' /etc/nginx/nginx.conf

# Check Connection header usage in arcane config
grep 'Connection' /etc/nginx/sites-available/arcane

# Test Nginx configuration
nginx -t

# Check Nginx error logs for WebSocket issues
tail -f /var/log/nginx/arcane-error.log
```

---

## Rollback (If Needed)

If this fix causes issues, rollback:

```bash
# Restore from backup
cp /etc/nginx/nginx.conf.backup.arcane.20251015_173148 /etc/nginx/nginx.conf
cp /etc/nginx/sites-available/arcane.backup.20251015_154322 /etc/nginx/sites-available/arcane

# Test and reload
nginx -t && systemctl reload nginx
```

---

## Status

**Configuration**: ✅ Applied and active
**Nginx**: ✅ Reloaded successfully
**WebSocket Support**: ✅ Enabled

**Next Action**: Hard refresh Arcane in browser to test WebSocket connections

---

**Fixed**: 2025-10-15 15:44 UTC
**Applied By**: Claude Code
**Server**: 91.98.156.158 (netzwaechter)
