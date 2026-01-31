"""Abstract ticket backend interface for claude-dev-cli.

Provides pluggable architecture for different ticket management systems.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Ticket:
    """Unified ticket representation across backends."""
    id: str
    title: str
    description: str
    status: str  # open, in-progress, blocked, closed, etc.
    priority: str  # critical, high, medium, low
    ticket_type: str  # feature, bug, refactor, test, doc
    assignee: Optional[str] = None
    labels: List[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Epic/Story hierarchy
    epic_id: Optional[str] = None
    story_id: Optional[str] = None
    parent_id: Optional[str] = None
    
    # Requirements and acceptance criteria
    requirements: List[str] = None
    acceptance_criteria: List[str] = None
    user_stories: List[str] = None
    
    # File context
    files: List[str] = None
    
    # Custom metadata
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.labels is None:
            self.labels = []
        if self.requirements is None:
            self.requirements = []
        if self.acceptance_criteria is None:
            self.acceptance_criteria = []
        if self.user_stories is None:
            self.user_stories = []
        if self.files is None:
            self.files = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class Epic:
    """Unified epic representation."""
    id: str
    title: str
    description: str
    status: str
    priority: str
    owner: Optional[str] = None
    ticket_ids: List[str] = None
    goals: List[str] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.ticket_ids is None:
            self.ticket_ids = []
        if self.goals is None:
            self.goals = []


@dataclass
class Story:
    """Unified user story representation."""
    id: str
    title: str
    description: str
    epic_id: Optional[str] = None
    status: str = "draft"
    priority: str = "medium"
    story_points: Optional[int] = None
    acceptance_criteria: List[str] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.acceptance_criteria is None:
            self.acceptance_criteria = []


class TicketBackend(ABC):
    """Abstract base class for ticket management backends.
    
    Implementations: RepoTicketsBackend, JiraBackend, LinearBackend, GitHubBackend, MarkdownBackend
    """
    
    @abstractmethod
    def connect(self) -> bool:
        """Connect to ticket backend and verify access.
        
        Returns:
            True if connection successful
        """
        pass
    
    @abstractmethod
    def fetch_ticket(self, ticket_id: str) -> Optional[Ticket]:
        """Fetch a ticket by ID.
        
        Args:
            ticket_id: Ticket identifier
            
        Returns:
            Ticket object or None if not found
        """
        pass
    
    @abstractmethod
    def create_epic(self, title: str, description: str = "", **kwargs) -> Epic:
        """Create a new epic.
        
        Args:
            title: Epic title
            description: Epic description
            **kwargs: Additional epic fields (priority, owner, etc.)
            
        Returns:
            Created Epic object
        """
        pass
    
    @abstractmethod
    def create_story(self, epic_id: str, title: str, description: str = "", **kwargs) -> Story:
        """Create a new user story within an epic.
        
        Args:
            epic_id: Parent epic ID
            title: Story title
            description: Story description
            **kwargs: Additional story fields
            
        Returns:
            Created Story object
        """
        pass
    
    @abstractmethod
    def create_task(self, story_id: Optional[str], title: str, description: str = "", **kwargs) -> Ticket:
        """Create a new task/ticket.
        
        Args:
            story_id: Parent story ID (optional)
            title: Task title
            description: Task description
            **kwargs: Additional task fields (priority, assignee, labels, etc.)
            
        Returns:
            Created Ticket object
        """
        pass
    
    @abstractmethod
    def update_ticket(self, ticket_id: str, **kwargs) -> Ticket:
        """Update a ticket's fields.
        
        Args:
            ticket_id: Ticket identifier
            **kwargs: Fields to update (status, description, assignee, etc.)
            
        Returns:
            Updated Ticket object
        """
        pass
    
    @abstractmethod
    def list_tickets(self, status: Optional[str] = None, epic_id: Optional[str] = None, 
                     **filters) -> List[Ticket]:
        """List tickets with optional filters.
        
        Args:
            status: Filter by status
            epic_id: Filter by epic
            **filters: Additional filters
            
        Returns:
            List of matching tickets
        """
        pass
    
    @abstractmethod
    def add_comment(self, ticket_id: str, comment: str, author: str = "") -> bool:
        """Add a comment to a ticket.
        
        Args:
            ticket_id: Ticket identifier
            comment: Comment text
            author: Comment author
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    def attach_file(self, ticket_id: str, file_path: str) -> bool:
        """Attach a file or reference to a ticket.
        
        Args:
            ticket_id: Ticket identifier
            file_path: Path to file
            
        Returns:
            True if successful
        """
        pass
    
    def get_backend_name(self) -> str:
        """Get the name of this backend.
        
        Returns:
            Backend name (e.g., 'repo-tickets', 'jira', 'linear')
        """
        return self.__class__.__name__.replace('Backend', '').lower()
