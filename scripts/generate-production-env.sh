#!/bin/bash

# ==============================================================================
# Generate Production Environment File with Secure Secrets
# ==============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Archon Production Environment Generator${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if .env already exists on server
if [ -f "/opt/archon/.env" ]; then
    echo -e "${YELLOW}Existing .env found. Reading current values...${NC}"

    # Source existing env to preserve values
    set -a
    source /opt/archon/.env
    set +a

    echo -e "${GREEN}✓${NC} Loaded existing environment variables"
    echo ""
fi

# Function to generate random string
generate_secret() {
    local length=${1:-32}
    openssl rand -base64 $length | tr -d "=+/" | cut -c1-$length
}

# Function to generate JWT secret (needs to be at least 32 characters)
generate_jwt_secret() {
    openssl rand -base64 48 | tr -d "=+/" | cut -c1-48
}

# Function to generate JWT token for Supabase
generate_jwt_token() {
    local role=$1
    local secret=$2

    # Header
    header='{"alg":"HS256","typ":"JWT"}'

    # Payload
    payload="{\"iss\":\"supabase-demo\",\"role\":\"$role\",\"exp\":1983812996}"

    # Base64 encode
    header_b64=$(echo -n "$header" | openssl base64 -e -A | sed 's/+/-/g; s/\//_/g; s/=//g')
    payload_b64=$(echo -n "$payload" | openssl base64 -e -A | sed 's/+/-/g; s/\//_/g; s/=//g')

    # Create signature
    signature=$(echo -n "${header_b64}.${payload_b64}" | openssl dgst -sha256 -hmac "$secret" -binary | openssl base64 -e -A | sed 's/+/-/g; s/\//_/g; s/=//g')

    # Return JWT
    echo "${header_b64}.${payload_b64}.${signature}"
}

echo -e "${BLUE}Generating secure secrets...${NC}"
echo ""

# Generate or preserve secrets
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-$(generate_secret 32)}
JWT_SECRET=${JWT_SECRET:-$(generate_jwt_secret)}
ARCHON_BOOTSTRAP_SECRET=${ARCHON_BOOTSTRAP_SECRET:-$(generate_secret 32)}

echo -e "${GREEN}✓${NC} PostgreSQL password: ${POSTGRES_PASSWORD:0:8}..."
echo -e "${GREEN}✓${NC} JWT secret: ${JWT_SECRET:0:12}..."
echo -e "${GREEN}✓${NC} Bootstrap secret: ${ARCHON_BOOTSTRAP_SECRET:0:8}..."
echo ""

# Generate JWT tokens using the JWT secret
echo -e "${BLUE}Generating JWT tokens for Supabase...${NC}"
SUPABASE_ANON_KEY=$(generate_jwt_token "anon" "$JWT_SECRET")
SUPABASE_SERVICE_KEY=$(generate_jwt_token "service_role" "$JWT_SECRET")

echo -e "${GREEN}✓${NC} Anon key generated"
echo -e "${GREEN}✓${NC} Service role key generated"
echo ""

# Preserve or set other values
POSTGRES_USER=${POSTGRES_USER:-postgres}
POSTGRES_DB=${POSTGRES_DB:-postgres}
OPENAI_API_KEY=${OPENAI_API_KEY:-}
ARCHON_SERVER_PORT=${ARCHON_SERVER_PORT:-8181}
ARCHON_MCP_PORT=${ARCHON_MCP_PORT:-8051}
ARCHON_UI_PORT=${ARCHON_UI_PORT:-3737}
ARCHON_AGENTS_PORT=${ARCHON_AGENTS_PORT:-8052}
AGENTS_ENABLED=${AGENTS_ENABLED:-false}
LOG_LEVEL=${LOG_LEVEL:-INFO}
HOST=${HOST:-archon.nexorithm.io}
VITE_ALLOWED_HOSTS=${VITE_ALLOWED_HOSTS:-archon.nexorithm.io,supabase.archon.nexorithm.io,91.98.156.158,localhost,127.0.0.1}

# Create .env.production file
ENV_FILE="/opt/archon/.env.production"

echo -e "${BLUE}Creating ${ENV_FILE}...${NC}"

cat > "$ENV_FILE" << EOF
# ==============================================================================
# ARCHON PRODUCTION ENVIRONMENT
# Generated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
# ==============================================================================

