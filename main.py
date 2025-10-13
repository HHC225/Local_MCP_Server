"""
Thinking Tools MCP Server - Main Entry Point
Advanced thinking and reasoning tools for problem-solving

This server provides:
- Recursive Thinking Model: Recursive reasoning for iterative answer improvement
- Sequential Thinking: Structured analytical thinking for software development

All tools are registered here.
"""
from fastmcp import FastMCP, Context
from config import ServerConfig
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# Initialize FastMCP server
mcp = FastMCP(
    name=ServerConfig.SERVER_NAME,
)

logger.info(f"Initializing {ServerConfig.SERVER_NAME} v{ServerConfig.SERVER_VERSION}")
logger.info(f"Description: {ServerConfig.SERVER_DESCRIPTION}")


# ============================================================================
# RECURSIVE THINKING TOOLS REGISTRATION
# ============================================================================

if ServerConfig.ENABLE_Rcursive_Thinking_TOOLS:
    from tools import (
        Rcursive_ThinkingInitializeTool,
        Rcursive_ThinkingUpdateLatentTool,
        Rcursive_ThinkingUpdateAnswerTool,
        Rcursive_ThinkingGetResultTool,
        Rcursive_ThinkingResetTool
    )
    
    logger.info("Registering Recursive Thinking tools...")
    
    # Initialize Recursive Thinking tools
    Rcursive_Thinking_init = Rcursive_ThinkingInitializeTool()
    Rcursive_Thinking_update_latent = Rcursive_ThinkingUpdateLatentTool()
    Rcursive_Thinking_update_answer = Rcursive_ThinkingUpdateAnswerTool()
    Rcursive_Thinking_get_result = Rcursive_ThinkingGetResultTool()
    Rcursive_Thinking_reset = Rcursive_ThinkingResetTool()
    
    @mcp.tool()
    async def recursive_thinking_initialize(
        question: str,
        initial_answer: str = "",
        n_latent_updates: int = 4,
        max_improvements: int = 16,
        ctx: Context = None
    ) -> str:
        """
        Initialize a new recursive reasoning session with Recursive Thinking Model.
        
        This tool sets up the recursive reasoning process where:
        - Question (x): The input problem to solve
        - Answer (y): The current predicted answer (starts empty or with initial guess)
        - Latent (z): Hidden reasoning state that helps improve the answer
        - n_latent_updates: How many times to recursively update latent z (default: 4)
        - max_improvements: Maximum improvement iterations (default: 16)
        
        Args:
            question: The problem or question to solve
            initial_answer: Optional starting answer (empty means start from scratch)
            n_latent_updates: Number of recursive latent updates per improvement step
            max_improvements: Maximum number of answer improvement iterations
        
        Returns:
            Confirmation message with session details including auto-generated unique session_id
        """
        return await Rcursive_Thinking_init.execute(question, initial_answer, n_latent_updates, max_improvements, ctx)
    
    @mcp.tool()
    async def recursive_thinking_update_latent(
        session_id: str,
        reasoning_insight: str,
        step_number: int,
        ctx: Context = None
    ) -> str:
        """
        Update the latent reasoning state (z) based on question (x), current answer (y), and previous latent (z).
        
        This is Step 1-n of the Recursive Thinking algorithm. The latent state represents the model's internal
        reasoning process. This function should be called n times (default: 4x) to recursively
        improve the latent reasoning before updating the answer.
        
        **VERIFICATION MODE**: When called after verify_final_answer, this performs mandatory
        final verification reasoning using the same 4-step systematic analysis.
        
        Think of this as "thinking deeply" about the problem with systematic analysis:
        
        **Step-by-Step Latent Reasoning Guidelines:**
        
        **Step 1 (Problem Decomposition):**
        - Break down the original question into core components and sub-problems
        - Identify what type of problem this is (mathematical, logical, analytical, creative, etc.)
        - List all given information, constraints, and assumptions explicitly
        - Determine what specific knowledge domains or reasoning patterns are needed
        
        **Step 2 (Current State Analysis):**
        - Thoroughly examine the current answer's logic and reasoning chain
        - Identify specific strengths: what parts are correct and why
        - Pinpoint exact weaknesses: logical gaps, incorrect assumptions, missing steps
        - Check for consistency between different parts of the reasoning
        
        **Step 3 (Alternative Perspectives & Deep Reasoning):**
        - Consider alternative approaches or interpretations of the problem
        - Apply domain-specific reasoning patterns (e.g., proof techniques for math, causal analysis for complex scenarios)
        - Question underlying assumptions and explore edge cases
        - Look for patterns, connections, or insights that weren't initially obvious
        
        **Step 4 (Synthesis & Improvement Strategy):**
        - Synthesize insights from previous steps into a coherent improvement plan
        - Prioritize which aspects of the answer need the most improvement
        - Develop specific strategies for addressing identified weaknesses
        - Prepare concrete recommendations for the next answer iteration
        
        **Cross-cutting Principles for All Steps:**
        - Be extremely specific and concrete in your reasoning
        - Reference specific parts of the question and current answer
        - Use evidence-based reasoning rather than vague intuitions
        - Build incrementally on insights from previous latent updates
        - Each recursive update should add new insights, not repeat previous ones
        
        Args:
            session_id: The reasoning session identifier
            reasoning_insight: Your new reasoning insight following the step-by-step guidelines above.
                              Include specific analysis, concrete observations, and actionable insights.
                              Reference exact parts of the question/answer being analyzed.
                              Each step should build progressively on previous insights.
            step_number: Which latent update step this is (1 to n_latent_updates)
                        Step 1: Problem decomposition and classification
                        Step 2: Current answer analysis (strengths/weaknesses)
                        Step 3: Alternative perspectives and deep domain reasoning  
                        Step 4: Synthesis and concrete improvement strategy
        
        Returns:
            Status of latent update and guidance for next step
        """
        return await Rcursive_Thinking_update_latent.execute(session_id, reasoning_insight, step_number, ctx)
    
    @mcp.tool()
    async def recursive_thinking_update_answer(
        session_id: str,
        improved_answer: str,
        improvement_rationale: str,
        ctx: Context = None
    ) -> str:
        """
        Update the answer (y) based on current answer and refined latent reasoning (z).
        
        This is Step n+1 of the Recursive Thinking algorithm. After recursively updating the latent reasoning
        n times, use those insights to improve the actual answer. This is where you:
        - Apply the reasoning insights from the latent state
        - Correct any errors in the previous answer
        - Refine and improve the solution
        
        **IMPORTANT**: This tool is also used to finalize the verified answer after completing
        the 4-step verification reasoning. When called after verification reasoning is complete,
        it finalizes the answer and marks verification as completed.

        Args:
            session_id: The reasoning session identifier
            improved_answer: The new improved answer based on latent reasoning (or verified answer after verification)
            improvement_rationale: Brief explanation of how you improved the answer (or verification summary)
        
        Returns:
            Updated answer and guidance on whether to continue iterating, or verification completion status
        """
        return await Rcursive_Thinking_update_answer.execute(session_id, improved_answer, improvement_rationale, ctx)
    
    @mcp.tool()
    async def recursive_thinking_get_result(
        session_id: str,
        ctx: Context = None
    ) -> str:
        """
        Retrieve the final answer and complete reasoning history.
        
        This tool checks verification status:
        - If not verified: Automatically starts verification mode with update_latent_reasoning (4 steps)
        - If verified: Returns the final verified answer with complete reasoning history
        
        Workflow: 
        1. Call get_final_result when confident in answer
        2. If verification needed: Complete 4 update_latent_reasoning steps → update_answer
        3. Call get_final_result again to retrieve final verified answer
        
        Args:
            session_id: The reasoning session identifier
        
        Returns:
            Either verification start instruction or complete verified results
        """
        return await Rcursive_Thinking_get_result.execute(session_id, ctx)
    
    @mcp.tool()
    async def recursive_thinking_reset(
        session_id: str,
        ctx: Context = None
    ) -> str:
        """
        Reset or delete a reasoning session.
        
        Args:
            session_id: The reasoning session identifier to reset
        
        Returns:
            Confirmation of reset
        """
        return await Rcursive_Thinking_reset.execute(session_id, ctx)
    
    logger.info("Rcursive_Thinking reasoning tools registered successfully")


