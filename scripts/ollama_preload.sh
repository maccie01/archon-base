#!/usr/bin/env bash
set -euo pipefail

# Preload required Ollama models into the running 'ollama' container

MODELS=(
  "qwen2.5-coder:7b"
  "nomic-embed-text"
)

if ! command -v docker >/dev/null 2>&1; then
  echo "docker ist nicht installiert." >&2
  exit 1
fi

if ! docker ps --format '{{.Names}}' | grep -q '^ollama$'; then
  echo "Ollama-Container 'ollama' läuft nicht. Bitte zuerst starten:" >&2
  echo "  docker compose -f docker/compose.ollama.yaml up -d" >&2
  exit 1
fi

for model in "${MODELS[@]}"; do
  echo "==> Lade Modell: $model"
  docker exec -it ollama ollama pull "$model"
done

echo "Alle Modelle geladen."


