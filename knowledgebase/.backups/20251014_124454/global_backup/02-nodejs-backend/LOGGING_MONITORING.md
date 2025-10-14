# Logging and Monitoring

Created: 2025-10-13

## Overview

Structured logging and health monitoring for production applications.

## Structured Logging

```typescript
import winston from 'winston';

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});

// Usage
logger.info('User created', { userId: user.id, username: user.username });
logger.error('Database error', { error: err.message, stack: err.stack });
```

## Request Logging

```typescript
import morgan from 'morgan';

// Development
app.use(morgan('dev'));

// Production
app.use(morgan('combined', {
  stream: { write: (message) => logger.info(message.trim()) }
}));
```

## Health Check Endpoint

```typescript
export const healthController = {
  check: asyncHandler(async (req, res) => {
    const dbHealth = await checkDatabaseHealth();
    
    const health = {
      status: dbHealth ? 'healthy' : 'unhealthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      database: dbHealth,
    };
    
    const status = health.status === 'healthy' ? 200 : 503;
    res.status(status).json(health);
  }),
};

// Route
router.get('/health', healthController.check);
```

## Database Health Check

```typescript
async function checkDatabaseHealth() {
  try {
    await pool.query('SELECT 1');
    return {
      connected: true,
      latency: Date.now() - start,
    };
  } catch (error) {
    return {
      connected: false,
      error: error.message,
    };
  }
}
```

## Best Practices

1. **Structured logs**: JSON format
2. **Log levels**: error, warn, info, debug
3. **Context**: Include relevant data
4. **Health checks**: Monitor critical services
5. **Metrics**: Track performance
6. **Alerts**: Set up for errors

See DATABASE_PATTERNS.md for connection monitoring.
