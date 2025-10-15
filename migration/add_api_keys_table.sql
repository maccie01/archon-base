-- API Keys Table Migration
-- Created: 2025-10-15
-- Purpose: Add API key authentication for securing Archon knowledge base and sensitive endpoints

-- Create API keys table
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key_name TEXT NOT NULL,
    key_hash TEXT NOT NULL UNIQUE,
    key_prefix TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_used_at TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    permissions JSONB DEFAULT '{"read": true, "write": true, "admin": false}'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT key_name_not_empty CHECK (length(key_name) > 0),
    CONSTRAINT key_hash_not_empty CHECK (length(key_hash) > 0),
    CONSTRAINT key_prefix_format CHECK (key_prefix ~ '^ak_[a-zA-Z0-9]{4}$')
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_api_keys_key_hash ON api_keys(key_hash);
CREATE INDEX IF NOT EXISTS idx_api_keys_is_active ON api_keys(is_active);
CREATE INDEX IF NOT EXISTS idx_api_keys_key_prefix ON api_keys(key_prefix);
CREATE INDEX IF NOT EXISTS idx_api_keys_created_at ON api_keys(created_at DESC);

-- Add comments for documentation
COMMENT ON TABLE api_keys IS 'API keys for authenticating requests to Archon';
COMMENT ON COLUMN api_keys.id IS 'Unique identifier for the API key';
COMMENT ON COLUMN api_keys.key_name IS 'Human-readable name for the API key';
COMMENT ON COLUMN api_keys.key_hash IS 'Bcrypt hash of the API key (never store plain text)';
COMMENT ON COLUMN api_keys.key_prefix IS 'First 8 characters of the key for identification (format: ak_XXXX)';
COMMENT ON COLUMN api_keys.created_at IS 'Timestamp when the key was created';
COMMENT ON COLUMN api_keys.last_used_at IS 'Timestamp when the key was last used';
COMMENT ON COLUMN api_keys.is_active IS 'Whether the key is active and can be used';
COMMENT ON COLUMN api_keys.permissions IS 'JSON object defining permissions: read, write, admin';
COMMENT ON COLUMN api_keys.metadata IS 'Additional metadata for the key (creator, purpose, etc.)';

-- Grant necessary permissions (adjust based on your Supabase setup)
-- Note: You may need to adjust these grants based on your specific Supabase roles
GRANT SELECT, INSERT, UPDATE ON api_keys TO service_role;
GRANT SELECT ON api_keys TO authenticated;
