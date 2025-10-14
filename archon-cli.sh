#!/usr/bin/env bash
# Archon CLI - Manage Archon and Supabase from anywhere
# Location: /Users/janschubert/tools/archon

set -e

ARCHON_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$ARCHON_DIR/docker-compose.yml"

cd "$ARCHON_DIR"

open_url() {
  local url="$1"
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$url" >/dev/null 2>&1 || echo "$url"
  elif command -v open >/dev/null 2>&1; then
    open "$url" >/dev/null 2>&1 || echo "$url"
  else
    echo "$url"
  fi
}

# Helper functions
is_supabase_running() {
  npx -y supabase@latest status 2>&1 | grep -q "supabase local development setup is running"
}

is_archon_running() {
  docker compose ps --services --filter "status=running" 2>/dev/null | grep -q "archon-server"
}

start_supabase() {
  if is_supabase_running; then
    echo "✓ Supabase is already running"
  else
    echo "Starting Supabase..."
    npx -y supabase@latest start
    echo "✅ Supabase started"
  fi
}

stop_supabase() {
  if is_supabase_running; then
    echo "Stopping Supabase..."
    npx -y supabase@latest stop
    echo "✅ Supabase stopped"
  else
    echo "✓ Supabase is not running"
  fi
}

start_archon() {
  local WITH_AGENTS=$1
  if [ "$WITH_AGENTS" = "--with-agents" ]; then
    docker compose --profile agents up -d
  else
    docker compose up -d
  fi
}

case "$1" in
  start)
    # Parse flags
    ARCHON_ONLY=false
    WITH_AGENTS=false

    for arg in "$@"; do
      case $arg in
        --archon-only)
          ARCHON_ONLY=true
          ;;
        --with-agents)
          WITH_AGENTS=true
          ;;
      esac
    done

    if [ "$ARCHON_ONLY" = true ]; then
      echo "Starting Archon only (Supabase must be running)..."
      if ! is_supabase_running; then
        echo "⚠️  Warning: Supabase is not running. Archon will fail to connect."
        echo "   Run 'archon start' without --archon-only to start both."
        exit 1
      fi
      start_archon $([ "$WITH_AGENTS" = true ] && echo "--with-agents")
      echo "✅ Archon services started!"
    else
      echo "Starting Supabase and Archon..."
      start_supabase
      echo ""
      echo "Starting Archon services..."
      start_archon $([ "$WITH_AGENTS" = true ] && echo "--with-agents")
      echo ""
      echo "✅ All services started!"
    fi

    echo ""
    echo "Access points:"
    echo "  • Archon UI:    http://localhost:3737"
    echo "  • Archon API:   http://localhost:8181"
    echo "  • MCP Server:   http://localhost:8051"
    echo "  • Supabase UI:  http://127.0.0.1:54323"
    echo ""
    echo "Check status:   archon status"
    echo "View logs:      archon logs [service]"
    ;;

  stop)
    # Parse flags
    ARCHON_ONLY=false

    for arg in "$@"; do
      case $arg in
        --archon-only)
          ARCHON_ONLY=true
          ;;
      esac
    done

    if [ "$ARCHON_ONLY" = true ]; then
      echo "Stopping Archon only (Supabase will keep running)..."
      docker compose down
      echo "✅ Archon services stopped"
    else
      echo "Stopping Archon and Supabase..."
      docker compose down
      stop_supabase
      echo "✅ All services stopped"
    fi
    ;;

  restart)
    SERVICE=$2
    if [ -n "$SERVICE" ]; then
      echo "Restarting $SERVICE..."
      docker compose restart "$SERVICE"
      echo "✅ Service $SERVICE restarted"
    else
      echo "Restarting all Archon services..."
      docker compose restart
      echo "✅ All Archon services restarted"
    fi
    ;;

  status|ps)
    echo "=== Supabase Status ==="
    if is_supabase_running; then
      npx -y supabase@latest status
    else
      echo "❌ Supabase is not running"
      echo "   Start with: archon start"
    fi

    echo ""
    echo "=== Archon Services ==="
    if is_archon_running; then
      docker compose ps
    else
      echo "❌ Archon is not running"
      echo "   Start with: archon start"
    fi
    ;;

  logs)
    SERVICE=$2
    if [ -z "$SERVICE" ]; then
      docker compose logs -f
    else
      docker compose logs -f "$SERVICE"
    fi
    ;;

  rebuild)
    echo "Rebuilding and restarting Archon services..."
    docker compose down
    docker compose up --build -d
    echo "✅ Archon services rebuilt and started"
    ;;

  supabase)
    shift
    if [ "$1" = "start" ]; then
      start_supabase
    elif [ "$1" = "stop" ]; then
      stop_supabase
    elif [ "$1" = "status" ]; then
      if is_supabase_running; then
        npx -y supabase@latest status
      else
        echo "❌ Supabase is not running"
      fi
    else
      npx -y supabase@latest "$@"
    fi
    ;;

  db)
    if ! is_supabase_running; then
      echo "⚠️  Supabase is not running. Starting it now..."
      start_supabase
      echo ""
    fi
    echo "Opening Supabase Studio..."
    open_url "http://127.0.0.1:54323"
    ;;

  ui)
    if ! is_archon_running; then
      echo "⚠️  Archon is not running. Start it with: archon start"
      exit 1
    fi
    echo "Opening Archon UI..."
    open_url "http://localhost:3737"
    ;;

  clean)
    echo "⚠️  This will remove all Archon data and containers."
    echo "    Supabase database will be preserved."
    read -p "Continue? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      echo "Cleaning up Archon containers and volumes..."
      docker compose down -v
      echo "✅ Archon cleanup complete"
      echo ""
      echo "To also reset Supabase database:"
      echo "  archon supabase db reset"
    else
      echo "Cancelled"
    fi
    ;;

  health)
    echo "=== Health Check ==="
    echo ""

    # Check Supabase
    echo -n "Supabase: "
    if is_supabase_running; then
      echo "✅ Running"
    else
      echo "❌ Not running"
    fi

    # Check Archon services
    echo -n "Archon Server: "
    if curl -s http://localhost:8181/health > /dev/null 2>&1; then
      echo "✅ Healthy"
    else
      echo "❌ Not responding"
    fi

    echo -n "MCP Server: "
    if curl -s http://localhost:8051/health > /dev/null 2>&1; then
      echo "✅ Healthy"
    else
      echo "❌ Not responding"
    fi

    echo -n "Archon UI: "
    if curl -s http://localhost:3737 > /dev/null 2>&1; then
      echo "✅ Healthy"
    else
      echo "❌ Not responding"
    fi

    echo -n "Ollama: "
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
      echo "✅ Running"
    else
      echo "❌ Not running"
    fi
    ;;

  help|--help|-h)
    cat <<EOF