# ============================================================================
# SEQUENTIAL THINKING TOOL REGISTRATION
# ============================================================================

if ServerConfig.ENABLE_ST_TOOLS:
    from tools import SequentialThinkingTool
    
    logger.info("Registering Sequential Thinking tool...")
    
    # Initialize ST tool
    st_tool = SequentialThinkingTool()
    
    @mcp.tool()
    async def st(
        thought: str,
        thought_number: int,
        total_thoughts: int,
        next_thought_needed: bool,
        is_revision: bool = None,
        revises_thought: int = None,
        branch_from_thought: int = None,
        branch_id: str = None,
        needs_more_thoughts: bool = None,
        action_required: bool = None,
        action_type: str = None,
        action_description: str = None,
        ctx: Context = None
    ) -> str:
        """
        Sequential Thinking Tool for Software Development Problem-Solving
        
        🧠 **CORE CONCEPT:**
        A structured analytical thinking process where each thought builds sequentially to solve 
        complex software problems. Thoughts can question, revise, or branch from previous insights 
        as understanding deepens.
        
        🎯 **SCOPE:** Software development, system architecture, API design, database optimization, 
        and technical analysis.
        
        ⚡ **KEY PRINCIPLES:**
        1. **Quality First**: Establish clear success criteria before starting. If final result 
           doesn't meet criteria, restart from thought 1.
        2. **Critical Analysis**: Question user input for logical errors, missing information, 
           or better approaches.
        3. **Adaptive Process**: Adjust total thoughts, revise decisions, or branch into alternatives 
           as needed.
        
        📋 **CORE PARAMETERS:**
        - thought: Current analytical step (architecture analysis, technical decisions, implementation planning)
        - thought_number: Current sequence number (1, 2, 3...)
        - total_thoughts: Estimated total needed (adjustable)
        - next_thought_needed: Whether to continue thinking
        - is_revision: Whether this revises previous thinking
        - revises_thought: Which thought number is being reconsidered
        - branch_from_thought: Starting point for alternative exploration
        - branch_id: Identifier for current branch
        - action_required: Whether this step requires immediate action
        - action_type: Type of action to be executed
        - action_description: Specific action to be taken
        
        🔄 **SEQUENTIAL THINKING FLOW:**
        1. Start with problem analysis and success criteria
        2. Each thought builds on or questions previous insights
        3. Revise or branch when better approaches emerge
        4. Take direct action when implementation is needed (code writing, file creation, etc.)
        5. Continue until robust, implementable solution is reached
        6. Verify solution meets initial criteria
        
        💡 **USE CASES:**
        - System architecture design and component breakdown
        - API endpoint structure and data flow planning
        - Database schema optimization and query analysis
        - Performance bottleneck identification and solutions
        - Security vulnerability assessment and mitigation
        - Code refactoring strategy and impact analysis
        
        ⚡ **DIRECT ACTION EXECUTION:**
        - When code needs to be written, write it immediately in that step
        - When files need to be created or modified, do it directly
        - When configurations need to be updated, make the changes
        - When tests need to be run, execute them in the current step
        - No intermediate planning - execute actions as they become clear
        
        Args:
            thought: Your current thinking step
            thought_number: Current thought number (numeric value, e.g., 1, 2, 3)
            total_thoughts: Estimated total thoughts needed (numeric value, e.g., 5, 10)
            next_thought_needed: Whether another thought step is needed
            is_revision: Whether this revises previous thinking
            revises_thought: Which thought is being reconsidered
            branch_from_thought: Branching point thought number
            branch_id: Branch identifier
            needs_more_thoughts: If more thoughts are needed
            action_required: Whether this step requires direct action
            action_type: Type of action (code_writing, file_creation, file_modification, 
                        configuration, testing, analysis, other)
            action_description: Description of the specific action to be taken
        
        Returns:
            JSON response with thought processing results
        """
        return await st_tool.execute(
            thought=thought,
            thought_number=thought_number,
            total_thoughts=total_thoughts,
            next_thought_needed=next_thought_needed,
            is_revision=is_revision,
            revises_thought=revises_thought,
            branch_from_thought=branch_from_thought,
            branch_id=branch_id,
            needs_more_thoughts=needs_more_thoughts,
            action_required=action_required,
            action_type=action_type,
            action_description=action_description,
            ctx=ctx
        )
    
    logger.info("Sequential Thinking tool registered successfully")


