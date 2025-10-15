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
    from wrappers.reasoning.recursive_thinking_wrappers import (
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
    
    logger.info("Recursive Thinking reasoning tools registered successfully")


# ============================================================================
# SEQUENTIAL THINKING TOOL REGISTRATION
# ============================================================================

if ServerConfig.ENABLE_ST_TOOLS:
    from wrappers.reasoning.sequential_thinking_wrapper import st
    
    logger.info("Registering Sequential Thinking tool...")
    
    # Register wrapper function as MCP tool
    mcp.tool()(st)
    
    logger.info("Sequential Thinking tool registered successfully")


# ============================================================================
# TREE OF THOUGHTS TOOL REGISTRATION
# ============================================================================

if ServerConfig.ENABLE_TOT_TOOLS:
    from wrappers.reasoning.tree_of_thoughts_wrapper import tt
    
    logger.info("Registering Tree of Thoughts tool...")
    
    # Register wrapper function as MCP tool
    mcp.tool()(tt)
    
    logger.info("Tree of Thoughts tool registered successfully")


# ============================================================================
# CONVERSATION MEMORY TOOLS REGISTRATION
# ============================================================================

if ServerConfig.ENABLE_CONVERSATION_MEMORY_TOOLS:
    from wrappers.memory.conversation_memory_wrappers import (
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
