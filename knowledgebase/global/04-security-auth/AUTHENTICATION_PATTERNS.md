# Authentication Patterns

Created: 2025-10-13
Status: Research Phase - Skeleton

## Overview
Comprehensive guide to authentication patterns for Node.js/Express applications, covering various approaches from session-based to modern token-based authentication.

## Authentication Methods Comparison

### Session-Based Authentication
**Use Cases**: Traditional web applications, server-side rendered apps
**Pros**:
- Server-side session control
- Easy session invalidation
- Familiar pattern
- Built-in CSRF protection

**Cons**:
- Server memory/storage requirements
- Scalability challenges
- Not ideal for mobile/API-first apps

**Implementation Pattern**:
```typescript
// Skeleton: express-session configuration
import session from 'express-session';
import RedisStore from 'connect-redis';
import { createClient } from 'redis';

// Session store configuration
const redisClient = createClient({
  // Configuration
});

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true, // HTTPS only
    httpOnly: true, // No JS access
    maxAge: 1000 * 60 * 60 * 24, // 24 hours
    sameSite: 'strict' // CSRF protection
  }
}));
```

### JWT Authentication
**Use Cases**: Stateless APIs, microservices, mobile apps, SPAs
**Pros**:
- Stateless (no server storage)
- Scalable across services
- Mobile-friendly
- Cross-domain support

**Cons**:
- Cannot invalidate tokens before expiry
- Token size (stored in every request)
- Refresh token complexity

**Implementation Pattern**:
```typescript
// Skeleton: JWT generation and verification
import jwt from 'jsonwebtoken';

interface JWTPayload {
  userId: string;
  email: string;
  role: string;
}

// Generate access token (short-lived)
function generateAccessToken(payload: JWTPayload): string {
  return jwt.sign(
    payload,
    process.env.JWT_SECRET!,
    { expiresIn: '15m', algorithm: 'HS256' }
  );
}

// Generate refresh token (long-lived)
function generateRefreshToken(payload: JWTPayload): string {
  return jwt.sign(
    payload,
    process.env.JWT_REFRESH_SECRET!,
    { expiresIn: '7d', algorithm: 'HS256' }
  );
}

// Verification middleware
function verifyToken(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;
  const token = authHeader?.split(' ')[1]; // Bearer TOKEN

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as JWTPayload;
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(403).json({ error: 'Invalid token' });
  }
}
```

### OAuth 2.0 / OpenID Connect
**Use Cases**: Third-party authentication, social login, enterprise SSO
**Pros**:
- Delegate authentication responsibility
- No password storage
- Industry standard
- User convenience

**Implementation Pattern**:
```typescript
// Skeleton: OAuth 2.0 with Passport.js
import passport from 'passport';
import { Strategy as GoogleStrategy } from 'passport-google-oauth20';

passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID!,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    callbackURL: '/auth/google/callback'
  },
  async (accessToken, refreshToken, profile, done) => {
    // Find or create user
    // Return user object
  }
));

// Routes
app.get('/auth/google',
  passport.authenticate('google', { scope: ['profile', 'email'] })
);

app.get('/auth/google/callback',
  passport.authenticate('google', { failureRedirect: '/login' }),
  (req, res) => {
    // Successful authentication
    res.redirect('/dashboard');
  }
);
```

## Multi-Factor Authentication (MFA)

### TOTP (Time-based One-Time Password)
```typescript
// Skeleton: TOTP implementation with speakeasy
import speakeasy from 'speakeasy';
import QRCode from 'qrcode';

// Generate MFA secret for user
async function setupMFA(userId: string) {
  const secret = speakeasy.generateSecret({
    name: `MyApp (${userId})`,
    length: 32
  });

  // Store secret.base32 in database
  // Generate QR code for user
  const qrCodeUrl = await QRCode.toDataURL(secret.otpauth_url!);

  return { secret: secret.base32, qrCode: qrCodeUrl };
}

// Verify TOTP token
function verifyMFAToken(secret: string, token: string): boolean {
  return speakeasy.totp.verify({
    secret,
    encoding: 'base32',
    token,
    window: 2 // Allow 2 steps before/after
  });
}
```

### SMS-Based MFA
```typescript
// Skeleton: SMS OTP
interface SMSOTPService {
  generateOTP(): string;
  sendOTP(phoneNumber: string, otp: string): Promise<void>;
  verifyOTP(userId: string, otp: string): boolean;
}

// Store OTPs with expiration (Redis recommended)
// Implement rate limiting to prevent abuse
```

## Passwordless Authentication

