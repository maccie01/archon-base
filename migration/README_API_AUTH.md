# API Key Authentication System

This document provides instructions for implementing and using the API key authentication system for Archon.

Created: 2025-10-15

## Overview

Archon now uses API key authentication to secure the knowledge base and all sensitive endpoints. This protects your sensitive business data from unauthorized access.

## Setup Instructions

### Step 1: Run Database Migration

First, you need to create the API keys table in your Supabase database:

1. Open Supabase Dashboard
2. Navigate to SQL Editor
3. Run the migration file: `/Users/janschubert/tools/archon/migration/add_api_keys_table.sql`

```sql
-- Copy and paste the contents of add_api_keys_table.sql into the SQL Editor
```

### Step 2: Configure Environment Variables

Add these environment variables to your `.env` file:

```bash
# Authentication Configuration
AUTH_ENABLED=true
ALLOWED_ORIGINS=https://archon.nexorithm.io,http://localhost:3737

# Bootstrap Secret (generate a random secure string)
# This is used ONLY for creating the first API key
ARCHON_BOOTSTRAP_SECRET=your-secure-random-secret-here
```

To generate a secure bootstrap secret:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 3: Create Your First API Key

After setting up the migration and environment variables, you can create your first API key using the bootstrap endpoint:

```bash
curl -X POST http://localhost:8181/api/auth/bootstrap \
  -H "Content-Type: application/json" \
  -d '{
    "bootstrap_secret": "your-secure-random-secret-here",
    "key_name": "Production Admin Key"
  }'
```

**IMPORTANT:** The API key will be displayed only once. Store it securely!

Example response:
```json
{
  "success": true,
  "message": "Initial API key created successfully. Store this key securely!",
  "api_key": "ak_A1B2_LONG_RANDOM_STRING_HERE",
  "key_name": "Production Admin Key",
  "key_id": "uuid-here",
  "warning": "This is the only time you will see this API key. Store it securely!"
}
```

### Step 4: Use the API Key

Include the API key in all requests using the Authorization header:

```bash
curl -H "Authorization: Bearer ak_A1B2_LONG_RANDOM_STRING_HERE" \
  http://localhost:8181/api/knowledge-items
```

## API Endpoints

### Authentication Status
```bash
GET /api/auth/status
```
Check if authentication is configured and bootstrap is available.

### Bootstrap (First Time Only)
```bash
POST /api/auth/bootstrap
```
Create the initial API key. Only works when no API keys exist.

### List API Keys
```bash
GET /api/auth/keys
Authorization: Bearer <api_key>
```
List all API keys (requires authentication).

### Create New API Key
```bash
POST /api/auth/keys
Authorization: Bearer <api_key>
Content-Type: application/json

{
  "name": "Development Key",
  "permissions": {
    "read": true,
    "write": true,
    "admin": false
  }
}
```
Create a new API key (requires admin permissions).

### Revoke API Key
```bash
DELETE /api/auth/keys/{key_id}
Authorization: Bearer <api_key>
```
Revoke an API key (requires admin permissions).

### Validate Current Key
```bash
POST /api/auth/validate
Authorization: Bearer <api_key>
```
Validate your current API key and get information about it.

## Protected Endpoints

The following endpoints now require authentication:

### Knowledge Management
- `POST /api/knowledge-items/crawl` - Crawl URLs
- `POST /api/documents/upload` - Upload documents
- `PUT /api/knowledge-items/{source_id}` - Update knowledge items
- `DELETE /api/knowledge-items/{source_id}` - Delete knowledge items
- `POST /api/knowledge-items/{source_id}/refresh` - Refresh knowledge items
- `DELETE /api/sources/{source_id}` - Delete sources
- `POST /api/knowledge-items/stop/{progress_id}` - Stop crawl tasks

### Settings & Credentials
- `POST /api/credentials` - Create credentials
- `PUT /api/credentials/{key}` - Update credentials
- `DELETE /api/credentials/{key}` - Delete credentials

### Projects (Write Operations)
- `POST /api/projects` - Create projects
- `PUT /api/projects/{id}` - Update projects
- `DELETE /api/projects/{id}` - Delete projects
- `POST /api/tasks` - Create tasks
- `PUT /api/tasks/{id}` - Update tasks
- `DELETE /api/tasks/{id}` - Delete tasks

## Exempt Endpoints

These endpoints do NOT require authentication:

- `/` - Root endpoint
- `/health` - Health check
- `/api/health` - API health check
- `/api/auth/bootstrap` - Bootstrap endpoint (for first key)
- `/api/auth/status` - Auth status check
- `/internal/*` - Internal API (uses IP-based auth)

## Security Best Practices

1. **Store API keys securely**: Never commit API keys to version control
2. **Use environment variables**: Store keys in `.env` or secure vault
3. **Rotate keys regularly**: Create new keys and revoke old ones periodically
4. **Use different keys for different environments**: Separate keys for dev, staging, prod
5. **Monitor key usage**: Check `last_used_at` timestamps in the API keys table
6. **Revoke compromised keys immediately**: Use the DELETE endpoint

## Permissions

API keys support three permission levels:

- `read`: Can read data (default: true)
- `write`: Can create/update/delete data (default: true)
- `admin`: Can manage API keys and admin functions (default: false for new keys)

The bootstrap key created via `/api/auth/bootstrap` gets admin permissions automatically.

## Troubleshooting

### 401 Unauthorized
- Check that you're including the Authorization header
- Verify the API key is correct (no extra spaces)
- Confirm the key hasn't been revoked (check `is_active` in database)

### 403 Forbidden
- Check that your API key has the required permissions
- Admin operations require `admin: true` in permissions

### Bootstrap endpoint returns 403
- API keys already exist in the database
- Use the regular API key management endpoints instead

## Disabling Authentication (Development Only)

To temporarily disable authentication for local development:

```bash
AUTH_ENABLED=false
```

**WARNING:** This is NOT recommended for production environments!

## Migration from Non-Authenticated Setup

If you're migrating from a version without authentication:

1. Run the database migration
2. Set `AUTH_ENABLED=false` temporarily
3. Create your first API key via bootstrap
4. Update your frontend/client code to include the API key
5. Set `AUTH_ENABLED=true`
6. Test all integrations

## Support

For issues or questions:
1. Check the Archon logs for authentication errors
2. Verify database migration ran successfully
3. Check environment variables are set correctly
4. Ensure bcrypt is installed: `pip install bcrypt`
