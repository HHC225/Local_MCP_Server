# Planning Tool Documentation

## Overview

The Planning Tool is an advanced Work Breakdown Structure (WBS) creation tool designed to help break down complex software development projects into manageable, hierarchical tasks before implementation. It uses a step-by-step planning process similar to Sequential Thinking, but focuses specifically on project decomposition, task identification, and dependency mapping.

## Core Concept

The Planning Tool prevents common development issues by ensuring thorough planning with:
- **Hierarchical task breakdown** (1.0 → 1.1 → 1.1.1)
- **Dependency mapping** between tasks
- **Priority assignment** for each task
- **Progressive WBS generation** during planning
- **Detailed implementation guidance** for AI agents
- **Automatic session management** with intelligent session detection

## Architecture

The Planning Tool consists of four main components:

### 1. PlanningValidator
Validates input data and WBS hierarchy integrity:
- Required field validation (`planning_step`, `step_number`, `total_steps`, `next_step_needed`)
- **CRITICAL parent_id validation**: All child items (level > 0) MUST have `parent_id` specified
- Hierarchical structure validation (no missing parent references)
- Circular dependency detection
- Data type checking
- Duplicate ID detection with warnings

### 2. PlanningSessionManager
Manages planning session lifecycle:
- Session creation with auto-generated IDs (`planning_YYYYMMDD_HHMMSS`)
- **Automatic session continuation**: Finds most recent active session for steps > 1
- WBS item merging (duplicate prevention)
- Parent-child relationship automatic rebuilding
- Planning history tracking with step records

### 3. WBSMarkdownGenerator
Generates structured markdown files:
- Hierarchical numbering (1, 1.1, 1.2.1, etc.) with automatic calculation
- Dependency formatting with task number and title display
- Checkbox generation for task tracking (unchecked by default)
- Planning summary with priority breakdown statistics
- Critical path analysis (top 5 tasks with most dependencies)
- Metadata section with session ID and timestamps

### 4. PlanningTool
Main orchestrator that coordinates all components:
- Input validation with detailed error messages
- **Smart session management**: Creates new session for step 1, continues existing for subsequent steps
- WBS item processing with validation and hierarchy building
- Progressive file generation (export on completion or when explicitly requested)
- Response formatting with progress tracking

## Data Structures

### WBSItem
```python
@dataclass
class WBSItem:
    id: str                          # Unique task identifier (e.g., "setup", "database-1")
    title: str                       # Task title
    description: str                 # Detailed implementation instructions
    level: int                       # Hierarchy level (0-4)
    priority: str                    # High/Medium/Low
    dependencies: List[str]          # Task IDs this depends on
    order: int                       # Order among siblings (default: 0)
    parent_id: Optional[str]         # Parent task ID (REQUIRED for level > 0)
    children: List[str]              # Child task IDs (auto-populated)
```

**CRITICAL REQUIREMENTS:**
- `parent_id` is **MANDATORY** for all child items (level > 0)
- `parent_id` MUST reference an existing parent item
- Do NOT rely on automatic inference - always specify `parent_id` explicitly
- `children` list is automatically maintained by the system

### PlanningStep
```python
@dataclass
class PlanningStep:
    step_number: int                 # Step number in planning sequence
    planning_step: str               # Planning analysis content
    timestamp: str                   # ISO 8601 timestamp
    wbs_items_added: int             # Number of items added in this step
    is_revision: bool                # Whether this is a revision
    revises_step: Optional[int]      # Which step is being revised
    branch_id: Optional[str]         # Branch identifier for alternatives
```

### PlanningSession
```python
@dataclass
class PlanningSession:
    id: str                          # Session identifier (auto-generated)
    problem_statement: str           # Original problem
    project_name: str                # Project name (auto-generated if not provided)
    status: str                      # active/completed/paused
    created_at: str                  # ISO 8601 creation timestamp
    last_updated: str                # ISO 8601 update timestamp
    wbs_items: List[WBSItem]        # All WBS items
    planning_history: List[PlanningStep]  # Planning steps history
    total_steps: Optional[int]       # Estimated total steps
    current_step: int                # Current step number
    output_path: Optional[str]       # WBS file path (set after export)
```

