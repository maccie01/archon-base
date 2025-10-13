# Security Overview - OWASP Top 10 and Core Principles

Created: 2025-10-13
Last Updated: 2025-10-13
Sources: OWASP Top 10 (2021), NIST, Security Industry Standards

## Overview

This document provides a comprehensive overview of web application security, focusing on the OWASP Top 10 vulnerabilities and fundamental security principles that should guide all development.

## OWASP Top 10 (2021)

### 1. Broken Access Control

**Risk Level**: Critical
**Description**: Restrictions on authenticated users are not properly enforced, allowing unauthorized access to data or functions.

**Common Vulnerabilities**:
- Bypassing access control checks by modifying URLs, internal state, or API requests
- Allowing primary key manipulation (e.g., changing user ID in URL)
- Missing authorization checks for API endpoints
- Privilege escalation (acting as admin without being logged in as one)
- CORS misconfiguration allowing unauthorized API access

**Prevention**:
- Deny by default - require explicit permission grants
- Implement access control checks on server-side
- Log access control failures and alert admins
- Rate limit API calls to minimize automated attacks
- Validate JWT tokens and session IDs thoroughly
- Disable directory listing on web servers
- Use attribute-based or policy-based access control

**Example Skeleton**:
```typescript
// TODO: Add role-based authorization middleware example
// TODO: Add attribute-based access control pattern
// TODO: Add resource ownership verification
```

### 2. Cryptographic Failures

**Risk Level**: Critical
**Description**: Failure to properly protect sensitive data through encryption, leading to exposure of passwords, credit cards, health records, or other sensitive information.

**Common Vulnerabilities**:
- Storing or transmitting data in clear text (HTTP, FTP, SMTP)
- Using old/weak cryptographic algorithms (MD5, SHA1, DES)
- Using default or weak encryption keys
- Not enforcing encryption (missing HSTS)
- Not validating SSL/TLS certificates properly
- Using insecure random number generators for security tokens

**Prevention**:
- Classify data and apply privacy controls
- Don't store sensitive data unnecessarily
- Encrypt all data at rest and in transit
- Use strong encryption algorithms (AES-256, RSA-2048+)
- Disable caching for sensitive data
- Use proper key management
- Enforce HTTPS with HSTS
- Use secure protocols (TLS 1.3, not SSL)

**Example Skeleton**:
```typescript
// TODO: Add data encryption at rest example
// TODO: Add TLS configuration example
// TODO: Add secure key storage pattern
```

### 3. Injection

**Risk Level**: Critical
**Description**: User-supplied data is not validated, filtered, or sanitized, allowing attackers to inject malicious code (SQL, NoSQL, OS commands, LDAP, etc.).

**Common Vulnerabilities**:
- SQL injection through unsanitized input
- NoSQL injection in MongoDB queries
- OS command injection via system calls
- LDAP injection in authentication systems
- XML injection and XXE (XML External Entities)

**Prevention**:
- Use parameterized queries (prepared statements)
- Use ORM frameworks safely
- Validate and sanitize all user input
- Use whitelist input validation
- Escape special characters
- Use LIMIT and other SQL controls to prevent mass disclosure
- Never concatenate or interpolate user input into queries

**Example Skeleton**:
```typescript
// TODO: Add parameterized query example
// TODO: Add input validation with Zod
// TODO: Add safe ORM usage pattern
```

### 4. Insecure Design

**Risk Level**: High
**Description**: Missing or ineffective security controls due to lack of business risk profiling, threat modeling, and secure design patterns.

**Common Vulnerabilities**:
- Missing rate limiting on critical functions
- Insufficient authentication requirements
- No account lockout after failed login attempts
- Missing security logging and monitoring
- No separation of tenant data in multi-tenant systems

**Prevention**:
- Establish secure development lifecycle
- Conduct threat modeling for critical flows
- Use established secure design patterns
- Implement defense in depth
- Use security requirements as user stories
- Conduct security-focused code reviews
- Perform penetration testing

**Example Skeleton**:
```typescript
// TODO: Add threat modeling template
// TODO: Add secure design checklist
// TODO: Add security requirements template
```

### 5. Security Misconfiguration

**Risk Level**: High
**Description**: Insecure default configurations, incomplete configurations, open cloud storage, misconfigured HTTP headers, verbose error messages.

**Common Vulnerabilities**:
- Default accounts with unchanged passwords
- Unnecessary features enabled (ports, services, pages)
- Stack traces shown to users
- Missing security headers
- Out-of-date software
- Improper CORS configuration
- Directory listing enabled

**Prevention**:
- Implement repeatable hardening process
- Minimal platform without unnecessary features
- Review and update configurations regularly
- Send security directives to clients (security headers)
- Automated verification of configurations
- Segmented application architecture
- Disable directory listing and default accounts

**Example Skeleton**:
```typescript
// TODO: Add security headers configuration
// TODO: Add environment configuration checklist
// TODO: Add hardening script template
```

### 6. Vulnerable and Outdated Components

