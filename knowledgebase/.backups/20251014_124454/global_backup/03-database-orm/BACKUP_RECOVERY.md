# Backup and Recovery Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Perplexity research on PostgreSQL backup strategies 2024-2025, disaster recovery planning

## Overview

Backups protect against data loss from hardware failure, human error, or disasters. A backup strategy is only as good as your tested recovery procedures.

## Core Principles

1. Backups you haven't tested are not backups
2. Automate backup processes
3. Store backups off-site (different geographic location)
4. Encrypt backups
5. Define RPO (Recovery Point Objective) and RTO (Recovery Time Objective)
6. Document and test recovery procedures

## Backup Types

### Logical Backups (pg_dump)

```bash
# TODO: Add pg_dump examples
# Full database backup
# Specific tables
# Custom format vs SQL
# Pros and cons
```

**Pros:**
- Portable across PostgreSQL versions
- Human-readable SQL format available
- Can backup specific tables

**Cons:**
- Slower for large databases
- Requires database to be running
- Locks tables during dump

### Physical Backups (pg_basebackup)

```bash
# TODO: Add pg_basebackup examples
# Binary backup
# Streaming replication backup
# Faster for large databases
```

**Pros:**
- Faster for large databases
- Can be used for replication
- Point-in-time recovery possible

**Cons:**
- Must be same PostgreSQL version
- Requires more storage
- Binary format

### Continuous Archiving (WAL)

```sql
# TODO: Add WAL archiving setup
# archive_mode = on
# archive_command
# Point-in-time recovery
```

## Backup Strategies

### Full Backups

```bash
# TODO: Add full backup schedule
# Daily, weekly, or monthly
# Retention policies
```

### Incremental Backups

```bash
# TODO: Add incremental backup strategy
# WAL archiving
# pgBackRest incremental backups
```

### Backup Schedule Example

```
# TODO: Add backup schedule
# Daily: incremental
# Weekly: full
# Monthly: full with extended retention
```

## Point-in-Time Recovery (PITR)

```bash
# TODO: Add PITR procedure
# Restoring to specific timestamp
# WAL replay
# Use cases
```

## Backup Tools

### pg_dump / pg_restore

```bash
# TODO: Add pg_dump/pg_restore examples
# Command syntax
# Options
# Parallel restore
```

### pgBackRest

```bash
# TODO: Add pgBackRest overview
# Features
# Configuration
# Incremental backups
```

### Barman

```bash
# TODO: Add Barman overview
# Features
# Configuration
```

## Cloud-Specific Backups

### AWS RDS Automated Backups

```
# TODO: Add RDS backup information
# Automated backups
# Snapshots
# Cross-region replication
```

### Managed PostgreSQL Services

```
# TODO: Add managed service backup features
# Azure Database for PostgreSQL
# Google Cloud SQL
# DigitalOcean Managed Databases
```

## Testing Recovery Procedures

### Regular Recovery Tests

```bash
# TODO: Add recovery test procedure
# Restore to test environment
# Verify data integrity
# Document recovery time
```

### Disaster Recovery Drills

```
# TODO: Add DR drill checklist
# Full recovery simulation
# Team training
# Documentation updates
```

## Backup Storage

### Off-Site Storage

```
# TODO: Add off-site storage recommendations
# S3, Google Cloud Storage, Azure Blob
# Geographic redundancy
```

### Backup Encryption

```bash
# TODO: Add backup encryption
# Encrypting backups
# Key management
```

### Retention Policies

```
# TODO: Add retention policy examples
# 7 daily, 4 weekly, 12 monthly
# Compliance requirements
# Storage costs
```

## Backup Monitoring

### Monitoring Backup Success

```bash
# TODO: Add backup monitoring
# Alerting on failures
# Backup age checks
# Storage capacity
```

## Recovery Scenarios

### Scenario 1: Accidental Data Deletion

```
# TODO: Add recovery procedure
# PITR to before deletion
# Selective restore
```

### Scenario 2: Hardware Failure

```
# TODO: Add hardware failure recovery
# Full restore from backup
# Replication failover
```

### Scenario 3: Corruption

```
# TODO: Add corruption recovery
# Identifying corruption
# Restoring from last good backup
```

## Backup Checklist

1. ☐ Automated daily backups configured
2. ☐ Off-site backup storage
3. ☐ Encryption enabled
4. ☐ WAL archiving for PITR
5. ☐ Documented recovery procedures
6. ☐ Regular recovery tests (quarterly minimum)
7. ☐ Monitoring and alerting
8. ☐ Retention policy defined and implemented
9. ☐ DR plan documented
10. ☐ Team trained on recovery procedures

## Additional Resources

### Documentation
- PostgreSQL Backup: https://www.postgresql.org/docs/current/backup.html
- pgBackRest: https://pgbackrest.org/
- Barman: https://www.pgbarman.org/

### Related Knowledge Base Articles
- [PostgreSQL Best Practices](./POSTGRESQL_BEST_PRACTICES.md)
- [Database Security](./DATABASE_SECURITY.md)
