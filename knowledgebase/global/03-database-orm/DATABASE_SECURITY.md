# Database Security Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Perplexity research on database security 2024-2025, SQL injection prevention, PostgreSQL security hardening

## Overview

Database security protects against unauthorized access, data breaches, and SQL injection attacks. Security must be built in from the start, not added later.

## Core Principles

1. Never trust user input - always use parameterized queries
2. Principle of least privilege - minimal necessary permissions
3. Defense in depth - multiple security layers
4. Encrypt sensitive data at rest and in transit
5. Regular security audits and updates

## SQL Injection Prevention

### Always Use Parameterized Queries

```typescript
// TODO: Add parameterized query examples
# GOOD: Parameterized
# BAD: String concatenation
# ORM safety
```

### Input Validation

```typescript
// TODO: Add input validation patterns
# Zod schemas
# Type checking
# Whitelist validation
```

## Authentication and Authorization

### User Management

```sql
# TODO: Add PostgreSQL user management
# CREATE ROLE
# GRANT/REVOKE permissions
# Role hierarchy
```

### Application Users

```
# TODO: Add application user patterns
# Separate users per service
# Read-only users for reporting
# Never use superuser
```

### Row-Level Security (RLS)

```sql
# TODO: Add RLS policy examples
# Multi-tenancy with RLS
# User-based access control
```

## Encryption

### SSL/TLS Connections

```typescript
# TODO: Add SSL connection configuration
# Requiring SSL
# Certificate validation
```

### Column-Level Encryption

```sql
# TODO: Add pgcrypto examples
# Encrypting sensitive fields
# Key management
```

## Network Security

### pg_hba.conf Configuration

```conf
# TODO: Add pg_hba.conf best practices
# IP restrictions
# Authentication methods
# scram-sha-256 vs md5
```

### Firewall Rules

```
# TODO: Add firewall configuration
# Restricting PostgreSQL port access
# VPN requirements
```

## Auditing and Monitoring

### Logging

```sql
# TODO: Add logging configuration
# log_statement
# log_connections
# Audit trail
```

### Failed Login Attempts

```sql
# TODO: Add failed login monitoring
# Detecting brute force attempts
```

## Password Management

### Password Policies

```
# TODO: Add password policy recommendations
# Minimum complexity
# Rotation policies
# Storage (bcrypt/scrypt/argon2)
```

## Backup Security

```
# TODO: Add backup security
# Encrypted backups
# Secure storage
# Access control
```

## Security Checklist

1. ☐ Use parameterized queries everywhere
2. ☐ Implement proper authentication
3. ☐ Apply least privilege principle
4. ☐ Enable SSL/TLS
5. ☐ Configure pg_hba.conf properly
6. ☐ Encrypt sensitive data
7. ☐ Enable audit logging
8. ☐ Regular security updates
9. ☐ Secure backups
10. ☐ Regular security audits

## Additional Resources

### Documentation
- PostgreSQL Security: https://www.postgresql.org/docs/current/security.html

### Related Knowledge Base Articles
- [Multi-Tenancy](./MULTI_TENANCY.md)
- [Audit Logging](./AUDIT_LOGGING.md)
- [PostgreSQL Best Practices](./POSTGRESQL_BEST_PRACTICES.md)
