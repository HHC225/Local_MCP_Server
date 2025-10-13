# Thinking Tools MCP Server

Advanced reasoning tools for AI assistants powered by Model Context Protocol (MCP). This server provides structured thinking methodologies including Recursive Thinking Model, Sequential Thinking, and Tree of Thoughts for complex problem-solving.

## ⚡ Quick Start

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

**Complete Workflow Example:**

1. **Initialize Session**
   ```
   Tool: recursive_thinking_initialize
   Parameters:
   - question: "How to design an efficient cache system in Python?"
   ```
   → Returns: session_id

2. **Deep Analysis (4 steps)**
   ```
   Tool: recursive_thinking_update_latent
   Step 1: Problem Decomposition - Break down cache requirements
   Step 2: Current State Analysis - Analyze existing approach
   Step 3: Alternative Perspectives - Consider different cache strategies
   Step 4: Synthesis - Develop improvement strategy
   ```

3. **Write Answer**
   ```
   Tool: recursive_thinking_update_answer
   Parameters:
   - improved_answer: "LRU cache with TTL and eviction policy..."
   - improvement_rationale: "Optimized based on latency and memory constraints"
   ```

4. **If Unsure → Repeat steps 2-3**
   
5. **If Confident → Get Result**
   ```
   Tool: recursive_thinking_get_result
   ```
   → If not verified: Auto-starts verification mode

6. **Verification (Auto-triggered)**
   ```
   Tool: recursive_thinking_update_latent (4 steps again)
   - Verify problem understanding
   - Check answer completeness
   - Test edge cases
   - Final validation
   ```

7. **Finalize Answer**
   ```
   Tool: recursive_thinking_update_answer
   - Final verified answer with verification insights
   ```

8. **Get Final Result**
   ```
   Tool: recursive_thinking_get_result
   ```
   → Returns: Complete verified answer + reasoning history

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

## 🧠 Available Tools

### Recursive Thinking Tools

Recursive Thinking implements recursive reasoning for iterative answer improvement through latent state updates.

#### Workflow Overview

1. **Initialize** → Start session
2. **Update Latent (4 steps)** → Analyze problem deeply  
3. **Update Answer** → Write/improve answer
4. **If unsure** → Repeat steps 2-3
5. **If confident** → Get Final Result
6. **Auto-verification** → If not verified, automatic 4-step verification starts
7. **Finalize** → Update answer with verification insights
8. **Get Final Result** → Retrieve verified answer

#### `recursive_thinking_initialize`
Initialize a new recursive reasoning session.

**Parameters:**
- `question` (string, required): The problem or question to solve
- `initial_answer` (string, optional): Starting answer (empty means start from scratch)
- `n_latent_updates` (integer, default: 4): Number of recursive latent updates per improvement step
- `max_improvements` (integer, default: 16): Maximum number of answer improvement iterations

**Returns:** Session confirmation with auto-generated unique session_id

#### `recursive_thinking_update_latent`
Update the latent reasoning state through recursive analysis.

**Parameters:**
- `session_id` (string, required): The reasoning session identifier
- `reasoning_insight` (string, required): Your new reasoning insight following step-by-step guidelines
- `step_number` (integer, required): Which latent update step (1 to n_latent_updates)

**Thinking Steps:**
1. **Problem Decomposition**: Break down the question into core components
2. **Current State Analysis**: Examine current answer's strengths and weaknesses
3. **Alternative Perspectives**: Consider different approaches and edge cases
4. **Synthesis**: Develop concrete improvement strategy

**Returns:** Status of latent update and guidance for next step

#### `recursive_thinking_update_answer`
Update the answer based on refined latent reasoning.

**Parameters:**
- `session_id` (string, required): The reasoning session identifier
- `improved_answer` (string, required): The new improved answer
- `improvement_rationale` (string, required): Brief explanation of improvements

**Returns:** Updated answer and guidance on whether to continue iterating

#### `recursive_thinking_get_result`
Retrieve the final answer and complete reasoning history.

**Parameters:**
- `session_id` (string, required): The reasoning session identifier

**Behavior:**
- **First call (not verified)**: Automatically starts verification mode → requires 4 update_latent steps → update_answer
- **Second call (verified)**: Returns complete verified results and reasoning trace

**Returns:** Either verification start instruction or complete verified results

#### `recursive_thinking_reset`
Reset or delete a reasoning session.

**Parameters:**
- `session_id` (string, required): The reasoning session identifier to reset

**Returns:** Confirmation of reset

### Sequential Thinking Tool (st)

Sequential analytical thinking for structured problem-solving where each thought builds upon previous insights.

