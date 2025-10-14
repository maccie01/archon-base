# Docker Patterns Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Docker best practices, container optimization

## Overview

Docker containerizes applications for consistent deployment across environments. This guide covers Dockerfile patterns, docker-compose, and container best practices.

## Core Principles

1. **Lightweight Images** - Minimize image size
2. **Layer Caching** - Optimize build speed
3. **Security** - Run as non-root user
4. **Single Process** - One process per container
5. **Immutability** - Containers don't change

## Dockerfile Patterns

### Node.js Application
```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM node:20-alpine

WORKDIR /app

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./

USER node

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

### Multi-Stage Build
```dockerfile
# TODO: Add complete multi-stage example
```

### Development Dockerfile
```dockerfile
# TODO: Add dev Dockerfile with hot reload
```

## Docker Compose

### Basic Setup
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    volumes:
      - .:/app
      - /app/node_modules
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Best Practices

1. Use multi-stage builds
2. Minimize layers
3. Cache dependencies
4. Use .dockerignore
5. Run as non-root user
6. Keep images small
7. Use specific versions
8. Scan for vulnerabilities
9. One process per container
10. Use health checks

## .dockerignore

```
node_modules
npm-debug.log
dist
.git
.env
coverage
.vscode
```

## Security

### Non-Root User
```dockerfile
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001

USER nodejs
```

### Scan for Vulnerabilities
```bash
docker scan myapp:latest
```

## Additional Resources

- [DEPLOYMENT_CONFIG.md](./DEPLOYMENT_CONFIG.md) - Deployment
- [CI_CD_PATTERNS.md](./CI_CD_PATTERNS.md) - Automation
- [Docker Documentation](https://docs.docker.com/)
