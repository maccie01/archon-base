#!/usr/bin/env bash

set -euo pipefail

echo "==> Archon local setup (Docker + prerequisites)"

require_cmd() {
  command -v "$1" >/dev/null 2>&1
}

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
  echo "Error: Privilege escalation required but neither sudo nor doas found." >&2
  echo "Solution: Run as root or install sudo/doas and retry." >&2
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
    echo "Error: sudo not found." >&2
    echo "Solution: Install sudo or run as root." >&2
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
      if ! require_cmd docker; then
        echo "Error: Docker installation failed on Arch." >&2
        echo "Context: pacman install completed but docker command not found." >&2
        exit 1
      fi
    else
      echo "Error: Unsupported OS for automatic Docker installation: $OS" >&2
      echo "Solution: Install Docker manually from https://docs.docker.com/engine/install/" >&2
      exit 1
    fi
  fi

  if [[ -f /bin/systemctl || -f /usr/bin/systemctl ]]; then
    sudo systemctl enable docker || true
    sudo systemctl start docker || true
  fi

  if getent group docker >/dev/null 2>&1; then
    if id -nG "$USER" | tr ' ' '\n' | grep -qx docker; then
      echo "User $USER already in docker group"
    else
      echo "Adding $USER to docker group (requires re-login)"
      sudo usermod -aG docker "$USER" || true
      echo "ACTION REQUIRED: Log out and log back in for docker group changes to take effect."
    fi
  else
    echo "Creating docker group and adding $USER"
    sudo groupadd docker || true
    sudo usermod -aG docker "$USER" || true
    echo "ACTION REQUIRED: Log out and log back in for docker group changes to take effect."
  fi
}

install_docker_macos() {
  if require_cmd docker; then
    echo "Docker already installed"
  else
    if require_cmd brew; then
      echo "Installing Docker (macOS via Homebrew)"
      brew install --cask docker
      echo "ACTION REQUIRED: Launch Docker Desktop manually to complete setup."
    else
      echo "Error: Homebrew not found on macOS." >&2
      echo "Solution: Install Docker Desktop from https://www.docker.com/products/docker-desktop" >&2
      echo "Or install Homebrew from https://brew.sh then retry." >&2
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
    echo "Error: Docker command not available after installation attempt." >&2
    echo "Solution: Verify Docker is installed correctly and in PATH." >&2
    exit 1
  fi

  if ! docker version >/dev/null 2>&1; then
    echo "Error: Docker daemon not running." >&2
    echo "Solution: Start Docker Desktop (macOS) or 'sudo systemctl start docker' (Linux)." >&2
    exit 1
  fi
}

ensure_docker_compose() {
  if docker compose version >/dev/null 2>&1; then
    echo "Docker Compose v2 detected"
    return
  fi
  echo "Docker Compose v2 not found, attempting installation"
  if [[ "$OS" == "ubuntu" ]]; then
    ensure_sudo
    sudo apt-get update -y
    sudo apt-get install -y docker-compose-plugin
  elif [[ "$OS" == "arch" ]]; then
    ensure_sudo
    sudo pacman --noconfirm -Sy docker-compose
  else
    echo "Error: Docker Compose v2 not found on OS: $OS" >&2
    echo "Solution: Install docker-compose-plugin manually for your OS." >&2
  fi
}

ensure_node_tools() {
  if ! require_cmd node; then
    echo "Error: Node.js not found." >&2
    echo "Solution: Install Node.js 18+ from https://nodejs.org/ and retry." >&2
    exit 1
  fi
  if ! require_cmd npm; then
    echo "Error: npm not found." >&2
    echo "Solution: npm usually comes with Node.js. Reinstall Node.js or install npm separately." >&2
    exit 1
  fi
  if ! require_cmd npx; then
    echo "Error: npx not found." >&2
    echo "Solution: npx comes with npm 5.2+. Update npm or install npx separately." >&2
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
        echo "Error: Homebrew required to install jq on macOS." >&2
        echo "Solution: Install Homebrew from https://brew.sh then retry." >&2
      fi
      ;;
  esac
}

ensure_docker
ensure_docker_compose
ensure_node_tools
ensure_jq

echo ""
echo "==> Prerequisites installed."
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "==> Step 1/5: Initializing Supabase..."
if [[ ! -d "$PROJECT_ROOT/supabase" ]]; then
  echo "Initializing Supabase (first run)"
  cd "$PROJECT_ROOT"
  npx -y supabase@latest init
else
  echo "Supabase already initialized"
fi

echo ""
echo "==> Step 2/5: Starting Supabase..."
cd "$PROJECT_ROOT"
npx -y supabase@latest start
echo "Supabase started"

echo ""
echo "==> Step 3/5: Starting Ollama container..."
if docker ps --format '{{.Names}}' | grep -q '^ollama$'; then
  echo "Ollama container already running"
else
  docker compose -f "$PROJECT_ROOT/docker/compose.ollama.yaml" up -d
  echo "Ollama container started"
  sleep 3
fi

echo ""
echo "==> Step 4/5: Preloading Ollama models..."
echo "Note: This may take several minutes depending on bandwidth."
bash "$SCRIPT_DIR/ollama_preload.sh"

echo ""
echo "==> Step 5/5: Generating .env values..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "                     COPY THESE VALUES TO YOUR .env FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

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
echo "# Optional LLM configuration (defaults shown, configurable in Settings UI):"
echo "# LLM_PROVIDER=ollama"
echo "# LLM_BASE_URL=http://host.docker.internal:11434/v1"
echo "# MODEL_CHOICE=qwen2.5-coder:7b"
echo "# EMBEDDING_MODEL=nomic-embed-text"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [[ -z "$URL" || -z "$SERVICE_KEY" ]]; then
  echo "Error: Could not retrieve SUPABASE_URL or SUPABASE_SERVICE_KEY." >&2
  echo "Context: Supabase may not be running or status command failed." >&2
  echo "Solution: Run 'npx supabase status' to verify Supabase is running." >&2
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


