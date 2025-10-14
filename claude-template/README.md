# Claude Template System

A comprehensive system for creating, analyzing, and improving CLAUDE.md files for AI-assisted development with Archon MCP integration.

## Overview

This directory contains agents, workflows, and research for optimizing CLAUDE.md templates that guide AI coding assistants (Claude Code, Cursor, Windsurf) in software development projects.

## Directory Structure

```
claude-template/
├── README.md                           # This file
├── research/                           # Research documents
│   ├── claude-1.md                    # Agent workflows (frontend/backend specialization)
│   └── claude-2.md                    # Context engineering and token budgeting
├── .claude/
│   ├── agents/                        # Specialized analysis agents
│   │   ├── claude-template-analyzer.md    # Quality analysis agent
│   │   └── claude-template-synthesizer.md # Template generation agent
│   └── commands/                      # Workflow commands
│       └── analyze-claude-template.md     # Analysis workflow
└── templates/                         # (To be generated)
    ├── base-template.md              # Minimal starting template
    ├── frontend-template.md          # React/Vue/Angular specialized
    ├── backend-template.md           # API/Service specialized
    └── full-stack-template.md        # Combined frontend + backend
```

## Components

### 1. Analysis Agent (`claude-template-analyzer`)

Comprehensive quality analyzer for CLAUDE.md files.

**Evaluates**:
- Core requirements (Archon-first rules, MCP tools, task workflow)
- Pattern quality (concrete examples, clear structure)
- Archon integration completeness
- AI optimization (clarity, actionability, examples)
- Gap identification

**Output**: Detailed analysis report with ratings, gaps, and improvement recommendations

### 2. Synthesis Agent (`claude-template-synthesizer`)

Template generation agent that combines best practices from research.

**Capabilities**:
- Integrates token budget allocation strategies
- Applies frontend/backend specialization patterns
- Ensures Archon MCP integration
- Generates project-specific customizations
- Validates against best practices

**Output**: Production-ready CLAUDE.md templates

### 3. Analysis Workflow Command

`/analyze-claude-template` - Complete analysis pipeline

**Usage**:
```bash
# Analyze current CLAUDE.md
/analyze-claude-template

# Analyze specific file
/analyze-claude-template path/to/CLAUDE.md
```

**Generates**: `claude-template-analysis.md` with comprehensive findings

## Research Insights

### Token Budget Strategy (from claude-2.md)

Total budget: ~180K tokens (reserve 20K for code context)

**Allocation**:
- Workflows & MCP config: ~55K tokens (30%)
- Coding standards & rules: ~40K tokens (22%)
- Agent roles: ~12K tokens (7%)
- Architecture decisions: ~20K tokens (11%)
- Project overview: ~10K tokens (6%)
- External references: ~1K tokens (1%)

### Agent Specialization (from claude-1.md)

**Frontend Agents**:
- UI Component Builder
- State Management Specialist
- Accessibility Validator

**Backend Agents**:
- API Endpoint Developer
- Database Schema Architect
- Business Logic Implementer
- Integration Specialist

**Quality Gates**:
- Visual regression testing
- Accessibility audits (WCAG 2.1 AA)
- Performance budgets
- Security scanning

## Best Practices

### 1. Structure

- YAML frontmatter for metadata
- H2/H3 semantic headings
- Concrete examples over prose
- External links for detailed docs

### 2. Content Priority

**Include in CLAUDE.md**:
- High-level goals and context
- Agent roles and permissions
- Workflow procedures
- MCP configurations
- Coding standards summary

**Externalize**:
- Detailed architectural diagrams
- Full API specifications
- Compliance checklists
- Voluminous reference material

### 3. Archon Integration

**Mandatory Elements**:
- Archon-first override rule at top
- Complete MCP tool reference with examples
- Task-driven workflow (todo → doing → review → done)
- RAG search patterns (2-5 keywords)
- Quality gate workflows (/review-code, /security-review, /design-review)

### 4. AI Optimization

- Clarity over completeness
- Examples over explanation
- Progressive disclosure
- Command-line ready examples
- DO/DON'T patterns

## Usage Workflows

### Analyze Existing Template

```bash
cd /path/to/project
/analyze-claude-template
```

Review `claude-template-analysis.md` for findings.

### Generate New Template

Use synthesis agent:

```bash
# Invoke agent with project requirements
Task tool → claude-template-synthesizer

# Provide:
# - Project type (frontend/backend/full-stack)
# - Tech stack
# - Team size
# - Existing patterns
```

### Customize Template

1. Start with appropriate base template
2. Fill in project-specific placeholders:
   - Project name, location, tech stack
   - Archon project ID
   - Coding standards
   - Architecture notes
   - Common patterns
3. Add domain-specific agent roles if needed
4. Validate with analyzer

## Key Principles

1. **Token Efficiency** - Every token must earn its place
2. **Concrete Over Abstract** - Show don't tell
3. **Archon-First** - MCP integration is mandatory
4. **Task-Driven** - All work flows through Archon tasks
5. **Knowledge-First** - Search before implementing
6. **Quality Gates** - Review before commit

## Template Checklist

Use this to validate any CLAUDE.md:

### Critical (Must Have)
- [ ] Archon-first override rule at top
- [ ] MCP tool reference with examples
- [ ] Task-driven workflow
- [ ] RAG search patterns
- [ ] Quality gate workflows
- [ ] Project identification
- [ ] Archon project ID placeholder

### High Priority (Should Have)
- [ ] Concrete code examples
- [ ] Error recovery procedures
- [ ] Archon CLI commands
- [ ] Search query best practices
- [ ] Complete development cycle example
- [ ] Project-specific coding standards
- [ ] Architecture notes

### Medium Priority (Nice to Have)
- [ ] Testing patterns
- [ ] Deployment workflow
- [ ] Debugging procedures
- [ ] Performance considerations
- [ ] Security guidelines
- [ ] Documentation standards

### Low Priority (Optional)
- [ ] Team conventions
- [ ] Historical context
- [ ] Related projects
- [ ] Learning resources

## Integration with Archon

This template system is designed to work seamlessly with Archon:

1. **Knowledge Base**: Research docs can be added to Archon for AI reference
2. **MCP Tools**: All templates use Archon MCP tools as primary interface
3. **Task Management**: Templates enforce task-driven development
4. **Workflows**: Templates include Archon workflow commands
5. **Quality Assurance**: Review workflows integrated

## Next Steps

1. **Generate Base Templates**: Create minimal, frontend, backend, and full-stack templates
2. **Analyze Current Template**: Run analyzer on `TEMPLATE_CLAUDE.md`
3. **Create Improved Version**: Use synthesizer to generate v2.0
4. **Document Common Patterns**: Extract patterns from analysis for reuse
5. **Integrate with Archon Workflows**: Make template generation part of project creation

## Contributing

When improving this system:

1. Add new research to `research/` directory
2. Update agents with new best practices
3. Regenerate templates when significant insights emerge
4. Document patterns in this README
5. Keep token budgets up to date

## Resources

- **Archon Documentation**: `/Users/janschubert/tools/archon/PRPs/ai_docs/`
- **Current Template**: `/Users/janschubert/tools/archon/TEMPLATE_CLAUDE.md`
- **Research Sources**: `research/claude-1.md`, `research/claude-2.md`

---

**Created**: 2025-01-13
**Version**: 1.0.0
**Status**: Production Ready
