"""ntfy.sh notification backend.

No signup required - works out of the box with public ntfy.sh server.
Users can self-host if desired.
"""

from typing import Optional
import requests

from claude_dev_cli.notifications.notifier import Notifier, NotificationPriority


class NtfyNotifier(Notifier):
    """ntfy.sh notification backend.
    
    Simple, free, no-signup push notifications via HTTP.
    https://ntfy.sh
    """
    
    def __init__(self, topic: str, server: str = "https://ntfy.sh"):
        """Initialize ntfy notifier.
        
        Args:
            topic: ntfy topic name (choose any unique name)
            server: ntfy server URL (default: public ntfy.sh)
        """
        self.topic = topic
        self.server = server.rstrip('/')
        self.url = f"{self.server}/{topic}"
    
    def send(
        self,
        title: str,
        message: str,
        priority: NotificationPriority = NotificationPriority.NORMAL,
        tags: Optional[list] = None
    ) -> bool:
        """Send notification via ntfy."""
        try:
            headers = {
                "Title": title,
                "Priority": self._map_priority(priority)
            }
            
            if tags:
                # ntfy supports emoji tags
                headers["Tags"] = ",".join(tags)
            
            response = requests.post(
                self.url,
                data=message.encode('utf-8'),
                headers=headers,
                timeout=10
            )
            
            return response.status_code == 200
        
        except (requests.RequestException, Exception):
            return False
    
    def test_connection(self) -> bool:
        """Test ntfy server connectivity."""
        try:
            # Send a test message
            response = requests.post(
                self.url,
                data="Test notification from claude-dev-cli".encode('utf-8'),
                headers={"Title": "Test"},
                timeout=5
            )
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def _map_priority(self, priority: NotificationPriority) -> str:
        """Map NotificationPriority to ntfy priority levels."""
        mapping = {
            NotificationPriority.LOW: "2",
            NotificationPriority.NORMAL: "3",
            NotificationPriority.HIGH: "4",
            NotificationPriority.URGENT: "5"
        }
        return mapping.get(priority, "3")
    
    def get_backend_name(self) -> str:
        """Return backend name."""
        return "ntfy"
