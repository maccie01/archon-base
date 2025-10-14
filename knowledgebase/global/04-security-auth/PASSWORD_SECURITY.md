# Password Security - Hashing, Salting, and Best Practices

Created: 2025-10-13
Last Updated: 2025-10-13
Sources: OWASP Password Storage Cheat Sheet, NIST SP 800-63B, Cryptography Standards

## Overview

Proper password security is fundamental to application security. This document covers modern password hashing algorithms, implementation patterns, and password policy best practices.

## Password Hashing Algorithms Comparison

| Algorithm | Status | Work Factor | Salt | Memory Hard | Recommendation |
|-----------|--------|-------------|------|-------------|----------------|
| **Argon2id** | Modern | Configurable | Built-in | Yes | **Recommended (2024)** |
| **bcrypt** | Mature | Configurable | Built-in | No | **Acceptable** |
| **scrypt** | Modern | Configurable | Built-in | Yes | Acceptable |
| **PBKDF2** | Legacy | Configurable | Manual | No | Legacy only |
| **SHA-256** | Weak | None | Manual | No | **Never use** |
| **MD5** | Broken | None | Manual | No | **Never use** |

## Pattern 1: Argon2id (Recommended)

### Overview
Argon2id is the winner of the 2015 Password Hashing Competition and the current gold standard for password hashing. It's memory-hard and resistant to both GPU and side-channel attacks.

### When to Use
- **All new projects** (2024 recommendation)
- High-security applications
- When defending against sophisticated attacks
- Applications with modern infrastructure

### Why Argon2id?
- **Memory-hard**: Expensive on GPUs and ASICs
- **Time-cost parameter**: Adjustable computational difficulty
- **Parallelism parameter**: Configurable parallel threads
- **Hybrid mode (id)**: Resistant to both side-channel and GPU attacks
- **OWASP recommended**: Official OWASP top choice

### Implementation Pattern

```typescript
// TODO: Add Argon2 implementation with argon2 npm package

import argon2 from 'argon2';

interface Argon2Options {
  type: argon2.argon2id;      // Use Argon2id variant
  memoryCost: number;          // Memory in KiB (64MB = 65536)
  timeCost: number;            // Number of iterations (3-4)
  parallelism: number;         // Number of threads (1-2)
  hashLength: number;          // Output length in bytes (32)
}

// Recommended settings for 2024
const ARGON2_OPTIONS: Argon2Options = {
  type: argon2.argon2id,
  memoryCost: 65536,           // 64 MB
  timeCost: 3,                 // 3 iterations
  parallelism: 1,              // 1 thread
  hashLength: 32               // 32 bytes = 256 bits
};

/**
 * Hash password using Argon2id
 * Output format: $argon2id$v=19$m=65536,t=3,p=1$<salt>$<hash>
 */
async function hashPassword(password: string): Promise<string> {
  try {
    const hash = await argon2.hash(password, ARGON2_OPTIONS);
    return hash;
  } catch (error) {
    throw new Error('Password hashing failed');
  }
}

/**
 * Verify password against Argon2id hash
 * Argon2 library automatically extracts parameters from hash string
 */
async function verifyPassword(password: string, hash: string): Promise<boolean> {
  try {
    const isValid = await argon2.verify(hash, password);

    // Optional: Check if hash needs rehashing with updated parameters
    if (isValid && argon2.needsRehash(hash, ARGON2_OPTIONS)) {
      // TODO: Rehash password with new parameters on next login
      console.log('Password hash needs updating with stronger parameters');
    }

    return isValid;
  } catch (error) {
    return false;
  }
}

// TODO: Add example of rehashing passwords with updated parameters
```

### Parameter Tuning

**Time vs Security Trade-off**:
- **Low security**: memoryCost=32MB, timeCost=2 (~50ms)
- **Medium security**: memoryCost=64MB, timeCost=3 (~100ms)
- **High security**: memoryCost=128MB, timeCost=4 (~200ms)

**Rule of Thumb**: Target 100-500ms on your server hardware.

### Security Considerations

**Strengths**:
- Industry-leading resistance to GPU/ASIC attacks
- Memory-hard algorithm increases attack cost
- Configurable parameters allow future-proofing
- Built-in salt generation
- No password length limitation

