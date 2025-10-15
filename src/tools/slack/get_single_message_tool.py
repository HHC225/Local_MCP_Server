"""
Get Single Message Tool
Retrieves a specific Slack message without thread replies
"""
import re
from typing import Optional, Dict, Any
from datetime import datetime
import aiohttp

from src.tools.base import BaseTool
from configs.slack import get_slack_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class GetSingleMessageTool(BaseTool):
    """
    Tool to retrieve a single Slack message without thread replies
    """
    
    def __init__(self):
        super().__init__(
            name="get_single_message",
            description="Retrieves a single Slack message without thread replies"
        )
        self.config = get_slack_config()
    
    async def execute(
        self,
        channel: Optional[str] = None,
        timestamp: Optional[str] = None,
        url: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Execute single message retrieval
        
        Args:
            channel: Channel ID (required if url not provided)
            timestamp: Message timestamp (required if url not provided)
            url: Slack URL to extract channel and timestamp from
            
        Returns:
            Formatted single message content
        """
        try:
            # Parse URL if provided
            if url:
                parsed = self._parse_slack_url(url)
                channel = parsed['channel']
                timestamp = parsed['message_ts']
            
            if not channel or not timestamp:
                raise ValueError("Either url or (channel + timestamp) must be provided")
            
            # Normalize timestamp
            timestamp = self._normalize_timestamp(timestamp)
            
            # Fetch single message
            message = await self._fetch_single_message(channel, timestamp)
            
            # Format for output
            formatted = self._format_message_content(message, channel, timestamp)
            
            return formatted
            
        except Exception as e:
            logger.error(f"Failed to get single message: {e}")
            return f"❌ Failed to retrieve single message: {str(e)}"
    
    def _parse_slack_url(self, url: str) -> Dict[str, Optional[str]]:
        """
        Parse Slack URL to extract channel and message timestamp
        
        Args:
            url: Slack message URL
            
        Returns:
            Dict with channel and message_ts
        """
        # Pattern: https://workspace.slack.com/archives/CHANNEL/pTIMESTAMP
        pattern = r'https://[^/]+/archives/([^/]+)/p(\d+)'
        match = re.search(pattern, url)
        
        if not match:
            raise ValueError(f"Invalid Slack URL format: {url}")
        
        channel = match.group(1)
        message_ts_raw = match.group(2)
        
        # Convert pTIMESTAMP to timestamp format
        message_ts = f"{message_ts_raw[:10]}.{message_ts_raw[10:]}"
        
        return {
            'channel': channel,
            'message_ts': message_ts
        }
    
    def _normalize_timestamp(self, ts: str) -> str:
        """Normalize timestamp to Slack format"""
        if '.' not in ts and ts.isdigit():
            # Unix timestamp to Slack format
            return f"{ts[:10]}.{ts[10:]}" if len(ts) > 10 else f"{ts}.000000"
        return ts
    
    async def _fetch_single_message(
        self,
        channel: str,
        timestamp: str
    ) -> Dict[str, Any]:
        """
        Fetch a single message using Slack API
        Uses conversations.history with inclusive timestamps
        
        Args:
            channel: Channel ID
            timestamp: Message timestamp
            
        Returns:
            Message dictionary
        """
        url = f"{self.config.base_url}/conversations.history"
        
        # Use USER token for GET operations (better channel access)
        token = self.config.user_token if self.config.user_token else self.config.bot_token
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        params = {
            'channel': channel,
            'latest': timestamp,
            'oldest': timestamp,
            'inclusive': 'true',
            'limit': 1
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                data = await response.json()
                
                if not data.get('ok'):
                    error_msg = data.get('error', 'Unknown error')
                    raise Exception(f"Slack API error: {error_msg}")
                
                messages = data.get('messages', [])
                if not messages:
                    raise Exception(f"Message not found: {timestamp}")
                
                return messages[0]
    
    def _format_message_content(
        self,
        message: Dict[str, Any],
        channel: str,
        timestamp: str
    ) -> str:
        """
        Format single message for output
        
        Args:
            message: Message dictionary
            channel: Channel ID
            timestamp: Message timestamp
            
        Returns:
            Formatted string
        """
        msg_ts = message.get('ts', timestamp)
        user = message.get('user', 'Unknown')
        text = message.get('text', '')
        
        # Format timestamp to readable format
        try:
            dt = datetime.fromtimestamp(float(msg_ts))
            time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            time_str = msg_ts
        
        # Check if message has thread replies
        reply_count = message.get('reply_count', 0)
        thread_info = f"\n📎 Thread replies: {reply_count}" if reply_count > 0 else ""
        
        # Extract attachments info if any
        attachments = message.get('files', [])
        attachments_info = ""
        if attachments:
            attachments_info = f"\n📁 Attachments: {len(attachments)} file(s)"
            for idx, file in enumerate(attachments, 1):
                file_name = file.get('name', 'Unknown')
                file_type = file.get('pretty_type', file.get('filetype', 'File'))
                attachments_info += f"\n  [{idx}] {file_name} ({file_type})"
        
        # Extract reactions if any
        reactions = message.get('reactions', [])
        reactions_info = ""
        if reactions:
            reactions_info = "\n💬 Reactions: "
            reaction_list = [f"{r.get('name', '?')} ({r.get('count', 0)})" for r in reactions]
            reactions_info += ", ".join(reaction_list)
        
        output = f"""📬 **Single Slack Message**

Channel: {channel}
Timestamp: {msg_ts}
Time: {time_str}
User: {user}{thread_info}{attachments_info}{reactions_info}

{"="*60}

{text}

{"="*60}
"""
        
        return output
