# Research Task: JWT Patterns

Created: 2025-10-13
Priority: P0
Estimated Effort: 2 hours
Status: Not Started

---

## Objective

Create comprehensive documentation on JWT (JSON Web Token) patterns for authentication and authorization in Node.js/Express.js applications, with a focus on security best practices.

---

## Context

**Current State**: File exists but is empty (0 bytes)
**Target**: 400+ lines of comprehensive JWT documentation
**Location**: `knowledgebase/global/04-security-auth/JWT_PATTERNS.md`

**Related Documentation**:
- `PASSWORD_SECURITY.md` (already complete)
- `SESSION_MANAGEMENT.md` (already complete)
- `OAUTH2_OPENID.md` (to be completed)

---

## Requirements

### 1. JWT Fundamentals
- What is JWT and when to use it
- JWT structure (header, payload, signature)
- JWT vs session-based authentication
- Token types: access tokens vs refresh tokens

### 2. Token Generation
- Creating JWTs with jsonwebtoken library
- Choosing signing algorithms (HS256 vs RS256)
- Setting appropriate expiration times
- Including claims (sub, iat, exp, custom claims)
- Code example: JWT generation function

### 3. Token Validation
- Verifying JWT signatures
- Checking expiration
- Validating claims
- Handling token errors
- Code example: JWT verification middleware for Express.js

### 4. Refresh Token Patterns
- Why refresh tokens are needed
- Refresh token rotation
- Storing refresh tokens securely
- Revocation strategies
- Code example: Refresh token endpoint

### 5. Token Storage
- httpOnly cookies vs localStorage
- Security implications of each approach
- CSRF considerations with cookies
- XSS considerations with localStorage
- Recommended approach for SPAs

### 6. JWKS and Key Rotation
- JSON Web Key Sets (JWKS)
- Public/private key pairs
- Key rotation strategies
- Code example: JWKS endpoint

### 7. Security Best Practices
- Short-lived access tokens (15 min recommended)
- Secure token storage
- HTTPS only transmission
- Audience and issuer validation
- Rate limiting token endpoints
- Monitoring for suspicious activity

### 8. Common Vulnerabilities
- None algorithm attack
- Weak signing keys
- Missing expiration validation
- Token leakage in logs/URLs
- JWT confusion attacks
- Mitigation strategies for each

---

## Output Format

Structure the documentation as follows:

```markdown
# JWT Patterns

Created: [DATE]
Last Updated: [DATE]

## When to Use JWT

[Decision guide: JWT vs sessions]

## JWT Structure

[Explanation with visual example]

## Generating JWTs

### Basic Token Generation
[Code example with comments]

### Custom Claims
[Code example]

### Signing Algorithms
[Comparison table + recommendations]

## Validating JWTs

### Express.js Middleware
[Complete middleware implementation]

### Error Handling
[Code example of handling various JWT errors]

## Refresh Token Pattern

### Why Refresh Tokens?
[Explanation]

### Implementation
[Code example: Complete refresh flow]

### Revocation
[Strategy + code example]

## Token Storage

### Comparison Table
[Cookies vs localStorage security analysis]

### Recommended Approach
[Decision tree + implementation]

## Security Best Practices

[Numbered list with explanations]

## Common Vulnerabilities & Mitigations

### None Algorithm Attack
[Explanation + prevention]

[... additional vulnerabilities]

## Anti-Patterns

### ❌ DON'T: Store sensitive data in JWT payload
[Explanation + why it's bad]

[... additional anti-patterns]

## Testing JWT Implementation

[Code example: Unit tests for JWT functions]

## References

[Links to authoritative sources]
```

---

## Code Examples Required

All examples must be production-ready TypeScript with:

1. **JWT Generation Function**
```typescript
import jwt from 'jsonwebtoken'

interface JWTPayload {
  userId: string
  email: string
  role: string
}

export function generateAccessToken(payload: JWTPayload): string {
  // Implementation with comments
}

export function generateRefreshToken(userId: string): string {
  // Implementation with comments
}
```

2. **JWT Verification Middleware**
```typescript
import { Request, Response, NextFunction } from 'express'

export function requireAuth(req: Request, res: Response, next: NextFunction) {
  // Complete implementation with error handling
}
```

3. **Refresh Token Endpoint**
```typescript
router.post('/auth/refresh', async (req, res) => {
  // Complete implementation with rotation
})
```

4. **Token Storage in Frontend**
```typescript
// Both approaches with security notes
```

---

## References

Research and cite these authoritative sources:

1. **RFC 7519** - JSON Web Token (JWT) standard
   - https://datatracker.ietf.org/doc/html/rfc7519

2. **OWASP JWT Cheat Sheet**
   - https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html

3. **Auth0 JWT Documentation**
   - https://auth0.com/docs/secure/tokens/json-web-tokens

4. **jsonwebtoken npm package**
   - https://github.com/auth0/node-jsonwebtoken

5. **JWT.io**
   - https://jwt.io/introduction

6. **OWASP Top 10 - Broken Authentication**
   - https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/

---

## Success Criteria

- [ ] Comprehensive JWT explanation (not just code)
- [ ] At least 5 working, tested code examples
- [ ] Security considerations highlighted throughout
- [ ] Common vulnerabilities documented with mitigations
- [ ] Anti-patterns clearly marked
- [ ] References to authoritative sources
- [ ] Integration examples with Express.js
- [ ] Refresh token pattern fully implemented
- [ ] Token storage comparison with recommendations
- [ ] Testing examples included
- [ ] Minimum 400 lines of content
- [ ] Follows existing knowledge base format

---

## Integration

Once completed, this file will:
- Replace the empty `global/04-security-auth/JWT_PATTERNS.md`
- Be referenced by `AUTHENTICATION_PATTERNS.md`
- Complement `SESSION_MANAGEMENT.md` (already complete)
- Link to `OAUTH2_OPENID.md` (future)
- Be tagged in Archon with: ["shared", "security", "authentication", "jwt"]

---

## Notes for Task Agent

- Focus on Node.js/Express.js ecosystem (matches project tech stack)
- Use TypeScript for all examples
- Test all code examples before including
- Emphasize security throughout (this is security documentation)
- Use real-world scenarios and explanations
- Avoid overly academic language; keep it practical
- Include visual aids where helpful (JWT structure diagram, flow diagrams)

---

Created: 2025-10-13
Status: Ready for task agent execution
Expected Output: 400+ line markdown file with working code examples