## Planning Workflow

### Step 1: Problem Analysis
Start by analyzing the problem and breaking it down. **Session is automatically created** with `problem_statement` and optional `project_name`:

```python
result = await planning(
    planning_step="""
    Analyzing requirement: Build a REST API for user management
    
    Main components identified:
    - Database layer (PostgreSQL)
    - API endpoints (Express.js)
    - Authentication (JWT)
    - User CRUD operations
    """,
    step_number=1,
    total_steps=5,
    next_step_needed=True,
    problem_statement="Build a REST API for user management with authentication",  # REQUIRED for step 1
    project_name="User Management API"  # Optional, auto-generated if not provided
)
```

**Step 1 Behavior:**
- Creates new session with auto-generated ID (`planning_YYYYMMDD_HHMMSS`)
- `problem_statement` is **REQUIRED**
- `project_name` is optional (auto-generated from first 5 words of problem statement)
- No WBS items required in step 1 (analysis phase)

### Step 2: Task Identification
Create main tasks with WBS items. **Session is automatically continued** from step 1:

```python
result = await planning(
    planning_step="""
    Identified main tasks and created WBS structure:
    - Environment setup
    - Database design
    - API implementation
    - Testing
    """,
    step_number=2,
    total_steps=5,
    next_step_needed=True,
    # No session_id needed - automatically finds most recent active session
    wbs_items=[
        {
            "id": "setup",
            "title": "Environment Setup",
            "description": "Initialize project structure and install dependencies",
            "level": 0,
            "priority": "High",
            "dependencies": [],
            "order": 1
            # No parent_id for level 0 (root level tasks)
        },
        {
            "id": "database",
            "title": "Database Design",
            "description": "Design and implement database schema",
            "level": 0,
            "priority": "High",
            "dependencies": ["setup"],  # Depends on setup task
            "order": 2
        }
    ]
)
```

**Step 2+ Behavior:**
- Automatically finds most recent active session (no manual session tracking needed)
- Returns error if no active session found (must start with step 1)
- WBS items are added and validated
- Parent-child relationships are automatically built

### Step 3: Subtask Breakdown
Break down main tasks into subtasks. **CRITICAL: Must specify `parent_id` for all child items:**

```python
result = await planning(
    planning_step="""
    Breaking down Environment Setup into subtasks:
    - Create project directory
    - Initialize npm package
    - Install Express, PostgreSQL client
    - Configure TypeScript
    """,
    step_number=3,
    total_steps=5,
    next_step_needed=True,
    wbs_items=[
        {
            "id": "setup-1",
            "title": "Create Project Structure",
            "description": "Create directories: src/, tests/, config/. Initialize git repository.",
            "level": 1,
            "priority": "High",
            "dependencies": [],
            "parent_id": "setup",  # REQUIRED for level > 0
            "order": 1
        },
        {
            "id": "setup-2",
            "title": "Install Dependencies",
            "description": "Run: npm install express pg jsonwebtoken bcrypt typescript @types/node",
            "level": 1,
            "priority": "High",
            "dependencies": ["setup-1"],  # Must wait for project structure
            "parent_id": "setup",  # REQUIRED - same parent
            "order": 2
        }
    ]
)
```

**Critical Requirements for Child Items:**
- `parent_id` is **MANDATORY** for all items with `level > 0`
- `parent_id` MUST reference an existing parent task ID
- Validation will fail if `parent_id` is missing or references non-existent task
- Error message: "Item {id}: 'parent_id' is REQUIRED for child items (level > 0)"

### Step 4: Dependency Mapping
Add dependencies between tasks:

```python
result = await planning(
    planning_step="""
    Mapping dependencies across all tasks:
    - API implementation depends on database schema
    - Testing depends on API implementation
    - Each subtask has clear prerequisites
    """,
    step_number=4,
    total_steps=5,
    next_step_needed=True,
    wbs_items=[
        {
            "id": "api",
            "title": "API Implementation",
            "description": "Implement REST endpoints for user operations",
            "level": 0,
            "priority": "High",
            "dependencies": ["database"],
            "order": 3
        }
    ]
)
```

### Step 5: Completion
Finalize planning and generate final WBS:

```python
result = await planning(
    planning_step="""
    Planning complete. Created comprehensive WBS with:
    - 4 main tasks
    - 12 subtasks
    - Clear dependencies
    - Priority assignments
    - Detailed descriptions
    """,
    step_number=5,
    total_steps=5,
    next_step_needed=False
)
```

## WBS Output Format

The generated markdown file follows this structure:

```markdown
# Project: User Management API

## Problem Statement
Build a REST API for user management with authentication

## Work Breakdown Structure

- [ ] **Environment Setup** (Priority: High)
  - Task ID: 1
  - Description: Initialize project structure and install dependencies
  - Dependencies: None

  - [ ] **Create Project Structure** (Priority: High)
    - Task ID: 1.1
    - Description: Create directories: src/, tests/, config/. Initialize git repository.
    - Dependencies: None

  - [ ] **Install Dependencies** (Priority: High)
    - Task ID: 1.2
    - Description: Run: npm install express pg jsonwebtoken bcrypt typescript @types/node
    - Dependencies: 1.1 (Create Project Structure)

- [ ] **Database Design** (Priority: High)
  - Task ID: 2
  - Description: Design and implement database schema
  - Dependencies: 1 (Environment Setup)

## Planning Summary

- **Total Planning Steps**: 5
- **Total WBS Items**: 4
- **Status**: completed
- **Created**: 2025-10-17T14:30:22
- **Last Updated**: 2025-10-17T14:35:45

### Priority Breakdown
- High: 3
- Medium: 1
- Low: 0

## Critical Path Analysis

### Tasks with Most Dependencies
- **3** API Implementation (2 dependencies)
- **4** Testing (1 dependencies)

## Planning Metadata

- **Session ID**: planning_20251017_143022
- **Project Name**: User Management API
- **Generated**: 2025-10-17T14:35:45
```

**Output Format Details:**
- Hierarchical numbering: 1, 1.1, 1.2, 2, 2.1, 2.2, etc. (calculated automatically)
- All checkboxes are `[ ]` (unchecked) by default
- Dependencies show both task number and title for clarity
- Planning summary includes priority breakdown statistics
- Critical path shows top 5 tasks with most dependencies
- Metadata includes session ID and generation timestamp

## Best Practices

### 1. Parent vs Child Task Descriptions

**PARENT TASKS (Level 0-1)**: High-level summaries only
```python
{
    "id": "database",
    "title": "Database Design",
    "description": "Design and implement database schema",  # Summary
    "level": 0
}
```

**CHILD TASKS (Level 2+)**: Detailed, actionable instructions
```python
{
    "id": "database-schema",
    "title": "Create User Table",
    "description": """
    Create PostgreSQL table with:
    - id: UUID primary key
    - email: VARCHAR(255) UNIQUE NOT NULL
    - password_hash: VARCHAR(255) NOT NULL
    - created_at: TIMESTAMP DEFAULT NOW()
    
    Run migration: npm run migrate:up
    """,  # Detailed implementation steps
    "level": 2
}
```

### 2. Dependency Specification

Use clear, consistent dependency references:

```python
# Good: Using task IDs
"dependencies": ["setup", "database"]

# Good: Using hierarchical numbers (in WBS items as strings)
"dependencies": ["1.1", "2.3"]

# Good: Using task titles
"dependencies": ["Database Setup", "API Configuration"]

# Bad: Mixed formats
"dependencies": ["setup", "1.1", "Some Task"]
```

### 3. Progressive Planning

Generate markdown files incrementally:

```python
# Force markdown generation even if not complete
result = await planning(
    planning_step="...",
    step_number=3,
    total_steps=5,
    next_step_needed=True,
    generate_markdown=True,  # Generate now
    export_to_file=True
)
```

### 4. Hierarchy Levels

Follow the hierarchy level guidelines:

| Level | Purpose | Example |
|-------|---------|---------|
| 0 | Main phases | "Environment Setup", "API Development" |
| 1 | Major tasks | "Install Dependencies", "Create Endpoints" |
| 2 | Subtasks | "Install Express", "Create User Endpoint" |
| 3 | Detailed steps | "Configure CORS middleware" |
| 4 | Micro tasks | "Add rate limiting to endpoint" |

### 5. Priority Assignment

Assign priorities based on:
- **High**: Critical path, blockers, must-have features
- **Medium**: Important but not blocking
- **Low**: Nice-to-have, optimization tasks

## Integration with WBS Execution

After creating a WBS with the Planning Tool, use the WBS Execution Tool to implement it:

```python
# 1. Create WBS with Planning Tool
planning_result = await planning(...)

# 2. Execute WBS with WBS Execution Tool
execution_result = await wbs_execution(
    action="start",
    wbs_file_path=planning_result.output_path
)
```

## Error Handling

### Circular Dependencies
```python
# This will be detected and rejected with detailed error message
wbs_items=[
    {"id": "task1", "dependencies": ["task2"], "level": 0, "title": "Task 1", "priority": "High"},
    {"id": "task2", "dependencies": ["task1"], "level": 0, "title": "Task 2", "priority": "High"}
]

# Error response:
{
  "success": false,
  "error": "Circular dependencies detected",
  "details": ["task2 -> task1"]
}
```

### Missing parent_id for Child Items
```python
# This will FAIL validation
wbs_items=[
    {
        "id": "child-task",
        "title": "Child Task",
        "level": 1,  # level > 0 requires parent_id
        "priority": "High"
        # Missing parent_id - VALIDATION ERROR
    }
]

# Error response:
{
  "success": false,
  "error": "WBS items validation failed",
  "details": [
    "Item child-task: 'parent_id' is REQUIRED for child items (level > 0). Current level: 1"
  ]
}
```

### Non-existent Parent Reference
```python
# This will FAIL validation
wbs_items=[
    {
        "id": "child-task",
        "title": "Child Task",
        "level": 1,
        "priority": "High",
        "parent_id": "nonexistent"  # Parent doesn't exist
    }
]

# Error response:
{
  "success": false,
  "error": "WBS items validation failed",
  "details": [
    "Item child-task: parent_id 'nonexistent' does not exist. Parent must be added before child."
  ]
}
```

### Duplicate IDs
```python
# Duplicate IDs are skipped with warning (no error)
wbs_items=[
    {"id": "task1", "title": "First", "level": 0, "priority": "High"},
    {"id": "task1", "title": "Duplicate", "level": 0, "priority": "High"}  # Skipped
]

# Response with warning:
{
  "success": true,
  "warnings": ["Item task1: Duplicate ID, will be skipped or merged"]
}
```

### Missing Dependencies
```python
# Warning issued for missing dependency (not an error)
wbs_items=[
    {
        "id": "task1",
        "title": "Task 1",
        "level": 0,
        "priority": "High",
        "dependencies": ["nonexistent"]  # Dependency doesn't exist yet
    }
]

# Response with warning:
{
  "success": true,
  "warnings": ["Item task1: Dependency 'nonexistent' not found"]
}
```

### No Active Session Found
```python
# Starting from step 2 without step 1
result = await planning(
    planning_step="...",
    step_number=2,  # Step > 1
    total_steps=5,
    next_step_needed=True
)

# Error response:
{
  "success": false,
  "error": "No active planning session found. Start with step_number=1"
}
```

## Advanced Features

### Revision Support
Revise previous planning steps:

```python
result = await planning(
    planning_step="Revising task breakdown based on new requirements",
    step_number=6,
    total_steps=7,
    next_step_needed=True,
    is_revision=True,
    revises_step=3,  # Revising step 3
    wbs_items=[...]  # Updated items
)
```

### Branch Planning
Create alternative planning branches:

```python
result = await planning(
    planning_step="Exploring alternative architecture",
    step_number=4,
    total_steps=6,
    next_step_needed=True,
    branch_from_step=2,
    branch_id="microservices-alternative"
)
```

### Custom Output Path
Specify custom WBS file location:

```python
result = await planning(
    planning_step="...",
    step_number=5,
    total_steps=5,
    next_step_needed=False,
    output_path="/custom/path/my_wbs.md"
)
```

## API Reference

### planning()

```python
async def planning(
    planning_step: str,              # Current planning analysis (REQUIRED)
    step_number: int,                # Current step, min: 1 (REQUIRED)
    total_steps: int,                # Estimated total steps, min: 1 (REQUIRED)
    next_step_needed: bool,          # Whether more steps needed (REQUIRED)
    problem_statement: str = None,   # REQUIRED for step 1 only
    project_name: str = None,        # Optional, auto-generated if not provided
    wbs_items: List[Dict] = None,    # WBS items to add (optional)
    refine_wbs: bool = False,        # Refine existing WBS (currently unused)
    is_revision: bool = False,       # Revision flag
    revises_step: int = None,        # Step being revised (required if is_revision=True)
    branch_from_step: int = None,    # Branch starting point
    branch_id: str = None,           # Branch identifier
    generate_markdown: bool = False, # Force markdown generation before completion
    export_to_file: bool = True,     # Export to file (default: True)
    output_path: str = None,         # Custom output path (optional)
    action_required: bool = False,   # Action flag (optional)
    action_type: str = None,         # Action type (optional)
    action_description: str = None   # Action description (optional)
) -> str:  # JSON response
```

### Required Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `planning_step` | str | ✅ Always | Current planning analysis content |
| `step_number` | int | ✅ Always | Current step number (1-based) |
| `total_steps` | int | ✅ Always | Estimated total steps needed |
| `next_step_needed` | bool | ✅ Always | Whether more steps are needed |
| `problem_statement` | str | ✅ Step 1 only | Problem to solve (creates new session) |

### Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `project_name` | str | Auto-generated | Project name (from first 5 words of problem) |
| `wbs_items` | List[Dict] | None | WBS items to add in this step |
| `is_revision` | bool | False | Whether revising previous step |
| `revises_step` | int | None | Which step number to revise |
| `branch_from_step` | int | None | Branch starting point |
| `branch_id` | str | None | Branch identifier |
| `generate_markdown` | bool | False | Force markdown generation mid-planning |
| `export_to_file` | bool | True | Export markdown to file |
| `output_path` | str | Auto-generated | Custom file path (default: `./output/planning/{project_name}_WBS.md`) |

### Response Format

**Success Response (Planning in Progress):**
```json
{
  "success": true,
  "sessionId": "planning_20251017_143022",
  "stepNumber": 3,
  "totalSteps": 5,
  "nextStepNeeded": true,
  "wbsItemsCount": 8,
  "wbsItemsAdded": 3,
  "status": "active",
  "message": "Step 3/5 completed (60%). Continue with next planning step."
}
```

**Success Response (Planning Complete with File Export):**
```json
{
  "success": true,
  "sessionId": "planning_20251017_143022",
  "stepNumber": 5,
  "totalSteps": 5,
  "nextStepNeeded": false,
  "wbsItemsCount": 12,
  "wbsItemsAdded": 2,
  "status": "completed",
  "message": "Planning completed! Generated WBS with 12 items.",
  "outputPath": "/path/to/output/planning/User_Management_API_WBS.md",
  "markdownGenerated": true
}
```

**Error Response (Validation Failed):**
```json
{
  "success": false,
  "error": "Input validation failed",
  "details": [
    "step_number (6) cannot exceed total_steps (5)",
    "planning_step is required and must be a string"
  ]
}
```

