# Workflow Integration Implementation Plan

**Created**: 2025-10-13
**Purpose**: Detailed technical implementation plan for integrating Code Review, Security Review, and Design Review workflows into Archon MCP

---

## Executive Summary

This document provides the complete implementation plan for adding three critical quality assurance workflows to Archon:

1. **Code Review Agent** - Pragmatic quality analysis with 7-level hierarchy
2. **Security Review Agent** - OWASP-based vulnerability scanning with high-confidence detection
3. **Design Review Agent** - UI/UX quality with Playwright automation and WCAG compliance

All three workflows will be exposed via MCP tools, integrated with Archon's knowledge base, and support automatic task creation for critical findings.

---

## 1. Code Review Agent Implementation

### Overview
Implement a pragmatic code quality review agent that analyzes git diffs and provides structured feedback across 7 quality dimensions.

### MCP Tool Specification

```python
@mcp.tool()
async def review_code(
    ctx: Context,
    diff: str,
    review_type: str = "pragmatic",  # "pragmatic" | "strict" | "fast"
    focus_areas: list[str] | None = None,  # Filter to specific categories
    project_id: str | None = None,  # Optional project context
    save_report: bool = True,  # Save report to knowledge base
    create_tasks: bool = False,  # Auto-create tasks for critical findings
    severity_threshold: str = "high"  # "critical" | "high" | "medium" | "low"
) -> str:
    """
    Perform comprehensive code review on git diff.

    Returns markdown report with findings categorized by:
    1. Architectural Design & Integrity (Critical)
    2. Functionality & Correctness (Critical)
    3. Security (Non-Negotiable)
    4. Maintainability & Readability (High Priority)
    5. Testing Strategy & Robustness (High Priority)
    6. Performance & Scalability (Important)
    7. Dependencies & Documentation (Important)

    Each finding includes:
    - Severity: Critical | High | Medium | Low | Nitpick
    - Category: architecture | functionality | security | etc.
    - File path and line numbers
    - Problem description
    - Specific improvement recommendation
    - Code snippet (if applicable)
    """
```

### Agent Service Structure

```
agents/features/code_review/
├── __init__.py
├── code_review_agent.py           # Main PydanticAI agent
├── review_frameworks.py           # Pragmatic, strict, fast templates
├── finding_classifier.py          # Severity and category classification
├── report_generator.py            # Markdown report generation
├── context_analyzer.py            # Analyze codebase context
└── task_creator.py                # Create Archon tasks for findings
```

### Implementation Details

#### 1. Agent Configuration (`code_review_agent.py`)

```python
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field

class CodeReviewFinding(BaseModel):
    severity: Literal["critical", "high", "medium", "low", "nitpick"]
    category: Literal["architecture", "functionality", "security", "maintainability", "testing", "performance", "dependencies"]
    file_path: str
    line_numbers: str  # e.g., "42-45"
    problem: str
    recommendation: str
    code_snippet: str | None = None

class CodeReviewReport(BaseModel):
    summary: str
    findings: list[CodeReviewFinding]
    stats: dict[str, int]  # Counts by severity

code_review_agent = Agent(
    "openai:gpt-4o",  # Or claude-3-5-sonnet-20241022
    result_type=CodeReviewReport,
    system_prompt="""You are a senior software engineer conducting pragmatic code reviews.

REVIEW PHILOSOPHY:
1. Net Positive > Perfection - Focus on impactful improvements
2. Substance over style - Prioritize correctness and maintainability
3. Grounded in principles - Base feedback on established best practices

HIERARCHICAL FRAMEWORK:
1. Architectural Design (Critical)
2. Functionality & Correctness (Critical)
3. Security (Non-Negotiable)
4. Maintainability & Readability (High Priority)
5. Testing Strategy (High Priority)
6. Performance & Scalability (Important)
7. Dependencies & Documentation (Important)

CONFIDENCE THRESHOLD:
Only report findings where you are >80% confident of the issue and impact.
""",
)
```

#### 2. Review Frameworks (`review_frameworks.py`)

```python
REVIEW_FRAMEWORKS = {
    "pragmatic": {
        "focus_areas": ["architecture", "functionality", "security", "maintainability", "testing"],
        "min_severity": "medium",
        "confidence_threshold": 0.8,
        "max_findings": 20,
    },
    "strict": {
        "focus_areas": ["architecture", "functionality", "security", "maintainability", "testing", "performance", "dependencies"],
        "min_severity": "low",
        "confidence_threshold": 0.7,
        "max_findings": 50,
    },
    "fast": {
        "focus_areas": ["functionality", "security"],
        "min_severity": "high",
        "confidence_threshold": 0.9,
        "max_findings": 10,
    }
}
```

#### 3. Context Analysis (`context_analyzer.py`)

```python
async def get_project_context(project_id: str | None) -> dict[str, Any]:
    """Fetch project-specific context from knowledge base."""
    if not project_id:
        return {}

    # Query Archon knowledge base for:
    # - Project coding standards
    # - Architecture documentation
    # - Common patterns and anti-patterns
    # - Technology stack

    sources = await rag_service.get_project_sources(project_id)
    context = {
        "coding_standards": [],
        "architecture_patterns": [],
        "tech_stack": [],
    }

    for source in sources:
        if "coding" in source.tags or "standards" in source.tags:
            context["coding_standards"].append(source.summary)
        # ... more context gathering

    return context
```

#### 4. Task Creation (`task_creator.py`)

```python
async def create_tasks_for_findings(
    findings: list[CodeReviewFinding],
    project_id: str,
    severity_threshold: str
) -> list[str]:
    """Create Archon tasks for critical/high severity findings."""

    threshold_order = ["critical", "high", "medium", "low", "nitpick"]
    threshold_index = threshold_order.index(severity_threshold)

    created_task_ids = []

    for finding in findings:
        if threshold_order.index(finding.severity) <= threshold_index:
            task = await task_service.create_task({
                "project_id": project_id,
                "title": f"[Code Review] {finding.category.title()}: {finding.file_path}:{finding.line_numbers}",
                "description": f"""**Problem**: {finding.problem}

**Recommendation**: {finding.recommendation}

**Severity**: {finding.severity.upper()}
**Category**: {finding.category}
**Location**: `{finding.file_path}:{finding.line_numbers}`

{f"```\n{finding.code_snippet}\n```" if finding.code_snippet else ""}
""",
                "status": "todo",
                "assignee": "Archon",
                "tags": ["code-review", finding.severity, finding.category],
            })
            created_task_ids.append(task.task_id)

    return created_task_ids
```

### MCP Tool Implementation

