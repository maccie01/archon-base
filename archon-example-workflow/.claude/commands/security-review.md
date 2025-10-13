---
description: Perform security vulnerability audit on code changes with OWASP-based scanning and exploit scenarios
---

# Security Review Workflow

Conduct focused security audit on code changes to identify high-confidence vulnerabilities before merge.

## Usage

```bash
# Security audit on all uncommitted changes
/security-review

# Audit specific files
/security-review path/to/file1.py path/to/file2.py

# Audit a specific commit
/security-review <commit-hash>

# Audit branch changes
/security-review main...HEAD
```

## Step 1: Gather Changes

Determine what to audit:

```bash
# If no args provided, audit uncommitted changes
git status
git diff

# If commit hash provided
git show <commit-hash>

# If branch comparison provided
git diff <comparison>

# If file paths provided
git diff -- <file1> <file2>
```

Store the diff content for security analysis.

## Step 2: Identify Attack Surface

Analyze what code is being changed:

```bash
# Look for security-sensitive areas
grep -r "password\|secret\|token\|api_key" <changed-files>
grep -r "exec\|eval\|system\|subprocess" <changed-files>
grep -r "SQL\|query\|execute" <changed-files>
grep -r "request\|input\|user" <changed-files>

# Check for authentication/authorization
grep -r "auth\|login\|permission\|role" <changed-files>

# Find external inputs
grep -r "request\.\|params\|query\|body" <changed-files>
```

Note any security-sensitive patterns found.

## Step 3: Search Security Documentation

Use Archon MCP tools to find security context:

```bash
# Search for security standards
rag_search_knowledge_base(query="security policy", match_count=5)

# Find authentication patterns
rag_search_code_examples(query="authentication secure", match_count=3)

# Search for known vulnerabilities
rag_search_knowledge_base(query="OWASP CVE", match_count=5)

# Get project security docs
rag_get_available_sources()
# Look for sources like "Security Guidelines", "OWASP", etc.
```

Store security guidelines and patterns.

## Step 4: Invoke Security Auditor Agent

Use the Task tool to invoke the security-auditor specialist agent:

```xml
<use_task_tool>
{
  "subagent_type": "security-auditor",
  "prompt": "Perform security vulnerability audit on the following code changes:

**Changes Summary:**
[Describe what changed - files, type of functionality added/modified]

**Git Diff:**
```
[Paste the diff content here]
```

**Attack Surface Analysis:**
[Include findings from grep searches - what security-sensitive code is present]

**Project Security Context:**
[Include security standards and patterns from knowledge base]

**Technology Stack:**
[List languages/frameworks from diff - Python, JavaScript, FastAPI, React, etc.]

Scan for OWASP Top 10 vulnerabilities with focus on:
- High-confidence findings only (>80% confidence)
- Clear exploitation paths
- Concrete attack scenarios
- Actionable remediation

Categories to check:
1. Input Validation (SQL injection, Command injection, Path traversal, XXE)
2. Authentication & Authorization (bypass, privilege escalation, session flaws)
3. Cryptography & Secrets (hardcoded credentials, weak crypto)
4. Injection & Code Execution (RCE, deserialization, XSS)
5. Data Exposure (sensitive logging, API leakage, IDOR)
",
  "description": "Perform security vulnerability audit"
}
</use_task_tool>
```

## Step 5: Present Security Findings

Present the security audit results with clear severity and actionability:

1. **Executive Summary**: Risk level and recommendation
2. **Critical Vulnerabilities**: Immediate fix required
3. **High Severity**: Fix before merge
4. **Medium Severity**: Consider fixing
5. **Defense in Depth**: Additional hardening recommendations

For each finding, include:
- Clear vulnerability description
- Attack vector explanation
- Concrete exploit scenario
- Security impact assessment
- Specific remediation code

## Step 6: Optional - Create Security Tasks

If vulnerabilities found, offer to create tracked tasks:

