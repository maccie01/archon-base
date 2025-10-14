# Express.js Best Practices

Created: 2025-10-13
Status: Research Phase - Comprehensive Skeleton

## Overview
Express.js is a minimal and flexible Node.js web application framework that provides a robust set of features for web and mobile applications. This document outlines industry-standard best practices for building scalable, maintainable Express.js applications in 2024.

## Project Structure

### Recommended Directory Layout
```
src/
├── app.js                  # Express app setup
├── server.js               # Server startup
├── config/                 # Configuration files
│   ├── database.js
│   ├── app.config.js
│   └── environment.js
├── modules/                # Feature-based modules
│   ├── users/
│   │   ├── user.controller.js
│   │   ├── user.service.js
│   │   ├── user.repository.js
│   │   ├── user.model.js
│   │   ├── user.routes.js
│   │   ├── user.validation.js
│   │   └── __tests__/
│   └── auth/
│       ├── auth.controller.js
│       ├── auth.service.js
│       └── auth.middleware.js
├── middleware/             # Global middleware
│   ├── error-handler.js
│   ├── auth.middleware.js
│   └── validation.js
├── utils/                  # Utility functions
│   ├── logger.js
│   ├── async-handler.js
│   └── api-error.js
└── tests/                  # Integration tests
```

### Alternative: Layered Structure
```
src/
├── controllers/    # Request handlers
├── services/       # Business logic
├── repositories/   # Data access
├── models/         # Data models
├── routes/         # Route definitions
└── middleware/     # Middleware
```

## Best Practices

### 1. Application Setup (app.js)
```javascript
// app.js - Separate app configuration from server
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const compression = require('compression');
const routes = require('./routes');
const errorHandler = require('./middleware/error-handler');

function createApp() {
  const app = express();

  // Security middleware
  app.use(helmet());
  app.use(cors({
    origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
    credentials: true
  }));

  // Body parsing
  app.use(express.json({ limit: '10mb' }));
  app.use(express.urlencoded({ extended: true, limit: '10mb' }));

  // Compression
  app.use(compression());

  // Request logging
  if (process.env.NODE_ENV !== 'test') {
    app.use(require('morgan')('combined'));
  }

  // Routes
  app.use('/api/v1', routes);

  // Health check
  app.get('/health', (req, res) => {
    res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() });
  });

  // 404 handler
  app.use((req, res) => {
    res.status(404).json({ error: 'Route not found' });
  });

  // Error handler (must be last)
  app.use(errorHandler);

  return app;
}

module.exports = createApp;
```

### 2. Server Startup (server.js)
```javascript
// server.js - Separate server startup for testing
const createApp = require('./app');
const logger = require('./utils/logger');

const PORT = process.env.PORT || 3000;
const app = createApp();

// Graceful shutdown
let server;

const startServer = async () => {
  try {
    // Database connection
    await require('./config/database').connect();

    server = app.listen(PORT, () => {
      logger.info(`Server running on port ${PORT} in ${process.env.NODE_ENV} mode`);
    });
  } catch (error) {
    logger.error('Failed to start server:', error);
    process.exit(1);
  }
};

const shutdown = async (signal) => {
  logger.info(`${signal} received, shutting down gracefully...`);

  if (server) {
    server.close(async () => {
      await require('./config/database').disconnect();
      logger.info('Server closed');
      process.exit(0);
    });
  }
};

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));

startServer();
```

### 3. Async/Await Patterns

#### AsyncHandler Wrapper
```javascript
// utils/async-handler.js
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

module.exports = asyncHandler;
```

#### Usage in Controllers
```javascript
// controllers/user.controller.js
const asyncHandler = require('../utils/async-handler');
const userService = require('../services/user.service');

exports.getUser = asyncHandler(async (req, res) => {
  const user = await userService.getUserById(req.params.id);
  res.status(200).json({ success: true, data: user });
});

exports.createUser = asyncHandler(async (req, res) => {
  const user = await userService.createUser(req.body);
  res.status(201).json({ success: true, data: user });
});
```

### 4. Middleware Order

