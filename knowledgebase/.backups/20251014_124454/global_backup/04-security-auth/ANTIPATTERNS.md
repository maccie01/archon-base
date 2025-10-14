# Security Anti-Patterns - Common Mistakes to Avoid

Created: 2025-10-13
Last Updated: 2025-10-13
Sources: OWASP, Security Research, Real-World Incidents, Industry Experience

## Overview

This document catalogs common security anti-patterns and mistakes that developers make. Learning what NOT to do is as important as learning best practices. Each anti-pattern includes why it's dangerous, real-world impact, and the correct approach.

## Critical Anti-Patterns (Never Do These)

### 1. Storing Passwords in Plain Text

**Anti-Pattern**:
```typescript
// NEVER DO THIS
const user = {
  username: 'john',
  password: 'MyPassword123'  // Stored in plain text
};

await db.insert('users', user);
```

**Why It's Dangerous**:
- Database breach exposes all passwords
- Admins can see user passwords
- Passwords can be used on other sites (credential stuffing)
- Violates data protection regulations
- Irreversible damage to user trust

**Real-World Impact**:
- LinkedIn (2012): 6.5M passwords compromised
- Adobe (2013): 153M passwords exposed
- Yahoo (2013-2014): 3B accounts affected

**Correct Approach**:
```typescript
// ALWAYS DO THIS
import argon2 from 'argon2';

const hashedPassword = await argon2.hash(user.password);
const user = {
  username: 'john',
  passwordHash: hashedPassword  // Hashed with Argon2id
};

await db.insert('users', user);
```

### 2. SQL Injection via String Concatenation

**Anti-Pattern**:
```typescript
// NEVER DO THIS
const userId = req.params.id;
const query = `SELECT * FROM users WHERE id = ${userId}`;
const user = await db.query(query);

// Attack: /users/1 OR 1=1--
// Result: Returns all users
```

**Why It's Dangerous**:
- Attacker can execute arbitrary SQL
- Database can be deleted
- Sensitive data can be exfiltrated
- Can lead to complete system compromise

**Real-World Impact**:
- TalkTalk (2015): £400k fine, customer data stolen
- Equifax (2017): 147M records compromised
- British Airways (2018): £183M fine

**Correct Approach**:
```typescript
// ALWAYS DO THIS - Use parameterized queries
const userId = req.params.id;
const user = await db.query('SELECT * FROM users WHERE id = $1', [userId]);

// Or use ORM safely
const user = await db.select().from('users').where({ id: userId });
```

### 3. Client-Side Security Only

**Anti-Pattern**:
```typescript
// NEVER DO THIS
// Frontend code
if (user.role === 'admin') {
  // Show admin panel
  showAdminPanel();
}

// Backend doesn't check permissions
app.delete('/api/users/:id', async (req, res) => {
  await db.delete('users', req.params.id);  // No auth check!
  res.json({ success: true });
});
```

**Why It's Dangerous**:
- Client-side code can be modified easily
- Browser DevTools can bypass any frontend check
- API remains accessible to attackers
- No security at all - pure security theater

**Correct Approach**:
```typescript
// ALWAYS DO THIS - Server-side validation
app.delete('/api/users/:id',
  requireAuth,                    // Check authentication
  requireRole('admin'),           // Check authorization
  async (req, res) => {
    const userId = parseInt(req.params.id);

    // Additional checks
    if (userId === req.user.id) {
      return res.status(400).json({ error: 'Cannot delete own account' });
    }

    await db.delete('users', userId);
    res.json({ success: true });
  }
);
```

### 4. Hardcoded Secrets in Code

**Anti-Pattern**:
```typescript
// NEVER DO THIS
const API_KEY = 'sk_live_abc123xyz789';
const DATABASE_PASSWORD = 'MySecretPass123';
const JWT_SECRET = 'super-secret-key';

// Even worse: committed to Git
const config = {
  aws: {
    accessKeyId: 'AKIAIOSFODNN7EXAMPLE',
    secretAccessKey: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
  }
};
```

**Why It's Dangerous**:
- Secrets exposed in version control forever
- Anyone with code access has secrets
- Can't rotate secrets without code change
- Automated scanners find hardcoded secrets
- Often pushed to public repositories

**Real-World Impact**:
- GitHub: Thousands of AWS keys exposed daily
- Uber (2016): Private keys in GitHub repo
- Toyota (2022): 296GB source code with secrets leaked

