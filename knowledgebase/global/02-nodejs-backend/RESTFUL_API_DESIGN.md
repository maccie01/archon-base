# RESTful API Design Principles

Created: 2025-10-13
Status: Research Phase - Comprehensive Skeleton

## Overview
REST (Representational State Transfer) is an architectural style for designing networked applications. This document outlines industry-standard principles and best practices for designing RESTful APIs that are intuitive, maintainable, and scalable.

## Core REST Principles

### 1. Resource-Based URLs
Resources are the fundamental concept in REST. URLs should represent resources (nouns), not actions (verbs).

```
GOOD:
GET    /api/users              # Get all users
GET    /api/users/123          # Get specific user
POST   /api/users              # Create new user
PUT    /api/users/123          # Update user
DELETE /api/users/123          # Delete user

BAD:
GET  /api/getUsers
POST /api/createUser
POST /api/updateUser
POST /api/deleteUser
```

### 2. HTTP Methods (Verbs)

| Method | Purpose | Idempotent | Safe | Request Body | Response Body |
|--------|---------|------------|------|--------------|---------------|
| GET | Retrieve resource(s) | Yes | Yes | No | Yes |
| POST | Create new resource | No | No | Yes | Yes |
| PUT | Replace entire resource | Yes | No | Yes | Yes |
| PATCH | Partial update | No | No | Yes | Yes |
| DELETE | Remove resource | Yes | No | Optional | Optional |
| HEAD | Get headers only | Yes | Yes | No | No |
| OPTIONS | Get available methods | Yes | Yes | No | Yes |

## Resource Naming Conventions

### Best Practices

1. Use plural nouns for collections
```
GET /api/users          # Collection
GET /api/users/123      # Individual resource
```

2. Use kebab-case for multi-word resources
```
GET /api/user-profiles
GET /api/order-items
```

3. Use nested resources for relationships
```
GET /api/users/123/orders           # User's orders
GET /api/users/123/orders/456       # Specific order of user
POST /api/users/123/orders          # Create order for user
```

4. Limit nesting depth (max 2-3 levels)
```
GOOD:
GET /api/users/123/orders
GET /api/orders/456/items

AVOID:
GET /api/users/123/orders/456/items/789/reviews
```

5. Use query parameters for filtering, not URLs
```
GOOD:
GET /api/users?status=active&role=admin

BAD:
GET /api/users/active/admin
```

## HTTP Status Codes

### Success Codes (2xx)
```javascript
// 200 OK - Successful GET, PUT, PATCH
res.status(200).json({ data: user });

// 201 Created - Successful POST
res.status(201).json({ data: newUser });

// 204 No Content - Successful DELETE (no body)
res.status(204).send();
```

### Client Error Codes (4xx)
```javascript
// 400 Bad Request - Invalid syntax/validation error
res.status(400).json({
  error: 'Invalid email format'
});

// 401 Unauthorized - Missing or invalid authentication
res.status(401).json({
  error: 'Authentication required'
});

// 403 Forbidden - Valid auth but insufficient permissions
res.status(403).json({
  error: 'Insufficient permissions'
});

// 404 Not Found - Resource doesn't exist
res.status(404).json({
  error: 'User not found'
});

// 409 Conflict - Resource already exists
res.status(409).json({
  error: 'Email already registered'
});

// 422 Unprocessable Entity - Semantic validation error
res.status(422).json({
  error: 'Invalid user data',
  details: [
    { field: 'age', message: 'Must be 18 or older' }
  ]
});

// 429 Too Many Requests - Rate limit exceeded
res.status(429).json({
  error: 'Rate limit exceeded',
  retryAfter: 60
});
```

### Server Error Codes (5xx)
```javascript
// 500 Internal Server Error - Unexpected error
res.status(500).json({
  error: 'An unexpected error occurred'
});

// 503 Service Unavailable - Temporary unavailability
res.status(503).json({
  error: 'Service temporarily unavailable',
  retryAfter: 300
});
```

## Response Formatting

### Standard Response Structure

#### Success Response
```javascript
{
  "success": true,
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "meta": {
    "timestamp": "2025-10-13T10:30:00Z",
    "version": "1.0"
  }
}
```

#### Error Response
```javascript
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User with ID 123 not found",
    "details": [],
    "timestamp": "2025-10-13T10:30:00Z"
  }
}
```