Critical middleware ordering:
```javascript
// 1. Security (helmet, cors)
app.use(helmet());
app.use(cors());

// 2. Body parsing
app.use(express.json());

// 3. Compression
app.use(compression());

// 4. Logging
app.use(morgan('combined'));

// 5. Authentication (if needed globally)
app.use(authMiddleware);

// 6. Routes
app.use('/api', routes);

// 7. 404 handler
app.use(notFoundHandler);

// 8. Error handler (MUST BE LAST)
app.use(errorHandler);
```

### 5. Environment-Specific Configuration
```javascript
// config/app.config.js
const config = {
  development: {
    port: 3000,
    logLevel: 'debug',
    corsOrigin: '*'
  },
  production: {
    port: process.env.PORT,
    logLevel: 'error',
    corsOrigin: process.env.ALLOWED_ORIGINS.split(',')
  },
  test: {
    port: 3001,
    logLevel: 'silent',
    corsOrigin: '*'
  }
};

module.exports = config[process.env.NODE_ENV || 'development'];
```

## Industry Standards

### Request/Response Patterns

#### Standard Response Format
```javascript
// Success Response
{
  "success": true,
  "data": { /* payload */ },
  "message": "Operation successful" // optional
}

// Error Response
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": [] // validation errors, etc.
  }
}

// Paginated Response
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

### HTTP Status Codes
- 200: OK - Successful GET, PUT, PATCH
- 201: Created - Successful POST
- 204: No Content - Successful DELETE
- 400: Bad Request - Validation error
- 401: Unauthorized - Missing/invalid authentication
- 403: Forbidden - Insufficient permissions
- 404: Not Found - Resource doesn't exist
- 409: Conflict - Resource already exists
- 422: Unprocessable Entity - Semantic errors
- 500: Internal Server Error - Server error

### Input Validation
```javascript
// Using express-validator
const { body, param, query, validationResult } = require('express-validator');

const validateCreateUser = [
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 8 }).isStrongPassword(),
  body('name').trim().notEmpty().isLength({ max: 100 }),
  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid input',
          details: errors.array()
        }
      });
    }
    next();
  }
];

// Route usage
router.post('/users', validateCreateUser, userController.createUser);
```

## Implementation Patterns

### Module-Based Structure Pattern
```javascript
// modules/users/user.routes.js
const express = require('express');
const router = express.Router();
const controller = require('./user.controller');
const { authenticate, authorize } = require('../../middleware/auth');
const validate = require('./user.validation');

router.get('/', authenticate, controller.getUsers);
router.get('/:id', authenticate, controller.getUser);
router.post('/', authenticate, authorize('admin'), validate.create, controller.createUser);
router.put('/:id', authenticate, authorize('admin'), validate.update, controller.updateUser);
router.delete('/:id', authenticate, authorize('admin'), controller.deleteUser);

module.exports = router;
```

### Dependency Injection Pattern
```javascript
// services/user.service.js
class UserService {
  constructor(userRepository, emailService) {
    this.userRepository = userRepository;
    this.emailService = emailService;
  }

  async createUser(userData) {
    const user = await this.userRepository.create(userData);
    await this.emailService.sendWelcomeEmail(user.email);
    return user;
  }
}

// Factory function
const createUserService = () => {
  const userRepository = require('../repositories/user.repository');
  const emailService = require('./email.service');
  return new UserService(userRepository, emailService);
};

module.exports = createUserService();
```

### Request Context Pattern
```javascript
// middleware/request-context.js
const { AsyncLocalStorage } = require('async_hooks');
const asyncLocalStorage = new AsyncLocalStorage();

const requestContextMiddleware = (req, res, next) => {
  const context = {
    requestId: req.headers['x-request-id'] || generateId(),
    userId: req.user?.id,
    timestamp: Date.now()
  };

  asyncLocalStorage.run(context, () => next());
};

const getRequestContext = () => asyncLocalStorage.getStore();

module.exports = { requestContextMiddleware, getRequestContext };
```

## Anti-Patterns to Avoid

### 1. Blocking the Event Loop
```javascript
// BAD - Synchronous operations
const fs = require('fs');
app.get('/file', (req, res) => {
  const data = fs.readFileSync('/path/to/file'); // BLOCKS!
  res.send(data);
});