**Risk Level**: High
**Description**: Using components with known vulnerabilities or unsupported versions.

**Common Vulnerabilities**:
- Unpatched operating systems, servers, frameworks
- Using deprecated npm packages
- Not scanning for vulnerabilities regularly
- Not subscribing to security bulletins
- Incompatible or outdated library versions

**Prevention**:
- Remove unused dependencies and features
- Continuously inventory versions of components
- Monitor CVE and NVD databases
- Use automated vulnerability scanning (npm audit, Snyk)
- Only obtain components from official sources
- Prefer signed packages
- Monitor for unmaintained libraries

**Example Skeleton**:
```bash
# TODO: Add dependency scanning script
# TODO: Add automated update workflow
# TODO: Add vulnerability monitoring setup
```

### 7. Identification and Authentication Failures

**Risk Level**: Critical
**Description**: Weak authentication and session management allowing attackers to compromise passwords, keys, or session tokens.

**Common Vulnerabilities**:
- Permitting credential stuffing attacks
- Allowing brute force attacks
- Using default or weak passwords
- Weak password recovery (knowledge-based answers)
- Plain text or weakly encrypted passwords
- Missing or ineffective MFA
- Exposing session IDs in URLs
- Not invalidating sessions after logout

**Prevention**:
- Implement multi-factor authentication
- Never ship with default credentials
- Implement weak password checks
- Enforce password complexity requirements
- Limit failed login attempts with rate limiting
- Use server-side session management
- Generate new session IDs after login
- Invalidate sessions after logout/timeout
- Use secure, randomly generated session IDs

**Example Skeleton**:
```typescript
// TODO: Add password complexity validation
// TODO: Add rate limiting for login attempts
// TODO: Add session management best practices
// TODO: Add MFA implementation pattern
```

### 8. Software and Data Integrity Failures

**Risk Level**: High
**Description**: Code and infrastructure that doesn't protect against integrity violations, such as using unverified plugins or insecure CI/CD pipelines.

**Common Vulnerabilities**:
- Auto-update without signature verification
- Insecure deserialization
- Using untrusted CDNs
- Lack of integrity checks on dependencies
- Insecure CI/CD pipeline allowing unauthorized access

**Prevention**:
- Use digital signatures for software updates
- Verify dependencies are from trusted repositories
- Use integrity checks (SRI for CDN resources)
- Review code and configuration changes
- Ensure CI/CD pipeline has proper access control
- Don't send unsigned or unencrypted serialized data

**Example Skeleton**:
```typescript
// TODO: Add SRI implementation for CDN resources
// TODO: Add dependency signature verification
// TODO: Add CI/CD security checklist
```

### 9. Security Logging and Monitoring Failures

**Risk Level**: Medium
**Description**: Insufficient logging and monitoring, or lack of appropriate response, allowing attackers to persist undetected.

**Common Vulnerabilities**:
- Not logging authentication failures
- Logs stored only locally
- No alerting for suspicious activities
- Log messages not actionable
- Penetration testing not triggering alerts
- No incident response plan

**Prevention**:
- Log all authentication, access control, and input validation failures
- Ensure logs can be consumed by log management solutions
- Encode log data to prevent injection attacks
- Establish effective monitoring and alerting
- Create incident response and recovery plans
- Use centralized logging
- Implement intrusion detection systems

**Example Skeleton**:
```typescript
// TODO: Add structured logging pattern
// TODO: Add security event logging
// TODO: Add alert configuration example
```

### 10. Server-Side Request Forgery (SSRF)

**Risk Level**: Medium-High
**Description**: Web application fetches a remote resource without validating the user-supplied URL, allowing attackers to coerce the application to send requests to unexpected destinations.

**Common Vulnerabilities**:
- Fetching URLs provided by users without validation
- Allowing access to internal resources
- Not sanitizing URL parameters
- Bypassing firewalls via SSRF

**Prevention**:
- Sanitize and validate all client-supplied input data
- Enforce URL schema, port, and destination with whitelist
- Disable HTTP redirections
- Use network segmentation
- Don't send raw responses to clients
- Implement deny-by-default firewall policies

**Example Skeleton**:
```typescript
// TODO: Add URL validation pattern
// TODO: Add whitelist-based URL filtering
// TODO: Add network segmentation diagram
```

## Core Security Principles

### 1. Defense in Depth

**Principle**: Implement multiple layers of security controls.

**Application**:
- Network security (firewalls, VPNs)
- Application security (input validation, authentication)
- Data security (encryption, access control)
- Physical security (server access)

### 2. Least Privilege

**Principle**: Grant minimum necessary permissions.

**Application**:
- User roles with minimal permissions
- Database users with limited access
- API keys with scope restrictions
- Service accounts with specific roles only

### 3. Fail Securely

**Principle**: Failures should result in denial of access, not unauthorized access.

**Application**:
- Default to denying access
- Don't expose error details to users
- Log failures for investigation
- Graceful degradation without security compromise

### 4. Zero Trust

**Principle**: Never trust, always verify.