**Correct Approach**:
```typescript
// ALWAYS DO THIS - Use environment variables
const API_KEY = process.env.API_KEY;
const DATABASE_PASSWORD = process.env.DATABASE_PASSWORD;
const JWT_SECRET = process.env.JWT_SECRET;

// Or use secret management service
import { SecretsManager } from '@aws-sdk/client-secrets-manager';

const secret = await secretsManager.getSecretValue({
  SecretId: 'prod/api/key'
});
```

### 5. Disabled or Missing HTTPS

**Anti-Pattern**:
```typescript
// NEVER DO THIS in production
const server = http.createServer(app);
server.listen(80);

// Or worse: ignoring certificate errors
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
```

**Why It's Dangerous**:
- All traffic sent in plain text
- Passwords intercepted on network
- Session cookies stolen (session hijacking)
- Man-in-the-middle attacks trivial
- No data integrity guarantees

**Correct Approach**:
```typescript
// ALWAYS DO THIS in production
import https from 'https';
import fs from 'fs';

const options = {
  key: fs.readFileSync('private-key.pem'),
  cert: fs.readFileSync('certificate.pem')
};

const server = https.createServer(options, app);
server.listen(443);

// Redirect HTTP to HTTPS
const httpServer = http.createServer((req, res) => {
  res.writeHead(301, { Location: `https://${req.headers.host}${req.url}` });
  res.end();
});
httpServer.listen(80);
```

## Authentication Anti-Patterns

### 6. Weak Password Requirements

**Anti-Pattern**:
```typescript
// NEVER DO THIS
function validatePassword(password: string): boolean {
  return password.length >= 6;  // Way too short!
}

// Or overly complex rules that don't help
function validatePassword(password: string): boolean {
  return /[A-Z]/.test(password) &&  // Forces Password1!
         /[a-z]/.test(password) &&
         /[0-9]/.test(password) &&
         /[!@#$]/.test(password) &&
         password.length >= 8;
}
```

**Why It's Dangerous**:
- Short passwords easily brute-forced
- Complex rules lead to predictable patterns
- Users write down complex passwords
- Doesn't check against breach databases

**Correct Approach**:
```typescript
// ALWAYS DO THIS
import zxcvbn from 'zxcvbn';

async function validatePassword(password: string): Promise<{valid: boolean, reason?: string}> {
  // Minimum length
  if (password.length < 12) {
    return { valid: false, reason: 'Minimum 12 characters required' };
  }

  // Check password strength
  const strength = zxcvbn(password);
  if (strength.score < 3) {
    return { valid: false, reason: strength.feedback.suggestions.join('. ') };
  }

  // Check against breach database
  const isCompromised = await checkHaveIBeenPwned(password);
  if (isCompromised) {
    return { valid: false, reason: 'Password found in data breach' };
  }

  return { valid: true };
}
```

### 7. No Rate Limiting on Authentication

**Anti-Pattern**:
```typescript
// NEVER DO THIS
app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  const user = await authenticateUser(username, password);

  if (user) {
    res.json({ success: true, user });
  } else {
    res.status(401).json({ error: 'Invalid credentials' });
  }
  // No rate limiting - infinite attempts allowed!
});
```

**Why It's Dangerous**:
- Brute force attacks succeed
- Credential stuffing attacks
- Account enumeration possible
- Server resource exhaustion
- No detection of attacks

**Correct Approach**:
```typescript
// ALWAYS DO THIS
import rateLimit from 'express-rate-limit';

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5,                    // 5 attempts
  skipSuccessfulRequests: true,
  standardHeaders: true,
  message: 'Too many login attempts, please try again later'
});