#### Collection Response
```javascript
{
  "success": true,
  "data": [
    { "id": 1, "name": "User 1" },
    { "id": 2, "name": "User 2" }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5,
    "hasNext": true,
    "hasPrev": false
  },
  "links": {
    "self": "/api/users?page=1",
    "next": "/api/users?page=2",
    "prev": null,
    "first": "/api/users?page=1",
    "last": "/api/users?page=5"
  }
}
```

## Pagination Patterns

### 1. Offset-Based Pagination
```javascript
// Query parameters
GET /api/users?page=2&limit=20

// Implementation
const getPaginatedUsers = async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 20;
  const offset = (page - 1) * limit;

  const users = await User.findAll({ limit, offset });
  const total = await User.count();

  res.json({
    success: true,
    data: users,
    pagination: {
      page,
      limit,
      total,
      pages: Math.ceil(total / limit)
    }
  });
};
```

### 2. Cursor-Based Pagination
```javascript
// Query parameters
GET /api/users?cursor=eyJpZCI6MTIzfQ&limit=20

// Implementation
const getCursorPaginatedUsers = async (req, res) => {
  const limit = parseInt(req.query.limit) || 20;
  const cursor = req.query.cursor ?
    JSON.parse(Buffer.from(req.query.cursor, 'base64').toString()) : null;

  const query = cursor ? { id: { $gt: cursor.id } } : {};
  const users = await User.find(query).limit(limit + 1);

  const hasNext = users.length > limit;
  const data = hasNext ? users.slice(0, -1) : users;

  const nextCursor = hasNext ?
    Buffer.from(JSON.stringify({ id: data[data.length - 1].id })).toString('base64') :
    null;

  res.json({
    success: true,
    data,
    pagination: {
      nextCursor,
      hasNext
    }
  });
};
```

### 3. Keyset Pagination
```javascript
// For time-based feeds
GET /api/posts?since=2025-10-13T00:00:00Z&until=2025-10-13T23:59:59Z&limit=20

const getKeysetPaginatedPosts = async (req, res) => {
  const { since, until, limit = 20 } = req.query;

  const posts = await Post.find({
    createdAt: {
      $gte: new Date(since),
      $lte: new Date(until)
    }
  })
  .sort({ createdAt: -1 })
  .limit(parseInt(limit));

  res.json({
    success: true,
    data: posts,
    pagination: {
      since,
      until,
      count: posts.length
    }
  });
};
```

## Filtering and Sorting

### Filtering
```javascript
// Multiple filters
GET /api/users?status=active&role=admin&country=US

// Range filters
GET /api/products?minPrice=10&maxPrice=100

// Date filters
GET /api/orders?startDate=2025-01-01&endDate=2025-12-31

// Search
GET /api/users?search=john

// Implementation
const getFilteredUsers = async (req, res) => {
  const { status, role, country, search } = req.query;

  const filters = {};
  if (status) filters.status = status;
  if (role) filters.role = role;
  if (country) filters.country = country;
  if (search) {
    filters.$or = [
      { name: { $regex: search, $options: 'i' } },
      { email: { $regex: search, $options: 'i' } }
    ];
  }

  const users = await User.find(filters);
  res.json({ success: true, data: users });
};
```

### Sorting
```javascript
// Single field
GET /api/users?sort=name

// Descending order
GET /api/users?sort=-createdAt

// Multiple fields
GET /api/users?sort=lastName,firstName

// Implementation
const getSortedUsers = async (req, res) => {
  const sortParam = req.query.sort || '-createdAt';
  const sortFields = sortParam.split(',').reduce((acc, field) => {
    const order = field.startsWith('-') ? -1 : 1;
    const fieldName = field.replace('-', '');
    acc[fieldName] = order;
    return acc;
  }, {});

  const users = await User.find().sort(sortFields);
  res.json({ success: true, data: users });
};
```

### Field Selection (Sparse Fieldsets)
```javascript
// Select specific fields
GET /api/users?fields=name,email,createdAt

// Implementation
const getUsersWithFields = async (req, res) => {
  const fields = req.query.fields?.split(',').join(' ');
  const users = await User.find().select(fields || '');
  res.json({ success: true, data: users });
};
```

## API Versioning Strategies

### 1. URL Versioning (Recommended)
```javascript
// Different versions in URL
GET /api/v1/users
GET /api/v2/users

// Implementation
app.use('/api/v1', require('./routes/v1'));
app.use('/api/v2', require('./routes/v2'));
```

