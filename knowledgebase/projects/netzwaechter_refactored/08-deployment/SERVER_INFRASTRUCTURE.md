# Netzwächter Production Server Infrastructure

**Created: 2025-10-14 | Timestamp: 15:57:30**

This document provides comprehensive documentation of the Netzwächter production server infrastructure hosted at Hetzner.

---

## Table of Contents

- [Server Specifications](#server-specifications)
- [Network Configuration](#network-configuration)
- [SSL/TLS Configuration](#ssltls-configuration)
- [Nginx Web Server Configuration](#nginx-web-server-configuration)
- [Security Measures](#security-measures)
- [System Resources](#system-resources)
- [Maintenance Procedures](#maintenance-procedures)

---

## Server Specifications

### Basic Information
- **Hostname**: netzwaechter
- **Domain**: netzwaechter.nexorithm.io
- **IP Address**: 91.98.156.158
- **Provider**: Hetzner Cloud
- **Operating System**: Ubuntu 24.04.3 LTS (ARM64)

### Hardware Resources
- **vCPU**: 8 cores
- **RAM**: 16 GB
- **Disk Space**: 160 GB
- **Architecture**: ARM64 (aarch64)

### Current Resource Usage
- **Disk Usage**: 3.1 GB used / 141 GB available (3% used)
- **Memory Usage**: 671 MB used / 14 GB available
- **Swap**: Not configured (0 B)

---

## Network Configuration

### Domain and DNS
- **Primary Domain**: netzwaechter.nexorithm.io
- **IP Address**: 91.98.156.158
- **DNS Configuration**: Points to Hetzner server IP

### Firewall Configuration (UFW)

The server uses UFW (Uncomplicated Firewall) with the following rules:

```bash
Status: active

     To                         Action      From
     --                         ------      ----
[ 1] 22/tcp                     ALLOW IN    Anywhere
[ 2] 80/tcp                     ALLOW IN    Anywhere
[ 3] 443/tcp                    ALLOW IN    Anywhere
[ 4] 22/tcp (v6)                ALLOW IN    Anywhere (v6)
[ 5] 80/tcp (v6)                ALLOW IN    Anywhere (v6)
[ 6] 443/tcp (v6)               ALLOW IN    Anywhere (v6)
```

### Open Ports and Their Purposes

| Port | Protocol | Purpose | Access |
|------|----------|---------|--------|
| 22 | TCP | SSH (Secure Shell) | Restricted to key-based authentication |
| 80 | TCP | HTTP | Redirects to HTTPS (443) |
| 443 | TCP | HTTPS | Main application access via SSL/TLS |

### Internal Services
- **Backend API**: Runs on localhost:3000 (not exposed externally)
- **Frontend**: Served as static files via Nginx
- **WebSocket**: Available at /ws endpoint (proxied through Nginx)

---

## SSL/TLS Configuration

### Certificate Details
- **Provider**: Let's Encrypt
- **Certificate Authority**: Let's Encrypt
- **Certificate Type**: ECDSA
- **Domain**: netzwaechter.nexorithm.io
- **Expiry Date**: 2026-01-12 14:19:49 UTC (Valid for 89 days as of 2025-10-14)

### Certificate Locations
```bash
Certificate Path: /etc/letsencrypt/live/netzwaechter.nexorithm.io/fullchain.pem
Private Key Path: /etc/letsencrypt/live/netzwaechter.nexorithm.io/privkey.pem
SSL Options: /etc/letsencrypt/options-ssl-nginx.conf
DH Parameters: /etc/letsencrypt/ssl-dhparams.pem
```

### Automatic Renewal
Certbot is configured to automatically renew certificates:

```bash
# Timer Status
NEXT: Wed 2025-10-15 06:07:07 UTC
SERVICE: certbot.service
TRIGGER: certbot.timer
```

**Renewal Command**:
```bash
certbot renew
```

The renewal process runs automatically via systemd timer. Certificates are renewed automatically when they have less than 30 days remaining.

### SSL Configuration in Nginx
- Uses Let's Encrypt recommended SSL settings
- Includes SSL session caching
- Implements strong cipher suites
- Enables OCSP stapling for certificate validation

---

## Nginx Web Server Configuration

### Configuration File Location
```bash
/etc/nginx/sites-available/netzwaechter
/etc/nginx/sites-enabled/netzwaechter (symlink)
```

### Complete Nginx Configuration

```nginx
server {
    server_name netzwaechter.nexorithm.io;

    # Serve frontend static files
    root /opt/netzwaechter/apps/frontend-web/dist;
    index index.html;

    # API requests
    location /api/ {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Frontend - serve static files, fallback to index.html for SPA routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 10240;
    gzip_proxied expired no-cache no-store private auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;

    listen [::]:443 ssl ipv6only=on; # managed by Certbot
    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/netzwaechter.nexorithm.io/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/netzwaechter.nexorithm.io/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}

server {
    if ($host = netzwaechter.nexorithm.io) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    listen 80;
    listen [::]:80;
    server_name netzwaechter.nexorithm.io;
    return 404; # managed by Certbot
}
```

### Nginx Configuration Highlights

#### Routing Strategy
- **Root Path (/)**: Serves static frontend files from `/opt/netzwaechter/apps/frontend-web/dist`
- **API Endpoints (/api/)**: Proxied to backend server at localhost:3000
- **WebSocket (/ws)**: Proxied to backend with WebSocket upgrade support
- **SPA Fallback**: All non-matching routes fall back to index.html for client-side routing

#### Proxy Settings
- **Backend Server**: http://localhost:3000
- **Protocol**: HTTP/1.1 with upgrade support
- **Headers Forwarded**:
  - X-Real-IP: Client's actual IP address
  - X-Forwarded-For: Chain of proxy IPs
  - X-Forwarded-Proto: Original protocol (https)
  - Host: Original host header

#### Performance Optimizations
- **Gzip Compression**: Enabled for text-based content types
- **Minimum Compression Size**: 10240 bytes
- **Compressed Types**: Plain text, CSS, XML, JavaScript, JSON
- **Cache Bypass**: Honors upgrade requests

---

## Security Measures

### SSH Security Configuration

**Authentication Method**: Key-based authentication only

```bash
PermitRootLogin prohibit-password
PubkeyAuthentication yes
PasswordAuthentication no
```

**Security Features**:
- Root login only permitted with SSH keys (no password)
- Public key authentication enabled
- Password authentication completely disabled
- Default SSH port: 22 (consider changing for additional security)

### Fail2Ban Intrusion Prevention

**Status**: Active and running

```bash
Service: fail2ban.service
Status: active (running) since Tue 2025-10-14 14:40:16 UTC
Uptime: 1h 17min
Memory Usage: 23.2 MB
```

**SSH Jail Statistics**:
- Currently failed attempts: 1
- Total failed attempts: 20
- Total banned IPs: 3
- Currently banned IPs: 0

Fail2Ban actively monitors SSH login attempts and automatically bans IP addresses that show malicious behavior (multiple failed login attempts).

### Firewall (UFW) Security

**Status**: Active

**Security Posture**:
- Only essential ports are open (22, 80, 443)
- All other ports are blocked by default
- Both IPv4 and IPv6 are protected
- Default deny policy for incoming connections

### Nginx Security Headers

The following security headers are implemented:

```nginx
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
```

**Header Descriptions**:
- **X-Frame-Options**: Prevents clickjacking attacks by disallowing embedding in iframes except from same origin
- **X-Content-Type-Options**: Prevents MIME type sniffing
- **X-XSS-Protection**: Enables browser's XSS filter

### SSL/TLS Security

**Security Features**:
- Strong cipher suites (managed by Let's Encrypt)
- TLS 1.2 and TLS 1.3 support
- HTTPS-only access (HTTP redirects to HTTPS)
- HSTS not currently enabled (recommended addition)
- Modern SSL configuration following Let's Encrypt best practices

---

## System Resources

### Disk Usage
```bash
Filesystem: /dev/sda1
Total Size: 150 GB
Used: 3.1 GB (3%)
Available: 141 GB
```

### Memory Usage
```bash
Total RAM: 15 GB
Used: 671 MB
Available: 14 GB
Swap: 0 B (not configured)
```

### Application Locations
- **Application Root**: /opt/netzwaechter/
- **Frontend Build**: /opt/netzwaechter/apps/frontend-web/dist
- **Backend Service**: Runs on localhost:3000

---

## Maintenance Procedures

### SSL Certificate Renewal

Certificates automatically renew via certbot timer. Manual renewal can be triggered:

```bash
# Check certificate expiry
ssh netzwaechter-prod 'certbot certificates'

# Manual renewal (if needed)
ssh netzwaechter-prod 'sudo certbot renew'

# Test renewal without actually renewing
ssh netzwaechter-prod 'sudo certbot renew --dry-run'

# Reload Nginx after certificate renewal
ssh netzwaechter-prod 'sudo systemctl reload nginx'
```

### Nginx Management

```bash
# Test configuration
ssh netzwaechter-prod 'sudo nginx -t'

# Reload configuration (no downtime)
ssh netzwaechter-prod 'sudo systemctl reload nginx'

# Restart Nginx
ssh netzwaechter-prod 'sudo systemctl restart nginx'

# Check Nginx status
ssh netzwaechter-prod 'sudo systemctl status nginx'

# View Nginx error logs
ssh netzwaechter-prod 'sudo tail -f /var/log/nginx/error.log'

# View Nginx access logs
ssh netzwaechter-prod 'sudo tail -f /var/log/nginx/access.log'
```

### Firewall Management

```bash
# Check firewall status
ssh netzwaechter-prod 'sudo ufw status numbered'

# Add a new rule
ssh netzwaechter-prod 'sudo ufw allow <port>/tcp'

# Delete a rule
ssh netzwaechter-prod 'sudo ufw delete <number>'

# Reload firewall
ssh netzwaechter-prod 'sudo ufw reload'
```

### Fail2Ban Management

```bash
# Check fail2ban status
ssh netzwaechter-prod 'sudo systemctl status fail2ban'

# Check SSH jail status
ssh netzwaechter-prod 'sudo fail2ban-client status sshd'

# Unban an IP address
ssh netzwaechter-prod 'sudo fail2ban-client set sshd unbanip <ip-address>'

# View fail2ban logs
ssh netzwaechter-prod 'sudo tail -f /var/log/fail2ban.log'
```

### System Updates

```bash
# Update package lists
ssh netzwaechter-prod 'sudo apt update'

# Upgrade packages
ssh netzwaechter-prod 'sudo apt upgrade -y'

# Check for security updates
ssh netzwaechter-prod 'sudo unattended-upgrades --dry-run'

# Reboot server (if needed)
ssh netzwaechter-prod 'sudo reboot'
```

### Monitoring Commands

```bash
# Check disk usage
ssh netzwaechter-prod 'df -h'

# Check memory usage
ssh netzwaechter-prod 'free -h'

# Check running processes
ssh netzwaechter-prod 'top -b -n 1 | head -20'

# Check system load
ssh netzwaechter-prod 'uptime'

# Check open ports
ssh netzwaechter-prod 'sudo netstat -tlnp'
```

---

## Security Recommendations

### Implemented
- SSH key-based authentication
- Password authentication disabled
- Fail2Ban intrusion prevention
- UFW firewall active
- SSL/TLS encryption via Let's Encrypt
- Security headers in Nginx
- Automatic SSL certificate renewal

### Future Enhancements to Consider
1. **HSTS (HTTP Strict Transport Security)**: Add `Strict-Transport-Security` header
2. **CSP (Content Security Policy)**: Implement content security policy headers
3. **Rate Limiting**: Add Nginx rate limiting for API endpoints
4. **SSH Port Change**: Consider moving SSH to non-standard port
5. **2FA for SSH**: Implement two-factor authentication for SSH access
6. **Log Monitoring**: Set up centralized log monitoring and alerting
7. **Backup Strategy**: Implement automated backup solution
8. **DDoS Protection**: Consider Cloudflare or similar DDoS protection service
9. **Security Scanning**: Regular vulnerability scans and penetration testing
10. **Swap Configuration**: Add swap space for better memory management

---

## Emergency Contacts and Access

### Server Access
- **SSH Connection**: `ssh netzwaechter-prod`
- **SSH Host Configuration**: Defined in `~/.ssh/config`
- **SSH Key**: Use configured private key for authentication

### Important URLs
- **Production Application**: https://netzwaechter.nexorithm.io
- **API Endpoint**: https://netzwaechter.nexorithm.io/api/
- **WebSocket**: wss://netzwaechter.nexorithm.io/ws

### Service Provider
- **Provider**: Hetzner Cloud
- **Account**: nexorithm.io organization
- **Control Panel**: https://console.hetzner.cloud/

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-10-14 | Initial infrastructure documentation created | System Administrator |

---

**Document Version**: 1.0
**Last Updated**: 2025-10-14 15:57:30
**Maintained By**: Nexorithm Development Team
