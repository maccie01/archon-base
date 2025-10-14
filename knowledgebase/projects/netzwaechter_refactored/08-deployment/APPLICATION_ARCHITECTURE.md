# Netzwächter Application Architecture

Production Server: 91.98.156.158 (netzwaechter.nexorithm.io)

Created: 2025-10-14

---

## Table of Contents

1. [Overview](#overview)
2. [Application Structure](#application-structure)
3. [Backend Architecture](#backend-architecture)
4. [Frontend Architecture](#frontend-architecture)
5. [Database Configuration](#database-configuration)
6. [Process Management](#process-management)
7. [Web Server Configuration](#web-server-configuration)
8. [Build Process](#build-process)
9. [Environment Variables](#environment-variables)
10. [Monitoring and Logging](#monitoring-and-logging)
11. [Architecture Diagrams](#architecture-diagrams)

---

## Overview

Netzwächter is a comprehensive network monitoring and energy management platform built with modern web technologies. The application follows a monorepo structure with separate backend and frontend applications.

### Technology Stack

- **Frontend**: React 18.3.1 + Vite 5.4.19 + TypeScript 5.6.3
- **Backend**: Node.js 20.19.5 + Express 4.21.2 + TypeScript
- **Database**: PostgreSQL (Neon hosted at 23.88.40.91:50184)
- **ORM**: Drizzle ORM 0.39.1
- **Process Manager**: PM2 (cluster mode)
- **Web Server**: Nginx (reverse proxy + static file serving)
- **Build Tools**: Vite (frontend), esbuild (backend), Turbo (monorepo)

---

## Application Structure

### Code Location

```
/opt/netzwaechter/
```

### Directory Structure

```
/opt/netzwaechter/
├── apps/
│   ├── backend-api/          # Backend Express application
│   │   ├── index.ts          # Entry point
│   │   ├── routes/           # API routes
│   │   ├── db/               # Database configuration
│   │   └── middleware/       # Express middleware
│   └── frontend-web/         # Frontend React application
│       ├── src/              # Source code
│       ├── public/           # Static assets
│       └── dist/             # Build output (production)
├── packages/
│   └── shared-types/         # Shared TypeScript types
│       └── schema.ts         # Drizzle schema definitions
├── config/                   # Configuration files
│   ├── build/                # Build configurations
│   └── testing/              # Test configurations
├── dist/                     # Backend build output
│   └── index.js             # Bundled backend (473KB)
├── logs/                     # Application logs
│   ├── pm2-out.log          # PM2 stdout logs
│   └── pm2-error.log        # PM2 stderr logs
├── .env                      # Environment variables (production)
├── ecosystem.config.cjs      # PM2 configuration
├── package.json              # Dependencies and scripts
└── node_modules/             # Dependencies
```

---

## Backend Architecture

### Entry Point

**Location**: `/opt/netzwaechter/dist/index.js`

**Source**: `apps/backend-api/index.ts`

### Core Components

#### 1. Express Application Setup

```typescript
// Port configuration
const port = parseInt(process.env.PORT || '3000', 10);

// Middleware stack
- express.json({ limit: '10mb' })
- express.urlencoded({ extended: false, limit: '10mb' })
- apiRateLimiter (DoS protection)
- Request/Response logging middleware
```

#### 2. API Routes

Routes are organized under `/api/*` and include:

- `/api/auth/*` - Authentication endpoints
- `/api/admin/*` - Admin functionality
- `/api/objects/*` - Object management
- `/api/mandants/*` - Tenant management
- `/api/users/*` - User management
- `/api/logbook/*` - Maintenance logbook
- `/api/agents/*` - Automated agents
- `/api/settings/*` - System settings

#### 3. Special Endpoints

**Health Check**: `GET /health`
```json
{
  "status": "healthy",
  "timestamp": "2025-10-14T15:52:00.000Z",
  "uptime": 3600
}
```

**Iframe Wrapper**: `GET /startki` - Provides embedded view

#### 4. Server Configuration

```typescript
server.listen({
  port: 3000,
  host: "0.0.0.0",
  reusePort: true, // Enables cluster mode port sharing
});
```

### Database Connection

**Initialization**: `apps/backend-api/db/index.ts`

```typescript
import { neon } from "@neondatabase/serverless";
import { drizzle } from "drizzle-orm/neon-http";
import * as schema from "@shared/schema";

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql, { schema });
```

### Key Features

1. **BigInt Serialization**: Automatic conversion to Number for JSON responses
2. **Rate Limiting**: Protection against API abuse
3. **Request Logging**: Detailed API request/response logging
4. **Graceful Shutdown**: SIGINT handler for clean process termination
5. **Error Handling**: Global error middleware for consistent error responses

---

## Frontend Architecture

### Build Output

**Location**: `/opt/netzwaechter/apps/frontend-web/dist/`

### Build Configuration

**Vite Config** (`apps/frontend-web/vite.config.ts`):

```typescript
{
  plugins: [react()],
  resolve: {
    alias: {
      '@': './src',
      '@shared': '../../packages/shared-types',
      '@netzwaechter/shared-validation': '../../packages/shared-validation/src'
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
}
```

### Application Structure

```
apps/frontend-web/
├── src/
│   ├── pages/              # Page components
│   ├── components/         # Reusable components
│   ├── hooks/              # Custom React hooks
│   ├── lib/                # Utilities and helpers
│   ├── api/                # API client functions
│   └── App.tsx             # Root component
├── public/                 # Static assets
├── dist/                   # Production build
│   ├── index.html
│   ├── assets/
│   │   ├── index-[hash].js
│   │   └── index-[hash].css
│   └── ...
└── index.html              # Template
```

### Key Libraries

- **UI Components**: Radix UI primitives
- **Styling**: Tailwind CSS 3.4.17
- **State Management**: TanStack Query 5.60.5
- **Routing**: Wouter 3.3.5
- **Forms**: React Hook Form 7.55.0 + Zod validation
- **Charts**: Recharts 2.15.4
- **Maps**: Leaflet 1.9.4 + React Leaflet

---

## Database Configuration

### Connection Details

- **Type**: PostgreSQL (Neon Serverless)
- **Host**: 23.88.40.91:50184
- **Database**: 20251001_neu_neondb
- **Connection**: Via `DATABASE_URL` environment variable
- **ORM**: Drizzle ORM

### Database Schema

**Location**: `packages/shared-types/schema.ts`

#### Core Tables

1. **users** - User accounts and authentication
   - Primary Key: `id` (VARCHAR)
   - Authentication: username/email + bcrypt password
   - Profiles: Linked to `user_profiles`
   - Multi-tenant: `mandant_id` + `mandant_access` (JSONB)

2. **mandants** - Tenant organizations
   - Primary Key: `id` (SERIAL)
   - Info fields: address, contact (JSONB)

3. **objects** - Monitored network objects/devices
   - Primary Key: `id` (SERIAL)
   - Unique Key: `objectid` (BIGINT)
   - Location: latitude, longitude, postal_code, city
   - Data fields: objdata, objanlage, portdata, meter, dashboard, alarm, etc. (JSONB)
   - Energy data: fltemp, rttemp, energy (JSONB)

4. **day_comp** - Daily consumption data
   - Time-series data with energy, volume, temperature, flow, power metrics
   - Indexed on: `_time`, `log` (object ID), composite index

5. **view_mon_comp** - Monthly aggregated data (PostgreSQL VIEW)
   - Monthly consumption calculations

6. **sessions** - Express session storage
   - Session-based authentication

7. **settings** - System, tenant, and user settings
   - Hierarchical: system-wide, tenant-specific, user-specific

8. **logbook_entries** - Maintenance logbook
   - Links to objects, tracks technician work, costs, attachments

9. **todo_tasks** - Task management

10. **agents** - Automated data collection agents
    - Trigger, source, processing, target configs (JSONB)

11. **daily_outdoor_temperatures** - Weather data by postal code
    - DWD (Deutscher Wetterdienst) data via Bright Sky API

12. **collaboration_annotations** - Team collaboration features
    - Real-time annotations, comments, threading

### Indexes

Strategic indexes on:
- Object lookups: `objectid`, `mandant_id`, `type`, `status`
- Time-series queries: `_time`, `log`
- Location queries: `city`, `postal_code`
- User activity: `user_id`, `action`, `timestamp`

---

## Process Management

### PM2 Configuration

**File**: `/opt/netzwaechter/ecosystem.config.cjs`

```javascript
module.exports = {
  apps: [{
    name: 'netzwaechter',
    script: './dist/index.js',
    cwd: '/opt/netzwaechter',
    instances: 2,                      // 2 cluster instances
    exec_mode: 'cluster',              // Cluster mode for load balancing
    env: envConfig,                    // Loaded from .env
    error_file: './logs/pm2-error.log',
    out_file: './logs/pm2-out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true,
    autorestart: true,                 // Auto-restart on crash
    watch: false,                      // No file watching
    max_memory_restart: '1G'           // Restart if memory exceeds 1GB
  }]
};
```

### Process Details

- **Node.js Version**: 20.19.5
- **Instances**: 2 processes (IDs 0 and 1)
- **Execution Mode**: cluster_mode (load balanced)
- **Memory Usage**: ~85-86 MB per instance
- **Uptime**: Auto-restart on failures (3 restarts recorded)
- **PID Files**: `/root/.pm2/pids/netzwaechter-{0,1}.pid`

### PM2 Management Commands

```bash
# View process status
pm2 list
pm2 describe netzwaechter

# View logs
pm2 logs netzwaechter
pm2 logs netzwaechter --lines 1000

# Process control
pm2 restart netzwaechter
pm2 reload netzwaechter    # Zero-downtime reload
pm2 stop netzwaechter
pm2 delete netzwaechter

# Monitor performance
pm2 monit

# Save process list (for auto-startup)
pm2 save
pm2 startup
```

### Log Files

- **Output**: `/opt/netzwaechter/logs/pm2-out.log`
- **Errors**: `/opt/netzwaechter/logs/pm2-error.log`
- **Format**: Timestamped with timezone

---

## Web Server Configuration

### Nginx Configuration

**File**: `/etc/nginx/sites-available/netzwaechter`

**Domain**: netzwaechter.nexorithm.io

### Configuration Overview

```nginx
server {
    server_name netzwaechter.nexorithm.io;

    # Frontend - Serve static files from build directory
    root /opt/netzwaechter/apps/frontend-web/dist;
    index index.html;

    # API Proxy - Forward API requests to Node.js backend
    location /api/ {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # WebSocket Support
    location /ws {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Frontend SPA - Fallback to index.html for client-side routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 10240;
    gzip_proxied expired no-cache no-store private auth;
    gzip_types text/plain text/css text/xml text/javascript
               application/x-javascript application/xml+rss application/json;

    # SSL Configuration (Let's Encrypt)
    listen [::]:443 ssl ipv6only=on;
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/netzwaechter.nexorithm.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/netzwaechter.nexorithm.io/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

# HTTP to HTTPS Redirect
server {
    listen 80;
    listen [::]:80;
    server_name netzwaechter.nexorithm.io;
    return 301 https://$host$request_uri;
}
```

### Request Flow

1. **Static Assets** (HTML, CSS, JS, images)
   - Client → Nginx → `/opt/netzwaechter/apps/frontend-web/dist/`

2. **API Requests** (`/api/*`)
   - Client → Nginx → Proxy → `localhost:3000` (Node.js/Express)

3. **WebSocket** (`/ws`)
   - Client → Nginx → Upgrade → `localhost:3000` (Node.js/Express)

4. **SPA Routing** (e.g., `/dashboard`, `/maps`)
   - Client → Nginx → `index.html` (React Router handles routing)

---

## Build Process

### Development Scripts

```json
{
  "dev": "pnpm run dev:backend & sleep 2 && pnpm run dev:frontend",
  "dev:frontend": "cd apps/frontend-web && vite",
  "dev:backend": "cd apps/backend-api && NODE_ENV=development tsx watch --env-file=../../.env index.ts"
}
```

### Production Build

**Command**: `pnpm run build`

**Process**:

1. **Turbo Build** - Build all packages
   ```bash
   turbo run build
   ```

2. **Frontend Build** - Vite production build
   ```bash
   vite build
   # Output: apps/frontend-web/dist/
   ```

3. **Backend Build** - esbuild bundle
   ```bash
   esbuild apps/backend-api/index.ts \
     --platform=node \
     --packages=external \
     --bundle \
     --format=esm \
     --outdir=dist
   # Output: dist/index.js (473KB)
   ```

### Build Outputs

- **Frontend**: `apps/frontend-web/dist/` (static HTML, CSS, JS)
- **Backend**: `dist/index.js` (single bundled file, ESM format)

### Individual Build Scripts

```json
{
  "build:packages": "turbo run build",
  "build:frontend": "vite build",
  "build:backend": "esbuild apps/backend-api/index.ts --platform=node --packages=external --bundle --format=esm --outdir=dist"
}
```

### Production Start

```bash
NODE_ENV=production node dist/index.js
```

---

## Environment Variables

### Location

**Production**: `/opt/netzwaechter/.env`

### Key Variables

```bash
# Node Environment
NODE_ENV=production
PORT=3000

# Database Connection
DATABASE_URL=postgresql://[user]:[pass]@23.88.40.91:50184/20251001_neu_neondb

# Session Configuration
SESSION_SECRET=[secret]

# Email Configuration (SendGrid)
SENDGRID_API_KEY=[key]
FROM_EMAIL=[email]

# File Upload (Google Cloud Storage)
GOOGLE_APPLICATION_CREDENTIALS=[path]
GCS_BUCKET_NAME=[bucket]

# Optional Features
SERVE_STATIC_FROM_BACKEND=false  # Nginx serves static files
```

### Environment Variable Loading

PM2 loads environment variables from `.env` file via `ecosystem.config.cjs`:

```javascript
const envConfig = {};
const envFile = readFileSync('/opt/netzwaechter/.env', 'utf8');
envFile.split('\n').forEach(line => {
  // Parse and load env vars
});
```

---

## Monitoring and Logging

### Application Logs

**PM2 Logs**:
- Location: `/opt/netzwaechter/logs/`
- Files: `pm2-out.log`, `pm2-error.log`
- Format: Timestamped with timezone

**Log Examples**:
```
2025-10-14 15:56:16 +00:00: 3:56:16 PM [express] GET /api/admin/database/status 200 in 8ms
2025-10-14 15:56:16 +00:00: ✅ [AUTH] Session valid, user authenticated
```

### Performance Metrics

**PM2 Metrics** (visible via `pm2 describe`):
- Used Heap Size: ~22-23 MB per instance
- Heap Usage: ~93-94%
- Event Loop Latency: 0.61-0.63 ms
- Event Loop Latency P95: 1.47-1.63 ms
- HTTP Requests: ~0.05 req/min (monitoring)
- HTTP Mean Latency: 42-42.5 ms
- HTTP P95 Latency: 56-60 ms

### Health Monitoring

**Health Check Endpoint**: `GET /health`

Returns:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-14T15:52:00.000Z",
  "uptime": 3600
}
```

### Database Status

**Admin Endpoint**: `GET /api/admin/database/status`

Returns:
```json
{
  "settingdbOnline": true,
  "settingdbStatus": "connected"
}
```

---

## Architecture Diagrams

### System Overview

```mermaid
graph TB
    subgraph Client["Client Browser"]
        A[Web Browser]
    end

    subgraph Server["Production Server 91.98.156.158"]
        B[Nginx :443/80]

        subgraph PM2["PM2 Cluster"]
            C1[Node.js Instance 0<br/>PID 27110]
            C2[Node.js Instance 1<br/>PID 27122]
        end

        D[Express Backend<br/>:3000]
        E[Frontend Static Files<br/>/opt/netzwaechter/apps/frontend-web/dist]
    end

    subgraph External["External Services"]
        F[PostgreSQL Database<br/>23.88.40.91:50184<br/>Neon]
        G[SendGrid<br/>Email Service]
        H[Google Cloud Storage<br/>File Uploads]
    end

    A -->|HTTPS| B
    B -->|Static Files| E
    B -->|/api/*| D
    B -->|/ws| D

    D --> C1
    D --> C2

    C1 --> F
    C2 --> F
    C1 --> G
    C2 --> G
    C1 --> H
    C2 --> H
```

### Request Flow

```mermaid
sequenceDiagram
    participant Client
    participant Nginx
    participant PM2
    participant Express
    participant Database

    Client->>Nginx: HTTPS Request

    alt Static Asset Request
        Nginx->>Nginx: Check /opt/netzwaechter/apps/frontend-web/dist/
        Nginx-->>Client: Return Static File
    else API Request (/api/*)
        Nginx->>PM2: Proxy to :3000
        PM2->>Express: Route to Handler
        Express->>Database: Query Data
        Database-->>Express: Return Results
        Express-->>PM2: JSON Response
        PM2-->>Nginx: Response
        Nginx-->>Client: JSON Response
    else SPA Route (/dashboard, /maps)
        Nginx->>Nginx: try_files → index.html
        Nginx-->>Client: Return index.html
        Client->>Client: React Router handles routing
    end
```

### Deployment Architecture

```mermaid
graph LR
    subgraph Development["Development"]
        A1[Local Dev<br/>tsx watch]
        A2[Vite Dev Server<br/>:5173]
    end

    subgraph Build["Build Process"]
        B1[turbo run build]
        B2[vite build<br/>Frontend]
        B3[esbuild<br/>Backend]
    end

    subgraph Production["Production Deploy"]
        C1[rsync to Server]
        C2[PM2 reload<br/>Zero Downtime]
        C3[Nginx serves<br/>static files]
    end

    A1 --> B1
    A2 --> B2
    B1 --> B2
    B1 --> B3
    B2 --> C1
    B3 --> C1
    C1 --> C2
    C1 --> C3
```

### Data Flow

```mermaid
graph TD
    subgraph Frontend["Frontend (React)"]
        A[Components]
        B[TanStack Query]
        C[API Client]
    end

    subgraph Backend["Backend (Express)"]
        D[API Routes]
        E[Middleware<br/>Auth, Rate Limit]
        F[Business Logic]
    end

    subgraph Data["Data Layer"]
        G[Drizzle ORM]
        H[PostgreSQL<br/>Neon]
    end

    subgraph External["External"]
        I[Agents<br/>Data Collection]
        J[Weather API<br/>DWD Bright Sky]
    end

    A --> B
    B --> C
    C -->|HTTP /api/*| D
    D --> E
    E --> F
    F --> G
    G --> H

    I --> D
    J --> I
```

---

## Summary

The Netzwächter application is a production-grade monitoring platform with:

- **High Availability**: PM2 cluster mode with 2 instances and auto-restart
- **Performance**: Efficient request handling (42ms mean latency)
- **Scalability**: Cluster mode with port reuse, PostgreSQL connection pooling
- **Security**: Nginx SSL/TLS, rate limiting, session-based auth
- **Monitoring**: Comprehensive logging, health checks, PM2 metrics
- **Modern Stack**: React 18, Node.js 20, TypeScript, Vite, Drizzle ORM

The architecture separates concerns cleanly:
- Nginx handles SSL, static files, and reverse proxy
- PM2 manages process lifecycle and clustering
- Express provides RESTful API and business logic
- React delivers modern, responsive UI
- PostgreSQL stores all application data

This setup provides a robust, maintainable, and scalable foundation for the Netzwächter monitoring platform.

---

## Additional Resources

- **Deployment Checklist**: See `.deployment/DEPLOYMENT_CHECKLIST.md`
- **SSH Setup**: See `.deployment/SSH_KEY_SETUP.md`
- **Hetzner Configuration**: See `.deployment/HETZNER_SETUP.md`
- **Quick Start Guide**: See `.deployment/QUICK_START.md`
