# Connection Pooling Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Perplexity research on PostgreSQL connection pooling, PgBouncer best practices 2024-2025

## Overview

Connection pooling is essential for PostgreSQL applications in production. PostgreSQL connections are heavyweight processes, and creating new connections for each request is expensive and doesn't scale.

## Core Principles

1. Always use connection pooling in production - no exceptions
2. PostgreSQL connections are heavyweight (memory overhead per connection)
3. PgBouncer is the most popular and battle-tested pooler
4. Pool size should match your workload, not arbitrarily large
5. Monitor connection usage and adjust pool settings

## Why Connection Pooling is Essential

### Problem: Native PostgreSQL Connections

```
# TODO: Add explanation of PostgreSQL connection architecture
# Each connection = separate process
# Memory overhead per connection
# Connection establishment cost
```

### Without Pooling

```typescript
// TODO: Add anti-pattern example
// Creating new connection per request
// Resource exhaustion
// Poor performance
```

### With Pooling

```typescript
// TODO: Add pooling example
// Reusing connections
# Stable resource usage
# Better performance
```

## PgBouncer

### What is PgBouncer?

```
# TODO: Add PgBouncer overview
# Lightweight connection pooler
# Sits between application and PostgreSQL
# Three pooling modes
```

### Pooling Modes

**Session Pooling:**
```
# TODO: Add session pooling explanation
# Connection held for entire session
# Most compatible
# Least efficient for connection reuse
```

**Transaction Pooling:**
```
# TODO: Add transaction pooling explanation
# Connection returned after transaction
# Most efficient
# Some features not available (prepared statements in older versions)
```

**Statement Pooling:**
```
# TODO: Add statement pooling explanation
# Connection returned after each statement
# Most aggressive
# Rarely used
```

### Configuration

```ini
# TODO: Add PgBouncer configuration example
# pgbouncer.ini
# Database connections
# Pool sizes
# Timeouts
```

### Installation and Setup

```bash
# TODO: Add PgBouncer installation
# Docker setup
# Native installation
# Configuration files
```

## Application-Level Pooling

### Node.js with pg

```typescript
// TODO: Add node-postgres pool example
import { Pool } from 'pg';

const pool = new Pool({
  // TODO: Add configuration options
});
```

### Drizzle with Pooling

```typescript
# TODO: Add Drizzle with pg Pool
# Connection configuration
# Pool size settings
```

## Pool Sizing

### Determining Pool Size

```
# TODO: Add pool sizing guide
# Formula: connections = ((core_count * 2) + effective_spindle_count)
# Considerations for workload type
# Testing and monitoring
```

### Pool Size Anti-Patterns

```
# TODO: Add anti-pattern warnings
# Setting pool size = max_connections (wrong!)
# Arbitrary large sizes
# Not monitoring actual usage
```

## Connection Lifecycle

### Acquiring Connections

```typescript
// TODO: Add connection acquisition example
# From pool
# Timeout handling
# Error handling
```

### Releasing Connections

```typescript
// TODO: Add connection release example
# Automatic release
# Try-finally patterns
# Common mistakes
```

## Monitoring and Troubleshooting

### Monitoring Pool Health

```typescript
// TODO: Add pool monitoring examples
# Pool metrics
# Connection count
# Wait time
# Errors
```

### Common Issues

```
# TODO: Add common pooling issues
# Connection leaks
# Pool exhaustion
# Timeout errors
# Solutions for each
```

## Additional Resources

### Documentation
- PgBouncer: https://www.pgbouncer.org/
- node-postgres pooling: https://node-postgres.com/features/pooling

### Related Knowledge Base Articles
- [PostgreSQL Best Practices](./POSTGRESQL_BEST_PRACTICES.md)
- [Drizzle ORM Patterns](./DRIZZLE_PATTERNS.md)
