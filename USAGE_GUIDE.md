# Archon Usage Guide for Multiple Projects

**Date**: October 13, 2025
**System**: MacBook Pro M2, 16GB RAM
**Projects Directory**: `/Users/janschubert/code-projects`

---

## Quick Reference

```bash
archon start          # Start everything (Supabase + Archon)
archon stop           # Stop everything (frees ~10GB RAM)
archon status         # Check what's running
archon health         # Detailed health check
archon help           # Full command list
```

**URLs:**
- Archon UI: http://localhost:3737
- Supabase Studio: http://127.0.0.1:54323

---

## Quick Start

Archon is now installed and configured as a **system-wide service** that you can use across all your code projects.

### Starting and Stopping Archon

From any directory, use these commands:

```bash
# Start both Supabase and Archon (default)
archon start

# Stop both Supabase and Archon (frees all resources)
archon stop

# Check service status
archon status            # Shows both Supabase and Archon
archon health            # Detailed health check

# View logs
archon logs              # All services
archon logs archon-server   # Specific service

# Restart services
archon restart           # All Archon services
archon restart archon-mcp   # Specific service
```

**Advanced Control:**
```bash
# Start/stop only Archon (Supabase stays running)
archon start --archon-only
archon stop --archon-only

# Control Supabase independently
archon supabase start
archon supabase stop
archon supabase status

# Start with optional agents service
archon start --with-agents
```

**Note**: The `archon` command is immediately available (installed in `~/.local/bin`). If it doesn't work, open a new terminal tab.

### Access Points

Once started, Archon is accessible at:

- **Web UI**: http://localhost:3737
- **API Server**: http://localhost:8181
- **MCP Server**: http://localhost:8051
- **Supabase Studio**: http://127.0.0.1:54323

---

## How Archon Works with Your Projects

Archon is a **centralized knowledge base** that works across all your projects. Here's how to integrate it:

### 1. Knowledge Base Approach (Recommended)

Use Archon to build a knowledge base for each project or technology:

**For a specific project:**
1. Go to Archon UI: http://localhost:3737
2. Navigate to "Knowledge Base" → "Add Source"
3. Options:
   - **Crawl project documentation** (e.g., framework docs)
   - **Upload project files** (markdown, code, PDFs)
   - **Crawl internal wikis** or READMEs

**For general technologies:**
- Crawl official documentation (React, FastAPI, etc.)
- Upload coding standards or style guides
- Store reusable code examples

### 2. MCP Integration (AI Coding Assistants)

Connect your AI coding assistant (Claude Code, Cursor, Windsurf) to Archon's MCP server:

1. Go to Archon UI → MCP tab: http://localhost:3737/mcp
2. Copy the MCP configuration
3. Add to your AI assistant's MCP settings
4. Your AI assistant can now:
   - Search your knowledge base
   - Retrieve code examples
   - Access project documentation

**Available MCP Tools:**
- `archon:rag_search_knowledge_base` - Search for relevant content
- `archon:rag_search_code_examples` - Find code snippets
- `archon:rag_get_available_sources` - List knowledge sources
- `archon:rag_read_full_page` - Read full documentation pages

### 3. Project Management (Optional)

Use Archon's Projects feature to organize work:

1. Enable Projects in Settings (enabled by default)
2. Create a project for each codebase in `/Users/janschubert/code-projects`
3. Link relevant knowledge sources to each project
4. Track tasks and document versions

---

## Workflow Examples

### Example 1: Starting a New React Project

```bash
cd /Users/janschubert/code-projects/new-react-app

# Archon is already running system-wide, just use it:
# 1. Open Archon UI
open http://localhost:3737

# 2. Add React documentation to knowledge base
#    - Navigate to Knowledge Base → Add Source
#    - Enter: https://react.dev/learn
#    - Archon will crawl and index the docs

# 3. Your AI assistant (with MCP) can now answer:
#    "Search the knowledge base for React hooks examples"
```

### Example 2: Working on an Existing Python Project

```bash
cd /Users/janschubert/code-projects/my-python-api

# Upload your project's README and docs to Archon
# Option A: Via UI
open http://localhost:3737
# Upload files through Knowledge Base → Upload

# Option B: Via API (automation)
curl -X POST http://localhost:8181/api/knowledge/upload \
  -F "file=@README.md" \
  -F "title=My Python API Docs"

# Your AI assistant can now reference your project docs
```

### Example 3: Building Knowledge for Multiple Projects

```bash
# Archon runs once, serves all projects

# Add knowledge sources for different tech stacks:
# - Frontend: React, Next.js docs
# - Backend: FastAPI, Django docs
# - DevOps: Docker, Kubernetes docs

# All projects in /Users/janschubert/code-projects can:
# 1. Access the same knowledge base
# 2. Use the same MCP connection
# 3. Share code examples and patterns
```

---

## Managing Archon

### Starting Fresh After Restart

If you restart your Mac, nothing runs automatically. Simply start Archon when you need it:

```bash
# Start both Supabase and Archon
archon start

# That's it! One command starts everything
```

**What happens:**
1. Checks if Supabase is already running
2. Starts Supabase if needed
3. Starts all Archon services
4. Waits for services to be healthy

**When you're done coding:**
```bash
# Stop everything and free ~10GB of RAM
archon stop
```

