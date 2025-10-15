# Planning Tool Documentation

## Overview

The Planning Tool is an advanced Work Breakdown Structure (WBS) creation tool designed for structured project decomposition before implementation. It helps prevent common development issues caused by inadequate planning by using a step-by-step systematic approach.

## Core Concept

The Planning Tool uses a systematic planning process where each step builds comprehensive WBS structures. It prevents implementation issues by ensuring thorough planning with:

- **Hierarchical task breakdown** (1.0 -> 1.1 -> 1.1.1)
- **Dependency analysis** between tasks
- **Priority assignment** (High/Medium/Low)
- **Progressive file generation** to prevent token overflow
- **Detailed task descriptions** for autonomous AI agent execution

## Planning Workflow

### 1. Problem Analysis
Break down complex requirements into manageable components.

### 2. Task Identification
Identify main tasks, subtasks, and detailed work items.

### 3. Hierarchy Building
Create proper WBS hierarchy with numbered structure.

### 4. Dependency Mapping
Identify task dependencies and critical paths using proper dependency specification.

### 5. Priority Setting
Assign priorities to tasks based on importance and urgency.

### 6. WBS Generation
Export structured markdown with checkboxes for agent execution.

## WBS Item Structure

Each WBS item must contain:

```python
{
    "id": "unique-task-id",                    # Unique identifier
    "title": "Task Title",                     # Short descriptive title
    "description": "Detailed description...",  # Implementation guidance
    "level": 0,                                # Hierarchy level (0=main, 1=sub, 2=detail)
    "parentId": "parent-task-id",              # Parent task ID (if applicable)
    "completed": False,                        # Completion status
    "dependencies": ["task-id-1", "1.2"],      # Dependent task IDs
    "priority": "high",                        # Priority level (high/medium/low)
    "tags": ["frontend", "api"],               # Optional tags
    "order": 1                                 # Order within same level
}
```

## Critical: Parent vs Child Task Distinction

### Parent Tasks (Level 0-1)
- Should contain **ONLY** high-level summaries and descriptions
- **NEVER** include actual implementation details or executable work
- Example: "Database Setup" with description "Database infrastructure and schema design phase"

### Child Tasks (Level 2+)
- Should contain **detailed, actionable implementation instructions**
- Can be executed directly by AI agents
- Include specific technologies, file paths, API endpoints, etc.
- Example: "Create Users Table" with detailed schema, columns, constraints, and SQL commands

## Dependency Specification

Dependencies must be specified correctly to show relationships between tasks:

### Using Task IDs
```python
"dependencies": ["setup-database", "create-api-endpoints"]
```

### Using Hierarchical Numbers
```python
"dependencies": ["1.1", "2.3.1"]
```

### Using Task Titles
```python
"dependencies": ["Database Schema Design", "API Authentication Setup"]
```

### Multiple Dependencies
```python
"dependencies": ["1.1", "setup-database", "API Design"]
```

## Usage Examples

### Example 1: Starting a New Planning Session

```python
await planning(
    problem_statement="Build a user authentication system with JWT",
    project_name="Auth System",
    planning_step="Analyzing authentication requirements: user registration, login, JWT tokens, password reset",
    step_number=1,
    total_steps=5,
    next_step_needed=True
)
```

### Example 2: Adding WBS Items

```python
await planning(
    planning_step="Breaking down authentication into main components",
    step_number=2,
    total_steps=5,
    next_step_needed=True,
    wbs_items=[
        {
            "id": "auth-backend",
            "title": "Backend Authentication",
            "description": "Server-side authentication implementation",
            "level": 0,
            "completed": False,
            "priority": "high",
            "order": 1,
            "dependencies": []
        },
        {
            "id": "user-registration",
            "title": "User Registration API",
            "description": "Create POST /api/auth/register endpoint with email validation, password hashing using bcrypt, and user creation in PostgreSQL database",
            "level": 1,
            "parentId": "auth-backend",
            "completed": False,
            "priority": "high",
            "order": 1,
            "dependencies": ["database-setup"]
        }
    ]
)
```

### Example 3: Completing Planning and Exporting

```python
await planning(
    planning_step="Final review and validation of WBS structure",
    step_number=5,
    total_steps=5,
    next_step_needed=False,
    export_to_file=True,
    output_path="/path/to/output"
)
```

## Output Format

The generated WBS markdown file follows this structure:

