# Quick Start Guide

Get up and running with Thinking Tools MCP Server in under 5 minutes.

## Prerequisites

- Python 3.12 or higher
- macOS, Linux, or Windows
- Claude Desktop, VSCode, or Cursor IDE

## Installation Steps

### Step 1: Install uv (Optional but Recommended)

uv is a fast Python package installer that's 10-100x faster than pip.

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternative (using pip):**
```bash
pip install uv
```

### Step 2: Clone Repository

```bash
git clone https://github.com/HHC225/Thinking_Tools_Local.git
cd Thinking_Tools_Local
```

### Step 3: Create Virtual Environment

**Using uv (recommended):**
```bash
uv venv
```

**Using Python venv:**
```bash
python -m venv .venv
```

### Step 4: Activate Virtual Environment

**macOS/Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```powershell
.venv\Scripts\activate
```

### Step 5: Install Dependencies

**Using uv:**
```bash
uv pip install -r requirements.txt
```

**Using pip:**
```bash
pip install -r requirements.txt
```

### Step 6: Test Server

```bash
python main.py
```

You should see:
```
INFO: Initializing Thinking Tools MCP Server v1.0.0
INFO: Registering Recursive Thinking tools...
INFO: Registering Sequential Thinking tools...
INFO: Registering Tree of Thoughts tools...
```

Press `Ctrl+C` to stop the server.

## IDE Configuration

### Claude Desktop

1. **Find config file location:**
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Get absolute path:**
   ```bash
   pwd  # Run this in Thinking_Tools_Local directory
   ```

3. **Edit config file:**
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

   **Windows example:**
   ```json
   {
     "mcpServers": {
       "thinking-tools": {
         "command": "C:\\Users\\YourName\\Thinking_Tools_Local\\.venv\\Scripts\\python.exe",
         "args": ["C:\\Users\\YourName\\Thinking_Tools_Local\\main.py"]
       }
     }
   }
   ```

4. **Restart Claude Desktop completely**

5. **Verify connection:**
   - Click 🔌 icon in bottom-left corner
   - Look for "thinking-tools" server

### VSCode / Cursor

1. **Create `.vscode` folder in your project:**
   ```bash
   mkdir -p .vscode
   ```

2. **Create `.vscode/settings.json`:**
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

3. **Restart VSCode/Cursor**

4. **Verify in MCP panel**

## First Test

### Try Recursive Thinking

Ask your AI assistant:

```
Use recursive thinking to help me design a caching system in Python.

1. Initialize a session with the question
2. Run the 4-step analysis
3. Write an answer
4. Get the result
```

### Try Sequential Thinking

```
Use sequential thinking to plan an API endpoint for user authentication.
Go through 5 thoughts covering requirements, design, implementation, testing, and deployment.
```

### Try Tree of Thoughts

```
Use tree of thoughts to compare REST vs GraphQL for my mobile app backend.
Generate 3 initial approaches, evaluate each, and select the best.
```

## Troubleshooting

### Server Not Found

**Check paths are absolute:**
```bash
# Get absolute path
cd /path/to/Thinking_Tools_Local
pwd  # Copy this path
```

**Verify Python path:**
```bash
which python  # macOS/Linux
where python  # Windows
```

### Import Errors

```bash
# Reinstall dependencies
uv pip install -r requirements.txt --reinstall
```

### Python Version Error

```bash
# Check version (must be 3.12+)
python --version

# Install Python 3.12+
# macOS:
brew install python@3.12

# Linux:
sudo apt install python3.12  # Ubuntu/Debian
sudo dnf install python3.12  # Fedora

# Windows:
# Download from python.org
```

### Permission Errors (macOS/Linux)

```bash
chmod +x main.py
chmod -R u+x .venv/bin/
```

## Configuration Options

Create `.env` file in root directory:

```bash
# Log level
MCP_LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR

# Enable/disable specific tools
ENABLE_RECURSIVE_THINKING_TOOLS=true
ENABLE_SEQUENTIAL_THINKING_TOOLS=true
ENABLE_TREE_OF_THOUGHTS_TOOLS=true
```

## Next Steps

1. **Read tool documentation:**
   - [Recursive Thinking Guide](recursive-thinking.md)
   - [Sequential Thinking Guide](sequential-thinking.md)
   - [Tree of Thoughts Guide](tree-of-thoughts.md)

2. **Try example problems:**
   - System design challenges
   - Algorithm optimization
   - Architecture decisions

3. **Explore advanced features:**
   - Session management
   - Custom configurations
   - Tool combinations

## Getting Help

- **Troubleshooting**: See [Troubleshooting Guide](troubleshooting.md)
- **Issues**: [GitHub Issues](https://github.com/HHC225/Thinking_Tools_Local/issues)
- **Documentation**: [Main README](../README.md)

## Quick Reference

### Common Commands

```bash
# Activate environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install/update dependencies
uv pip install -r requirements.txt

# Run server
python main.py

# Update uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Check Python version
python --version

# Get current directory path
pwd  # macOS/Linux
cd    # Windows
```

### Path Templates

**macOS:**
```
/Users/YourUsername/Thinking_Tools_Local/.venv/bin/python
/Users/YourUsername/Thinking_Tools_Local/main.py
```

**Linux:**
```
/home/YourUsername/Thinking_Tools_Local/.venv/bin/python
/home/YourUsername/Thinking_Tools_Local/main.py
```

**Windows:**
```
C:\Users\YourUsername\Thinking_Tools_Local\.venv\Scripts\python.exe
C:\Users\YourUsername\Thinking_Tools_Local\main.py
```

---

Ready to start? Head back to the [Main README](../README.md) or dive into [tool documentation](recursive-thinking.md)!
