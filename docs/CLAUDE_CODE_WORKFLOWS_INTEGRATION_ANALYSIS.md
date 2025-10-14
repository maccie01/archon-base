# Claude Code Workflows Integration Analysis for Archon

**Date**: October 13, 2025
**Source Repository**: https://github.com/OneRedOak/claude-code-workflows
**Purpose**: Analyze how to integrate automated code review, security review, and design review workflows into Archon as MCP-accessible agents

---

## Executive Summary

The claude-code-workflows repository contains three sophisticated AI-powered review workflows (Code Review, Security Review, Design Review) that are currently implemented as Claude Code slash commands and GitHub Actions. These workflows represent **missing critical functionality** in Archon that would significantly enhance its value as a development coordination platform.

**Key Finding**: Archon currently has **no built-in code quality assurance agents**. Integrating these workflows would position Archon as a comprehensive development command center with automated quality gates.

---

## Repository Overview

### Three Core Workflows

1. **Code Review Workflow** - Pragmatic code quality analysis
   - Focuses on architecture, security, maintainability, testing, performance
   - Uses "Pragmatic Quality" framework (net positive > perfection)
   - Prioritized findings (Critical/Blocker, Improvement, Nit)

2. **Security Review Workflow** - OWASP-based vulnerability scanning
   - Focuses on high-confidence exploitable vulnerabilities
   - Covers OWASP Top 10, secret detection, crypto issues
   - Includes sophisticated false-positive filtering

3. **Design Review Workflow** - UI/UX quality assurance
   - Uses Playwright for live environment testing
   - Covers accessibility (WCAG 2.1 AA), responsiveness, visual polish
   - Multi-phase systematic review process

---

## Analysis by Workflow

## 1. Code Review Workflow

### Current Implementation (claude-code-workflows)

**Architecture**:
- **Slash Command**: `/review` - triggers on-demand code review
- **Subagent**: `pragmatic-code-review` - isolated review agent
- **GitHub Action**: Automated PR reviews

**Key Features**:
- Hierarchical review framework (7 priority levels)
- Pragmatic Quality philosophy (net positive > perfection)
- Grounded in engineering principles (SOLID, DRY, KISS, YAGNI)
- Triaged findings (Critical, Improvement, Nit)
- Context-aware (analyzes git diff, understands existing patterns)

**Review Categories**:
1. Architectural Design & Integrity (Critical)
2. Functionality & Correctness (Critical)
3. Security (Non-Negotiable)
4. Maintainability & Readability (High Priority)
5. Testing Strategy & Robustness (High Priority)
6. Performance & Scalability (Important)
7. Dependencies & Documentation (Important)

### What Archon is Missing

**Current State**:
- ❌ No code review capabilities
- ❌ No code quality analysis
- ❌ No automated PR review
- ❌ No standards enforcement

**Gap Analysis**:
- Archon has RAG search for patterns but no analysis/review engine
- Archon tracks tasks but doesn't validate code quality
- Archon stores knowledge but doesn't apply it to review code
- No integration with git workflows or PR processes

### Archon Integration Approach

**Option 1: MCP Agent for Code Review** (Recommended)

Create new MCP tool: `archon:review_code`

```typescript
{
  "tool": "archon:review_code",
  "arguments": {
    "diff": "git diff content",
    "review_type": "pragmatic",  // or "strict", "fast"
    "focus_areas": ["security", "architecture", "testing"],
    "project_id": "optional-for-project-specific-standards",
    "save_report": true  // Save to project documents
  }
}
```

**Implementation Requirements**:

1. **New Agent Service** (`python/src/agents/features/code_review/`):
   ```
   code_review/
   ├── __init__.py
   ├── code_review_agent.py      # PydanticAI agent
   ├── review_frameworks.py      # Pragmatic, strict, fast
   ├── finding_classifier.py     # Severity and category
   └── report_generator.py       # Markdown reports
   ```

2. **New MCP Tool** (`python/src/mcp_server/features/code_review/`):
   ```
   code_review/
   ├── __init__.py
   └── code_review_tools.py      # MCP tool implementation
   ```

3. **Knowledge Base Integration**:
   - Search project-specific coding standards from Archon knowledge base
   - Reference architectural patterns for consistency checking
   - Use code examples for pattern matching

4. **Project Integration**:
   - Link code review reports to project documents
   - Create tasks for critical/high-priority findings
   - Track fix progress via task status updates

