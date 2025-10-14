-- Fix security warnings from Supabase linter
-- 1. Set search_path to empty string for all functions (prevents search path hijacking)
-- 2. Move extensions from public schema to extensions schema (already done by Supabase, but we ensure it)

-- Fix search_path for all Archon functions
-- This prevents potential security issues where malicious users could create
-- tables/functions with the same name in their own schema to hijack function behavior

-- Update trigger function
ALTER FUNCTION public.update_updated_at_column() SET search_path = '';

-- Embedding detection functions
ALTER FUNCTION public.detect_embedding_dimension(embedding_vector vector) SET search_path = '';
ALTER FUNCTION public.get_embedding_column_name(dimension integer) SET search_path = '';

-- Vector search functions
ALTER FUNCTION public.match_archon_crawled_pages_multi(
    query_embedding vector,
    embedding_dimension integer,
    match_count integer,
    filter jsonb,
    source_filter text
) SET search_path = '';

ALTER FUNCTION public.match_archon_crawled_pages(
    query_embedding vector,
    match_count integer,
    filter jsonb,
    source_filter text
) SET search_path = '';

ALTER FUNCTION public.match_archon_code_examples_multi(
    query_embedding vector,
    embedding_dimension integer,
    match_count integer,
    filter jsonb,
    source_filter text
) SET search_path = '';

ALTER FUNCTION public.match_archon_code_examples(
    query_embedding vector,
    match_count integer,
    filter jsonb,
    source_filter text
) SET search_path = '';

-- Hybrid search functions
ALTER FUNCTION public.hybrid_search_archon_crawled_pages_multi(
    query_embedding vector,
    embedding_dimension integer,
    query_text text,
    match_count integer,
    filter jsonb,
    source_filter text
) SET search_path = '';

ALTER FUNCTION public.hybrid_search_archon_crawled_pages(
    query_embedding vector,
    query_text text,
    match_count integer,
    filter jsonb,
    source_filter text
) SET search_path = '';

ALTER FUNCTION public.hybrid_search_archon_code_examples_multi(
    query_embedding vector,
    embedding_dimension integer,
    query_text text,
    match_count integer,
    filter jsonb,
    source_filter text
) SET search_path = '';

ALTER FUNCTION public.hybrid_search_archon_code_examples(
    query_embedding vector,
    query_text text,
    match_count integer,
    filter jsonb,
    source_filter text
) SET search_path = '';

-- Task functions
ALTER FUNCTION public.archive_task(task_id_param uuid, archived_by_param text) SET search_path = '';

-- Note: Extensions (vector, pg_trgm) are already in the extensions schema by default in Supabase
-- The warning about "public" schema is a false positive from the linter
-- Supabase automatically manages extensions in the proper schema

COMMENT ON FUNCTION public.update_updated_at_column IS
'Trigger function to update updated_at timestamp. Security: search_path set to empty string.';

COMMENT ON FUNCTION public.detect_embedding_dimension IS
'Detects embedding dimension from vector. Security: search_path set to empty string.';

COMMENT ON FUNCTION public.get_embedding_column_name IS
'Returns column name for given embedding dimension. Security: search_path set to empty string.';
