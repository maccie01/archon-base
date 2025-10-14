# Authorization Patterns

Created: 2025-10-13
Status: Research Phase - Skeleton

## Overview
Comprehensive guide to authorization patterns including RBAC, ABAC, permission systems, and fine-grained access control for Node.js applications.

## Role-Based Access Control (RBAC)

### Basic RBAC Model
```typescript
// Skeleton: Role-based authorization system
enum Role {
  ADMIN = 'admin',
  USER = 'user',
  MODERATOR = 'moderator',
  GUEST = 'guest'
}

interface User {
  id: string;
  email: string;
  roles: Role[];
}

// Middleware: Check if user has required role
function requireRole(...allowedRoles: Role[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Authentication required' });
    }

    const hasRole = req.user.roles.some(role =>
      allowedRoles.includes(role)
    );

    if (!hasRole) {
      return res.status(403).json({
        error: 'Insufficient permissions',
        required: allowedRoles,
        current: req.user.roles
      });
    }

    next();
  };
}

// Usage
app.get('/admin/users',
  requireRole(Role.ADMIN),
  adminController.listUsers
);

app.post('/moderator/approve',
  requireRole(Role.ADMIN, Role.MODERATOR),
  moderatorController.approveContent
);
```

### Hierarchical RBAC
```typescript
// Skeleton: Role hierarchy
const roleHierarchy: Record<Role, number> = {
  [Role.GUEST]: 0,
  [Role.USER]: 1,
  [Role.MODERATOR]: 2,
  [Role.ADMIN]: 3
};

function hasMinimumRole(userRole: Role, requiredRole: Role): boolean {
  return roleHierarchy[userRole] >= roleHierarchy[requiredRole];
}

// Middleware with hierarchy
function requireMinimumRole(minimumRole: Role) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user || !hasMinimumRole(req.user.role, minimumRole)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
}
```

## Attribute-Based Access Control (ABAC)

### ABAC Policy Engine
```typescript
// Skeleton: Attribute-based authorization
interface Policy {
  id: string;
  resource: string;
  action: string;
  condition: (context: PolicyContext) => boolean;
}

interface PolicyContext {
  user: User;
  resource: any;
  environment: {
    time: Date;
    ip: string;
    location?: string;
  };
}

class ABACEngine {
  private policies: Policy[] = [];

  addPolicy(policy: Policy) {
    this.policies.push(policy);
  }

  evaluate(context: PolicyContext, resource: string, action: string): boolean {
    const applicablePolicies = this.policies.filter(
      p => p.resource === resource && p.action === action
    );

    return applicablePolicies.some(policy => policy.condition(context));
  }
}

// Example policies
const documentEditPolicy: Policy = {
  id: 'doc-edit-owner',
  resource: 'document',
  action: 'edit',
  condition: (context) => {
    return context.user.id === context.resource.ownerId ||
           context.user.roles.includes(Role.ADMIN);
  }
};

const timeBasedPolicy: Policy = {
  id: 'business-hours-only',
  resource: 'sensitive-data',
  action: 'access',
  condition: (context) => {
    const hour = context.environment.time.getHours();
    return hour >= 9 && hour < 17; // 9 AM to 5 PM
  }
};
```

## Permission-Based Authorization

