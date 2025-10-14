#!/usr/bin/env bash
set -euo pipefail

MODELS=(
  "qwen2.5-coder:7b"
  "nomic-embed-text"
)

if ! command -v docker >/dev/null 2>&1; then
  echo "Error: docker command not found." >&2
  echo "Solution: Install Docker and ensure it's in PATH." >&2
  exit 1
fi

if ! docker ps --format '{{.Names}}' | grep -q '^ollama$'; then
  echo "Error: Ollama container 'ollama' not running." >&2
  echo "Solution: Start Ollama container first:" >&2
  echo "  docker compose -f docker/compose.ollama.yaml up -d" >&2
  exit 1
fi

for model in "${MODELS[@]}"; do
  echo "==> Pulling model: $model"
  docker exec -it ollama ollama pull "$model"
done

echo "All models loaded."


