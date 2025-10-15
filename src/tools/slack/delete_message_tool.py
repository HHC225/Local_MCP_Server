"""
Delete Message Tool
Deletes messages from Slack channels
"""
import re
from typing import Optional
import aiohttp

from src.tools.base import BaseTool
from configs.slack import get_slack_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DeleteMessageTool(BaseTool):
    """
    Tool to delete messages from Slack channels
    Can only delete messages sent by the bot or messages the bot has permission to delete
    """
    
    def __init__(self):
        super().__init__(
            name="delete_message",
            description="Deletes message from Slack channel"
        )
        self.config = get_slack_config()
    
    async def execute(
        self,
        channel: Optional[str] = None,
        ts: Optional[str] = None,
        url: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Execute message deletion
        
        Args:
            channel: Channel ID (required if url not provided)
            ts: Message timestamp (required if url not provided)
            url: Slack message URL to extract channel and timestamp
            
        Returns:
            Success/failure message with details
        """
        try:
            # Parse URL if provided
            if url:
                parsed = self._parse_slack_url(url)
                channel = parsed['channel']
                ts = parsed['ts']
            
            if not channel or not ts:
                raise ValueError("Either url or (channel + ts) must be provided")
            
            # Validate timestamp format
            if not re.match(r'^\d+\.\d+$', ts):
                raise ValueError(f"Invalid timestamp format: {ts}. Expected format: 1234567890.123456")
            
            # Delete message via Slack API
            await self._delete_message(channel, ts)
            
            return self._format_success_response(channel, ts)
            
        except Exception as e:
            logger.error(f"Failed to delete message: {e}")
            return self._format_error_response(str(e), channel, ts)
    
    def _parse_slack_url(self, url: str) -> dict:
        """
        Parse Slack URL to extract channel and timestamp
        
        Args:
            url: Slack message URL
            
        Returns:
            Dict with channel and ts
        """
        # Pattern: https://workspace.slack.com/archives/CHANNEL/pTIMESTAMP
        pattern = r'https://[^/]+/archives/([^/]+)/p(\d+)'
        match = re.search(pattern, url)
        
        if not match:
            raise ValueError(f"Invalid Slack URL format: {url}")
        
        channel = match.group(1)
        timestamp_raw = match.group(2)
        
        # Convert pTIMESTAMP to timestamp format
        timestamp = f"{timestamp_raw[:10]}.{timestamp_raw[10:]}"
        
        return {
            'channel': channel,
            'ts': timestamp
        }
    
    async def _delete_message(self, channel: str, ts: str) -> None:
        """
        Delete message via Slack API
        
        Args:
            channel: Channel ID
            ts: Message timestamp
        """
        url = f"{self.config.base_url}/chat.delete"
        headers = {
            'Authorization': f'Bearer {self.config.bot_token}',
            'Content-Type': 'application/json'
        }
        payload = {
            'channel': channel,
            'ts': ts
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                data = await response.json()
                
                if not data.get('ok'):
                    error_msg = data.get('error', 'Unknown error')
                    raise Exception(f"Slack API error: {error_msg}")
    
    def _format_success_response(self, channel: str, ts: str) -> str:
        """Format success response"""
        return f"""✅ Message deleted successfully

📋 **Deletion Details:**
- Channel: {channel}
- Timestamp: {ts}
- Status: Deleted

💡 Deleted messages cannot be restored."""
    
    def _format_error_response(
        self,
        error: str,
        channel: Optional[str],
        ts: Optional[str]
    ) -> str:
        """Format error response"""
        error_details = []
        
        if 'message_not_found' in error:
            error_details.append("🔍 **Error:** Message not found")
            error_details.append("**Check:**")
            error_details.append("  - Verify channel ID is correct")
            error_details.append("  - Verify timestamp is correct")
            error_details.append("  - Message may already be deleted")
        elif 'cant_delete_message' in error:
            error_details.append("🚫 **Error:** No permission to delete this message")
            error_details.append("**Check:**")
            error_details.append("  - Message must be sent by bot")
            error_details.append("  - Bot must have delete permissions")
        elif 'channel_not_found' in error:
            error_details.append("🔍 **Error:** Channel not found")
            error_details.append("**Check:**")
            error_details.append("  - Verify channel ID is correct")
            error_details.append("  - Bot must be in channel")
        else:
            error_details.append(f"🔍 **Error:** {error}")
            error_details.append("**Common Causes:**")
            error_details.append("  - Network connection issues")
            error_details.append("  - Slack API authentication issues")
            error_details.append("  - Insufficient permissions")
        
        result = [
            "❌ Failed to delete message\n",
            f"Channel: {channel or 'N/A'}",
            f"Timestamp: {ts or 'N/A'}",
            ""
        ]
        result.extend(error_details)
        
        return "\n".join(result)
