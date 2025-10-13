# Authentication Patterns

Created: 2025-10-13
Last Updated: 2025-10-13

## Overview

Authentication verifies user identity. Choose between session-based and token-based (JWT) approaches.

## Session-Based Authentication (Recommended for Server-Rendered)

```typescript
import session from 'express-session';
import bcrypt from 'bcrypt';

// Setup
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    maxAge: 24 * 60 * 60 * 1000, // 24 hours
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
  },
}));

// Login
export const login = asyncHandler(async (req, res) => {
  const { username, password } = req.body;

  const user = await userRepository.findByUsername(username);
  
  if (!user) {
    // Prevent timing attacks
    await bcrypt.compare(password, '$2b$12$dummy');
    throw createAuthError('Invalid credentials');
  }

  const isValid = await bcrypt.compare(password, user.password);
  
  if (!isValid) {
    throw createAuthError('Invalid credentials');
  }

  req.session.user = {
    id: user.id,
    email: user.email,
    role: user.role,
  };

  res.json({ message: 'Login successful', user });
});

// Logout
export const logout = asyncHandler(async (req, res) => {
  req.session.destroy((err) => {
    if (err) throw err;
    res.json({ message: 'Logged out' });
  });
});

// Auth Middleware
export function requireAuth(req, res, next) {
  if (!req.session?.user) {
    throw createAuthError('Authentication required');
  }
  next();
}
```

## JWT-Based Authentication

```typescript
import jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET;
const JWT_EXPIRES_IN = '24h';

// Login
export const login = asyncHandler(async (req, res) => {
  const { username, password } = req.body;

  const user = await authService.validateCredentials(username, password);

  if (!user) {
    throw createAuthError('Invalid credentials');
  }

  const token = jwt.sign(
    { id: user.id, email: user.email, role: user.role },
    JWT_SECRET,
    { expiresIn: JWT_EXPIRES_IN }
  );

  res.json({ token, user });
});

// Auth Middleware
export function requireAuth(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    throw createAuthError('No token provided');
  }

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    throw createAuthError('Invalid token');
  }
}
```

## Password Hashing

```typescript
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12;

// Hash password
export async function hashPassword(password: string): Promise<string> {
  return await bcrypt.hash(password, SALT_ROUNDS);
}

// Verify password
export async function verifyPassword(
  password: string,
  hash: string
): Promise<boolean> {
  return await bcrypt.compare(password, hash);
}

// Prevent timing attacks
export async function safeVerifyPassword(
  password: string,
  hash: string | null
): Promise<boolean> {
  if (!hash) {
    await bcrypt.compare(password, '$2b$12$dummy');
    return false;
  }
  return await bcrypt.compare(password, hash);
}
```

## Best Practices

1. **Use bcrypt**: Never store plain text passwords
2. **Timing Attack Prevention**: Always hash even for non-existent users
3. **Secure Cookies**: httpOnly, secure, sameSite
4. **Session Management**: Implement timeouts and heartbeats
5. **Strong Secrets**: Use cryptographically random secrets
6. **HTTPS Only**: Always use HTTPS in production

## Additional Resources

- See AUTHORIZATION.md for access control
- See SECURITY.md for security best practices
- See MIDDLEWARE_PATTERNS.md for auth middleware
