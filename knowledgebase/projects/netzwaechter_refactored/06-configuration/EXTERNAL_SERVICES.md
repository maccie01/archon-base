# External Services & Integrations

Documentation of all third-party services, APIs, and external integrations used in the Netzwächter project.

Created: 2025-10-13
Last Updated: 2025-10-13

---

## Overview

The Netzwächter application integrates with several external services for database hosting, email delivery, weather data, and potentially AI-powered features. This document provides comprehensive information about each service, configuration, and usage.

---

## Database Services

### Neon - Serverless PostgreSQL

**Purpose:** Primary database hosting
**Package:** `@neondatabase/serverless@0.10.4`
**Website:** https://neon.tech

#### Service Details

**Type:** Serverless PostgreSQL Database
**Features:**
- Auto-scaling compute
- Automatic backups
- Point-in-time recovery
- Database branching
- Global edge network
- Connection pooling

#### Integration

**Connection:**
```typescript
import { Pool } from '@neondatabase/serverless';
// Uses standard PostgreSQL connection pool
```

**Configuration:**
- Connection string via `DATABASE_URL` environment variable
- SSL/TLS encryption required in production
- Connection pooling managed by application

#### Pricing Tiers

**Free Tier:**
- 1 project
- 10 branches
- 3 GB storage
- 100 simultaneous connections
- Compute auto-suspend after 5 min

**Pro Tier:**
- Unlimited projects & branches
- Unlimited storage
- 1000+ connections
- Configurable compute
- Higher performance

#### Benefits

1. **Serverless Architecture:**
   - Pay only for compute used
   - Auto-scaling based on demand
   - No infrastructure management

2. **Developer Experience:**
   - Database branching for testing
   - Instant preview environments
   - GitHub integration

3. **Reliability:**
   - Automatic backups
   - Point-in-time recovery
   - High availability

#### Monitoring

**Neon Dashboard:**
- Connection metrics
- Query performance
- Storage usage
- Billing information

**Application Metrics:**
- Connection pool stats
- Query execution times
- Error rates

---

## Email Services

### Nodemailer - Email Delivery

**Purpose:** Email sending (password resets, notifications)
**Package:** `nodemailer@7.0.6`
**Website:** https://nodemailer.com

#### Service Details

**Type:** Email transport library
**SMTP Server:** smtps.udag.de (configured in database)
**Features:**
- SMTP transport
- TLS/SSL support
- Custom CA certificates
- Template support

#### Configuration

**SMTP Settings (stored in database - settings table):**
```json
{
  "email": "portal@monitoring.direct",
  "username": "monitoring-direct-0002",
  "smtp_server": "smtps.udag.de",
  "port_ssl": 465,
  "port_starttls": 587,
  "password_env": "MAILSERVER_PASSWORD"
}
```

**Environment Variable:**
```bash
MAILSERVER_PASSWORD=your-smtp-password
```

**Optional Custom CA:**
```bash
MAILSERVER_CA_CERT=/path/to/ca-certificate.pem
```

#### Usage

**Send Email:**
```typescript
import nodemailer from 'nodemailer';

const transporter = nodemailer.createTransport({
  host: 'smtps.udag.de',
  port: 465,
  secure: true,
  auth: {
    user: 'monitoring-direct-0002',
    pass: process.env.MAILSERVER_PASSWORD
  }
});

await transporter.sendMail({
  from: 'portal@monitoring.direct',
  to: 'user@example.com',
  subject: 'Password Reset',
  html: '<p>Reset your password...</p>'
});
```

#### Email Types

1. **Password Reset:**
   - Secure token generation
   - Time-limited links
   - User verification

2. **Notifications:**
   - System alerts
   - Maintenance reminders
   - Report delivery

3. **Account Management:**
   - Welcome emails
   - Account activation
   - Security alerts

#### Security

**TLS/SSL:**
- TLS 1.2+ required
- SSL port: 465 (recommended)
- STARTTLS port: 587

**Authentication:**
- Strong password required
- Password stored in environment variable only
- Not logged or exposed

**Best Practices:**
- Rate limiting
- SPF/DKIM/DMARC configuration
- Template validation
- Content sanitization

---

## Weather Data Services

### DWD (Deutscher Wetterdienst) via Bright Sky API

**Purpose:** Historical and current outdoor temperature data
**API:** Bright Sky API (DWD data)
**Website:** https://brightsky.dev
**Cost:** Free (public data)

#### Service Details

**Type:** Weather data API
**Provider:** Deutscher Wetterdienst (German Weather Service)
**API Wrapper:** Bright Sky
**Data Source:** Official DWD weather stations

#### Integration

**Table:** `daily_outdoor_temperatures`
**Script:** `apps/backend-api/scripts/importWeatherData.ts`

**Data Fields:**
- Date
- Postal code
- City
- Temperature min/max/mean
- Data source
- Data quality

#### API Usage

**Endpoint:**
```
GET https://api.brightsky.dev/weather
```

