"""
Post Ephemeral Message Wrapper for MCP Registration
"""
from fastmcp import Context
from src.tools.slack.post_ephemeral_tool import PostEphemeralTool

# Initialize tool instance
_post_ephemeral_tool = PostEphemeralTool()


async def post_ephemeral_message(
    channel: str,
    content: str,
    title: str = None,
    thread_ts: str = None,
    format_type: str = 'detailed',
    user: str = None,
    ctx: Context = None
) -> str:
    """
    Post private message visible only to specific user
    
    Posts an ephemeral (temporary) message that only the specified user can see.
    Perfect for private analysis results, personal notifications, or sensitive information.
    
    **Parameters:**
    - channel: Channel ID (required, e.g., C1234567890)
    - content: Message content (required)
    - title: Message title (optional, adds header)
    - thread_ts: Thread timestamp for replying in thread (optional)
    - format_type: Display format - 'simple' or 'detailed' (default: 'detailed')
    - user: Target user ID (optional, uses default_user_id from config if not provided)
    
    **Returns:**
    Success confirmation with post details
    
    **Example:**
    ```python
    # Simple private message
    result = await post_ephemeral_message(
        channel="C1234567890",
        content="This is a private analysis result for you only."
    )
    
    # Detailed format with title
    result = await post_ephemeral_message(
        channel="C1234567890",
        title="Thread Analysis Report",
        content="Analysis results:\n- Key point 1\n- Key point 2\n- Key point 3",
        format_type='detailed'
    )
    
    # Reply to specific user in thread
    result = await post_ephemeral_message(
        channel="C1234567890",
        content="Here's the information you requested",
        thread_ts="1234567890.123456",
        user="U1234567890"
    )
    ```
    
    **Use Cases:**
    - Private analysis results
    - Personal search results
    - Individual notifications
    - Sensitive information sharing
    - User-specific feedback
    - Testing bot responses
    
    **Requirements:**
    - MUST use bot token (user token will fail)
    - Bot must be in channel
    - Target user must be channel member
    - default_user_id must be configured if user not specified
    
    **Important Notes:**
    - Message is temporary and disappears on page reload
    - Only visible to specified user
    - Cannot be seen by other channel members
    - Ideal for private bot interactions
    
    **Format Types:**
    - 'simple': Plain text with optional title
    - 'detailed': Structured format with enhanced readability
    """
    return await _post_ephemeral_tool.execute(
        channel=channel,
        content=content,
        title=title,
        thread_ts=thread_ts,
        format_type=format_type,
        user=user,
        ctx=ctx
    )