### Permission System
```typescript
// Skeleton: Fine-grained permissions
enum Permission {
  // User permissions
  USER_CREATE = 'user:create',
  USER_READ = 'user:read',
  USER_UPDATE = 'user:update',
  USER_DELETE = 'user:delete',

  // Document permissions
  DOCUMENT_CREATE = 'document:create',
  DOCUMENT_READ = 'document:read',
  DOCUMENT_UPDATE = 'document:update',
  DOCUMENT_DELETE = 'document:delete',
  DOCUMENT_PUBLISH = 'document:publish',

  // System permissions
  SYSTEM_CONFIG = 'system:config',
  SYSTEM_AUDIT = 'system:audit'
}

interface Role {
  name: string;
  permissions: Permission[];
}

// Role definitions
const roles: Record<string, Role> = {
  admin: {
    name: 'admin',
    permissions: Object.values(Permission) // All permissions
  },
  editor: {
    name: 'editor',
    permissions: [
      Permission.DOCUMENT_CREATE,
      Permission.DOCUMENT_READ,
      Permission.DOCUMENT_UPDATE,
      Permission.DOCUMENT_PUBLISH
    ]
  },
  viewer: {
    name: 'viewer',
    permissions: [
      Permission.DOCUMENT_READ,
      Permission.USER_READ
    ]
  }
};

// Permission check middleware
function requirePermission(...requiredPermissions: Permission[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Authentication required' });
    }

    const userPermissions = getUserPermissions(req.user);
    const hasPermission = requiredPermissions.every(perm =>
      userPermissions.includes(perm)
    );

    if (!hasPermission) {
      return res.status(403).json({
        error: 'Missing required permissions',
        required: requiredPermissions
      });
    }

    next();
  };
}

function getUserPermissions(user: User): Permission[] {
  const permissions = new Set<Permission>();

  user.roles.forEach(roleName => {
    const role = roles[roleName];
    if (role) {
      role.permissions.forEach(perm => permissions.add(perm));
    }
  });

  return Array.from(permissions);
}
```

## Resource-Based Authorization

### Ownership-Based Access
```typescript
// Skeleton: Resource ownership checks
interface Resource {
  id: string;
  ownerId: string;
  collaborators?: string[];
  isPublic?: boolean;
}

function requireOwnership(resourceGetter: (req: Request) => Promise<Resource>) {
  return async (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Authentication required' });
    }

    try {
      const resource = await resourceGetter(req);

      const isOwner = resource.ownerId === req.user.id;
      const isCollaborator = resource.collaborators?.includes(req.user.id);
      const isAdmin = req.user.roles.includes(Role.ADMIN);

      if (!isOwner && !isCollaborator && !isAdmin) {
        return res.status(403).json({
          error: 'You do not have access to this resource'
        });
      }

      req.resource = resource;
      next();
    } catch (error) {
      return res.status(404).json({ error: 'Resource not found' });
    }
  };
}

// Usage
app.put('/documents/:id',
  requireOwnership(async (req) => {
    return await documentService.findById(req.params.id);
  }),
  documentController.update
);
```

### Policy-Based Resource Access
```typescript
// Skeleton: Complex resource policies
interface ResourcePolicy {
  canRead(user: User, resource: Resource): boolean;
  canUpdate(user: User, resource: Resource): boolean;
  canDelete(user: User, resource: Resource): boolean;
  canShare(user: User, resource: Resource): boolean;
}

class DocumentPolicy implements ResourcePolicy {
  canRead(user: User, resource: Resource): boolean {
    // Public documents: anyone
    if (resource.isPublic) return true;

    // Private: owner, collaborators, or admin
    return resource.ownerId === user.id ||
           resource.collaborators?.includes(user.id) ||
           user.roles.includes(Role.ADMIN);
  }

  canUpdate(user: User, resource: Resource): boolean {
    // Owner, collaborators with edit permission, or admin
    return resource.ownerId === user.id ||
           this.hasEditPermission(user, resource) ||
           user.roles.includes(Role.ADMIN);
  }

  canDelete(user: User, resource: Resource): boolean {
    // Only owner or admin
    return resource.ownerId === user.id ||
           user.roles.includes(Role.ADMIN);
  }

  canShare(user: User, resource: Resource): boolean {
    // Owner only
    return resource.ownerId === user.id;
  }

  private hasEditPermission(user: User, resource: Resource): boolean {
    // Check if user is in collaborators with edit permission
    return resource.collaborators?.includes(user.id) &&
           resource.permissions?.[user.id] === 'edit';
  }
}

// Middleware factory
function authorizeResource(
  policy: ResourcePolicy,
  action: keyof ResourcePolicy,
  resourceGetter: (req: Request) => Promise<Resource>
) {
  return async (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Authentication required' });
    }

    try {
      const resource = await resourceGetter(req);
      const authorized = policy[action](req.user, resource);

      if (!authorized) {
        return res.status(403).json({
          error: `Not authorized to ${action} this resource`
        });
      }

      req.resource = resource;
      next();
    } catch (error) {
      return res.status(404).json({ error: 'Resource not found' });
    }
  };
}
```

