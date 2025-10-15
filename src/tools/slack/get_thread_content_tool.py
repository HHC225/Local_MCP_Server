"""
Get Thread Content Tool
Retrieves Slack thread content including all messages and replies
"""
import re
from typing import Optional, Dict, Any, List
from datetime import datetime
import aiohttp
import asyncio

from src.tools.base import BaseTool
from configs.slack import get_slack_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class GetThreadContentTool(BaseTool):
    """
    Tool to retrieve Slack thread content with all messages and replies
    """
    
    def __init__(self):
        super().__init__(
            name="get_thread_content",
            description="Retrieves Slack thread content for analysis"
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
        Execute thread content retrieval
        
        Args:
            channel: Channel ID (required if url not provided)
            timestamp: Thread timestamp (required if url not provided)
            url: Slack URL to extract channel and timestamp from
            
        Returns:
            Formatted thread content for analysis
        """
        try:
            # Parse URL if provided
            if url:
                parsed = self._parse_slack_url(url)
                channel = parsed['channel']
                timestamp = parsed['thread_ts'] or parsed['message_ts']
            
            if not channel or not timestamp:
                raise ValueError("Either url or (channel + timestamp) must be provided")
            
            # Normalize timestamp
            timestamp = self._normalize_timestamp(timestamp)
            
            # Fetch thread messages
            messages = await self._fetch_thread_messages(channel, timestamp)
            
            # Format for output
            formatted = self._format_thread_content(messages, channel, timestamp)
            
            return formatted
            
        except Exception as e:
            logger.error(f"Failed to get thread content: {e}")
            return f"❌ Failed to retrieve thread content: {str(e)}"
    
    def _parse_slack_url(self, url: str) -> Dict[str, Optional[str]]:
        """
        Parse Slack URL to extract channel and timestamps
        
        Args:
            url: Slack message URL
            
        Returns:
            Dict with channel, message_ts, and thread_ts
        """
        # Pattern: https://workspace.slack.com/archives/CHANNEL/pTIMESTAMP?thread_ts=THREAD_TS
        pattern = r'https://[^/]+/archives/([^/]+)/p(\d+)(?:\?thread_ts=([\d.]+))?'
        match = re.search(pattern, url)
        
        if not match:
            raise ValueError(f"Invalid Slack URL format: {url}")
        
        channel = match.group(1)
        message_ts_raw = match.group(2)
        thread_ts = match.group(3)
        
        # Convert pTIMESTAMP to timestamp format
        message_ts = f"{message_ts_raw[:10]}.{message_ts_raw[10:]}"
        
        return {
            'channel': channel,
            'message_ts': message_ts,
            'thread_ts': thread_ts
        }
    
    def _normalize_timestamp(self, ts: str) -> str:
        """Normalize timestamp to Slack format"""
        if '.' not in ts and ts.isdigit():
            # Unix timestamp to Slack format
            return f"{ts[:10]}.{ts[10:]}" if len(ts) > 10 else f"{ts}.000000"
        return ts
    
    async def _fetch_thread_messages(
        self,
        channel: str,
        thread_ts: str
    ) -> List[Dict[str, Any]]:
        """
        Fetch all messages in a thread using Slack API
        Uses USER token for better channel access
        
        Args:
            channel: Channel ID
            thread_ts: Thread timestamp
            
        Returns:
            List of message dictionaries
        """
        url = f"{self.config.base_url}/conversations.replies"
        
        # Use USER token for GET operations (better channel access)
        token = self.config.user_token if self.config.user_token else self.config.bot_token
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        params = {
            'channel': channel,
            'ts': thread_ts,
            'limit': 1000
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                data = await response.json()
                
                if not data.get('ok'):
                    error_msg = data.get('error', 'Unknown error')
                    raise Exception(f"Slack API error: {error_msg}")
                
                return data.get('messages', [])
    
    def _format_thread_content(
        self,
        messages: List[Dict[str, Any]],
        channel: str,
        thread_ts: str
    ) -> str:
        """
        Format thread messages for output
        
        Args:
            messages: List of message dictionaries
            channel: Channel ID
            thread_ts: Thread timestamp
            
        Returns:
            Formatted string
        """
        output = [
            "📨 **Slack Thread Content**",
            f"Channel: {channel}",
            f"Thread TS: {thread_ts}",
            f"Total Messages: {len(messages)}",
            "\n" + "="*60 + "\n"
        ]
        
        for idx, msg in enumerate(messages, 1):
            timestamp = msg.get('ts', '')
            user = msg.get('user', 'Unknown')
            text = msg.get('text', '')
            
            # Format timestamp to readable format
            try:
                dt = datetime.fromtimestamp(float(timestamp))
                time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                time_str = timestamp
            
            output.append(f"[{idx}] {time_str} - User: {user}")
            output.append(f"{text}")
            output.append("-" * 60)
        
        return "\n".join(output)
