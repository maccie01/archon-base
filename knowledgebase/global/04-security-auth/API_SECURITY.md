# Research Result: 09_API_SECURITY


# API SECURITY Patterns

Created: 2025-10-13
Last Updated: 2025-10-14

## Authentication vs Authorization

**Authentication** verifies client identity; **Authorization** determines access rights based on identity. Both are crucial in API security.

- Authentication: login, tokens, API keys.
- Authorization: role-based access control (RBAC), permissions, scopes.

## API Keys vs OAuth Tokens vs JWT

| Mechanism   | Use Case                      | Lifespan          | Revocation          |
| ----------- | ----------------------------- | ----------------- | ------------------- |
| API Key     | Simple service access         | Long-lived        | Manual rotate       |
| OAuth Token | User consent, third-party     | Short-lived (min) | Refresh or revoke   |
| JWT         | Stateless auth, microservices | Short-lived       | Blacklist or expiry |

### Example: API Key Validation

```typescript
// apiKeyMiddleware.ts
import { Request, Response, NextFunction } from 'express';
const validKeys = new Set([process.env.API_KEY]);

export function apiKeyMiddleware(req: Request, res: Response, next: NextFunction) {
  const apiKey = req.header('x-api-key');
  if (!apiKey || !validKeys.has(apiKey)) {
    return res.status(401).json({ error: 'Invalid API key' });
  }
  next();
}
```

## Request Signing and HMAC

Ensure integrity and authenticity by signing requests with a secret key using HMAC (SHA256).

```typescript
// signing.ts
import crypto from 'crypto';

export function signRequest(body: string, secret: string) {
  return crypto.createHmac('sha256', secret).update(body).digest('hex');
}

export function verifySignature(reqBody: string, signature: string, secret: string) {
  const expected = signRequest(reqBody, secret);
  return crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(signature));
}
```

## Idempotency Keys

Prevent duplicate operations by requiring a unique idempotency key per request.

```typescript
// idempotency.ts
import { Request, Response, NextFunction } from 'express';
const store = new Map<string, any>();

export function idempotencyMiddleware(req: Request, res: Response, next: NextFunction) {
  const key = req.header('Idempotency-Key');
  if (!key) return res.status(400).json({ error: 'Missing Idempotency-Key' });

  if (store.has(key)) {
    const cached = store.get(key);
    return res.status(cached.status).json(cached.body);
  }

  const originalSend = res.send.bind(res);
  res.send = (body: any) => {
    store.set(key, { status: res.statusCode, body });
    return originalSend(body);
  };
  next();
}
```

## API Versioning Strategies

- **URL Versioning**: `/api/v1/resource`
- **Header Versioning**: `Accept: application/vnd.app.v2+json`
- **Parameter Versioning**: `/api/resource?version=2`
- **Media Type Versioning**: Content negotiation.

## Error Handling (Don’t Leak Info)

Avoid exposing stack traces or internal errors. Provide generic messages.

```typescript
// errorHandler.ts
import { Request, Response, NextFunction } from 'express';
export function errorHandler(err: any, req: Request, res: Response, next: NextFunction) {
  console.error(err);
  const status = err.status || 500;
  res.status(status).json({ error: status === 500 ? 'Internal Server Error' : err.message });
}
```

## Rate Limiting Integration

Integrate rate limiting middleware to protect against brute force and abuse.

```typescript
import { redisLimiter } from './rateLimiter';
app.use(redisLimiter);
```

## API Gateway Patterns

Use API Gateway (e.g., AWS API Gateway) to centralize:

- Authentication
- Rate limiting
- Request validation
- Routing to microservices

## Express.js Auth Middleware Example

```typescript
// authMiddleware.ts
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

export interface AuthPayload { userId: string; roles: string[]; }

export function authMiddleware(req: Request, res: Response, next: NextFunction) {
  const token = req.header('Authorization')?.replace('Bearer ', '');
  if (!token) return res.status(401).json({ error: 'Missing token' });

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET) as AuthPayload;
    req.user = payload;
    next();
  } catch (err) {
    return res.status(401).json({ error: 'Invalid token' });
  }
}
```

## Idempotency Implementation Example

```typescript
app.post('/payments', idempotencyMiddleware, (req, res) => {
  // Process payment
  res.json({ success: true });
});
```

## Secure Error Responses

```typescript
app.get('/data', async (req, res, next) => {
  try {
    const data = await fetchData();
    res.json(data);
  } catch (err) {
    next({ status: 502, message: 'Bad Gateway' });
  }
});
app.use(errorHandler);
```

## Common Pitfalls

- ❌ **Exposing stack traces** in production
- ❌ **Using long-lived tokens** without refresh/invalidation
- ❌ **Skipping signature verification** for webhooks
- ❌ **Not enforcing idempotency** for critical endpoints
- ❌ **Hardcoding secrets** in code

## Testing Examples

```typescript
// jest test authMiddleware
import request from 'supertest';
import app from '../app';

describe('Auth', () => {
  it('rejects missing token', async () => {
    const res = await request(app).get('/secure');
    expect(res.status).toBe(401);
  });
});
```

## Security Considerations

- Rotate API keys and secrets regularly.
- Use HTTPS for all endpoints.
- Enforce least privilege in scopes and roles.
- Log and monitor auth failures.
- Throttle login and sensitive operations.

## References

1. OWASP API Security Top 10
2. RFC 7231 (HTTP Semantics)
3. JWT RFC 7519
4. HMAC (RFC 2104)
5. express-rate-limit documentation
