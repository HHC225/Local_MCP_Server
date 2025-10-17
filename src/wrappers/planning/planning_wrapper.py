"""
Planning Tool Wrapper for MCP Registration
"""
from fastmcp import Context
from src.tools.planning.planning_tool import PlanningTool
from configs.planning import PlanningConfig
from typing import Optional, List, Dict, Any

# Initialize tool instance with configured output directory
_planning_tool = PlanningTool(default_output_dir=PlanningConfig.PLANNING_OUTPUT_DIR)


async def planning(
    planning_step: str,
    step_number: int,
    total_steps: int,
    next_step_needed: bool,
    problem_statement: str = None,
    project_name: str = None,
    wbs_items: List[Dict[str, Any]] = None,
    refine_wbs: bool = False,
    is_revision: bool = None,
    revises_step: int = None,
    branch_from_step: int = None,
    branch_id: str = None,
    generate_markdown: bool = False,
    export_to_file: bool = True,
    output_path: str = None,
    action_required: bool = None,
    action_type: str = None,
    action_description: str = None,
    ctx: Context = None
) -> str:
    """
    Advanced Planning Tool for Work Breakdown Structure (WBS) Creation
    
    🎯 **PURPOSE:**
    Creates structured Work Breakdown Structures (WBS) before implementation to prevent common 
    development issues caused by inadequate planning. Uses step-by-step thinking similar to 
    Sequential Thinking but focused on project decomposition and task planning.
    
    🧠 **CORE CONCEPT:**
    A systematic planning process where each step builds comprehensive WBS structures. Prevents 
    implementation issues by ensuring thorough planning with hierarchical task breakdown and 
    dependency analysis before coding begins.
    
    📋 **PLANNING WORKFLOW:**
    1. **Problem Analysis**: Break down complex requirements into manageable components
    2. **Task Identification**: Identify main tasks, subtasks, and detailed work items
    3. **Hierarchy Building**: Create proper WBS hierarchy (1.0 -> 1.1 -> 1.1.1)
    4. **Dependency Mapping**: Identify task dependencies and critical paths
    5. **Priority Setting**: Assign priorities to tasks
    6. **WBS Generation**: Export structured markdown with checkboxes for agent execution
    
    **CRITICAL: DEPENDENCY SPECIFICATION**
    When creating WBS items, always specify dependencies using one of these formats:
    - Task IDs: ["setup-environment", "install-dependencies"]
    - Hierarchical numbers: ["1.1", "1.2", "2.1"]
    - Task titles: ["Database Setup", "API Configuration"]
    
    **WBS ITEM STRUCTURE REQUIREMENTS:**
    Each WBS item must follow this exact structure:
    ```json
    {
        "id": "2.1",                    // Required: Unique identifier
        "title": "Task Title",          // Required: Task name
        "description": "Details...",    // Required: Implementation details
        "level": 1,                     // Required: 0=root, 1,2,3...=child levels
        "parent_id": "2.0",            // Required for level > 0, null for level 0
        "priority": "High",            // Required: "High", "Medium", or "Low"
        "dependencies": ["1.1", "1.2"], // Optional: List of dependency IDs
        "order": 1                     // Optional: Display order (default: 0)
    }
    ```
    
    ✅ **WBS OUTPUT FORMAT:**
    Generates clean markdown files with:
    - Hierarchical numbered structure (1.1, 1.1.1, 1.1.2, etc.)
    - Checkboxes for each actionable item
    - Priority levels (High/Medium/Low)
    - Detailed task descriptions with implementation guidance
    - Clear dependencies between tasks
    - Progressive file updates during planning
    - Summary statistics and critical path analysis
    
    🔄 **PROGRESSIVE WBS GENERATION:**
    - WBS markdown file is created and updated incrementally during each planning step
    - Prevents token limit issues by updating file progressively
    - Ensures early planning steps are preserved in the final output
    
    📝 **DETAILED DESCRIPTIONS FOR AI AGENTS:**
    Task descriptions must include:
    - Specific implementation requirements
    - Technical specifications and constraints
    - Expected deliverables and acceptance criteria
    - Tools, frameworks, or technologies to use
    - Step-by-step guidance where applicable
    
    **CRITICAL: PARENT vs CHILD TASK DISTINCTION:**
    - **PARENT TASKS (Level 0, 1)**: High-level summaries only, NO implementation details
    - **CHILD TASKS (Level 2+)**: Detailed, actionable implementation instructions
    
    **CRITICAL: PARENT_ID REQUIREMENT:**
    - **ALL child items (level > 0) MUST specify parent_id explicitly**
    - **NEVER rely on automatic inference - always provide parent_id**
    - parent_id must reference an existing parent item's ID
    - Example: {"id": "2.1", "level": 1, "parent_id": "2.0", ...}
    - Level 0 items (root) should NOT have parent_id
    
    🔗 **DEPENDENCY SPECIFICATION GUIDELINES:**
    - Use Task IDs, hierarchical numbers, or task titles
    - Separate multiple dependencies with commas
    - Ensure dependencies reflect actual work order
    
    📄 **FIXED OUTPUT FORMAT:**
    Every WBS.md file follows consistent structure:
    - Project header with problem statement
    - Hierarchical work breakdown structure
    - Planning summary with statistics
    - Critical path analysis
    - Planning metadata
    
    🔄 **STEP-BY-STEP PLANNING:**
    Similar to Sequential Thinking but planning-focused:
    - Each step deepens understanding and refines WBS
    - Supports revision and branching for alternative approaches
    - Builds comprehensive task structure before implementation
    - Validates hierarchy consistency and dependencies
    
    ⚡ **KEY BENEFITS:**
    - Prevents implementation issues through thorough planning
    - Creates actionable task lists for agents to follow
    - Enables progress tracking with checkbox completion
    - Identifies dependencies and critical paths early
    - Progressive file updates prevent token overflow
    - Detailed descriptions enable autonomous agent execution
    
    🎯 **USE CASES:**
    - Complex software development projects
    - System architecture planning
    - API development breakdown
    - Database design planning
    - Testing strategy creation
    - DevOps pipeline planning
    - Code refactoring projects
    
    📤 **EXPORT CAPABILITIES:**
    - Generates markdown files with checkbox format progressively
    - Creates planning summaries and statistics
    - Enables file export to custom paths
    - Maintains session history and metadata
    - Real-time file updates during planning process
    
    Args:
        planning_step: Current planning analysis and breakdown (required)
        step_number: Current planning step number (required, min: 1)
        total_steps: Estimated total planning steps needed (required, min: 1)
        next_step_needed: Whether more planning steps are needed (required)
        problem_statement: Initial problem statement to break down (for new sessions)
        project_name: Name for the project/planning session (optional)
        wbs_items: WBS items to add in this planning step (optional)
        refine_wbs: Whether to refine existing WBS structure (optional)
        is_revision: Whether this revises a previous planning step (optional)
        revises_step: Which planning step is being revised (optional)
        branch_from_step: Step number to branch from (optional)
        branch_id: Branch identifier for alternative planning (optional)
        generate_markdown: Generate WBS markdown even if planning continues (optional)
        export_to_file: Export WBS to markdown file (default: True)
        output_path: Custom output path for WBS file (optional)
        action_required: Whether this step requires immediate action (optional)
        action_type: Type of action (wbs_creation, refinement, export, analysis)
        action_description: Description of the specific action (optional)
    
    Returns:
        JSON response with planning results and WBS summary
    """
    if ctx:
        await ctx.info(f"Executing planning step {step_number}/{total_steps}")
    
    result = await _planning_tool.execute(
        planning_step=planning_step,
        step_number=step_number,
        total_steps=total_steps,
        next_step_needed=next_step_needed,
        problem_statement=problem_statement,
        project_name=project_name,
        wbs_items=wbs_items,
        refine_wbs=refine_wbs,
        is_revision=is_revision,
        revises_step=revises_step,
        branch_from_step=branch_from_step,
        branch_id=branch_id,
        generate_markdown=generate_markdown,
        export_to_file=export_to_file,
        output_path=output_path,
        action_required=action_required,
        action_type=action_type,
        action_description=action_description,
        ctx=ctx
    )
    
    return result