**Application**:
- Verify every request regardless of source
- Authenticate and authorize all API calls
- Validate all input data
- Don't trust client-side validation alone

### 5. Security by Design

**Principle**: Build security in from the start.

**Application**:
- Include security requirements in planning
- Conduct threat modeling during design
- Security code reviews
- Regular security testing

### 6. Keep Security Simple

**Principle**: Complexity is the enemy of security.

**Application**:
- Use established security libraries
- Avoid custom cryptography
- Clear and simple security logic
- Well-documented security controls

### 7. Complete Mediation

**Principle**: Check every access to every resource.

**Application**:
- Don't cache authorization decisions
- Re-verify permissions on each request
- Check authorization at multiple layers
- No security through obscurity

## Security Development Lifecycle

### Phase 1: Requirements
- Define security requirements
- Identify compliance needs
- Determine data classification
- Plan authentication/authorization

### Phase 2: Design
- Threat modeling
- Security architecture review
- Select security controls
- Design defense in depth

### Phase 3: Implementation
- Secure coding practices
- Input validation
- Output encoding
- Error handling

### Phase 4: Testing
- Security unit tests
- Penetration testing
- Vulnerability scanning
- Security code review

### Phase 5: Deployment
- Secure configuration
- Security hardening
- Monitoring setup
- Incident response plan

### Phase 6: Maintenance
- Security patching
- Vulnerability management
- Security monitoring
- Regular security audits

## Threat Modeling Process

### Step 1: Identify Assets
- User data
- Authentication credentials
- Business logic
- Infrastructure components

### Step 2: Create Architecture Overview
- Data flow diagrams
- Trust boundaries
- Entry/exit points
- External dependencies

### Step 3: Identify Threats (STRIDE)
- **S**poofing identity
- **T**ampering with data
- **R**epudiation
- **I**nformation disclosure
- **D**enial of service
- **E**levation of privilege

### Step 4: Rank Threats
- Probability of occurrence
- Impact if exploited
- Priority for remediation

### Step 5: Mitigate Threats
- Define security controls
- Implement protections
- Test effectiveness
- Document residual risks

## Security Testing Checklist

### Authentication Testing
- [ ] Test for weak passwords
- [ ] Test for account enumeration
- [ ] Test for brute force protection
- [ ] Test for session fixation
- [ ] Test for password reset vulnerabilities
- [ ] Test MFA implementation

### Authorization Testing
- [ ] Test for privilege escalation
- [ ] Test for insecure direct object references
- [ ] Test for missing function-level access control
- [ ] Test for path traversal

### Input Validation Testing
- [ ] Test for SQL injection
- [ ] Test for XSS
- [ ] Test for command injection
- [ ] Test for XML injection
- [ ] Test for LDAP injection

### Session Management Testing
- [ ] Test for session fixation
- [ ] Test for session timeout
- [ ] Test for session hijacking
- [ ] Test for concurrent sessions
- [ ] Test for logout effectiveness

### Configuration Testing
- [ ] Test for default credentials
- [ ] Test for directory listing
- [ ] Test for unnecessary HTTP methods
- [ ] Test for security headers
- [ ] Test for verbose error messages

## Common Security Anti-Patterns

### 1. Security Through Obscurity
Relying on secrecy of implementation rather than proper security controls.

### 2. Client-Side Security
Trusting client-side validation or authorization without server-side verification.

### 3. Hard-Coded Credentials
Embedding passwords, API keys, or secrets in source code.

### 4. Insufficient Logging
Not logging security events or logging sensitive data.

### 5. Custom Cryptography
Implementing custom encryption algorithms instead of using proven standards.

### 6. Ignoring Updates
Not applying security patches and updates promptly.

### 7. Overly Permissive CORS
Allowing access from any origin without proper restrictions.

### 8. Weak Password Policies
Not enforcing password complexity and allowing common passwords.

## Security Resources

### Organizations
- OWASP (Open Web Application Security Project)
- NIST (National Institute of Standards and Technology)
- SANS Institute
- CIS (Center for Internet Security)

### Tools
- OWASP ZAP (vulnerability scanner)
- Burp Suite (security testing)
- npm audit (dependency scanning)
- Snyk (vulnerability management)
- SonarQube (code quality and security)

### Standards
- OWASP Top 10
- CWE Top 25
- NIST Cybersecurity Framework
- PCI DSS
- ISO 27001

## Next Steps

1. Review authentication patterns: [AUTHENTICATION_PATTERNS.md](./AUTHENTICATION_PATTERNS.md)
2. Implement password security: [PASSWORD_SECURITY.md](./PASSWORD_SECURITY.md)
3. Configure security headers: [SECURITY_HEADERS.md](./SECURITY_HEADERS.md)
4. Set up security testing: [SECURITY_TESTING.md](./SECURITY_TESTING.md)

## References

- OWASP Top 10 2021: https://owasp.org/Top10/
- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework
- CWE Top 25: https://cwe.mitre.org/top25/
- OWASP Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