```markdown
# Project: [PROJECT_NAME]

## Problem Statement
[DETAILED_PROBLEM_DESCRIPTION]

## Work Breakdown Structure

### 1. [MAIN_CATEGORY_TITLE]
- [ ] **[MAIN_CATEGORY_TITLE]** (Priority: High)
  - Task ID: 1
  - Description: [SUMMARY_DESCRIPTION]
  - Dependencies: None
  - [ ] **[SUBTASK_TITLE]** (Priority: High)
    - Task ID: 1.1
    - Description: [DETAILED_IMPLEMENTATION]
    - Dependencies: None

## Planning Summary

- **Total Tasks**: 10
- **High Priority**: 5
- **Medium Priority**: 3
- **Low Priority**: 2
- **Completed Tasks**: 0
- **Remaining Tasks**: 10
- **Progress**: 0%

### Critical Path
- Task 1.1 (depends on: database-setup)
- Task 2.1 (depends on: 1.1, api-design)

## Planning Metadata

- **Session ID**: planning_20250115_123456
- **Status**: exported
- **Created**: 2025-01-15T12:34:56
- **Last Updated**: 2025-01-15T13:45:23
- **Planning Steps**: 5

---
*Generated by Planning Tool - 2025-01-15T13:45:23*
```

## Progressive WBS Generation

Unlike traditional planning tools that generate files only at the end:

- **WBS markdown file is created and updated incrementally** during each planning step
- **Prevents token limit issues** by updating file progressively
- **Ensures early planning steps are preserved** in the final output
- Each step adds or refines WBS items in real-time

## Key Benefits

1. **Prevents implementation issues** through thorough planning
2. **Creates actionable task lists** for agents to follow
3. **Enables progress tracking** with checkbox completion
4. **Identifies dependencies** and critical paths early
5. **Progressive file updates** prevent token overflow
6. **Detailed descriptions** enable autonomous agent execution
7. **Structured task organization** for better project management

## Use Cases

- Complex software development projects
- System architecture planning
- API development breakdown
- Database design planning
- Testing strategy creation
- DevOps pipeline planning
- Code refactoring projects
- Multi-phase implementation planning

## Best Practices

### 1. Start with Clear Problem Statement
Define the problem clearly before starting planning.

### 2. Use Hierarchical Structure
Maintain proper hierarchy: Main tasks -> Subtasks -> Detail tasks

### 3. Write Detailed Descriptions for Child Tasks
Include enough detail for AI agents to implement without clarification:
- Specific file names and paths
- Exact API endpoints and methods
- Database schemas with column definitions
- Technology and framework choices
- Expected deliverables

### 4. Specify Dependencies Accurately
Use correct dependency references to ensure proper task ordering.

### 5. Set Realistic Priorities
Prioritize based on criticality, dependencies, and project constraints.

### 6. Review and Refine
Use revision and branching capabilities to refine the plan.

### 7. Export Progressively
Let the tool update the WBS file progressively to avoid token limits.

## Session Management

The Planning Tool maintains session state to track:
- Planning steps history
- WBS items accumulation
- Export file path
- Branch alternatives
- Completion status

Sessions are created automatically when a new problem statement is provided.

## Configuration

Enable the Planning Tool in your `.env` file:

```bash
ENABLE_PLANNING_TOOLS="true"
```

## Integration with Other Tools

The Planning Tool works well with:

- **Sequential Thinking**: For detailed implementation planning after WBS creation
- **Recursive Thinking**: For iterative refinement of planning decisions
- **Tree of Thoughts**: For exploring alternative planning approaches

## Troubleshooting

### Issue: WBS Hierarchy Validation Failed

**Solution**: Ensure parent tasks exist before creating child tasks, and level numbers are consistent.

### Issue: Export Failed

**Solution**: Check that the output directory exists and has write permissions.

### Issue: Dependencies Not Showing

**Solution**: Verify dependency IDs match existing task IDs, hierarchical numbers, or task titles.

## Advanced Features

### Branching
Create alternative planning approaches:

```python
await planning(
    planning_step="Exploring microservices architecture alternative",
    step_number=3,
    total_steps=6,
    next_step_needed=True,
    branch_from_step=2,
    branch_id="microservices-approach"
)
```

### Revision
Revise previous planning steps:

```python
await planning(
    planning_step="Revised authentication approach with OAuth2",
    step_number=2,
    total_steps=5,
    next_step_needed=True,
    is_revision=True,
    revises_step=2
)
```

### Custom Output Path
Specify custom export location:

```python
await planning(
    planning_step="Final planning step",
    step_number=5,
    total_steps=5,
    next_step_needed=False,
    output_path="/projects/my-project/WBS.md"
)
```

## Comparison with TypeScript Implementation

This Python implementation maintains feature parity with the original TypeScript version:

✅ Session management
✅ WBS item creation and validation
✅ Hierarchical structure enforcement
✅ Dependency tracking
✅ Progressive file generation
✅ Markdown export
✅ Summary statistics
✅ Critical path analysis
✅ Branching and revision support

## API Reference

See the function docstring in `planning_wrapper.py` for detailed parameter descriptions and examples.

## Support

For issues or questions about the Planning Tool, please refer to the main documentation or create an issue in the repository.
