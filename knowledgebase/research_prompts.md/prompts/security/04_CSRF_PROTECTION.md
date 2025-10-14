# Research Task: CSRF Protection

Created: 2025-10-13
Priority: P0
Estimated Effort: 1.5 hours
Status: Not Started

---

## Objective

Create comprehensive documentation on Cross-Site Request Forgery (CSRF) protection patterns for Express.js applications, covering both traditional and modern SPA approaches.

---

## Context

**Current State**: File exists but is empty (0 bytes)
**Target**: 250+ lines of comprehensive CSRF protection documentation
**Location**: `knowledgebase/global/04-security-auth/CSRF_PROTECTION.md`

**Why This Matters**: CSRF attacks can trick authenticated users into performing unintended actions. Modern SPAs using tokens have different protection needs than traditional form-based applications.

---

## Requirements

### 1. CSRF Fundamentals
- What is CSRF and how attacks work
- Real-world attack scenario examples
- Who is vulnerable and when
- CSRF vs XSS

### 2. CSRF Protection Strategies
- Synchronizer Token Pattern (traditional forms)
- Double-Submit Cookie Pattern
- SameSite Cookie Attribute (modern approach)
- Custom Request Headers
- Origin/Referer Header Validation

### 3. SameSite Cookie Attribute
- SameSite=Strict vs SameSite=Lax vs SameSite=None
- Browser support and compatibility
- Impact on user experience
- When to use each setting

### 4. Token-Based Protection
- CSRF token generation
- Token validation
- Token expiration and rotation
- Where to store tokens (hidden fields vs headers)

### 5. Express.js Implementation
- csurf middleware
- Custom CSRF middleware
- Integration with session management
- SameSite cookie configuration

### 6. SPA Considerations
- CSRF with JWT/Bearer tokens
- Why Bearer tokens are CSRF-resistant
- Custom headers (X-Requested-With)
- When SPAs still need CSRF protection

### 7. Common Pitfalls
- GET requests modifying state
- Missing CSRF on API endpoints
- Incorrect SameSite configuration
- Weak token generation
- Not validating on state-changing operations

### 8. Testing CSRF Protection
- Manual testing approach
- Automated testing
- Browser developer tools

---

## Output Format

```markdown
# CSRF Protection

Created: [DATE]
Last Updated: [DATE]

## What is CSRF?

[Explanation with attack scenario diagram]

## How CSRF Attacks Work

### Real-World Attack Example
[Step-by-step attack flow]

## CSRF Protection Strategies

### Synchronizer Token Pattern
[Explanation + when to use]

### Double-Submit Cookie Pattern
[Explanation + when to use]

### SameSite Cookie Attribute
[Explanation + browser support]

### Comparison Table
[Strategy comparison with pros/cons]

## SameSite Cookie Attribute

### SameSite=Strict
[Explanation + code example]

### SameSite=Lax
[Explanation + code example]

### SameSite=None
[Explanation + code example + security implications]

## Express.js Implementation

### Using csurf Middleware (Traditional Forms)
[Code example]

### Custom CSRF Middleware
[Code example from scratch]

### SameSite Cookie Configuration
[Code example]

## CSRF Protection for SPAs

### JWT/Bearer Token Approach
[Why it's CSRF-resistant + code example]

### Custom Header Validation
[Code example]

### When SPAs Still Need CSRF Protection
[Scenarios + solutions]

## Security Best Practices

[Numbered list with explanations]

## Common Pitfalls

### ❌ GET Requests Modifying State
[Why it's dangerous + example]

[... additional pitfalls]

## Testing CSRF Protection

[Manual testing steps + code examples]

## References

[Links to authoritative sources]
```

---

## Code Examples Required

1. **SameSite Cookie Configuration**
```typescript
import express from 'express'
import session from 'express-session'

const app = express()

app.use(session({
  secret: process.env.SESSION_SECRET!,
  cookie: {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax', // or 'strict' or 'none'
    maxAge: 24 * 60 * 60 * 1000 // 24 hours
  }
}))
```

2. **CSRF Token with csurf Middleware**
```typescript
import csrf from 'csurf'

const csrfProtection = csrf({ cookie: true })

// Generate token endpoint
app.get('/api/csrf-token', csrfProtection, (req, res) => {
  res.json({ csrfToken: req.csrfToken() })
})

// Protected endpoint
app.post('/api/transfer', csrfProtection, (req, res) => {
  // Process request - CSRF validated automatically
})
```

3. **Custom CSRF Middleware**
```typescript
import crypto from 'crypto'

function generateCsrfToken(): string {
  return crypto.randomBytes(32).toString('hex')
}

function csrfProtection(req: Request, res: Response, next: NextFunction) {
  if (req.method === 'GET' || req.method === 'HEAD' || req.method === 'OPTIONS') {
    return next()
  }
  
  const token = req.headers['x-csrf-token'] as string
  const sessionToken = req.session.csrfToken
  
  if (!token || !sessionToken || token !== sessionToken) {
    return res.status(403).json({ error: 'Invalid CSRF token' })
  }
  
  next()
}
```

4. **SPA with Custom Header Validation**
```typescript
// Backend validation
function validateCustomHeader(req: Request, res: Response, next: NextFunction) {
  const customHeader = req.headers['x-requested-with']
  
  if (customHeader !== 'XMLHttpRequest') {
    return res.status(403).json({ error: 'Forbidden' })
  }
  
  next()
}

// Frontend - axios example
axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
```

5. **JWT/Bearer Token (CSRF-Resistant)**
```typescript
// Why Bearer tokens in Authorization header are CSRF-resistant:
// - Not automatically sent by browser (unlike cookies)
// - JavaScript explicitly adds them to requests
// - CSRF can't read them due to Same-Origin Policy

// Frontend
const token = localStorage.getItem('token')
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
```

---

## References

1. **OWASP CSRF Cheat Sheet**
   - https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html

2. **MDN Web Docs - SameSite Cookies**
   - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite

3. **csurf npm package**
   - https://github.com/expressjs/csurf

4. **OWASP Top 10 - Broken Access Control**
   - https://owasp.org/Top10/A01_2021-Broken_Access_Control/

5. **RFC 6265 - HTTP State Management Mechanism**
   - https://datatracker.ietf.org/doc/html/rfc6265

---

## Success Criteria

- [ ] Clear CSRF attack explanation with diagram
- [ ] Real-world attack scenario documented
- [ ] All protection strategies explained with comparison
- [ ] SameSite cookie attribute fully covered (Strict/Lax/None)
- [ ] At least 5 working code examples
- [ ] Traditional forms AND SPA approaches covered
- [ ] Common pitfalls documented with mitigations
- [ ] Testing methodology included
- [ ] References to authoritative sources
- [ ] Minimum 250 lines of content
- [ ] Follows existing knowledge base format

---

## Integration

Once completed, this file will:
- Replace the empty `global/04-security-auth/CSRF_PROTECTION.md`
- Be referenced by `API_SECURITY.md`
- Link to `SESSION_MANAGEMENT.md` (cookies context)
- Link to `CORS_CONFIGURATION.md` (cross-origin context)
- Be tagged in Archon with: ["shared", "security", "csrf", "cookies"]

---

## Notes for Task Agent

- Focus on modern SPA approaches (SameSite cookies + Bearer tokens)
- Show both traditional and modern patterns
- Emphasize why Bearer tokens are CSRF-resistant
- Include browser compatibility notes for SameSite
- Test all code examples before including
- Use TypeScript for type safety
- Provide visual attack flow diagram

---

Created: 2025-10-13
Status: Ready for task agent execution
Expected Output: 250+ line markdown file with working code examples