# ============================================================================
# TREE OF THOUGHTS TOOL REGISTRATION
# ============================================================================

if ServerConfig.ENABLE_TOT_TOOLS:
    from tools import TreeOfThoughtsTool
    
    logger.info("Registering Tree of Thoughts tool...")
    
    # Initialize ToT tool
    tot_tool = TreeOfThoughtsTool()
    
    @mcp.tool()
    async def tt(
        action: str,
        session_id: str = None,
        problem_statement: str = None,
        config: dict = None,
        parent_node_id: str = None,
        thoughts: list = None,
        node_id: str = None,
        evaluation: dict = None,
        search_strategy: str = None,
        dead_end_node_id: str = None,
        backtrack_strategy: str = None,
        solution: str = None,
        ctx: Context = None
    ) -> str:
        """
        Advanced Tree of Thoughts (ToT) framework for complex software development and system design problem-solving.
        
        This tool implements the complete ToT framework optimized for IT professionals working on application development, 
        server architecture, and system design challenges.
        
        🌳 **Software Development Components:**
        
        **🔧 Architecture Decomposition**: Breaks complex system design problems into manageable components (frontend, backend, database, APIs, etc.)
        **💡 Solution Generation**: Uses sampling or proposing strategies to explore multiple implementation approaches
        **📊 Code/Design Evaluation**: Evaluates solutions using technical criteria (performance, scalability, maintainability, security)  
        **🔍 Implementation Search**: Employs systematic exploration to find optimal technical solutions
        
        **Key Features for Software Development:**
        - **Multi-Architecture Exploration**: Explore different system architectures simultaneously (microservices vs monolith, REST vs GraphQL, etc.)
        - **Technical Backtracking**: Return to previous design decisions when implementation proves problematic
        - **Code Quality Assessment**: Evaluate code approaches for maintainability, performance, and scalability
        - **API Design Strategies**: Choose between different API design patterns and implementation approaches
        - **Testing Strategy Planning**: Develop comprehensive testing approaches (unit, integration, E2E, performance)
        - **Development Workflow Management**: Track multiple development approaches and technical decisions
        
        **Use Cases in Software Development:**
        - **System Architecture Design**: Designing scalable web applications, microservices, or distributed systems
        - **API Development Planning**: Choosing optimal API patterns, authentication methods, and data flow strategies
        - **Database Design**: Exploring different database schemas, indexing strategies, and data modeling approaches
        - **Performance Optimization**: Analyzing bottlenecks and exploring multiple optimization strategies
        - **Testing Strategy Development**: Planning comprehensive testing approaches for complex applications
        - **Technology Stack Selection**: Evaluating different frameworks, libraries, and tools for projects
        - **Code Refactoring Plans**: Systematic approach to legacy code improvement and modernization
        - **DevOps Pipeline Design**: Planning CI/CD workflows, deployment strategies, and infrastructure setup
        
        **Development Workflow:**
        1. Define your technical problem or system requirement
        2. Generate multiple implementation approaches using LLM (sampling or proposing strategies)
        3. Evaluate each approach for technical feasibility, scalability, and maintainability using LLM
        4. Search for the most promising technical path using systematic exploration
        5. Backtrack when technical constraints make paths infeasible
        6. Continue until optimal technical solution is identified
        
        **Actions:**
        - create_session: Start a new technical problem-solving session
        - add_thoughts: Add multiple implementation approaches generated by LLM to the tree
        - add_evaluation: Add LLM evaluation results for technical solutions (value: 1-10, confidence: 0-1, viability: promising/uncertain/dead_end, reasoning)
        - search_next: Find the next best technical approach to explore
        - backtrack: Return to previous design decisions when current path proves problematic
        - set_solution: Document the final technical solution with implementation details
        - get_session: Retrieve complete technical analysis and decision history
        - list_sessions: List all active software development problem-solving sessions
        - display_results: Display ranked solutions with scores and paths
        
        **Important Note:** 
        This tool manages the Tree of Thoughts structure and algorithms. All actual thinking, solution generation, 
        and evaluation is performed by the LLM. The tool provides the framework for organizing and navigating 
        through the solution space systematically.
        
        Args:
            action: The action to perform (create_session, add_thoughts, add_evaluation, search_next, backtrack, 
                   set_solution, get_session, list_sessions, display_results)
            session_id: Session ID (required for most actions)
            problem_statement: Problem to solve (required for create_session)
            config: Configuration dict with search_strategy (bfs/dfs), generation_strategy (sampling/proposing),
                   evaluation_method (value/vote), max_depth, max_branches
            parent_node_id: Parent node to attach thoughts to (optional, defaults to root)
            thoughts: List of thought strings to add (required for add_thoughts)
            node_id: Node ID to evaluate (required for add_evaluation)
            evaluation: Evaluation dict with value (1-10), confidence (0-1), viability (promising/uncertain/dead_end),
                       reasoning (required for add_evaluation)
            search_strategy: Search strategy override for search_next (bfs or dfs)
            dead_end_node_id: Node ID that reached dead end (required for backtrack)
            backtrack_strategy: Strategy for backtracking (parent, best_alternative, root)
            solution: Final solution text (required for set_solution)
        
        Returns:
            JSON response with action results
        """
        return await tot_tool.execute(
            action=action,
            session_id=session_id,
            problem_statement=problem_statement,
            config=config,
            parent_node_id=parent_node_id,
            thoughts=thoughts,
            node_id=node_id,
            evaluation=evaluation,
            search_strategy=search_strategy,
            dead_end_node_id=dead_end_node_id,
            backtrack_strategy=backtrack_strategy,
            solution=solution,
            ctx=ctx
        )
    
    logger.info("Tree of Thoughts tool registered successfully")


