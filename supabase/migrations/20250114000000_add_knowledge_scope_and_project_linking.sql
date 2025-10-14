-- =====================================================
-- Knowledge Organization System - Phase 1: Database Schema
-- =====================================================
-- Migration: Add scope-based knowledge organization
-- Version: 0.2.0
-- Date: 2025-01-14
-- =====================================================

-- =====================================================
-- SECTION 1: ADD SCOPE COLUMNS TO ARCHON_SOURCES
-- =====================================================

-- Add knowledge scope column
ALTER TABLE archon_sources
ADD COLUMN IF NOT EXISTS knowledge_scope TEXT DEFAULT 'global'
CHECK (knowledge_scope IN ('global', 'project'));

-- Add project_id column for project-specific knowledge
ALTER TABLE archon_sources
ADD COLUMN IF NOT EXISTS project_id UUID REFERENCES archon_projects(id) ON DELETE CASCADE;

-- Add comments
COMMENT ON COLUMN archon_sources.knowledge_scope IS 'Scope of knowledge: global (shared across all work) or project (specific to a project)';
COMMENT ON COLUMN archon_sources.project_id IS 'Foreign key to archon_projects when knowledge_scope=project. NULL for global knowledge.';

-- =====================================================
-- SECTION 2: CREATE KNOWLEDGE TAGS TABLE
-- =====================================================

-- Create knowledge_tags table for tag definitions
CREATE TABLE IF NOT EXISTS archon_knowledge_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tag_name TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    usage_guidelines TEXT,
    color_hex TEXT,
    icon_name TEXT,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    -- Tag categories constraint
    CONSTRAINT chk_tag_category CHECK (category IN (
        'framework',
        'language',
        'architecture',
        'security',
        'testing',
        'deployment',
        'documentation',
        'database',
        'api',
        'ui',
        'general'
    ))
);

-- Create indexes for query performance
CREATE INDEX IF NOT EXISTS idx_knowledge_tags_category ON archon_knowledge_tags(category);
CREATE INDEX IF NOT EXISTS idx_knowledge_tags_name ON archon_knowledge_tags(tag_name);

-- Create trigger for updated_at
CREATE TRIGGER update_archon_knowledge_tags_updated_at
    BEFORE UPDATE ON archon_knowledge_tags
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Enable RLS
ALTER TABLE archon_knowledge_tags ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for public read access
CREATE POLICY "Allow public read access to archon_knowledge_tags"
    ON archon_knowledge_tags FOR SELECT TO public
    USING (true);

-- Add table comment
COMMENT ON TABLE archon_knowledge_tags IS 'Predefined tags for knowledge organization with descriptions and usage guidelines';

-- =====================================================
-- SECTION 3: CREATE PROJECT KNOWLEDGE FOLDERS TABLE
-- =====================================================

-- Create project knowledge folders for organization
CREATE TABLE IF NOT EXISTS archon_project_knowledge_folders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES archon_projects(id) ON DELETE CASCADE,
    folder_name TEXT NOT NULL,
    description TEXT,
    color_hex TEXT DEFAULT '#6366f1',
    icon_name TEXT DEFAULT 'folder',
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    -- Ensure unique folder names per project
    UNIQUE(project_id, folder_name)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_project_folders_project_id ON archon_project_knowledge_folders(project_id);
CREATE INDEX IF NOT EXISTS idx_project_folders_sort_order ON archon_project_knowledge_folders(project_id, sort_order);

-- Create trigger
CREATE TRIGGER update_archon_project_knowledge_folders_updated_at
    BEFORE UPDATE ON archon_project_knowledge_folders
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Enable RLS
ALTER TABLE archon_project_knowledge_folders ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for public read access
CREATE POLICY "Allow public read access to archon_project_knowledge_folders"
    ON archon_project_knowledge_folders FOR SELECT TO public
    USING (true);

-- Add table comment
COMMENT ON TABLE archon_project_knowledge_folders IS 'Organizational folders for project-specific knowledge sources (single-level, not nested)';
COMMENT ON COLUMN archon_project_knowledge_folders.folder_name IS 'Unique folder name within project';
COMMENT ON COLUMN archon_project_knowledge_folders.description IS 'Optional description of folder purpose';
COMMENT ON COLUMN archon_project_knowledge_folders.sort_order IS 'Display order within project (default: 0)';

-- =====================================================
-- SECTION 4: ADD FOLDER_ID TO ARCHON_SOURCES
-- =====================================================