app.post('/login', loginLimiter, async (req, res) => {
  const { username, password } = req.body;

  // Add delay for failed attempts (timing attack mitigation)
  const user = await authenticateUser(username, password);

  if (!user) {
    // Consistent timing for invalid credentials
    await new Promise(resolve => setTimeout(resolve, 1000));
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  res.json({ success: true, user });
});
```

### 8. Exposing User Enumeration

**Anti-Pattern**:
```typescript
// NEVER DO THIS
app.post('/login', async (req, res) => {
  const user = await findUser(req.body.username);

  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }

  const isValid = await verifyPassword(req.body.password, user.passwordHash);

  if (!isValid) {
    return res.status(401).json({ error: 'Invalid password' });
  }

  res.json({ success: true });
});
```

**Why It's Dangerous**:
- Attackers can enumerate valid usernames
- Different responses leak information
- Timing differences leak existence
- Makes targeted attacks easier

**Correct Approach**:
```typescript
// ALWAYS DO THIS - Same response for all failures
app.post('/login', loginLimiter, async (req, res) => {
  const { username, password } = req.body;

  const user = await findUser(username);

  // Always hash password even if user doesn't exist (timing attack)
  if (!user) {
    // Hash a dummy value to maintain consistent timing
    await argon2.hash('dummy-password');
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const isValid = await argon2.verify(user.passwordHash, password);

  if (!isValid) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // Same generic message for all failures
  res.json({ success: true });
});
```

## Session Management Anti-Patterns

### 9. Not Regenerating Session ID After Login

**Anti-Pattern**:
```typescript
// NEVER DO THIS
app.post('/login', async (req, res) => {
  const user = await authenticateUser(req.body);

  // Just set user in existing session - WRONG!
  req.session.user = user;

  res.json({ success: true });
});
```

**Why It's Dangerous**:
- Session fixation attacks succeed
- Attacker can set session ID beforehand
- Victim logs in with attacker's session ID
- Attacker has access to victim's session

**Correct Approach**:
```typescript
// ALWAYS DO THIS
app.post('/login', async (req, res) => {
  const user = await authenticateUser(req.body);

  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // CRITICAL: Regenerate session ID after authentication
  req.session.regenerate((err) => {
    if (err) {
      return res.status(500).json({ error: 'Session error' });
    }

    req.session.user = user;
    req.session.createdAt = Date.now();

    res.json({ success: true, user });
  });
});
```

### 10. Storing Sensitive Data in JWT

**Anti-Pattern**:
```typescript
// NEVER DO THIS
const token = jwt.sign({
  userId: user.id,
  email: user.email,
  creditCard: '4532-1234-5678-9010',  // NEVER!
  ssn: '123-45-6789',                 // NEVER!
  passwordHash: user.passwordHash      // NEVER!
}, JWT_SECRET);
```

**Why It's Dangerous**:
- JWT is base64 encoded, not encrypted
- Anyone can decode JWT and read data
- JWTs are logged, cached, stored client-side
- Can't remove data after token issued

**Correct Approach**:
```typescript
// ALWAYS DO THIS - Minimal, non-sensitive claims only
const token = jwt.sign({
  sub: user.id,           // User ID only
  role: user.role,        // Role for authorization
  iat: Math.floor(Date.now() / 1000),
  exp: Math.floor(Date.now() / 1000) + (15 * 60)  // 15 min expiry
}, JWT_SECRET);

// Fetch sensitive data from database when needed
```

## Input Validation Anti-Patterns

### 11. Trusting Client Input

**Anti-Pattern**:
```typescript
// NEVER DO THIS
app.post('/api/users', async (req, res) => {
  // Trust everything from client
  const user = req.body;
  await db.insert('users', user);  // User could set role=admin!
  res.json({ success: true });
});
```

**Why It's Dangerous**:
- Mass assignment vulnerabilities
- Privilege escalation
- Data type mismatches
- Required fields missing
- Database injection

**Correct Approach**:
```typescript
// ALWAYS DO THIS - Validate and sanitize
import { z } from 'zod';

const CreateUserSchema = z.object({
  username: z.string().min(3).max(50),
  email: z.string().email(),
  password: z.string().min(12),
  // Explicitly list allowed fields
  // Role NOT included - set server-side
});

app.post('/api/users', async (req, res) => {
  // Validate input
  const result = CreateUserSchema.safeParse(req.body);

  if (!result.success) {
    return res.status(400).json({ errors: result.error.errors });
  }

  // Server controls sensitive fields
  const user = {
    ...result.data,
    role: 'user',  // Server-side default
    createdAt: new Date(),
    isActive: true
  };

  const hashedPassword = await argon2.hash(user.password);
  await db.insert('users', { ...user, passwordHash: hashedPassword });

  res.json({ success: true });
});
```

### 12. Blacklist Input Validation

**Anti-Pattern**:
```typescript
// NEVER DO THIS
function sanitizeInput(input: string): string {
  // Trying to block malicious patterns (blacklist approach)
  return input
    .replace(/<script>/gi, '')
    .replace(/SELECT/gi, '')
    .replace(/DROP/gi, '')
    .replace(/--/g, '');
}

// Easy to bypass: <scr<script>ipt>, SeLeCt, DROP TABLE
```

**Why It's Dangerous**:
- Blacklists are incomplete
- Attackers find bypasses
- Case sensitivity bypasses
- Encoding bypasses (URL, Unicode, etc.)
- False sense of security

**Correct Approach**:
```typescript
// ALWAYS DO THIS - Whitelist approach
import { z } from 'zod';
import DOMPurify from 'isomorphic-dompurify';

// Whitelist validation - only allow known good
const UsernameSchema = z.string()
  .min(3).max(50)
  .regex(/^[a-zA-Z0-9_-]+$/); // Only alphanumeric, underscore, hyphen

// For HTML content - use sanitizer
function sanitizeHTML(html: string): string {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['p', 'br', 'strong', 'em'],
    ALLOWED_ATTR: []
  });
}