**Workflow**:
```
Developer: "Review my auth module changes"

Claude Code via MCP:
1. archon:review_code(diff=git_diff, project_id="netzwaechter")
2. Archon agent:
   - Searches knowledge base for "netzwaechter coding standards"
   - Analyzes diff against standards
   - Generates pragmatic review report
3. archon:manage_document(action="create", content=report)
4. archon:manage_task for critical findings
5. Returns: Markdown report + task IDs
```

**Benefits**:
- Leverages existing Archon knowledge base
- Integrates with project/task management
- Can reference project-specific standards
- Provides audit trail via document versions

---

## 2. Security Review Workflow

### Current Implementation

**Architecture**:
- **Slash Command**: `/security-review` - on-demand security scanning
- **GitHub Action**: Automated PR security checks
- **Source**: From Anthropic's [claude-code-security-review](https://github.com/anthropics/claude-code-security-review)

**Key Features**:
- OWASP Top 10 coverage
- High-confidence vulnerability detection (>80% exploitability)
- Sophisticated false-positive filtering
- Severity classification (High, Medium, Low)
- Detailed exploit scenarios and remediation

**Security Categories**:
1. Input Validation (SQL, Command, XXE, Template, NoSQL injection)
2. Authentication & Authorization (bypass, privilege escalation)
3. Crypto & Secrets (hardcoded keys, weak crypto)
4. Injection & Code Execution (RCE, deserialization, XSS)
5. Data Exposure (PII, logging, API leakage)

**Analysis Methodology**:
- Phase 1: Repository context research
- Phase 2: Comparative analysis (new vs existing patterns)
- Phase 3: Vulnerability assessment (data flow tracing)

### What Archon is Missing

**Current State**:
- ❌ No security scanning capabilities
- ❌ No vulnerability detection
- ❌ No secret detection
- ❌ No OWASP-based analysis
- ❌ No security-focused code review

**Gap Analysis**:
- Archon could store security policies in knowledge base but has no enforcement
- No integration with security frameworks or vulnerability databases
- No automated security checks in refactoring workflows
- Critical gap for production-ready code

### Archon Integration Approach

**Option 1: MCP Agent for Security Review** (Recommended)

Create new MCP tool: `archon:security_review`

```typescript
{
  "tool": "archon:security_review",
  "arguments": {
    "diff": "git diff content",
    "severity_threshold": "medium",  // Only report medium+
    "categories": ["injection", "auth", "crypto", "data_exposure"],
    "project_id": "optional",
    "save_findings": true
  }
}
```

**Implementation Requirements**:

1. **New Agent Service** (`python/src/agents/features/security_review/`):
   ```
   security_review/
   ├── __init__.py
   ├── security_review_agent.py   # PydanticAI agent
   ├── vulnerability_scanner.py   # OWASP checkers
   ├── false_positive_filter.py   # Confidence scoring
   ├── exploit_analyzer.py        # Exploit scenario generator
   └── remediation_guide.py       # Fix recommendations
   ```

2. **New MCP Tool** (`python/src/mcp_server/features/security_review/`):
   ```
   security_review/
   ├── __init__.py
   └── security_review_tools.py
   ```

3. **Knowledge Base Integration**:
   - Store security policies and threat models
   - Reference secure coding patterns from knowledge base
   - Learn from past security findings

4. **Task Auto-Creation**:
   - Auto-create high-severity security tasks
   - Assign to security team or specific developers
   - Block merges until security tasks resolved

**Workflow**:
```
Developer: "Run security scan on my changes"

Claude Code via MCP:
1. archon:security_review(diff=git_diff, severity_threshold="high")
2. Archon agent:
   - Scans for OWASP Top 10 vulnerabilities
   - Filters false positives with confidence scoring
   - Generates exploit scenarios
3. For each HIGH finding:
   - archon:manage_task(action="create", title="[Security] SQL Injection in auth.ts")
4. archon:manage_document(action="create", content=security_report)
5. Returns: Findings report + critical task IDs
```

**Benefits**:
- Proactive security before code reaches production
- Consistent security standards across all projects
- Audit trail of security findings and fixes
- Integration with Archon's task tracking

---

## 3. Design Review Workflow

### Current Implementation

**Architecture**:
- **Slash Command**: `/design-review` - UI/UX review
- **Subagent**: `design-review` - specialized design agent
- **Playwright MCP Integration**: Live environment testing

