# Slack Tools for FastMCP

## Overview

Five essential Slack tools implemented in Python using FastMCP framework:
1. **Get Thread Content** - Retrieve entire Slack thread with all replies
2. **Get Single Message** - Retrieve a specific message without thread replies
3. **Post Message** - Send public messages to channels
4. **Post Ephemeral Message** - Send private messages to specific users
5. **Delete Message** - Remove messages from channels

## Architecture

```
Local_MCP_Server/
├── configs/
│   ├── slack.py.template                 # Template (commit to Git)
│   └── slack.py                          # Actual config (DO NOT commit)
├── src/
│   ├── tools/
│   │   └── slack/
│   │       ├── __init__.py
│   │       ├── get_thread_content_tool.py    # Thread retrieval tool (with replies)
│   │       ├── get_single_message_tool.py    # Single message retrieval tool
│   │       ├── post_message_tool.py          # Public message tool
│   │       ├── post_ephemeral_tool.py        # Private message tool
│   │       └── delete_message_tool.py        # Message deletion tool
│   └── wrappers/
│       └── slack/
│           ├── __init__.py
│           ├── get_thread_content_wrapper.py
│           ├── get_single_message_wrapper.py
│           ├── post_message_wrapper.py
│           ├── post_ephemeral_wrapper.py
│           └── delete_message_wrapper.py
└── main.py                                # Tool registration
```

## Key Design Decisions

### 1. **No Separate API Client**
- Slack API calls are integrated directly into each tool
- Uses `aiohttp` for async HTTP requests
- Reduces abstraction layers and complexity

### 2. **Consistent with Existing Tools**
- Follows same pattern as Recursive Thinking, Sequential Thinking, etc.
- Config file (`slack.py`) placed directly in `configs/` directory
- Tools inherit from `BaseTool` class
- Wrappers provide FastMCP-compatible interfaces

### 3. **Comprehensive Documentation**
- Each wrapper function has detailed docstrings
- Includes usage examples, parameters, return values
- Documents requirements and error cases
- Provides best practices and use cases

## Configuration

### Environment Variables

```bash
# Required
export SLACK_BOT_TOKEN="xoxb-your-bot-token-here"

# Optional (for user-level operations)
export SLACK_USER_TOKEN="xoxp-your-user-token-here"
```

### Configuration File

Edit `configs/slack.py` to customize:

```python
@dataclass
class SlackConfig:
    bot_token: str                        # Bot token (xoxb-...)
    user_token: Optional[str] = None      # User token (optional)
    base_url: str = "https://slack.com/api"
    timeout: int = 30                     # Request timeout (seconds)
    retry_attempts: int = 3               # Retry count
    workspace_domain: str = "your-workspace.slack.com"
    default_user_id: str = "U00000000"   # For ephemeral messages
    ENABLE_SLACK_TOOLS: bool = True       # Enable/disable flag
```

## Usage Examples

### 1. Get Thread Content (with all replies)

```python
from src.wrappers.slack import get_thread_content

# Using Slack URL (recommended)
content = await get_thread_content(
    url="https://your-workspace.slack.com/archives/C1234567890/p1234567890123456?thread_ts=1234567890.123456"
)

# Using channel + timestamp
content = await get_thread_content(
    channel="C1234567890",
    timestamp="1234567890.123456"
)
```

**Output:**
```
📨 **Slack Thread Content**
Channel: C1234567890
Thread TS: 1234567890.123456
Total Messages: 5

============================================================

[1] 2025-01-15 09:30:45 - User: U1234567890
Message text here...
------------------------------------------------------------
[2] 2025-01-15 09:31:20 - User: U0987654321
Reply text here...
------------------------------------------------------------
```

### 2. Get Single Message (without replies)

```python
from src.wrappers.slack import get_single_message

# Using Slack URL (recommended)
message = await get_single_message(
    url="https://your-workspace.slack.com/archives/C1234567890/p1234567890123456"
)

# Using channel + timestamp
message = await get_single_message(
    channel="C1234567890",
    timestamp="1234567890.123456"
)
```

**Output:**
```
📬 **Single Slack Message**

Channel: C1234567890
Timestamp: 1234567890.123456
Time: 2025-01-15 09:30:45
User: U1234567890
📎 Thread replies: 3
📁 Attachments: 1 file(s)
  [1] report.pdf (PDF)
💬 Reactions: thumbsup (5), eyes (2)

============================================================

Message content here...

============================================================
```

**Use Cases:**
- Quick message lookup without loading entire thread
- Checking message metadata (reactions, attachments)
- Verifying message existence
- Getting message details for reference

### 3. Post Public Message

```python
from src.wrappers.slack import post_message

# Simple message
result = await post_message(
    channel="C1234567890",
    text="Hello team! This is an announcement."
)

# Customized with emoji and username
result = await post_message(
    channel="C1234567890",
    text="*Daily Report* ✅\n\nAll tasks completed successfully!",
    username="Report Bot",
    icon_emoji=":chart_with_upwards_trend:"
)

# Reply to thread
result = await post_message(
    channel="C1234567890",
    text="Follow-up comment",
    thread_ts="1234567890.123456"
)
```

### 4. Post Private Message

