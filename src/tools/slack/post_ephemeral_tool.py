"""
Post Ephemeral Message Tool
Posts private messages visible only to specific users
"""
from typing import Optional
import aiohttp

from src.tools.base import BaseTool
from configs.slack import get_slack_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PostEphemeralTool(BaseTool):
    """
    Tool to post ephemeral (private) messages to Slack
    Only visible to the specified user
    """
    
    def __init__(self):
        super().__init__(
            name="post_ephemeral_message",
            description="Posts private message visible to specific user only"
        )
        self.config = get_slack_config()
    
    async def execute(
        self,
        channel: str,
        content: str,
        title: Optional[str] = None,
        thread_ts: Optional[str] = None,
        format_type: str = 'detailed',
        user: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Execute ephemeral message posting
        
        Args:
            channel: Channel ID (required)
            content: Message content (required)
            title: Message title (optional)
            thread_ts: Thread timestamp for reply (optional)
            format_type: Display format ('simple' or 'detailed')
            user: User ID (optional, uses default_user_id from config)
            
        Returns:
            Success/failure message with details
        """
        try:
            if not channel or not content:
                raise ValueError("Both 'channel' and 'content' are required parameters")
            
            # Use default user if not specified
            target_user = user or self.config.default_user_id
            
            if not target_user:
                raise ValueError("User ID not specified and default_user_id not configured")
            
            # Format message text
            message_text = self._format_message(content, title, format_type)
            
            # Prepare payload
            payload = {
                'channel': channel,
                'user': target_user,
                'text': message_text
            }
            
            if thread_ts:
                payload['thread_ts'] = thread_ts
            
            # Send ephemeral message via Slack API
            result = await self._post_ephemeral(payload)
            
            return self._format_success_response(result, channel, target_user)
            
        except Exception as e:
            logger.error(f"Failed to post ephemeral message: {e}")
            return self._format_error_response(str(e), channel)
    
    def _format_message(
        self,
        content: str,
        title: Optional[str],
        format_type: str
    ) -> str:
        """
        Format message content based on type
        
        Args:
            content: Main content
            title: Optional title
            format_type: 'simple' or 'detailed'
            
        Returns:
            Formatted message text
        """
        if format_type == 'simple':
            return f"{title}\n\n{content}" if title else content
        else:
            # Detailed format with structure
            parts = []
            if title:
                parts.append(f"*{title}*")
                parts.append("")
            parts.append(content)
            return "\n".join(parts)
    
    async def _post_ephemeral(self, payload: dict) -> dict:
        """
        Post ephemeral message via Slack API
        
        Args:
            payload: Message payload
            
        Returns:
            API response dict
        """
        url = f"{self.config.base_url}/chat.postEphemeral"
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
        user: str
    ) -> str:
        """Format success response"""
        return f"""✅ Ephemeral message posted successfully

**Post Details:**
- Channel: {channel}
- Target User: {user}
- Message Type: Private (Ephemeral)

**Note:** This message is only visible to the specified user."""
    
    def _format_error_response(self, error: str, channel: str) -> str:
        """Format error response"""
        return f"""❌ Failed to post ephemeral message

**Error Details:**
- Channel: {channel}
- Error: {error}

**Possible Causes:**
- Bot token required (user token won't work)
- Bot not in channel
- User not in channel
- Invalid user ID

**Solutions:**
1. Verify bot token is configured
2. Invite bot to channel
3. Verify user is channel member
4. Check default_user_id in config"""
