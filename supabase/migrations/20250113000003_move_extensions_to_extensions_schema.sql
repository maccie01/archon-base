-- Move vector and pg_trgm extensions from public to extensions schema
-- This addresses security warnings about extensions in the public schema

-- Move vector extension
ALTER EXTENSION vector SET SCHEMA extensions;

-- Move pg_trgm extension
ALTER EXTENSION pg_trgm SET SCHEMA extensions;

-- Add comment explaining the change
COMMENT ON SCHEMA extensions IS 'Schema for database extensions. Extensions here are accessible via search_path configuration.';

-- Note: All existing functions, indexes, and tables using these extensions will continue to work
-- because the search_path is configured to include both 'public' and 'extensions' schemas
-- (see config.toml: extra_search_path = ["public", "extensions"])