# ============================================================================
# CONVERSATION MEMORY TOOLS REGISTRATION
# ============================================================================

if ServerConfig.ENABLE_CONVERSATION_MEMORY_TOOLS:
    from tools import ConversationMemoryTool
    
    logger.info("Registering Conversation Memory tools...")
    
    # Initialize Conversation Memory tool
    conversation_memory_tool = ConversationMemoryTool(
        persist_directory=ServerConfig.CONVERSATION_MEMORY_DB_PATH
    )
    
    @mcp.tool()
    async def conversation_memory_store(
        conversation_text: str,
        speaker: str = None,
        summary: str = None,
        metadata: dict = None,
        conversation_id: str = None,
        ctx: Context = None
    ) -> dict:
        """
        Store important conversation content in vector database.
        
        This tool stores conversation summaries or full text in ChromaDB with automatic embedding.
        The LLM should provide a summary of important conversation points before calling this tool.
        
        Args:
            conversation_text: The full conversation content to store
            speaker: Name of the speaker/participant (e.g., "User", "GitHub Copilot", "Assistant")
            summary: Summary of the conversation (recommended - should be generated by LLM)
            metadata: Additional metadata as dict (e.g., {"topic": "API design", "importance": "high"})
            conversation_id: Optional unique identifier (auto-generated if not provided)
        
        Returns:
            dict: Storage confirmation with conversation_id and metadata
        
        Example:
            Store a summarized conversation:
            {
                "conversation_text": "User asked about API design patterns. Discussed REST vs GraphQL...",
                "speaker": "GitHub Copilot",
                "summary": "Discussion about API design: REST vs GraphQL trade-offs, recommended REST for simple CRUD",
                "metadata": {"topic": "API design", "context": "architecture planning"}
            }
        """
        return await conversation_memory_tool.execute(
            action="store",
            ctx=ctx,
            conversation_text=conversation_text,
            speaker=speaker,
            summary=summary,
            metadata=metadata,
            conversation_id=conversation_id
        )
    
    @mcp.tool()
    async def conversation_memory_query(
        query_text: str,
        n_results: int = None,
        filter_metadata: dict = None,
        ctx: Context = None
    ) -> dict:
        """
        Query stored conversations using semantic search.
        
        This tool searches the vector database for relevant conversation memories
        based on semantic similarity to the query text.
        
        Args:
            query_text: Text to search for (will find semantically similar conversations)
            n_results: Number of results to return (default: 5)
            filter_metadata: Optional metadata filters as dict (e.g., {"speaker": "User"})
        
        Returns:
            dict: Search results with relevant conversations and their metadata
        
        Example:
            Find conversations about database design:
            {
                "query_text": "How should I design the database schema?",
                "n_results": 3,
                "filter_metadata": {"topic": "database"}
            }
        """
        if n_results is None:
            n_results = ServerConfig.CONVERSATION_MEMORY_DEFAULT_RESULTS
            
        return await conversation_memory_tool.execute(
            action="query",
            ctx=ctx,
            query_text=query_text,
            n_results=n_results,
            filter_metadata=filter_metadata
        )
    
    @mcp.tool()
    async def conversation_memory_list(
        limit: int = None,
        offset: int = 0,
        ctx: Context = None
    ) -> dict:
        """
        List all stored conversation memories.
        
        Args:
            limit: Maximum number of conversations to return (None = all)
            offset: Number of conversations to skip
        
        Returns:
            dict: List of all stored conversations with metadata
        """
        return await conversation_memory_tool.execute(
            action="list",
            ctx=ctx,
            limit=limit,
            offset=offset
        )
    
    @mcp.tool()
    async def conversation_memory_delete(
        conversation_id: str,
        ctx: Context = None
    ) -> dict:
        """
        Delete a specific conversation from the database.
        
        Args:
            conversation_id: ID of the conversation to delete
        
        Returns:
            dict: Deletion confirmation
        """
        return await conversation_memory_tool.execute(
            action="delete",
            ctx=ctx,
            conversation_id=conversation_id
        )
    
    @mcp.tool()
    async def conversation_memory_clear(
        ctx: Context = None
    ) -> dict:
        """
        Clear all conversations from the database.
        
        WARNING: This will permanently delete all stored conversation memories.
        
        Returns:
            dict: Clear confirmation with count of deleted items
        """
        return await conversation_memory_tool.execute(
            action="clear",
            ctx=ctx
        )
    
    logger.info("Conversation Memory tools registered successfully")


