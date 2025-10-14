# CI/CD Patterns Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: GitHub Actions, CI/CD best practices, DevOps patterns

## Overview

Continuous Integration and Continuous Deployment (CI/CD) automate testing, building, and deployment processes. This ensures code quality and enables rapid, reliable releases.

## Core Principles

1. **Automate Everything** - Build, test, deploy
2. **Fast Feedback** - Quick pipeline execution
3. **Fail Fast** - Stop on first error
4. **Reproducible** - Consistent across environments
5. **Security First** - Scan for vulnerabilities

## CI/CD Pipeline Stages

### 1. Code Quality
- Linting
- Formatting
- Type checking

### 2. Testing
- Unit tests
- Integration tests
- E2E tests

### 3. Building
- Compile code
- Bundle assets
- Generate artifacts

### 4. Security
- Dependency scanning
- SAST (Static Application Security Testing)
- Secret detection

### 5. Deployment
- Staging deployment
- Production deployment
- Rollback capability

## GitHub Actions

### Basic Workflow
```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npm run type-check

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build
```

### Full Pipeline Example
```yaml
# TODO: Add complete CI/CD workflow
# Matrix builds, caching, artifacts, deployment
```

### Caching Dependencies
```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### Matrix Testing
```yaml
strategy:
  matrix:
    node-version: [18, 20]
    os: [ubuntu-latest, macos-latest, windows-latest]

runs-on: ${{ matrix.os }}

steps:
  - uses: actions/setup-node@v4
    with:
      node-version: ${{ matrix.node-version }}
```

## Testing in CI

### Unit and Integration Tests
```yaml
- name: Run tests
  run: npm test -- --coverage

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage/coverage-final.json
```

### E2E Tests
```yaml
- name: Install Playwright
  run: npx playwright install --with-deps

- name: Run E2E tests
  run: npm run test:e2e

- name: Upload test results
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: playwright-report
    path: playwright-report/
```

## Build and Deploy

### Build Artifact
```yaml
- name: Build
  run: npm run build

- name: Upload artifact
  uses: actions/upload-artifact@v3
  with:
    name: dist
    path: dist/
```

### Deploy to Vercel
```yaml
# TODO: Add Vercel deployment
```

### Deploy to Netlify
```yaml
# TODO: Add Netlify deployment
```

### Deploy to AWS
```yaml
# TODO: Add AWS deployment
```

## Environment Variables and Secrets

```yaml
env:
  NODE_ENV: production

steps:
  - name: Deploy
    env:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
      API_KEY: ${{ secrets.API_KEY }}
    run: npm run deploy
```

## Security Scanning

### Dependency Audit
```yaml
- name: Audit dependencies
  run: npm audit --audit-level=high
```

### CodeQL Analysis
```yaml
- name: Initialize CodeQL
  uses: github/codeql-action/init@v2
  with:
    languages: javascript, typescript

- name: Perform CodeQL Analysis
  uses: github/codeql-action/analyze@v2
```

### Secret Scanning
```yaml
# TODO: Add gitleaks or truffleHog
```

## Monorepo CI/CD

```yaml
# TODO: Add Turborepo CI example
# Selective testing, caching, affected packages
```

## Branch Protection Rules

### Required Checks
```yaml
# Settings > Branches > Branch protection rules
- Require status checks to pass
- Require branches to be up to date
- Require review from Code Owners
- No force pushes
- No deletions
```

## Performance Optimization

### Parallel Jobs
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build
```

### Conditional Execution
```yaml
- name: Deploy to production
  if: github.ref == 'refs/heads/main'
  run: npm run deploy:prod
```

## Deployment Strategies

### Blue-Green Deployment
```yaml
# TODO: Add blue-green deployment pattern
```

### Canary Deployment
```yaml
# TODO: Add canary deployment pattern
```

### Rolling Deployment
```yaml
# TODO: Add rolling deployment pattern
```

## Rollback Strategies

```yaml
# TODO: Add rollback workflow
# Revert deployment, restore database
```

## Notifications

### Slack Notifications
```yaml
- name: Slack notification
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'CI/CD Pipeline completed'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
  if: always()
```

## Best Practices

1. Keep pipelines fast (< 10 minutes)
2. Cache dependencies
3. Run tests in parallel
4. Fail fast on errors
5. Use matrix builds for multiple environments
6. Store secrets securely
7. Deploy to staging first
8. Automate rollbacks
9. Monitor pipeline performance
10. Use reusable workflows

## Common Mistakes

### 1. Slow Pipelines
```yaml
# Bad: Sequential jobs
# Good: Parallel jobs when possible
```

### 2. No Caching
```yaml
# Bad: Install deps every time
# Good: Cache node_modules
```

### 3. Secrets in Code
```yaml
# Bad: Hardcoded secrets
# Good: Use GitHub Secrets
```

## Tools and Services

### CI/CD Platforms
- GitHub Actions
- GitLab CI
- CircleCI
- Jenkins
- Travis CI

### Deployment Platforms
- Vercel
- Netlify
- AWS
- Google Cloud
- Azure

## Additional Resources

- [GIT_WORKFLOW.md](./GIT_WORKFLOW.md) - Git practices
- [DOCKER_PATTERNS.md](./DOCKER_PATTERNS.md) - Containerization
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