**Key Features**:
- Live UI testing (not just static code analysis)
- Multi-phase systematic review (7 phases)
- WCAG 2.1 AA accessibility compliance
- Responsive design testing (desktop/tablet/mobile)
- Visual evidence via screenshots
- World-class standards (Stripe, Airbnb, Linear)

**Review Phases**:
0. Preparation (setup preview environment)
1. Interaction & User Flow (test primary flows)
2. Responsiveness Testing (3 viewport sizes)
3. Visual Polish (spacing, typography, color)
4. Accessibility (WCAG AA, keyboard navigation)
5. Robustness Testing (edge cases, error states)
6. Code Health (component reuse, design tokens)
7. Content & Console (grammar, errors)

**Output Format**:
- Triaged findings (Blocker, High-Priority, Medium-Priority, Nitpick)
- Screenshots for visual issues
- "Problems over prescriptions" philosophy

### What Archon is Missing

**Current State**:
- ❌ No design review capabilities
- ❌ No UI/UX analysis
- ❌ No accessibility testing
- ❌ No visual consistency checking
- ❌ No browser automation integration

**Gap Analysis**:
- Archon has no frontend-specific review capabilities
- No integration with browser automation (Playwright)
- Could store design systems in knowledge base but no enforcement
- Missing critical piece for frontend-heavy projects like Netzwächter

### Archon Integration Approach

**Option 1: MCP Agent for Design Review** (Recommended)

Create new MCP tool: `archon:design_review`

```typescript
{
  "tool": "archon:design_review",
  "arguments": {
    "preview_url": "http://localhost:3000",
    "pages_to_test": ["/login", "/dashboard"],
    "viewports": ["desktop", "tablet", "mobile"],
    "focus_areas": ["accessibility", "responsiveness", "visual_polish"],
    "project_id": "optional-for-design-system-reference",
    "save_screenshots": true
  }
}
```

**Implementation Requirements**:

1. **New Agent Service** (`python/src/agents/features/design_review/`):
   ```
   design_review/
   ├── __init__.py
   ├── design_review_agent.py     # PydanticAI agent
   ├── accessibility_checker.py   # WCAG compliance
   ├── visual_analyzer.py         # Layout, typography, color
   ├── responsive_tester.py       # Multi-viewport testing
   └── playwright_controller.py   # Browser automation
   ```

2. **New MCP Tool** (`python/src/mcp_server/features/design_review/`):
   ```
   design_review/
   ├── __init__.py
   └── design_review_tools.py
   ```

3. **Playwright Integration**:
   - Add Playwright as dependency (already Python library)
   - Create browser automation helpers
   - Screenshot storage in Supabase or local storage
   - Accessibility tree analysis

4. **Knowledge Base Integration**:
   - Store design system and brand guidelines
   - Reference UI component library patterns
   - Learn from past design reviews

5. **Document Storage**:
   - Save review reports with embedded screenshots
   - Link to project documentation
   - Version control for design iterations

**Workflow**:
```
Developer: "Review the new dashboard UI"

Claude Code via MCP:
1. archon:design_review(
     preview_url="http://localhost:3737",
     pages=["/dashboard"],
     project_id="netzwaechter"
   )
2. Archon agent:
   - Launches Playwright browser
   - Tests desktop/tablet/mobile viewports
   - Captures screenshots at each viewport
   - Checks WCAG accessibility
   - Analyzes visual hierarchy
   - Tests keyboard navigation
3. archon:manage_document(
     action="create",
     content=report_with_screenshots
   )
4. For each Blocker:
   - archon:manage_task(action="create", priority="high")
5. Returns: Design review report + task IDs + screenshot URLs
```

**Benefits**:
- Catch UI issues before they reach users
- Ensure accessibility compliance (legal requirement)
- Maintain consistent design across features
- Objective, automated design standards enforcement

**Note**: Requires running preview environment (e.g., `npm run dev`)

---

## Cross-Cutting Integration Requirements

### 1. Agent Service Infrastructure

**Location**: `python/src/agents/features/`

