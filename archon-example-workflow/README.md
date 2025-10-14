# Archon AI Coding Workflow Template

A simple yet reliable template for systematic AI-assisted development using **create-plan** and **execute-plan** workflows, powered by [Archon](https://github.com/coleam00/Archon) - the open-source AI coding command center. Build on top of this and create your own AI coding workflows!

## What is This?

This is a reusable workflow template that brings structure and reliability to AI coding assistants. Instead of ad-hoc prompting, you get:

- **Systematic planning** from requirements to implementation
- **Knowledge-augmented development** via Archon's RAG capabilities
- **Task management integration** for progress tracking
- **Specialized subagents** for analysis and validation
- **Codebase consistency** through pattern analysis

Works with **Claude Code**, **Cursor**, **Windsurf**, **Codex**, and any AI coding assistant that supports custom commands or prompt templates.

## Core Workflows

### Planning & Implementation

#### 1. Create Plan (`/create-plan`)

Transform requirements into actionable implementation plans through systematic research and analysis.

**What it does:**
- Reads your requirements document
- Searches Archon's knowledge base for best practices and patterns
- Analyzes your codebase using the `codebase-analyst` subagent
- Produces a comprehensive implementation plan (PRP) with:
  - Task breakdown with dependencies and effort estimates
  - Technical architecture and integration points
  - Code references and patterns to follow
  - Testing strategy and success criteria

**Usage:**
```bash
/create-plan requirements/my-feature.md
```

#### 2. Execute Plan (`/execute-plan`)

Execute implementation plans with integrated Archon task management and validation.

**What it does:**
- Reads your implementation plan
- Creates an Archon project and tasks automatically
- Implements each task systematically (`todo` → `doing` → `review` → `done`)
- Validates with the `validator` subagent to create unit tests
- Tracks progress throughout with full visibility

**Usage:**
```bash
/execute-plan PRPs/my-feature.md
```

### Quality Assurance Workflows

#### 3. Code Review (`/review-code`)

Perform pragmatic code quality review on changes before committing or creating PRs.

**What it does:**
- Analyzes code changes across 7 quality dimensions
- Searches Archon knowledge base for project-specific standards
- Uses `code-reviewer` subagent for structured feedback
- Categorizes findings: Critical, High Priority, Medium Priority
- Focuses on high-impact improvements (not nitpicks)

**Quality dimensions:**
1. Architectural Design & Integrity
2. Functionality & Correctness
3. Security
4. Maintainability & Readability
5. Testing Strategy
6. Performance & Scalability
7. Dependencies & Documentation

**Usage:**
```bash
/review-code                    # Review uncommitted changes
/review-code <commit-hash>      # Review specific commit
/review-code main...HEAD        # Review branch changes
```

#### 4. Security Review (`/security-review`)

Conduct focused security vulnerability audit with OWASP-based scanning.

**What it does:**
- Scans for OWASP Top 10 vulnerabilities
- Uses `security-auditor` subagent for high-confidence findings (>80%)
- Provides concrete exploit scenarios and remediation code
- Searches Archon for project security standards
- Creates severity-based reports (Critical, High, Medium)

**Categories scanned:**
- Input Validation (SQL injection, Command injection, Path traversal, XXE)
- Authentication & Authorization
- Cryptography & Secrets Management
- Injection & Code Execution (RCE, XSS, deserialization)
- Data Exposure (sensitive logging, IDOR, API leakage)

**Usage:**
```bash
/security-review                # Audit uncommitted changes
/security-review <commit-hash>  # Audit specific commit
/security-review main...HEAD    # Audit branch changes
```

#### 5. Design Review (`/design-review`)

Perform comprehensive UI/UX quality review on frontend changes.

**What it does:**
- Reviews across 7 design phases (see below)
- Uses `design-reviewer` subagent for accessibility and UX feedback
- Validates WCAG 2.1 AA compliance
- Checks responsive design (desktop, tablet, mobile)
- Ensures design system consistency

**Review phases:**
1. Interaction & User Flow
2. Responsiveness (1440px, 768px, 375px)
3. Visual Polish (spacing, typography, colors)
4. Accessibility (WCAG 2.1 AA)
5. Robustness (empty states, loading, errors)
6. Code Health (component reuse, design tokens)
7. Content & Console (clear labels, no errors)

**Usage:**
```bash
/design-review                  # Review UI changes
/design-review src/components/* # Review specific components
```

## Why Archon?

[Archon](https://github.com/coleam00/Archon) is an open-source AI coding OS that provides:

- **Knowledge Base**: RAG-powered search across documentation, PDFs, and crawled websites
- **Task Management**: Hierarchical projects with AI-assisted task creation and tracking
- **Smart Search**: Hybrid search with contextual embeddings and reranking
- **Multi-Agent Support**: Connect multiple AI assistants to shared context
- **Model Context Protocol**: Standard MCP server for seamless integration

Think of it as the command center that keeps your AI coding assistant informed and organized.

## What's Included

```
.claude/
├── commands/
│   ├── create-plan.md       # Requirements → Implementation plan
│   ├── execute-plan.md      # Plan → Tracked implementation
│   ├── review-code.md       # Code quality review workflow
│   ├── security-review.md   # Security vulnerability audit
│   ├── design-review.md     # UI/UX quality review
│   └── primer.md            # Project context loader
├── agents/
│   ├── codebase-analyst.md  # Pattern analysis specialist
│   ├── validator.md         # Testing specialist
│   ├── code-reviewer.md     # Code quality reviewer
│   ├── security-auditor.md  # Security vulnerability scanner
│   └── design-reviewer.md   # UI/UX design reviewer
├── CLAUDE.md                # Archon-first workflow rules
└── README.md                # This file
```

## Setup Instructions

### For Claude Code

1. **Copy the template to your project:**
   ```bash
   cp -r use-cases/archon-example-workflow/.claude /path/to/your-project/
   ```

2. **Install Archon MCP server** (if not already installed):
   - Follow instructions at [github.com/coleam00/Archon](https://github.com/coleam00/Archon)
   - Configure in your Claude Code settings

3. **Start using workflows:**
   ```bash
   # In Claude Code
   /create-plan requirements/your-feature.md
   # Review the generated plan, then:
   /execute-plan PRPs/your-feature.md
   ```

### For Other AI Assistants

The workflows are just markdown prompt templates - adapt them to your tool - examples:

#### **Cursor / Windsurf**
- Copy files to `.cursor/` or `.windsurf/` directory
- Use as custom commands or rules files
- Manually invoke workflows by copying prompt content

#### **Cline / Aider / Continue.dev**
- Save workflows as prompt templates
- Reference them in your session context
- Adapt the MCP tool calls to your tool's API

#### **Generic Usage**
Even without tool-specific integrations:
1. Read `create-plan.md` and follow its steps manually
2. Use Archon's web UI for task management if MCP isn't available
3. Adapt the workflow structure to your assistant's capabilities

## Workflow in Action

### New Project Example

```bash
# 1. Write requirements
echo "Build a REST API for user authentication" > requirements/auth-api.md

# 2. Create plan
/create-plan requirements/auth-api.md
# → AI searches Archon knowledge base for JWT best practices
# → AI analyzes your codebase patterns
# → Generates PRPs/auth-api.md with 12 tasks

# 3. Execute plan
/execute-plan PRPs/auth-api.md
# → Creates Archon project "Authentication API"
# → Creates 12 tasks in Archon
# → Implements task-by-task with status tracking
# → Runs validator subagent for unit tests
# → Marks tasks done as they complete
```

### Existing Project Example

```bash
# 1. Create feature requirements
# 2. Run create-plan (it analyzes existing codebase)
/create-plan requirements/new-feature.md
# → Discovers existing patterns from your code
# → Suggests integration points
# → Follows your project's conventions

# 3. Execute with existing Archon project
# Edit execute-plan.md to reference project ID or let it create new one
/execute-plan PRPs/new-feature.md
```

## Key Benefits

### For New Projects
- **Pattern establishment**: AI learns and documents your conventions
- **Structured foundation**: Plans prevent scope creep and missed requirements
- **Knowledge integration**: Leverage best practices from day one

### For Existing Projects
- **Convention adherence**: Codebase analysis ensures consistency
- **Incremental enhancement**: Add features that fit naturally
- **Context retention**: Archon keeps project history and patterns

## Customization

### Adapt the Workflows

Edit the markdown files to match your needs - examples:

- **Change task granularity** in `create-plan.md` (Step 3.1)
- **Add custom validation** in `execute-plan.md` (Step 6)
- **Modify report format** in either workflow
- **Add your own subagents** for specialized tasks

### Extend with Subagents

Create new specialized agents in `.claude/agents/`:

```markdown
---
name: "performance-auditor"
description: "Reviews code for performance issues"
tools: Read, Grep, Bash
color: yellow
---

You are a performance specialist who reviews code for...
```

Then reference in your workflows using the Task tool.

## Complete Workflow Examples

### Full Development Cycle with Quality Assurance

```bash
# 1. Plan the feature
/create-plan requirements/new-dashboard.md
# → Generates PRPs/new-dashboard.md with tasks

# 2. Implement the feature
/execute-plan PRPs/new-dashboard.md
# → Creates project, implements tasks, validates with tests

# 3. Review code quality
/review-code
# → Identifies issues across 7 quality dimensions

# 4. Fix any issues found, then run security audit
/security-review
# → Scans for vulnerabilities (OWASP Top 10)

# 5. For frontend features, run design review
/design-review
# → Validates UI/UX, accessibility, responsiveness

# 6. Commit and create PR with confidence!
git add .
git commit -m "Add new dashboard with full quality checks"
```

### Quick Quality Check Before PR

```bash
# Run all three reviews in sequence
/review-code && /security-review && /design-review

# Or run specific review based on change type:
/review-code         # For backend/logic changes
/security-review     # For authentication/data handling
/design-review       # For UI components
```

## Quality Assurance Best Practices

### When to Use Each Review

**Code Review** (`/review-code`):
- After implementing any feature
- Before committing to main branch
- When refactoring existing code
- For all pull requests

**Security Review** (`/security-review`):
- When handling user input
- For authentication/authorization code
- When working with sensitive data
- For API endpoints
- Before deploying to production

**Design Review** (`/design-review`):
- After implementing UI components
- Before finalizing user-facing features
- When updating styles or layouts
- For accessibility compliance checks
- Before design handoff or stakeholder review

### Integration with Archon Task Management

All review workflows can automatically create Archon tasks for findings:

```bash
# After review completes, Claude Code will ask:
"Would you like me to create Archon tasks for the [critical/high-priority] findings?"

# If yes, tasks are created with:
- Proper severity tagging
- Detailed descriptions
- Remediation recommendations
- Links to relevant code
```

Track and manage review findings alongside your development tasks in Archon.