**Parameters:**
- `thought` (string, required): Current analytical step
- `thought_number` (integer, required): Current sequence number (1, 2, 3...)
- `total_thoughts` (integer, required): Estimated total thoughts needed
- `next_thought_needed` (boolean, required): Whether another thought step is needed
- `is_revision` (boolean, optional): Whether this revises previous thinking
- `revises_thought` (integer, optional): Which thought is being reconsidered
- `branch_from_thought` (integer, optional): Branching point thought number
- `branch_id` (string, optional): Branch identifier
- `needs_more_thoughts` (boolean, optional): If more thoughts are needed
- `action_required` (boolean, optional): Whether this step requires direct action
- `action_type` (string, optional): Type of action (code_writing, file_creation, etc.)
- `action_description` (string, optional): Description of the action

**Use Cases:**
- System architecture design and component breakdown
- API endpoint structure and data flow planning
- Database schema optimization
- Code refactoring strategy
- Performance bottleneck analysis

**Returns:** JSON response with thought processing results

### Tree of Thoughts Tool (tt)

Advanced ToT framework for exploring multiple solution paths with branching, evaluation, and backtracking.

**Actions:**

#### `create_session`
Start a new problem-solving session.

**Parameters:**
- `action`: "create_session"
- `problem_statement` (string, required): Problem to solve
- `config` (object, optional): Configuration with search_strategy (bfs/dfs), generation_strategy (sampling/proposing), evaluation_method (value/vote), max_depth, max_branches

#### `add_thoughts`
Add multiple implementation approaches to the tree.

**Parameters:**
- `action`: "add_thoughts"
- `session_id` (string, required)
- `thoughts` (array, required): List of thought strings
- `parent_node_id` (string, optional): Parent node to attach thoughts to

#### `add_evaluation`
Add evaluation results for solutions.

**Parameters:**
- `action`: "add_evaluation"
- `session_id` (string, required)
- `node_id` (string, required): Node ID to evaluate
- `evaluation` (object, required): Contains value (1-10), confidence (0-1), viability (promising/uncertain/dead_end), reasoning

#### `search_next`
Find the next best approach to explore.

**Parameters:**
- `action`: "search_next"
- `session_id` (string, required)
- `search_strategy` (string, optional): "bfs" or "dfs"

#### `backtrack`
Return to previous design decisions.

**Parameters:**
- `action`: "backtrack"
- `session_id` (string, required)
- `dead_end_node_id` (string, required): Node that reached dead end
- `backtrack_strategy` (string, optional): parent, best_alternative, or root

#### `set_solution`
Document the final solution.

**Parameters:**
- `action`: "set_solution"
- `session_id` (string, required)
- `solution` (string, required): Final solution text

#### `get_session`
Retrieve complete analysis history.

**Parameters:**
- `action`: "get_session"
- `session_id` (string, required)

#### `list_sessions`
List all active sessions.

**Parameters:**
- `action`: "list_sessions"

#### `display_results`
Display ranked solutions with scores.

**Parameters:**
- `action`: "display_results"
- `session_id` (string, required)

**Use Cases:**
- Multi-architecture exploration (microservices vs monolith)
- Technology stack selection
- API design pattern comparison
- Database design alternatives
- DevOps pipeline design

**Returns:** JSON response with action results

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

## 📚 Additional Resources

- [QUICKSTART.md](QUICKSTART.md): Detailed quick start guide
- [CONTRIBUTING.md](CONTRIBUTING.md): Learn how to contribute
- [CHANGELOG.md](CHANGELOG.md): Version history
- [GitHub Issues](https://github.com/HHC225/Thinking_Tools_Local/issues): Report issues or suggest features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

**⚠️ Important: All contributions must go through Pull Requests**

- Direct commits to `main` branch are NOT allowed
- Fork the repository first
- Create a feature branch in your fork
- Submit a Pull Request for review

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines including:
- Branch protection policy
- Pull request process
- Coding standards
- Testing requirements

**Quick Start for Contributors:**
```bash
# 1. Fork the repo on GitHub
# 2. Clone YOUR fork
git clone https://github.com/YOUR_USERNAME/Thinking_Tools_Local.git
cd Thinking_Tools_Local

# 3. Add upstream
git remote add upstream https://github.com/HHC225/Thinking_Tools_Local.git

# 4. Create feature branch
git checkout -b feature/your-feature-name

# 5. Make changes, test, and submit PR
```

---

If issues persist, ask on [GitHub Issues](https://github.com/HHC225/Thinking_Tools_Local/issues)!
