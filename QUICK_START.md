# Archon Quick Start

**Status**: ✅ Fully Configured and Ready
**Setup Date**: October 13, 2025

---

## Initial Setup

If this is your first time setting up Archon, run the automated setup script:

```bash
bash scripts/setup.sh
```

This will:
- Install prerequisites (Docker, Node, jq)
- Initialize and start Supabase
- Start Ollama with required models
- Generate your `.env` values

Then copy the displayed values to your `.env` file and start Archon.

For detailed server setup instructions, see **SERVER_SETUP.md**.

---

## Essential Commands

```bash
archon start          # Start everything (Supabase + Archon)
archon stop           # Stop everything (frees ~10GB RAM)
archon status         # Check what's running
archon health         # Detailed health check
archon help           # See all commands
```

## Access Points

- **Archon UI**: http://localhost:3737
- **Supabase Studio**: http://127.0.0.1:54323
- **Archon API**: http://localhost:8181
- **MCP Server**: http://localhost:8051

---

## Typical Workflow

### Starting a Coding Session

```bash
# From any directory in your code projects
cd ~/code-projects/my-project

# Start Archon (one command starts everything)
archon start

# Verify everything is healthy
archon health
```

**What starts:**
- ✅ Supabase database (12 containers, ~1GB RAM)
- ✅ Archon services (3 containers, ~2-3GB RAM)
- ✅ Total: ~10GB RAM used

### During Development

**Open the UI:**
```bash
archon ui  # Opens http://localhost:3737
```

**Add knowledge to Archon:**
1. Crawl documentation (React, FastAPI, etc.)
2. Upload project files (README, docs)
3. Extract code examples

**Connect AI Assistant:**
1. Go to http://localhost:3737/mcp
2. Copy MCP configuration
3. Add to your AI assistant (Claude Code, Cursor, Windsurf)

### Ending Your Session

```bash
# Stop everything and free resources
archon stop

# Frees ~10GB of RAM
```

---

## Advanced Control

### Independent Control

```bash
# Start/stop only Archon (leave Supabase running)
archon start --archon-only
archon stop --archon-only

# Control Supabase separately
archon supabase start
archon supabase stop
archon supabase status

# Start with optional agents service
archon start --with-agents
```

### Troubleshooting

```bash
# Check detailed status
archon status

# View logs
archon logs                  # All services
archon logs archon-server    # Specific service

# Restart a service
archon restart archon-mcp

# Check health
archon health
```

### Common Issues

**Services won't start:**
```bash
archon status  # Check what's running
archon stop    # Stop everything
archon start   # Fresh start
```

**Check specific service:**
```bash
archon logs archon-server  # API logs
archon logs archon-mcp     # MCP logs
```

**Database issues:**
```bash
archon supabase status     # Check Supabase
archon db                  # Open Studio UI
```

---

## Configuration

### What's Configured

**Local LLM (Ollama)**:
- Model: `qwen2.5-coder:7b` (4.9GB)
- Embeddings: `nomic-embed-text` (274MB)
- Port: 11434
- Zero cost, runs locally

**Database (Supabase)**:
- PostgreSQL 17 with pgvector
- Ports: 54321 (API), 54322 (DB), 54323 (Studio)
- All migrations applied
- Security configured

**Archon Services**:
- Server: Port 8181 (Core API and crawling)
- MCP: Port 8051 (MCP protocol interface)
- UI: Port 3737 (Web interface)
- Agents: Port 8052 (Optional ML/reranking)

### Configuration Files

- **CLI**: `~/.local/bin/archon` → `/Users/janschubert/tools/archon/archon-cli.sh`
- **Environment**: `/Users/janschubert/tools/archon/.env`
- **Docker Compose**: `/Users/janschubert/tools/archon/docker-compose.yml`
- **Supabase**: `/Users/janschubert/tools/archon/supabase/config.toml`

---

## Using Archon with Your Projects

### How It Works

Archon is a **centralized knowledge base** for all projects in `/Users/janschubert/code-projects`:

1. **Start once**, use everywhere
2. **One knowledge base** for all projects
3. **MCP integration** for AI assistants
4. **No per-project setup** required

### Example: New React Project

```bash
cd ~/code-projects/new-react-app

# 1. Archon is already running (or start it)
archon start

# 2. Open Archon UI
archon ui

# 3. Add React documentation
#    - Knowledge Base → Add Source
#    - Enter: https://react.dev/learn
#    - Archon crawls and indexes

# 4. Your AI assistant can now:
#    - Search React docs via MCP
#    - Find code examples
#    - Reference patterns
```

### Example: Python API Project

```bash
cd ~/code-projects/my-python-api

# 1. Upload project docs to Archon
archon ui
# Knowledge Base → Upload → README.md, ARCHITECTURE.md

# 2. Add FastAPI docs
# Knowledge Base → Add Source → https://fastapi.tiangolo.com

# 3. AI assistant references:
#    - Your project docs
#    - FastAPI documentation
#    - Code examples from both
```

---

## Resource Usage

**Memory Usage:**
- Supabase: ~1GB
- Archon: ~2-3GB
- Ollama (models loaded): ~5.5GB
- **Total**: ~8-10GB / 16GB

**When Stopped:**
- All containers stopped
- RAM freed
- Ollama still running (always available)
- **Free**: ~14GB / 16GB

---

## Next Steps

### First Time Setup

1. ✅ **Start Archon**: `archon start`
2. ✅ **Verify Health**: `archon health`
3. 📝 **Add Knowledge**: Open http://localhost:3737
   - Crawl documentation sites
   - Upload project files
4. 🔌 **Connect AI Assistant**:
   - Go to http://localhost:3737/mcp
   - Copy MCP config
   - Add to Claude Code/Cursor/Windsurf

### Daily Workflow

**Morning:**
```bash
archon start  # One command, ~30 seconds
```

**During the day:**
- Use AI assistant with MCP integration
- Add knowledge as you discover useful docs
- Upload project documentation

**Evening:**
```bash
archon stop   # Frees ~10GB RAM
```

---

## Help and Documentation

**Quick Help:**
```bash
archon help
```

**Detailed Guides:**
- **USAGE_GUIDE.md**: Complete usage documentation
- **SERVER_SETUP.md**: Server setup for Ubuntu with local Supabase + Ollama
- **SETUP_VALIDATION_REPORT.md**: Full setup validation
- **DATABASE_REVIEW.md**: Database schema details

**Community:**
- GitHub: https://github.com/coleam00/archon
- Issues: https://github.com/coleam00/archon/issues
- Discussions: https://github.com/coleam00/archon/discussions

---

## Summary

✅ **Archon is ready to use!**

**Key Points:**
- One command to start: `archon start`
- One command to stop: `archon stop`
- Works across all your projects
- Zero API costs (local Ollama)
- Centralized knowledge base
- MCP integration for AI assistants

**Start using it now:**
```bash
archon start
archon ui
```

Add your first knowledge source and start building your personal knowledge base!
