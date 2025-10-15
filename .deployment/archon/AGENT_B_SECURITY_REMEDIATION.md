# Agent B: Nginx & Network Security Remediation

Date: 2025-10-15 18:15 UTC
Agent: B (Network Security Specialist)
Server: 91.98.156.158 (netzwaechter)
Focus: Nginx configuration, SSL/TLS, security headers, rate limiting

---

## Agent B Responsibilities

**Primary Focus**: All tasks related to Nginx web server, reverse proxy configuration, SSL/TLS, and security headers.

**Working Directory**: `/etc/nginx/`
**No Conflicts With Agent A**: Agent A handles docker-compose.yml files only

---

## Task List for Agent B

### IMMEDIATE PRIORITY (Complete First)

#### Task B1: Disable Deprecated TLS Protocols ⚠️ HIGH
**Status**: COMPLETED (2025-10-15 16:23 UTC)
**Priority**: IMMEDIATE
**Risk**: HIGH - Vulnerable to downgrade attacks (POODLE, BEAST)
**Completion Notes**: TLS configuration was already updated to only support TLSv1.2 and TLSv1.3. Verified with openssl and nmap tests.

**Objective**: Remove TLSv1 and TLSv1.1, keep only TLSv1.2 and TLSv1.3

**Current Configuration**:
```nginx
ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;
```