**New Structure**:
```
agents/features/
├── code_review/
│   ├── __init__.py
│   ├── code_review_agent.py
│   └── ...
├── security_review/
│   ├── __init__.py
│   ├── security_review_agent.py
│   └── ...
├── design_review/
│   ├── __init__.py
│   ├── design_review_agent.py
│   └── ...
└── shared/
    ├── report_formatter.py      # Markdown report generation
    ├── finding_classifier.py    # Severity/priority classification
    └── knowledge_integration.py # RAG search integration
```

### 2. MCP Server Extensions

**Location**: `python/src/mcp_server/features/`

**New Tools**:
```python
# MCP tool registration in each feature's __init__.py

@mcp.tool()
async def review_code(
    ctx: Context,
    diff: str,
    review_type: str = "pragmatic",
    focus_areas: list[str] | None = None,
    project_id: str | None = None,
    save_report: bool = True
) -> str:
    """
    Perform comprehensive code review on git diff.

    Returns JSON:
    {
      "success": bool,
      "report": str (markdown),
      "findings": [
        {"severity": "critical", "category": "security", "description": "..."}
      ],
      "tasks_created": [task_ids],
      "document_id": str
    }
    """

@mcp.tool()
async def security_review(
    ctx: Context,
    diff: str,
    severity_threshold: str = "medium",
    categories: list[str] | None = None,
    project_id: str | None = None
) -> str:
    """
    Perform security-focused vulnerability scan.

    Returns JSON with vulnerabilities, exploit scenarios, remediation
    """

@mcp.tool()
async def design_review(
    ctx: Context,
    preview_url: str,
    pages_to_test: list[str],
    viewports: list[str] = ["desktop", "tablet", "mobile"],
    focus_areas: list[str] | None = None,
    project_id: str | None = None
) -> str:
    """
    Perform UI/UX design review with browser automation.

    Returns JSON with findings, screenshots, accessibility issues
    """
```

### 3. Knowledge Base Integration

**Pattern**: All review agents should search Archon knowledge base for context

**Examples**:

**Code Review**:
- Search: "coding standards", "architectural patterns"
- Use: Compare new code against established patterns
- Benefit: Project-specific review criteria

**Security Review**:
- Search: "security policies", "threat model", "secure patterns"
- Use: Understand security requirements
- Benefit: Context-aware vulnerability detection

**Design Review**:
- Search: "design system", "brand guidelines", "UI components"
- Use: Check consistency with design standards
- Benefit: Automated design system enforcement

**Implementation**:
```python
# In each agent

from src.server.services.search.rag_service import RAGService

async def get_project_standards(project_id: str, category: str):
    """Fetch project-specific standards from knowledge base."""
    rag = RAGService(supabase_client)
    success, results = await rag.perform_rag_query(
        query=f"{category} standards patterns",
        source=f"project_{project_id}",
        match_count=5
    )
    return results.get("results", [])
```

### 4. Task Auto-Creation

**Pattern**: Critical findings automatically create tasks

**Implementation**:
```python
from src.server.services.task_service import TaskService

async def create_finding_tasks(findings: list, project_id: str):
    """Auto-create tasks for critical/high findings."""
    task_service = TaskService(supabase_client)
    created_tasks = []

    for finding in findings:
        if finding["severity"] in ["critical", "high"]:
            task = await task_service.create_task({
                "project_id": project_id,
                "title": f"[{finding['category']}] {finding['title']}",
                "description": finding["description"],
                "status": "todo",
                "assignee": "team",
                "priority": finding["severity"],
                "metadata": {
                    "finding_type": finding["category"],
                    "source": "automated_review"
                }
            })
            created_tasks.append(task["id"])

    return created_tasks
```

### 5. Document Storage

**Pattern**: Save review reports as project documents

**Implementation**:
```python
from src.server.services.document_service import DocumentService

async def save_review_report(
    report: str,
    project_id: str,
    review_type: str,
    metadata: dict
):
    """Save review report as project document."""
    doc_service = DocumentService(supabase_client)

    doc = await doc_service.create_document({
        "project_id": project_id,
        "title": f"{review_type} Review - {metadata.get('date')}",
        "content": report,
        "doc_type": "review_report",
        "metadata": {
            "review_type": review_type,
            "findings_count": metadata.get("findings_count"),
            "severity_breakdown": metadata.get("severity_breakdown"),
            **metadata
        }
    })

    return doc["id"]
```

---

## Implementation Phases

### Phase 1: Code Review Agent (Weeks 1-2)

**Priority**: High - Most universal need

