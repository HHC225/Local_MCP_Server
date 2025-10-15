"""
Delete Message Wrapper for MCP Registration
"""
from fastmcp import Context
from src.tools.slack.delete_message_tool import DeleteMessageTool

# Initialize tool instance
_delete_message_tool = DeleteMessageTool()


async def delete_message(
    channel: str = None,
    ts: str = None,
    url: str = None,
    ctx: Context = None
) -> str:
    """
    Delete message from Slack channel
    
    Deletes a message from Slack channel. Can only delete messages sent by the bot
    or messages the bot has explicit permission to delete.
    
    **Parameters:**
    Method 1 - Using URL (recommended):
    - url: Slack message URL (e.g., https://workspace.slack.com/archives/CHANNEL/pTIMESTAMP)
    
    Method 2 - Using channel + timestamp:
    - channel: Channel ID (e.g., C1234567890)
    - ts: Message timestamp (e.g., 1234567890.123456)
    
    **Returns:**
    Success confirmation or detailed error message
    
    **Example:**
    ```python
    # Delete using URL
    result = await delete_message(
        url="https://workspace.slack.com/archives/C1234567890/p1234567890123456"
    )
    
    # Delete using channel + timestamp
    result = await delete_message(
        channel="C1234567890",
        ts="1234567890.123456"
    )
    ```
    
    **Use Cases:**
    - Remove incorrectly sent messages
    - Delete messages sent to wrong channel
    - Clean up test messages
    - Remove outdated information
    - Delete spam or inappropriate content (if bot has permission)
    
    **Requirements:**
    - Bot must have sent the message OR
    - Bot must have explicit delete permission
    - Valid channel ID and timestamp
    - Bot must be in channel
    
    **Important Warnings:**
    ⚠️ Deleted messages CANNOT be restored
    ⚠️ Deletion is permanent and immediate
    ⚠️ Consider archiving important messages before deletion
    
    **Error Cases:**
    - message_not_found: Message doesn't exist or already deleted
    - cant_delete_message: No permission to delete (not sent by bot)
    - channel_not_found: Invalid channel ID or bot not in channel
    - invalid_auth: Bot token authentication failed
    
    **Best Practices:**
    1. Verify message details before deletion
    2. Use URL method for accuracy
    3. Check bot permissions first
    4. Log important deletions
    5. Have backup/recovery plan for critical data
    """
    return await _delete_message_tool.execute(
        channel=channel,
        ts=ts,
        url=url,
        ctx=ctx
    )
