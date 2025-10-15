# Local MCP Server

Advanced reasoning tools for AI assistants powered by Model Context Protocol (MCP). This server provides structured thinking methodologies for complex problem-solving.

## 📁 Project Structure

```
Local_MCP_Server/
├── main.py                 # Server entry point & tool registration
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
│
├── tools/                 # Tool implementations (business logic)
│   ├── base.py           # Base tool classes
│   ├── memory/           # Memory tools
│   │   └── conversation_memory_tool.py
│   └── reasoning/        # Reasoning tools
│       ├── recursive_thinking_tool.py
│       ├── sequential_thinking_tool.py
│       └── tree_of_thoughts_tool.py
│
├── wrappers/             # MCP registration wrappers
│   ├── memory/           # Memory tool wrappers
│   │   └── conversation_memory_wrappers.py
│   └── reasoning/        # Reasoning tool wrappers
│       ├── recursive_thinking_wrappers.py
│       ├── sequential_thinking_wrapper.py
│       └── tree_of_thoughts_wrapper.py
│
├── utils/                # Utilities
│   └── logger.py        # Logging configuration
│
├── chroma_db/           # ChromaDB persistent storage
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
| **Recursive Thinking** | Iterative refinement | Deep analysis, verification needed | High |
| **Sequential Thinking** | Linear progression | Step-by-step planning | Medium |
| **Tree of Thoughts** | Branching exploration | Comparing multiple options | High |

## 📖 Documentation

- **Tools**:
  - [Conversation Memory Guide](docs/conversation-memory.md)
  - [Recursive Thinking Guide](docs/recursive-thinking.md)
  - [Sequential Thinking Guide](docs/sequential-thinking.md)
  - [Tree of Thoughts Guide](docs/tree-of-thoughts.md)
- **Help**:
  - [Quick Start Guide](docs/quickstart.md)
  - [Troubleshooting Guide](docs/troubleshooting.md)
  - [GitHub Issues](https://github.com/HHC225/Local_MCP_Server/issues)

## 💡 Quick Tips

- **Adjust Log Level**: Create `.env` file and set `MCP_LOG_LEVEL="DEBUG"`
- **Enable/Disable Tools**: Use `ENABLE_*_TOOLS` settings in `.env`
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