**Error Response (WBS Validation Failed):**
```json
{
  "success": false,
  "error": "WBS items validation failed",
  "details": [
    "Item child-task: 'parent_id' is REQUIRED for child items (level > 0). Current level: 1",
    "Item api: 'priority' must be High, Medium, or Low"
  ],
  "warnings": [
    "Item task1: Dependency 'nonexistent' not found"
  ]
}
```

## Troubleshooting

### "No active planning session found"
**Problem**: Error when calling with `step_number > 1`

**Solution**: 
- Always start with `step_number=1` which includes `problem_statement`
- Session is automatically created and tracked
- Subsequent steps (2, 3, 4...) automatically continue the most recent active session

**Example:**
```python
# Step 1 - Creates new session
await planning(step_number=1, problem_statement="...", ...)

# Step 2 - Automatically continues session
await planning(step_number=2, ...)  # No session_id needed!
```

### "Input validation failed"
**Problem**: Required field validation errors

**Solution**: Check all required fields are provided:
- `planning_step`: Non-empty string
- `step_number`: Positive integer (>= 1)
- `total_steps`: Positive integer (>= 1)
- `next_step_needed`: Boolean
- `step_number` must not exceed `total_steps`
- If `is_revision=True`, must provide `revises_step`

### "parent_id is REQUIRED for child items"
**Problem**: Child item (level > 0) missing `parent_id`

**Solution**: Always specify `parent_id` for child items:
```python
# ❌ WRONG - Missing parent_id
{
    "id": "subtask-1",
    "level": 1,  # Child level
    "title": "Subtask"
    # Missing parent_id!
}

# ✅ CORRECT - Includes parent_id
{
    "id": "subtask-1",
    "level": 1,
    "title": "Subtask",
    "parent_id": "main-task"  # Required!
}
```

### "Circular dependencies detected"
**Problem**: Tasks depend on each other in a cycle

**Solution**: Review and fix dependency chain:
```python
# ❌ WRONG - Circular dependency
{"id": "A", "dependencies": ["B"]},
{"id": "B", "dependencies": ["A"]}  # A depends on B, B depends on A

# ✅ CORRECT - Linear dependency
{"id": "A", "dependencies": []},
{"id": "B", "dependencies": ["A"]}  # B depends on A only
```

### Hierarchy Validation Issues
**Problem**: WBS hierarchy structure errors

**Solution**: Ensure proper hierarchy:
- Level 0: Root tasks (no `parent_id`)
- Level 1+: Child tasks (must have `parent_id`)
- Parent must exist before adding children
- No gaps in hierarchy (e.g., level 0 → level 2 without level 1)

## Session Management

### Automatic Session Tracking
The Planning Tool automatically manages sessions:

1. **Step 1**: Creates new session with auto-generated ID
2. **Step 2+**: Automatically finds and continues most recent active session
3. **No manual session management needed** - just increment `step_number`

### Multiple Planning Sessions
If you need multiple planning sessions simultaneously:
- Complete one planning session (`next_step_needed=False`)
- Start new session with `step_number=1` and new `problem_statement`
- Previous session status becomes `completed`
- New session becomes the active one

### Session Status
- `active`: Currently being planned
- `completed`: Planning finished (`next_step_needed=False`)
- `paused`: Reserved for future use

## Configuration

Configure the Planning Tool in `configs/planning.py`:

```python
class PlanningConfig:
    ENABLE_PLANNING = True
    PLANNING_OUTPUT_DIR = Path("./output/planning")
    PLANNING_WBS_FILENAME = "WBS.md"
    PLANNING_DEFAULT_FORMAT = "markdown"
    PLANNING_AUTO_VERSION = True
```

## Related Tools

- **WBS Execution Tool**: Execute tasks from generated WBS
- **Sequential Thinking**: Similar step-by-step process for analysis
- **Vibe Coding**: Interactive prompt refinement before planning