```python
# python/src/mcp_server/features/code_review/code_review_tools.py

from mcp import Context
from src.agents.features.code_review.code_review_agent import code_review_agent
from src.agents.features.code_review.context_analyzer import get_project_context
from src.agents.features.code_review.task_creator import create_tasks_for_findings
from src.agents.features.code_review.report_generator import generate_markdown_report

@mcp.tool()
async def review_code(
    ctx: Context,
    diff: str,
    review_type: str = "pragmatic",
    focus_areas: list[str] | None = None,
    project_id: str | None = None,
    save_report: bool = True,
    create_tasks: bool = False,
    severity_threshold: str = "high"
) -> str:
    """Perform comprehensive code review on git diff."""

    # Get project context if available
    project_context = await get_project_context(project_id) if project_id else {}

    # Run code review agent
    result = await code_review_agent.run(
        f"""Review the following git diff:

```diff
{diff}
```

Review Type: {review_type}
Focus Areas: {', '.join(focus_areas) if focus_areas else 'All'}

Project Context:
{project_context}
""",
    )

    report = result.data

    # Generate markdown report
    markdown_report = generate_markdown_report(report, review_type)

    # Save report to knowledge base
    if save_report and project_id:
        await knowledge_service.save_document(
            content=markdown_report,
            title=f"Code Review - {datetime.now().isoformat()}",
            project_id=project_id,
            knowledge_type="review",
            tags=["code-review", review_type],
        )

    # Create tasks for critical findings
    if create_tasks and project_id:
        task_ids = await create_tasks_for_findings(
            report.findings,
            project_id,
            severity_threshold
        )
        markdown_report += f"\n\n---\n\n**Created {len(task_ids)} tasks for critical findings.**"

    return markdown_report
```

### Knowledge Base Integration

#### Schema Extensions

```sql
-- Add review-specific metadata to archon_sources
ALTER TABLE archon_sources
ADD COLUMN review_type TEXT CHECK (review_type IN ('code-review', 'security-review', 'design-review'));

ALTER TABLE archon_sources
ADD COLUMN review_metadata JSONB DEFAULT '{}';
-- Example: {"severity_counts": {"critical": 2, "high": 5}, "git_ref": "abc123"}
```

---

## 2. Security Review Agent Implementation

### Overview
Implement an OWASP-based vulnerability scanning agent with high-confidence detection (>80% exploitability) and false-positive filtering.

### MCP Tool Specification

```python
@mcp.tool()
async def security_review(
    ctx: Context,
    diff: str,
    severity_threshold: str = "medium",  # "critical" | "high" | "medium" | "low"
    categories: list[str] | None = None,  # Filter to specific vulnerability types
    project_id: str | None = None,
    save_report: bool = True,
    create_tasks: bool = True,  # Default to True for security findings
    confidence_threshold: float = 0.8  # Minimum confidence score (0-1)
) -> str:
    """
    Perform security-focused vulnerability scan on git diff.

    Scans for:
    - Input Validation (SQL injection, Command injection, XXE, Path traversal)
    - Authentication & Authorization (bypass, privilege escalation, session flaws)
    - Crypto & Secrets (hardcoded credentials, weak algorithms)
    - Injection & Code Execution (RCE, deserialization, XSS)
    - Data Exposure (sensitive logging, PII handling, API leakage)

    Returns markdown report with:
    - Vulnerability title and file location
    - Severity (Critical/High/Medium/Low)
    - Confidence score (0.7-1.0, only >0.8 reported)
    - Exploit scenario
    - Remediation recommendation
    """
```

### Agent Service Structure

```
agents/features/security_review/
├── __init__.py
├── security_review_agent.py       # Main PydanticAI agent
├── vulnerability_scanner.py       # OWASP category scanners
├── false_positive_filter.py       # Confidence scoring and filtering
├── exploit_analyzer.py            # Generate exploit scenarios
├── remediation_guide.py           # Fix recommendations
└── task_creator.py                # Create high-priority security tasks
```

### Implementation Details

#### 1. Agent Configuration (`security_review_agent.py`)

```python
from pydantic_ai import Agent
from pydantic import BaseModel, Field

class SecurityFinding(BaseModel):
    title: str
    file_path: str
    line_numbers: str
    severity: Literal["critical", "high", "medium", "low"]
    category: Literal[
        "sql_injection", "command_injection", "xxe", "path_traversal",
        "auth_bypass", "privilege_escalation", "session_flaw",
        "hardcoded_secret", "weak_crypto",
        "rce", "deserialization", "xss",
        "data_exposure", "pii_leak"
    ]
    confidence: float = Field(ge=0.7, le=1.0)
    description: str
    exploit_scenario: str
    remediation: str

class SecurityReviewReport(BaseModel):
    summary: str
    findings: list[SecurityFinding]
    stats: dict[str, int]

security_review_agent = Agent(
    "openai:gpt-4o",
    result_type=SecurityReviewReport,
    system_prompt="""You are a senior security engineer conducting focused security reviews.

OBJECTIVE:
Identify HIGH-CONFIDENCE security vulnerabilities with real exploitation potential.
This is NOT a general code review - focus ONLY on security implications.

CRITICAL INSTRUCTIONS:
1. MINIMIZE FALSE POSITIVES: Only flag issues where you're >80% confident of actual exploitability
2. AVOID NOISE: Skip theoretical issues, style concerns, or low-impact findings
3. FOCUS ON IMPACT: Prioritize vulnerabilities leading to unauthorized access, data breaches, or system compromise

HARD EXCLUSIONS (DO NOT REPORT):
- Denial of Service (DOS) vulnerabilities
- Secrets stored on disk (handled separately)
- Rate limiting concerns
- Memory safety issues in memory-safe languages (Rust, Go, etc.)
- Test files only
- Log spoofing
- SSRF that only controls path (not host/protocol)
- User-controlled content in AI prompts
- Regex injection or DOS
- Documentation security concerns
- Lack of audit logs

SECURITY CATEGORIES:
1. Input Validation: SQL injection, Command injection, XXE, Path traversal
2. Authentication & Authorization: Bypass, privilege escalation, session flaws
3. Crypto & Secrets: Hardcoded credentials, weak algorithms
4. Injection & Code Execution: RCE, deserialization, XSS
5. Data Exposure: Sensitive logging, PII leaks, API data leakage

CONFIDENCE SCORING:
- 0.9-1.0: Certain exploit path identified
- 0.8-0.9: Clear vulnerability pattern with known exploitation methods
- 0.7-0.8: Suspicious pattern requiring specific conditions
- Below 0.7: DO NOT REPORT

SEVERITY GUIDELINES:
- CRITICAL: RCE, authentication bypass, direct data breach
- HIGH: Privilege escalation, SQL injection, sensitive data exposure
- MEDIUM: Requires specific conditions but significant impact
- LOW: Defense-in-depth issues

Only report findings with confidence >= 0.8.
""",
)
```

#### 2. False Positive Filtering (`false_positive_filter.py`)