```bash
# Ask user
"Found [N] security vulnerabilities. Would you like me to create Archon tasks for tracking fixes?"

# If yes, create tasks with high priority:
# For each critical/high vulnerability:
manage_task(
  action="create",
  project_id="<project-id>",
  title="[SECURITY] <vulnerability-title>",
  description="**Severity**: <Critical/High/Medium>
**CWE**: <CWE-ID>
**Impact**: <Data breach/RCE/etc>

**Issue**: <description>

**Exploit Scenario**:
<attack-steps>

**Fix**: <remediation-code>",
  status="todo",
  assignee="<developer>",
  task_order=100,  # Highest priority
  tags=["security", "vulnerability", "<severity>", "<cwe>"]
)
```

## Step 7: Generate Security Report

Optionally save the security audit to project documentation:

```bash
# Ask user
"Would you like me to save this security audit report to the project?"

# If yes, create document via Archon:
manage_document(
  action="create",
  project_id="<project-id>",
  document_type="security_audit",
  title="Security Audit - <date>",
  content={
    "summary": "<executive-summary>",
    "findings": "<all-findings>",
    "recommendations": "<remediation-steps>"
  },
  tags=["security", "audit", "<date>"]
)
```

## Important Notes

- **High confidence only**: Only report vulnerabilities with >80% confidence
- **Concrete exploits**: Show exact attack paths, not theoretical concerns
- **Skip excluded categories**: No DoS, rate limiting, test-only issues, log spoofing
- **Focus on reachable code**: Ensure vulnerability is actually exploitable
- **Provide fixes**: Always include specific remediation code

## Example Output Format

```markdown
# Security Audit Report

## Executive Summary
- **Files Audited**: 8
- **Vulnerabilities Found**: 2 Critical, 1 High, 0 Medium
- **Risk Level**: CRITICAL
- **Recommendation**: BLOCK MERGE - Fix critical issues immediately

## Critical Vulnerabilities 🚨

### 1. SQL Injection in User Search

- **File**: `api/search.py:45`
- **Category**: Input Validation - SQL Injection
- **Severity**: Critical
- **Confidence**: 0.95 (Certain)
- **CWE**: CWE-89

**Description:**
User input from search parameter is directly concatenated into SQL query without parameterization.

**Attack Vector:**
Attacker controls `search_term` parameter in `/api/users/search?q=<input>`

**Exploit Scenario:**
1. Attacker sends: `/api/users/search?q=' OR '1'='1`
2. Query becomes: `SELECT * FROM users WHERE name = '' OR '1'='1'`
3. Result: All user records returned, database exposed

**Security Impact:**
- [x] Data Breach - Full database dump possible
- [x] Authentication Bypass - Can extract password hashes
- [ ] Remote Code Execution
- [ ] Privilege Escalation

**Remediation:**
```python
# BEFORE (vulnerable)
query = f"SELECT * FROM users WHERE name = '{search_term}'"
cursor.execute(query)

# AFTER (secure)
query = "SELECT * FROM users WHERE name = ?"
cursor.execute(query, (search_term,))
```

---

### 2. Command Injection in File Processing

[Similar detailed format]

## High Severity ⚠️

### 1. Hardcoded API Key

[Similar format]

## Defense in Depth Recommendations 🛡️

1. Add input validation middleware for all endpoints
2. Implement rate limiting on authentication endpoints
3. Enable security headers (CSP, HSTS, X-Frame-Options)
4. Add automated security scanning to CI/CD

## Next Steps

1. **IMMEDIATELY**: Fix critical SQL injection (search.py:45)
2. **BEFORE MERGE**: Fix critical command injection (processor.py:78)
3. **BEFORE MERGE**: Remove hardcoded API key (config.py:12)
4. **FOLLOW-UP**: Implement defense-in-depth recommendations

**DO NOT MERGE** until critical and high-severity issues are resolved.
```

## Integration with Development Workflow

After security review:

1. **Fix vulnerabilities**: Address critical and high findings
2. **Re-run security review**: Verify fixes are effective
3. **Update security docs**: Document new security measures
4. **Create follow-up tasks**: Track medium-severity and defense-in-depth items
5. **Review with team**: Discuss findings and prevention strategies

## Remember

- **Zero tolerance for critical vulnerabilities**: Never merge code with critical security issues
- **Evidence-based**: Only report vulnerabilities you can exploit
- **Clear impact**: Explain real-world consequences
- **Actionable fixes**: Provide specific remediation code
- **Learn and prevent**: Use findings to improve development practices