**Tasks**:
1. Create agent service (`agents/features/code_review/`)
2. Implement pragmatic review framework
3. Create MCP tool (`archon:review_code`)
4. Integrate with knowledge base for standards
5. Test with Netzwächter codebase
6. Document usage in ARCHON_CAPABILITIES_REFERENCE.md

**Deliverables**:
- Working MCP tool `archon:review_code`
- Agent generates structured markdown reports
- Findings classified by severity
- Integration with project documents
- Auto-create tasks for critical findings

### Phase 2: Security Review Agent (Weeks 2-3)

**Priority**: High - Security is non-negotiable

**Tasks**:
1. Create agent service (`agents/features/security_review/`)
2. Implement OWASP-based vulnerability scanners
3. Build false-positive filtering
4. Create MCP tool (`archon:security_review`)
5. Integrate with knowledge base for security policies
6. Test with common vulnerability patterns

**Deliverables**:
- Working MCP tool `archon:security_review`
- OWASP Top 10 coverage
- High-confidence vulnerability detection
- Exploit scenarios and remediation guidance
- Auto-create security tasks

### Phase 3: Design Review Agent (Weeks 3-4)

**Priority**: Medium - Frontend-specific but high value

**Tasks**:
1. Add Playwright dependency
2. Create agent service (`agents/features/design_review/`)
3. Implement browser automation
4. Build accessibility checker (WCAG)
5. Create responsive testing
6. Create MCP tool (`archon:design_review`)
7. Test with Netzwächter frontend

**Deliverables**:
- Working MCP tool `archon:design_review`
- Multi-viewport testing
- Accessibility compliance checking
- Screenshot capture and storage
- Design consistency enforcement

### Phase 4: Integration & Polish (Week 4)

**Tasks**:
1. Create unified review dashboard in Archon UI
2. Add review metrics and analytics
3. Implement review history tracking
4. Create slash command templates for Claude Code
5. Write comprehensive documentation
6. Create video tutorials

**Deliverables**:
- Unified review experience
- Metrics tracking (reviews run, findings by severity, fix rates)
- Complete documentation
- Example workflows

---

## Benefits Summary

### For Individual Developers

**Without Archon Review Agents**:
- Manual code review (slow, inconsistent)
- Security issues discovered late (expensive to fix)
- UI inconsistencies slip through
- No enforcement of standards

**With Archon Review Agents**:
- Instant code review feedback
- Security vulnerabilities caught before commit
- UI/UX issues detected in development
- Automated standards enforcement
- Learning from AI feedback

### For Teams (Multi-Agent Netzwächter Refactor)

**Scenario**: 5 Claude Code agents refactoring 457 files in parallel

**Without Review Agents**:
- Each agent might introduce different patterns
- Security vulnerabilities only found in manual review
- UI inconsistencies across modules
- Significant integration issues during merge

**With Archon Review Agents**:
```
Workflow per agent:
1. Refactor file(s)
2. archon:review_code - ensures consistency with standards
3. archon:security_review - catches vulnerabilities immediately
4. archon:design_review (if UI change) - maintains design consistency
5. Commit only if all reviews pass
6. Auto-created tasks for any critical findings
```

**Result**:
- All 457 files follow same patterns (fetched from Archon knowledge base)
- Zero security vulnerabilities slip through
- Consistent UI/UX across all modules
- Smooth integration (no surprises during merge)
- Complete audit trail of reviews

### For Archon Platform

**Current State**:
- Knowledge base (passive reference)
- Task management (manual tracking)
- MCP integration (basic CRUD operations)

**With Review Agents**:
- Knowledge base → Active standards enforcement
- Task management → Auto-populated from findings
- MCP integration → Intelligent code quality gates
- New value proposition: "Development command center with automated quality assurance"

---

## Technical Considerations

### 1. Performance

**Challenge**: Code review can be slow with large diffs

**Solution**:
- Chunk large diffs into smaller pieces
- Parallel analysis of independent files
- Cache analysis results for unchanged files
- Stream findings as they're discovered (don't wait for complete analysis)

### 2. Model Selection

**Code Review**: Sonnet (balance of speed and quality)
**Security Review**: Opus (higher accuracy for critical findings)
**Design Review**: Sonnet (sufficient for visual analysis)

### 3. Cost Management