```python
async def filter_false_positives(
    findings: list[SecurityFinding],
    project_context: dict[str, Any]
) -> list[SecurityFinding]:
    """Apply multi-stage false positive filtering."""

    # Stage 1: Hard exclusions (from system prompt)
    filtered = []
    for finding in findings:
        if should_exclude(finding):
            continue
        filtered.append(finding)

    # Stage 2: Confidence threshold
    filtered = [f for f in filtered if f.confidence >= 0.8]

    # Stage 3: Context-aware filtering
    # Example: Check if input validation exists elsewhere
    # Example: Check if framework provides automatic protection (React XSS)

    # Stage 4: Exploit scenario validation
    # Run secondary agent to verify exploit path
    verified_findings = []
    for finding in filtered:
        if await verify_exploit_path(finding, project_context):
            verified_findings.append(finding)

    return verified_findings

def should_exclude(finding: SecurityFinding) -> bool:
    """Apply hard exclusion rules."""
    exclusion_keywords = [
        "denial of service",
        "rate limiting",
        "memory consumption",
        "test file",
        "log spoofing",
        "regex injection",
    ]

    desc_lower = finding.description.lower()
    for keyword in exclusion_keywords:
        if keyword in desc_lower:
            return True

    # Exclude test files
    if "test" in finding.file_path or "spec" in finding.file_path:
        return True

    # Exclude markdown files
    if finding.file_path.endswith(".md"):
        return True

    return False

async def verify_exploit_path(
    finding: SecurityFinding,
    context: dict[str, Any]
) -> bool:
    """Use secondary agent to verify exploit path exists."""

    verification_agent = Agent(
        "openai:gpt-4o",
        result_type=bool,
        system_prompt="""You are a security expert verifying exploit paths.

Given a potential security finding, determine if there is a CONCRETE, EXPLOITABLE vulnerability.

Answer TRUE only if:
1. There is a clear attack vector with untrusted input
2. The vulnerability is reachable in the application flow
3. The impact is significant (not just theoretical)
4. No existing mitigations are in place

Answer FALSE if:
- The issue is theoretical or requires unrealistic conditions
- Existing framework protections mitigate the issue
- The code is not reachable by untrusted input
- The impact is negligible
""",
    )

    result = await verification_agent.run(
        f"""Verify this security finding:

**Title**: {finding.title}
**File**: {finding.file_path}:{finding.line_numbers}
**Category**: {finding.category}
**Severity**: {finding.severity}
**Description**: {finding.description}
**Exploit Scenario**: {finding.exploit_scenario}

**Project Context**:
- Tech Stack: {context.get('tech_stack', 'Unknown')}
- Framework Protections: {context.get('security_features', [])}

Is this a CONCRETE, EXPLOITABLE vulnerability?
""",
    )

    return result.data
```

#### 3. Exploit Scenario Generation (`exploit_analyzer.py`)

```python
async def generate_exploit_scenario(
    finding: SecurityFinding,
    code_context: str
) -> str:
    """Generate detailed exploit scenario with steps."""

    exploit_agent = Agent(
        "openai:gpt-4o",
        result_type=str,
        system_prompt="""You are a penetration tester writing exploit scenarios.

Given a vulnerability, provide a SPECIFIC, STEP-BY-STEP exploit scenario that:
1. Shows the exact attack vector
2. Provides concrete payloads or input examples
3. Explains the expected outcome
4. Describes the security impact

Format:
1. **Attack Vector**: [How the attacker accesses the vulnerability]
2. **Payload Example**: `[specific malicious input]`
3. **Expected Outcome**: [What happens when exploit succeeds]
4. **Security Impact**: [Consequences: data breach, RCE, privilege escalation, etc.]

Be CONCRETE and SPECIFIC. Use actual code examples and payloads.
""",
    )

    result = await exploit_agent.run(
        f"""Generate exploit scenario for:

**Vulnerability**: {finding.title}
**Category**: {finding.category}
**Description**: {finding.description}

**Code Context**:
```
{code_context}
```
""",
    )

    return result.data
```

### MCP Tool Implementation

```python
# python/src/mcp_server/features/security_review/security_review_tools.py

@mcp.tool()
async def security_review(
    ctx: Context,
    diff: str,
    severity_threshold: str = "medium",
    categories: list[str] | None = None,
    project_id: str | None = None,
    save_report: bool = True,
    create_tasks: bool = True,
    confidence_threshold: float = 0.8
) -> str:
    """Perform security-focused vulnerability scan."""

    # Get project context
    project_context = await get_project_context(project_id) if project_id else {}

    # Run security review agent
    result = await security_review_agent.run(
        f"""Perform security review on the following git diff:

```diff
{diff}
```

Severity Threshold: {severity_threshold}
Categories: {', '.join(categories) if categories else 'All'}
Confidence Threshold: {confidence_threshold}

Project Context:
- Tech Stack: {project_context.get('tech_stack', [])}
- Security Features: {project_context.get('security_features', [])}
""",
    )

    report = result.data

    # Filter false positives
    report.findings = await filter_false_positives(report.findings, project_context)

    # Re-calculate stats after filtering
    report.stats = {
        "critical": sum(1 for f in report.findings if f.severity == "critical"),
        "high": sum(1 for f in report.findings if f.severity == "high"),
        "medium": sum(1 for f in report.findings if f.severity == "medium"),
        "low": sum(1 for f in report.findings if f.severity == "low"),
    }

    # Generate markdown report
    markdown_report = generate_security_report_markdown(report)

    # Save to knowledge base
    if save_report and project_id:
        await knowledge_service.save_document(
            content=markdown_report,
            title=f"Security Review - {datetime.now().isoformat()}",
            project_id=project_id,
            knowledge_type="security-review",
            tags=["security", "vulnerability-scan"],
        )

    # Auto-create tasks for security findings (default behavior)
    if create_tasks and project_id:
        task_ids = await create_security_tasks(
            report.findings,
            project_id,
            severity_threshold
        )
        markdown_report += f"\n\n---\n\n**🚨 Created {len(task_ids)} security tasks for critical findings.**"

    return markdown_report
```

---

## 3. Design Review Agent Implementation

### Overview
Implement a UI/UX quality review agent with Playwright browser automation, WCAG 2.1 AA compliance testing, and responsive design verification.

### MCP Tool Specification

```python
@mcp.tool()
async def design_review(
    ctx: Context,
    preview_url: str,
    pages_to_test: list[str],  # e.g., ["/dashboard", "/settings"]
    viewports: list[str] = ["desktop", "tablet", "mobile"],
    focus_areas: list[str] | None = None,  # e.g., ["accessibility", "responsiveness"]
    project_id: str | None = None,
    save_report: bool = True,
    create_tasks: bool = False,
    capture_screenshots: bool = True
) -> str:
    """
    Perform comprehensive UI/UX design review with browser automation.

    Tests:
    1. Interaction & User Flow
    2. Responsiveness (1440px, 768px, 375px)
    3. Visual Polish (layout, typography, color)
    4. Accessibility (WCAG 2.1 AA - keyboard nav, focus states, contrast)
    5. Robustness (form validation, edge cases, loading states)
    6. Code Health (component reuse, design tokens)
    7. Content & Console (text quality, errors)

    Returns markdown report with:
    - Summary and overall assessment
    - Findings categorized by severity (Blocker, High, Medium, Nitpick)
    - Screenshots for visual issues
    - Accessibility violations with WCAG references
    """
```

### Agent Service Structure

```
agents/features/design_review/
├── __init__.py
├── design_review_agent.py         # Main PydanticAI agent
├── accessibility_checker.py       # WCAG 2.1 AA compliance
├── visual_analyzer.py             # Layout, typography, color analysis
├── responsive_tester.py           # Multi-viewport testing
├── playwright_controller.py       # Browser automation wrapper
├── screenshot_manager.py          # Screenshot capture and storage
└── task_creator.py                # Create design improvement tasks
```