**Parameters:**
- `date` - Date (YYYY-MM-DD)
- `lat` - Latitude
- `lon` - Longitude
- `dwd_station_id` - Station ID

**Example Request:**
```bash
curl "https://api.brightsky.dev/weather?date=2024-01-15&lat=52.52&lon=13.40"
```

#### Data Import

**Historical Import:**
```bash
pnpm run import:weather
```

**Daily Update:**
```bash
pnpm run weather:daily
```

**Features:**
- Automatic postal code to coordinates conversion
- Daily temperature aggregation
- Data quality tracking
- Historical data backfill

#### Use Cases

1. **Heating Degree Days:**
   - Energy efficiency calculations
   - Temperature normalization
   - Performance comparisons

2. **Efficiency Analysis:**
   - Weather-corrected consumption
   - Seasonal adjustments
   - Anomaly detection

3. **Reporting:**
   - Weather context in reports
   - Climate data visualization
   - Historical comparisons

---

## Potential AI Services

### OpenAI Integration

**Purpose:** AI-powered report generation (ki-reports module)
**Package:** `openai@5.23.1`
**Status:** Configured but optional

#### Service Details

**Type:** AI/ML API
**Features:**
- Text generation
- Report synthesis
- Data analysis
- Natural language processing

#### Configuration

**Not Currently Active:**
- No API key in environment variables
- Module present: `apps/backend-api/modules/ki-reports/`
- Package installed but not required

#### Potential Use Cases

1. **Automated Reports:**
   - Energy consumption summaries
   - Efficiency recommendations
   - Anomaly explanations

2. **Data Analysis:**
   - Pattern recognition
   - Predictive maintenance
   - Optimization suggestions

3. **Natural Language:**
   - Query interface
   - Report generation
   - Data interpretation

**Note:** This integration is optional and not currently in active use. If enabled in the future, it would require:
- OpenAI API key configuration
- Rate limiting
- Usage monitoring
- Cost management

---

## Google Cloud Services

### Google Cloud Storage

**Purpose:** File storage and management
**Package:** `@google-cloud/storage@7.16.0`
**Status:** Installed but usage unclear

#### Potential Use Cases

1. **Document Storage:**
   - Logbook attachments
   - Report PDFs
   - Export files

2. **Backup Storage:**
   - Database backups
   - Configuration backups
   - Log archives

3. **Static Assets:**
   - Images
   - Documents
   - Media files

#### Configuration

**Required (if used):**
- Service account credentials
- Bucket configuration
- Access permissions
- Regional settings

**Note:** Currently installed but specific usage not documented. May be legacy dependency.

---

## Email Service Providers

### SendGrid (Optional)

**Purpose:** Alternative email delivery service
**Package:** `@sendgrid/mail@8.1.5`
**Status:** Installed but not actively used

#### Service Details

**Type:** Cloud email delivery platform
**Features:**
- Transactional emails
- Email templates
- Analytics & tracking
- High deliverability

#### Configuration (if enabled)

**Required:**
```bash
SENDGRID_API_KEY=your-api-key
```

**Usage:**
```typescript
import sgMail from '@sendgrid/mail';
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

await sgMail.send({
  to: 'user@example.com',
  from: 'portal@monitoring.direct',
  subject: 'Welcome',
  html: '<p>Welcome to Netzwächter</p>'
});
```

**Benefits:**
- Better deliverability than SMTP
- Built-in analytics
- Template management
- Webhook support

**Note:** Currently using direct SMTP (nodemailer). SendGrid is available as an alternative if needed.

---

## Authentication Services

### Google OAuth (Potential)

**Purpose:** OAuth authentication
**Package:** `google-auth-library@10.2.1`
**Status:** Installed, usage unclear

#### Potential Features

1. **Social Login:**
   - Google account authentication
   - Simplified onboarding
   - No password management

2. **API Authentication:**
   - Service account auth
   - Google Cloud services
   - API access tokens

**Note:** Package installed but not actively used in authentication flow. May be for Google Cloud Storage integration.

---

## Service Dependencies Summary

### Active Services

| Service | Purpose | Package | Status |
|---------|---------|---------|--------|
| Neon | Database | @neondatabase/serverless | Active |
| Nodemailer | Email | nodemailer | Active |
| Bright Sky API | Weather data | HTTP requests | Active |

### Installed But Inactive

| Service | Purpose | Package | Status |
|---------|---------|---------|--------|
| OpenAI | AI reports | openai | Optional |
| SendGrid | Email (alt) | @sendgrid/mail | Available |
| Google Storage | File storage | @google-cloud/storage | Available |
| Google Auth | OAuth | google-auth-library | Available |

---

## Service Configuration Best Practices

### 1. API Keys & Credentials

**Storage:**
- Environment variables only
- Never commit to git
- Different keys per environment
- Rotate regularly

**Security:**
```bash
# Strong credential generation
openssl rand -base64 32

# File permissions
chmod 600 .env
```

### 2. Rate Limiting

**Implement for All APIs:**
- Request throttling
- Retry logic with backoff
- Error handling
- Usage monitoring

