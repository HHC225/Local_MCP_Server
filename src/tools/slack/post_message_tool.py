"""
Post Message Tool
Posts public messages to Slack channels
"""
from typing import Optional
import aiohttp

from src.tools.base import BaseTool
from configs.slack import get_slack_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PostMessageTool(BaseTool):
    """
    Tool to post public messages to Slack channels
    All channel members can view these messages
    """
    
    def __init__(self):
        super().__init__(
            name="post_message",
            description="Posts public message to Slack channel"
        )
        self.config = get_slack_config()
    
    async def execute(
        self,
        channel: str,
        text: str,
        username: Optional[str] = None,
        icon_emoji: Optional[str] = None,
        thread_ts: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Execute message posting
        
        Args:
            channel: Channel ID (required)
            text: Message text (required)
            username: Display name (optional)
            icon_emoji: Icon emoji (optional, e.g., :robot_face:)
            thread_ts: Thread timestamp for reply (optional)
            
        Returns:
            Success/failure message with details
        """
        try:
            if not channel or not text:
                raise ValueError("Both 'channel' and 'text' are required parameters")
            
            # Prepare message payload
            payload = {
                'channel': channel,
                'text': text
            }
            
            if username:
                payload['username'] = username
            if icon_emoji:
                payload['icon_emoji'] = icon_emoji
            if thread_ts:
                payload['thread_ts'] = thread_ts
            
            # Send message via Slack API
            result = await self._post_message(payload)
            
            return self._format_success_response(result, channel, text)
            
        except Exception as e:
            logger.error(f"Failed to post message: {e}")
            return self._format_error_response(str(e), channel)
    
    async def _post_message(self, payload: dict) -> dict:
        """
        Post message via Slack API
        
        Args:
            payload: Message payload
            
        Returns:
            API response dict
        """
        url = f"{self.config.base_url}/chat.postMessage"
        headers = {
            'Authorization': f'Bearer {self.config.bot_token}',
            'Content-Type': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                data = await response.json()
                
                if not data.get('ok'):
                    error_msg = data.get('error', 'Unknown error')
                    raise Exception(f"Slack API error: {error_msg}")
                
                return data
    
    def _format_success_response(
        self,
        result: dict,
        channel: str,
        text: str
    ) -> str:
        """Format success response"""
        timestamp = result.get('ts', 'N/A')
        preview = text[:100] + '...' if len(text) > 100 else text
        
        return f"""✅ Message posted successfully

**Post Details:**
- Channel: {channel}
- Timestamp: {timestamp}
- Message Length: {len(text)} characters

**Message Preview:**
{preview}"""
    
    def _format_error_response(self, error: str, channel: str) -> str:
        """Format error response"""
        return f"""❌ Failed to post message

**Error Details:**
- Channel: {channel}
- Error: {error}

**Possible Causes:**
- Invalid channel ID
- Bot not in channel
- Missing permissions
- Network/API error

**Solutions:**
1. Verify channel ID
2. Invite bot to channel
3. Check network connection
4. Retry after a moment"""