**Weaknesses**:
- Higher memory usage than bcrypt
- Requires more server resources
- Less mature ecosystem than bcrypt
- Not available in all environments

**Best Practices**:
1. Use Argon2id variant (not Argon2i or Argon2d)
2. Tune parameters based on server capacity
3. Monitor hashing time (aim for 100-500ms)
4. Store hash parameters with the hash
5. Implement hash parameter upgrading
6. Log hashing failures for monitoring
7. Use constant-time comparison (built-in)
8. Never log or transmit passwords

## Pattern 2: bcrypt (Industry Standard)

### Overview
bcrypt is the most widely adopted password hashing algorithm, based on the Blowfish cipher. While not as strong as Argon2id, it remains secure and battle-tested.

### When to Use
- Existing projects using bcrypt
- Legacy system compatibility required
- Limited server memory
- When Argon2 is not available

### Implementation Pattern

```typescript
// TODO: Add bcrypt implementation

import bcrypt from 'bcrypt';

// Work factor (cost factor): 2^12 = 4096 iterations
// Higher = more secure but slower
// Recommendation for 2024: 12-14
const BCRYPT_ROUNDS = 12;

/**
 * Hash password using bcrypt
 * Output format: $2b$12$<salt><hash>
 */
async function hashPasswordBcrypt(password: string): Promise<string> {
  try {
    const hash = await bcrypt.hash(password, BCRYPT_ROUNDS);
    return hash;
  } catch (error) {
    throw new Error('Password hashing failed');
  }
}

/**
 * Verify password against bcrypt hash
 */
async function verifyPasswordBcrypt(password: string, hash: string): Promise<boolean> {
  try {
    return await bcrypt.compare(password, hash);
  } catch (error) {
    return false;
  }
}

/**
 * Check if hash needs rehashing with higher work factor
 */
function needsRehash(hash: string, currentRounds: number = BCRYPT_ROUNDS): boolean {
  // Extract rounds from hash: $2b$12$...
  const rounds = parseInt(hash.split('$')[2], 10);
  return rounds < currentRounds;
}

// TODO: Add migration from bcrypt to Argon2id example
```

### Work Factor Guidelines

| Year | Minimum Rounds | Recommended | Time (approx) |
|------|----------------|-------------|---------------|
| 2024 | 10 | 12-14 | 100-500ms |
| 2020 | 10 | 12 | 100-250ms |
| 2015 | 8 | 10 | 50-100ms |

**Rule**: Increase work factor by 1 every 1-2 years to maintain security.

### Security Considerations

**Strengths**:
- Proven track record (20+ years)
- Wide library support
- Automatic salt generation
- Built-in work factor
- Resistant to rainbow tables

**Weaknesses**:
- Not memory-hard (vulnerable to GPUs)
- 72-character password limit
- Less resistant to modern attacks than Argon2
- Fixed salt length

**Best Practices**:
1. Use minimum work factor of 12 (2024)
2. Truncate passwords longer than 72 characters carefully
3. Use bcryptjs for pure JavaScript environments
4. Monitor hashing time and adjust rounds
5. Plan migration to Argon2id
6. Never use synchronous hashing in production
7. Implement rate limiting on login attempts
8. Log unusual password verification patterns

## Pattern 3: scrypt

### Overview
Memory-hard key derivation function designed to be costly on hardware.

### When to Use
- When Argon2 is not available
- Legacy systems that already use scrypt
- As fallback option

### Implementation Pattern

```typescript
// TODO: Add scrypt implementation with Node.js crypto module

import { scrypt, randomBytes, timingSafeEqual } from 'crypto';
import { promisify } from 'util';

const scryptAsync = promisify(scrypt);

const SCRYPT_PARAMS = {
  N: 32768,        // CPU/memory cost (2^15)
  r: 8,            // Block size
  p: 1,            // Parallelization
  keyLength: 64,   // Output length
  saltLength: 16   // Salt length
};

/**
 * Hash password using scrypt
 */
async function hashPasswordScrypt(password: string): Promise<string> {
  const salt = randomBytes(SCRYPT_PARAMS.saltLength).toString('hex');
  const derivedKey = await scryptAsync(
    password,
    salt,
    SCRYPT_PARAMS.keyLength,
    { N: SCRYPT_PARAMS.N, r: SCRYPT_PARAMS.r, p: SCRYPT_PARAMS.p }
  ) as Buffer;

  return `${salt}:${derivedKey.toString('hex')}`;
}

/**
 * Verify password against scrypt hash
 */
async function verifyPasswordScrypt(password: string, hash: string): Promise<boolean> {
  const [salt, key] = hash.split(':');
  const keyBuffer = Buffer.from(key, 'hex');

  const derivedKey = await scryptAsync(
    password,
    salt,
    SCRYPT_PARAMS.keyLength,
    { N: SCRYPT_PARAMS.N, r: SCRYPT_PARAMS.r, p: SCRYPT_PARAMS.p }
  ) as Buffer;

  return timingSafeEqual(keyBuffer, derivedKey);
}

// TODO: Add parameter tuning guidance
```

