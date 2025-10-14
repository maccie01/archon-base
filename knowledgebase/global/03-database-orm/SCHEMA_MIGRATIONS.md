# Research Result: Schema Migrations

# Drizzle Schema Migrations: End-to-End Workflows, Patterns, and Production Practices

Main takeaway: Standardize on “code-first with generated SQL” using Drizzle Kit generate/migrate for controlled rollouts, pair it with an expand/contract zero-downtime strategy, and wrap it in CI/CD with automated backups, status checks, and rollback playbooks. Use custom SQL files for gaps and deterministic seeding for test/stage reliability.[orm.drizzle**+3**](https://orm.drizzle.team/docs/kit-overview)

## 1) Creating Migrations

## 1.1 Drizzle Kit configuration (drizzle.config.ts)

A minimal, portable config for PostgreSQL that supports multi-environment usage and generated SQL migrations.

ts<code>// drizzle.config.ts
import{ defineConfig }from"drizzle-kit";
import"dotenv/config";

exportdefaultdefineConfig({
  schema:"./src/db/schema.ts",// your Drizzle TS schema
  out:"./drizzle/migrations",// generated SQL migrations
  dialect:"postgresql",// or "mysql" | "sqlite"
// Optional when using drizzle-kit migrate (recommended):
  dbCredentials:{
    url: process.env.DATABASE_URL!,// use env per env stage
},
// Optional: multiple configs via CLI --config path
});
</code>

Why: Drizzle Kit needs dialect and schema path to generate migrations. The CLI supports generate, migrate, push, pull, studio, check, and up commands.[orm.drizzle](https://orm.drizzle.team/docs/kit-overview)

## 1.2 Generate migrations from schema changes

Generate migration SQL files from your TypeScript schema changes.

bash<code># First time or after schema edits
npx drizzle-kit generate --config drizzle.config.ts
# or via package.json scripts:
# "db:generate": "drizzle-kit generate --config drizzle.config.ts"
</code>

Effect: Compares current schema.ts to the target DB state (via configured DB or local state) and emits ordered SQL files under out (e.g., drizzle/migrations).[orm.drizzle**+1**](https://orm.drizzle.team/docs/migrations)

## 1.3 Manual/Custom migrations

Use custom SQL when Drizzle cannot express a DDL or for data changes.

bash<code># Create an empty migration to hand-write SQL
# (Drizzle supports custom/empty migration files you write by hand)
# After creating an empty file, you place your SQL there.
</code>

sql<code>-- drizzle/migrations/00XX_custom_feature.sql
-- Example: policies, triggers, function definitions, data backfills, etc.
-- Write pure SQL here; it will be applied by drizzle-kit migrate.
</code>

Why: Drizzle supports generating empty migration files for custom SQL not covered by Drizzle or for data seeding scripts; these run with drizzle-kit migrate.[orm.drizzle](https://orm.drizzle.team/docs/kit-custom-migrations)

## 1.4 Migration file structure

Generated migrations include:

* SQL files with deterministic hashes tracked in the __drizzle_migrations table (hash, created_at, status planned).[github](https://github.com/drizzle-team/drizzle-orm/discussions/2624)
* A “journal/init” concept for initial state; use migrate with --no-init on existing databases that already match the schema.[github](https://github.com/drizzle-team/drizzle-orm/discussions/2624)

## 2) Running Migrations

## 2.1 Apply migrations (up)

Preferred command for new and existing environments.

bash<code># Apply all pending migrations
npx drizzle-kit migrate --config drizzle.config.ts

# For targets that already have an 'init' schema equivalent:
npx drizzle-kit migrate --config drizzle.config.ts --no-init
</code>

Notes:

* --no-init skips the initial snapshot when the DB already contains the schema, avoiding conflicts with already-existing objects.[github](https://github.com/drizzle-team/drizzle-orm/discussions/2624)
* drizzle-kit migrate reads the migrations folder and updates the __drizzle_migrations journal table.[orm.drizzle**+1**](https://orm.drizzle.team/docs/migrations)

## 2.2 Rollback (down)

Current status and approaches:

* Drizzle historically did not support automatic “down” migrations; teams maintain paired .down.sql files or manual rollback playbooks in custom pipelines.[github](https://github.com/drizzle-team/drizzle-orm/discussions/1339)
* drizzle-kit drop removes migration records but does not revert DB state; not a rollback mechanism.[stackoverflow](https://stackoverflow.com/questions/78745661/anyway-to-migrate-down-in-drizzle)

Recommended patterns:

* Write explicit reverse SQL in custom files for high-risk changes and wire a “rollback job” in CI/CD that runs those SQL scripts.
* Keep point-in-time restore and backup-based rollback as the authoritative safety net (see Production Best Practices).

## 2.3 Migration status checking and conflicts

Useful commands/practices:

* drizzle-kit check helps detect race conditions or collisions among generated migrations.[orm.drizzle](https://orm.drizzle.team/docs/kit-overview)
* When moving environments that pre-exist the schema, prefer --no-init to avoid “objects exist” errors; Drizzle now hints this path.[github](https://github.com/drizzle-team/drizzle-orm/discussions/2624)

## 3) Migration Strategies

## 3.1 Code-first strategies supported by Drizzle

Drizzle supports:

* push: Directly apply schema from code (fast for prototypes/dev).[orm.drizzle](https://orm.drizzle.team/docs/migrations)
* generate + migrate: Produce SQL and apply in a controlled, reviewable manner (recommended for prod).[orm.drizzle](https://orm.drizzle.team/docs/migrations)
* pull: Introspect DB to schema in code (database-first scenarios).[orm.drizzle](https://orm.drizzle.team/docs/migrations)

## 3.2 Zero-downtime migrations (expand/contract)

Pattern:

* Expand: Add new nullable columns, new tables, or backfill-friendly structures. Deploy code that reads/writes both old and new paths.
* Backfill: Run data migration in batches to populate new structures.
* Contract: Add constraints (e.g., NOT NULL) only after backfill; drop old columns after code no longer depends on them.

Drizzle provides the migration engine; apply the pattern operationally (dual-writes/feature flags) to avoid blocking locks. Tools like pgroll formalize this approach for Postgres (expand/contract with reversibility).[neon](https://neon.com/guides/pgroll)

## 3.3 Data migrations vs schema migrations

* Schema migrations: DDL-only SQL generated by Drizzle, versioned and deterministic.
* Data migrations: DML scripts for backfills/fixes; add as custom SQL files and run via drizzle-kit migrate, or run application-managed scripts during deploys. Keep them idempotent and chunked.

## 3.4 Handling breaking changes

* Avoid in-place destructive changes. Use expand/contract, feature flags, and phased rollouts.
* If breaking is unavoidable, coordinate maintenance windows and have restore/rollback prepared.

## 4) Seeding Data

## 4.1 Seed file structure

Option A: Deterministic seeds with drizzle-seed

* drizzle-seed generates deterministic, reproducible fake data using a seeded PRNG; supports per-table configuration, with/relationships, weighted random, and dialect-aware reset routines.[orm.drizzle](https://orm.drizzle.team/docs/seed-overview)

ts<code>// scripts/seed.ts
import{ drizzle }from"drizzle-orm/node-postgres";
import{ Pool }from"pg";
import{ seed }from"drizzle-seed";
import{ users, posts }from"../src/db/schema";
import"dotenv/config";

const pool =newPool({ connectionString: process.env.DATABASE_URL});
const db =drizzle(pool);

awaitseed(db,{ count:20, seed:1337}).refine(({ int, text })=>({
  users:{
    columns:{
      username: text.username(),
      email: text.email(),
},
with:{
      posts:3,// create 3 posts per user (one-to-many)
},
},
  posts:{
    columns:{
      title: text.lorem({ sentences:1}),
      body: text.lorem({ sentences:3}),
      likes: int.between(0,1000),
},
},
}));
await pool.end();
</code>

Option B: Custom seed script (faker)

* Roll your own using faker and a Node client; good for basic scenarios.[dev](https://dev.to/anasrin/seeding-database-with-drizzle-orm-fga)

ts<code>// scripts/seed-basic.ts
import{ drizzle }from"drizzle-orm/node-postgres";
import{ Pool }from"pg";
import{ users }from"../src/db/schema";
import{ faker }from"@faker-js/faker";
import"dotenv/config";

const pool =newPool({ connectionString: process.env.DATABASE_URL});
const db =drizzle(pool);

const batch =Array.from({ length:20},()=>({
  username: faker.internet.userName(),
  email: faker.internet.email(),
}));

await db.insert(users).values(batch);
await pool.end();
</code>

## 4.2 Development vs production seeds

* Development: Rich, deterministic datasets to aid developer workflows and integration tests.
* Production: Minimal baseline or reference data only. Prefer idempotent scripts that safely upsert core rows.

## 4.3 Idempotent seeds and resets

* Make seeds safe to re-run (check existence, upsert unique keys).
* drizzle-seed includes a reset helper for dialect-specific table truncation with CASCADE on Postgres.[orm.drizzle](https://orm.drizzle.team/docs/seed-overview)

## 5) Testing Migrations

## 5.1 Testing migration up/down locally

* Spin up an ephemeral Postgres (Docker, Testcontainers).
* Run drizzle-kit migrate against it.
* Optionally test custom rollback scripts on a clone to validate “down” SQL.

bash<code># Example: CI step to validate migrations apply
npx drizzle-kit migrate --config drizzle.config.ts --no-init
</code>

## 5.2 Integration tests with migrations

* Before integration tests, provision DB, run migrations, then seed deterministic data.
* Prefer deterministic seeding (drizzle-seed) for reproducibility across runs.[orm.drizzle](https://orm.drizzle.team/docs/seed-overview)

## 5.3 CI/CD integration (GitHub Actions example)

* On PR: generate migrations, run check, apply to ephemeral DB, run tests.
* On main: apply to staging DB; on release: apply to production.

text<code># .github/workflows/db.yml
name: Database Migrations

on:
  pull_request:
  push:
    branches: [ main ]

jobs:
  migrate-and-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_USER: postgres
          POSTGRES_DB: app
        ports: ["5432:5432"]
        options: >-
          --health-cmd="pg_isready -U postgres" --health-interval=10s
          --health-timeout=5s --health-retries=5
    env:
      DATABASE_URL: postgres://postgres:postgres@localhost:5432/app
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci
      - run: npx drizzle-kit generate --config drizzle.config.ts
      - run: npx drizzle-kit check --config drizzle.config.ts
      - run: npx drizzle-kit migrate --config drizzle.config.ts --no-init
      - run: npm run test
</code>

Reference practices: Drizzle supports generate/migrate flows suitable for CI; use --no-init when the DB already contains the init layout; the migrations journal tracks applied hashes and statuses.[orm.drizzle**+2**](https://orm.drizzle.team/docs/kit-overview)

## 6) Production Best Practices

## 6.1 Backup before migration

* Create a snapshot/backup or enable PITR before applying production DDL.
* For Postgres on managed services, take a snapshot immediately pre-deploy.
* Treat backup restore as the primary rollback path for catastrophic issues.

## 6.2 Migration monitoring and observability

* Track migration start/end, success/failure; consider Drizzle’s planned migrations status column (failed/applied/rollbacked).[github](https://github.com/drizzle-team/drizzle-orm/discussions/2624)
* Monitor DB locks, replication lag, long-running transactions during deploys.

## 6.3 Rollback procedures

* For logical rollback: maintain custom “down” SQL files for high-risk migrations; wire a CI/CD job to run them on demand.[github](https://github.com/drizzle-team/drizzle-orm/discussions/1339)
* For catastrophic rollback: perform DB restore to snapshot/PITR checkpoint.
* For dual-write phases: use feature flags to disable new paths while rolling back schema changes in contract steps.

## 6.4 Blue-green and phased deploys

* Apply migrations to the “green” environment first, verify health, then switch traffic.
* For zero-downtime: use expand/contract pattern; add non-blocking changes first, backfill, then enforce constraints after cutover.[neon](https://neon.com/guides/pgroll)
* Use --no-init for applying to existing environments with the same schema baseline.[github](https://github.com/drizzle-team/drizzle-orm/discussions/2624)

## Complete Workflow: From Schema Change to Production

1. Edit schema.ts (code-first source of truth).[orm.drizzle](https://orm.drizzle.team/docs/migrations)
2. npx drizzle-kit generate to produce SQL.[orm.drizzle](https://orm.drizzle.team/docs/kit-overview)
3. Review SQL (and add custom SQL files if needed).[orm.drizzle](https://orm.drizzle.team/docs/kit-custom-migrations)
4. Local apply: npx drizzle-kit migrate (or --no-init for existing DB).[github](https://github.com/drizzle-team/drizzle-orm/discussions/2624)
5. Seed dev/stage deterministically with drizzle-seed or custom scripts.[dev**+1**](https://dev.to/anasrin/seeding-database-with-drizzle-orm-fga)
6. CI on PR: generate, check, migrate against ephemeral DB, run tests, publish artifacts.[orm.drizzle**+1**](https://orm.drizzle.team/docs/kit-overview)
7. Staging: apply migrations, run smoke and backfill scripts; monitor.
8. Production: backup snapshot, apply migrations during low-traffic window or via blue-green; monitor locks/latency.
9. Contract step when safe: enforce constraints, drop old columns after dual-write is retired.[neon](https://neon.com/guides/pgroll)
10. Rollback plan: custom down SQL or restore; keep instructions in runbooks and wire an emergency CI job.[github](https://github.com/drizzle-team/drizzle-orm/discussions/1339)

## Code Examples Library

## Example A: package.json scripts

json<code>{
"scripts":{
"db:studio":"drizzle-kit studio --config drizzle.config.ts",
"db:generate":"drizzle-kit generate --config drizzle.config.ts",
"db:check":"drizzle-kit check --config drizzle.config.ts",
"db:migrate":"drizzle-kit migrate --config drizzle.config.ts",
"db:migrate:noinit":"drizzle-kit migrate --config drizzle.config.ts --no-init",
"db:pull":"drizzle-kit pull --config drizzle.config.ts",
"db:push":"drizzle-kit push --config drizzle.config.ts",
"db:seed":"tsx scripts/seed.ts",
"db:seed:reset":"tsx scripts/seed-reset.ts"
}
}
</code>

Notes: Studio is optional but handy; pull and push support database-first and code-first workflows respectively.[orm.drizzle**+1**](https://orm.drizzle.team/docs/kit-overview)

## Example B: Apply migrations in Node entrypoint (runtime apply)

Useful for monolith zero-downtime deploys where the app applies pending migrations on start, guarded by health checks.[orm.drizzle](https://orm.drizzle.team/docs/migrations)

ts<code>// .drizzle/migrate.ts
import{ drizzle }from"drizzle-orm/node-postgres";
import{ migrate }from"drizzle-orm/node-postgres/migrator";
import{ Pool }from"pg";
import"dotenv/config";

asyncfunctionrun(){
const pool =newPool({ connectionString: process.env.DATABASE_URL});
const db =drizzle(pool);
awaitmigrate(db,{ migrationsFolder:"./drizzle/migrations"});
await pool.end();
}

run().catch((e)=>{
console.error("Migration failed", e);
  process.exit(1);
});
</code>

Wrap with a deployment pre-start step or blue-green hook.

## Example C: Custom data backfill migration (SQL)

Part of expand/contract. Run after adding a new nullable column.

sql<code>-- drizzle/migrations/00XX_backfill_orders_total.sql
-- Backfill totals in small batches to avoid long locks.
DO $$
DECLARE
  batch_size integer :=5000;
BEGIN
LOOP
WITH cte AS(
SELECT id
FROM orders
WHERE total ISNULL
LIMIT batch_size
)
UPDATE orders o
SET total = sub.t
FROM(
SELECT oi.order_id,SUM(oi.price * oi.qty)AS t
FROM order_items oi
JOIN cte ON oi.order_id = cte.id
GROUPBY oi.order_id
) sub
WHERE o.id = sub.order_id;
EXITWHENNOT FOUND;
    PERFORM pg_sleep(0.05);
ENDLOOP;
END
$$;
</code>

## Example D: Contract step (add constraint when safe)

sql<code>-- drizzle/migrations/00XY_contract_orders_total_not_null.sql
ALTERTABLE orders
ALTERCOLUMN total SETNOTNULL;
</code>

## Example E: Idempotent baseline seed (prod-safe)

Upsert by natural keys or add unique constraints to prevent duplicates.

ts<code>// scripts/seed-baseline.ts
import{ drizzle }from"drizzle-orm/node-postgres";
import{ Pool }from"pg";
import{ roles }from"../src/db/schema";
import{ sql }from"drizzle-orm";
import"dotenv/config";

const pool =newPool({ connectionString: process.env.DATABASE_URL});
const db =drizzle(pool);

await db.execute(sql`
  INSERT INTO roles (code, name)
  VALUES ('admin','Administrator'), ('user','User')
  ON CONFLICT (code) DO UPDATE SET name = EXCLUDED.name;
`);

await pool.end();
</code>

## Example F: Deterministic testing seed (drizzle-seed)

See the earlier drizzle-seed example; reproducible data is invaluable for CI.[orm.drizzle](https://orm.drizzle.team/docs/seed-overview)

## Example G: CI migration job (GitHub Actions)

See the CI example in section 5.3; includes check and migrate.[orm.drizzle**+2**](https://orm.drizzle.team/docs/kit-overview)

## Example H: Backup-and-migrate deploy script (shell)

Wrap DB snapshot, apply migrations, verify, and notify.

bash<code>#!/usr/bin/env bash
set -euo pipefail

echo"Creating DB snapshot..."
# invoke cloud provider snapshot or PITR marker here

echo"Applying migrations..."
npx drizzle-kit migrate --config drizzle.config.ts --no-init

echo"Running post-migration checks..."
# health checks, smoke queries

echo"Done."
</code>

## Example I: Rollback playbook (custom down SQL)

For high-risk migrations, pre-create reverse SQL.

sql<code>-- drizzle/migrations/00XY_down_orders_total.sql
ALTERTABLE orders
ALTERCOLUMN total DROPNOTNULL;

-- Optional: drop column only if feature flag is disabled
-- ALTER TABLE orders DROP COLUMN total;
</code>

Run via a dedicated CI job on demand.

## Example J: Handling existing DBs (no-init)

When deploying to an environment that already matches the initial schema:

bash<code>npx drizzle-kit migrate --config drizzle.config.ts --no-init
</code>

Avoids re-applying init; Drizzle will also prompt this in errors and guidance.[github](https://github.com/drizzle-team/drizzle-orm/discussions/2624)

## Notes, Tradeoffs, and Operational Guidance

* Choose push vs generate/migrate: push is fast but less reviewable; generate/migrate produces SQL you can review and track, better for teams and prod.[orm.drizzle](https://orm.drizzle.team/docs/migrations)
* Down migrations: unsupported as a built-in in many versions; treat rollback as a separate procedure via custom SQL plus backup restores.[stackoverflow**+1**](https://stackoverflow.com/questions/78745661/anyway-to-migrate-down-in-drizzle)
* Zero downtime: expand/contract is the proven pattern; avoid ALTER TABLE operations that take ACCESS EXCLUSIVE locks during traffic spikes; batch DML work.[neon](https://neon.com/guides/pgroll)
* Journaling and status: Drizzle’s migration table tracks hashes and is adding statuses for failure/rollback clarity; ensure your monitoring surfaces these states.[github](https://github.com/drizzle-team/drizzle-orm/discussions/2624)
* Squashing migrations: for long-lived repos, periodically collapse migrations into a new baseline after ensuring all environments are on the latest schema; carefully sync the journal row/hash to production if you reset the file set.[answeroverflow**+1**](https://www.answeroverflow.com/m/1405835544222634055)

## References (inline)

* Drizzle Kit overview and commands[orm.drizzle](https://orm.drizzle.team/docs/kit-overview)
* Drizzle migrations fundamentals and flows (push/generate/pull)[orm.drizzle](https://orm.drizzle.team/docs/migrations)
* Custom migrations (empty files for custom SQL)[orm.drizzle](https://orm.drizzle.team/docs/kit-custom-migrations)
* Seeding with drizzle-seed (deterministic data, reset, with/weighted)[orm.drizzle](https://orm.drizzle.team/docs/seed-overview)
* Example custom seeding with faker and Node Postgres[dev](https://dev.to/anasrin/seeding-database-with-drizzle-orm-fga)
* Expand/contract and zero-downtime patterns; pgroll write-up for Postgres approach[neon](https://neon.com/guides/pgroll)
* Rollback limitations and community workarounds[stackoverflow**+1**](https://stackoverflow.com/questions/78745661/anyway-to-migrate-down-in-drizzle)
* Updated migration process: --no-init, journal/status evolution[github](https://github.com/drizzle-team/drizzle-orm/discussions/2624)

This document satisfies:

* Complete workflow from schema change to production with Drizzle Kit.[orm.drizzle**+1**](https://orm.drizzle.team/docs/kit-overview)
* 10+ code examples across config, generate/apply, rollback, seeds, and CI.
* Rollback procedures documented with custom down SQL and backup restore guidance.[github**+1**](https://github.com/drizzle-team/drizzle-orm/discussions/1339)
* Seeding covered with deterministic and custom approaches.[dev**+1**](https://dev.to/anasrin/seeding-database-with-drizzle-orm-fga)
* Testing and CI/CD examples included.[orm.drizzle**+2**](https://orm.drizzle.team/docs/migrations)