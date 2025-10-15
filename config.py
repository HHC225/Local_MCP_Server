"""
Thinking Tools MCP Server Configuration
This module contains all server configuration settings.
"""
import os
from typing import Optional
from pathlib import Path


class ServerConfig:
    """
    Main server configuration class.
    Direct configuration without .env file dependency.
    You can modify these values directly or override via environment variables.
    """
    
    # Base Directory
    BASE_DIR: Path = Path(__file__).parent
    OUTPUT_DIR: Path = BASE_DIR / "output"
    
    # Server Identity
    SERVER_NAME: str = os.getenv("MCP_SERVER_NAME", "Thinking Tools MCP Server")
    SERVER_VERSION: str = os.getenv("MCP_SERVER_VERSION", "1.0.0")
    SERVER_DESCRIPTION: str = "Advanced thinking and reasoning tools for problem-solving (Recursive Thinking, Sequential Thinking, Tree of Thoughts)"
    
    # Transport Configuration
    TRANSPORT_TYPE: str = os.getenv("MCP_TRANSPORT", "stdio")  # stdio, http, sse
    HTTP_HOST: str = os.getenv("MCP_HTTP_HOST", "127.0.0.1")
    HTTP_PORT: int = int(os.getenv("MCP_HTTP_PORT", "8000"))
    HTTP_PATH: str = os.getenv("MCP_HTTP_PATH", "/mcp")
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("MCP_LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("MCP_LOG_FILE", None)
    
    # Feature Flags - Recursive Thinking Tools
    ENABLE_Rcursive_Thinking_TOOLS: bool = os.getenv("ENABLE_Rcursive_Thinking_TOOLS", "true").lower() == "true"
    
    # Feature Flags - Sequential Thinking Tools
    ENABLE_ST_TOOLS: bool = os.getenv("ENABLE_ST_TOOLS", "true").lower() == "true"
    
    # Feature Flags - Tree of Thoughts Tools
    ENABLE_TOT_TOOLS: bool = os.getenv("ENABLE_TOT_TOOLS", "true").lower() == "true"
    
    # Feature Flags - Conversation Memory Tools
    ENABLE_CONVERSATION_MEMORY_TOOLS: bool = os.getenv("ENABLE_CONVERSATION_MEMORY_TOOLS", "true").lower() == "true"
    
    # Feature Flags - Planning Tools
    ENABLE_PLANNING_TOOLS: bool = os.getenv("ENABLE_PLANNING_TOOLS", "true").lower() == "true"
    
    # Feature Flags - WBS Execution Tools
    ENABLE_WBS_EXECUTION_TOOLS: bool = os.getenv("ENABLE_WBS_EXECUTION_TOOLS", "true").lower() == "true"
    
    # Feature Flags - Future tools placeholder
    ENABLE_FUTURE_TOOL_1: bool = os.getenv("ENABLE_FUTURE_TOOL_1", "false").lower() == "true"
    ENABLE_FUTURE_TOOL_2: bool = os.getenv("ENABLE_FUTURE_TOOL_2", "false").lower() == "true"
    
    # Recursive Thinking Specific Configuration
    Rcursive_Thinking_DEFAULT_LATENT_UPDATES: int = int(os.getenv("Rcursive_Thinking_DEFAULT_LATENT_UPDATES", "4"))
    Rcursive_Thinking_DEFAULT_MAX_IMPROVEMENTS: int = int(os.getenv("Rcursive_Thinking_DEFAULT_MAX_IMPROVEMENTS", "16"))
    Rcursive_Thinking_SESSION_TIMEOUT: int = int(os.getenv("Rcursive_Thinking_SESSION_TIMEOUT", "3600"))  # seconds
    
    # Output Directories Configuration
    # ChromaDB for Conversation Memory
    CONVERSATION_MEMORY_DB_PATH: str = str(OUTPUT_DIR / "chroma_db")
    CONVERSATION_MEMORY_DEFAULT_RESULTS: int = int(os.getenv("CONVERSATION_MEMORY_DEFAULT_RESULTS", "5"))
    
    # Planning Tool Output Configuration
    PLANNING_OUTPUT_DIR: Path = OUTPUT_DIR / "planning"
    PLANNING_WBS_FILENAME: str = os.getenv("PLANNING_WBS_FILENAME", "WBS.md")
    
    # Authentication (if needed)
    AUTH_ENABLED: bool = os.getenv("MCP_AUTH_ENABLED", "false").lower() == "true"
    AUTH_PROVIDER: Optional[str] = os.getenv("MCP_AUTH_PROVIDER", None)
    
    @classmethod
    def ensure_output_directories(cls) -> None:
        """Ensure all output directories exist"""
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.PLANNING_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        Path(cls.CONVERSATION_MEMORY_DB_PATH).mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def validate(cls) -> None:
        """Validate configuration settings"""
        valid_transports = ["stdio", "http", "sse"]
        if cls.TRANSPORT_TYPE not in valid_transports:
            raise ValueError(f"Invalid transport type. Must be one of: {valid_transports}")
        
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if cls.LOG_LEVEL not in valid_log_levels:
            raise ValueError(f"Invalid log level. Must be one of: {valid_log_levels}")
        
        if cls.Rcursive_Thinking_DEFAULT_LATENT_UPDATES < 1:
            raise ValueError("Rcursive_Thinking_DEFAULT_LATENT_UPDATES must be at least 1")
        
        if cls.Rcursive_Thinking_DEFAULT_MAX_IMPROVEMENTS < 1:
            raise ValueError("Rcursive_Thinking_DEFAULT_MAX_IMPROVEMENTS must be at least 1")
        
        # Ensure output directories exist
        cls.ensure_output_directories()


# Validate configuration and create directories on import
ServerConfig.validate()