### Security Considerations

**Strengths**:
- Memory-hard algorithm
- Native Node.js support
- Tunable parameters
- No password length limit

**Weaknesses**:
- Less battle-tested than bcrypt
- More complex parameter tuning
- Not as widely adopted as Argon2
- Less research than Argon2

## Password Policy Best Practices

### Length Requirements

**NIST SP 800-63B Recommendations (2024)**:
- **Minimum**: 8 characters (absolute minimum)
- **Recommended**: 12 characters
- **Ideal**: 15+ characters
- **Maximum**: No maximum (accept up to 64+ characters)

```typescript
// TODO: Add password length validation

const PASSWORD_POLICY = {
  minLength: 12,
  maxLength: 128,    // Practical limit
  requireUppercase: false,  // NIST: Don't force composition
  requireLowercase: false,
  requireNumbers: false,
  requireSpecial: false,
  allowUnicode: true,       // Support passphrases in any language
};

function validatePasswordLength(password: string): boolean {
  return password.length >= PASSWORD_POLICY.minLength &&
         password.length <= PASSWORD_POLICY.maxLength;
}
```

### Composition Rules (What NOT to do)

**Avoid Complex Composition Rules**:
- L Require uppercase + lowercase + numbers + special chars
- L Prohibit common words
- L Require special characters in specific positions
- L Prohibit repeating characters

**Why?** These rules often lead to predictable patterns (Password1!, Summer2024!)

**Instead**:
-  Enforce minimum length (12+ characters)
-  Check against compromised password lists
-  Allow passphrases ("correct horse battery staple")
-  Support password managers

### Password Strength Validation

```typescript
// TODO: Add password strength validation with zxcvbn

import zxcvbn from 'zxcvbn';

interface PasswordStrength {
  score: number;           // 0-4
  feedback: string[];
  crackTimeSeconds: number;
  isStrong: boolean;
}

function checkPasswordStrength(password: string, userInputs?: string[]): PasswordStrength {
  // zxcvbn performs realistic password strength estimation
  const result = zxcvbn(password, userInputs);

  return {
    score: result.score,
    feedback: result.feedback.suggestions,
    crackTimeSeconds: result.crack_times_seconds.offline_slow_hashing_1e4_per_second,
    isStrong: result.score >= 3  // 3 or 4 is acceptable
  };
}

// TODO: Add integration with Have I Been Pwned API
```

### Compromised Password Checking

```typescript
// TODO: Add Have I Been Pwned integration

import crypto from 'crypto';

/**
 * Check if password appears in breach databases using k-anonymity
 * Uses Have I Been Pwned API with k-anonymity (no password sent)
 */
async function isPasswordCompromised(password: string): Promise<boolean> {
  // SHA-1 hash the password
  const hash = crypto.createHash('sha1').update(password).digest('hex').toUpperCase();
  const prefix = hash.substring(0, 5);
  const suffix = hash.substring(5);

  // Query HIBP API with first 5 chars only (k-anonymity)
  const response = await fetch(`https://api.pwnedpasswords.com/range/${prefix}`);
  const data = await response.text();

  // Check if hash suffix appears in results
  return data.includes(suffix);
}

// Usage in registration/password change
async function validateNewPassword(password: string): Promise<{valid: boolean, reason?: string}> {
  // Length check
  if (password.length < 12) {
    return { valid: false, reason: 'Password must be at least 12 characters' };
  }

  // Strength check
  const strength = checkPasswordStrength(password);
  if (!strength.isStrong) {
    return { valid: false, reason: strength.feedback.join('. ') };
  }

  // Breach check
  const isCompromised = await isPasswordCompromised(password);
  if (isCompromised) {
    return { valid: false, reason: 'Password found in data breach. Please choose another.' };
  }

  return { valid: true };
}
```

## Password Reset Security

### Secure Reset Token Generation

```typescript
// TODO: Add password reset token generation

