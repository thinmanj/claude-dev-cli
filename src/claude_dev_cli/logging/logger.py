"""Abstract progress logger interface."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass


@dataclass
class LogEntry:
    """A log entry for progress tracking."""
    timestamp: datetime
    message: str
    ticket_id: Optional[str] = None
    level: str = "info"  # info, success, error, warning
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize metadata."""
        if self.metadata is None:
            self.metadata = {}


class ProgressLogger(ABC):
    """Abstract base class for progress logging."""
    
    @abstractmethod
    def init(self, project_name: str) -> bool:
        """Initialize logging for a project.
        
        Args:
            project_name: Name of the project
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    def log(
        self,
        message: str,
        ticket_id: Optional[str] = None,
        level: str = "info",
        **metadata
    ) -> bool:
        """Log a progress entry.
        
        Args:
            message: Log message
            ticket_id: Related ticket ID
            level: Log level (info, success, error, warning)
            **metadata: Additional metadata
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    def link_artifact(self, ticket_id: str, artifact_path: str) -> bool:
        """Link an artifact (file, code, etc.) to a ticket.
        
        Args:
            ticket_id: Ticket identifier
            artifact_path: Path to artifact
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    def get_report(self) -> str:
        """Generate a progress report.
        
        Returns:
            Formatted progress report
        """
        pass
    
    def get_logger_name(self) -> str:
        """Get logger backend name."""
        return self.__class__.__name__.replace('Logger', '').lower()