### Implementation Details

#### 1. Agent Configuration (`design_review_agent.py`)

```python
from pydantic_ai import Agent
from pydantic import BaseModel

class DesignFinding(BaseModel):
    severity: Literal["blocker", "high", "medium", "nitpick"]
    category: Literal[
        "interaction", "responsiveness", "visual_polish",
        "accessibility", "robustness", "code_health", "content"
    ]
    page: str
    viewport: str | None = None  # e.g., "desktop" | "tablet" | "mobile"
    issue: str
    screenshot_path: str | None = None
    wcag_reference: str | None = None  # e.g., "WCAG 2.1 AA 1.4.3"

class DesignReviewReport(BaseModel):
    summary: str
    positive_feedback: str
    findings: list[DesignFinding]
    stats: dict[str, int]

design_review_agent = Agent(
    "openai:gpt-4o",
    result_type=DesignReviewReport,
    system_prompt="""You are an elite design review specialist with expertise in UX, visual design, accessibility, and front-end implementation.

REVIEW METHODOLOGY:
Follow the "Live Environment First" principle - assess interactive experience before static analysis.

REVIEW PHASES:
1. Interaction & User Flow - Test primary flows, interactive states, confirmations
2. Responsiveness - Test desktop (1440px), tablet (768px), mobile (375px)
3. Visual Polish - Layout alignment, typography, color consistency
4. Accessibility (WCAG 2.1 AA) - Keyboard nav, focus states, contrast ratios (4.5:1)
5. Robustness - Form validation, edge cases, loading/error states
6. Code Health - Component reuse, design tokens, established patterns
7. Content & Console - Text clarity, browser errors

COMMUNICATION PRINCIPLES:
1. Problems over prescriptions - Describe impact, not solutions
2. Triage matrix - Categorize every issue (Blocker, High, Medium, Nitpick)
3. Evidence-based - Provide screenshots for visual issues
4. Positive acknowledgment - Start with what works well

SEVERITY GUIDELINES:
- BLOCKER: Critical failures requiring immediate fix (broken flows, critical a11y violations)
- HIGH: Significant issues to fix before merge (poor UX, major visual inconsistencies)
- MEDIUM: Improvements for follow-up (minor visual issues, enhancement opportunities)
- NITPICK: Minor aesthetic details (prefix with "Nit:")

Only report issues that meaningfully impact user experience or accessibility.
""",
)
```

#### 2. Playwright Controller (`playwright_controller.py`)

```python
from playwright.async_api import async_playwright, Page, Browser

class PlaywrightController:
    """Wrapper for Playwright browser automation."""

    def __init__(self):
        self.browser: Browser | None = None
        self.page: Page | None = None

    async def initialize(self):
        """Initialize Playwright browser."""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()

    async def navigate(self, url: str):
        """Navigate to URL."""
        await self.page.goto(url)
        await self.page.wait_for_load_state("networkidle")

    async def set_viewport(self, viewport: str):
        """Set viewport size."""
        sizes = {
            "desktop": {"width": 1440, "height": 900},
            "tablet": {"width": 768, "height": 1024},
            "mobile": {"width": 375, "height": 667},
        }
        await self.page.set_viewport_size(sizes[viewport])

    async def take_screenshot(self, name: str) -> str:
        """Capture screenshot and return path."""
        path = f"/tmp/screenshots/{name}.png"
        await self.page.screenshot(path=path, full_page=True)
        return path

    async def get_console_errors(self) -> list[str]:
        """Get console error messages."""
        errors = []
        self.page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        return errors

    async def check_keyboard_navigation(self) -> dict[str, bool]:
        """Test keyboard navigation."""
        results = {}

        # Test Tab key navigation
        await self.page.keyboard.press("Tab")
        focused = await self.page.evaluate("document.activeElement.tagName")
        results["tab_works"] = focused != "BODY"

        # Test focus visibility
        focus_visible = await self.page.evaluate("""
            () => {
                const style = window.getComputedStyle(document.activeElement);
                return style.outline !== 'none' || style.boxShadow !== 'none';
            }
        """)
        results["focus_visible"] = focus_visible

        return results

    async def check_color_contrast(self) -> list[dict[str, Any]]:
        """Check WCAG color contrast ratios."""
        violations = await self.page.evaluate("""
            () => {
                // Use axe-core or manual contrast calculation
                // Return list of elements with insufficient contrast
                return [];  // Placeholder
            }
        """)
        return violations

    async def close(self):
        """Close browser."""
        if self.browser:
            await self.browser.close()
```

#### 3. Accessibility Checker (`accessibility_checker.py`)

```python
async def check_accessibility(
    controller: PlaywrightController,
    page_url: str
) -> list[DesignFinding]:
    """Perform WCAG 2.1 AA accessibility checks."""

    findings = []

    # Navigate to page
    await controller.navigate(page_url)

    # 1. Keyboard Navigation
    kb_results = await controller.check_keyboard_navigation()
    if not kb_results["tab_works"]:
        findings.append(DesignFinding(
            severity="blocker",
            category="accessibility",
            page=page_url,
            issue="Keyboard navigation (Tab key) does not work - no focusable elements detected",
            wcag_reference="WCAG 2.1 AA 2.1.1 (Keyboard)"
        ))

    if not kb_results["focus_visible"]:
        findings.append(DesignFinding(
            severity="high",
            category="accessibility",
            page=page_url,
            issue="Focus states are not visible - users cannot see which element is focused",
            wcag_reference="WCAG 2.1 AA 2.4.7 (Focus Visible)"
        ))

    # 2. Color Contrast
    contrast_violations = await controller.check_color_contrast()
    for violation in contrast_violations:
        findings.append(DesignFinding(
            severity="high",
            category="accessibility",
            page=page_url,
            issue=f"Insufficient color contrast ratio: {violation['ratio']} (minimum 4.5:1 required)",
            wcag_reference="WCAG 2.1 AA 1.4.3 (Contrast Minimum)"
        ))

    # 3. Alt Text on Images
    missing_alt = await controller.page.evaluate("""
        () => {
            const images = Array.from(document.querySelectorAll('img'));
            return images.filter(img => !img.alt).length;
        }
    """)
    if missing_alt > 0:
        findings.append(DesignFinding(
            severity="high",
            category="accessibility",
            page=page_url,
            issue=f"{missing_alt} images missing alt text - screen readers cannot describe images",
            wcag_reference="WCAG 2.1 AA 1.1.1 (Non-text Content)"
        ))

    # 4. Form Labels
    unlabeled_inputs = await controller.page.evaluate("""
        () => {
            const inputs = Array.from(document.querySelectorAll('input, textarea, select'));
            return inputs.filter(input => {
                const label = document.querySelector(`label[for="${input.id}"]`);
                return !label && !input.getAttribute('aria-label');
            }).length;
        }
    """)
    if unlabeled_inputs > 0:
        findings.append(DesignFinding(
            severity="high",
            category="accessibility",
            page=page_url,
            issue=f"{unlabeled_inputs} form inputs missing labels - users cannot understand input purpose",
            wcag_reference="WCAG 2.1 AA 3.3.2 (Labels or Instructions)"
        ))

    return findings
```

