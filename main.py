"""
Thinking Tools MCP Server - Main Entry Point
Advanced thinking and reasoning tools for problem-solving

This server provides:
- Recursive Thinking Model: Recursive reasoning for iterative answer improvement
- Sequential Thinking: Structured analytical thinking for software development
- Tree of Thoughts: Multi-path exploration and evaluation
- Conversation Memory: Long-term memory and context retention
- Planning & WBS: Project planning and work breakdown structure

All tools are registered here with modular configuration.
"""
from fastmcp import FastMCP, Context
from configs import ServerConfig, ReasoningConfig, MemoryConfig, PlanningConfig
from src.utils.logger import get_logger

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

if ReasoningConfig.ENABLE_RECURSIVE_THINKING:
    from src.wrappers.reasoning.recursive_thinking_wrappers import (
        recursive_thinking_initialize,
        recursive_thinking_update_latent,
        recursive_thinking_update_answer,
        recursive_thinking_get_result,
        recursive_thinking_reset
    )
    
    logger.info("Registering Recursive Thinking tools...")
    
    # Register wrapper functions as MCP tools
    mcp.tool()(recursive_thinking_initialize)
    mcp.tool()(recursive_thinking_update_latent)
    mcp.tool()(recursive_thinking_update_answer)
    mcp.tool()(recursive_thinking_get_result)
    mcp.tool()(recursive_thinking_reset)
    
    logger.info("Recursive Thinking tools registered successfully")


# ============================================================================
# SEQUENTIAL THINKING TOOL REGISTRATION
# ============================================================================

if ReasoningConfig.ENABLE_SEQUENTIAL_THINKING:
    from src.wrappers.reasoning.sequential_thinking_wrapper import st
    
    logger.info("Registering Sequential Thinking tool...")
    
    # Register wrapper function as MCP tool
    mcp.tool()(st)
    
    logger.info("Sequential Thinking tool registered successfully")


# ============================================================================
# TREE OF THOUGHTS TOOL REGISTRATION
# ============================================================================

if ReasoningConfig.ENABLE_TREE_OF_THOUGHTS:
    from src.wrappers.reasoning.tree_of_thoughts_wrapper import tt
    
    logger.info("Registering Tree of Thoughts tool...")
    
    # Register wrapper function as MCP tool
    mcp.tool()(tt)
    
    logger.info("Tree of Thoughts tool registered successfully")


# ============================================================================
# CONVERSATION MEMORY TOOLS REGISTRATION
# ============================================================================

if MemoryConfig.ENABLE_CONVERSATION_MEMORY:
    from src.wrappers.memory.conversation_memory_wrappers import (
        conversation_memory_store,
        conversation_memory_query,
        conversation_memory_list,
        conversation_memory_delete,
        conversation_memory_clear
    )
    
    logger.info("Registering Conversation Memory tools...")
    
    # Register wrapper functions as MCP tools
    mcp.tool()(conversation_memory_store)
    mcp.tool()(conversation_memory_query)
    mcp.tool()(conversation_memory_list)
    mcp.tool()(conversation_memory_delete)
    mcp.tool()(conversation_memory_clear)
    
    logger.info("Conversation Memory tools registered successfully")


# ============================================================================
# PLANNING TOOLS REGISTRATION
# ============================================================================

if PlanningConfig.ENABLE_PLANNING:
    from src.wrappers.planning.planning_wrapper import planning
    
    logger.info("Registering Planning tool...")
    
    # Register wrapper function as MCP tool
    mcp.tool()(planning)
    
    logger.info("Planning tool registered successfully")


# ============================================================================
# WBS EXECUTION TOOLS REGISTRATION
# ============================================================================

if PlanningConfig.ENABLE_WBS_EXECUTION:
    from src.wrappers.planning.wbs_execution_wrapper import wbs_execution
    
    logger.info("Registering WBS Execution tool...")
    
    # Register wrapper function as MCP tool
    mcp.tool()(wbs_execution)
    
    logger.info("WBS Execution tool registered successfully")


# ============================================================================
# SLACK TOOLS REGISTRATION
# ============================================================================

try:
    from configs.slack import SlackConfig, get_slack_config
    
    # Check if Slack is enabled
    slack_config = get_slack_config()
    if slack_config.ENABLE_SLACK_TOOLS:
        from src.wrappers.slack import (
            get_thread_content,
            get_single_message,
            post_message,
            post_ephemeral_message,
            delete_message
        )
        
        logger.info("Registering Slack tools...")
        
        # Register wrapper functions as MCP tools
        mcp.tool()(get_thread_content)
        mcp.tool()(get_single_message)
        mcp.tool()(post_message)
        mcp.tool()(post_ephemeral_message)
        mcp.tool()(delete_message)
        
        logger.info("Slack tools registered successfully")
    else:
        logger.info("Slack tools disabled in configuration")
        
except Exception as e:
    logger.warning(f"Slack tools not available: {e}")
    logger.info("Continuing without Slack tools...")


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