### 2. Header Versioning
```javascript
// Custom header
GET /api/users
Headers: API-Version: 1

// Accept header
GET /api/users
Headers: Accept: application/vnd.myapi.v1+json

// Implementation
const versionMiddleware = (req, res, next) => {
  const version = req.headers['api-version'] || '1';
  req.apiVersion = version;
  next();
};
```

### 3. Content Negotiation
```javascript
// Accept header with version
GET /api/users
Headers: Accept: application/vnd.myapi+json;version=1

// Implementation
const parseAcceptHeader = (req, res, next) => {
  const acceptHeader = req.headers.accept || '';
  const versionMatch = acceptHeader.match(/version=(\d+)/);
  req.apiVersion = versionMatch ? versionMatch[1] : '1';
  next();
};
```

### Version Deprecation Strategy
```javascript
// Deprecated version with warning header
app.use('/api/v1', (req, res, next) => {
  res.set('X-API-Deprecated', 'true');
  res.set('X-API-Sunset', '2026-01-01');
  res.set('Link', '</api/v2>; rel="successor-version"');
  next();
});
```

## HATEOAS (Hypermedia as the Engine of Application State)

### Including Links in Responses
```javascript
{
  "success": true,
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "links": {
    "self": "/api/users/123",
    "orders": "/api/users/123/orders",
    "edit": "/api/users/123",
    "delete": "/api/users/123"
  }
}
```

### State-Based Actions
```javascript
{
  "id": 456,
  "status": "pending",
  "total": 99.99,
  "actions": {
    "cancel": {
      "method": "POST",
      "href": "/api/orders/456/cancel"
    },
    "pay": {
      "method": "POST",
      "href": "/api/orders/456/pay"
    }
  }
}
```

## Bulk Operations

### Bulk Create
```javascript
POST /api/users/bulk
{
  "users": [
    { "name": "User 1", "email": "user1@example.com" },
    { "name": "User 2", "email": "user2@example.com" }
  ]
}

// Response
{
  "success": true,
  "data": {
    "created": 2,
    "results": [
      { "id": 1, "name": "User 1" },
      { "id": 2, "name": "User 2" }
    ]
  }
}
```

### Bulk Update
```javascript
PATCH /api/users/bulk
{
  "updates": [
    { "id": 1, "status": "active" },
    { "id": 2, "status": "inactive" }
  ]
}
```

### Bulk Delete
```javascript
DELETE /api/users/bulk
{
  "ids": [1, 2, 3, 4, 5]
}

// Response
{
  "success": true,
  "data": {
    "deleted": 5
  }
}
```

## Batch Requests
```javascript
POST /api/batch
{
  "requests": [
    {
      "id": "req1",
      "method": "GET",
      "url": "/api/users/123"
    },
    {
      "id": "req2",
      "method": "GET",
      "url": "/api/orders/456"
    }
  ]
}

// Response
{
  "responses": [
    {
      "id": "req1",
      "status": 200,
      "body": { "id": 123, "name": "John" }
    },
    {
      "id": "req2",
      "status": 200,
      "body": { "id": 456, "total": 99.99 }
    }
  ]
}
```

## Long-Running Operations

### Asynchronous Processing
```javascript
// Initial request
POST /api/exports
{
  "format": "csv",
  "filters": { "status": "active" }
}

// Response with job ID
{
  "success": true,
  "data": {
    "jobId": "job-123",
    "status": "processing"
  },
  "links": {
    "status": "/api/jobs/job-123",
    "result": "/api/jobs/job-123/result"
  }
}

// Check status
GET /api/jobs/job-123
{
  "jobId": "job-123",
  "status": "completed",
  "progress": 100,
  "result": {
    "url": "/api/downloads/export-123.csv",
    "expiresAt": "2025-10-14T00:00:00Z"
  }
}
```

## Rate Limiting Headers
```javascript
// Include rate limit info in headers
res.set({
  'X-RateLimit-Limit': '100',
  'X-RateLimit-Remaining': '95',
  'X-RateLimit-Reset': '1697198400',
  'Retry-After': '60' // When rate limited
});
```

## Caching Headers
```javascript
// Cache control
res.set({
  'Cache-Control': 'public, max-age=3600',
  'ETag': 'W/"123-456"',
  'Last-Modified': 'Wed, 13 Oct 2025 10:00:00 GMT'
});

// Conditional requests
if (req.headers['if-none-match'] === etag) {
  return res.status(304).send(); // Not Modified
}
```

