# Environment Variables

Comprehensive documentation of all environment variables used in the Netzwächter monitoring portal.

Created: 2025-10-13
Last Updated: 2025-10-13

---

## Overview

Environment variables are used to configure the application across different environments (development, staging, production) without hardcoding sensitive information.

**Location:** `.env` file (root directory)
**Template:** `.env.example`
**Security:** Never commit `.env` to version control

---

## Required Variables

### DATABASE_URL

**Purpose:** PostgreSQL connection string for the main application database

**Format:**
```
postgresql://username:password@host:port/database?sslmode=MODE
```

**Example:**
```bash
DATABASE_URL=postgresql://postgres:SecurePass123@db.example.com:5432/netzwaechter?sslmode=require
```

**SSL Modes:**
| Mode | Security | Use Case |
|------|----------|----------|
| `require` | Enforced | Production (recommended) |
| `prefer` | Optional | Development |
| `disable` | None | Local development only |
| `verify-ca` | CA verified | High security |
| `verify-full` | Full verification | Maximum security |

**Used By:**
- Backend API (database connection pool)
- Drizzle ORM (migrations)
- All database operations

**Default:** None (required)

**Validation:**
- Must be valid PostgreSQL connection string
- Must include `sslmode=require` in production
- Credentials must be strong (12+ character password)

---

### SESSION_SECRET

**Purpose:** Secret key for signing and verifying session cookies

**Format:** 128-character hexadecimal string (64 bytes)

**Generation:**
```bash
node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"
```

**Example:**
```bash
SESSION_SECRET=a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890
```

**Used By:**
- Express session middleware
- Cookie signing/verification
- Session security

**Security Requirements:**
- Minimum 128 characters (64 bytes)
- Cryptographically random
- Different per environment
- Never logged or exposed
- Rotated every 90 days

**Impact of Change:**
- All active sessions invalidated
- All users logged out
- Must re-authenticate

---

### MAILSERVER_PASSWORD

**Purpose:** SMTP authentication password for sending emails (password resets, notifications)

**Format:** String (provider-dependent)

**Example:**
```bash
MAILSERVER_PASSWORD="MySecureEmailPass2025!"
```

**Used By:**
- Email service (password resets)
- Notification system
- Alert emails

**Related Configuration:**
Additional SMTP settings stored in database (`settings` table):
- `smtp_server`: smtps.udag.de
- `port_ssl`: 465
- `port_starttls`: 587
- `username`: monitoring-direct-0002
- `email`: portal@monitoring.direct

**Security Requirements:**
- Strong password (12+ characters)
- Not stored in database
- Not logged
- Rotated every 180 days

---

## Optional Variables

### NODE_ENV

**Purpose:** Application environment mode

**Values:**
- `development` - Development mode
- `production` - Production mode
- `test` - Testing mode

**Default:** `development`

**Example:**
```bash
NODE_ENV=production
```

**Impact:**

| Feature | Development | Production |
|---------|-------------|------------|
| Database SSL | Relaxed | Strict (required) |
| Email SSL | Relaxed | Strict |
| Error Messages | Full stack traces | Minimal info |
| Logging | Verbose | Essential only |
| Session Cookie Secure | false | true |
| Session Cookie SameSite | lax | strict |
| Source Maps | Yes | No |

**Used By:**
- All application modules
- Security settings
- Logging configuration
- Error handling

---

### PORT

**Purpose:** HTTP server port number

**Format:** Integer (1024-65535)

**Default:** `5000` (from code)

**Example:**
```bash
PORT=5000
```

**Common Values:**
- `5000` - Default development
- `5001` - Alternative development
- `3000` - Common production
- `8080` - Alternative HTTP

**Used By:**
- Backend API server
- Express application

**Notes:**
- Avoid ports < 1024 (privileged)
- Must not conflict with other services
- Frontend dev server uses 5173 (Vite default)

---

### Connection Pool Variables

#### DB_POOL_MIN

**Purpose:** Minimum persistent database connections

**Format:** Integer

**Default:** `5`

**Example:**
```bash
DB_POOL_MIN=5
```

**Recommended Values:**
- Development: 2-5
- Production: 5-10

#### DB_POOL_MAX

**Purpose:** Maximum concurrent database connections

**Format:** Integer

**Default:** `20`

**Example:**
```bash
DB_POOL_MAX=20
```

**Recommended Values:**
- Development: 10-20
- Production: 20-50

**Notes:**
- Must not exceed database server limits
- Neon Free tier: 100 connections
- Neon Pro: 1000+ connections

#### DB_POOL_IDLE_TIMEOUT

**Purpose:** Time (ms) before closing idle connections

**Format:** Integer (milliseconds)

**Default:** `30000` (30 seconds)