Archon CLI - Manage Archon and Supabase from anywhere

Usage: archon <command> [options]

Main Commands:
  start [flags]           Start services (default: both Supabase and Archon)
  stop [flags]            Stop services (default: both Supabase and Archon)
  restart [service]       Restart Archon services or specific service
  status | ps             Show status of all services
  health                  Check health of all services
  logs [service]          View logs (all services or specific)

Flags for start/stop:
  --archon-only           Only start/stop Archon (not Supabase)
  --with-agents           Include agents service (optional, for start only)

Supabase Commands:
  supabase start          Start only Supabase
  supabase stop           Stop only Supabase
  supabase status         Check Supabase status
  supabase <cmd>          Run any Supabase CLI command

Utility Commands:
  db                      Open Supabase Studio UI
  ui                      Open Archon UI
  rebuild                 Rebuild and restart Archon services
  clean                   Remove Archon containers and volumes

Services:
  archon-server           Core API and crawling (port 8181)
  archon-mcp              MCP protocol interface (port 8051)
  archon-ui               Web interface (port 3737)
  archon-agents           AI/ML operations (port 8052, optional)

Examples:
  archon start                    # Start both Supabase and Archon
  archon start --with-agents      # Start with agents service
  archon start --archon-only      # Start only Archon (Supabase must be running)
  archon stop                     # Stop both (frees all resources)
  archon stop --archon-only       # Stop only Archon (keep Supabase running)
  archon status                   # Check what's running
  archon health                   # Detailed health check
  archon supabase start           # Start only Supabase
  archon supabase stop            # Stop only Supabase
  archon logs archon-server       # View server logs
  archon restart archon-mcp       # Restart MCP server
  archon supabase db reset        # Reset database

Location: $ARCHON_DIR
EOF
    ;;

  *)
    echo "Unknown command: $1"
    echo "Run 'archon help' for usage information"
    exit 1
    ;;
esac
