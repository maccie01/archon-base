# Archon MCP & Agents Architecture Guide

**Created**: 2025-10-13
**Purpose**: Comprehensive guide to Archon's MCP tools, agent architecture, and usage patterns

---

## Table of Contents

1. [Currently Exposed MCP Tools](#currently-exposed-mcp-tools)
2. [How Agents Are Meant to Be Used](#how-agents-are-meant-to-be-used)
3. [Architecture Patterns](#architecture-patterns)
4. [Integration Examples](#integration-examples)
5. [Best Practices](#best-practices)

---

## Currently Exposed MCP Tools

Archon exposes MCP tools through a **microservices architecture** where the MCP server (port 8051) makes HTTP calls to the API server (port 8181) and agents service (port 8052).

### Complete List of MCP Tools

**Source**: `python/src/mcp_server/mcp_server.py` (lines 422-531)

#### 1. **RAG / Knowledge Base Tools** (Read-Only)

**Module**: `python/src/mcp_server/features/rag/rag_tools.py`

```python
@mcp.tool()
async def rag_get_available_sources(ctx: Context) -> str:
    """Get list of available sources in the knowledge base.

    Returns:
        JSON with sources containing: id, title, url, summary, tags
    """

@mcp.tool()
async def rag_search_knowledge_base(
    ctx: Context,
    query: str,
    source_id: str | None = None,
    match_count: int = 5,
    return_mode: str = "pages"
) -> str:
    """Search knowledge base for relevant content using RAG.

    IMPORTANT: Keep queries SHORT (2-5 keywords) for best results!
    ✅ GOOD: "vector search pgvector"
    ❌ BAD: "how to implement vector search with pgvector in PostgreSQL"

    Args:
        query: 2-5 keyword search query
        source_id: Filter to specific source (from rag_get_available_sources)
        match_count: Number of results (default: 5)
        return_mode: "pages" (full pages) or "chunks" (text snippets)
    """

@mcp.tool()
async def rag_search_code_examples(
    ctx: Context,
    query: str,
    source_id: str | None = None,
    match_count: int = 3
) -> str:
    """Search for relevant code examples in the knowledge base.

    Args:
        query: 2-5 keywords describing the code pattern
        source_id: Filter to specific source
        match_count: Number of examples (default: 3)
    """

@mcp.tool()
async def rag_list_pages_for_source(
    ctx: Context,
    source_id: str
) -> str:
    """List all pages for a given knowledge source.

    Useful for browsing documentation structure.
    """

@mcp.tool()
async def rag_read_full_page(
    ctx: Context,
    page_id: str = None,
    page_url: str = None
) -> str:
    """Retrieve full page content from knowledge base.

    Use either page_id or page_url to specify the page.
    """
```

**Note**: Knowledge base population (crawling, uploading) is **NOT** exposed via MCP. Use:
- Archon UI at `http://localhost:3737`
- Direct API calls to `http://localhost:8181/api/knowledge-items/crawl` or `/api/documents/upload`

#### 2. **Project Management Tools**

**Module**: `python/src/mcp_server/features/projects/project_tools.py`

```python
@mcp.tool()
async def find_projects(
    ctx: Context,
    query: str | None = None,
    project_id: str | None = None,
    page: int = 1,
    per_page: int = 10
) -> str:
    """Find projects - supports list, search, and get single project.

    Usage patterns:
    - List all: find_projects()
    - Search: find_projects(query="authentication")
    - Get specific: find_projects(project_id="proj-123")
    """

@mcp.tool()
async def manage_project(
    ctx: Context,
    action: str,  # "create" | "update" | "delete"
    project_id: str | None = None,
    title: str | None = None,
    description: str | None = None,
    github_repo: str | None = None,
    # ... additional fields
) -> str:
    """Manage projects with consolidated create/update/delete actions.

    Examples:
    - Create: manage_project("create", title="My Feature", description="...")
    - Update: manage_project("update", project_id="proj-123", title="New Title")
    - Delete: manage_project("delete", project_id="proj-123")
    """
```

#### 3. **Task Management Tools**

**Module**: `python/src/mcp_server/features/tasks/task_tools.py`

```python
@mcp.tool()
async def find_tasks(
    ctx: Context,
    query: str | None = None,
    task_id: str | None = None,
    filter_by: str | None = None,  # "status" | "project" | "assignee"
    filter_value: str | None = None,
    page: int = 1,
    per_page: int = 10
) -> str:
    """Find tasks - supports list, search, filter, and get single task.

    Usage patterns:
    - List all: find_tasks()
    - Search: find_tasks(query="authentication")
    - Get specific: find_tasks(task_id="task-123")
    - Filter by status: find_tasks(filter_by="status", filter_value="todo")
    - Filter by project: find_tasks(filter_by="project", filter_value="proj-123")
    """

@mcp.tool()
async def manage_task(
    ctx: Context,
    action: str,  # "create" | "update" | "delete"
    task_id: str | None = None,
    project_id: str | None = None,
    title: str | None = None,
    description: str | None = None,
    status: str | None = None,  # "todo" | "doing" | "review" | "done"
    assignee: str | None = None,
    task_order: int | None = None,  # 0-100 (higher = more priority)
    # ... additional fields
) -> str:
    """Manage tasks with consolidated create/update/delete actions.

    Examples:
    - Create: manage_task("create", project_id="proj-123", title="Implement API")
    - Update status: manage_task("update", task_id="task-123", status="doing")
    - Delete: manage_task("delete", task_id="task-123")
    """
```

**Task Status Flow**: `todo` → `doing` → `review` → `done`

#### 4. **Document Management Tools**

**Module**: `python/src/mcp_server/features/documents/document_tools.py`

```python
@mcp.tool()
async def find_documents(
    ctx: Context,
    project_id: str,
    document_id: str | None = None,
    query: str | None = None,
    document_type: str | None = None,  # "prd" | "technical_spec" | etc.
    page: int = 1,
    per_page: int = 10
) -> str:
    """Find documents within a project.

    Usage patterns:
    - List all: find_documents(project_id="proj-123")
    - Search: find_documents(project_id="proj-123", query="auth")
    - Filter by type: find_documents(project_id="proj-123", document_type="prd")
    - Get specific: find_documents(project_id="proj-123", document_id="doc-123")
    """

@mcp.tool()
async def manage_document(
    ctx: Context,
    action: str,  # "create" | "update" | "delete"
    project_id: str,
    document_id: str | None = None,
    title: str | None = None,
    document_type: str | None = None,
    content: dict | None = None,
    tags: list[str] | None = None,
    # ... additional fields
) -> str:
    """Manage documents with consolidated create/update/delete actions."""
```

#### 5. **Version Management Tools**

**Module**: `python/src/mcp_server/features/documents/version_tools.py`

```python
@mcp.tool()
async def find_versions(
    ctx: Context,
    project_id: str,
    version_id: str | None = None,
    page: int = 1,
    per_page: int = 10
) -> str:
    """Find version history for a project."""

@mcp.tool()
async def manage_version(
    ctx: Context,
    action: str,  # "create" | "restore"
    project_id: str,
    version_id: str | None = None,
    description: str | None = None,
    # ... additional fields
) -> str:
    """Manage versions - create snapshots or restore previous versions."""
```

#### 6. **Feature Management Tools**

**Module**: `python/src/mcp_server/features/feature_tools.py`

```python
@mcp.tool()
async def manage_features(
    ctx: Context,
    action: str,  # "enable" | "disable" | "get_status"
    feature_name: str | None = None
) -> str:
    """Manage optional features (e.g., projects feature toggle)."""
```

#### 7. **Health & Session Tools**

**Built-in** (in `mcp_server.py`):

```python
@mcp.tool()
async def health_check(ctx: Context) -> str:
    """Check health status of MCP server and dependencies."""

@mcp.tool()
async def session_info(ctx: Context) -> str:
    """Get current and active session information."""
```

### MCP Tool Naming Convention

All Archon MCP tools follow the pattern: `archon:<tool_name>`

When connected via MCP in Claude Code/Cursor/Windsurf, they appear as:
- `archon:rag_search_knowledge_base`
- `archon:find_projects`
- `archon:manage_task`
- etc.

---

## How Agents Are Meant to Be Used

Archon has **TWO distinct types of agents**:

### 1. **Backend PydanticAI Agents** (Internal)

**Location**: `python/src/agents/`

**Purpose**: Server-side AI agents that run **inside** the Archon backend services

**Available Agents**:

#### A. **Document Agent** (`document_agent.py`)

**Purpose**: Conversational document management

**Capabilities**:
- Create new documents (PRDs, technical specs, meeting notes)
- Update existing document content
- Modify document structure and metadata
- Query document information
- Track changes and maintain version history
- Create React Flow feature plans
- Generate ERDs with SQL schemas
- Request approval workflows

**Usage Pattern**:
```python
# Called via API endpoint: /api/agent-chat/document
from src.agents.document_agent import DocumentAgent

agent = DocumentAgent(model="openai:gpt-4o")
result = await agent.run_conversation(
    user_message="Create a PRD for user authentication",
    project_id="proj-123",
    user_id="user-456"
)
```

**Access**: Available through Archon UI's Agent Chat interface or direct API calls

#### B. **RAG Agent** (`rag_agent.py`)

**Purpose**: Intelligent knowledge base search with multi-step reasoning

**Capabilities**:
- Multi-step RAG queries with reasoning
- Automatic query refinement
- Source credibility assessment
- Cross-document synthesis

**Usage Pattern**:
```python
# Called via API endpoint: /api/knowledge/agentic-search
from src.agents.rag_agent import RAGAgent

agent = RAGAgent(model="openai:gpt-4o")
result = await agent.run_search(
    query="How do I implement JWT authentication?",
    source_ids=["src-123", "src-456"]
)
```

#### C. **Base Agent** (`base_agent.py`)

**Purpose**: Abstract base class for all PydanticAI agents

**Features**:
- Rate limiting with exponential backoff
- Error handling and retries
- Logging and monitoring
- Standard dependency injection
- Timeout protection (2 minutes)

**Creating New Agents**:
```python
from src.agents.base_agent import BaseAgent, ArchonDependencies
from pydantic import BaseModel
from pydantic_ai import Agent

class MyAgentOutput(BaseModel):
    result: str
    success: bool

class MyAgent(BaseAgent[ArchonDependencies, MyAgentOutput]):
    def _create_agent(self, **kwargs) -> Agent:
        agent = Agent(
            model=self.model,
            deps_type=ArchonDependencies,
            result_type=MyAgentOutput,
            system_prompt="You are a specialized agent...",
            **kwargs
        )

        @agent.tool
        async def my_tool(ctx: RunContext[ArchonDependencies], param: str) -> str:
            """Tool description."""
            return f"Result: {param}"

        return agent

    def get_system_prompt(self) -> str:
        return "My agent system prompt"
```

**Key Characteristics**:
- **Server-side execution**: Run in Archon backend (ports 8181 or 8052)
- **Internal tools**: Can call Supabase directly, use HTTP clients, etc.
- **Not exposed via MCP**: These are implementation details, not user-facing
- **Used by API endpoints**: Wrapped in FastAPI routes

### 2. **Claude Code Subagents** (External)

**Location**: `.claude/agents/` directories (project-specific)

**Purpose**: Specialized agents for **Claude Code IDE** that use MCP tools

**Example from archon-example-workflow**:

#### A. **Codebase Analyst Agent**

**File**: `archon-example-workflow/.claude/agents/codebase-analyst.md`

**Purpose**: Deep codebase pattern analysis and convention discovery

**Configuration**:
```markdown
---
name: "codebase-analyst"
description: "Use proactively to find codebase patterns, coding style and team standards"
model: "sonnet"
---

You are a specialized codebase analysis agent focused on discovering patterns...

## Analysis Methodology

### 1. Project Structure Discovery
- Start looking for Architecture docs rules files
- Continue with root-level config files
- Map directory structure
...

### 2. Pattern Extraction
- Find similar implementations
- Extract common patterns
- Identify naming conventions
...
```

**Usage in Claude Code**:
```bash
# In .claude/commands/create-plan.md
Use the codebase-analyst subagent via the Task tool to analyze the codebase
and discover patterns relevant to this feature.
```

#### B. **Validator Agent**

**File**: `archon-example-workflow/.claude/agents/validator.md`

**Purpose**: Testing specialist that creates unit tests

**Key Characteristics**:
- **Client-side execution**: Run in Claude Code IDE
- **Uses MCP tools**: Can call `archon:*` tools via MCP connection
- **Triggered by commands**: Invoked via Task tool in slash commands
- **No internal access**: Cannot directly access Supabase or Archon internals

---

## Architecture Patterns

### Pattern 1: MCP Tools for External Access

**Use Case**: AI IDE (Claude Code, Cursor, Windsurf) needs to interact with Archon

**Flow**:
```
Claude Code IDE
  ↓ (MCP connection)
archon:find_tasks()
  ↓ (HTTP call)
MCP Server (port 8051)
  ↓ (HTTP call)
API Server (port 8181)
  ↓ (database query)
Supabase
```

**Example**:
```bash
# In Claude Code
User: "What tasks do I have for project X?"

# Claude Code calls MCP tool
archon:find_tasks(filter_by="project", filter_value="proj-123")

# Returns JSON response
{
  "success": true,
  "tasks": [
    {"id": "task-1", "title": "Implement API", "status": "todo"},
    {"id": "task-2", "title": "Write tests", "status": "doing"}
  ]
}
```

### Pattern 2: Backend Agents for Complex Operations

**Use Case**: User needs conversational document creation or agentic RAG search

**Flow**:
```
User → Archon UI (port 3737)
  ↓ (HTTP request)
API Server (port 8181)
  ↓ (instantiate agent)
DocumentAgent / RAGAgent
  ↓ (LLM calls with tools)
OpenAI / Anthropic
  ↓ (tool calls)
Supabase / Knowledge Base
```

**Example**:
```python
# API endpoint: POST /api/agent-chat/document
async def chat_with_document_agent(request: AgentChatRequest):
    agent = DocumentAgent(model="openai:gpt-4o")
    result = await agent.run_conversation(
        user_message=request.message,
        project_id=request.project_id,
        user_id=request.user_id
    )
    return result
```

### Pattern 3: Claude Code Subagents with MCP Tools

**Use Case**: Specialized analysis or validation in Claude Code

**Flow**:
```
User types: /create-plan requirements.md
  ↓ (command expands to prompt)
Claude Code
  ↓ (Task tool invokes subagent)
@codebase-analyst subagent
  ↓ (uses MCP tools)
archon:rag_search_knowledge_base(query="FastAPI patterns")
  ↓
Returns analysis to main Claude session
```

**Example from archon-example-workflow**:

```markdown
<!-- .claude/commands/create-plan.md -->

## Step 1: Analyze Codebase Patterns

Use the codebase-analyst subagent to understand existing patterns:

<use_task_tool>
{
  "subagent_type": "codebase-analyst",
  "prompt": "Analyze the codebase to find patterns relevant to: [feature]",
  "description": "Analyze codebase patterns"
}
</use_task_tool>
```

### Pattern 4: Workflow Example (archon-example-workflow)

**archon-example-workflow** demonstrates the **recommended pattern** for using Archon with Claude Code:

#### Files Structure:
```
archon-example-workflow/
├── .claude/
│   ├── commands/
│   │   ├── create-plan.md      # Requirements → Implementation plan
│   │   ├── execute-plan.md     # Plan → Tracked implementation
│   │   └── primer.md           # Project context loader
│   ├── agents/
│   │   ├── codebase-analyst.md # Pattern analysis specialist
│   │   └── validator.md        # Testing specialist
│   └── CLAUDE.md               # Archon-first workflow rules
├── CLAUDE.md                    # Project-specific rules
└── README.md                    # Workflow documentation
```

#### Workflow Sequence:

**1. Create Plan** (`/create-plan requirements/feature.md`):

```markdown
<!-- .claude/commands/create-plan.md -->

**Step 1**: Read requirements file
**Step 2**: Search Archon knowledge base using MCP tools
  - archon:rag_search_knowledge_base(query="feature patterns")
  - archon:rag_search_code_examples(query="similar code")
**Step 3**: Invoke codebase-analyst subagent via Task tool
**Step 4**: Generate implementation plan (PRP)
  - Task breakdown with dependencies
  - Architecture and integration points
  - Code references and patterns
```

**2. Execute Plan** (`/execute-plan PRPs/feature.md`):

```markdown
<!-- .claude/commands/execute-plan.md -->

**Step 1**: Read implementation plan
**Step 2**: Create Archon project and tasks via MCP
  - archon:manage_project("create", title="Feature", description="...")
  - archon:manage_task("create", project_id="...", title="Task 1")
  - archon:manage_task("create", project_id="...", title="Task 2")
**Step 3**: For each task:
  - archon:manage_task("update", task_id="...", status="doing")
  - Implement the task
  - archon:manage_task("update", task_id="...", status="review")
**Step 4**: Invoke validator subagent for testing
**Step 5**: Mark tasks done
  - archon:manage_task("update", task_id="...", status="done")
```

**Key Insight**: The workflow uses **both** patterns:
- **MCP tools** for task management (`archon:manage_task`, `archon:find_tasks`)
- **Subagents** for specialized analysis (codebase-analyst, validator)

---

## Integration Examples

### Example 1: Task-Driven Development (Claude Code)

**Scenario**: Developer working on authentication feature

```bash
# In Claude Code with Archon MCP connected

# 1. List available tasks
User: "What tasks do I have?"
Claude: [Calls archon:find_tasks()]

# 2. Start working on task
User: "Start task-123"
Claude: [Calls archon:manage_task("update", task_id="task-123", status="doing")]

# 3. Research before implementation
User: "Search for JWT examples"
Claude: [Calls archon:rag_search_code_examples(query="JWT authentication")]

# 4. Implement feature
[Developer codes...]

# 5. Mark for review
User: "Mark task-123 for review"
Claude: [Calls archon:manage_task("update", task_id="task-123", status="review")]

# 6. Get next task
User: "What's next?"
Claude: [Calls archon:find_tasks(filter_by="status", filter_value="todo")]
```

### Example 2: Document Creation (Archon UI)

**Scenario**: Product manager creating PRD

```bash
# In Archon UI → Agent Chat → Document Agent

User: "Create a PRD for user authentication feature with OAuth support"

# Backend flow:
1. API receives request → /api/agent-chat/document
2. Instantiates DocumentAgent
3. Agent generates structured PRD with sections:
   - Project Overview
   - Goals
   - Scope
   - Technical Requirements
   - Architecture
   - User Stories
   - Timeline & Milestones
   - Risks & Mitigations
4. Saves to project documents via DocumentService
5. Returns success message with document ID
```

### Example 3: Knowledge Base Search (Both)

**Scenario A: Direct search via MCP (Claude Code)**

```bash
User: "Find Supabase vector function examples"

Claude:
1. [Calls archon:rag_get_available_sources()] → Get source list
2. [Finds Supabase docs source_id: "src-abc123"]
3. [Calls archon:rag_search_code_examples(
     query="vector functions",
     source_id="src-abc123",
     match_count=5
   )]
4. Returns relevant code examples
```

**Scenario B: Agentic search via backend (Archon UI)**

```bash
User: "How do I implement real-time subscriptions with Supabase?"

Archon UI:
1. API → /api/knowledge/agentic-search
2. Instantiates RAGAgent
3. Agent performs multi-step reasoning:
   - Initial search: "Supabase real-time subscriptions"
   - Refines query: "Supabase Realtime WebSocket setup"
   - Searches: "Supabase channel subscribe patterns"
   - Synthesizes results across sources
4. Returns comprehensive answer with source citations
```

### Example 4: Workflow Automation (archon-example-workflow)

**Scenario**: Building new feature from requirements

```bash
# Step 1: Write requirements
$ echo "Build REST API for user authentication with JWT" > requirements/auth-api.md

# Step 2: Generate plan in Claude Code
/create-plan requirements/auth-api.md

# Claude Code flow:
1. Reads requirements file
2. Searches knowledge base:
   - archon:rag_search_knowledge_base(query="JWT FastAPI")
   - archon:rag_search_code_examples(query="authentication patterns")
3. Invokes codebase-analyst subagent:
   - Analyzes project structure
   - Finds existing auth patterns
   - Discovers coding conventions
4. Generates PRPs/auth-api.md with:
   - 12 tasks (setup → implementation → testing)
   - Architecture diagram
   - Integration points
   - Code references

# Step 3: Execute plan
/execute-plan PRPs/auth-api.md

# Claude Code flow:
1. Reads implementation plan
2. Creates Archon project:
   - archon:manage_project("create", title="Auth API", ...)
3. Creates 12 tasks:
   - archon:manage_task("create", title="Setup environment", task_order=100)
   - archon:manage_task("create", title="Create JWT utils", task_order=90)
   - ...
4. For each task (todo → doing → review → done):
   - archon:manage_task("update", status="doing")
   - [Implements the task]
   - archon:manage_task("update", status="review")
   - [Invokes validator subagent for tests]
   - archon:manage_task("update", status="done")
5. All tasks complete → Feature implemented!
```

---

## Best Practices

### 1. MCP Tool Usage

**DO**:
- ✅ Use short queries (2-5 keywords) for RAG searches
- ✅ Filter searches by source_id when searching specific docs
- ✅ Update task status as you work (`todo` → `doing` → `review` → `done`)
- ✅ Only have ONE task in `doing` status at a time
- ✅ Search knowledge base before implementing

**DON'T**:
- ❌ Don't use long, verbose queries for RAG ("how to implement...")
- ❌ Don't skip task status updates
- ❌ Don't try to crawl/upload via MCP (use UI or API directly)
- ❌ Don't work on multiple tasks simultaneously

### 2. Backend Agent Usage

**When to use**:
- Conversational interfaces (chat-based operations)
- Complex multi-step operations requiring reasoning
- Operations that benefit from LLM intelligence (document generation, agentic search)

**When NOT to use**:
- Simple CRUD operations (use direct API calls)
- Performance-critical operations (agents add latency)
- Operations that don't need intelligence (data retrieval)

### 3. Claude Code Subagent Usage

**When to create subagents**:
- Specialized analysis (codebase patterns, security audits)
- Validation and testing (test generation, code review)
- Complex research requiring focused expertise
- Workflows that benefit from specialized prompts

**Best practices**:
- Give subagents clear, narrow responsibilities
- Provide specific tool allowlists
- Write detailed system prompts with examples
- Use Task tool to invoke subagents from commands

### 4. Workflow Design

**Recommended structure** (following archon-example-workflow):

```
.claude/
├── commands/          # User-facing workflows (slash commands)
│   ├── create-plan.md
│   ├── execute-plan.md
│   └── review-code.md
├── agents/            # Specialized subagents
│   ├── codebase-analyst.md
│   ├── security-auditor.md
│   └── validator.md
└── CLAUDE.md          # Workflow rules and instructions
```

**Command design**:
1. **Clear steps**: Number each step in the workflow
2. **Tool integration**: Explicitly call MCP tools
3. **Subagent invocation**: Use Task tool when specialized analysis needed
4. **Output format**: Specify expected deliverables

**Example**:
```markdown
<!-- .claude/commands/my-workflow.md -->

# Step 1: Gather Context
- Read input file: [file path]
- Search knowledge base: archon:rag_search_knowledge_base(query="...")

# Step 2: Analyze Patterns
Use codebase-analyst subagent via Task tool to discover existing patterns.

# Step 3: Create Tasks
- archon:manage_project("create", ...)
- archon:manage_task("create", ...)

# Step 4: Implement
For each task:
- archon:manage_task("update", status="doing")
- [Implementation]
- archon:manage_task("update", status="done")
```

---

## Key Architectural Decisions

### 1. Why Separate MCP Tools and Backend Agents?

**MCP Tools** (External, Client-facing):
- **Purpose**: Expose Archon functionality to AI IDEs
- **Access**: Read-only knowledge base, full task/project management
- **Security**: Validated HTTP requests, session management
- **Use Case**: Developer workflow automation

**Backend Agents** (Internal, Server-side):
- **Purpose**: Complex AI operations requiring context and reasoning
- **Access**: Direct database access, internal service calls
- **Performance**: Can cache, optimize, batch operations
- **Use Case**: Document generation, agentic search, conversational interfaces

**Rationale**: Separation of concerns - external tools for integration, internal agents for intelligence.

### 2. Why Read-Only Knowledge Base via MCP?

**Current Design**:
- MCP tools: Read-only (`rag_search_*`, `rag_get_*`, `rag_read_*`)
- Population: UI or direct API calls

**Rationale**:
- **Performance**: Crawling/uploading are slow, long-running operations
- **Progress tracking**: Need real-time progress updates (WebSocket/SSE)
- **Error handling**: Complex failure scenarios (rate limits, timeouts)
- **UX**: Better handled by dedicated UI with progress bars

**Future**: Could add MCP tools for crawling if async progress tracking is solved.

### 3. Why Use PydanticAI for Backend Agents?

**Advantages**:
- **Structured outputs**: Pydantic models ensure type safety
- **Tool integration**: Easy to register Python functions as tools
- **Rate limiting**: Built-in retry logic with exponential backoff
- **Validation**: Automatic input/output validation
- **Type hints**: Full IDE support and static analysis

**Example**:
```python
class DocumentOperation(BaseModel):
    operation_type: str
    document_id: str | None
    success: bool
    message: str

agent = Agent(
    model="openai:gpt-4o",
    result_type=DocumentOperation,
    # Agent MUST return valid DocumentOperation
)
```

### 4. Why Use archon-example-workflow Pattern?

**Benefits**:
- **Systematic**: Enforces planning → execution workflow
- **Knowledge-augmented**: Leverages Archon's knowledge base
- **Task-tracked**: Full visibility into progress
- **Pattern-consistent**: Codebase analysis ensures consistency
- **Reusable**: Template structure adaptable to any project

**Adoption**: Copy `.claude/` directory to any project → instant workflow support

---

## Summary: How to Use Archon

### For AI IDE Users (Claude Code, Cursor, Windsurf)

1. **Connect Archon MCP server** (configuration in IDE settings)
2. **Use MCP tools directly** for task management and knowledge search
3. **Create slash commands** in `.claude/commands/` for workflows
4. **Define subagents** in `.claude/agents/` for specialized tasks
5. **Follow archon-example-workflow** pattern for systematic development

### For Archon Backend Developers

1. **Expose functionality via MCP tools** in `python/src/mcp_server/features/`
2. **Create backend agents** in `python/src/agents/` for complex operations
3. **Extend BaseAgent** for new agent types
4. **Register agents in API routes** for UI/API access
5. **Document MCP tools** in MCP_INSTRUCTIONS in `mcp_server.py`

### For Workflow Designers

1. **Start with archon-example-workflow** as template
2. **Design slash commands** that orchestrate MCP tools
3. **Create specialized subagents** for analysis/validation
4. **Write clear system prompts** with examples
5. **Test workflows end-to-end** with real projects

---

## Next Steps for Integration

Based on the claude-code-workflows analysis, here's how the new review agents should be integrated:

### Recommended Approach: **Hybrid Model**

**Code Review, Security Review, Design Review** should follow **BOTH patterns**:

#### 1. Backend PydanticAI Agents (for API/UI)
```
python/src/agents/features/
├── code_review/
│   └── code_review_agent.py        # PydanticAI agent
├── security_review/
│   └── security_review_agent.py    # PydanticAI agent
└── design_review/
    └── design_review_agent.py      # PydanticAI agent
```

**Usage**: Via API endpoints or Archon UI

#### 2. MCP Tools (for AI IDE access)
```
python/src/mcp_server/features/
├── code_review/
│   └── code_review_tools.py        # MCP tool wrapper
├── security_review/
│   └── security_review_tools.py    # MCP tool wrapper
└── design_review/
    └── design_review_tools.py      # MCP tool wrapper
```

**Usage**: Via `archon:review_code`, `archon:security_review`, `archon:design_review` in Claude Code

#### 3. Claude Code Subagents (for workflows)
```
.claude/agents/
├── code-reviewer.md      # Slash command subagent
├── security-auditor.md   # Slash command subagent
└── design-reviewer.md    # Slash command subagent
```

**Usage**: Via Task tool in `/review-code`, `/security-review`, `/design-review` commands

**Why Hybrid?**
- **Flexibility**: Available in UI, API, and IDE
- **Context**: Backend agents can access full project context
- **Performance**: MCP tools for quick checks, agents for deep analysis
- **Workflows**: Subagents enable automated review workflows

---

*Created: 2025-10-13*
*Last Updated: 2025-10-13*
*Document Version: 1.0*
