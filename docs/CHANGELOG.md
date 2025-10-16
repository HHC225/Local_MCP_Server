# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0] - 2025-10-16

### Added
- **Vibe Coding Tool** - Interactive prompt refinement through clarifying questions
  - Prevents AI from making assumptions about vague requirements
  - Provides exactly 3 specific alternatives at each decision point
  - Interactive loop that waits for explicit user selection
  - Session management to maintain conversation context
  - Progressive refinement until prompt is fully concrete
  
### Features
- **Actions**: start, respond, get_status, list_sessions, finalize
- **3 Alternatives Rule**: Always provides exactly 3 specific suggestions
- **No Assumptions**: Forces explicit user choices instead of AI guessing
- **Session Persistence**: In-memory sessions with full conversation history
- **Status Flow**: refinement_needed → awaiting_response → completed

### Technical Details
- Implementation: `src/tools/vibe/vibe_coding_tool.py`
- Wrapper: `src/wrappers/vibe/vibe_coding_wrapper.py`
- Configuration: `configs/vibe.py`
- Feature flag: `ENABLE_VIBE_CODING` in configs/vibe.py
- Global session store: `vc_sessions` dictionary

### Configuration Options
- `ENABLE_VIBE_CODING`: Enable/disable tool (default: true)
- `MAX_REFINEMENT_STAGES`: Maximum refinement cycles (default: 10)
- `NUM_SUGGESTIONS`: Number of alternatives to provide (default: 3)
- `SESSION_TIMEOUT`: Session timeout in seconds (default: 3600)

### Documentation
- Added comprehensive [Vibe Coding Guide](docs/vibe-coding.md)
- Updated README with Vibe Coding section and examples
- Added to tool comparison table
- Includes AI usage patterns and best practices

### Use Cases
- Refining vague project requirements into concrete specifications
- Exploring architecture alternatives systematically
- Making informed technology stack decisions
- Building detailed specifications from high-level ideas
- Structured requirement gathering with stakeholders

## [1.3.0] - 2025-10-15

### Added
- **WBS Execution Tool** - Systematic task-by-task execution for WBS-based projects
  - Parse WBS markdown files and extract hierarchical tasks
  - Execute tasks step-by-step with deep thinking analysis
  - Real-time checkbox updates in WBS files after task completion
  - Automatic dependency resolution and validation
  - Session management for resumable execution
  - Progress tracking with completion statistics
  - Error prevention through strict validation
  - Complex task detection with Sequential Thinking integration
  - Parent task auto-completion when all children complete
  
### Features
- **Actions**: start, continue, execute_task, get_status, list_sessions
- **Dependency Management**: Enforces proper execution order
- **Error Handling**: Validates prerequisites before execution
- **File Updates**: Real-time WBS file checkbox synchronization
- **Session Persistence**: In-memory sessions with full state tracking

### Technical Details
- Implementation: `tools/planning/wbs_execution_tool.py`
- Wrapper: `wrappers/planning/wbs_execution_wrapper.py`
- Feature flag: `ENABLE_WBS_EXECUTION_TOOLS` in config.py
- Follows Planning Tool directory structure
- Compatible with Planning Tool WBS output format

### Documentation
- Added comprehensive [WBS Execution Guide](docs/wbs-execution.md)
- Updated README with tool comparison and examples
- Added API reference and troubleshooting section

## [1.2.0] - 2025-10-15

### Changed
- **Configuration System Refactoring**
  - Removed `.env` file dependency - `config.py` is now the main configuration file
  - Direct configuration in `config.py` with environment variable override support
  - Cleaner, more maintainable configuration approach

### Added
- **Centralized Output Directory Management**
  - New `output/` directory for all tool-generated files
  - `output/chroma_db/` - ChromaDB conversation memory storage
  - `output/planning/` - Planning tool WBS files
  - Auto-creation of output directories on startup
