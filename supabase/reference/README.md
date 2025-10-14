# Docker Compose Reference

This folder contains reference Docker Compose files for running Supabase manually without the CLI.

## Files

- `docker-compose-reference.yml` - Minimal Supabase setup
- `kong-reference.yml` - Kong API Gateway configuration (from original setup)

## Why Reference Only?

We use **Supabase CLI** (`npx supabase`) instead because it:
- Includes Studio UI for database management
- Handles migrations automatically
- Gets official updates
- Provides additional tooling

## When to Use This

Use these reference files if you:
- Want to run without Node.js/npx
- Need a minimal, lightweight setup
- Want to customize the stack heavily
- Are deploying to production-like environments

## How to Use

```bash
cd /Users/janschubert/tools/archon/supabase/reference
docker compose -f docker-compose-reference.yml up -d
```

But for development, we recommend using the CLI from the parent directory:
```bash
cd /Users/janschubert/tools/archon/supabase
npx supabase start
```