import crypto from 'crypto';

interface ResetToken {
  token: string;
  hashedToken: string;
  expiresAt: Date;
}

/**
 * Generate secure password reset token
 */
function generateResetToken(): ResetToken {
  // Generate cryptographically random token
  const token = crypto.randomBytes(32).toString('hex');

  // Hash token before storing (protect against database leaks)
  const hashedToken = crypto.createHash('sha256').update(token).digest('hex');

  // 15 minute expiration
  const expiresAt = new Date(Date.now() + 15 * 60 * 1000);

  return { token, hashedToken, expiresAt };
}

/**
 * Validate reset token
 */
async function validateResetToken(token: string): Promise<{valid: boolean, userId?: string}> {
  const hashedToken = crypto.createHash('sha256').update(token).digest('hex');

  // TODO: Query database for hashed token
  // Check expiration
  // Return user ID if valid

  return { valid: false };
}

// TODO: Add rate limiting for reset requests
// TODO: Add email verification step
```

### Reset Process Best Practices

1. **Generate random tokens**: Use crypto.randomBytes (not Math.random)
2. **Hash tokens in database**: Protect against database breaches
3. **Short expiration**: 15-30 minutes maximum
4. **One-time use**: Invalidate after successful reset
5. **Rate limiting**: Prevent abuse (e.g., 3 requests per hour)
6. **Email verification**: Send to registered email only
7. **No user enumeration**: Same response for valid/invalid emails
8. **Require current password**: For logged-in password changes
9. **Invalidate all sessions**: After password change
10. **Notify user**: Email notification of password change

## Password Storage Migration

### Migrating from Weak Hashing

```typescript
// TODO: Add migration strategy from SHA-256 to Argon2

interface PasswordMigrationStrategy {
  // Phase 1: Wrap existing hashes
  wrapLegacyHash(legacyHash: string): Promise<string>;

  // Phase 2: Rehash on login
  rehashOnLogin(password: string, userId: string): Promise<void>;

  // Phase 3: Force reset for remaining users
  forcePasswordReset(userId: string): Promise<void>;
}

/**
 * Example: Migrating from MD5 to Argon2
 */
async function migratePassword(password: string, oldMD5Hash: string): Promise<string> {
  // Verify against old hash
  const md5Hash = crypto.createHash('md5').update(password).digest('hex');
  if (md5Hash !== oldMD5Hash) {
    throw new Error('Invalid password');
  }

  // Generate new Argon2 hash
  const newHash = await hashPassword(password);

  // TODO: Update database with new hash
  // TODO: Mark migration complete

  return newHash;
}
```

### Upgrading Hash Parameters

```typescript
// TODO: Add hash parameter upgrade strategy

/**
 * Check if hash needs upgrading and rehash if necessary
 */
async function upgradeHashIfNeeded(password: string, currentHash: string, userId: string): Promise<void> {
  // For Argon2
  if (argon2.needsRehash(currentHash, ARGON2_OPTIONS)) {
    const newHash = await hashPassword(password);
    // TODO: Update database
    console.log(`Upgraded password hash for user ${userId}`);
  }

  // For bcrypt
  if (needsRehash(currentHash, BCRYPT_ROUNDS)) {
    const newHash = await hashPasswordBcrypt(password);
    // TODO: Update database
    console.log(`Upgraded bcrypt rounds for user ${userId}`);
  }
}
```

## Common Mistakes and Anti-Patterns

### 1. Plain Text Storage
```typescript
// L NEVER DO THIS
const password = user.password; // Stored in plain text

//  ALWAYS DO THIS
const hash = await hashPassword(user.password);
```

### 2. Weak Hashing
```typescript
// L NEVER DO THIS
const hash = crypto.createHash('md5').update(password).digest('hex');
const hash = crypto.createHash('sha256').update(password).digest('hex');

