# Research Task: Rate Limiting Patterns

Created: 2025-10-13
Priority: P0
Estimated Effort: 1.5 hours
Status: Not Started

---

## Objective

Create comprehensive documentation on rate limiting patterns for protecting APIs from abuse, DDoS attacks, and brute force attempts in Express.js applications.

---

## Context

**Current State**: File exists but is empty (0 bytes)
**Target**: 300+ lines of comprehensive rate limiting documentation
**Location**: `knowledgebase/global/04-security-auth/RATE_LIMITING.md`

**Why This Matters**: Rate limiting is essential for preventing brute force attacks on authentication endpoints, protecting against DDoS, and ensuring fair resource usage.

---

## Requirements

### 1. Rate Limiting Fundamentals
- What is rate limiting and why it's needed
- Attack scenarios prevented by rate limiting
- Rate limiting vs throttling
- HTTP 429 Too Many Requests response

### 2. Rate Limiting Strategies
- Fixed window
- Sliding window
- Token bucket
- Leaky bucket
- Comparison and when to use each

### 3. Implementation Approaches
- In-memory rate limiting (for single server)
- Redis-based rate limiting (for distributed systems)
- Database-based rate limiting
- CDN/WAF rate limiting (Cloudflare, AWS WAF)

### 4. Granularity Levels
- Per-IP rate limiting
- Per-user rate limiting
- Per-endpoint rate limiting
- Combined rate limiting (IP + user)

### 5. Express.js Implementation
- express-rate-limit middleware
- Custom rate limiting middleware
- Redis integration for distributed systems
- Configuration options

### 6. Rate Limit Response
- 429 status code
- Retry-After header
- X-RateLimit headers (limit, remaining, reset)
- User-friendly error messages

### 7. Special Cases
- Authentication endpoint protection (stricter limits)
- Public endpoints vs authenticated endpoints
- Admin endpoints (even stricter limits)
- Whitelisting trusted IPs
- Bypassing rate limits for internal services

### 8. Monitoring and Alerting
- Logging rate limit violations
- Detecting DDoS attempts
- Metrics to track
- Alerting on suspicious patterns

---

## Output Format

```markdown
# Rate Limiting Patterns

Created: [DATE]
Last Updated: [DATE]

## What is Rate Limiting?

[Explanation with attack scenarios]

## Rate Limiting Strategies

### Fixed Window
[Explanation + diagram]

### Sliding Window
[Explanation + diagram]

### Token Bucket
[Explanation + diagram]

[Comparison table]

## Express.js Implementation

### Basic In-Memory Rate Limiting
[Code example with express-rate-limit]

### Redis-Based Rate Limiting
[Code example for distributed systems]

### Custom Rate Limiter
[Code example from scratch]

## Granularity Patterns

### Per-IP Rate Limiting
[Code example]

### Per-User Rate Limiting
[Code example with authentication]

### Per-Endpoint Rate Limiting
[Code example with different limits]

## Configuration Patterns

### Authentication Endpoints
[Strict rate limiting code example]

### Public API Endpoints
[Standard rate limiting code example]

### Admin Endpoints
[Very strict rate limiting code example]

## Rate Limit Response Format

[Code example with proper headers]

## Security Best Practices

[Numbered list with explanations]

## Monitoring Rate Limits

[Code example: Logging and metrics]

## Common Pitfalls

### ❌ Using in-memory limits in distributed systems
[Why it's problematic]

[... additional pitfalls]

## Testing Rate Limits

[Code examples: Unit tests, integration tests]

## References

[Links to authoritative sources]
```

---

## Code Examples Required

1. **Basic express-rate-limit Setup**
```typescript
import rateLimit from 'express-rate-limit'

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  standardHeaders: true,
  legacyHeaders: false,
  message: 'Too many requests, please try again later.'
})

app.use(limiter)
```

2. **Redis-Based Rate Limiting**
```typescript
import rateLimit from 'express-rate-limit'
import RedisStore from 'rate-limit-redis'
import { createClient } from 'redis'

const client = createClient({ url: process.env.REDIS_URL })
await client.connect()

const limiter = rateLimit({
  store: new RedisStore({
    client,
    prefix: 'rl:'
  }),
  windowMs: 15 * 60 * 1000,
  max: 100
})
```

3. **Per-Endpoint Rate Limiting**
```typescript
// Strict rate limiting for authentication
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // 5 attempts per 15 minutes
  skipSuccessfulRequests: true
})

app.post('/api/auth/login', authLimiter, loginHandler)

// Standard rate limiting for API
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
})

app.use('/api', apiLimiter)
```

4. **Custom Rate Limiter with User ID**
```typescript
const userRateLimiter = rateLimit({
  keyGenerator: (req) => {
    // Rate limit by user ID if authenticated, otherwise by IP
    return req.user?.id || req.ip
  },
  windowMs: 15 * 60 * 1000,
  max: 100
})
```

5. **Rate Limit with Proper Response**
```typescript
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  handler: (req, res) => {
    res.status(429).json({
      error: 'Too Many Requests',
      message: 'Rate limit exceeded. Please try again later.',
      retryAfter: req.rateLimit.resetTime
    })
  },
  standardHeaders: true, // Return rate limit info in headers
  legacyHeaders: false
})
```

---

## References

1. **OWASP Rate Limiting Cheat Sheet**
   - https://cheatsheetseries.owasp.org/cheatsheets/Denial_of_Service_Cheat_Sheet.html

2. **express-rate-limit npm package**
   - https://github.com/express-rate-limit/express-rate-limit

3. **rate-limit-redis npm package**
   - https://github.com/express-rate-limit/rate-limit-redis

4. **RFC 6585 - Additional HTTP Status Codes (429)**
   - https://datatracker.ietf.org/doc/html/rfc6585#section-4

5. **OWASP API Security Top 10 - API4:2023 Unrestricted Resource Consumption**
   - https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/

---

## Success Criteria

- [ ] Clear explanation of rate limiting strategies
- [ ] Visual diagrams for each strategy
- [ ] At least 5 working code examples
- [ ] Both in-memory and Redis implementations
- [ ] Per-IP and per-user examples
- [ ] Proper 429 response handling
- [ ] X-RateLimit headers included
- [ ] Authentication endpoint protection emphasized
- [ ] Monitoring and logging examples
- [ ] References to authoritative sources
- [ ] Minimum 300 lines of content
- [ ] Follows existing knowledge base format

---

## Integration

Once completed, this file will:
- Replace the empty `global/04-security-auth/RATE_LIMITING.md`
- Be referenced by `API_SECURITY.md`
- Link to authentication patterns (protecting login)
- Be tagged in Archon with: ["shared", "security", "api", "rate-limiting"]

---

## Notes for Task Agent

- Focus on practical brute force protection scenarios
- Show both single-server and distributed implementations
- Emphasize authentication endpoint protection
- Include Redis setup for production systems
- Test all code examples before including
- Use TypeScript for type safety
- Provide clear visual diagrams for strategies

---

Created: 2025-10-13
Status: Ready for task agent execution
Expected Output: 300+ line markdown file with working code examples