// Use parameterized queries (SQL injection)
// Use ORM safely (prevents injection)
```

## Error Handling Anti-Patterns

### 13. Verbose Error Messages

**Anti-Pattern**:
```typescript
// NEVER DO THIS
app.post('/login', async (req, res) => {
  try {
    const user = await db.query(
      'SELECT * FROM users WHERE email = $1',
      [req.body.email]
    );
    // ... authentication logic
  } catch (error) {
    // Exposing internal details
    res.status(500).json({
      error: error.message,           // Don't expose!
      stack: error.stack,              // NEVER expose!
      query: 'SELECT * FROM users...', // Don't expose!
      database: 'postgres://prod...'   // NEVER expose!
    });
  }
});
```

**Why It's Dangerous**:
- Reveals internal implementation
- Exposes database structure
- Shows file paths and versions
- Helps attackers plan attacks
- Leaks sensitive configuration

**Correct Approach**:
```typescript
// ALWAYS DO THIS
app.post('/login', async (req, res) => {
  try {
    const user = await authenticateUser(req.body);
    res.json({ success: true, user });
  } catch (error) {
    // Log detailed error server-side
    console.error('Login error:', {
      error: error.message,
      stack: error.stack,
      timestamp: new Date().toISOString(),
      ip: req.ip,
      userAgent: req.headers['user-agent']
    });

    // Generic message to client
    res.status(500).json({
      error: 'An error occurred',
      code: 'INTERNAL_ERROR'
    });
  }
});
```

### 14. Catch-All Exception Handlers

**Anti-Pattern**:
```typescript
// NEVER DO THIS
try {
  // Some operation
  await dangerousOperation();
} catch (error) {
  // Swallow all errors silently
  console.log('Error occurred');
  // No handling, no logging, no alerting
}

// Or worse
process.on('uncaughtException', (error) => {
  console.log('Caught error, ignoring...');
  // Continue running - DANGEROUS!
});
```

**Why It's Dangerous**:
- Masks security issues
- Application in inconsistent state
- Data corruption possible
- No visibility into problems
- Makes debugging impossible

**Correct Approach**:
```typescript
// ALWAYS DO THIS
try {
  await operation();
} catch (error) {
  if (error instanceof ValidationError) {
    return res.status(400).json({ error: error.message });
  }

  if (error instanceof AuthenticationError) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  // Log unexpected errors
  logger.error('Unexpected error:', {
    error: error.message,
    stack: error.stack,
    context: { /* relevant data */ }
  });

  // Alert on critical errors
  await alerting.notify('Critical error in operation');

  res.status(500).json({ error: 'Internal server error' });
}

// Global uncaught exception handler
process.on('uncaughtException', (error) => {
  logger.fatal('Uncaught exception:', error);
  alerting.notifyUrgent('Application crash', error);

  // Graceful shutdown
  server.close(() => {
    process.exit(1);
  });
});
```

## CORS Anti-Patterns

### 15. Wildcard CORS with Credentials

**Anti-Pattern**:
```typescript
// NEVER DO THIS
app.use(cors({
  origin: '*',                    // Allow all origins
  credentials: true               // AND allow credentials - DANGER!
}));

