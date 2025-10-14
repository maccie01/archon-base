## Archon Server Setup (Ubuntu)

This guide targets a fresh Ubuntu server (root or sudo access). Goal: run local Supabase via Supabase CLI, Ollama in Docker, generate required `.env` values, and later start Archon services via CLI.

### 1) Prepare the repository

```bash
git clone https://github.com/<ORG>/archon-base.git /opt/archon-base
cd /opt/archon-base
```

Optional: update system packages
```bash
sudo apt-get update -y && sudo apt-get upgrade -y
```

### 2) Automated Setup

The setup script will automatically:
- Install Docker and Docker Compose v2
- Add your user to the docker group
- Verify Node/npm/npx availability
- Initialize and start Supabase
- Start Ollama container
- Preload required Ollama models
- Generate and display your .env values

```bash
bash /opt/archon-base/scripts/setup.sh
```

**What happens:**
1. Prerequisites check (Docker, Node, jq)
2. Supabase initialization (if first run)
3. Supabase startup (creates 12 containers)
4. Ollama container startup
5. Model preloading (qwen2.5-coder:7b, nomic-embed-text)
6. .env values generation and display

**Notes:**
- After being added to the `docker` group, you must log out and back in for the change to take effect.
- Model preloading may take several minutes depending on your bandwidth.
- The script will display all required .env values at the end.

### 3) Configure Environment Variables

The setup script displays all required values. Copy them to your `.env`:

```bash
cd /opt/archon-base
cp .env.example .env
# Edit .env and paste the values shown by setup.sh
```

**Required values** (displayed by setup.sh):
```env
SUPABASE_URL=http://127.0.0.1:54321
SUPABASE_SERVICE_KEY=<generated-service-key>
```

**Optional values** (can be configured later in Settings UI):
```env
LLM_PROVIDER=ollama
LLM_BASE_URL=http://host.docker.internal:11434/v1
MODEL_CHOICE=qwen2.5-coder:7b
EMBEDDING_MODEL=nomic-embed-text
```

### 4) Validation

Verify everything is running:

```bash
# Check Supabase
npx -y supabase@latest status

# Check Ollama
curl -s http://localhost:11434/api/tags | jq

# Verify Docker containers
docker ps
```

If `host.docker.internal` does not resolve on Linux, add to affected Compose services:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

### 5) Start Archon services (after `.env` is set)

The CLI is included and adapted for Linux.

```bash
bash /opt/archon-base/archon-cli.sh start
# Check status
bash /opt/archon-base/archon-cli.sh status
```

Access points:
- Archon UI: `http://<server-ip>:3737`
- Archon API: `http://<server-ip>:8181`
- MCP Server: `http://<server-ip>:8051`
- Supabase Studio (port bound to localhost only; use SSH tunnel): `http://127.0.0.1:54323`

### 6) Stop/restart services

```bash
bash /opt/archon-base/archon-cli.sh stop
bash /opt/archon-base/archon-cli.sh restart <service>
```

### Troubleshooting

- Docker permission denied: after running `setup.sh`, re-login or run `newgrp docker`.
- Docker not running: `sudo systemctl enable --now docker` and check logs `journalctl -u docker -e`.
- Supabase keys empty: ensure `npx supabase start` succeeded; inspect `npx supabase status --json`.
- Ollama not responding: `docker logs ollama`, open port 11434, preload models.
- Missing `host.docker.internal`: see `extra_hosts` above.

### Arch Linux notes

- Docker: `sudo pacman -Syu docker` and enable service: `sudo systemctl enable --now docker`.
- Supabase CLI: use via `npx supabase` per project (no system-wide installation needed).
- Same workflow: `scripts/setup.sh`, `npx supabase start`, Ollama compose, generate `.env`, start Archon.

### macOS notes (local development)

- Install Docker Desktop (GUI), then run `scripts/setup.sh` (installs jq, validates Node/npx).
- `host.docker.internal` is available by default.
- Start flow: `npx supabase start`, Ollama compose, generate `.env`, `archon-cli.sh start`.