**OpenAI Costs**:
- Code review: ~$0.01-0.05 per review (depending on diff size)
- Security review: ~$0.02-0.10 per review (more thorough)
- Design review: ~$0.03-0.10 per review (multiple viewports)

**Ollama Alternative** (Free):
- Use Ollama for code/security review (qwen2.5-coder:7b)
- Slightly lower quality but zero cost
- Good for frequent reviews during development

### 4. Browser Automation Dependencies

**Design Review Only**:
- Add Playwright to Python dependencies
- Requires preview environment running
- Screenshot storage strategy (Supabase storage or local)

### 5. Git Integration

**All Reviews**:
- Need git diff access
- Consider integrating with GitHub/GitLab APIs for PR comments
- Support for local changes (unstaged/staged)

---

## Comparison to Existing Archon Capabilities

| Capability | Current Archon | With Review Agents |
|------------|----------------|-------------------|
| **Code Analysis** | ❌ None | ✅ Comprehensive review |
| **Security Scanning** | ❌ None | ✅ OWASP-based scanning |
| **Design Review** | ❌ None | ✅ Automated UI/UX review |
| **Standards Enforcement** | ⚠️ Passive (KB only) | ✅ Active enforcement |
| **Quality Gates** | ❌ None | ✅ Pre-commit checks |
| **Finding Tracking** | ⚠️ Manual tasks | ✅ Auto-created tasks |
| **Audit Trail** | ⚠️ Limited | ✅ Complete review history |

---

## Alternative Integration Approaches

### Option 2: Slash Command Templates (Simpler but less integrated)

**Approach**: Provide slash command templates that users add to their projects

**Pros**:
- Faster to implement (no Archon code changes)
- Works immediately with existing Claude Code
- Users can customize for their needs

**Cons**:
- No integration with Archon knowledge base
- No automatic task creation
- No review history tracking
- No centralized metrics

**Recommendation**: Start with this for rapid testing, then migrate to full MCP integration

### Option 3: GitHub Actions Only (CI/CD focused)

**Approach**: Provide GitHub Actions workflows instead of MCP tools

**Pros**:
- Automated on every PR
- No manual triggering needed
- Standard CI/CD integration

**Cons**:
- Only works at PR time (not during development)
- No inner-loop feedback
- No integration with Archon features

**Recommendation**: Complement MCP tools with GitHub Actions for outer-loop

---

## Recommended Implementation Strategy

### Short-term (Weeks 1-2): Validate Value

1. Create slash command templates (no Archon changes)
2. Test with Netzwächter project
3. Gather feedback on usefulness
4. Validate business case for full integration

### Medium-term (Weeks 3-6): MCP Integration

1. Implement Phase 1 (Code Review Agent)
2. Test with multi-agent Netzwächter refactor
3. Measure impact on code quality
4. Implement Phase 2 (Security Review Agent)

### Long-term (Weeks 7-8): Complete Platform

1. Implement Phase 3 (Design Review Agent)
2. Add review dashboard to Archon UI
3. Integrate with GitHub/GitLab for PR comments
4. Create comprehensive documentation and tutorials

---

## Success Metrics

### Developer Experience
- Time to get code review feedback: <5 minutes (vs hours for human review)
- False positive rate: <20% (high signal-to-noise)
- Developer satisfaction: >80% find reviews helpful

### Code Quality
- Security vulnerabilities detected: Track count and severity
- Design issues caught: Track accessibility and visual consistency issues
- Standards adherence: % of code following project patterns

### Business Impact
- Cost savings: Human review time reduced by 60%+
- Faster development: Review feedback in inner loop vs outer loop
- Higher quality: Fewer bugs reaching production

---

## Conclusion

**Summary**: The claude-code-workflows repository contains three **missing critical capabilities** for Archon:

1. **Code Review** - Systematic quality analysis
2. **Security Review** - Vulnerability detection
3. **Design Review** - UI/UX quality assurance

**Integration Approach**: Create MCP tools backed by PydanticAI agents that leverage Archon's knowledge base for context-aware reviews.

**Timeline**: 4-8 weeks for full implementation across 3 phases.

**Impact**: Transforms Archon from a passive knowledge base into an **active development quality assurance platform** that enforces standards, detects issues early, and maintains consistency across parallel development efforts.

**Next Step**: Create detailed implementation tasks and begin Phase 1 (Code Review Agent).

---

**Document Version**: 1.0
**Status**: Analysis Complete - Ready for Implementation Planning
