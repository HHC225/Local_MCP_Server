"""
Get Single Message Wrapper for MCP Registration
"""
from fastmcp import Context
from src.tools.slack.get_single_message_tool import GetSingleMessageTool

# Initialize tool instance
_get_single_message_tool = GetSingleMessageTool()


async def get_single_message(
    channel: str = None,
    timestamp: str = None,
    url: str = None,
    ctx: Context = None
) -> str:
    """
    Retrieve a single Slack message without thread replies
    
    Retrieves only the specified message without any thread replies.
    Useful for getting specific message content or checking message details.
    
    **Usage:**
    - Provide Slack URL (recommended): Automatically extracts channel and timestamp
    - Or provide channel + timestamp: Manual specification
    
    **Parameters:**
    - url: Slack URL (e.g., https://workspace.slack.com/archives/CHANNEL/pTIMESTAMP)
    - channel: Channel ID (e.g., C1234567890) - required if url not provided
    - timestamp: Message timestamp (e.g., 1234567890.123456) - required if url not provided
    
    **Returns:**
    Formatted single message with metadata (reactions, attachments, thread info)
    
    **Example:**
    ```python
    # Using URL
    message = await get_single_message(
        url="https://workspace.slack.com/archives/C1234567890/p1234567890123456"
    )
    
    # Using channel + timestamp
    message = await get_single_message(
        channel="C1234567890",
        timestamp="1234567890.123456"
    )
    ```
    
    **Use Cases:**
    - Getting specific message content
    - Checking message metadata (reactions, attachments)
    - Verifying message existence
    - Quick message lookup without thread context
    
    **Note:**
    - If you need all thread replies, use `get_thread_content` instead
    - This tool only returns the single specified message
    """
    if ctx:
        ctx.info(f"Retrieving single message - Channel: {channel or 'from URL'}, TS: {timestamp or 'from URL'}")
    
    result = await _get_single_message_tool.execute(
        channel=channel,
        timestamp=timestamp,
        url=url
    )
    
    if ctx:
        ctx.info("Single message retrieval completed")
    
    return result
