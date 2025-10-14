# TypeScript Backend Best Practices

Created: 2025-10-13

## Overview

TypeScript patterns for Express backends.

## Type-Safe Express

```typescript
import { Request, Response, NextFunction } from 'express';

// Extend Express types
declare global {
  namespace Express {
    interface Request {
      user?: SessionUser;
    }
  }
}

// Type-safe request handler
interface TypedRequest<T> extends Request {
  body: T;
}

export const createUser = asyncHandler(
  async (req: TypedRequest<CreateUserData>, res: Response) => {
    const user = await userService.createUser(req.body);
    res.status(201).json({ data: user });
  }
);
```

## Shared Types

```typescript
// user.types.ts
export interface User {
  id: string;
  username: string;
  email: string;
  role: 'user' | 'admin';
  createdAt: Date;
  updatedAt: Date;
}

export type CreateUserData = Omit<User, 'id' | 'createdAt' | 'updatedAt'>;
export type UpdateUserData = Partial<CreateUserData>;
```

## Type Inference from Zod

```typescript
import { z } from 'zod';

const userSchema = z.object({
  username: z.string(),
  email: z.string().email(),
  password: z.string().min(8),
});

// Automatic type inference
type CreateUserData = z.infer<typeof userSchema>;
```

## Best Practices

1. **Strict mode**: Enable in tsconfig.json
2. **Shared types**: Reuse across layers
3. **Infer from schemas**: Use Zod for validation + types
4. **Type middleware**: Properly type req/res
5. **Avoid any**: Use unknown or proper types

See VALIDATION.md for Zod patterns.
