# Contributing to Thinking Tools MCP Server

Thank you for your interest in contributing to Thinking Tools MCP Server! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## 📜 Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please be respectful and constructive in all interactions.

## 🚀 Getting Started

### ⚠️ Important: Branch Protection Policy

**Direct commits to `main` branch are NOT allowed for contributors.**

All contributions must go through the Pull Request process:

1. **Fork** the repository on GitHub (do NOT clone the main repository directly)
2. **Clone** your fork locally
3. **Create a new branch** for your feature or bugfix (never work on main)
4. Make your changes
5. Test your changes thoroughly
6. **Submit a Pull Request** to the main repository

### Contribution Workflow

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or bugfix
4. Make your changes
5. Test your changes thoroughly
6. Submit a pull request

## 🔧 Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Setup Steps

```bash
# 1. Fork the repository on GitHub first!
# 2. Clone YOUR fork (not the main repository)
git clone https://github.com/YOUR_USERNAME/Thinking_Tools_Local.git
cd Thinking_Tools_Local

# 3. Add upstream remote to sync with main repository
git remote add upstream https://github.com/HHC225/Thinking_Tools_Local.git

# 4. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 5. Install dependencies
pip install -r requirements.txt

# Install development dependencies (if any)
pip install -r requirements-dev.txt  # If exists

# Copy environment variables
cp .env.example .env
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=tools --cov=utils

# Run specific test file
python -m pytest tests/test_Rcursive_Thinking_tools.py
```

## 🤝 How to Contribute

### Reporting Bugs

When reporting bugs, please include:

- Clear and descriptive title
- Detailed description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, IDE)
- Error logs (if applicable)

**Template:**
```markdown
**Bug Description:**
A clear and concise description of the bug.

**To Reproduce:**
1. Step 1
2. Step 2
3. ...

**Expected Behavior:**
What you expected to happen.

**Actual Behavior:**
What actually happened.

**Environment:**
- OS: [e.g., macOS 13.0]
- Python Version: [e.g., 3.9.6]
- IDE: [e.g., VSCode with Copilot]

**Logs:**
```
paste relevant logs here
```
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

- Clear and descriptive title
- Detailed description of the enhancement
- Use cases and benefits
- Possible implementation approach
- Any relevant examples or mockups

### Adding New Tools

To add a new thinking tool:

1. **Create Tool Class**

```python
# tools/your_category/your_tool.py
from tools.base import ReasoningTool
from typing import Dict, Any
from fastmcp import Context

class YourTool(ReasoningTool):
    """Your tool description"""
    
    def __init__(self):
        super().__init__(
            name="your_tool",
            description="Detailed description of what your tool does"
        )
    
    async def execute(self, **kwargs) -> str:
        """
        Execute your tool logic
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            str: JSON string with results
        """
        # Implementation
        pass
```

2. **Register in Package**

```python
# tools/__init__.py
from .your_category.your_tool import YourTool

__all__ = [
    # ... existing tools
    'YourTool',
]
```

3. **Add to Main Server**

```python
# main.py
if ServerConfig.ENABLE_YOUR_TOOL:
    from tools import YourTool
    
    logger.info("Registering your tool...")
    your_tool = YourTool()
    
    @mcp.tool()
    async def your_tool_name(param1: str, param2: int, ctx: Context = None) -> str:
        """
        Tool description for IDE autocomplete
        
        Args:
            param1: Description of param1
            param2: Description of param2
            
        Returns:
            Result description
        """
        return await your_tool.execute(param1=param1, param2=param2, ctx=ctx)
```

4. **Add Configuration**

```python
# config.py
class ServerConfig:
    # ... existing config
    ENABLE_YOUR_TOOL: bool = os.getenv("ENABLE_YOUR_TOOL", "true").lower() == "true"
```

```bash
# .env.example
ENABLE_YOUR_TOOL="true"
```

5. **Document Your Tool**

Add comprehensive documentation to `README.md`:

```markdown
### Your Tool Name

Brief description of what the tool does.

#### `your_tool_name`
Detailed description.

**Parameters:**
- `param1` (type, required/optional): Description
- `param2` (type, required/optional): Description

**Returns:** Description of return value

**Example Usage:**
```
Example of how to use the tool
```
```

6. **Add Tests**

```python
# tests/test_your_tool.py
import pytest
from tools.your_category.your_tool import YourTool

def test_your_tool_initialization():
    tool = YourTool()
    assert tool.name == "your_tool"

async def test_your_tool_execution():
    tool = YourTool()
    result = await tool.execute(param1="test")
    assert result is not None
```

## 📏 Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line Length**: Maximum 100 characters (not 79)
- **Imports**: Group in order: standard library, third-party, local
- **Docstrings**: Use Google-style docstrings
- **Type Hints**: Use type hints for all function signatures
- **Naming**:
  - Classes: `PascalCase`
  - Functions/Variables: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
  - Private: `_leading_underscore`

### Example Code Style

```python
"""
Module docstring describing the module purpose.
"""
from typing import Dict, Any, Optional, List
import json
from datetime import datetime

from fastmcp import Context
from tools.base import ReasoningTool