**Target Configuration**:
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
```

**Steps**:

1. **Backup Current Configuration**:
   ```bash
   ssh root@91.98.156.158
   cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup.tls_update.$(date +%Y%m%d_%H%M%S)
   ```

2. **Update TLS Protocols**:
   ```bash
   sed -i 's/ssl_protocols.*/ssl_protocols TLSv1.2 TLSv1.3;/' /etc/nginx/nginx.conf
   ```

3. **Verify Configuration**:
   ```bash
   nginx -t
   ```

4. **Apply Changes**:
   ```bash
   systemctl reload nginx
   ```

5. **Test TLS Configuration**:
   ```bash
   # From local machine
   nmap --script ssl-enum-ciphers -p 443 archon.nexorithm.io | grep "TLSv1\."
   # Should only show TLSv1.2 and TLSv1.3
   ```

6. **Online SSL Test**:
   - Visit: https://www.ssllabs.com/ssltest/analyze.html?d=archon.nexorithm.io
   - Should achieve A+ rating

**Expected Outcome**: Only TLSv1.2 and TLSv1.3 enabled, improved SSL Labs score

**Rollback Plan**:
```bash
cp /etc/nginx/nginx.conf.backup.tls_update.YYYYMMDD_HHMMSS /etc/nginx/nginx.conf
nginx -t && systemctl reload nginx
```

---

#### Task B2: Verify WebSocket Configuration After Agent A Changes ⚠️ HIGH
**Status**: PENDING (wait for Agent A Task A4)
**Priority**: IMMEDIATE (after Agent A completes localhost binding)
**Risk**: HIGH - WebSocket functionality break

**Objective**: Ensure WebSocket connections still work after services bound to 127.0.0.1

**Dependencies**: Wait for Agent A to complete Task A4 (localhost binding)

**Steps**:

1. **Wait for Agent A Notification**: Agent A will notify when A4 is complete

2. **Test Arcane WebSocket**:
   ```bash
   # From local machine with browser
   # Open https://arcane.nexorithm.io
   # Check browser console (F12 → Console)
   # Should NOT see: "Stats websocket error"
   ```

3. **Test WebSocket Upgrade**:
   ```bash
   # From local machine
   curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" \
        -H "Sec-WebSocket-Version: 13" -H "Sec-WebSocket-Key: test" \
        https://arcane.nexorithm.io/ws
   # Should see: "HTTP/1.1 101 Switching Protocols"
   ```

4. **Check Nginx Logs**:
   ```bash
   ssh root@91.98.156.158
   tail -f /var/log/nginx/arcane-access.log | grep "upgrade"
   # Should see successful 101 responses
   ```

5. **If Issues Found**:
   - Verify proxy_pass still points to correct localhost port
   - Check WebSocket upgrade map still in nginx.conf
   - Verify Connection header uses $connection_upgrade

**Expected Outcome**: WebSocket connections work correctly after localhost binding changes

---

### SHORT-TERM PRIORITY (Week 1)

#### Task B3: Harden Netzwaechter Site Configuration ⚠️ HIGH
**Status**: COMPLETED (2025-10-15 16:27 UTC)
**Priority**: SHORT-TERM
**Risk**: HIGH - Missing security protections
**Completion Notes**:
- Applied to netzwaechter.nexorithm.io (strawa.cockpit365.pro domain not yet configured)
- Added rate limiting zone: netzwaechter_limit (120r/m, burst 30)
- Added enhanced security headers: HSTS with includeSubDomains+preload, X-Frame-Options DENY, CSP, Referrer-Policy, Permissions-Policy
- Applied rate limiting to /api/ and /ws endpoints
- Added protection for sensitive files (.files, backup files)
- All security headers verified with curl test

**Objective**: Apply modern security headers and rate limiting to strawa.cockpit365.pro

**Current Issues**:
- ❌ No rate limiting configured
- ❌ Missing Content-Security-Policy header
- ❌ Basic security headers only (no includeSubDomains on HSTS)
- ❌ No Referrer-Policy
- ❌ No fail2ban integration

**Steps**:

1. **Backup Configuration**:
   ```bash
   ssh root@91.98.156.158
   # Find the correct config file
   grep -r "strawa.cockpit365.pro" /etc/nginx/sites-available/

   # Assuming it's /etc/nginx/sites-available/netzwaechter
   cp /etc/nginx/sites-available/netzwaechter \
      /etc/nginx/sites-available/netzwaechter.backup.$(date +%Y%m%d_%H%M%S)
   ```

2. **Add Rate Limiting Zone to nginx.conf**:
   ```bash
   # Edit /etc/nginx/nginx.conf
   # Add inside http {} block:
   limit_req_zone $binary_remote_addr zone=netzwaechter_limit:10m rate=120r/m;
   ```

3. **Update Site Configuration**:
   Create updated configuration at `/etc/nginx/sites-available/netzwaechter`:

   ```nginx
   # Rate limiting zone (in nginx.conf http block)
   # limit_req_zone $binary_remote_addr zone=netzwaechter_limit:10m rate=120r/m;

   server {
       listen 443 ssl http2;
       listen [::]:443 ssl http2;
       server_name strawa.cockpit365.pro;

       # SSL Configuration (verify paths)
       ssl_certificate /etc/letsencrypt/live/strawa.cockpit365.pro/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/strawa.cockpit365.pro/privkey.pem;
       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384';
       ssl_prefer_server_ciphers off;

       # Enhanced Security Headers
       add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
       add_header X-Frame-Options "DENY" always;
       add_header X-Content-Type-Options "nosniff" always;
       add_header X-XSS-Protection "1; mode=block" always;
       add_header Referrer-Policy "strict-origin-when-cross-origin" always;
       add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

       # Content Security Policy
       add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self'; frame-ancestors 'none';" always;

       # Logging
       access_log /var/log/nginx/netzwaechter-access.log;
       error_log /var/log/nginx/netzwaechter-error.log;

       # Client body size limit
       client_max_body_size 10M;

       # Root location with rate limiting
       location / {
           # Rate limiting: 120 requests per minute per IP
           limit_req zone=netzwaechter_limit burst=30 nodelay;
           limit_req_status 429;

           proxy_pass http://127.0.0.1:XXXX;  # UPDATE WITH CORRECT PORT
           proxy_http_version 1.1;

           # WebSocket support (if needed)
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection $connection_upgrade;
           proxy_cache_bypass $http_upgrade;

           # Standard proxy headers
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;

           # Timeouts
           proxy_connect_timeout 60s;
           proxy_send_timeout 60s;
           proxy_read_timeout 60s;
       }

       # Block access to sensitive files
       location ~ /\. {
           deny all;
           access_log off;
           log_not_found off;
       }

       # Block access to backup files
       location ~ ~$ {
           deny all;
           access_log off;
           log_not_found off;
       }
   }

   # HTTP to HTTPS redirect
   server {
       listen 80;
       listen [::]:80;
       server_name strawa.cockpit365.pro;
       return 301 https://$server_name$request_uri;
   }
   ```

4. **Identify Backend Port**:
   ```bash
   # Find what port the Netzwaechter app uses
   ss -tulpn | grep LISTEN | grep -E "(3000|5000|8000|8080)"
   # Update proxy_pass line with correct port
   ```

5. **Test Configuration**:
   ```bash
   nginx -t
   ```

6. **Apply Changes**:
   ```bash
   systemctl reload nginx
   ```

7. **Verify Security Headers**:
   ```bash
   curl -I https://strawa.cockpit365.pro | grep -E "Strict-Transport|X-Frame|X-Content|CSP|Referrer"
   ```

8. **Test Rate Limiting**:
   ```bash
   for i in {1..150}; do
       curl -s -o /dev/null -w "%{http_code}\n" https://strawa.cockpit365.pro
       sleep 0.1
   done
   # Should see 429 after ~120 requests
   ```

**Expected Outcome**: Netzwaechter site has same security level as Archon and Arcane sites

---

#### Task B4: Strengthen SSL/TLS Cipher Suites ⚠️ MEDIUM
**Status**: COMPLETED (2025-10-15 16:27 UTC) - Already Configured
**Priority**: SHORT-TERM
**Risk**: MEDIUM - Weak cipher support
**Completion Notes**:
- Mozilla Modern cipher suite already configured in /etc/letsencrypt/options-ssl-nginx.conf
- Ciphers: ECDHE-ECDSA-AES128-GCM-SHA256, ECDHE-RSA-AES128-GCM-SHA256, ECDHE-ECDSA-AES256-GCM-SHA384, ECDHE-RSA-AES256-GCM-SHA384, ECDHE-ECDSA-CHACHA20-POLY1305, ECDHE-RSA-CHACHA20-POLY1305, DHE-RSA-AES128-GCM-SHA256, DHE-RSA-AES256-GCM-SHA384
- ssl_prefer_server_ciphers: off (correct for Modern profile)
- Verified with openssl s_client tests on all domains
- nmap scan shows cipher strength grade: A

**Objective**: Ensure only strong, modern ciphers are enabled

**Steps**:

1. **Check Current Ciphers**:
   ```bash
   ssh root@91.98.156.158
   grep "ssl_ciphers" /etc/nginx/nginx.conf
   ```

2. **Update to Mozilla Modern Configuration**:
   ```nginx
   # In /etc/nginx/nginx.conf (http block)
   ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384';
   ssl_prefer_server_ciphers off;
   ```

3. **Test Configuration**:
   ```bash
   nginx -t && systemctl reload nginx
   ```

4. **Verify Ciphers**:
   ```bash
   nmap --script ssl-enum-ciphers -p 443 archon.nexorithm.io
   # Should only show strong ciphers (no CBC mode, no RC4, no 3DES)
   ```

**Expected Outcome**: Only strong, modern ciphers enabled

---

#### Task B5: Implement HTTP/2 Push and Optimization ⚠️ LOW
**Status**: PENDING
**Priority**: SHORT-TERM
**Risk**: LOW - Performance optimization

**Objective**: Optimize HTTP/2 configuration for better performance

**Steps**:

1. **Verify HTTP/2 Enabled**:
   ```bash
   curl -I --http2 https://archon.nexorithm.io | grep "HTTP/2"
   ```

2. **Add HTTP/2 Optimization**:
   ```nginx
   # In /etc/nginx/nginx.conf (http block)
   http2_max_field_size 16k;
   http2_max_header_size 32k;
   http2_max_requests 1000;
   ```

3. **Test and Apply**:
   ```bash
   nginx -t && systemctl reload nginx
   ```

**Expected Outcome**: Improved HTTP/2 performance

---

### MEDIUM-TERM PRIORITY (Weeks 2-4)

#### Task B6: Implement Advanced Rate Limiting ⚠️ MEDIUM
**Status**: PENDING
**Priority**: MEDIUM-TERM
**Risk**: MEDIUM - API abuse, DDoS

**Objective**: Add granular rate limiting for different endpoint types

**Steps**:

1. **Add Multiple Rate Limit Zones**:
   ```nginx
   # In /etc/nginx/nginx.conf (http block)

   # General page requests
   limit_req_zone $binary_remote_addr zone=general_limit:10m rate=120r/m;

   # API endpoints (more restrictive)
   limit_req_zone $binary_remote_addr zone=api_limit:10m rate=200r/m;

   # Authentication endpoints (very restrictive)
   limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=10r/m;

   # Static assets (more permissive)
   limit_req_zone $binary_remote_addr zone=static_limit:10m rate=300r/m;
   ```

2. **Apply to Site Configurations**:
   ```nginx
   # In site config files

   # API endpoints
   location /api/ {
       limit_req zone=api_limit burst=50 nodelay;
       # ... proxy config
   }

   # Auth endpoints
   location ~ ^/api/auth/(login|register) {
       limit_req zone=auth_limit burst=5 nodelay;
       # ... proxy config
   }

   # Static assets
   location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
       limit_req zone=static_limit burst=100 nodelay;
       expires 30d;
       add_header Cache-Control "public, immutable";
       # ... proxy config
   }

   # General pages
   location / {
       limit_req zone=general_limit burst=30 nodelay;
       # ... proxy config
   }
   ```

3. **Test Each Zone**:
   ```bash
   # Test auth limit (should fail after 10 requests)
   for i in {1..15}; do curl -s -o /dev/null -w "%{http_code}\n" \
       https://archon.nexorithm.io/api/auth/login; done

   # Test API limit (should fail after 200 requests)
   for i in {1..250}; do curl -s -o /dev/null -w "%{http_code}\n" \
       https://archon.nexorithm.io/api/health; done
   ```

**Expected Outcome**: Granular rate limiting protecting different endpoint types

---

#### Task B7: Implement Nginx Log Rotation and Management ⚠️ LOW
**Status**: PENDING
**Priority**: MEDIUM-TERM
**Risk**: LOW - Disk space, log analysis

**Objective**: Proper log rotation to prevent disk fill and enable log analysis

**Steps**:

1. **Create Logrotate Configuration**:
   ```bash
   cat > /etc/logrotate.d/nginx-custom << 'EOF'
   /var/log/nginx/*.log {
       daily
       missingok
       rotate 14
       compress
       delaycompress
       notifempty
       create 0640 www-data adm
       sharedscripts
       prerotate
           if [ -d /etc/logrotate.d/httpd-prerotate ]; then \
               run-parts /etc/logrotate.d/httpd-prerotate; \
           fi \
       endscript
       postrotate
           invoke-rc.d nginx rotate >/dev/null 2>&1
       endscript
   }

   /var/log/nginx/arcane-*.log {
       daily
       missingok
       rotate 30
       compress
       delaycompress
       notifempty
       create 0640 www-data adm
       sharedscripts
       postrotate
           invoke-rc.d nginx rotate >/dev/null 2>&1
       endscript
   }
   EOF
   ```

2. **Test Logrotate**:
   ```bash
   logrotate -d /etc/logrotate.d/nginx-custom
   # Dry run - check for errors

   logrotate -f /etc/logrotate.d/nginx-custom
   # Force rotation - test it works
   ```

3. **Verify Rotation**:
   ```bash
   ls -lah /var/log/nginx/
   # Should see .1.gz files
   ```

**Expected Outcome**: Automatic log rotation preventing disk fill

---

#### Task B8: Implement Nginx Access Log Analysis ⚠️ LOW
**Status**: PENDING
**Priority**: MEDIUM-TERM
**Risk**: LOW - Threat detection, monitoring

**Objective**: Automated analysis of access logs for security threats

**Steps**:

1. **Install goaccess** (web log analyzer):
   ```bash
   ssh root@91.98.156.158
   apt update && apt install goaccess -y
   ```

2. **Create Daily Log Analysis Script**:
   ```bash
   cat > /usr/local/bin/daily-nginx-analysis.sh << 'EOF'
   #!/bin/bash
   DATE=$(date +%Y%m%d)
   REPORT_DIR="/root/security-reports/nginx"
   mkdir -p "$REPORT_DIR"

   # Analyze Archon logs
   echo "=== Archon Top IPs ===" > "$REPORT_DIR/archon-$DATE.txt"
   awk '{print $1}' /var/log/nginx/archon-access.log | sort | uniq -c | sort -rn | head -20 >> "$REPORT_DIR/archon-$DATE.txt"

   echo "" >> "$REPORT_DIR/archon-$DATE.txt"
   echo "=== Archon 4xx/5xx Errors ===" >> "$REPORT_DIR/archon-$DATE.txt"
   grep -E ' (4|5)[0-9]{2} ' /var/log/nginx/archon-access.log | tail -50 >> "$REPORT_DIR/archon-$DATE.txt"

   # Analyze Arcane logs
   echo "=== Arcane Top IPs ===" > "$REPORT_DIR/arcane-$DATE.txt"
   awk '{print $1}' /var/log/nginx/arcane-access.log | sort | uniq -c | sort -rn | head -20 >> "$REPORT_DIR/arcane-$DATE.txt"

   echo "" >> "$REPORT_DIR/arcane-$DATE.txt"
   echo "=== Arcane Rate Limit Hits ===" >> "$REPORT_DIR/arcane-$DATE.txt"
   grep ' 429 ' /var/log/nginx/arcane-access.log | tail -20 >> "$REPORT_DIR/arcane-$DATE.txt"

   # Generate HTML report with goaccess
   goaccess /var/log/nginx/archon-access.log -o "$REPORT_DIR/archon-$DATE.html" --log-format=COMBINED
   goaccess /var/log/nginx/arcane-access.log -o "$REPORT_DIR/arcane-$DATE.html" --log-format=COMBINED

   # Find suspicious patterns
   echo "=== Suspicious Requests ===" > "$REPORT_DIR/suspicious-$DATE.txt"
   grep -E '(\.\.\/|union.*select|<script|eval\(|base64)' /var/log/nginx/*-access.log >> "$REPORT_DIR/suspicious-$DATE.txt" 2>/dev/null
   EOF
   chmod +x /usr/local/bin/daily-nginx-analysis.sh
   ```

3. **Schedule Daily Analysis**:
   ```bash
   crontab -e
   # Add: 0 6 * * * /usr/local/bin/daily-nginx-analysis.sh
   ```

4. **Run Initial Analysis**:
   ```bash
   /usr/local/bin/daily-nginx-analysis.sh
   ls -lah /root/security-reports/nginx/
   ```

**Expected Outcome**: Daily automated analysis of access logs with threat detection

---

#### Task B9: Implement GeoIP Blocking (Optional) ⚠️ LOW
**Status**: PENDING
**Priority**: MEDIUM-TERM
**Risk**: LOW - Targeted geographic blocking

**Objective**: Block traffic from high-risk countries (if needed)

**Note**: Only implement if seeing attacks from specific countries

**Steps**:

1. **Install GeoIP Module**:
   ```bash
   apt install libnginx-mod-http-geoip2 mmdb-bin -y
   ```

2. **Download GeoIP Database**:
   ```bash
   mkdir -p /etc/nginx/geoip
   cd /etc/nginx/geoip
   wget https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-Country.mmdb
   ```

3. **Configure GeoIP**:
   ```nginx
   # In /etc/nginx/nginx.conf (http block)
   geoip2 /etc/nginx/geoip/GeoLite2-Country.mmdb {
       auto_reload 5m;
       $geoip2_metadata_country_build metadata build_epoch;
       $geoip2_data_country_code country iso_code;
       $geoip2_data_country_name country names en;
   }

   # Block specific countries (example)
   map $geoip2_data_country_code $blocked_country {
       default 0;
       CN 1;  # China
       RU 1;  # Russia
       KP 1;  # North Korea
   }
   ```

4. **Apply Blocking in Site Config**:
   ```nginx
   server {
       # ... other config

       if ($blocked_country) {
           return 403 "Access from your country is not allowed";
       }
   }
   ```

5. **Test**:
   ```bash
   nginx -t && systemctl reload nginx
   ```

**Expected Outcome**: Traffic from specified countries blocked (use sparingly)

---

### LONG-TERM PRIORITY (Months 2-3)

#### Task B10: Implement ModSecurity WAF ⚠️ MEDIUM
**Status**: PENDING
**Priority**: LONG-TERM
**Risk**: MEDIUM - Advanced attack protection

**Objective**: Add Web Application Firewall for advanced threat protection

**Steps**:

1. **Install ModSecurity**:
   ```bash
   apt update
   apt install libnginx-mod-http-modsecurity libmodsecurity3 -y
   ```

2. **Enable ModSecurity**:
   ```bash
   mkdir -p /etc/nginx/modsec
   cp /usr/share/modsecurity-crs/modsecurity.conf-recommended /etc/nginx/modsec/modsecurity.conf
   ```

3. **Download OWASP Core Rule Set**:
   ```bash
   cd /etc/nginx/modsec
   git clone https://github.com/coreruleset/coreruleset.git
   cp coreruleset/crs-setup.conf.example crs-setup.conf
   ```

4. **Configure Nginx to Use ModSecurity**:
   ```nginx
   # In /etc/nginx/nginx.conf (http block)
   modsecurity on;
   modsecurity_rules_file /etc/nginx/modsec/modsecurity.conf;
   ```

5. **Test in Detection-Only Mode**:
   ```bash
   # In modsecurity.conf
   SecRuleEngine DetectionOnly  # Monitor only, don't block

   nginx -t && systemctl reload nginx
   ```

6. **Monitor for False Positives** (1 week):
   ```bash
   tail -f /var/log/nginx/modsec_audit.log
   ```

7. **Enable Blocking Mode** (after tuning):
   ```bash
   # In modsecurity.conf
   SecRuleEngine On  # Start blocking

   systemctl reload nginx
   ```

**Expected Outcome**: WAF protecting against OWASP Top 10 attacks

**Caution**: Requires careful tuning to avoid blocking legitimate traffic

---

#### Task B11: Implement Certificate Pinning ⚠️ LOW
**Status**: PENDING
**Priority**: LONG-TERM
**Risk**: LOW - MITM protection

**Objective**: Implement HTTP Public Key Pinning (HPKP) or Expect-CT

**Note**: HPKP is deprecated, use Expect-CT instead

**Steps**:

1. **Enable Expect-CT Header**:
   ```nginx
   # In site configs
   add_header Expect-CT "max-age=86400, enforce" always;
   ```

2. **Test**:
   ```bash
   curl -I https://archon.nexorithm.io | grep Expect-CT
   ```

**Expected Outcome**: Certificate transparency enforcement

---

#### Task B12: Implement Nginx Security Monitoring ⚠️ LOW
**Status**: PENDING
**Priority**: LONG-TERM
**Risk**: LOW - Real-time threat detection

**Objective**: Real-time monitoring of Nginx security events

**Steps**:

1. **Install Prometheus Nginx Exporter**:
   ```bash
   wget https://github.com/nginxinc/nginx-prometheus-exporter/releases/download/v0.11.0/nginx-prometheus-exporter_0.11.0_linux_amd64.tar.gz
   tar -xzf nginx-prometheus-exporter_0.11.0_linux_amd64.tar.gz
   mv nginx-prometheus-exporter /usr/local/bin/
   ```

2. **Create Systemd Service**:
   ```bash
   cat > /etc/systemd/system/nginx-exporter.service << 'EOF'
   [Unit]
   Description=Nginx Prometheus Exporter
   After=network.target

   [Service]
   Type=simple
   User=www-data
   ExecStart=/usr/local/bin/nginx-prometheus-exporter -nginx.scrape-uri=http://localhost/nginx_status
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   EOF
   ```

3. **Enable Nginx Stub Status**:
   ```nginx
   # In /etc/nginx/sites-available/default or new file
   server {
       listen 127.0.0.1:8080;
       server_name localhost;

       location /nginx_status {
           stub_status on;
           access_log off;
           allow 127.0.0.1;
           deny all;
       }
   }
   ```

4. **Start Exporter**:
   ```bash
   systemctl enable nginx-exporter
   systemctl start nginx-exporter
   ```

5. **Verify Metrics**:
   ```bash
   curl http://localhost:9113/metrics
   ```

**Expected Outcome**: Nginx metrics available for Prometheus/Grafana monitoring

---

## Task Dependencies

```
B1 (Disable deprecated TLS) ─── Can run immediately
B2 (Verify WebSocket) ──────── Wait for Agent A Task A4
B3 (Harden Netzwaechter) ───── Can run immediately
B4 (Strengthen ciphers) ────── Can run after B1
B5 (HTTP/2 optimization) ───── Can run anytime

B6 (Advanced rate limiting) ─── Can run after B3
B7 (Log rotation) ──────────── Independent, can run anytime
B8 (Log analysis) ──────────── Can run after B7
B9 (GeoIP blocking) ────────── Optional, run if needed

B10 (ModSecurity WAF) ──────── Long-term, independent
B11 (Certificate pinning) ──── Long-term, independent
B12 (Security monitoring) ──── Long-term, independent
```

---

## Verification Checklist

After completing all tasks, verify:

- [x] Only TLSv1.2 and TLSv1.3 enabled (B1 COMPLETED)
- [ ] WebSocket connections work after Agent A changes (B2 PENDING - waiting for Agent A)
- [x] Netzwaechter site has rate limiting and security headers (B3 COMPLETED)
- [x] Strong cipher suites configured (B4 COMPLETED)
- [ ] HTTP/2 optimizations applied (B5 PENDING)
- [ ] Advanced rate limiting for different endpoints (B6 PENDING)
- [ ] Log rotation configured (B7 PENDING)
- [ ] Automated log analysis running (B8 PENDING)
- [ ] SSL Labs grade A+ on all sites (To be tested)
- [x] No security header warnings (All sites have proper headers)

---

## Testing Commands

### Test TLS Configuration
```bash
# Check TLS versions
nmap --script ssl-enum-ciphers -p 443 archon.nexorithm.io

# Check SSL Labs grade
# Visit: https://www.ssllabs.com/ssltest/analyze.html?d=archon.nexorithm.io
```

### Test Security Headers
```bash
# Archon
curl -I https://archon.nexorithm.io | grep -E "Strict-Transport|X-Frame|X-Content|CSP"

# Arcane
curl -I https://arcane.nexorithm.io | grep -E "Strict-Transport|X-Frame|X-Content|CSP"

# Netzwaechter
curl -I https://strawa.cockpit365.pro | grep -E "Strict-Transport|X-Frame|X-Content|CSP"
```

### Test Rate Limiting
```bash
# Test Archon rate limit
for i in {1..250}; do
    curl -s -o /dev/null -w "%{http_code}\n" https://archon.nexorithm.io/api/health
    sleep 0.1
done

# Test Arcane rate limit
for i in {1..120}; do
    curl -s -o /dev/null -w "%{http_code}\n" https://arcane.nexorithm.io/health
    sleep 0.1
done
```

### Test WebSocket
```bash
# Check WebSocket upgrade
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" \
     -H "Sec-WebSocket-Version: 13" -H "Sec-WebSocket-Key: test" \
     https://arcane.nexorithm.io/ws
# Should see: HTTP/1.1 101 Switching Protocols
```

---

## Rollback Procedures

All configurations backed up with timestamps:
```bash
# List all backups
ls -lah /etc/nginx/*.backup.*
ls -lah /etc/nginx/sites-available/*.backup.*

# Rollback to specific backup
cp /etc/nginx/nginx.conf.backup.YYYYMMDD_HHMMSS /etc/nginx/nginx.conf
nginx -t && systemctl reload nginx

# Check Nginx status
systemctl status nginx
curl -I https://archon.nexorithm.io
```

---

## Communication with Agent A

**Coordination Point**: Notify Agent A after completing B2 (WebSocket verification)

**Message to Agent A After B2**:
```
Agent A: WebSocket verification complete (Task B2)
Status: ✅ PASS / ❌ FAIL
Issues: [None / List any issues found]
Services verified:
- Arcane WebSocket: [Working / Not working]
- Archon proxy: [Working / Not working]
- Netzwaechter proxy: [Working / Not working]
```

**Wait for Agent A**: Before starting B2, wait for Agent A to complete Task A4 (localhost binding)

---

## Security Header Reference

### Expected Headers on All Sites

```http
HTTP/2 200
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; ...
```

### Security Header Grades

| Header | Grade | Impact |
|--------|-------|--------|
| Strict-Transport-Security | A+ | Force HTTPS, preload list |
| X-Frame-Options: DENY | A | Prevent clickjacking |
| X-Content-Type-Options: nosniff | A | Prevent MIME sniffing |
| X-XSS-Protection: 1; mode=block | A | XSS protection |
| Content-Security-Policy | A | Comprehensive protection |
| Referrer-Policy | A | Privacy protection |

---

## Nginx Configuration Best Practices

### File Organization
```
/etc/nginx/
├── nginx.conf                    # Main config
├── conf.d/                       # Additional configs
├── sites-available/              # Site configs
│   ├── archon                    # Archon site
│   ├── arcane                    # Arcane site
│   └── netzwaechter              # Netzwaechter site
├── sites-enabled/                # Enabled sites (symlinks)
├── snippets/                     # Reusable snippets
│   ├── ssl-params.conf           # SSL/TLS settings
│   └── security-headers.conf     # Security headers
└── modsec/                       # ModSecurity (if installed)
```

### Reusable Security Headers Snippet
```nginx
# /etc/nginx/snippets/security-headers.conf
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self'; frame-ancestors 'none';" always;
```

**Usage in site configs**:
```nginx
server {
    # ... other config
    include snippets/security-headers.conf;
}
```

---

**Agent B Start Date**: 2025-10-15 18:15 UTC
**Expected Completion**: Week 1 for immediate/short-term tasks
**Progress Tracking**: Update this file with completion status
