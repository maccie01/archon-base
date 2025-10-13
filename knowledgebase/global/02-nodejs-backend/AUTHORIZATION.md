# Authorization Patterns

Created: 2025-10-13

## Overview

Authorization controls what authenticated users can access.

## Role-Based Access Control (RBAC)

```typescript
export function requireRole(role: string) {
  return (req, res, next) => {
    const user = req.session?.user;
    
    if (!user) {
      throw createAuthError('Authentication required');
    }
    
    if (user.role !== role && user.role !== 'superadmin') {
      throw createForbiddenError(`Role '${role}' required`);
    }
    
    next();
  };
}

// Usage
router.delete('/users/:id', requireRole('admin'), userController.deleteUser);
```

## Resource Ownership Check

```typescript
export async function requireOwnership(req, res, next) {
  const userId = req.params.id;
  const currentUserId = req.session?.user?.id;
  
  if (userId !== currentUserId && req.session?.user?.role !== 'admin') {
    throw createForbiddenError('Can only modify own resources');
  }
  
  next();
}

// Usage
router.patch('/users/:id', requireAuth, requireOwnership, userController.updateUser);
```

## Permission-Based

```typescript
const permissions = {
  'user.read': ['user', 'admin'],
  'user.write': ['admin'],
  'user.delete': ['admin'],
};

export function requirePermission(permission: string) {
  return (req, res, next) => {
    const userRole = req.session?.user?.role;
    
    if (!permissions[permission]?.includes(userRole)) {
      throw createForbiddenError('Insufficient permissions');
    }
    
    next();
  };
}
```

## Best Practices

1. **Check authentication first**: Then authorization
2. **Fail securely**: Default to deny
3. **Centralize logic**: Reusable middleware
4. **Audit access**: Log authorization failures
5. **Test thoroughly**: Security-critical code

See AUTHENTICATION.md and MIDDLEWARE_PATTERNS.md.