-- Add folder_id column for project-scoped knowledge organization
ALTER TABLE archon_sources
ADD COLUMN IF NOT EXISTS folder_id UUID REFERENCES archon_project_knowledge_folders(id) ON DELETE SET NULL;

-- Create index for folder filtering
CREATE INDEX IF NOT EXISTS idx_sources_folder_id ON archon_sources(folder_id);

-- Add comment
COMMENT ON COLUMN archon_sources.folder_id IS 'Optional folder for organizing project-scoped knowledge. NULL for global or unfiled project knowledge.';

-- =====================================================
-- SECTION 5: ADD INDEXES FOR SCOPE FILTERING
-- =====================================================

-- Add index for scope filtering
CREATE INDEX IF NOT EXISTS idx_archon_sources_scope ON archon_sources(knowledge_scope);

-- Add composite index for project-scoped queries
CREATE INDEX IF NOT EXISTS idx_archon_sources_project_scope ON archon_sources(project_id, knowledge_scope)
WHERE project_id IS NOT NULL;

-- =====================================================
-- SECTION 6: ADD CONSTRAINTS
-- =====================================================

-- Constraint: scope='global' requires project_id IS NULL
-- Constraint: scope='project' requires project_id IS NOT NULL
ALTER TABLE archon_sources
ADD CONSTRAINT chk_project_scope
CHECK (
    (knowledge_scope = 'global' AND project_id IS NULL) OR
    (knowledge_scope = 'project' AND project_id IS NOT NULL)
);

-- Constraint: folder_id only allowed when scope='project'
ALTER TABLE archon_sources
ADD CONSTRAINT chk_folder_project_scope
CHECK (
    (knowledge_scope = 'global' AND folder_id IS NULL) OR
    (knowledge_scope = 'project')
);

-- =====================================================
-- SECTION 7: SEED STANDARD TAGS
-- =====================================================

-- Insert standard tag definitions (40+ tags across 11 categories)
INSERT INTO archon_knowledge_tags (tag_name, category, description, usage_guidelines, color_hex) VALUES
-- Framework Tags (5)
('react', 'framework', 'React framework for building user interfaces', 'Use for React-specific documentation, component patterns, hooks usage', '#61dafb'),
('nextjs', 'framework', 'Next.js React framework', 'Use for Next.js routing, SSR, API routes', '#000000'),
('fastapi', 'framework', 'FastAPI Python web framework', 'Use for FastAPI endpoints, dependency injection, Pydantic models', '#009688'),
('django', 'framework', 'Django Python web framework', 'Use for Django models, views, ORM', '#092e20'),
('express', 'framework', 'Express.js Node framework', 'Use for Express routing, middleware', '#000000'),

-- Language Tags (5)
('python', 'language', 'Python programming language', 'Use for Python code, syntax, standard library', '#3776ab'),
('typescript', 'language', 'TypeScript programming language', 'Use for TypeScript code, types, interfaces', '#3178c6'),
('javascript', 'language', 'JavaScript programming language', 'Use for vanilla JS, ES6+ features', '#f7df1e'),
('rust', 'language', 'Rust programming language', 'Use for Rust code, ownership patterns', '#ce412b'),
('go', 'language', 'Go programming language', 'Use for Go code, concurrency patterns', '#00add8'),

-- Architecture Tags (5)
('microservices', 'architecture', 'Microservices architecture pattern', 'Use for service design, inter-service communication', '#4caf50'),
('rest-api', 'architecture', 'REST API design and implementation', 'Use for RESTful endpoint design, HTTP methods', '#ff9800'),
('graphql', 'architecture', 'GraphQL API design', 'Use for GraphQL schemas, resolvers, queries', '#e535ab'),
('event-driven', 'architecture', 'Event-driven architecture', 'Use for event sourcing, message queues, pub/sub', '#2196f3'),
('monolith', 'architecture', 'Monolithic architecture', 'Use for single-codebase applications', '#9e9e9e'),

-- Security Tags (4)
('authentication', 'security', 'Authentication mechanisms', 'Use for login systems, OAuth, JWT, session management', '#f44336'),
('authorization', 'security', 'Authorization and access control', 'Use for permissions, RBAC, policies', '#e91e63'),
('encryption', 'security', 'Data encryption', 'Use for TLS, data-at-rest encryption, hashing', '#9c27b0'),
('security-best-practices', 'security', 'General security best practices', 'Use for OWASP guidelines, secure coding', '#673ab7'),