# ============================================================================
# FUTURE TOOLS REGISTRATION PLACEHOLDERS
# Section for future tools to be added
# ============================================================================

if ServerConfig.ENABLE_FUTURE_TOOL_1:
    logger.info("Future Tool 1 is enabled but not yet implemented")
    # TODO: Implement Future Tool 1
    pass

if ServerConfig.ENABLE_FUTURE_TOOL_2:
    logger.info("Future Tool 2 is enabled but not yet implemented")
    # TODO: Implement Future Tool 2
    pass


# ============================================================================
# SERVER STARTUP
# ============================================================================

if __name__ == "__main__":
    logger.info(f"Starting {ServerConfig.SERVER_NAME} with transport: {ServerConfig.TRANSPORT_TYPE}")
    
    # Run the MCP server
    if ServerConfig.TRANSPORT_TYPE == "stdio":
        mcp.run(transport='stdio')
    elif ServerConfig.TRANSPORT_TYPE == "http":
        logger.info(f"HTTP server starting on {ServerConfig.HTTP_HOST}:{ServerConfig.HTTP_PORT}{ServerConfig.HTTP_PATH}")
        # Note: HTTP transport configuration would go here
        mcp.run(transport='stdio')  # Fallback to stdio for now
    else:
        logger.warning(f"Unknown transport type: {ServerConfig.TRANSPORT_TYPE}, falling back to stdio")
        mcp.run(transport='stdio')