class ExampleTool(ReasoningTool):
    """
    Brief one-line description.
    
    More detailed description of the tool, its purpose,
    and how it should be used.
    """
    
    def __init__(self):
        """Initialize the tool with default configuration."""
        super().__init__(
            name="example_tool",
            description="Tool description"
        )
        self._internal_state: Dict[str, Any] = {}
    
    async def execute(
        self,
        required_param: str,
        optional_param: Optional[int] = None,
        ctx: Context = None
    ) -> str:
        """
        Execute the tool logic.
        
        Args:
            required_param: Description of required parameter
            optional_param: Description of optional parameter
            ctx: FastMCP context (injected automatically)
        
        Returns:
            JSON string containing the result
        
        Raises:
            ValueError: If required_param is empty
        """
        if not required_param:
            raise ValueError("required_param cannot be empty")
        
        # Implementation
        result = self._process_data(required_param, optional_param)
        
        return json.dumps({
            "status": "success",
            "data": result
        }, indent=2)
    
    def _process_data(
        self,
        data: str,
        option: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Internal helper method.
        
        Args:
            data: Data to process
            option: Optional processing option
        
        Returns:
            Processed result
        """
        # Implementation
        return {"processed": data}
```

### Documentation Standards

- All public classes and methods must have docstrings
- Use type hints consistently
- Include parameter descriptions and return values
- Provide usage examples for complex tools
- Keep README.md updated with new features

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── __init__.py
├── test_Rcursive_Thinking_tools.py
├── test_sequential_thinking.py
├── test_tree_of_thoughts.py
└── test_utils.py
```

### Writing Tests

```python
import pytest
from tools.reasoning.Rcursive_Thinking_tools import Rcursive_ThinkingInitializeTool

@pytest.fixture
def Rcursive_Thinking_tool():
    """Fixture providing a Rcursive_Thinking tool instance."""
    return Rcursive_ThinkingInitializeTool()

class TestRcursive_ThinkingInitialize:
    """Test suite for Rcursive_Thinking initialization tool."""
    
    @pytest.mark.asyncio
    async def test_basic_initialization(self, Rcursive_Thinking_tool):
        """Test basic tool initialization."""
        result = await Rcursive_Thinking_tool.execute(
            question="Test question",
            initial_answer=""
        )
        assert result is not None
        assert "session_id" in result
    
    @pytest.mark.asyncio
    async def test_with_initial_answer(self, Rcursive_Thinking_tool):
        """Test initialization with initial answer."""
        result = await Rcursive_Thinking_tool.execute(
            question="Test question",
            initial_answer="Initial guess"
        )
        data = json.loads(result)
        assert data["answer"] == "Initial guess"
    
    @pytest.mark.asyncio
    async def test_invalid_parameters(self, Rcursive_Thinking_tool):
        """Test handling of invalid parameters."""
        with pytest.raises(ValueError):
            await Rcursive_Thinking_tool.execute(question="")
```

### Test Coverage

- Aim for at least 80% code coverage
- Test both success and failure cases
- Test edge cases and boundary conditions
- Mock external dependencies

## 💬 Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(Rcursive_Thinking): add verification step to Rcursive_Thinking reasoning

Add a mandatory verification step before finalizing answers.
This ensures higher quality results by performing a final
4-step analysis of the answer.

Closes #123
```

```
fix(sequential): resolve branch tracking issue

Fixed issue where branch IDs were not properly tracked
when creating multiple branches from the same thought.

Fixes #456
```

## 🔄 Pull Request Process

### Branch Naming Convention

Use descriptive branch names:
- `feature/description` - for new features
- `fix/description` - for bug fixes
- `docs/description` - for documentation
- `refactor/description` - for code refactoring
- `test/description` - for test additions/updates

Examples:
```bash
# Create a feature branch
git checkout -b feature/add-reasoning-tool

# Create a bugfix branch
git checkout -b fix/sequential-thinking-error

# Create a docs branch
git checkout -b docs/update-quickstart
```

### Keeping Your Fork Updated

Before starting work, always sync with upstream:

```bash
# Fetch latest changes from upstream
git fetch upstream

# Switch to your main branch
git checkout main

# Merge upstream changes
git merge upstream/main

# Push to your fork
git push origin main
```

### Before Submitting

1. ✅ Update documentation
2. ✅ Add/update tests
3. ✅ Ensure all tests pass
4. ✅ Update CHANGELOG.md
5. ✅ Follow code style guidelines
6. ✅ Rebase on latest main branch

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
Describe how you tested your changes

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Changes are backwards compatible (or breaking changes documented)

## Related Issues
Closes #XXX
```

### Review Process

1. At least one maintainer must approve
2. All CI checks must pass
3. No unresolved conversations
4. Up-to-date with main branch

### After Approval

Your PR will be merged using one of these strategies:
- **Squash and merge**: For feature branches
- **Rebase and merge**: For clean, logical commits
- **Merge commit**: For significant features with valuable history

## 🎯 Priority Areas

We especially welcome contributions in these areas:

1. **Testing**: Expand test coverage
2. **Documentation**: Improve examples and guides
3. **Performance**: Optimize tool execution
4. **New Tools**: Add more thinking/reasoning tools
5. **Bug Fixes**: Address reported issues
6. **UI/UX**: Improve developer experience

## ❓ Questions?

If you have questions about contributing:

1. Check existing issues and discussions
2. Open a new discussion in GitHub Discussions
3. Reach out to maintainers

## 🙏 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!
