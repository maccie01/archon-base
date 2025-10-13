# Local Supabase for Archon (CLI-based)

This directory contains a Supabase CLI setup for running Supabase locally with Archon.

## Quick Start

### 1. Start Supabase

```bash
cd /Users/janschubert/tools/archon/supabase
npx supabase start
```

This will:
- Start all Supabase services in Docker
- Create PostgreSQL database with pgvector
- Run Archon migrations automatically
- Start Studio UI for database management
- Display connection keys

### 2. Copy Connection Details

After starting, you'll see output like:

```
Started supabase local development setup.

         API URL: http://127.0.0.1:54321
          DB URL: postgresql://postgres:postgres@127.0.0.1:54322/postgres
      Studio URL: http://127.0.0.1:54323
        anon key: eyJhbGc...
service_role key: eyJhbGc...  <-- Copy this!
```

### 3. Update Archon's .env

Edit `/Users/janschubert/tools/archon/.env`:

```bash
# For Archon running in Docker
SUPABASE_URL=http://host.docker.internal:54321
SUPABASE_SERVICE_KEY=<paste_service_role_key_here>
```

### 4. Start Archon

```bash
cd /Users/janschubert/tools/archon
docker compose up -d
```

### 5. Access Studio UI

Open http://127.0.0.1:54323 in your browser to:
- Browse Archon tables
- Run SQL queries
- View API logs
- Test endpoints

## Directory Structure

```
supabase/
├── config.toml                # Supabase configuration
├── migrations/                # Database migrations
│   └── 20250101000000_archon_initial_setup.sql
├── reference/                 # Docker Compose reference files
│   ├── docker-compose-reference.yml
│   └── kong-reference.yml
└── README.md                  # This file
```

## Common Commands

### Start Services
```bash
npx supabase start
```

### Stop Services
```bash
npx supabase stop
```

### Reset Database (Fresh Start)
```bash
npx supabase db reset
```
This will:
- Drop all tables
- Re-run all migrations
- Give you a clean database

### Check Status
```bash
npx supabase status
```

### View Logs
```bash
npx supabase logs
```

### Access Database
```bash
# Using psql
psql postgresql://postgres:postgres@127.0.0.1:54322/postgres

# Or use any GUI tool:
# - TablePlus
# - DBeaver
# - pgAdmin
```

## Connection Details

When services are running:

- **API URL**: `http://127.0.0.1:54321`
- **Database**: `postgresql://postgres:postgres@127.0.0.1:54322/postgres`
- **Studio UI**: `http://127.0.0.1:54323`
- **Service Role Key**: Shown on startup (long JWT token)

**For Archon**: Use `http://host.docker.internal:54321` (not localhost!)

## Database Management

### Studio UI (Recommended)

http://127.0.0.1:54323

Features:
- **Table Editor**: Browse and edit data
- **SQL Editor**: Run queries
- **Database**: View schema
- **API**: Test endpoints

### External Tools

Connect with any PostgreSQL client:

**Connection Settings:**
- Host: `127.0.0.1`
- Port: `54322`
- User: `postgres`
- Password: `postgres`
- Database: `postgres`

**Recommended Tools:**
- **TablePlus** (Paid, beautiful UI)
- **DBeaver** (Free, powerful)
- **pgAdmin** (Free, web-based)

## Migrations

### View Migrations
```bash
npx supabase migration list
```

### Create New Migration
```bash
npx supabase migration new your_migration_name
```

This creates a new file in `migrations/`. Edit it with your SQL.

### Apply Migrations
```bash
npx supabase db push
```

Or just restart:
```bash
npx supabase db reset
```

## Troubleshooting

### Port Conflicts

If ports are in use, edit `config.toml`:

```toml
[api]
port = 54321  # Change this

[db]
port = 54322  # And this

[studio]
port = 54323  # And this
```

Then restart:
```bash
npx supabase stop
npx supabase start
```

### Database Not Initializing

```bash
npx supabase stop --no-backup
npx supabase start
```

### Archon Can't Connect

Make sure you're using `host.docker.internal` in Archon's `.env`:

```bash
SUPABASE_URL=http://host.docker.internal:54321  # ✅ Correct
# NOT: http://localhost:54321                   # ❌ Wrong
```

### View All Containers

```bash
docker ps | grep supabase
```

Should show ~8 containers running.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Archon Services                         │
│  (archon-server, archon-mcp, archon-ui)                 │
│                                                          │
│  Connect via: http://host.docker.internal:54321         │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│         Supabase Stack (Managed by CLI)                  │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Studio UI   │  │   PostgREST  │  │   Realtime   │  │
│  │  (54323)     │  │   (54321)    │  │              │  │
│  └──────────────┘  └──────┬───────┘  └──────┬───────┘  │
│                            │                  │          │
│  ┌──────────────┐         │                  │          │
│  │   Storage    │         │                  │          │
│  │   Service    │         │                  │          │
│  └──────┬───────┘         │                  │          │
│         │                 │                  │          │
│         └─────────────────┴──────────────────┘          │
│                           │                             │
│                           ▼                             │
│  ┌──────────────────────────────────────────────────┐  │
│  │   PostgreSQL + pgvector (54322)                  │  │
│  │   - Archon tables                                │  │
│  │   - Vector embeddings                            │  │
│  │   - Project/task data                            │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Benefits of CLI

✅ **Studio UI** - Beautiful web interface
✅ **Official** - Maintained by Supabase team
✅ **Auto-updates** - Get latest features
✅ **Migration tools** - Built-in management
✅ **Type generation** - For TypeScript
✅ **Easy reset** - One command clean slate

## Reference Files

See `reference/` folder for:
- Manual Docker Compose setup (if you want to run without CLI)
- Kong configuration
- Useful for understanding what's happening under the hood

## Workflow

### Daily Startup

```bash
# Terminal 1: Start Supabase
cd /Users/janschubert/tools/archon/supabase
npx supabase start

# Terminal 2: Start Archon
cd /Users/janschubert/tools/archon
docker compose up -d

# Access:
# - Archon: http://localhost:3737
# - Studio: http://localhost:54323
```

### Daily Shutdown

```bash
# Stop Archon
cd /Users/janschubert/tools/archon
docker compose down

# Optional: Stop Supabase (saves RAM)
cd supabase
npx supabase stop
```

### When Developing

Keep Supabase running, restart Archon as needed:

```bash
cd /Users/janschubert/tools/archon
docker compose restart archon-server
```

## Data Management

### Backup
```bash
npx supabase db dump -f backup.sql
```

### Restore
```bash
npx supabase db reset
psql postgresql://postgres:postgres@127.0.0.1:54322/postgres < backup.sql
```

### Export Data
Use Studio UI → Table Editor → Export

## Next Steps

1. Start Supabase: `npx supabase start`
2. Note the `service_role key` from output
3. Update Archon's `.env` with connection details
4. Start Archon: `cd .. && docker compose up -d`
5. Open Studio UI: http://127.0.0.1:54323
6. Open Archon UI: http://localhost:3737

## Documentation

- [Supabase CLI Reference](https://supabase.com/docs/guides/cli)
- [Local Development Guide](https://supabase.com/docs/guides/local-development)
- [Archon Documentation](../README.md)