#### 4. Responsive Testing (`responsive_tester.py`)

```python
async def test_responsiveness(
    controller: PlaywrightController,
    page_url: str,
    viewports: list[str]
) -> list[DesignFinding]:
    """Test responsive design across viewports."""

    findings = []

    for viewport in viewports:
        await controller.navigate(page_url)
        await controller.set_viewport(viewport)

        # Capture screenshot
        screenshot_path = await controller.take_screenshot(f"{page_url}_{viewport}")

        # 1. Check for horizontal scrolling (except mobile)
        has_horizontal_scroll = await controller.page.evaluate("""
            () => document.documentElement.scrollWidth > window.innerWidth
        """)
        if has_horizontal_scroll and viewport != "mobile":
            findings.append(DesignFinding(
                severity="high",
                category="responsiveness",
                page=page_url,
                viewport=viewport,
                issue="Horizontal scrolling detected - content overflows viewport width",
                screenshot_path=screenshot_path
            ))

        # 2. Check for overlapping elements
        overlaps = await controller.page.evaluate("""
            () => {
                // Check for element overlaps (simplified)
                const elements = Array.from(document.querySelectorAll('*'));
                // ... overlap detection logic
                return 0;  // Placeholder
            }
        """)
        if overlaps > 0:
            findings.append(DesignFinding(
                severity="medium",
                category="responsiveness",
                page=page_url,
                viewport=viewport,
                issue=f"{overlaps} overlapping elements detected - layout breaks at this viewport",
                screenshot_path=screenshot_path
            ))

        # 3. Check touch target sizes (mobile only)
        if viewport == "mobile":
            small_targets = await controller.page.evaluate("""
                () => {
                    const buttons = Array.from(document.querySelectorAll('button, a, input'));
                    return buttons.filter(btn => {
                        const rect = btn.getBoundingClientRect();
                        return rect.width < 44 || rect.height < 44;  // Apple HIG minimum
                    }).length;
                }
            """)
            if small_targets > 0:
                findings.append(DesignFinding(
                    severity="medium",
                    category="responsiveness",
                    page=page_url,
                    viewport=viewport,
                    issue=f"{small_targets} interactive elements smaller than 44x44px - difficult to tap on mobile",
                    screenshot_path=screenshot_path
                ))

    return findings
```

### MCP Tool Implementation

```python
# python/src/mcp_server/features/design_review/design_review_tools.py

@mcp.tool()
async def design_review(
    ctx: Context,
    preview_url: str,
    pages_to_test: list[str],
    viewports: list[str] = ["desktop", "tablet", "mobile"],
    focus_areas: list[str] | None = None,
    project_id: str | None = None,
    save_report: bool = True,
    create_tasks: bool = False,
    capture_screenshots: bool = True
) -> str:
    """Perform comprehensive UI/UX design review."""

    # Initialize Playwright
    controller = PlaywrightController()
    await controller.initialize()

    all_findings = []

    try:
        for page in pages_to_test:
            full_url = f"{preview_url}{page}"

            # Phase 1: Accessibility checks
            if not focus_areas or "accessibility" in focus_areas:
                accessibility_findings = await check_accessibility(controller, full_url)
                all_findings.extend(accessibility_findings)

            # Phase 2: Responsiveness testing
            if not focus_areas or "responsiveness" in focus_areas:
                responsive_findings = await test_responsiveness(controller, full_url, viewports)
                all_findings.extend(responsive_findings)

            # Phase 3: Visual polish (run agent on screenshots)
            if not focus_areas or "visual_polish" in focus_areas:
                visual_findings = await analyze_visual_polish(controller, full_url, viewports)
                all_findings.extend(visual_findings)

            # Phase 4: Console errors
            console_errors = await controller.get_console_errors()
            if console_errors:
                all_findings.append(DesignFinding(
                    severity="medium",
                    category="content",
                    page=full_url,
                    issue=f"Console errors detected: {', '.join(console_errors[:3])}"
                ))

        # Generate comprehensive report
        report = DesignReviewReport(
            summary=f"Reviewed {len(pages_to_test)} pages across {len(viewports)} viewports",
            positive_feedback="[To be generated by agent based on findings]",
            findings=all_findings,
            stats={
                "blocker": sum(1 for f in all_findings if f.severity == "blocker"),
                "high": sum(1 for f in all_findings if f.severity == "high"),
                "medium": sum(1 for f in all_findings if f.severity == "medium"),
                "nitpick": sum(1 for f in all_findings if f.severity == "nitpick"),
            }
        )

        # Run main design review agent for final analysis
        final_report = await design_review_agent.run(
            f"""Analyze the following automated design review findings and generate a comprehensive report:

**Pages Tested**: {', '.join(pages_to_test)}
**Viewports**: {', '.join(viewports)}
**Preview URL**: {preview_url}

**Automated Findings**:
{generate_findings_summary(report)}

Provide:
1. Positive feedback on what works well
2. Comprehensive summary of issues
3. Additional observations not caught by automation
4. Prioritized recommendations
""",
        )

        # Generate markdown report
        markdown_report = generate_design_report_markdown(final_report.data)

        # Save to knowledge base
        if save_report and project_id:
            await knowledge_service.save_document(
                content=markdown_report,
                title=f"Design Review - {datetime.now().isoformat()}",
                project_id=project_id,
                knowledge_type="design-review",
                tags=["design", "ui-ux", "accessibility"],
            )

        # Create tasks for high-priority issues
        if create_tasks and project_id:
            task_ids = await create_design_tasks(
                final_report.data.findings,
                project_id
            )
            markdown_report += f"\n\n---\n\n**Created {len(task_ids)} design improvement tasks.**"

        return markdown_report

    finally:
        await controller.close()
```

---

## 4. Cross-Cutting Integration Requirements

### Shared Infrastructure

#### 1. Agent Service Base Class

```python
# agents/features/shared/base_review_agent.py

from abc import ABC, abstractmethod
from pydantic_ai import Agent

class BaseReviewAgent(ABC):
    """Base class for all review agents."""

    def __init__(self, agent: Agent):
        self.agent = agent

    @abstractmethod
    async def review(self, **kwargs) -> str:
        """Perform review and return markdown report."""
        pass

    async def get_project_context(self, project_id: str | None) -> dict[str, Any]:
        """Fetch project context from knowledge base."""
        if not project_id:
            return {}

        # Query Archon knowledge base
        sources = await rag_service.get_project_sources(project_id)

        context = {
            "tech_stack": [],
            "coding_standards": [],
            "design_principles": [],
            "security_features": [],
        }

        for source in sources:
            # Extract relevant context based on tags and knowledge_type
            if "tech-stack" in source.tags:
                context["tech_stack"].append(source.summary)
            elif "coding-standards" in source.tags:
                context["coding_standards"].append(source.summary)
            elif "design-principles" in source.tags:
                context["design_principles"].append(source.summary)
            elif "security" in source.tags:
                context["security_features"].append(source.summary)

        return context

    async def save_report(
        self,
        report: str,
        title: str,
        project_id: str,
        review_type: str,
        tags: list[str]
    ):
        """Save review report to knowledge base."""
        await knowledge_service.save_document(
            content=report,
            title=title,
            project_id=project_id,
            knowledge_type=review_type,
            tags=tags,
        )
```