# ------------------------------------------------------------------------------
# PostgreSQL Configuration
# ------------------------------------------------------------------------------
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_DB=${POSTGRES_DB}

# ------------------------------------------------------------------------------
# Supabase JWT (for PostgREST)
# IMPORTANT: JWT_SECRET must be at least 32 characters
# ------------------------------------------------------------------------------
JWT_SECRET=${JWT_SECRET}
JWT_EXP=3600

# ------------------------------------------------------------------------------
# Supabase API Keys (Generated JWT tokens)
# These are used by Kong to authenticate requests to PostgREST
# ------------------------------------------------------------------------------
SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}

# ------------------------------------------------------------------------------
# OpenAI API Key
# ------------------------------------------------------------------------------
OPENAI_API_KEY=${OPENAI_API_KEY}

# ------------------------------------------------------------------------------
# Archon Service Ports (all bound to 127.0.0.1)
# ------------------------------------------------------------------------------
ARCHON_SERVER_PORT=${ARCHON_SERVER_PORT}
ARCHON_MCP_PORT=${ARCHON_MCP_PORT}
ARCHON_UI_PORT=${ARCHON_UI_PORT}
ARCHON_AGENTS_PORT=${ARCHON_AGENTS_PORT}

# ------------------------------------------------------------------------------
# Features
# ------------------------------------------------------------------------------
AGENTS_ENABLED=${AGENTS_ENABLED}
PROD=true

# ------------------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------------------
LOG_LEVEL=${LOG_LEVEL}
LOGFIRE_TOKEN=

# ------------------------------------------------------------------------------
# Security
# ARCHON_BOOTSTRAP_SECRET: Used for initial API key creation via /api/auth/bootstrap
# ------------------------------------------------------------------------------
ARCHON_BOOTSTRAP_SECRET=${ARCHON_BOOTSTRAP_SECRET}

# ------------------------------------------------------------------------------
# Hosts and Domains
# ------------------------------------------------------------------------------
HOST=${HOST}
VITE_ALLOWED_HOSTS=${VITE_ALLOWED_HOSTS}
VITE_SHOW_DEVTOOLS=false

# ==============================================================================
# NOTES:
# - All services bind to 127.0.0.1 (localhost only)
# - External access only through Nginx reverse proxy
# - Archon uses custom API key authentication (not Supabase Auth)
# - JWT tokens are only used for PostgREST authorization
# ==============================================================================
EOF

echo -e "${GREEN}✓${NC} Environment file created: ${ENV_FILE}"
echo ""

# Display important values
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}IMPORTANT SECRETS (Save Securely!)${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}PostgreSQL Database:${NC}"
echo "  User: ${POSTGRES_USER}"
echo "  Password: ${POSTGRES_PASSWORD}"
echo "  Database: ${POSTGRES_DB}"
echo ""
echo -e "${YELLOW}Supabase JWT Secret:${NC}"
echo "  ${JWT_SECRET}"
echo ""
echo -e "${YELLOW}Supabase API Keys:${NC}"
echo "  Anon Key: ${SUPABASE_ANON_KEY:0:50}..."
echo "  Service Key: ${SUPABASE_SERVICE_KEY:0:50}..."
echo ""
echo -e "${YELLOW}Archon Bootstrap Secret:${NC}"
echo "  ${ARCHON_BOOTSTRAP_SECRET}"
echo ""
echo -e "${YELLOW}OpenAI API Key:${NC}"
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "  ${RED}NOT SET${NC} - Add to .env.production after generation"
else
    echo "  ${OPENAI_API_KEY:0:20}..."
fi
echo ""

# Create backup of old .env if it exists
if [ -f "/opt/archon/.env" ] && [ "$ENV_FILE" != "/opt/archon/.env" ]; then
    backup_file="/opt/archon/.env.backup.$(date +%Y%m%d_%H%M%S)"
    cp /opt/archon/.env "$backup_file"
    echo -e "${GREEN}✓${NC} Backup of old .env created: ${backup_file}"
    echo ""
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Next Steps:${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "1. Review the generated .env.production file"
echo "2. Add your OpenAI API key if not already set"
echo "3. Copy to .env: cp /opt/archon/.env.production /opt/archon/.env"
echo "4. Proceed with migration: /opt/archon/scripts/migrate-to-consolidated.sh"
echo ""
