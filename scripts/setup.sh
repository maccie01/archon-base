#!/usr/bin/env bash

set -euo pipefail

# Cross-platform setup for local prerequisites
# - Ubuntu/Arch/macOS detection
# - Installs Docker, Docker Compose plugin (if needed)
# - Adds current user to docker group (Linux) using sudo
# - Validates Node/npm/npx availability for running Supabase via npx
# - Does NOT start Archon containers; only prepares environment

echo "==> Archon local setup (Docker + prerequisites)"

require_cmd() {
  command -v "$1" >/dev/null 2>&1
}

# Determine privilege escalation tool (sudo/doas) or none if running as root
SUDO=""
set_sudo_prefix() {
  if [[ "${EUID:-$(id -u)}" -eq 0 ]]; then
    SUDO=""
    return
  fi
  if require_cmd sudo; then
    SUDO="sudo"
    return
  fi
  if require_cmd doas; then
    SUDO="doas"
    return
  fi
  echo "Neither sudo nor doas found. Run this script as root or install sudo/doas." >&2
  exit 1
}

OS="unknown"
if [[ "${OSTYPE:-}" == linux* ]]; then
  if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    case "${ID:-}" in
      ubuntu|debian)
        OS="ubuntu"
        ;;
      arch)
        OS="arch"
        ;;
      *)
        OS="linux"
        ;;
    esac
  else
    OS="linux"
  fi
elif [[ "${OSTYPE:-}" == darwin* ]]; then
  OS="macos"
fi

echo "Detected OS: $OS"

ensure_sudo() {
  if ! require_cmd sudo; then
    echo "sudo is required. Please install/configure sudo and re-run." >&2
    exit 1
  fi
}

install_docker_linux() {
  ensure_sudo
  if require_cmd docker; then
    echo "Docker already installed"
  else
    if [[ "$OS" == "ubuntu" ]]; then
      echo "Installing Docker (Ubuntu)"
      sudo apt-get update -y
      sudo apt-get install -y ca-certificates curl gnupg lsb-release
      sudo install -m 0755 -d /etc/apt/keyrings
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
      echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
      sudo apt-get update -y
      sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    elif [[ "$OS" == "arch" ]]; then
      echo "Installing Docker (Arch)"
      sudo pacman --noconfirm -Sy docker
      # docker compose plugin on Arch is part of docker-compose v2 in community; fallback to docker-compose if needed
      if ! require_cmd docker; then
        echo "Docker installation failed on Arch." >&2
        exit 1
      fi
    else
      echo "Please install Docker manually for OS: $OS" >&2
      exit 1
    fi
  fi

  # Enable/start Docker service on Linux
  if [[ -f /bin/systemctl || -f /usr/bin/systemctl ]]; then
    sudo systemctl enable docker || true
    sudo systemctl start docker || true
  fi

  # Add current user to docker group
  if getent group docker >/dev/null 2>&1; then
    if id -nG "$USER" | tr ' ' '\n' | grep -qx docker; then
      echo "User $USER already in docker group"
    else
      echo "Adding $USER to docker group (requires re-login)"
      sudo usermod -aG docker "$USER" || true
      echo "Please log out and log back in for group changes to take effect."
    fi
  else
    echo "Creating docker group and adding $USER"
    sudo groupadd docker || true
    sudo usermod -aG docker "$USER" || true
    echo "Please log out and log back in for group changes to take effect."
  fi
}

install_docker_macos() {
  if require_cmd docker; then
    echo "Docker already installed"
  else
    if require_cmd brew; then
      echo "Installing Docker (macOS via Homebrew Cask)"
      brew install --cask docker
      echo "Launch Docker Desktop manually to finish setup."
    else
      echo "Homebrew not found. Install Docker Desktop from: https://www.docker.com/products/docker-desktop" >&2
    fi
  fi
}

ensure_docker() {
  if [[ "$OS" == "macos" ]]; then
    install_docker_macos
  else
    install_docker_linux
  fi

  if ! require_cmd docker; then
    echo "Docker not available after installation." >&2
    exit 1
  fi

  if ! docker version >/dev/null 2>&1; then
    echo "Docker daemon not running. Please start Docker and retry." >&2
    exit 1
  fi
}