#### 2. Unified Report Generator

```python
# agents/features/shared/report_generator.py

def generate_review_report_markdown(
    report_type: str,
    findings: list[Any],
    summary: str,
    stats: dict[str, int]
) -> str:
    """Generate standardized markdown report."""

    md = f"# {report_type.title()} Review Report\n\n"
    md += f"**Generated**: {datetime.now().isoformat()}\n"
    md += f"**Total Findings**: {sum(stats.values())}\n\n"

    md += "## Summary\n\n"
    md += summary + "\n\n"

    md += "## Statistics\n\n"
    for severity, count in stats.items():
        md += f"- **{severity.title()}**: {count}\n"
    md += "\n"

    # Group findings by severity
    severity_order = ["critical", "blocker", "high", "medium", "low", "nitpick"]
    grouped = {}
    for severity in severity_order:
        grouped[severity] = [f for f in findings if f.severity == severity]

    # Generate findings sections
    for severity, items in grouped.items():
        if not items:
            continue

        md += f"## {severity.title()} Findings\n\n"
        for i, finding in enumerate(items, 1):
            md += f"### {i}. {finding.get('title', 'Issue')}\n\n"
            md += f"**Location**: `{finding['file_path']}`"
            if finding.get('line_numbers'):
                md += f":{finding['line_numbers']}"
            md += "\n\n"

            md += f"**Description**: {finding['description']}\n\n"

            if finding.get('recommendation'):
                md += f"**Recommendation**: {finding['recommendation']}\n\n"

            if finding.get('code_snippet'):
                md += f"```\n{finding['code_snippet']}\n```\n\n"

            if finding.get('screenshot_path'):
                md += f"![Screenshot]({finding['screenshot_path']})\n\n"

            md += "---\n\n"

    return md
```

#### 3. Task Creation Service

```python
# agents/features/shared/task_creator.py

async def create_review_tasks(
    findings: list[Any],
    project_id: str,
    review_type: str,
    severity_threshold: str
) -> list[str]:
    """Create Archon tasks for review findings."""

    threshold_order = ["critical", "blocker", "high", "medium", "low", "nitpick"]
    threshold_index = threshold_order.index(severity_threshold)

    created_task_ids = []

    for finding in findings:
        finding_severity = finding.severity if hasattr(finding, 'severity') else finding.get('severity')

        if threshold_order.index(finding_severity) <= threshold_index:
            # Generate task title
            title = f"[{review_type.title()}] {finding_severity.title()}: "
            if hasattr(finding, 'title'):
                title += finding.title
            elif hasattr(finding, 'category'):
                title += finding.category.replace('_', ' ').title()

            # Generate task description
            description = ""
            if hasattr(finding, 'description'):
                description += f"**Issue**: {finding.description}\n\n"

            if hasattr(finding, 'recommendation'):
                description += f"**Recommendation**: {finding.recommendation}\n\n"

            if hasattr(finding, 'file_path'):
                location = f"{finding.file_path}"
                if hasattr(finding, 'line_numbers'):
                    location += f":{finding.line_numbers}"
                description += f"**Location**: `{location}`\n\n"

            if hasattr(finding, 'exploit_scenario'):
                description += f"**Exploit Scenario**:\n{finding.exploit_scenario}\n\n"

            if hasattr(finding, 'wcag_reference'):
                description += f"**WCAG Reference**: {finding.wcag_reference}\n\n"

            # Create task
            task = await task_service.create_task({
                "project_id": project_id,
                "title": title,
                "description": description,
                "status": "todo",
                "assignee": "Archon",
                "tags": [review_type, finding_severity, getattr(finding, 'category', 'general')],
            })
            created_task_ids.append(task.task_id)

    return created_task_ids
```

### Knowledge Base Integration

#### Schema Updates

```sql
-- Add review_type to archon_sources
ALTER TABLE archon_sources
ADD COLUMN IF NOT EXISTS review_type TEXT
CHECK (review_type IN ('code-review', 'security-review', 'design-review'));

-- Add review metadata
ALTER TABLE archon_sources
ADD COLUMN IF NOT EXISTS review_metadata JSONB DEFAULT '{}';

-- Example metadata:
-- {
--   "git_ref": "abc123",
--   "severity_counts": {"critical": 2, "high": 5},
--   "pages_tested": ["/dashboard", "/settings"],
--   "viewports_tested": ["desktop", "mobile"]
-- }

-- Create index for review queries
CREATE INDEX IF NOT EXISTS idx_archon_sources_review_type
ON archon_sources(review_type)
WHERE review_type IS NOT NULL;
```

### MCP Server Registration

```python
# python/src/mcp_server/server.py

# Register all review tools
from src.mcp_server.features.code_review.code_review_tools import review_code
from src.mcp_server.features.security_review.security_review_tools import security_review
from src.mcp_server.features.design_review.design_review_tools import design_review

# Tools are automatically registered via @mcp.tool() decorator
```

---

## 5. Implementation Phases

### Phase 1: Code Review Agent (Weeks 1-2)

**Priority**: Highest - Most universal need

**Deliverables**:
1. PydanticAI agent with pragmatic review framework
2. MCP tool: `archon:review_code`
3. Knowledge base integration
4. Task creation for findings
5. Tests and documentation

**Tasks**:
- [ ] Create agent service structure (`agents/features/code_review/`)
- [ ] Implement `code_review_agent.py` with 7-level hierarchy
- [ ] Implement `review_frameworks.py` (pragmatic, strict, fast)
- [ ] Implement `context_analyzer.py` for project context
- [ ] Implement `task_creator.py` for automatic task generation
- [ ] Create MCP tool in `mcp_server/features/code_review/code_review_tools.py`
- [ ] Add knowledge base schema updates
- [ ] Write unit tests
- [ ] Create documentation in `docs/workflows/code-review.md`
- [ ] Test with Netzwächter refactoring PRs

### Phase 2: Security Review Agent (Weeks 2-3)

**Priority**: High - Security is non-negotiable

**Deliverables**:
1. PydanticAI agent with OWASP categories
2. MCP tool: `archon:security_review`
3. False positive filtering with confidence scoring
4. Exploit scenario generation
5. Automatic security task creation

**Tasks**:
- [ ] Create agent service structure (`agents/features/security_review/`)
- [ ] Implement `security_review_agent.py` with OWASP categories
- [ ] Implement `vulnerability_scanner.py`
- [ ] Implement `false_positive_filter.py` with multi-stage filtering
- [ ] Implement `exploit_analyzer.py` for scenario generation
- [ ] Implement `remediation_guide.py`
- [ ] Create MCP tool in `mcp_server/features/security_review/`
- [ ] Write unit tests
- [ ] Create documentation in `docs/workflows/security-review.md`
- [ ] Test with security-sensitive code changes

### Phase 3: Design Review Agent (Weeks 3-4)

