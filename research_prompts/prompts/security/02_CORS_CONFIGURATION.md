# Research Task: CORS Configuration

Created: 2025-10-13
Priority: P0
Estimated Effort: 1.5 hours
Status: Not Started

---

## Objective

Create comprehensive documentation on Cross-Origin Resource Sharing (CORS) configuration patterns for Express.js APIs, with focus on security and practical implementation.

---

## Context

**Current State**: File exists but is empty (0 bytes)
**Target**: 300+ lines of comprehensive CORS documentation
**Location**: `knowledgebase/global/04-security-auth/CORS_CONFIGURATION.md`

**Why This Matters**: CORS is one of the most commonly misconfigured security features. Incorrect CORS settings can expose APIs to unauthorized origins or break legitimate requests.

---

## Requirements

### 1. CORS Fundamentals
- What is CORS and why it exists
- Same-Origin Policy explained
- When CORS is needed (SPAs calling APIs)
- CORS vs JSONP

### 2. CORS Headers Explained
- Access-Control-Allow-Origin
- Access-Control-Allow-Methods
- Access-Control-Allow-Headers
- Access-Control-Allow-Credentials
- Access-Control-Max-Age
- Access-Control-Expose-Headers

### 3. Preflight Requests
- What triggers a preflight (OPTIONS request)
- Simple vs complex requests
- Handling OPTIONS method
- Caching preflight responses

### 4. Origin Whitelisting
- Dynamic origin validation
- Environment-based configuration
- Wildcard (*) dangers
- Subdomain handling

### 5. Credentials and Cookies
- When to use credentials: true
- Cookie security with CORS
- Cannot use wildcard with credentials

### 6. Express.js Implementation
- Using cors middleware
- Custom CORS middleware
- Route-specific CORS
- Global CORS configuration

### 7. Common Misconfigurations
- Allowing all origins in production
- Missing credentials configuration
- Incorrect preflight caching
- Not handling all HTTP methods
- Security implications of each

### 8. Development vs Production
- Relaxed CORS for development
- Strict CORS for production
- Environment variable configuration

---

## Output Format

```markdown
# CORS Configuration

Created: [DATE]
Last Updated: [DATE]

## What is CORS?

[Explanation of Same-Origin Policy and why CORS exists]

## When Do You Need CORS?

[Decision guide with examples]

## CORS Headers Reference

[Table with each header, purpose, example values]

## Preflight Requests

### What Triggers a Preflight?
[Explanation]

### Handling OPTIONS Requests
[Code example]

## Express.js Implementation

### Basic CORS Setup
[Code example using cors middleware]

### Dynamic Origin Validation
[Code example with whitelist]

### Credentials Configuration
[Code example with cookies]

### Custom CORS Middleware
[Code example from scratch]

## Configuration Patterns

### Development Configuration
[Code example with relaxed settings]

### Production Configuration
[Code example with strict settings]

### Environment-Based Config
[Code example using .env]

## Common Misconfigurations

### ❌ Allowing All Origins in Production
[Why it's dangerous + impact]

[... additional misconfigurations]

## Security Best Practices

[Numbered list with explanations]

## Testing CORS Configuration

[Code examples: Testing preflight, testing credentials]

## Troubleshooting

[Common CORS errors and solutions]

## References

[Links to authoritative sources]
```

---

## Code Examples Required

1. **Basic CORS Setup**
```typescript
import express from 'express'
import cors from 'cors'

const app = express()

// Basic CORS configuration
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(','),
  credentials: true
}))
```

2. **Dynamic Origin Validation**
```typescript
import cors from 'cors'

const allowedOrigins = [
  'https://app.example.com',
  'https://admin.example.com'
]

const corsOptions = {
  origin: (origin, callback) => {
    // Implementation with validation logic
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}

app.use(cors(corsOptions))
```

3. **Custom CORS Middleware**
```typescript
function customCors(req: Request, res: Response, next: NextFunction) {
  // Implementation from scratch
}
```

4. **Environment-Based Configuration**
```typescript
// config/cors.ts
import { CorsOptions } from 'cors'

export const getCorsOptions = (): CorsOptions => {
  // Environment-specific logic
}
```

5. **Route-Specific CORS**
```typescript
// Different CORS for different routes
app.get('/public', cors(), handler)
app.post('/admin', cors(strictCorsOptions), handler)
```

---

## References

1. **MDN Web Docs - CORS**
   - https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

2. **OWASP CORS Cheat Sheet**
   - https://cheatsheetseries.owasp.org/cheatsheets/Cross-Origin_Resource_Sharing_Cheat_Sheet.html

3. **Express.js CORS Middleware**
   - https://expressjs.com/en/resources/middleware/cors.html

4. **W3C CORS Specification**
   - https://www.w3.org/TR/cors/

5. **OWASP Top 10 - Security Misconfiguration**
   - https://owasp.org/Top10/A05_2021-Security_Misconfiguration/

---

## Success Criteria

- [ ] Clear explanation of CORS fundamentals
- [ ] All CORS headers documented with examples
- [ ] At least 5 working code examples
- [ ] Development vs production configurations shown
- [ ] Common misconfigurations highlighted with security impact
- [ ] Preflight request handling explained
- [ ] Credentials and cookies properly covered
- [ ] Troubleshooting section for common errors
- [ ] References to authoritative sources
- [ ] Minimum 300 lines of content
- [ ] Follows existing knowledge base format

---

## Integration

Once completed, this file will:
- Replace the empty `global/04-security-auth/CORS_CONFIGURATION.md`
- Be referenced by `API_SECURITY.md`
- Link to `CSRF_PROTECTION.md` (credentials context)
- Be tagged in Archon with: ["shared", "security", "api", "cors"]

---

## Notes for Task Agent

- Include real-world scenarios (SPA calling API)
- Show both simple and complex request examples
- Emphasize security implications of misconfigurations
- Provide working Express.js middleware examples
- Test all code examples before including
- Use TypeScript for type safety
- Include troubleshooting for "CORS error" messages

---

Created: 2025-10-13
Status: Ready for task agent execution
Expected Output: 300+ line markdown file with working code examples