// This combination is actually blocked by browsers, but attempting it shows misunderstanding
```

**Why It's Dangerous**:
- Would allow any site to make authenticated requests
- Complete bypass of same-origin policy
- User's credentials stolen
- CSRF attacks trivial

**Correct Approach**:
```typescript
// ALWAYS DO THIS
const ALLOWED_ORIGINS = [
  'https://myapp.com',
  'https://www.myapp.com',
  ...(process.env.NODE_ENV === 'development' ? ['http://localhost:3000'] : [])
];

app.use(cors({
  origin: (origin, callback) => {
    // Allow requests with no origin (mobile apps, curl, etc.)
    if (!origin) return callback(null, true);

    if (ALLOWED_ORIGINS.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  maxAge: 86400  // 24 hours
}));
```

## Dependency Anti-Patterns

### 16. Ignoring Dependency Updates

**Anti-Pattern**:
```typescript
// NEVER DO THIS
// package.json unchanged for years
{
  "dependencies": {
    "express": "4.16.0",        // 4 years old
    "jsonwebtoken": "8.0.0",    // Has known vulnerabilities
    "mongoose": "5.0.0"          // Missing security patches
  }
}

// Never running npm audit
// Ignoring security warnings
```

**Why It's Dangerous**:
- Known vulnerabilities exploited
- Missing security patches
- Compliance violations
- Technical debt compounds
- Eventually forced emergency upgrade

**Correct Approach**:
```typescript
// ALWAYS DO THIS
// Regularly update dependencies
npm audit fix
npm outdated
npm update

// Use automated tools
// - Dependabot (GitHub)
// - Snyk
// - npm audit in CI/CD

// CI pipeline
"scripts": {
  "security-check": "npm audit --audit-level=moderate && npm outdated"
}

// .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

## Testing Anti-Patterns

### 17. No Security Testing

**Anti-Pattern**:
```typescript
// NEVER DO THIS
// Only testing happy paths
describe('User API', () => {
  it('should create user', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ username: 'test', password: 'test123' });

    expect(res.status).toBe(200);
  });

  // No security tests!
});
```

**Why It's Dangerous**:
- Security bugs go unnoticed
- Vulnerabilities shipped to production
- No regression testing for security
- False confidence in security

**Correct Approach**:
```typescript
// ALWAYS DO THIS
describe('User API Security', () => {
  describe('Authentication', () => {
    it('should reject requests without authentication', async () => {});
    it('should reject invalid JWTs', async () => {});
    it('should reject expired tokens', async () => {});
  });

  describe('Authorization', () => {
    it('should prevent privilege escalation', async () => {});
    it('should enforce role-based access', async () => {});
    it('should prevent horizontal privilege escalation', async () => {});
  });

  describe('Input Validation', () => {
    it('should reject SQL injection attempts', async () => {});
    it('should reject XSS attempts', async () => {});
    it('should validate input types', async () => {});
    it('should enforce input length limits', async () => {});
  });

  describe('Rate Limiting', () => {
    it('should block after 5 failed login attempts', async () => {});
    it('should enforce API rate limits', async () => {});
  });

  describe('Session Security', () => {
    it('should regenerate session ID after login', async () => {});
    it('should expire sessions after timeout', async () => {});
    it('should invalidate session on logout', async () => {});
  });
});
```

## Logging Anti-Patterns

### 18. Logging Sensitive Data

**Anti-Pattern**:
```typescript
// NEVER DO THIS
app.post('/login', async (req, res) => {
  console.log('Login attempt:', {
    username: req.body.username,
    password: req.body.password,        // NEVER log passwords!
    creditCard: req.body.creditCard,    // NEVER log payment info!
    ssn: req.body.ssn                    // NEVER log PII!
  });

  // Or in error logs
  logger.error('User data:', user);  // Might contain sensitive fields
});
```

**Why It's Dangerous**:
- Credentials exposed in logs
- Violates data protection laws (GDPR, CCPA)
- Log files often widely accessible
- Logs stored unencrypted
- Log aggregation exposes data

**Correct Approach**:
```typescript
// ALWAYS DO THIS
app.post('/login', async (req, res) => {
  // Log only non-sensitive information
  logger.info('Login attempt:', {
    username: req.body.username,  // Username OK
    ip: req.ip,
    userAgent: req.headers['user-agent'],
    timestamp: new Date().toISOString()
    // NO password, NO tokens, NO PII
  });

  // Sanitize objects before logging
  function sanitizeUser(user: User): Record<string, any> {
    const { password, passwordHash, ssn, creditCard, ...safe } = user;
    return safe;
  }

  logger.info('User created:', sanitizeUser(user));
});
```

## Deployment Anti-Patterns

### 19. Debug Mode in Production

**Anti-Pattern**:
```typescript
// NEVER DO THIS
const app = express();
app.set('env', 'development');  // In production!

// Or
process.env.NODE_ENV = 'development';  // In production!

// Or keeping debug endpoints
app.get('/debug/users', (req, res) => {
  res.json(allUsers);  // Exposed in production!
});
```

**Why It's Dangerous**:
- Verbose error messages leak info
- Debug endpoints exposed
- Performance degraded
- Additional attack surface
- Stack traces revealed

**Correct Approach**:
```typescript
// ALWAYS DO THIS
// Set NODE_ENV=production
process.env.NODE_ENV = 'production';

// Remove/disable debug routes in production
if (process.env.NODE_ENV !== 'production') {
  app.get('/debug/users', debugUsersHandler);
}

// Different error handling by environment
if (process.env.NODE_ENV === 'production') {
  app.use((err, req, res, next) => {
    logger.error(err);
    res.status(500).json({ error: 'Internal server error' });
  });
} else {
  app.use((err, req, res, next) => {
    res.status(500).json({
      error: err.message,
      stack: err.stack
    });
  });
}
```

### 20. No Security Headers

**Anti-Pattern**:
```typescript
// NEVER DO THIS
const app = express();
// No security headers configured
app.get('/', (req, res) => {
  res.send('<h1>Hello World</h1>');
});

// Vulnerable to XSS, clickjacking, etc.
```

**Why It's Dangerous**:
- XSS attacks possible
- Clickjacking attacks
- MIME sniffing vulnerabilities
- No HTTPS enforcement
- Missing basic protections

**Correct Approach**:
```typescript
// ALWAYS DO THIS
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:'],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  },
  frameguard: { action: 'deny' },
  noSniff: true,
  xssFilter: true,
}));
```

## Summary Checklist

Use this checklist to avoid common anti-patterns:

### Authentication & Authorization
- [ ] Never store passwords in plain text
- [ ] Never use weak hashing (MD5, SHA-256 alone)
- [ ] Always implement rate limiting on auth endpoints
- [ ] Always regenerate session ID after login
- [ ] Never trust client-side authorization
- [ ] Always validate on server-side

### Input & Data
- [ ] Never concatenate SQL queries with user input
- [ ] Never trust client input without validation
- [ ] Always use whitelist validation (not blacklist)
- [ ] Never log sensitive data (passwords, tokens, PII)
- [ ] Always sanitize output to prevent XSS

### Sessions & Tokens
- [ ] Never store sensitive data in JWT payload
- [ ] Always set HttpOnly and Secure flags on cookies
- [ ] Never expose session tokens in URLs
- [ ] Always implement session timeout
- [ ] Never use predictable session IDs

### Configuration
- [ ] Never hardcode secrets in code
- [ ] Never commit secrets to version control
- [ ] Always use HTTPS in production
- [ ] Always set security headers
- [ ] Never run debug mode in production

### Error Handling
- [ ] Never expose stack traces to clients
- [ ] Never reveal database errors to clients
- [ ] Always log errors server-side
- [ ] Never swallow exceptions silently

### Dependencies
- [ ] Never ignore security updates
- [ ] Always run npm audit regularly
- [ ] Never use packages with known vulnerabilities
- [ ] Always pin dependency versions

## References

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OWASP Cheat Sheets: https://cheatsheetseries.owasp.org/
- CWE Top 25: https://cwe.mitre.org/top25/
- Security Anti-Patterns: https://www.securecoding.cert.org/

## Related Documentation

- [SECURITY_OVERVIEW.md](./SECURITY_OVERVIEW.md) - OWASP Top 10 and principles
- [PASSWORD_SECURITY.md](./PASSWORD_SECURITY.md) - Proper password handling
- [SESSION_MANAGEMENT.md](./SESSION_MANAGEMENT.md) - Secure session patterns
- [INPUT_VALIDATION.md](./INPUT_VALIDATION.md) - Validation best practices
- [SECURITY_TESTING.md](./SECURITY_TESTING.md) - Testing security controls