-- Testing Tags (3)
('unit-testing', 'testing', 'Unit testing practices', 'Use for test frameworks, mocking, assertions', '#8bc34a'),
('integration-testing', 'testing', 'Integration testing', 'Use for API tests, database integration', '#4caf50'),
('e2e-testing', 'testing', 'End-to-end testing', 'Use for Playwright, Cypress, full user flows', '#009688'),

-- Deployment Tags (3)
('docker', 'deployment', 'Docker containerization', 'Use for Dockerfile, docker-compose, container best practices', '#2496ed'),
('kubernetes', 'deployment', 'Kubernetes orchestration', 'Use for K8s manifests, deployments, services', '#326ce5'),
('ci-cd', 'deployment', 'CI/CD pipelines', 'Use for GitHub Actions, GitLab CI, automated deployments', '#2088ff'),

-- Database Tags (4)
('postgresql', 'database', 'PostgreSQL database', 'Use for Postgres-specific features, queries, indexes', '#336791'),
('mongodb', 'database', 'MongoDB NoSQL database', 'Use for document models, aggregation pipelines', '#47a248'),
('redis', 'database', 'Redis in-memory data store', 'Use for caching, pub/sub, data structures', '#dc382d'),
('vector-search', 'database', 'Vector similarity search', 'Use for embeddings, pgvector, semantic search', '#6366f1'),

-- API Tags (2)
('openapi', 'api', 'OpenAPI/Swagger specification', 'Use for API documentation, schema definitions', '#85ea2d'),
('websockets', 'api', 'WebSocket real-time communication', 'Use for bidirectional communication, Socket.IO', '#010101'),

-- UI Tags (3)
('tailwind', 'ui', 'Tailwind CSS framework', 'Use for utility-first CSS, responsive design', '#06b6d4'),
('radix-ui', 'ui', 'Radix UI primitives', 'Use for accessible components, headless UI', '#8b5cf6'),
('design-system', 'ui', 'Design system and components', 'Use for UI patterns, component libraries', '#f59e0b'),

-- Documentation Tags (4)
('api-reference', 'documentation', 'API reference documentation', 'Use for endpoint docs, request/response formats', '#3b82f6'),
('tutorial', 'documentation', 'Tutorial and how-to guides', 'Use for step-by-step instructions, learning paths', '#10b981'),
('architecture-docs', 'documentation', 'Architecture documentation', 'Use for system design docs, diagrams, ADRs', '#8b5cf6'),
('troubleshooting', 'documentation', 'Troubleshooting and debugging', 'Use for error resolution, common issues', '#ef4444'),

-- General Tags (2)
('best-practices', 'general', 'Best practices and patterns', 'Use for general coding standards, patterns, conventions', '#3b82f6'),
('getting-started', 'general', 'Getting started guides', 'Use for onboarding, setup instructions, quick starts', '#10b981')

ON CONFLICT (tag_name) DO NOTHING;

-- =====================================================
-- SECTION 8: UPDATE EXISTING DATA
-- =====================================================

-- Set all existing sources to global scope (backward compatibility)
UPDATE archon_sources
SET knowledge_scope = 'global'
WHERE knowledge_scope IS NULL;

-- Update metadata to include scope for backward compatibility
UPDATE archon_sources
SET metadata = jsonb_set(
    COALESCE(metadata, '{}'::jsonb),
    '{knowledge_scope}',
    to_jsonb(knowledge_scope)
)
WHERE NOT (metadata ? 'knowledge_scope');

-- =====================================================
-- SECTION 9: MIGRATION TRACKING
-- =====================================================

-- Record this migration as applied
INSERT INTO archon_migrations (version, migration_name)
VALUES ('0.2.0', '012_add_knowledge_scope_and_project_linking')
ON CONFLICT (version, migration_name) DO NOTHING;

-- =====================================================
-- MIGRATION COMPLETE
-- =====================================================
-- Knowledge organization system Phase 1 schema is now in place!
--
-- Schema Changes:
-- - archon_sources: Added knowledge_scope, project_id, folder_id
-- - archon_knowledge_tags: New table with 42 predefined tags
-- - archon_project_knowledge_folders: New table for project folders
-- - Indexes added for efficient scope-based queries
-- - Constraints ensure data integrity
--
-- Next Steps:
-- - Phase 2: Backend services and API endpoints
-- - Phase 3: MCP tool updates for scope-aware search
-- - Phase 4: Frontend UI with tab-based navigation
-- =====================================================