**Example:**
```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});

app.use('/api/', limiter);
```

### 3. Error Handling

**Graceful Degradation:**
- Fallback mechanisms
- Service availability checks
- Error logging
- User notifications

**Example:**
```typescript
try {
  await sendEmail(options);
} catch (error) {
  logger.error('Email failed:', error);
  // Fallback: queue for retry
  await queueEmail(options);
}
```

### 4. Monitoring

**Track for Each Service:**
- Request counts
- Response times
- Error rates
- Success rates
- Usage costs

**Metrics:**
```typescript
// Service health check
async function checkServiceHealth() {
  const services = {
    database: await checkDatabaseConnection(),
    email: await checkEmailService(),
    weather: await checkWeatherAPI()
  };
  return services;
}
```

---

## Service Configuration Files

### Email Service Configuration

**Location:** Database `settings` table
**Category:** `Mailserver_Portal`
**Key:** `mailserver_config`

**Fields:**
```json
{
  "email": "portal@monitoring.direct",
  "username": "monitoring-direct-0002",
  "smtp_server": "smtps.udag.de",
  "port_ssl": 465,
  "port_starttls": 587,
  "password_env": "MAILSERVER_PASSWORD"
}
```

**Benefits:**
- Runtime configuration changes
- No application restart needed
- Per-tenant configuration possible
- Audit trail in database

---

## Troubleshooting

### Email Service Issues

**Problem:** Email sending fails

**Checks:**
1. MAILSERVER_PASSWORD is set
2. SMTP server is reachable
3. Port is correct (465 or 587)
4. Credentials are valid
5. Rate limits not exceeded

**Solutions:**
```bash
# Test SMTP connection
telnet smtps.udag.de 587

# Test authentication
curl -v --url 'smtps://smtps.udag.de:465' \
  --user 'monitoring-direct-0002:password' \
  --mail-from 'portal@monitoring.direct' \
  --mail-rcpt 'test@example.com' \
  -T message.txt
```

### Weather Data Import Issues

**Problem:** Weather import fails

**Checks:**
1. API endpoint accessible
2. Date format correct
3. Coordinates valid
4. Rate limits respected
5. Database connection active

**Solutions:**
```bash
# Test API
curl "https://api.brightsky.dev/weather?date=2024-01-15&lat=52.52&lon=13.40"

# Check logs
tail -f logs/weather-import.log

# Manual import
pnpm run import:weather
```

### Database Connection Issues

**Problem:** Cannot connect to Neon

**Checks:**
1. DATABASE_URL is set correctly
2. Internet connection available
3. Neon service status
4. Connection pool not exhausted
5. SSL mode correct

**Solutions:**
```bash
# Test connection
psql $DATABASE_URL -c "SELECT 1;"

# Check pool health
curl http://localhost:5000/api/health

# Review Neon dashboard
# Check https://console.neon.tech
```

---

## Future Service Integrations

### Potential Additions

1. **InfluxDB:**
   - Time-series data storage
   - High-performance metrics
   - Better for energy data

2. **Redis:**
   - Session storage
   - Caching layer
   - Rate limiting

3. **Prometheus/Grafana:**
   - Metrics collection
   - Visualization
   - Alerting

4. **Sentry:**
   - Error tracking
   - Performance monitoring
   - Issue management

5. **S3/MinIO:**
   - Object storage
   - File uploads
   - Backup storage

---

## Cost Considerations

### Current Costs

**Neon (Database):**
- Free tier: $0/month
- Pro tier: Variable based on usage
- Compute: Pay-per-use
- Storage: Per GB

**Bright Sky API (Weather):**
- Free (public data)
- No rate limits documented
- Courtesy rate limiting recommended

**SMTP Email:**
- Provider-dependent
- Typically fixed monthly cost
- Rate limits may apply

### Cost Optimization

**Strategies:**
1. Use free tiers where possible
2. Optimize database queries
3. Cache API responses
4. Batch operations
5. Monitor usage regularly

**Budget Monitoring:**
- Set up billing alerts
- Review usage monthly
- Optimize resource usage
- Scale based on needs

---

## Security Considerations

### API Security

**Best Practices:**
1. Rotate keys regularly (90-180 days)
2. Use environment variables
3. Implement rate limiting
4. Monitor for abuse
5. Log access attempts

### Data Security

**In Transit:**
- TLS/SSL for all external services
- Certificate validation
- Strong cipher suites

**At Rest:**
- Encrypted storage (Neon)
- Secure credential storage
- Access control

### Compliance

**Considerations:**
- GDPR (data privacy)
- Data residency requirements
- Audit logging
- Access controls

---

## References

### Service Documentation
- [Neon](https://neon.tech/docs)
- [Nodemailer](https://nodemailer.com/about/)
- [Bright Sky API](https://brightsky.dev/docs/)
- [OpenAI](https://platform.openai.com/docs)

### Internal Documentation
- Environment variables: `ENVIRONMENT_VARIABLES.md`
- Database configuration: `DATABASES.md`
- API documentation: `apps/backend-api/`