### Magic Link
```typescript
// Skeleton: Email magic link
import crypto from 'crypto';

interface MagicLinkService {
  generateMagicLink(email: string): Promise<string>;
  verifyMagicLink(token: string): Promise<User | null>;
}

async function generateMagicLink(email: string): Promise<string> {
  const token = crypto.randomBytes(32).toString('hex');

  // Store token with expiration (15 minutes)
  await storeToken(email, token, 15 * 60);

  const magicLink = `${process.env.APP_URL}/auth/verify?token=${token}`;
  // Send email with magic link

  return magicLink;
}
```

### WebAuthn / FIDO2
```typescript
// Skeleton: WebAuthn implementation
import {
  generateRegistrationOptions,
  verifyRegistrationResponse,
  generateAuthenticationOptions,
  verifyAuthenticationResponse
} from '@simplewebauthn/server';

// Registration
async function startRegistration(userId: string) {
  const options = generateRegistrationOptions({
    rpName: 'MyApp',
    rpID: 'example.com',
    userID: userId,
    userName: user.email,
    attestationType: 'none'
  });

  // Store challenge temporarily
  return options;
}

// Authentication
async function startAuthentication(userId: string) {
  const options = generateAuthenticationOptions({
    rpID: 'example.com',
    allowCredentials: user.credentials // From database
  });

  return options;
}
```

## Token Refresh Strategies

### Refresh Token Rotation
```typescript
// Skeleton: Secure refresh token rotation
interface TokenPair {
  accessToken: string;
  refreshToken: string;
}

async function refreshTokens(oldRefreshToken: string): Promise<TokenPair> {
  // Verify old refresh token
  const decoded = jwt.verify(oldRefreshToken, process.env.JWT_REFRESH_SECRET!);

  // Check if refresh token is in database (not blacklisted)
  const tokenExists = await checkRefreshToken(decoded.userId, oldRefreshToken);
  if (!tokenExists) {
    throw new Error('Invalid refresh token');
  }

  // Generate new token pair
  const newAccessToken = generateAccessToken(decoded);
  const newRefreshToken = generateRefreshToken(decoded);

  // Store new refresh token, invalidate old one (rotation)
  await rotateRefreshToken(decoded.userId, oldRefreshToken, newRefreshToken);

  return { accessToken: newAccessToken, refreshToken: newRefreshToken };
}
```

### Sliding Sessions
```typescript
// Skeleton: Automatic session extension
app.use((req, res, next) => {
  if (req.session && req.session.user) {
    // Extend session if activity detected
    req.session.touch();
  }
  next();
});
```

## Security Considerations

### Token Storage
- Access tokens: Memory only (never localStorage for sensitive apps)
- Refresh tokens: httpOnly cookies or secure storage
- Never expose tokens in URLs

### Token Expiration
- Access tokens: 15 minutes to 1 hour
- Refresh tokens: 7-30 days
- Session tokens: Based on risk assessment

### Brute Force Protection
```typescript
// Skeleton: Rate limiting login attempts
import rateLimit from 'express-rate-limit';

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: 'Too many login attempts, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
  // Store in Redis for distributed systems
});

app.post('/login', loginLimiter, loginHandler);
```

## Anti-Patterns to Avoid

1. Storing passwords in plain text
2. Using weak session secrets
3. Not implementing token expiration
4. Storing JWT in localStorage (XSS risk)
5. Not validating token signatures
6. Using predictable session IDs
7. Not implementing refresh token rotation
8. Mixing authentication methods inconsistently

## Common Vulnerabilities

- Session fixation
- Token leakage
- Replay attacks
- Timing attacks
- Credential stuffing
- Session hijacking
- Token prediction

## Industry Standards

- OWASP Authentication Cheat Sheet
- NIST Digital Identity Guidelines (SP 800-63B)
- OAuth 2.0 RFC 6749
- OpenID Connect Core 1.0
- JWT RFC 7519
- WebAuthn W3C Recommendation

## Testing Authentication

```typescript
// Skeleton: Authentication tests
describe('Authentication', () => {
  describe('JWT Authentication', () => {
    it('should generate valid access token', () => {});
    it('should reject expired tokens', () => {});
    it('should reject invalid signatures', () => {});
    it('should implement token refresh', () => {});
  });

  describe('Session Authentication', () => {
    it('should create session on login', () => {});
    it('should destroy session on logout', () => {});
    it('should prevent session fixation', () => {});
  });

  describe('MFA', () => {
    it('should verify valid TOTP tokens', () => {});
    it('should reject invalid tokens', () => {});
    it('should handle token expiration', () => {});
  });
});
```

## References

- OWASP Authentication Cheat Sheet
- Auth0 Blog on Authentication Best Practices
- NIST Digital Identity Guidelines
- JWT.io Best Practices
- WebAuthn Guide
- OAuth 2.0 Security Best Current Practice