```python
from src.wrappers.slack import post_ephemeral_message

# Simple private message
result = await post_ephemeral_message(
    channel="C1234567890",
    content="This is visible only to you."
)

# Detailed format with title
result = await post_ephemeral_message(
    channel="C1234567890",
    title="Analysis Report",
    content="Key findings:\n• Point 1\n• Point 2\n• Point 3",
    format_type='detailed'
)

# Specify target user (optional)
result = await post_ephemeral_message(
    channel="C1234567890",
    content="Personal notification",
    user="U1234567890"
)
```

### 5. Delete Message

```python
from src.wrappers.slack import delete_message

# Delete using URL (recommended)
result = await delete_message(
    url="https://your-workspace.slack.com/archives/C1234567890/p1234567890123456"
)

# Delete using channel + timestamp
result = await delete_message(
    channel="C1234567890",
    ts="1234567890.123456"
)
```

## Requirements

### Python Dependencies

```bash
pip install aiohttp fastmcp
```

### Slack Bot Permissions

Required OAuth scopes for bot token:
- `channels:history` - Read channel messages
- `channels:read` - View channel information
- `chat:write` - Send messages
- `chat:write.public` - Send messages to channels without joining
- `groups:history` - Read private channel messages
- `groups:read` - View private channel information

## Error Handling

All tools provide detailed error messages with troubleshooting guidance:

```python
# Example error response
❌ Failed to post message

**Error Details:**
- Channel: C1234567890
- Error: channel_not_found

**Possible Causes:**
- Invalid channel ID
- Bot not in channel
- Missing permissions
- Network/API error

**Solutions:**
1. Verify channel ID
2. Invite bot to channel
3. Check network connection
4. Retry after a moment
```

## Testing

### Test Connection

```python
from configs.slack import get_slack_config, validate_slack_config

config = get_slack_config()
is_valid = validate_slack_config(config)
print(f"Configuration valid: {is_valid}")
```

### Test Tool Execution

```python
# Test message posting
from src.wrappers.slack import post_message

result = await post_message(
    channel="C1234567890",
    text="Test message from Slack tools"
)
print(result)
```

## Security & Configuration

### Template vs Actual Configuration

**IMPORTANT**: Never commit actual workspace credentials to Git!

1. **Template File** (`configs/slack.py.template`):
   - Generic template with placeholder values
   - Safe to commit to Git
   - Contains example configuration structure

2. **Actual Configuration** (`configs/slack.py`):
   - Contains real workspace credentials
   - Must be in `.gitignore`
   - Created by copying and editing template

### Setup Instructions

```bash
# 1. Copy template to actual config
cp configs/slack.py.template configs/slack.py

# 2. Edit slack.py with your actual values
# Replace:
#   - workspace_domain: "your-workspace.slack.com" → "actual-workspace.slack.com"
#   - default_user_id: "U00000000" → "U01234567"
#   - bot_token via environment variable

# 3. Verify .gitignore includes slack.py
echo "configs/slack.py" >> .gitignore
```

## Comparison with TypeScript Implementation

| Feature | TypeScript | Python (FastMCP) |
|---------|-----------|------------------|
| API Client | Separate `SlackApiClient` class | Integrated into each tool |
| Framework | Custom MCP implementation | FastMCP framework |
| Async | Promises | asyncio/await |
| HTTP Library | axios | aiohttp |
| Configuration | `slack-config.ts` | `configs/slack.py` |
| Tool Registration | Manual export | `@mcp.tool()` decorator |

## Implementation Notes

### Why No Separate API Client?

1. **Simplicity**: Each tool is self-contained
2. **Clarity**: API calls visible in tool implementation
3. **Maintenance**: Easier to update individual tools
4. **FastMCP Pattern**: Aligns with FastMCP best practices

### Async Implementation

All tools use async/await pattern:
- `aiohttp` for non-blocking HTTP requests
- Compatible with FastMCP's async architecture
- Efficient for I/O-bound Slack API calls

### Error Messages

Designed for end-users:
- Clear problem description
- Possible causes listed
- Actionable solutions provided
- Context-specific guidance

## Troubleshooting

### Bot Token Issues

```bash
# Verify token format
echo $SLACK_BOT_TOKEN
# Should start with 'xoxb-'

# Test token validity
curl -X POST https://slack.com/api/auth.test \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN"
```

### Permission Errors

1. Check bot is in channel: `/invite @YourBotName`
2. Verify OAuth scopes in Slack App settings
3. Reinstall app if scopes changed

### Network Issues

1. Check firewall settings
2. Verify Slack API is accessible
3. Test with `curl` or `wget`

## Future Enhancements

Possible additions:
- Search messages
- Upload files
- Manage reactions
- Get channel history
- Bulk operations
- Rate limiting handling
- Retry with exponential backoff

## License

Same as parent project

## Contributing

Follow the existing tool pattern:
1. Create tool class in `src/tools/slack/`
2. Add wrapper function in `src/wrappers/slack/`
3. Register in `main.py`
4. Add comprehensive docstrings
5. Test thoroughly
6. Never commit actual credentials

## Support

For issues or questions:
1. Check logs in console output
2. Verify configuration
3. Test Slack API directly
4. Review error messages carefully