**Priority**: Medium - Frontend-specific but high value

**Deliverables**:
1. PydanticAI agent with design principles
2. Playwright automation integration
3. MCP tool: `archon:design_review`
4. WCAG 2.1 AA accessibility checks
5. Multi-viewport responsive testing

**Tasks**:
- [ ] Create agent service structure (`agents/features/design_review/`)
- [ ] Implement `design_review_agent.py`
- [ ] Implement `playwright_controller.py` for browser automation
- [ ] Implement `accessibility_checker.py` (WCAG 2.1 AA)
- [ ] Implement `responsive_tester.py` for multi-viewport
- [ ] Implement `visual_analyzer.py`
- [ ] Implement `screenshot_manager.py`
- [ ] Create MCP tool in `mcp_server/features/design_review/`
- [ ] Write unit tests
- [ ] Create documentation in `docs/workflows/design-review.md`
- [ ] Test with Netzwächter UI changes

### Phase 4: Integration & Polish (Week 4)

**Priority**: Essential for user experience

**Deliverables**:
1. Unified review dashboard in Archon UI
2. Review history and comparison
3. Comprehensive documentation
4. Example workflows for Netzwächter

**Tasks**:
- [ ] Create review dashboard page in `archon-ui-main/src/pages/ReviewsPage.tsx`
- [ ] Add review history view
- [ ] Implement review comparison (before/after)
- [ ] Create unified report viewer
- [ ] Add filtering and search for reviews
- [ ] Write comprehensive user guide
- [ ] Create video tutorials
- [ ] Document integration with Netzwächter workflows
- [ ] Performance optimization
- [ ] Final testing and bug fixes

---

## 6. Testing Strategy

### Unit Tests

Each agent service must include comprehensive unit tests:

```python
# agents/features/code_review/tests/test_code_review_agent.py

import pytest
from src.agents.features.code_review.code_review_agent import code_review_agent

@pytest.mark.asyncio
async def test_code_review_basic_functionality():
    """Test basic code review functionality."""
    diff = """
diff --git a/app.py b/app.py
+def process_user_input(user_input):
+    query = f"SELECT * FROM users WHERE name = '{user_input}'"
+    return db.execute(query)
"""

    result = await code_review_agent.run(f"Review this diff:\n\n{diff}")

    assert result.data.findings
    assert any(f.category == "security" for f in result.data.findings)
    assert any("SQL injection" in f.problem.lower() for f in result.data.findings)

@pytest.mark.asyncio
async def test_code_review_confidence_threshold():
    """Test confidence threshold filtering."""
    # Test that low-confidence findings are filtered out
    # ...
```

### Integration Tests

Test full MCP tool workflows:

```python
# mcp_server/features/code_review/tests/test_code_review_integration.py

@pytest.mark.asyncio
async def test_review_code_tool_with_project_context():
    """Test review_code MCP tool with project context."""

    # Create test project
    project = await project_service.create_project({
        "name": "Test Project",
        "description": "Integration test"
    })

    # Add coding standards to knowledge base
    await knowledge_service.save_document(
        content="Always use prepared statements for SQL queries.",
        title="SQL Security Standards",
        project_id=project.project_id,
        knowledge_type="technical",
        tags=["coding-standards", "security"]
    )

    # Run code review
    diff = "..." # SQL injection vulnerability
    result = await review_code(
        ctx=mock_context,
        diff=diff,
        project_id=project.project_id,
        create_tasks=True
    )

    # Verify findings reference project standards
    assert "prepared statements" in result.lower()

    # Verify tasks were created
    tasks = await task_service.get_tasks_by_project(project.project_id)
    assert len(tasks) > 0
    assert any("SQL injection" in t.title for t in tasks)
```

### End-to-End Tests

Test complete workflows in Claude Code / Cursor / Windsurf:

1. **Code Review E2E**:
   ```bash
   # In IDE with MCP connection
   1. Make code change introducing security issue
   2. Call archon:review_code with diff
   3. Verify findings reported
   4. Verify tasks created in Archon
   5. Fix issue
   6. Re-run review
   7. Verify issue resolved
   ```

2. **Security Review E2E**:
   ```bash
   1. Create PR with potential vulnerability
   2. Call archon:security_review with diff
   3. Verify high-confidence findings only
   4. Verify exploit scenarios provided
   5. Verify remediation guidance
   6. Check false positive rate (<10%)
   ```

3. **Design Review E2E**:
   ```bash
   1. Deploy preview environment
   2. Call archon:design_review with preview URL
   3. Verify accessibility checks run
   4. Verify responsive testing across viewports
   5. Verify screenshots captured
   6. Review markdown report
   ```

---

## 7. Documentation Requirements

### User Documentation

1. **Quick Start Guide** (`docs/workflows/quick-start.md`):
   - How to run each review type
   - Basic usage examples
   - Common parameters
   - Interpreting results

2. **Code Review Guide** (`docs/workflows/code-review.md`):
   - Review philosophy and framework
   - Severity guidelines
   - Best practices
   - Example workflows

3. **Security Review Guide** (`docs/workflows/security-review.md`):
   - OWASP categories covered
   - Confidence scoring explained
   - False positive filtering
   - Remediation strategies

4. **Design Review Guide** (`docs/workflows/design-review.md`):
   - WCAG compliance testing
   - Responsive design verification
   - Setting up preview environments
   - Interpreting visual feedback

### Developer Documentation

1. **Agent Architecture** (`docs/development/agent-architecture.md`):
   - PydanticAI integration
   - Agent service structure
   - Adding new review types

2. **MCP Tool Development** (`docs/development/mcp-tools.md`):
   - Tool registration
   - Parameter design
   - Error handling
   - Testing strategies

3. **Knowledge Base Integration** (`docs/development/knowledge-base.md`):
   - Schema design
   - Storing review reports
   - Querying review history
   - Linking reviews to projects

---

## 8. Performance Considerations

### Agent Execution Time

**Target latencies**:
- Code Review: 15-30 seconds for typical PR (< 500 lines)
- Security Review: 20-40 seconds (includes false positive filtering)
- Design Review: 30-60 seconds (includes browser automation)

**Optimizations**:
1. **Parallel Processing**: Run multiple checks concurrently
2. **Caching**: Cache project context and coding standards
3. **Incremental Analysis**: Only analyze changed files
4. **Batch Processing**: Process multiple files in single agent call

### Model Selection

**Recommended models**:

1. **Code Review**:
   - Primary: `claude-3-5-sonnet-20241022` (best reasoning)
   - Fast: `gpt-4o-mini` (pragmatic mode)

2. **Security Review**:
   - Primary: `claude-3-5-sonnet-20241022` (best security analysis)
   - Verification: `gpt-4o` (false positive filtering)

3. **Design Review**:
   - Primary: `gpt-4o` (best vision + reasoning)
   - Accessibility: `claude-3-5-sonnet-20241022` (WCAG expertise)

### Cost Management

**Estimated costs per review** (based on Claude Sonnet 3.5):
- Code Review: $0.05-0.15 per PR
- Security Review: $0.10-0.25 per PR (includes verification)
- Design Review: $0.15-0.35 per review (multi-viewport)

