# Research Result: 03_RATE_LIMITING


# Rate Limiting Patterns

Created: 2025-10-13
Last Updated: 2025-10-14

## What is Rate Limiting?

Rate limiting controls the number of requests a client can make to an API within a given timeframe to prevent abuse, DDoS attacks, and brute force attempts. It protects resources by returning a **429 Too Many Requests** response when limits are exceeded.

### Attack Scenarios Prevented

- **Brute Force Attacks**: Limits login attempts to prevent credential stuffing.
- **DDoS Attacks**: Throttles traffic surges to maintain service availability.
- **API Abuse**: Ensures fair usage by clients, preventing a single client from exhausting resources.

### Rate Limiting vs Throttling

- **Rate Limiting**: Enforces a hard cap on request counts per window; excess requests are rejected immediately.
- **Throttling**: Gradually reduces service quality or delays requests beyond a threshold instead of outright rejection.

## Rate Limiting Strategies

### Fixed Window

Clients have a fixed window (e.g., 60s). All counts reset at window boundary.

```text
| Window [0-60s] | Window [60-120s] |
| Max 100 req    | Max 100 req      |
```

### Sliding Window

Tracks requests over a rolling window using sub-windows for finer granularity.

```text
Time: 0    30   60   90 120
Reqs: *----*----*----*
Window: last 60s
```

### Token Bucket

Bucket starts with N tokens; each request consumes a token. Tokens refill at a rate R per second. Allows bursts when tokens accumulate.

### Leaky Bucket

Uniformly processes requests at fixed rate; excess requests queue up and drop if queue is full.

### Strategy Comparison

| Strategy       | Accuracy | Burst Support | Complexity |
| -------------- | -------- | ------------- | ---------- |
| Fixed Window   | Low      | No            | Low        |
| Sliding Window | High     | No            | Medium     |
| Token Bucket   | High     | Yes           | Medium     |
| Leaky Bucket   | Medium   | No            | Medium     |

## Implementation Approaches

### In-Memory Rate Limiting

Suitable for single-server apps; simple and fast but state lost on restart or scale-out.

### Redis-Based Rate Limiting

Distributed, shared state; persistence across restarts; appropriate for multi-instance deployments.

### Database-Based Rate Limiting

Uses SQL/NoSQL tables to track counts; durable but higher latency.

### CDN/WAF Rate Limiting

Offloads limits to edge (e.g., Cloudflare, AWS WAF); reduces origin load.

## Granularity Levels

- **Per-IP Rate Limiting**: Limits by client IP address.
- **Per-User Rate Limiting**: Uses authenticated user ID as key.
- **Per-Endpoint Rate Limiting**: Different limits per route.
- **Combined Rate Limiting**: Composite keys (IP + user).

## Express.js Implementation

### Basic In-Memory Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  standardHeaders: true, // RFC-compliant headers
  legacyHeaders: false,  // disable X-RateLimit- headers
  message: 'Too many requests, please try again later.'
});

app.use(limiter);
```

### Redis-Based Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import { createClient } from 'redis';

const client = createClient({ url: process.env.REDIS_URL });
await client.connect();

const redisLimiter = rateLimit({
  store: new RedisStore({ client, prefix: 'rl:' }),
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,
  legacyHeaders: false
});

app.use(redisLimiter);
```

### Database-Based Rate Limiter (Pseudo)

```typescript
// Use a table with columns: key, count, expiresAt
async function dbRateLimiter(req, res, next) {
  const key = req.ip;
  const record = await db.find(key);
  if (record && record.count >= MAX) {
    return res.status(429).send('Too Many Requests');
  }
  await db.upsert(key, record?.count + 1 || 1, newExpiresAt);
  next();
}
```

### CDN/WAF Integration

Configure Cloudflare or AWS WAF rules to set per-IP thresholds and block excessive requests at edge.

## Rate Limit Response

Use **429** status code with headers and JSON body for clarity.

```typescript
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  handler: (req, res) => {
    res
      .status(429)
      .set('Retry-After', Math.ceil((req.rateLimit.resetTime - new Date()) / 1000))
      .json({
        error: 'Too Many Requests',
        message: 'Rate limit exceeded. Please try again later.',
        limit: req.rateLimit.limit,
        remaining: req.rateLimit.remaining,
        reset: req.rateLimit.resetTime
      });
  },
  standardHeaders: true,
  legacyHeaders: false
});
```

## Special Cases

### Authentication Endpoint Protection

```typescript
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // 5 attempts per window
  skipSuccessfulRequests: true, // only count failed attempts
  handler: (req, res) => res.status(429).send('Too many login attempts')
});

app.post('/api/auth/login', authLimiter, loginHandler);
```

### Public vs Authenticated vs Admin

```typescript
// Public endpoints: standard limits
app.use('/api', limiter);

// Authenticated: per-user
app.use('/api/user', userLimiter);

// Admin: stricter
app.use('/api/admin', adminLimiter);
```

### Whitelisting Internal IPs

```typescript
const skipInternal = (req) => trustedIPs.includes(req.ip);

const limiter = rateLimit({
  windowMs: 60 * 1000,
  max: 50,
  skip: skipInternal
});
```

## Monitoring and Alerting

- **Logging Violations**: Log every 429 with IP, endpoint, timestamp.
- **Metrics**: Track counts, spikes, violation rates in Prometheus.
- **Alerts**: Set alerts for abnormal violation surge (e.g., >1000/min).

```typescript
app.use((req, res, next) => {
  res.on('finish', () => {
    if (res.statusCode === 429) {
      logger.warn('Rate limit hit', { ip: req.ip, path: req.path });
      metrics.increment('rate_limit_hits');
    }
  });
  next();
});
```

## Common Pitfalls

1. ❌ **In-Memory Store in Distributed Systems**: Limits reset per instance, allowing bypass.
2. ❌ **Unlimited Burst**: Token bucket with high refill without burst control allows spikes.
3. ❌ **Skipping Successful Requests** incorrectly counting successes.
4. ❌ **Missing Retry-After Header** reduces client guidance.

## Testing Rate Limits

### Unit Test with Supertest

```typescript
import request from 'supertest';
import app from '../app';

describe('Rate Limiter', () => {
  it('returns 429 after limit', async () => {
    for (let i = 0; i < 101; i++) {
      await request(app).get('/api');
    }
    const res = await request(app).get('/api');
    expect(res.status).toBe(429);
    expect(res.body.error).toBe('Too Many Requests');
    expect(res.headers['retry-after']).toBeDefined();
  });
});
```

### Integration Test for Auth Endpoint

```typescript
describe('Auth Rate Limiting', () => {
  it('blocks after 5 failed logins', async () => {
    for (let i = 0; i < 5; i++) {
      await request(app).post('/api/auth/login').send({ user: 'x', pass: 'y' });
    }
    const res = await request(app).post('/api/auth/login').send({ user: 'x', pass: 'y' });
    expect(res.status).toBe(429);
  });
});
```

## References

1. OWASP Denial of Service Cheat Sheet
2. express-rate-limit NPM Package
3. rate-limit-redis NPM Package
4. RFC 6585 (HTTP 429)
5. OWASP API Security Top 10 (Unrestricted Resource Consumption)

---

*Tags: shared, security, api, rate-limiting*
