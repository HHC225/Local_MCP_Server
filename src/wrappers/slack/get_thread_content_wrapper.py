"""
Get Thread Content Wrapper for MCP Registration
"""
from fastmcp import Context
from src.tools.slack.get_thread_content_tool import GetThreadContentTool

# Initialize tool instance
_get_thread_tool = GetThreadContentTool()


async def get_thread_content(
    channel: str = None,
    timestamp: str = None,
    url: str = None,
    ctx: Context = None
) -> str:
    """
    Retrieve Slack thread content for analysis
    
    Retrieves all messages in a Slack thread including replies.
    Useful for analyzing discussion context and history.
    
    **Usage:**
    - Provide Slack URL (recommended): Automatically extracts channel and timestamp
    - Or provide channel + timestamp: Manual specification
    
    **Parameters:**
    - url: Slack URL (e.g., https://workspace.slack.com/archives/CHANNEL/pTIMESTAMP?thread_ts=THREAD_TS)
    - channel: Channel ID (e.g., C1234567890) - required if url not provided
    - timestamp: Thread timestamp (e.g., 1234567890.123456) - required if url not provided
    
    **Returns:**
    Formatted thread content with all messages, timestamps, and user information
    
    **Example:**
    ```python
    # Using URL
    content = await get_thread_content(
        url="https://workspace.slack.com/archives/C1234567890/p1234567890123456?thread_ts=1234567890.123456"
    )
    
    # Using channel + timestamp
    content = await get_thread_content(
        channel="C1234567890",
        timestamp="1234567890.123456"
    )
    ```
    
    **Use Cases:**
    - Analyzing team discussions
    - Reviewing decision-making threads
    - Extracting key information from conversations
    - Tracking issue resolution progress
    """
    return await _get_thread_tool.execute(
        channel=channel,
        timestamp=timestamp,
        url=url,
        ctx=ctx
    )