ensure_docker_compose() {
  if docker compose version >/dev/null 2>&1; then
    echo "Docker Compose v2 detected"
    return
  fi
  echo "Docker Compose v2 plugin not found. Installing (Linux only)."
  if [[ "$OS" == "ubuntu" ]]; then
    ensure_sudo
    sudo apt-get update -y
    sudo apt-get install -y docker-compose-plugin
  elif [[ "$OS" == "arch" ]]; then
    ensure_sudo
    sudo pacman --noconfirm -Sy docker-compose
  else
    echo "Please install Docker Compose manually for OS: $OS" >&2
  fi
}

ensure_node_tools() {
  if ! require_cmd node; then
    echo "Node.js ist erforderlich. Bitte Node.js 18+ installieren und erneut ausführen." >&2
    exit 1
  fi
  if ! require_cmd npm; then
    echo "npm ist erforderlich. Bitte npm installieren (kommt normalerweise mit Node.js)." >&2
    exit 1
  fi
  if ! require_cmd npx; then
    echo "npx ist erforderlich. Bitte npm/npx installieren (kommt normalerweise mit Node.js)." >&2
    exit 1
  fi
}

ensure_jq() {
  if require_cmd jq; then
    return
  fi
  case "$OS" in
    ubuntu|linux)
      ensure_sudo
      sudo apt-get update -y && sudo apt-get install -y jq
      ;;
    arch)
      ensure_sudo
      sudo pacman --noconfirm -Sy jq
      ;;
    macos)
      if require_cmd brew; then
        brew install jq
      else
        echo "Install Homebrew first: https://brew.sh" >&2
      fi
      ;;
  esac
}

# Execute prerequisite checks
ensure_docker
ensure_docker_compose
ensure_node_tools
ensure_jq

echo ""
echo "==> Prerequisites installed."
echo ""

# Get script directory for relative paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Step 1: Initialize Supabase if needed
echo "==> Step 1/5: Initializing Supabase..."
if [[ ! -d "$PROJECT_ROOT/supabase" ]]; then
  echo "Initializing Supabase (first run)..."
  cd "$PROJECT_ROOT"
  npx -y supabase@latest init
else
  echo "Supabase already initialized (supabase/ directory exists)"
fi

# Step 2: Start Supabase
echo ""
echo "==> Step 2/5: Starting Supabase..."
cd "$PROJECT_ROOT"
npx -y supabase@latest start
echo "Supabase started successfully"

# Step 3: Start Ollama
echo ""
echo "==> Step 3/5: Starting Ollama container..."
if docker ps --format '{{.Names}}' | grep -q '^ollama$'; then
  echo "Ollama container already running"
else
  docker compose -f "$PROJECT_ROOT/docker/compose.ollama.yaml" up -d
  echo "Ollama container started"
  sleep 3
fi

# Step 4: Preload Ollama models
echo ""
echo "==> Step 4/5: Preloading Ollama models (this may take several minutes)..."
bash "$SCRIPT_DIR/ollama_preload.sh"

# Step 5: Generate and display .env values
echo ""
echo "==> Step 5/5: Generating .env values..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "                     COPY THESE VALUES TO YOUR .env FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get Supabase values
SUPA_JSON=$(npx -y supabase@latest status --json 2>/dev/null || echo '{}')
URL=$(echo "$SUPA_JSON" | jq -r '.apiUrl // empty')
SERVICE_KEY=$(echo "$SUPA_JSON" | jq -r '.serviceRoleKey // empty')

echo "# 1. Copy .env.example to .env:"
echo "#    cp .env.example .env"
echo ""
echo "# 2. Add these values to your .env file:"
echo ""
echo "SUPABASE_URL=$URL"
echo "SUPABASE_SERVICE_KEY=$SERVICE_KEY"
echo ""
echo "# Optional LLM configuration (defaults are shown, can be changed in Settings UI):"
echo "# LLM_PROVIDER=ollama"
echo "# LLM_BASE_URL=http://host.docker.internal:11434/v1"
echo "# MODEL_CHOICE=qwen2.5-coder:7b"
echo "# EMBEDDING_MODEL=nomic-embed-text"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [[ -z "$URL" || -z "$SERVICE_KEY" ]]; then
  echo "⚠️  Warning: Could not retrieve SUPABASE_URL or SUPABASE_SERVICE_KEY." >&2
  echo "    Supabase may not be running correctly. Check: npx supabase status" >&2
  echo ""
fi

echo "==> Setup complete!"
echo ""
echo "Next steps:"
echo "  1) Copy the values above into your .env file"
echo "  2) Start Archon services:"
if [[ -f "$PROJECT_ROOT/archon-cli.sh" ]]; then
  echo "     bash $PROJECT_ROOT/archon-cli.sh start"
else
  echo "     docker compose up -d"
fi
echo ""


