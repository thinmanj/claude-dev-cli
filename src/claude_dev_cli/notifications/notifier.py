"""Abstract notification interface for claude-dev-cli."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class NotificationPriority(Enum):
    """Notification priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class NotificationConfig:
    """Configuration for notification backend."""
    backend: str  # ntfy, telegram, discord, slack, email
    enabled: bool = True
    settings: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize settings."""
        if self.settings is None:
            self.settings = {}


class Notifier(ABC):
    """Abstract base class for notification backends."""
    
    @abstractmethod
    def send(
        self,
        title: str,
        message: str,
        priority: NotificationPriority = NotificationPriority.NORMAL,
        tags: Optional[list] = None
    ) -> bool:
        """Send a notification.
        
        Args:
            title: Notification title
            message: Notification message
            priority: Priority level
            tags: Optional tags/labels
            
        Returns:
            True if sent successfully
        """
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """Test if notification backend is properly configured.
        
        Returns:
            True if backend is accessible
        """
        pass
    
    def get_backend_name(self) -> str:
        """Get the name of this notification backend.
        
        Returns:
            Backend name
        """
        return self.__class__.__name__.replace('Notifier', '').lower()