### Updating Knowledge Base

**Add new sources:**
```bash
archon ui  # Opens http://localhost:3737
# Navigate to Knowledge Base → Add Source
```

**Remove outdated sources:**
1. Go to Knowledge Base
2. Find the source
3. Delete it

**Re-crawl updated documentation:**
1. Go to Knowledge Base
2. Select source
3. Click "Re-crawl"

### Monitoring

```bash
# Check all services are running
archon status

# View real-time logs
archon logs

# Check specific service health
curl http://localhost:8181/health  # Server
curl http://localhost:8051/health  # MCP
```

### Troubleshooting

**Services won't start:**
```bash
# Check what's using the ports
lsof -i :3737  # Archon UI
lsof -i :8181  # Archon Server
lsof -i :8051  # Archon MCP

# Check Supabase is running
npx supabase status

# Restart everything
archon stop
archon start
```

**Can't connect to Supabase:**
```bash
# Verify Supabase is running
docker ps | grep supabase

# Restart Supabase
npx supabase stop
npx supabase start
```

**MCP connection issues:**
```bash
# Check MCP server logs
archon logs archon-mcp

# Verify MCP health
curl http://localhost:8051/health

# Get MCP configuration
open http://localhost:3737/mcp
```

---

## Advanced Usage

### Using Different Models

Archon is configured to use Ollama with `qwen2.5-coder:7b`. To change models:

1. Pull a new model:
   ```bash
   ollama pull llama3.2:3b  # Smaller, faster
   ollama pull deepseek-coder:6.7b  # Code-focused
   ```

2. Update `.env`:
   ```bash
   cd /Users/janschubert/tools/archon
   nano .env
   # Change: MODEL_CHOICE=qwen2.5-coder:7b
   # To:     MODEL_CHOICE=llama3.2:3b
   ```

3. Restart Archon:
   ```bash
   archon restart
   ```

### Accessing Supabase Database

**Via Studio UI:**
```bash
archon db  # Opens http://127.0.0.1:54323
```

**Via psql:**
```bash
psql postgresql://postgres:postgres@127.0.0.1:54322/postgres
```

**View data:**
- `archon_sources` - Knowledge sources
- `archon_crawled_pages` - Indexed documents
- `archon_code_examples` - Code snippets
- `archon_projects` - Projects (if enabled)
- `archon_tasks` - Tasks

### Backup Your Knowledge Base

```bash
# Backup Supabase database
cd /Users/janschubert/tools/archon
npx supabase db dump -f backup_$(date +%Y%m%d).sql

# Restore from backup
npx supabase db reset
psql postgresql://postgres:postgres@127.0.0.1:54322/postgres < backup_20251013.sql
```

---

## Best Practices

### 1. Organize Knowledge Sources

Create clear categories:
- **Project Docs**: Upload your project's README, architecture docs
- **Framework Docs**: Crawl official documentation
- **Code Examples**: Upload or extract reusable patterns
- **Team Standards**: Coding guidelines, style guides

### 2. Keep Knowledge Fresh

- Re-crawl documentation when frameworks update
- Remove outdated sources
- Update code examples as patterns evolve

### 3. Use Projects Feature

For each codebase in `/Users/janschubert/code-projects`:
- Create an Archon project
- Link relevant knowledge sources
- Track tasks and features
- Store version history

### 4. Integrate with AI Assistants

- Connect Claude Code, Cursor, or Windsurf via MCP
- Use tools like `rag_search_knowledge_base` in prompts
- Let AI assistants reference your knowledge base automatically

---

## Configuration Files

**Archon CLI**: `/Users/janschubert/tools/archon/archon-cli.sh` (symlinked to `~/.local/bin/archon`)
**Environment**: `/Users/janschubert/tools/archon/.env`
**Docker Compose**: `/Users/janschubert/tools/archon/docker-compose.yml`
**Supabase Config**: `/Users/janschubert/tools/archon/supabase/config.toml`

**How the `archon` command works:**
- Symlink in `~/.local/bin/archon` → actual script at `/Users/janschubert/tools/archon/archon-cli.sh`
- `~/.local/bin` is already in your PATH (configured by pipx)
- Works immediately in any terminal without sourcing

---

## Resource Usage

**Expected Memory Usage:**
- Ollama (qwen2.5-coder:7b): ~5.5GB
- Archon Containers: ~2-3GB
- Supabase: ~1GB
- **Total**: ~8-10GB / 16GB available

**Ports Used:**
- 3737 - Archon UI
- 8181 - Archon Server
- 8051 - Archon MCP
- 8052 - Archon Agents (optional)
- 11434 - Ollama
- 54321-54324 - Supabase

---

## Summary

Archon is now ready to use across all your projects in `/Users/janschubert/code-projects`:

**To start working:**
1. `archon start` (from any directory)
2. Open http://localhost:3737
3. Add knowledge sources (documentation, files)
4. Connect your AI assistant via MCP
5. Build your knowledge base over time

**Key Advantage**: One centralized knowledge base for all projects, accessible from anywhere via MCP or UI.

**Need Help?**
- View logs: `archon logs`
- Check status: `archon status`
- Help: `archon help`

---

**Setup Date**: October 13, 2025
**Status**: ✅ Fully Configured and Running
