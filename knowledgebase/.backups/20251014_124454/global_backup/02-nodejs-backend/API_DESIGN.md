# RESTful API Design

Created: 2025-10-13

## Overview

REST API design principles for consistent, maintainable endpoints.

## HTTP Methods

- **GET**: Retrieve resources
- **POST**: Create resources
- **PUT**: Replace resources
- **PATCH**: Update resources partially
- **DELETE**: Remove resources

## URL Structure

```
/api/users              GET    - List users
/api/users/:id          GET    - Get user
/api/users              POST   - Create user
/api/users/:id          PATCH  - Update user
/api/users/:id          DELETE - Delete user

/api/users/:id/posts    GET    - List user's posts
```

## Status Codes

- **200 OK**: Successful GET, PATCH, PUT
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Validation error
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: No permission
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

## Response Format

```typescript
// Success
{
  "data": { ... },
  "message": "Operation successful"
}

// Error
{
  "message": "Error description",
  "status": 400
}

// List with pagination
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150
  }
}
```

## Best Practices

1. **Use nouns, not verbs**: /users not /getUsers
2. **Plural names**: /users not /user
3. **Nested resources**: /users/:id/posts
4. **Versioning**: /api/v1/users (if needed)
5. **Pagination**: Include limit/offset
6. **Filtering**: Use query params (?role=admin)
7. **Consistent responses**: Same format everywhere

See EXPRESS_BEST_PRACTICES.md for implementation.