//  ALWAYS DO THIS
const hash = await argon2.hash(password);
const hash = await bcrypt.hash(password, 12);
```

### 3. No Salt / Static Salt
```typescript
// L NEVER DO THIS
const hash = sha256(password + 'myStaticSalt');

//  ALWAYS DO THIS
// bcrypt and Argon2 handle salts automatically
const hash = await bcrypt.hash(password, rounds);
```

### 4. Password in Logs
```typescript
// L NEVER DO THIS
console.log(`User login: ${username} / ${password}`);

//  ALWAYS DO THIS
console.log(`User login attempt: ${username}`);
```

### 5. Password in URLs
```typescript
// L NEVER DO THIS
GET /reset-password?token=abc&newPassword=secret123

//  ALWAYS DO THIS
POST /reset-password
Body: { token: 'abc', newPassword: 'secret123' }
```

### 6. Client-Side Hashing Only
```typescript
// L NEVER DO THIS (alone)
// Client hashes password, server stores hash
// This makes the hash the effective password

//  DO THIS
// Client can hash for transport security
// Server MUST hash again with proper algorithm
```

### 7. Timing Attacks
```typescript
// L VULNERABLE TO TIMING ATTACKS
function verifyPassword(password: string, hash: string): boolean {
  return password === hash; // String comparison leaks timing
}

//  USE CONSTANT-TIME COMPARISON
import { timingSafeEqual } from 'crypto';
// Or use bcrypt.compare() / argon2.verify() which handle this
```

## Security Checklist

### Implementation Checklist
- [ ] Use Argon2id or bcrypt (never MD5, SHA-1, SHA-256 alone)
- [ ] Implement password strength validation
- [ ] Check against compromised password database
- [ ] Enforce minimum length (12+ characters)
- [ ] Hash passwords asynchronously (don't block event loop)
- [ ] Use constant-time comparison for verification
- [ ] Implement rate limiting on authentication attempts
- [ ] Never log or expose passwords
- [ ] Use HTTPS for all password transmission
- [ ] Implement secure password reset flow

### Storage Checklist
- [ ] Never store passwords in plain text
- [ ] Store only hash (not password)
- [ ] Let algorithm handle salt automatically
- [ ] Store hash parameters with hash
- [ ] Plan for hash parameter upgrades
- [ ] Implement hash rehashing strategy
- [ ] Protect database backups
- [ ] Audit database access logs

### Policy Checklist
- [ ] Minimum 12 character length
- [ ] No maximum length (up to practical limit)
- [ ] Don't enforce complex composition rules
- [ ] Support Unicode passphrases
- [ ] Check against breach databases
- [ ] Implement account lockout after failed attempts
- [ ] Require password change after breach detection
- [ ] Notify users of password changes

## Testing Password Security

```typescript
// TODO: Add password security test suite

describe('Password Security', () => {
  describe('Hashing', () => {
    it('should hash passwords with Argon2id', async () => {});
    it('should generate unique hashes for same password', async () => {});
    it('should verify correct password', async () => {});
    it('should reject incorrect password', async () => {});
    it('should complete hashing in reasonable time (<500ms)', async () => {});
  });

  describe('Password Policy', () => {
    it('should enforce minimum length', () => {});
    it('should reject compromised passwords', async () => {});
    it('should allow strong passphrases', () => {});
    it('should support Unicode characters', () => {});
  });

  describe('Password Reset', () => {
    it('should generate secure random tokens', () => {});
    it('should expire tokens after 15 minutes', () => {});
    it('should hash reset tokens in database', () => {});
    it('should invalidate token after use', () => {});
  });
});
```

## References

- OWASP Password Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- NIST SP 800-63B: https://pages.nist.gov/800-63-3/sp800-63b.html
- Argon2 RFC: https://datatracker.ietf.org/doc/html/rfc9106
- Have I Been Pwned API: https://haveibeenpwned.com/API/v3
- Password Hashing Competition: https://www.password-hashing.net/
- OWASP Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html

## Next Steps

1. Review session management: [SESSION_MANAGEMENT.md](./SESSION_MANAGEMENT.md)
2. Implement MFA: [MFA_PATTERNS.md](./MFA_PATTERNS.md)
3. Set up rate limiting: [RATE_LIMITING.md](./RATE_LIMITING.md)
4. Configure security headers: [SECURITY_HEADERS.md](./SECURITY_HEADERS.md)