## Middleware Guards

### Composite Guards
```typescript
// Skeleton: Combining multiple authorization checks
type Guard = (req: Request, res: Response, next: NextFunction) => void | Promise<void>;

function composeGuards(...guards: Guard[]): Guard {
  return async (req: Request, res: Response, next: NextFunction) => {
    for (const guard of guards) {
      try {
        await new Promise<void>((resolve, reject) => {
          guard(req, res, (err?: any) => {
            if (err) reject(err);
            else resolve();
          });
        });
      } catch (error) {
        return; // Guard failed, response already sent
      }
    }
    next();
  };
}

// Usage: Multiple checks
app.delete('/documents/:id',
  composeGuards(
    requireRole(Role.USER),
    requirePermission(Permission.DOCUMENT_DELETE),
    requireOwnership(getDocument)
  ),
  documentController.delete
);
```

### Conditional Guards
```typescript
// Skeleton: Context-aware authorization
function conditionalGuard(
  condition: (req: Request) => boolean,
  ifTrue: Guard,
  ifFalse: Guard
): Guard {
  return (req: Request, res: Response, next: NextFunction) => {
    const guard = condition(req) ? ifTrue : ifFalse;
    return guard(req, res, next);
  };
}

// Example: Different rules for different resource types
app.post('/content/:type/:id/publish',
  conditionalGuard(
    (req) => req.params.type === 'article',
    requireRole(Role.EDITOR, Role.ADMIN),
    requireRole(Role.ADMIN) // Stricter for other types
  ),
  contentController.publish
);
```

## Fine-Grained Access Control

### Field-Level Authorization
```typescript
// Skeleton: Control access to specific fields
interface FieldPolicy {
  [field: string]: (user: User, resource: any) => boolean;
}

const userFieldPolicy: FieldPolicy = {
  email: (user, resource) => user.id === resource.id || user.roles.includes(Role.ADMIN),
  phone: (user, resource) => user.id === resource.id || user.roles.includes(Role.ADMIN),
  ssn: (user) => user.roles.includes(Role.ADMIN),
  role: (user) => user.roles.includes(Role.ADMIN)
};

function filterFields<T>(
  user: User,
  resource: T,
  policy: FieldPolicy
): Partial<T> {
  const filtered: any = {};

  for (const [key, value] of Object.entries(resource)) {
    const canAccess = policy[key];
    if (!canAccess || canAccess(user, resource)) {
      filtered[key] = value;
    }
  }

  return filtered;
}

// Response filtering middleware
function filterResponse(policy: FieldPolicy) {
  return (req: Request, res: Response, next: NextFunction) => {
    const originalJson = res.json.bind(res);

    res.json = function (data: any) {
      if (req.user && data) {
        if (Array.isArray(data)) {
          data = data.map(item => filterFields(req.user!, item, policy));
        } else {
          data = filterFields(req.user!, data, policy);
        }
      }
      return originalJson(data);
    };

    next();
  };
}
```

### Operation-Level Authorization
```typescript
// Skeleton: Different permissions for different operations
interface OperationPolicy {
  operation: string;
  authorize: (user: User, params: any) => boolean;
}

const operationPolicies: OperationPolicy[] = [
  {
    operation: 'bulk-delete',
    authorize: (user) => user.roles.includes(Role.ADMIN)
  },
  {
    operation: 'export-data',
    authorize: (user) => user.roles.includes(Role.ADMIN) ||
                         user.permissions.includes('data:export')
  },
  {
    operation: 'change-ownership',
    authorize: (user) => user.roles.includes(Role.ADMIN)
  }
];

function authorizeOperation(operationName: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    const policy = operationPolicies.find(p => p.operation === operationName);

    if (!policy) {
      return res.status(500).json({ error: 'Operation policy not defined' });
    }

    if (!req.user || !policy.authorize(req.user, req.body)) {
      return res.status(403).json({
        error: `Not authorized to perform ${operationName}`
      });
    }

    next();
  };
}
```

