# Local MCP Server

Advanced reasoning tools for AI assistants powered by Model Context Protocol (MCP). This server provides structured thinking methodologies for complex problem-solving.

## 📁 Project Structure

```
Local_MCP_Server/
├── main.py                 # Server entry point & tool registration
├── config.py              # Configuration management (no .env needed)
├── requirements.txt       # Python dependencies
│
├── tools/                 # Tool implementations (business logic)
│   ├── base.py           # Base tool classes
│   ├── memory/           # Memory tools
│   │   └── conversation_memory_tool.py
│   ├── planning/         # Planning tools
│   │   ├── planning_tool.py
│   │   └── wbs_execution_tool.py
│   └── reasoning/        # Reasoning tools
│       ├── recursive_thinking_tool.py
│       ├── sequential_thinking_tool.py
│       └── tree_of_thoughts_tool.py
│
├── wrappers/             # MCP registration wrappers
│   ├── memory/           # Memory tool wrappers
│   │   └── conversation_memory_wrappers.py
│   ├── planning/         # Planning tool wrappers
│   │   ├── planning_wrapper.py
│   │   └── wbs_execution_wrapper.py
│   └── reasoning/        # Reasoning tool wrappers
│       ├── recursive_thinking_wrappers.py
│       ├── sequential_thinking_wrapper.py
│       └── tree_of_thoughts_wrapper.py
│
├── utils/                # Utilities
│   └── logger.py        # Logging configuration
│
├── output/              # All tool-generated outputs
│   ├── chroma_db/       # ChromaDB persistent storage
│   └── planning/        # WBS and planning files
│
└── docs/                # Documentation
```

### Architecture Design

**Separation of Concerns**:
- **`tools/`**: Core tool implementations with business logic
- **`wrappers/`**: MCP-specific wrappers with tool descriptions for registration
- **`main.py`**: Central registration point that imports from `wrappers/`

This structure ensures:
- ✅ Clean separation between tool logic and MCP interface
- ✅ Easy maintenance (modify wrappers without touching tool logic)
- ✅ Scalability (add new tools without cluttering existing directories)

## ⚡ Quick Start

### 1. Clone and Install

```bash
# Clone repository
git clone https://github.com/HHC225/Local_MCP_Server.git
cd Local_MCP_Server

# Install uv (fast Python package installer)
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# or: pip install uv

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### 2. Test Server

```bash
python main.py
```

Expected output:
```
INFO: Initializing Thinking Tools MCP Server v1.0.0
INFO: Registering Recursive Thinking tools...
INFO: Registering Sequential Thinking tools...
INFO: Registering Tree of Thoughts tools...
INFO: Registering Conversation Memory tools...
INFO: Registering Planning tool...
INFO: Registering WBS Execution tool...
```

Press `Ctrl+C` to stop.

### 3. Configure Your IDE

#### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "thinking-tools": {
      "command": "/ABSOLUTE/PATH/TO/Local_MCP_Server/.venv/bin/python",
      "args": ["/ABSOLUTE/PATH/TO/Local_MCP_Server/main.py"]
    }
  }
}
```

#### VSCode/Cursor (macOS/Linux)

Create `.vscode/settings.json`:

```json
{
  "mcp.servers": {
    "thinking-tools": {
      "command": "/ABSOLUTE/PATH/TO/Local_MCP_Server/.venv/bin/python",
      "args": ["/ABSOLUTE/PATH/TO/Local_MCP_Server/main.py"]
    }
  }
}
```

**Important**: Replace `/ABSOLUTE/PATH/TO/` with your actual path! Use `pwd` to get it.

#### VSCode/Cursor (Windows with WSL)

Edit `%APPDATA%\Code\User\mcp.json`:

```json
{
  "servers": {
    "thinking-tools": {
      "command": "C:\\Windows\\System32\\wsl.exe",
      "args": [
        "-d", "Ubuntu",
        "--cd", "/home/YOUR_USERNAME/Local_MCP_Server",
        "/home/YOUR_USERNAME/Local_MCP_Server/.venv/bin/python3",
        "/home/YOUR_USERNAME/Local_MCP_Server/main.py"
      ],
      "env": {
        "NODE_ENV": "production",
        "CHROMA_DB_PATH": "./chroma_db"
      },
      "type": "stdio"
    }
  }
}
```