## Content Negotiation
```javascript
// Support multiple formats
app.get('/api/users/:id', (req, res) => {
  const user = getUserById(req.params.id);

  res.format({
    'application/json': () => res.json(user),
    'application/xml': () => res.send(toXML(user)),
    'text/html': () => res.render('user', user),
    'default': () => res.status(406).send('Not Acceptable')
  });
});
```

## Anti-Patterns to Avoid

### 1. Using Verbs in URLs
```javascript
// BAD
POST /api/createUser
GET  /api/getAllUsers
POST /api/updateUser/123

// GOOD
POST   /api/users
GET    /api/users
PUT    /api/users/123
```

### 2. Ignoring HTTP Methods
```javascript
// BAD - Using POST for everything
POST /api/users/get
POST /api/users/update
POST /api/users/delete

// GOOD - Using proper HTTP methods
GET    /api/users
PUT    /api/users/123
DELETE /api/users/123
```

### 3. Inconsistent Naming
```javascript
// BAD - Mixed conventions
GET /api/users
GET /api/user-orders
GET /api/ProductItems

// GOOD - Consistent kebab-case, plural
GET /api/users
GET /api/user-orders
GET /api/product-items
```

### 4. Not Versioning
```javascript
// BAD - Breaking changes without versioning
// Breaking change breaks all clients

// GOOD - Version your API
GET /api/v1/users  # Old clients still work
GET /api/v2/users  # New clients use new version
```

### 5. Exposing Internal IDs
```javascript
// BAD - Database IDs exposed
GET /api/users/internal-db-id-12345

// BETTER - Use UUIDs or obfuscated IDs
GET /api/users/550e8400-e29b-41d4-a716-446655440000
```

## Code Examples

### Complete RESTful Resource Implementation
```javascript
// routes/user.routes.js
const express = require('express');
const router = express.Router();
const controller = require('../controllers/user.controller');
const { authenticate, authorize } = require('../middleware/auth');
const { validate } = require('../middleware/validation');
const { userSchema } = require('../schemas/user.schema');

// Collection operations
router.get('/',
  authenticate,
  controller.getUsers
);

router.post('/',
  authenticate,
  authorize('admin'),
  validate(userSchema.create),
  controller.createUser
);

// Individual resource operations
router.get('/:id',
  authenticate,
  controller.getUser
);

router.put('/:id',
  authenticate,
  authorize('admin'),
  validate(userSchema.update),
  controller.updateUser
);

router.patch('/:id',
  authenticate,
  validate(userSchema.partialUpdate),
  controller.patchUser
);

router.delete('/:id',
  authenticate,
  authorize('admin'),
  controller.deleteUser
);

// Sub-resources
router.get('/:id/orders',
  authenticate,
  controller.getUserOrders
);

// Bulk operations
router.post('/bulk',
  authenticate,
  authorize('admin'),
  validate(userSchema.bulkCreate),
  controller.bulkCreateUsers
);

module.exports = router;
```

### Response Helper
```javascript
// utils/response-helper.js
class ResponseHelper {
  static success(res, data, statusCode = 200, meta = {}) {
    return res.status(statusCode).json({
      success: true,
      data,
      meta: {
        timestamp: new Date().toISOString(),
        ...meta
      }
    });
  }

  static created(res, data) {
    return this.success(res, data, 201);
  }

  static noContent(res) {
    return res.status(204).send();
  }

  static error(res, error, statusCode = 500) {
    return res.status(statusCode).json({
      success: false,
      error: {
        code: error.code || 'INTERNAL_ERROR',
        message: error.message,
        details: error.details || [],
        timestamp: new Date().toISOString()
      }
    });
  }

  static paginated(res, data, pagination, links = {}) {
    return res.json({
      success: true,
      data,
      pagination,
      links
    });
  }
}

module.exports = ResponseHelper;
```

## References

- REST API Design Best Practices
- RFC 7231: HTTP/1.1 Semantics and Content
- JSON API Specification (jsonapi.org)
- Microsoft REST API Guidelines
- Google API Design Guide
- OpenAPI Specification

## Related Documents

- API_DOCUMENTATION_STANDARDS.md
- EXPRESS_BEST_PRACTICES.md
- ERROR_HANDLING_PATTERNS.md
- MIDDLEWARE_PATTERNS.md
