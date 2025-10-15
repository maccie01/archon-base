# API Authentication Testing Guide

This document provides curl commands to test the API key authentication system.

Created: 2025-10-15

## Prerequisites

1. Database migration applied (add_api_keys_table.sql)
2. Environment variables set (AUTH_ENABLED=true, ARCHON_BOOTSTRAP_SECRET)
3. Archon server running

## Test 1: Check Authentication Status

```bash
curl http://localhost:8181/api/auth/status
```

Expected response:
```json
{
  "authentication_enabled": true,
  "has_api_keys": false,
  "bootstrap_available": true,
  "message": "Bootstrap endpoint available"
}
```

## Test 2: Create First API Key (Bootstrap)

Replace `YOUR_BOOTSTRAP_SECRET` with the value from your .env file:

```bash
curl -X POST http://localhost:8181/api/auth/bootstrap \
  -H "Content-Type: application/json" \
  -d '{
    "bootstrap_secret": "YOUR_BOOTSTRAP_SECRET",
    "key_name": "Test Admin Key"
  }'
```

Expected response:
```json
{
  "success": true,
  "message": "Initial API key created successfully...",
  "api_key": "ak_XXXX_LONG_RANDOM_STRING",
  "key_name": "Test Admin Key",
  "key_id": "uuid-here",
  "warning": "This is the only time you will see this API key..."
}
```

**IMPORTANT**: Save the `api_key` value! You'll need it for the next tests.

## Test 3: Validate API Key

Replace `YOUR_API_KEY` with the key from Test 2:

```bash
curl -X POST http://localhost:8181/api/auth/validate \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Expected response:
```json
{
  "success": true,
  "valid": true,
  "key_id": "uuid-here",
  "key_name": "Test Admin Key",
  "permissions": {
    "read": true,
    "write": true,
    "admin": true
  }
}
```

## Test 4: Access Protected Endpoint WITHOUT Authentication

```bash
curl http://localhost:8181/api/knowledge-items
```

Expected response (401 Unauthorized):
```json
{
  "error": "Authentication required",
  "message": "Missing Authorization header...",
  "error_type": "missing_auth_header"
}
```

## Test 5: Access Protected Endpoint WITH Authentication

```bash
curl http://localhost:8181/api/knowledge-items \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Expected response: List of knowledge items (200 OK)

## Test 6: Access Health Check (Exempt)

Health checks should work without authentication:

```bash
curl http://localhost:8181/health
```

Expected response (200 OK):
```json
{
  "status": "healthy",
  "service": "archon-backend",
  ...
}
```

## Test 7: List API Keys

```bash
curl http://localhost:8181/api/auth/keys \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Expected response:
```json
{
  "success": true,
  "keys": [
    {
      "id": "uuid",
      "key_name": "Test Admin Key",
      "key_prefix": "ak_XXXX",
      "created_at": "...",
      "last_used_at": "...",
      "is_active": true,
      "permissions": {...}
    }
  ],
  "total": 1
}
```

## Test 8: Create Additional API Key

```bash
curl -X POST http://localhost:8181/api/auth/keys \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Development Key",
    "permissions": {
      "read": true,
      "write": true,
      "admin": false
    }
  }'
```

Expected response:
```json
{
  "success": true,
  "api_key": "ak_YYYY_ANOTHER_RANDOM_STRING",
  "key_name": "Development Key",
  ...
}
```

## Test 9: Attempt Bootstrap Again (Should Fail)

```bash
curl -X POST http://localhost:8181/api/auth/bootstrap \
  -H "Content-Type: application/json" \
  -d '{
    "bootstrap_secret": "YOUR_BOOTSTRAP_SECRET",
    "key_name": "Another Key"
  }'
```

Expected response (403 Forbidden):
```json
{
  "error": "Bootstrap not available",
  "message": "API keys already exist. Use the API key management endpoints.",
  "error_type": "bootstrap_already_complete"
}
```

## Test 10: Invalid API Key

```bash
curl http://localhost:8181/api/knowledge-items \
  -H "Authorization: Bearer invalid_key_12345"
```

Expected response (401 Unauthorized):
```json
{
  "error": "Invalid API key",
  "message": "The provided API key is invalid or has been revoked",
  "error_type": "invalid_api_key"
}
```

## Test 11: Revoke API Key

Get a key_id from Test 7, then:

```bash
curl -X DELETE http://localhost:8181/api/auth/keys/KEY_ID_HERE \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Expected response:
```json
{
  "success": true,
  "message": "API key revoked successfully",
  "key_id": "uuid-here"
}
```

## Test 12: Test Revoked Key

Try using the revoked key:

```bash
curl http://localhost:8181/api/knowledge-items \
  -H "Authorization: Bearer REVOKED_KEY"
```

Expected response (401 Unauthorized):
```json
{
  "error": "Invalid API key",
  "message": "The provided API key is invalid or has been revoked",
  "error_type": "invalid_api_key"
}
```

## Test 13: CORS Headers

```bash
curl -X OPTIONS http://localhost:8181/api/knowledge-items \
  -H "Origin: https://archon.nexorithm.io" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: Authorization" \
  -v
```

Check for CORS headers in the response.

## Test 14: Update Knowledge Item (Protected Write Operation)

```bash
curl -X PUT http://localhost:8181/api/knowledge-items/SOURCE_ID \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tags": ["updated", "test"]}'
```

Expected response: Updated knowledge item details

## Troubleshooting

### 401 Unauthorized
- Verify API key is correct (copy/paste carefully)
- Check for extra spaces in the Authorization header
- Confirm key is active in database: `SELECT * FROM api_keys WHERE is_active = true;`

### 403 Forbidden
- Check if endpoint requires admin permissions
- Verify your key has admin: true in permissions
- Use an admin key for admin operations

### 500 Internal Server Error
- Check server logs for details
- Verify database migration ran successfully
- Ensure bcrypt is installed: `pip list | grep bcrypt`

### Connection Refused
- Ensure Archon server is running
- Check ARCHON_SERVER_PORT in .env
- Verify firewall settings

## Performance Testing

Test API key validation performance:

```bash
time for i in {1..100}; do
  curl -s http://localhost:8181/api/auth/validate \
    -H "Authorization: Bearer YOUR_API_KEY" > /dev/null
done
```

This should complete in a reasonable time (bcrypt verification is intentionally slow for security).

## Security Testing

### Test 1: SQL Injection Attempt
```bash
curl http://localhost:8181/api/auth/validate \
  -H "Authorization: Bearer ak_TEST'; DROP TABLE api_keys; --"
```
Should return 401, not cause any database damage.

### Test 2: XSS Attempt in Key Name
```bash
curl -X POST http://localhost:8181/api/auth/keys \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "<script>alert(\"xss\")</script>",
    "permissions": {"read": true, "write": false, "admin": false}
  }'
```
Should store safely without executing script.

### Test 3: Brute Force Protection
Run multiple invalid authentication attempts quickly and monitor server behavior.

## Cleanup

To remove test API keys:

```bash
# List all keys
curl http://localhost:8181/api/auth/keys \
  -H "Authorization: Bearer YOUR_API_KEY"

# Revoke specific key
curl -X DELETE http://localhost:8181/api/auth/keys/KEY_ID \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Or directly in database:
```sql
UPDATE api_keys SET is_active = false WHERE key_name LIKE '%Test%';
```