**Important**: 
- Replace `YOUR_USERNAME` with your WSL username (use `whoami` in WSL to get it)
- Replace `Ubuntu` with your WSL distribution name if different (use `wsl -l` in PowerShell)
- Full path example: `/home/john/Local_MCP_Server`

### 4. Restart IDE and Verify

1. Completely close and restart your IDE
2. Claude Desktop: Click 🔌 icon to verify "thinking-tools" server
3. VSCode/Cursor: Check MCP panel for server status

## 🧠 Available Tools

### [Conversation Memory](docs/conversation-memory.md)

Store and retrieve important conversation context using ChromaDB vector database.

**Best for**: Maintaining context across conversations, remembering important decisions, building knowledge base

**Quick Example**:
```
1. Store conversation summary with speaker info
2. Query relevant past conversations
3. Build context-aware responses
```

[📖 Full Documentation →](docs/conversation-memory.md) | [🔧 Setup Guide →](docs/conversation-memory-setup.md)

### [Recursive Thinking](docs/recursive-thinking.md)

Iterative answer improvement through deep recursive analysis with automatic verification.

**Best for**: Complex algorithm design, system architecture decisions, deep technical analysis

**Quick Example**:
```
1. Initialize session with your problem
2. Run 4-step deep analysis (update_latent)
3. Write improved answer (update_answer)
4. Get result → Auto-verification starts if needed
5. Finalize with verified answer
```

[📖 Full Documentation →](docs/recursive-thinking.md)

### [Sequential Thinking](docs/sequential-thinking.md)

Step-by-step structured analysis where each thought builds on previous insights.

**Best for**: API design, database schema planning, code refactoring strategies

**Quick Example**:
```
Thought 1: Problem analysis
Thought 2: Initial approach
Thought 3: Refinement (can revise earlier thoughts)
Thought N: Final solution
```

[📖 Full Documentation →](docs/sequential-thinking.md)

### [Planning Tool](docs/planning.md)

Create structured Work Breakdown Structures (WBS) before implementation to prevent common development issues.

**Best for**: Project decomposition, task planning, WBS creation, dependency mapping

**Quick Example**:
```
Step 1: Problem analysis and breakdown
Step 2: Identify tasks and subtasks with WBS items
Step 3: Add dependencies and priorities
Step N: Final WBS export to markdown with checkboxes
```

[📖 Full Documentation →](docs/planning.md)

### [WBS Execution Tool](docs/wbs-execution.md)

Systematic task-by-task execution tool for WBS-based project implementation with real-time progress tracking.

**Best for**: Implementing planned tasks, dependency-aware execution, progress tracking

**Quick Example**:
```
1. Start: Load WBS file and create session
2. Continue: Get next executable task
3. Execute: Implement task with thinking analysis
4. Repeat: Continue until all tasks complete
```

[📖 Full Documentation →](docs/wbs-execution.md)

### [Tree of Thoughts](docs/tree-of-thoughts.md)

Explore multiple solution paths with branching, evaluation, and backtracking.

**Best for**: Technology stack selection, architecture comparisons, multi-option decisions

**Quick Example**:
```
1. Create session with problem
2. Add multiple solution approaches
3. Evaluate each with scores
4. Explore promising paths deeper
5. Backtrack from dead ends
6. Select optimal solution
```

[📖 Full Documentation →](docs/tree-of-thoughts.md)

## 🛠️ Tool Comparison

| Tool | Structure | Best For | Complexity |
|------|-----------|----------|------------|
| **Conversation Memory** | Vector DB storage | Context retention, knowledge base | Low |
| **Planning Tool** | WBS hierarchy | Project breakdown, task planning | Medium |
| **WBS Execution Tool** | Task execution | Implementing WBS tasks systematically | Medium |
| **Recursive Thinking** | Iterative refinement | Deep analysis, verification needed | High |
| **Sequential Thinking** | Linear progression | Step-by-step planning | Medium |
| **Tree of Thoughts** | Branching exploration | Comparing multiple options | High |