**Cost optimization strategies**:
1. Use `gpt-4o-mini` for fast/pragmatic reviews
2. Implement token usage tracking
3. Add review result caching (avoid re-reviewing same code)
4. Offer tiered review options (fast, standard, comprehensive)

---

## 9. Success Metrics

### Developer Experience Metrics

1. **Adoption Rate**:
   - % of PRs with code reviews
   - % of security-sensitive PRs scanned
   - % of UI changes design-reviewed

2. **Time Savings**:
   - Average time to identify issues (vs manual review)
   - Reduction in review cycle time
   - Faster time to merge

3. **Satisfaction**:
   - Developer feedback scores
   - False positive rate (<10% target)
   - Usefulness of recommendations

### Code Quality Metrics

1. **Issues Found**:
   - Critical issues caught before merge
   - Security vulnerabilities prevented
   - Accessibility violations fixed

2. **Issue Resolution**:
   - % of findings addressed
   - Time to fix critical issues
   - Recurrence rate of similar issues

3. **Quality Trends**:
   - Reduction in bugs reaching production
   - Improvement in code maintainability scores
   - Increase in test coverage

### Business Impact Metrics

1. **Risk Reduction**:
   - Security incidents prevented
   - Accessibility compliance improvements
   - Production bugs avoided

2. **Development Velocity**:
   - Faster PR review cycles
   - Reduced back-and-forth iterations
   - Improved first-time quality

3. **Platform Adoption**:
   - Number of teams using workflows
   - Growth in review volume
   - Integration with CI/CD pipelines

---

## 10. Future Enhancements

### Phase 5+: Advanced Features

1. **Learning from Feedback**:
   - Track developer actions on findings (accepted/rejected)
   - Fine-tune agents based on feedback
   - Improve false positive filtering over time

2. **Custom Review Templates**:
   - Team-specific review frameworks
   - Industry-specific checklists (healthcare, finance)
   - Custom severity thresholds

3. **Review Comparison**:
   - Compare reviews over time
   - Track quality improvements
   - Identify recurring patterns

4. **Integration with CI/CD**:
   - GitHub Actions integration
   - Automated PR comments
   - Block merges on critical findings

5. **Multi-Agent Collaboration**:
   - Coordinate reviews across agents
   - Cross-reference findings (security + code quality)
   - Holistic quality assessment

---

## 11. Dependencies

### Python Packages

```toml
# python/pyproject.toml

[project]
dependencies = [
    # ... existing dependencies
    "pydantic-ai>=0.1.0",  # Agent framework
    "playwright>=1.40.0",   # Browser automation
]

[project.optional-dependencies]
agents = [
    "openai>=1.0.0",       # OpenAI models
    "anthropic>=0.8.0",    # Claude models
]
```

### System Dependencies

```bash
# Install Playwright browsers
playwright install chromium
```

### MCP Server Dependencies

- Existing Archon MCP server infrastructure
- Knowledge base service (RAG)
- Project/Task services
- Database (Supabase)

---

## 12. Risk Assessment

### Technical Risks

1. **Agent Accuracy**:
   - **Risk**: False positives overwhelm developers
   - **Mitigation**: High confidence thresholds, multi-stage filtering, continuous calibration

2. **Performance**:
   - **Risk**: Reviews too slow for developer workflow
   - **Mitigation**: Parallel processing, incremental analysis, fast review modes

3. **Cost**:
   - **Risk**: LLM API costs exceed budget
   - **Mitigation**: Token usage tracking, cheaper models for non-critical reviews, caching

### Integration Risks

1. **MCP Compatibility**:
   - **Risk**: Tool signatures change, breaking integrations
   - **Mitigation**: Versioned tools, backward compatibility, comprehensive tests

2. **Knowledge Base Performance**:
   - **Risk**: Large review reports slow down knowledge base
   - **Mitigation**: Pagination, summary views, archival strategies

3. **Browser Automation**:
   - **Risk**: Playwright automation flaky or environment-dependent
   - **Mitigation**: Retry logic, headless mode, Docker containerization

### Organizational Risks

1. **Adoption**:
   - **Risk**: Developers don't use new workflows
   - **Mitigation**: Clear documentation, video tutorials, success stories, gradual rollout

2. **Over-Reliance**:
   - **Risk**: Teams stop doing manual reviews
   - **Mitigation**: Position as augmentation, not replacement; highlight limitations

3. **False Confidence**:
   - **Risk**: Developers assume all issues caught
   - **Mitigation**: Clear disclaimers, confidence scores, encourage manual verification

---

## 13. Rollout Plan

### Week 1-2: Code Review Agent (Alpha)

**Target Users**: Internal Archon development team

**Activities**:
- Deploy code review agent to production
- Test with Archon codebase PRs
- Gather feedback on accuracy and usefulness
- Iterate on prompts and thresholds

**Success Criteria**:
- <15% false positive rate
- >80% of findings actionable
- Average review time <30 seconds

### Week 3: Security Review Agent (Beta)

**Target Users**: Security-conscious teams

**Activities**:
- Deploy security review agent
- Test with known vulnerable code samples
- Validate exploit scenarios
- Refine false positive filtering

**Success Criteria**:
- >90% true positive rate
- All high/critical findings have exploit scenarios
- Zero false negatives on OWASP Top 10 samples

### Week 4: Design Review Agent (Beta)

**Target Users**: Frontend teams

**Activities**:
- Deploy design review agent
- Test with Archon UI and Netzwächter
- Validate accessibility checks
- Verify responsive testing accuracy

**Success Criteria**:
- WCAG 2.1 AA compliance checks 100% accurate
- Responsive issues detected across all viewports
- Screenshots useful for visual debugging

### Week 5: Public Release

**Target Users**: All Archon users

**Activities**:
- Publish documentation
- Create video tutorials
- Announce on GitHub/Discord
- Monitor usage and feedback

**Success Criteria**:
- >50% of active projects use at least one workflow
- <5% negative feedback rate
- >100 reviews performed in first week

---

## 14. Conclusion

This implementation plan provides a comprehensive roadmap for integrating Code Review, Security Review, and Design Review workflows into Archon via MCP tools. The phased approach ensures:

1. **Incremental Value**: Each phase delivers standalone value
2. **Risk Management**: Early feedback loops catch issues before full rollout
3. **Quality Focus**: High confidence thresholds prevent false positive fatigue
4. **Developer Experience**: Clear documentation, fast performance, actionable feedback

**Next Steps**:
1. Review and approve this plan
2. Begin Phase 1: Code Review Agent implementation
3. Set up development environment and dependencies
4. Create initial tests and documentation structure

**Estimated Timeline**: 8 weeks to full production release

**Estimated Effort**:
- Code Review: 2 weeks (1 developer)
- Security Review: 1.5 weeks (1 developer)
- Design Review: 1.5 weeks (1 developer)
- Integration & Polish: 1 week (1 developer)
- Documentation & Testing: Ongoing

**Total**: ~6 weeks of focused development + 2 weeks of testing/documentation

---

*Created: 2025-10-13*
*Last Updated: 2025-10-13*
*Document Version: 1.0*