**Example:**
```bash
DB_POOL_IDLE_TIMEOUT=30000
```

**Recommended Values:**
- Development: 30000 (30s)
- Production: 30000-60000 (30-60s)

#### DB_CONNECTION_TIMEOUT

**Purpose:** Timeout (ms) for acquiring connection from pool

**Format:** Integer (milliseconds)

**Default:** `5000` (5 seconds)

**Example:**
```bash
DB_CONNECTION_TIMEOUT=5000
```

**Recommended Values:**
- All environments: 5000 (5s)

**Pool Optimization Results:**
- 90% reduction in persistent connections (50 → 5)
- 60% reduction in max connections (50 → 20)
- Idle connections auto-close (resource savings)
- Auto-scaling based on demand

---

### LOCAL_DATABASE_URL

**Purpose:** Fallback local PostgreSQL connection string

**Format:** Same as `DATABASE_URL`

**Example:**
```bash
LOCAL_DATABASE_URL=postgresql://localhost:5432/netzwaechter_dev?sslmode=prefer
```

**Use Cases:**
- Local development
- Offline development
- Testing without cloud database

**Notes:**
- Can use relaxed SSL mode (`prefer` or `disable`)
- Not used if `DATABASE_URL` is available

---

### MAILSERVER_CA_CERT

**Purpose:** Custom CA certificate path for SMTP TLS verification

**Format:** File path (absolute)

**Example:**
```bash
MAILSERVER_CA_CERT=/path/to/ca-certificate.pem
```

**Use Cases:**
- Corporate internal CA
- Self-signed certificates
- Custom certificate chains

**Validation:**
```bash
openssl x509 -in /path/to/ca-certificate.pem -text -noout
```

**Used By:**
- Email service (nodemailer)
- TLS verification

---

## Environment Variable Summary Table

| Variable | Required | Default | Type | Purpose |
|----------|----------|---------|------|---------|
| DATABASE_URL | Yes | None | String | PostgreSQL connection |
| SESSION_SECRET | Yes | None | String (128 chars) | Session signing |
| MAILSERVER_PASSWORD | Yes | None | String | SMTP authentication |
| NODE_ENV | No | development | Enum | Environment mode |
| PORT | No | 5000 | Integer | Server port |
| DB_POOL_MIN | No | 5 | Integer | Min connections |
| DB_POOL_MAX | No | 20 | Integer | Max connections |
| DB_POOL_IDLE_TIMEOUT | No | 30000 | Integer | Idle timeout (ms) |
| DB_CONNECTION_TIMEOUT | No | 5000 | Integer | Acquire timeout (ms) |
| LOCAL_DATABASE_URL | No | None | String | Local DB fallback |
| MAILSERVER_CA_CERT | No | None | String | Custom CA cert path |

---

## Configuration by Environment

### Development Environment

```bash
# .env (development)
NODE_ENV=development
DATABASE_URL=postgresql://localhost:5432/netzwaechter_dev?sslmode=prefer
SESSION_SECRET=[128-char-generated-secret]
MAILSERVER_PASSWORD=dev_password
PORT=5000
DB_POOL_MIN=2
DB_POOL_MAX=10
DB_POOL_IDLE_TIMEOUT=30000
DB_CONNECTION_TIMEOUT=5000
```

**Characteristics:**
- Relaxed security
- Local database optional
- Verbose logging
- Hot module replacement
- Full error details

### Production Environment

```bash
# .env (production)
NODE_ENV=production
DATABASE_URL=postgresql://user:pass@prod-db.com:5432/netzwaechter?sslmode=require
SESSION_SECRET=[different-128-char-generated-secret]
MAILSERVER_PASSWORD=[strong-production-password]
PORT=3000
DB_POOL_MIN=5
DB_POOL_MAX=20
DB_POOL_IDLE_TIMEOUT=30000
DB_CONNECTION_TIMEOUT=5000
```

**Characteristics:**
- Strict security
- SSL required
- Minimal logging
- Optimized builds
- Secure cookies

### Testing Environment

```bash
# .env.test
NODE_ENV=test
DATABASE_URL=postgresql://localhost:5432/netzwaechter_test?sslmode=disable
SESSION_SECRET=[test-only-secret]
MAILSERVER_PASSWORD=test_password
PORT=5555
DB_POOL_MIN=1
DB_POOL_MAX=5
```

**Characteristics:**
- Test-specific settings
- In-memory or test database
- Fast execution
- Mocked services

---

## Setup Instructions

### Initial Setup

1. **Copy Template**
```bash
cp .env.example .env
```

2. **Generate SESSION_SECRET**
```bash
node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"
```

3. **Edit .env File**
```bash
nano .env  # or vim, code, etc.
```