## 📖 Documentation

- **Tools**:
  - [Conversation Memory Guide](docs/conversation-memory.md)
  - [Planning Tool Guide](docs/planning.md)
  - [WBS Execution Tool Guide](docs/wbs-execution.md)
  - [Recursive Thinking Guide](docs/recursive-thinking.md)
  - [Sequential Thinking Guide](docs/sequential-thinking.md)
  - [Tree of Thoughts Guide](docs/tree-of-thoughts.md)
- **Help**:
  - [Quick Start Guide](docs/quickstart.md)
  - [Troubleshooting Guide](docs/troubleshooting.md)
  - [GitHub Issues](https://github.com/HHC225/Local_MCP_Server/issues)

## ⚙️ Configuration

This server uses **`config.py`** as the main configuration file - **no `.env` file needed**!

### Direct Configuration

Edit `config.py` directly to change settings:

```python
class ServerConfig:
    # Server settings
    SERVER_NAME: str = "Thinking Tools MCP Server"
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR
    
    # Output directories (auto-created)
    OUTPUT_DIR: Path = BASE_DIR / "output"
    PLANNING_OUTPUT_DIR: Path = OUTPUT_DIR / "planning"
    CONVERSATION_MEMORY_DB_PATH: str = str(OUTPUT_DIR / "chroma_db")
    
    # Planning tool
    PLANNING_WBS_FILENAME: str = "WBS.md"
    
    # Feature flags
    ENABLE_Rcursive_Thinking_TOOLS: bool = True
    ENABLE_ST_TOOLS: bool = True
    ENABLE_TOT_TOOLS: bool = True
    ENABLE_CONVERSATION_MEMORY_TOOLS: bool = True
    ENABLE_PLANNING_TOOLS: bool = True
    ENABLE_WBS_EXECUTION_TOOLS: bool = True
```

### Environment Variable Overrides

You can still override settings via environment variables:

```bash
# Temporary override for one session
MCP_LOG_LEVEL=DEBUG python main.py

# Or set in your shell profile
export MCP_LOG_LEVEL=DEBUG
export ENABLE_TOT_TOOLS=false
```

### Output Directory Structure

All tool-generated files are organized under `output/`:

```
output/
├── chroma_db/          # Conversation Memory database
│   ├── chroma.sqlite3
│   └── [vector data]
└── planning/           # Planning tool WBS files
    ├── Project_Name_WBS.md
    └── Another_Project_WBS.md
```

**Note**: The `output/` directory is in `.gitignore` and created automatically on startup.

## 💡 Quick Tips

- **Adjust Log Level**: Edit `LOG_LEVEL` in `config.py` or use `MCP_LOG_LEVEL` env var
- **Enable/Disable Tools**: Edit `ENABLE_*_TOOLS` in `config.py`
- **Output Location**: All files go to `output/` directory (auto-organized)
- **Save Session IDs**: Keep them in notepad for resuming later
- **Use uv for Speed**: 10-100x faster than pip for installations

## 🚀 Why uv?

[uv](https://github.com/astral-sh/uv) is a fast Python package installer:
- ⚡ 10-100x faster than pip
- 🔒 Built-in dependency resolution
- 🎯 Drop-in replacement for pip

```bash
# Common uv commands
uv pip install package_name
uv pip install -r requirements.txt
uv venv
```

## 🤝 Contributing

**⚠️ Important: All contributions must go through Pull Requests**

1. Fork the repository on GitHub
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Local_MCP_Server.git`
3. Create feature branch: `git checkout -b feature/your-feature`
4. Make changes, test, and submit PR

Direct commits to `main` branch are NOT allowed.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Need help?** Check the [Troubleshooting Guide](docs/troubleshooting.md) or [open an issue](https://github.com/HHC225/Local_MCP_Server/issues)!
