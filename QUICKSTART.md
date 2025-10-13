# Thinking Tools MCP Server - Quick Start Guide

Get up and running with Thinking Tools MCP Server in just 5 minutes.

## ⚡ 5-Minute Quick Start

### 1. Clone and Install (2 minutes)

```bash
# Clone repository
git clone https://github.com/HHC225/Thinking_Tools_Local.git
cd Thinking_Tools_Local

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# or: pip install uv

# Create virtual environment
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies with uv
uv pip install -r requirements.txt
```

### 2. Test Server (1 minute)

```bash
# Run server test
python main.py
```

If working correctly, you'll see:
```
INFO: Initializing Thinking Tools MCP Server v1.0.0
INFO: Registering Recursive Thinking tools...
INFO: Registering Sequential Thinking tools...
INFO: Registering Tree of Thoughts tools...
```

Press `Ctrl+C` to stop the server.

### 3. IDE Setup (2 minutes)

#### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "thinking-tools": {
      "command": "/ABSOLUTE/PATH/TO/Thinking_Tools_Local/.venv/bin/python",
      "args": ["/ABSOLUTE/PATH/TO/Thinking_Tools_Local/main.py"]
    }
  }
}
```

**Important**: Replace `/ABSOLUTE/PATH/TO/` with your actual path!

Get path:
```bash
pwd  # Prints current directory absolute path
```

#### VSCode/Cursor

Create `.vscode/settings.json` in your project:

```json
{
  "mcp.servers": {
    "thinking-tools": {
      "command": "/ABSOLUTE/PATH/TO/Thinking_Tools_Local/.venv/bin/python",
      "args": ["/ABSOLUTE/PATH/TO/Thinking_Tools_Local/main.py"]
    }
  }
}
```

### 4. Restart IDE and Verify

1. Completely close and restart IDE
2. Claude Desktop: Click 🔌 icon in bottom-left to verify "thinking-tools"
3. VSCode/Cursor: Check server status in MCP panel

## 🎯 First Use

### Solving Problems with Recursive Thinking

1. **Start Session**
   ```
   Tool: recursive_thinking_initialize
   Parameters:
   - question: "How to design an efficient cache system in Python?"
   ```

2. **4-Step Analysis**
   ```
   Tool: recursive_thinking_update_latent (run 4 times)
   Step 1: Problem Decomposition
   Step 2: Current State Analysis
   Step 3: Alternative Perspectives
   Step 4: Integration Strategy
   ```

3. **Improve Answer**
   ```
   Tool: recursive_thinking_update_answer
   Parameters:
   - improved_answer: "Design combining LRU cache with TTL..."
   ```

4. **Get Result**
   ```
   Tool: recursive_thinking_get_result
   ```

### Step-by-Step Analysis with Sequential Thinking

```
Tool: st
Parameters:
- thought: "First step in API endpoint design: Requirements analysis"
- thought_number: 1
- total_thoughts: 5
- next_thought_needed: true
```

### Compare Options with Tree of Thoughts

```
Tool: tt
Parameters:
- action: "create_session"
- problem_statement: "Microservices vs Monolithic architecture choice"
```

## 🔧 Troubleshooting

### Server Not Connecting

1. **Verify Paths**
   ```bash
   # Check Python path
   which python  # or absolute path of .venv/bin/python
   
   # Check main.py path
   ls -la main.py
   pwd
   ```

2. **Use Absolute Paths**
   - Relative path (❌): `./main.py`
   - Absolute path (✅): `/Users/username/Thinking_Tools_Local/main.py`

3. **Restart IDE**

### Import Errors

```bash
# Reinstall dependencies with uv
uv pip install -r requirements.txt --reinstall

# Add PYTHONPATH to IDE config
"env": {
  "PYTHONPATH": "/ABSOLUTE/PATH/TO/Thinking_Tools_Local"
}
```

### Python Version Error

```bash
# Check Python version (must be 3.12+)
python --version

# Install Python 3.12+
# macOS:
brew install python@3.12

# Or use pyenv:
pyenv install 3.12
pyenv local 3.12
```

### Permission Errors (macOS/Linux)

```bash
chmod +x main.py
chmod +x setup_git.sh
```

## 📚 Next Steps

- [README.md](README.md): Read full documentation
- [CONTRIBUTING.md](CONTRIBUTING.md): Learn how to contribute
- [GitHub Issues](https://github.com/HHC225/Thinking_Tools_Local/issues): Report issues or suggest features

## 💡 Tips

1. **Adjust Log Level**: Create `.env` file and set `MCP_LOG_LEVEL="DEBUG"`
2. **Use Specific Tools**: Change `ENABLE_*_TOOLS` settings in `.env`
3. **Manage Sessions**: Save session IDs in notepad for later reuse
4. **Use uv for Speed**: `uv` is much faster than `pip` for package installation

## 🚀 Why uv?

[uv](https://github.com/astral-sh/uv) is a fast Python package installer written in Rust:

- ⚡ **10-100x faster** than pip
- 🔒 **Built-in dependency resolution**
- 🎯 **Drop-in replacement** for pip
- 🔄 **Compatible** with requirements.txt

### Common uv Commands

```bash
# Install packages
uv pip install package_name

# Install from requirements.txt
uv pip install -r requirements.txt

# Create virtual environment
uv venv

# Sync dependencies
uv pip sync requirements.txt
```

---

If issues persist, ask on [GitHub Issues](https://github.com/HHC225/Thinking_Tools_Local/issues)!
