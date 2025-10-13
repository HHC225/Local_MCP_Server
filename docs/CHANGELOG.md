# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
