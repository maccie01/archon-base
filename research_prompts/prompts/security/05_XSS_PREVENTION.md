# Research Task: XSS Prevention

Created: 2025-10-13
Priority: P0
Estimated Effort: 1.5 hours
Status: Not Started

---

## Objective

Create comprehensive documentation on Cross-Site Scripting (XSS) prevention patterns for web applications, covering React auto-escaping, DOMPurify, Content Security Policy, and backend sanitization.

---

## Context

**Current State**: File exists but is empty (0 bytes)
**Target**: 250+ lines of comprehensive XSS prevention documentation
**Location**: `knowledgebase/global/04-security-auth/XSS_PREVENTION.md`

**Why This Matters**: XSS is one of the most common web vulnerabilities. Modern frameworks like React provide automatic escaping, but developers must understand when additional protection is needed.

---

## Requirements

### 1. XSS Fundamentals
- What is XSS and how attacks work
- Three types: Reflected, Stored, DOM-based
- Real-world attack examples
- Impact of successful XSS attacks

### 2. XSS Attack Types

#### Reflected XSS
- Attack mechanism
- Example scenario
- Prevention

#### Stored XSS
- Attack mechanism
- Example scenario (comment systems, user profiles)
- Prevention

#### DOM-Based XSS
- Attack mechanism
- Example scenario (innerHTML, eval)
- Prevention

### 3. React Auto-Escaping
- How React escapes by default
- When React's escaping is not enough
- dangerouslySetInnerHTML (when and why to avoid)
- Safe alternatives to dangerouslySetInnerHTML

### 4. Output Encoding
- HTML encoding
- JavaScript encoding
- URL encoding
- CSS encoding
- When to use each

### 5. DOMPurify
- What DOMPurify does
- When to use DOMPurify
- Integration with React
- Configuration options
- Performance considerations

### 6. Content Security Policy (CSP)
- What is CSP
- CSP directives (script-src, style-src, etc.)
- Nonce-based CSP
- Hash-based CSP
- CSP reporting
- Express.js implementation with Helmet

### 7. Backend Input Sanitization
- When backend sanitization is needed
- HTML sanitization libraries
- Validation vs sanitization
- Database storage considerations

### 8. Common Mistakes
- Trusting user input
- Using eval() or Function()
- Improper use of innerHTML
- Rendering user content without encoding
- Weak CSP policies

---

## Output Format

```markdown
# XSS Prevention

Created: [DATE]
Last Updated: [DATE]

## What is XSS?

[Explanation with impact]

## XSS Attack Types

### Reflected XSS
[Explanation + example + prevention]

### Stored XSS
[Explanation + example + prevention]

### DOM-Based XSS
[Explanation + example + prevention]

## React's Built-in Protection

### Automatic Escaping
[How React protects by default + code example]

### dangerouslySetInnerHTML
[Why it's dangerous + when to use + code example]

### Safe Alternatives
[Code examples]

## Output Encoding

### HTML Encoding
[Explanation + code example]

### JavaScript Encoding
[Explanation + code example]

[... other encoding types]

## DOMPurify

### What is DOMPurify?
[Explanation]

### Integration with React
[Code example]

### Configuration
[Code example with options]

## Content Security Policy (CSP)

### What is CSP?
[Explanation]

### CSP Directives
[Table with directive explanations]

### Implementing CSP with Helmet
[Code example]

### Nonce-Based CSP
[Code example]

### CSP Reporting
[Code example]

## Backend Sanitization

### When to Sanitize
[Decision guide]

### HTML Sanitization
[Code example]

## Security Best Practices

[Numbered list with explanations]

## Common Mistakes

### ❌ Using innerHTML with User Content
[Why it's dangerous + example]

[... additional mistakes]

## Testing for XSS

[Testing methodology + tools]

## References

[Links to authoritative sources]
```

---

## Code Examples Required

1. **React Auto-Escaping (Safe)**
```typescript
function UserProfile({ user }: { user: User }) {
  // React automatically escapes this - SAFE
  return <div>{user.bio}</div>
  
  // Even if user.bio contains <script>alert('XSS')</script>
  // React will render it as text, not execute it
}
```

