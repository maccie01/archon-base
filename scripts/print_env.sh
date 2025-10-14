#!/usr/bin/env bash
set -euo pipefail

# Prints required .env values for Archon based on local Supabase CLI status
# Does not write files; only prints lines to copy into .env

if ! command -v node >/dev/null 2>&1 || ! command -v npx >/dev/null 2>&1; then
  echo "Node.js/npx nicht gefunden. Bitte Node.js 18+ installieren." >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "jq ist nicht installiert. Bitte zuerst scripts/setup.sh ausführen." >&2
  exit 1
fi

SUPA_JSON=$(npx -y supabase@latest status --json 2>/dev/null || echo '{}')
URL=$(echo "$SUPA_JSON" | jq -r '.apiUrl // empty')
SERVICE_KEY=$(echo "$SUPA_JSON" | jq -r '.serviceRoleKey // empty')

echo "LLM_PROVIDER=ollama"
echo "LLM_BASE_URL=http://host.docker.internal:11434/v1"
echo "MODEL_CHOICE=qwen2.5-coder:7b"
echo "EMBEDDING_MODEL=nomic-embed-text"
echo "SUPABASE_URL=$URL"
echo "SUPABASE_SERVICE_KEY=$SERVICE_KEY"

if [[ -z "$URL" || -z "$SERVICE_KEY" ]]; then
  echo "Hinweis: Konnte SUPABASE_URL oder SUPABASE_SERVICE_KEY nicht ermitteln. Läuft Supabase? (npx supabase start)" >&2
fi