4. **Update Required Values**
- Set `DATABASE_URL` with real connection string
- Paste generated `SESSION_SECRET`
- Set `MAILSERVER_PASSWORD`
- Configure `NODE_ENV`

5. **Set Permissions**
```bash
chmod 600 .env
```

6. **Verify Configuration**
```bash
grep -E "^[A-Z_]+=" .env | cut -d'=' -f1
```

7. **Test Application**
```bash
pnpm run dev
```

---

## Security Best Practices

### 1. Secret Generation

**Strong Secrets:**
```bash
# SESSION_SECRET (128 characters)
node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"

# Random password (24 characters)
node -e "console.log(require('crypto').randomBytes(18).toString('base64'))"

# Using openssl
openssl rand -hex 64      # SESSION_SECRET
openssl rand -base64 24   # Passwords
```

### 2. File Permissions

**Set Correct Permissions:**
```bash
# .env readable only by owner
chmod 600 .env

# Verify
ls -l .env  # Should show: -rw-------

# .env.example can be readable
chmod 644 .env.example
```

### 3. Git Protection

**Ensure Not Tracked:**
```bash
# Check .gitignore
grep ".env" .gitignore

# Verify not tracked
git ls-files --error-unmatch .env
# Should fail (file not tracked)

# Remove if accidentally added
git rm --cached .env
git commit -m "Remove .env from version control"
```

### 4. Rotation Schedule

| Secret | Development | Production | After Incident |
|--------|-------------|------------|----------------|
| SESSION_SECRET | Periodically | Every 90 days | Immediately |
| Database Password | Yearly | Every 180 days | Immediately |
| Email Password | Yearly | Every 180 days | Immediately |

### 5. Environment Separation

**Different Secrets Per Environment:**
- Development: Own secrets
- Staging: Own secrets
- Production: Own secrets (strongest)
- Never reuse across environments

### 6. Validation

**Check Variable Length:**
```bash
echo -n "$SESSION_SECRET" | wc -c  # Should be 128+
```

**Validate Format:**
```bash
echo "$SESSION_SECRET" | grep -qE '^[0-9a-f]{128,}$' && echo "Valid" || echo "Invalid"
```

---

## Troubleshooting

### Issue: Variable Not Set

**Symptoms:**
```
Error: DATABASE_URL environment variable not set
```

**Solutions:**
1. Check `.env` file exists: `ls -la .env`
2. Check variable in file: `grep DATABASE_URL .env`
3. Verify file loaded: Check application startup logs
4. Restart application: `pnpm run dev`

### Issue: Weak SESSION_SECRET

**Symptoms:**
```
Warning: SESSION_SECRET is too short or weak
```

**Solutions:**
1. Generate new secret: `node -e "...randomBytes..."`
2. Update `.env` with new value
3. Verify length: `echo -n "$SESSION_SECRET" | wc -c`
4. Restart application

### Issue: SSL Connection Failed

**Symptoms:**
```
Error: SSL connection to database failed
```

**Solutions:**
1. Check database supports SSL
2. Use correct SSL mode (`require`, `prefer`, or `disable`)
3. For local dev, use `sslmode=disable`
4. For production, use `sslmode=require`
5. Check custom CA cert if needed

### Issue: Session Not Persisting

**Causes:**
1. SESSION_SECRET changed (invalidates sessions)
2. SESSION_SECRET too short
3. Cookie configuration issue
4. Database connection issue

**Solutions:**
1. Verify SESSION_SECRET unchanged during testing
2. Check length: 128+ characters
3. Verify NODE_ENV matches deployment (HTTP vs HTTPS)
4. Check database sessions table

---

## Validation Scripts

### Check All Required Variables

```bash
#!/bin/bash
required=(
  "DATABASE_URL"
  "SESSION_SECRET"
  "MAILSERVER_PASSWORD"
)

for var in "${required[@]}"; do
  if grep -q "^${var}=" .env; then
    echo "✓ $var is set"
  else
    echo "✗ $var is missing"
  fi
done
```

### Validate SESSION_SECRET Length

```bash
#!/bin/bash
secret=$(grep "^SESSION_SECRET=" .env | cut -d'=' -f2)
length=${#secret}

if [ $length -ge 128 ]; then
  echo "✓ SESSION_SECRET length is sufficient ($length chars)"
else
  echo "✗ SESSION_SECRET is too short ($length chars, need 128+)"
fi
```

---

## References

### Documentation
- `.env.example` - Template file
- `apps/backend-api/ENVIRONMENT_VARIABLES.md` - Detailed docs
- `apps/backend-api/SESSION_SECURITY.md` - Session security

### External Resources
- [12-Factor App: Config](https://12factor.net/config)
- [OWASP Configuration Management](https://cheatsheetseries.owasp.org/cheatsheets/Configuration_Management_Cheat_Sheet.html)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)