// GOOD - Async operations
app.get('/file', asyncHandler(async (req, res) => {
  const data = await fs.promises.readFile('/path/to/file');
  res.send(data);
}));
```

### 2. Fat Controllers
```javascript
// BAD - Business logic in controller
exports.createOrder = async (req, res) => {
  const order = await Order.create(req.body);
  const inventory = await Inventory.findById(order.productId);
  inventory.quantity -= order.quantity;
  await inventory.save();
  await sendEmail(order.userEmail, 'Order confirmation');
  res.json(order);
};

// GOOD - Delegate to service layer
exports.createOrder = asyncHandler(async (req, res) => {
  const order = await orderService.createOrder(req.body);
  res.status(201).json({ success: true, data: order });
});
```

### 3. Not Handling Async Errors
```javascript
// BAD - Unhandled promise rejection
app.get('/users', async (req, res) => {
  const users = await userService.getUsers(); // If this throws, app crashes
  res.json(users);
});

// GOOD - Using asyncHandler
app.get('/users', asyncHandler(async (req, res) => {
  const users = await userService.getUsers();
  res.json({ success: true, data: users });
}));
```

### 4. Hardcoded Configuration
```javascript
// BAD
const db = mongoose.connect('mongodb://localhost:27017/myapp');

// GOOD
const db = mongoose.connect(process.env.MONGODB_URI);
```

### 5. Not Using Compression
```javascript
// BAD - Large JSON responses without compression
app.get('/large-data', (req, res) => {
  res.json(largeDataset); // Could be MBs
});

// GOOD - Use compression middleware
app.use(compression());
```

## Performance Optimization

### 1. Enable Caching
```javascript
const apicache = require('apicache');
const cache = apicache.middleware;

// Cache for 5 minutes
app.get('/api/public-data', cache('5 minutes'), controller.getPublicData);
```

### 2. Connection Pooling
```javascript
// Database connection pool
const pool = new Pool({
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

### 3. Response Streaming
```javascript
// For large datasets
app.get('/large-export', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  const stream = databaseStream();
  stream.pipe(res);
});
```

## Testing Best Practices

### Unit Test Example
```javascript
// __tests__/user.service.test.js
describe('UserService', () => {
  let userService;
  let mockRepository;

  beforeEach(() => {
    mockRepository = {
      create: jest.fn(),
      findById: jest.fn()
    };
    userService = new UserService(mockRepository);
  });

  it('should create a user', async () => {
    const userData = { email: 'test@test.com', name: 'Test' };
    mockRepository.create.mockResolvedValue({ id: 1, ...userData });

    const user = await userService.createUser(userData);

    expect(user).toHaveProperty('id');
    expect(mockRepository.create).toHaveBeenCalledWith(userData);
  });
});
```

### Integration Test Example
```javascript
// __tests__/user.routes.test.js
const request = require('supertest');
const createApp = require('../app');

describe('User Routes', () => {
  let app;

  beforeAll(() => {
    app = createApp();
  });

  it('GET /api/users should return users list', async () => {
    const response = await request(app)
      .get('/api/users')
      .set('Authorization', 'Bearer valid-token');

    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('success', true);
    expect(response.body).toHaveProperty('data');
  });
});
```

## Security Best Practices

### 1. Helmet for Security Headers
```javascript
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"]
    }
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true
  }
}));
```

### 2. Rate Limiting
```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP'
});

app.use('/api/', limiter);
```

### 3. Input Sanitization
```javascript
const mongoSanitize = require('express-mongo-sanitize');
const xss = require('xss-clean');

app.use(mongoSanitize()); // Prevent NoSQL injection
app.use(xss()); // Prevent XSS attacks
```

## Code Examples

### Complete Feature Module
```javascript
// modules/users/index.js
module.exports = {
  routes: require('./user.routes'),
  controller: require('./user.controller'),
  service: require('./user.service'),
  model: require('./user.model')
};

// Main app.js
const userModule = require('./modules/users');
app.use('/api/users', userModule.routes);
```

## References

- Express.js Official Documentation: https://expressjs.com/
- Node.js Best Practices: https://github.com/goldbergyoni/nodebestpractices
- REST API Design Guidelines
- OWASP Node.js Security Cheat Sheet
- The Twelve-Factor App Methodology

## Related Documents

- ERROR_HANDLING_PATTERNS.md
- LAYERED_ARCHITECTURE.md
- MIDDLEWARE_PATTERNS.md
- API_DOCUMENTATION_STANDARDS.md