2. **dangerouslySetInnerHTML (Unsafe)**
```typescript
// ❌ DANGEROUS - Never do this with user input
function UnsafeComponent({ userContent }: { userContent: string }) {
  return <div dangerouslySetInnerHTML={{ __html: userContent }} />
}

// ✅ SAFE - Use DOMPurify first
import DOMPurify from 'dompurify'

function SafeComponent({ userContent }: { userContent: string }) {
  const clean = DOMPurify.sanitize(userContent)
  return <div dangerouslySetInnerHTML={{ __html: clean }} />
}
```

3. **DOMPurify Configuration**
```typescript
import DOMPurify from 'dompurify'

// Basic sanitization
const clean = DOMPurify.sanitize(dirty)

// Custom configuration
const clean = DOMPurify.sanitize(dirty, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
  ALLOWED_ATTR: ['href'],
  ALLOW_DATA_ATTR: false
})

// React component
function SafeHTML({ html }: { html: string }) {
  const sanitized = useMemo(
    () => DOMPurify.sanitize(html),
    [html]
  )
  
  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />
}
```

4. **Content Security Policy with Helmet**
```typescript
import helmet from 'helmet'

app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"], // Avoid 'unsafe-inline' in production
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", 'data:', 'https:'],
      connectSrc: ["'self'"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"]
    }
  })
)
```

5. **Nonce-Based CSP**
```typescript
import crypto from 'crypto'

app.use((req, res, next) => {
  res.locals.nonce = crypto.randomBytes(16).toString('base64')
  next()
})

app.use(
  helmet.contentSecurityPolicy({
    directives: {
      scriptSrc: ["'self'", (req, res) => `'nonce-${res.locals.nonce}'`]
    }
  })
)

// In HTML template
<script nonce="<%= nonce %>">
  // Your inline script
</script>
```

6. **Backend HTML Sanitization**
```typescript
import createDOMPurify from 'isomorphic-dompurify'

const DOMPurify = createDOMPurify()

// API endpoint that accepts user content
app.post('/api/comments', async (req, res) => {
  const { content } = req.body
  
  // Sanitize before storing
  const sanitized = DOMPurify.sanitize(content, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p'],
    ALLOWED_ATTR: ['href']
  })
  
  await db.insert(comments).values({
    content: sanitized,
    userId: req.user.id
  })
  
  res.json({ success: true })
})
```

---

## References

1. **OWASP XSS Cheat Sheet**
   - https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html

2. **OWASP DOM Based XSS Prevention**
   - https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html

3. **DOMPurify Documentation**
   - https://github.com/cure53/DOMPurify

4. **MDN Web Docs - Content Security Policy**
   - https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP

5. **React Documentation - dangerouslySetInnerHTML**
   - https://react.dev/reference/react-dom/components/common#dangerously-setting-the-inner-html

6. **OWASP Top 10 - Injection**
   - https://owasp.org/Top10/A03_2021-Injection/

---

## Success Criteria

- [ ] All three XSS types explained with examples
- [ ] React auto-escaping covered thoroughly
- [ ] DOMPurify integration with React examples
- [ ] CSP implementation with Helmet examples
- [ ] Nonce-based CSP implementation
- [ ] Backend sanitization patterns
- [ ] At least 6 working code examples
- [ ] Common mistakes documented with safe alternatives
- [ ] Testing methodology included
- [ ] References to authoritative sources
- [ ] Minimum 250 lines of content
- [ ] Follows existing knowledge base format

---

## Integration

Once completed, this file will:
- Replace the empty `global/04-security-auth/XSS_PREVENTION.md`
- Be referenced by `INPUT_VALIDATION.md`
- Link to `SECURITY_HEADERS.md` (CSP context)
- Be tagged in Archon with: ["shared", "security", "xss", "frontend"]

---

## Notes for Task Agent

- Focus on React ecosystem (primary frontend framework)
- Show both frontend and backend protection
- Emphasize React's automatic escaping
- Warn strongly against dangerouslySetInnerHTML without sanitization
- Include CSP as defense-in-depth
- Test all code examples before including
- Use TypeScript for type safety

---

Created: 2025-10-13
Status: Ready for task agent execution
Expected Output: 250+ line markdown file with working code examples
