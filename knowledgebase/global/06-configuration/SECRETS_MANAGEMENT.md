# Secrets Management Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Security best practices, secrets management patterns, DevSecOps

## Overview

Secrets (passwords, API keys, tokens, certificates) require special handling to prevent security breaches. Never commit secrets to version control.

## Core Principles

1. **Never Commit Secrets** - Use .gitignore
2. **Encrypt at Rest** - Use secrets managers
3. **Rotate Regularly** - Change secrets periodically
4. **Least Privilege** - Grant minimal access
5. **Audit Access** - Log secret usage

## Local Development

### .env Files (Development Only)
```bash
# .env (gitignored)
DATABASE_PASSWORD=dev_password
JWT_SECRET=dev_secret_key_min_32_chars
API_KEY=sk_test_1234567890
```

### .env.example (Committed)
```bash
# .env.example
DATABASE_PASSWORD=
JWT_SECRET=
API_KEY=
```

### Never Commit Secrets
```bash
# .gitignore
.env
.env.local
.env.*.local
secrets/
*.key
*.pem
```

## Production Secrets Management

### Cloud Provider Secrets Managers

#### AWS Secrets Manager
```typescript
// TODO: Add AWS Secrets Manager example
// Retrieving secrets, caching, rotation
```

#### Azure Key Vault
```typescript
// TODO: Add Azure Key Vault example
```

#### Google Cloud Secret Manager
```typescript
// TODO: Add GCP Secret Manager example
```

### HashiCorp Vault
```typescript
// TODO: Add Vault integration example
```

### Doppler
```typescript
// TODO: Add Doppler secrets sync
```

## Secret Rotation

### Automated Rotation
```typescript
// TODO: Add rotation strategy
// Regular schedule, post-incident rotation
```

### Rotation Checklist
- [ ] Database passwords
- [ ] API keys
- [ ] JWT secrets
- [ ] Session secrets
- [ ] Encryption keys
- [ ] Service credentials

## Secret Detection

### Pre-commit Hooks
```bash
# TODO: Add git-secrets or gitleaks
```

### CI/CD Scanning
```yaml
# TODO: Add secret scanning in CI
```

### Tools
- git-secrets
- gitleaks
- truffleHog
- detect-secrets

## Access Control

### Principle of Least Privilege
```typescript
// TODO: Add IAM role examples
// Minimal permissions per service
```

### Audit Logging
```typescript
// TODO: Add secret access logging
```

## Secret Types

### Database Credentials
```bash
DATABASE_URL=postgresql://user:password@host:port/db
```

### API Keys
```bash
STRIPE_API_KEY=sk_live_...
SENDGRID_API_KEY=SG....
```

### JWT/Session Secrets
```bash
JWT_SECRET=minimum_32_char_random_string
SESSION_SECRET=another_random_string
```

### Encryption Keys
```bash
ENCRYPTION_KEY=base64_encoded_key
```

### Certificates
```bash
SSL_CERT_PATH=/path/to/cert.pem
SSL_KEY_PATH=/path/to/key.pem
```

## Best Practices

1. Never commit secrets to git
2. Use secrets managers in production
3. Rotate secrets regularly
4. Use strong random secrets
5. Encrypt secrets at rest
6. Audit secret access
7. Minimal secret exposure
8. Use short-lived tokens when possible
9. Scan for leaked secrets
10. Document secret requirements

## Common Mistakes

### 1. Committing Secrets
```bash
# Bad: .env committed to git
git add .env

# Good: .env in .gitignore
echo ".env" >> .gitignore
```

### 2. Logging Secrets
```typescript
// Bad
console.log(`Database URL: ${process.env.DATABASE_URL}`)

// Good
console.log('Database connection established')
```

### 3. Weak Secrets
```bash
# Bad
JWT_SECRET=secret

# Good
JWT_SECRET=randomly_generated_32_char_minimum_string
```

## Tools and Services

### Secrets Managers
- AWS Secrets Manager
- Azure Key Vault
- Google Cloud Secret Manager
- HashiCorp Vault
- Doppler
- 1Password Secrets Automation

### Detection Tools
- gitleaks
- git-secrets
- truffleHog
- GitHub secret scanning

## Additional Resources

- [ENVIRONMENT_VARIABLES.md](./ENVIRONMENT_VARIABLES.md) - Env var management
- [CI_CD_PATTERNS.md](./CI_CD_PATTERNS.md) - CI/CD secrets
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