- **Planning Tool Configuration**
  - `PLANNING_OUTPUT_DIR` - configurable planning output directory
  - `PLANNING_WBS_FILENAME` - customizable WBS filename
  - Default WBS files now saved to `output/planning/`

### Fixed
- ChromaDB path now uses centralized config
- Planning tool WBS export now uses centralized output directory
- Removed hardcoded paths from tool implementations

### Technical Details
- `ServerConfig.ensure_output_directories()` - auto-creates all output paths
- `Path` objects used for cross-platform path handling
- Backward compatible: environment variables still work for overrides
- Migrated existing `chroma_db/` data to `output/chroma_db/`

### Documentation
- Updated README with new configuration section
- Marked `.env.example` as deprecated
- Added output directory structure documentation

## [1.1.0] - 2025-10-14

### Added
- **Conversation Memory Tool** with ChromaDB integration
  - Store important conversation summaries with speaker tracking
  - Semantic search for retrieving relevant conversations
  - Automatic embedding generation (no manual embedding needed)
  - Metadata filtering and organization
  - List, delete, and clear operations
  - Persistent storage across server restarts
- New `tools/memory/` directory for memory-related tools
- ChromaDB dependency (v1.1.1) with automatic embedding support
- Comprehensive documentation:
  - Full feature guide: `docs/conversation-memory.md`
  - Setup and configuration: `docs/conversation-memory-setup.md`
- Test suite: `test_conversation_memory.py`
- Configuration options:
  - `ENABLE_CONVERSATION_MEMORY_TOOLS` flag
  - `CONVERSATION_MEMORY_DB_PATH` for custom database location
  - `CONVERSATION_MEMORY_DEFAULT_RESULTS` for query limits

### Changed
- Reorganized tool structure: memory tools now in separate directory
- Updated `requirements.txt` with all installed dependencies (generated from pip freeze)
- Enhanced README with Conversation Memory section
- Updated `.gitignore` to exclude ChromaDB database files

### Technical Details
- ChromaDB uses `all-MiniLM-L6-v2` embedding model (384 dimensions)
- Automatic persistence to disk (SQLite + embeddings)
- Semantic similarity search with distance scoring
- Support for custom metadata schemas

## [1.0.0] - 2025-10-13

### Added
- Initial release of Thinking Tools MCP Server
- Recursive Thinking Model reasoning tools
  - Initialize reasoning sessions
  - Update latent reasoning with 4-step systematic analysis
  - Update answer based on reasoning insights
  - Verify final answer with mandatory verification loop
  - Get result and status of sessions
  - Reset sessions
- Sequential Thinking tool for structured analytical thinking
  - Sequential thought progression
  - Revision capabilities
  - Branch exploration
  - Action execution integration
- Tree of Thoughts tool for complex problem-solving
  - Session creation and management
  - Thought node addition
  - Node evaluation
  - Search strategies (BFS/DFS)
  - Backtracking capabilities
  - Solution ranking and display
- FastMCP server implementation with modular architecture
- Comprehensive logging system
- Environment-based configuration management
- Feature flags for tool activation/deactivation

### Documentation
- Complete README.md with installation and usage instructions
- CONTRIBUTING.md for contribution guidelines
- LICENSE file (MIT License)
- .env.example for environment configuration
- Detailed tool documentation with parameters and examples

### Configuration
- .gitignore for Python projects
- .gitattributes for consistent line endings
- Environment variable support via python-dotenv
- Configurable logging levels

## [Unreleased]

### Planned
- Persistent session storage (SQLite/Redis)
- Web UI interface
- Additional thinking tools (Analogical Reasoning, Critical Thinking)
- Tool integration workflows
- Performance metrics and analytics
- Multi-language support
- Unit tests and integration tests
- CI/CD pipeline
- Docker containerization
- API documentation with examples

---

For more details, see the [full commit history](https://github.com/HHC225/Thinking_Tools_Local/commits/main).
