# Input Validation Patterns

Created: 2025-10-13

## Overview

Always validate user input before processing. Use Zod for TypeScript type safety and runtime validation.

## Zod Validation (Recommended)

```typescript
import { z } from 'zod';

// Define schema
const createUserSchema = z.object({
  username: z.string().min(3).max(50),
  email: z.string().email(),
  password: z.string().min(8).max(100),
  role: z.enum(['user', 'admin']).optional(),
});

// Type inference
type CreateUserData = z.infer<typeof createUserSchema>;

// Validate
const result = createUserSchema.safeParse(data);
if (!result.success) {
  throw createValidationError('Validation failed', result.error.errors);
}
```

## Validation Middleware

```typescript
export function validate(schema: ZodSchema, source = 'body') {
  return async (req, res, next) => {
    try {
      req[source] = await schema.parseAsync(req[source]);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        const formattedErrors = error.errors.map(err => ({
          field: err.path.join('.'),
          message: err.message,
        }));
        throw createValidationError('Validation failed', formattedErrors);
      }
      next(error);
    }
  };
}

// Usage
router.post('/users', validate(createUserSchema), userController.createUser);
```

## Common Validation Patterns

```typescript
// Email
z.string().email()

// Min/max length
z.string().min(3).max(50)

// Number range
z.number().int().min(1).max(100)

// Optional with default
z.string().optional().default('user')

// Enum
z.enum(['user', 'admin', 'moderator'])

// Array
z.array(z.string())

// Object
z.object({
  name: z.string(),
  age: z.number(),
})

// Regex
z.string().regex(/^[a-zA-Z0-9_]+$/)

// Custom validation
z.string().refine(val => val !== 'admin', {
  message: 'Username cannot be admin',
})
```

## Best Practices

1. **Validate all inputs**: Body, query, params
2. **Use TypeScript types**: Infer from schemas
3. **Return clear errors**: Help users fix issues
4. **Sanitize data**: Remove dangerous characters
5. **Validate business rules**: In service layer

## Additional Resources

- Zod documentation
- See CONTROLLER_LAYER.md for usage
- See MIDDLEWARE_PATTERNS.md for middleware
