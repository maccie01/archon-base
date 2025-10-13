# Supabase Setup Guide

## Step 1: Clean Up the Folder

Run the cleanup script:
```bash
cd /Users/janschubert/tools/archon/supabase
chmod +x cleanup.sh
./cleanup.sh
```

This will:
- Move old docker-compose files to `reference/`
- Remove outdated documentation
- Leave only: `config.toml`, `migrations/`, `reference/`, and `README.md`

## Step 2: Start Supabase

```bash
npx supabase start
```

**First time:** This will download Docker images (~2-3 minutes)
**Subsequent starts:** Much faster

## Step 3: Note the Keys

You'll see output like:
```
Started supabase local development setup.

         API URL: http://127.0.0.1:54321
          DB URL: postgresql://postgres:postgres@127.0.0.1:54322/postgres
      Studio URL: http://127.0.0.1:54323
        anon key: eyJhbGc...
service_role key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1v...
```

**Copy the entire `service_role key`** (the long JWT token)

## Step 4: Update Archon's .env

```bash
cd /Users/janschubert/tools/archon
nano .env  # or your preferred editor
```

Add these lines (or update if they exist):
```bash
SUPABASE_URL=http://host.docker.internal:54321
SUPABASE_SERVICE_KEY=<paste_the_service_role_key_here>
```

**Important:** Use `host.docker.internal` NOT `localhost` or `127.0.0.1`

## Step 5: Open Studio UI

Open in your browser:
**http://127.0.0.1:54323**

You should see:
- Table Editor with Archon tables (sources, documents, archon_projects, archon_tasks)
- SQL Editor for running queries
- Database schema view

## Step 6: Start Archon

```bash
cd /Users/janschubert/tools/archon
docker compose up -d
```

Access Archon at: **http://localhost:3737**

## Troubleshooting

### Error: "supabase not found"
The npx command will automatically download it. Just wait.

### Error: "Port already in use"
Something is using port 54321, 54322, or 54323.

Check what's running:
```bash
lsof -i :54321
lsof -i :54322
lsof -i :54323
```

Kill if needed or edit `config.toml` to use different ports.

### Error: "Cannot connect to Docker"
Make sure Docker Desktop is running.

### Migration errors
If migrations don't run automatically:
```bash
npx supabase db reset
```

## What Error Did You Get?

Please share the exact error message from `npx supabase start` so I can help troubleshoot!