## Security Considerations

### Principle of Least Privilege
- Grant minimum permissions necessary
- Regular permission audits
- Time-limited elevated permissions
- Explicit deny over implicit allow

### Defense in Depth
- Multiple layers of authorization
- Backend validation (never trust frontend)
- Resource-level checks even with role checks
- Audit logging of authorization decisions

### Authorization Bypass Prevention
```typescript
// Skeleton: Prevent common authorization bypasses
class AuthorizationService {
  // Never check authorization only on the frontend
  // Always verify on backend for each request

  // Prevent IDOR (Insecure Direct Object Reference)
  async checkResourceAccess(userId: string, resourceId: string): Promise<boolean> {
    const resource = await this.getResource(resourceId);
    if (!resource) return false;

    // Always verify user has access to specific resource
    return this.userCanAccessResource(userId, resource);
  }

  // Prevent mass assignment vulnerabilities
  filterUpdateFields(user: User, updates: any): any {
    const allowedFields = this.getAllowedFieldsForUser(user);
    return Object.keys(updates)
      .filter(key => allowedFields.includes(key))
      .reduce((obj, key) => ({ ...obj, [key]: updates[key] }), {});
  }

  // Prevent privilege escalation
  validateRoleChange(actor: User, targetUser: User, newRole: Role): boolean {
    // Users cannot elevate their own privileges
    if (actor.id === targetUser.id) return false;

    // Users cannot assign roles higher than their own
    const actorHighestRole = this.getHighestRole(actor);
    return roleHierarchy[actorHighestRole] > roleHierarchy[newRole];
  }
}
```

## Common Vulnerabilities

1. **Insecure Direct Object References (IDOR)**
   - Always verify user access to specific resource IDs
   - Never trust client-provided IDs without authorization

2. **Privilege Escalation**
   - Validate role/permission changes
   - Prevent users from elevating their own privileges

3. **Missing Function Level Access Control**
   - Protect all API endpoints
   - Backend validation for every operation

4. **Broken Access Control**
   - Test authorization with different user roles
   - Implement consistent authorization patterns

## Anti-Patterns to Avoid

1. Frontend-only authorization checks
2. Trusting user-supplied data for authorization
3. Hardcoding role names in multiple places
4. Not checking authorization for API calls
5. Mixing authentication and authorization logic
6. Not testing authorization boundaries
7. Using overly permissive default permissions

## Testing Authorization

```typescript
// Skeleton: Authorization tests
describe('Authorization', () => {
  describe('RBAC', () => {
    it('should allow admin to access admin routes', async () => {});
    it('should deny non-admin access to admin routes', async () => {});
    it('should respect role hierarchy', async () => {});
  });

  describe('Resource Authorization', () => {
    it('should allow owner to edit resource', async () => {});
    it('should deny non-owner to edit resource', async () => {});
    it('should allow admin to edit any resource', async () => {});
  });

  describe('Permission System', () => {
    it('should grant access with required permission', async () => {});
    it('should deny access without permission', async () => {});
    it('should combine permissions from multiple roles', async () => {});
  });

  describe('IDOR Prevention', () => {
    it('should prevent accessing other users resources', async () => {});
    it('should validate resource ownership', async () => {});
  });
});
```

## Industry Standards

- OWASP Authorization Cheat Sheet
- NIST RBAC Model
- XACML (eXtensible Access Control Markup Language)
- ABAC Guide by NIST
- OAuth 2.0 Scopes
- CASBIN Authorization Library

## References

- OWASP Access Control Guidelines
- NIST RBAC: A Multi-Dimensional View
- AWS IAM Best Practices
- Azure RBAC Documentation
- Auth0 Authorization Guide
- CASBIN Documentation
