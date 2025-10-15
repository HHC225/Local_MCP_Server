"""
Post Message Wrapper for MCP Registration
"""
from fastmcp import Context
from src.tools.slack.post_message_tool import PostMessageTool

# Initialize tool instance
_post_message_tool = PostMessageTool()


async def post_message(
    channel: str,
    text: str,
    username: str = None,
    icon_emoji: str = None,
    thread_ts: str = None,
    ctx: Context = None
) -> str:
    """
    Post public message to Slack channel
    
    Posts a message that all channel members can see.
    Ideal for team announcements, reports, and shared information.
    
    **Parameters:**
    - channel: Channel ID (required, e.g., C1234567890 or G01G9JY2U3C)
    - text: Message content (required)
    - username: Display name (optional, for bot customization)
    - icon_emoji: Icon emoji (optional, e.g., :robot_face:)
    - thread_ts: Thread timestamp for replying to existing thread (optional)
    
    **Returns:**
    Success confirmation with message timestamp and details
    
    **Example:**
    ```python
    # Simple message
    result = await post_message(
        channel="C1234567890",
        text="Hello team! This is an announcement."
    )
    
    # Customized message with emoji and username
    result = await post_message(
        channel="C1234567890",
        text="Daily report completed successfully ✅",
        username="Report Bot",
        icon_emoji=":chart_with_upwards_trend:"
    )
    
    # Reply to thread
    result = await post_message(
        channel="C1234567890",
        text="This is a follow-up comment",
        thread_ts="1234567890.123456"
    )
    ```
    
    **Use Cases:**
    - Team announcements
    - Daily digest reports
    - Status updates
    - Automated notifications
    - Scheduled messages
    
    **Requirements:**
    - Bot must be invited to the channel
    - Bot token must have chat:write permission
    - Channel ID must be valid
    
    **Note:**
    Message formatting supports Slack markdown:
    - *bold text*
    - _italic text_
    - `code`
    - ```code block```
    - > quote
    - • bullet list
    """
    return await _post_message_tool.execute(
        channel=channel,
        text=text,
        username=username,
        icon_emoji=icon_emoji,
        thread_ts=thread_ts,
        ctx=ctx
    )
