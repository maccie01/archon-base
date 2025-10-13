# Node.js Backend Antipatterns

Created: 2025-10-13
Last Updated: 2025-10-13

## Overview

Common mistakes to avoid when building Node.js backends.

## Architecture Antipatterns

### 1. Fat Controllers

**Problem**: Controllers contain business logic

```typescript
// BAD
export const createUser = async (req, res) => {
  const { username, email, password } = req.body;
  
  // Business logic in controller
  if (username.length < 3) {
    return res.status(400).json({ error: 'Username too short' });
  }
  
  const existingUser = await pool.query('SELECT * FROM users WHERE username = $1', [username]);
  if (existingUser.rows.length > 0) {
    return res.status(400).json({ error: 'Username taken' });
  }
  
  const hashedPassword = await bcrypt.hash(password, 12);
  const result = await pool.query('INSERT INTO users (...) VALUES (...)', [...]);
  
  res.status(201).json({ data: result.rows[0] });
};
```

**Solution**: Move to service layer

```typescript
// GOOD
export const createUser = asyncHandler(async (req, res) => {
  const user = await userService.createUser(req.body);
  res.status(201).json({ data: user });
});
```

### 2. No Error Handling

**Problem**: Async errors crash the server

```typescript
// BAD
app.get('/users/:id', async (req, res) => {
  const user = await userService.getUser(req.params.id);
  res.json({ data: user });
});
```

**Solution**: Use asyncHandler

```typescript
// GOOD
app.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await userService.getUser(req.params.id);
  res.json({ data: user });
}));
```

### 3. SQL Injection

**Problem**: String concatenation in queries

```typescript
// BAD - SQL INJECTION VULNERABILITY
const userId = req.params.id;
const result = await pool.query(`SELECT * FROM users WHERE id = '${userId}'`);
```

**Solution**: Use parameterized queries

```typescript
// GOOD
const result = await pool.query('SELECT * FROM users WHERE id = $1', [userId]);
```

### 4. No Input Validation

**Problem**: Trusting user input

```typescript
// BAD
export const createUser = async (req, res) => {
  const user = await userRepository.create(req.body);
  res.status(201).json({ data: user });
};
```

**Solution**: Validate with Zod or middleware

```typescript
// GOOD
const createUserSchema = z.object({
  username: z.string().min(3).max(50),
  email: z.string().email(),
  password: z.string().min(8),
});

router.post('/users', validate(createUserSchema), userController.createUser);
```

### 5. Blocking the Event Loop

**Problem**: Synchronous operations

```typescript
// BAD
const fs = require('fs');
const data = fs.readFileSync('large-file.json', 'utf8'); // Blocks!
```

**Solution**: Use async operations

```typescript
// GOOD
const data = await fs.promises.readFile('large-file.json', 'utf8');
```

### 6. Not Using Connection Pooling

**Problem**: Creating new connections

```typescript
// BAD
export async function getUser(id: string) {
  const client = new Client({ connectionString: process.env.DATABASE_URL });
  await client.connect();
  const result = await client.query('SELECT * FROM users WHERE id = $1', [id]);
  await client.end();
  return result.rows[0];
}
```

**Solution**: Use connection pool

```typescript
// GOOD
export async function getUser(id: string) {
  const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
  return result.rows[0];
}
```

### 7. Exposing Sensitive Data

**Problem**: Returning password hashes

```typescript
// BAD
export async function getUser(id: string) {
  const user = await userRepository.findById(id);
  return user; // Includes password hash!
}
```

**Solution**: Sanitize data

```typescript
// GOOD
export async function getUser(id: string) {
  const user = await userRepository.findById(id);
  const { password, ...sanitized } = user;
  return sanitized;
}
```

### 8. No Rate Limiting

**Problem**: Vulnerable to abuse

```typescript
// BAD - No protection
app.post('/api/auth/login', authController.login);
```

**Solution**: Add rate limiting

```typescript
// GOOD
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
});

app.use('/api', limiter);
```

### 9. Ignoring HTTP Status Codes

**Problem**: Always returning 200

```typescript
// BAD
res.json({ error: 'User not found' }); // Status 200!
```

**Solution**: Use appropriate codes

```typescript
// GOOD
throw createNotFoundError('User not found'); // Status 404
```

### 10. Callback Hell

**Problem**: Nested callbacks

```typescript
// BAD
getUser(id, (err, user) => {
  if (err) return handleError(err);
  getPosts(user.id, (err, posts) => {
    if (err) return handleError(err);
    getComments(posts[0].id, (err, comments) => {
      if (err) return handleError(err);
      res.json({ user, posts, comments });
    });
  });
});
```

**Solution**: Use async/await

```typescript
// GOOD
const user = await getUser(id);
const posts = await getPosts(user.id);
const comments = await getComments(posts[0].id);
res.json({ user, posts, comments });
```

## Additional Resources

- See EXPRESS_BEST_PRACTICES.md
- See ERROR_HANDLING.md
- See SECURITY.md
