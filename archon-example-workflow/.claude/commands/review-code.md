---
description: Perform pragmatic code review on recent changes with structured feedback across 7 quality dimensions
---

# Code Review Workflow

Perform comprehensive code quality review on your changes before committing or creating a PR.

## Usage

```bash
# Review all uncommitted changes
/review-code

# Review specific files
/review-code path/to/file1.ts path/to/file2.ts

# Review a specific commit
/review-code <commit-hash>

# Review changes in current branch vs main
/review-code main...HEAD
```

## Step 1: Gather Changes

Determine what to review based on user input or current git state:

```bash
# If no args provided, review uncommitted changes
git status
git diff

# If commit hash provided, review that commit
git show <commit-hash>

# If branch comparison provided (e.g., main...HEAD)
git diff <comparison>

# If file paths provided, review those files
git diff -- <file1> <file2>
```

Store the diff content for review.

## Step 2: Search Archon Knowledge Base

Before reviewing, gather project-specific context:

Use Archon MCP tools to find relevant standards and patterns:

```bash
# Search for coding standards
rag_search_knowledge_base(query="coding standards", match_count=5)

# Find security guidelines
rag_search_knowledge_base(query="security best practices", match_count=3)

# Search for similar code patterns
rag_search_code_examples(query="<relevant pattern from diff>", match_count=3)

# Get available sources
rag_get_available_sources()
```

Store any relevant findings to inform the review.

## Step 3: Invoke Code Review Agent

Use the Task tool to invoke the code-reviewer specialist agent:

```xml
<use_task_tool>
{
  "subagent_type": "code-reviewer",
  "prompt": "Review the following code changes:

**Changes Summary:**
[Describe what changed - files, number of lines, type of change]

**Git Diff:**
```
[Paste the diff content here]
```

**Project Context from Knowledge Base:**
[Include relevant standards, patterns, or guidelines found]

**Focus Areas:**
[If user specified focus areas, include them - e.g., \"focus on security\" or \"check performance\"]

Provide structured code review following the 7-level hierarchy:
1. Architectural Design & Integrity
2. Functionality & Correctness
3. Security
4. Maintainability & Readability
5. Testing Strategy
6. Performance & Scalability
7. Dependencies & Documentation
",
  "description": "Perform pragmatic code review"
}
</use_task_tool>
```

## Step 4: Present Review Results

Once the code-reviewer agent completes, present the results to the user in a clear format:

1. **Summary**: Overall assessment and recommendation
2. **Critical Issues**: Must fix before merge
3. **High Priority**: Should fix before merge
4. **Medium Priority**: Consider for follow-up
5. **Positive Observations**: What's working well

## Step 5: Optional - Create Tasks for Findings

If user wants to track review findings in Archon:

```bash
# Ask user if they want to create tasks
"Would you like me to create Archon tasks for the critical and high-priority findings?"

# If yes, create tasks:
# For each critical/high finding:
manage_task(
  action="create",
  project_id="<project-id>",
  title="[Code Review] <issue-title>",
  description="<finding-details>",
  status="todo",
  tags=["code-review", "<severity>", "<category>"]
)
```

## Notes

- **Be pragmatic**: Focus on high-impact issues, not nitpicks
- **Provide context**: Explain WHY issues matter
- **Give examples**: Show specific fixes when possible
- **Stay positive**: Acknowledge good patterns too
- **Confidence threshold**: Only report issues with >80% confidence

## Example Output Format

```markdown
# Code Review: <Change Summary>

## Summary
- **Files Changed**: 5
- **Lines Modified**: +120, -45
- **Change Type**: Feature enhancement
- **Overall Assessment**: Ready to merge with minor improvements

## Critical Issues 🚨
None found - great work on security and correctness!

## High Priority ⚠️

### 1. Missing Error Handling in API Call
- **File**: `src/api/users.ts:45`
- **Category**: Functionality & Correctness
- **Issue**: API call lacks error handling, could crash app on network failure
- **Impact**: Poor user experience and potential data loss
- **Recommendation**: Wrap in try-catch and show user-friendly error message

## Medium Priority 💡

### 1. Function Complexity
- **File**: `src/utils/parser.ts:120`
- **Category**: Maintainability
- **Issue**: 80-line function doing too many things
- **Recommendation**: Consider extracting parsing steps into separate functions

## Positive Observations ✅
- Excellent test coverage for new features
- Clear naming conventions throughout
- Good use of TypeScript types
- Proper separation of concerns

## Next Steps
1. Address high-priority error handling issue
2. Consider refactoring complex function (optional)
3. All other changes look good!
```
