# Security Best Practices

Created: 2025-10-13

## Overview

Essential security patterns for Node.js backends.

## Security Headers (Helmet)

```typescript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: true,
  hsts: { maxAge: 31536000 },
  noSniff: true,
  xssFilter: true,
}));
```

## CORS Configuration

```typescript
import cors from 'cors';

app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(','),
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
}));
```

## Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: 'Too many requests',
});

app.use('/api', limiter);
```

## Input Validation

```typescript
// Always validate and sanitize
app.post('/users', validate(createUserSchema), handler);
```

## SQL Injection Prevention

```typescript
// Always use parameterized queries
const result = await pool.query(
  'SELECT * FROM users WHERE id = $1',
  [userId] // Never string concatenation!
);
```

## XSS Prevention

```typescript
// Escape user content before rendering
import escape from 'escape-html';

const safe = escape(userInput);
```

## CSRF Protection

```typescript
import csurf from 'csurf';

app.use(csurf({ cookie: true }));
```

## Best Practices

1. **Always use HTTPS**: In production
2. **Secure cookies**: httpOnly, secure, sameSite
3. **Hash passwords**: Use bcrypt
4. **Validate inputs**: All user data
5. **Rate limit**: Prevent abuse
6. **Security headers**: Use helmet
7. **Keep dependencies updated**: Regular updates
8. **Environment variables**: Never commit secrets

See AUTHENTICATION.md and VALIDATION.md.
