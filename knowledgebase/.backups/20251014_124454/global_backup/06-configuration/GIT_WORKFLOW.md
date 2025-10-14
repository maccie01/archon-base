# Git Workflow Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Git best practices, conventional commits, branching strategies

## Overview

A well-defined Git workflow ensures code quality, enables collaboration, and maintains project history. This guide covers branching strategies, commit conventions, and PR practices.

## Core Principles

1. **Atomic Commits** - One logical change per commit
2. **Clear History** - Readable commit messages
3. **Branch Protection** - Require reviews and checks
4. **Clean Branches** - Delete after merge
5. **Consistent Process** - Same workflow for all

## Branching Strategies

### Trunk-Based Development (Recommended)
```
main (production-ready)
  - feature/user-auth
  - feature/dashboard
  - fix/login-bug
```

**Benefits:**
- Simple
- Fast integration
- Fewer merge conflicts
- Better for CI/CD

### GitFlow (Complex Projects)
```
main (production)
develop (integration)
  - feature/xxx
  - release/v1.2.0
  - hotfix/critical-bug
```

**Use When:**
- Multiple release versions
- Long-running releases
- Complex release process

## Branch Naming Conventions

```bash
# Features
feature/user-authentication
feature/dashboard-redesign

# Bug fixes
fix/login-redirect
fix/memory-leak

# Hotfixes
hotfix/security-patch
hotfix/critical-bug

# Releases
release/v1.2.0
release/2024-01

# Experimental
experiment/new-architecture
spike/performance-test
```

## Commit Message Convention

### Conventional Commits
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting, no code change
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks
- `perf`: Performance improvement
- `ci`: CI/CD changes
- `build`: Build system changes

### Examples
```bash
feat(auth): add JWT authentication

Implement JWT-based authentication with refresh tokens.
Includes login, logout, and token refresh endpoints.

Closes #123

---

fix(api): handle null user profile

Prevent null pointer exception when user profile is not set.

---

docs: update API documentation

Add examples for new authentication endpoints.

---

refactor(database): optimize query performance

Replace N+1 queries with batch loading.
Reduces API response time by 50%.
```

### Commit Message Rules
1. Use imperative mood ("add" not "added")
2. Keep subject under 50 characters
3. Capitalize subject line
4. No period at end of subject
5. Separate subject from body with blank line
6. Wrap body at 72 characters
7. Explain what and why, not how

## Pull Request Process

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No console.logs left
- [ ] Tests pass locally

## Related Issues
Closes #123
```

### PR Best Practices
1. Keep PRs small (< 400 lines)
2. Single purpose per PR
3. Write descriptive title
4. Include context in description
5. Link related issues
6. Request specific reviewers
7. Respond to feedback promptly
8. Squash commits if needed

## Code Review Guidelines

### Reviewer Responsibilities
- Review within 24 hours
- Be constructive and kind
- Focus on logic, not style
- Ask questions, don't demand
- Approve when ready

### Author Responsibilities
- Keep PR small and focused
- Write clear description
- Respond to all comments
- Make requested changes
- Update PR when ready

## Pre-commit Hooks

### Setup with Husky
```bash
npm install -D husky lint-staged
npx husky install
```

### Pre-commit Hook
```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npx lint-staged
```

### lint-staged Configuration
```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,css}": [
      "prettier --write"
    ]
  }
}
```

### Commit Message Validation
```bash
# .husky/commit-msg
npx --no -- commitlint --edit $1
```

## Common Git Commands

### Starting Work
```bash
# Get latest changes
git pull origin main

# Create feature branch
git checkout -b feature/new-feature

# Check status
git status
```

### Making Changes
```bash
# Stage changes
git add .

# Commit with message
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/new-feature
```

### Updating Branch
```bash
# Rebase on main
git fetch origin
git rebase origin/main

# Or merge
git merge origin/main
```

### Fixing Mistakes
```bash
# Amend last commit
git commit --amend

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard local changes
git restore .
```

## Best Practices

1. Commit often, push regularly
2. Write clear commit messages
3. Keep branches up to date
4. Review your own PR first
5. Delete merged branches
6. Use .gitignore properly
7. Never force push to main
8. Test before committing
9. Keep PR description updated
10. Resolve conflicts promptly

## Common Mistakes

### 1. Large Commits
```bash
# Bad: Everything in one commit
git add .
git commit -m "Update stuff"

# Good: Logical commits
git add src/auth/
git commit -m "feat(auth): add JWT authentication"
git add src/api/
git commit -m "feat(api): add auth endpoints"
```

### 2. Vague Messages
```bash
# Bad
git commit -m "fix bug"
git commit -m "update"
git commit -m "wip"

# Good
git commit -m "fix(auth): prevent null user error"
git commit -m "docs: update API examples"
git commit -m "refactor(db): optimize queries"
```

### 3. Working Directly on Main
```bash
# Bad
git checkout main
# make changes
git commit -m "changes"

# Good
git checkout -b feature/my-feature
# make changes
git commit -m "feat: add feature"
```

## Tools

### Git Clients
- GitKraken
- SourceTree
- GitHub Desktop
- VS Code Git integration

### Commit Message Tools
- commitlint
- commitizen
- git-cz

### Code Review
- GitHub PR reviews
- GitLab MR reviews
- Gerrit

## Additional Resources

- [CI_CD_PATTERNS.md](./CI_CD_PATTERNS.md) - Automation
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Best Practices](https://git-scm.com/book/en/v2)
