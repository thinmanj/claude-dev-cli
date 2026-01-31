"""Markdown-based fallback ticket backend.

Simple file-based ticket system when external backends aren't available.
"""

import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

from claude_dev_cli.tickets.backend import TicketBackend, Ticket, Epic, Story


class MarkdownBackend(TicketBackend):
    """Simple markdown-based ticket system.
    
    Stores tickets as JSON files in .cdc-tickets/ directory.
    Provides fallback when repo-tickets or other systems aren't available.
    """
    
    def __init__(self, base_dir: Optional[Path] = None):
        """Initialize markdown backend.
        
        Args:
            base_dir: Base directory for tickets (default: current directory)
        """
        self.base_dir = base_dir or Path.cwd()
        self.tickets_dir = self.base_dir / ".cdc-tickets"
        self.epics_dir = self.tickets_dir / "epics"
        self.stories_dir = self.tickets_dir / "stories"
        self.tasks_dir = self.tickets_dir / "tasks"
    
    def connect(self) -> bool:
        """Initialize ticket directories if needed."""
        try:
            self.tickets_dir.mkdir(exist_ok=True)
            self.epics_dir.mkdir(exist_ok=True)
            self.stories_dir.mkdir(exist_ok=True)
            self.tasks_dir.mkdir(exist_ok=True)
            return True
        except OSError:
            return False
    
    def fetch_ticket(self, ticket_id: str) -> Optional[Ticket]:
        """Fetch ticket from JSON file."""
        ticket_file = self.tasks_dir / f"{ticket_id}.json"
        
        if not ticket_file.exists():
            return None
        
        try:
            with open(ticket_file, 'r') as f:
                data = json.load(f)
            
            return self._dict_to_ticket(data)
        except (json.JSONDecodeError, OSError):
            return None
    
    def create_epic(self, title: str, description: str = "", **kwargs) -> Epic:
        """Create epic as JSON file."""
        epic_id = f"EPIC-{self._generate_id()}"
        
        epic = Epic(
            id=epic_id,
            title=title,
            description=description,
            status=kwargs.get("status", "draft"),
            priority=kwargs.get("priority", "medium"),
            owner=kwargs.get("owner"),
            created_at=datetime.now()
        )
        
        # Save to file
        epic_file = self.epics_dir / f"{epic_id}.json"
        with open(epic_file, 'w') as f:
            json.dump(self._epic_to_dict(epic), f, indent=2, default=str)
        
        return epic
    
    def create_story(self, epic_id: str, title: str, description: str = "", **kwargs) -> Story:
        """Create story as JSON file."""
        story_id = f"STORY-{self._generate_id()}"
        
        story = Story(
            id=story_id,
            title=title,
            description=description,
            epic_id=epic_id,
            status=kwargs.get("status", "draft"),
            priority=kwargs.get("priority", "medium"),
            story_points=kwargs.get("story_points")
        )
        
        # Save to file
        story_file = self.stories_dir / f"{story_id}.json"
        with open(story_file, 'w') as f:
            json.dump(self._story_to_dict(story), f, indent=2, default=str)
        
        # Link to epic
        epic_file = self.epics_dir / f"{epic_id}.json"
        if epic_file.exists():
            with open(epic_file, 'r') as f:
                epic_data = json.load(f)
            
            if story_id not in epic_data.get('ticket_ids', []):
                epic_data.setdefault('ticket_ids', []).append(story_id)
                
                with open(epic_file, 'w') as f:
                    json.dump(epic_data, f, indent=2, default=str)
        
        return story
    
    def create_task(self, story_id: Optional[str], title: str, description: str = "", **kwargs) -> Ticket:
        """Create task as JSON file."""
        task_id = f"TASK-{self._generate_id()}"
        
        ticket = Ticket(
            id=task_id,
            title=title,
            description=description,
            status=kwargs.get("status", "open"),
            priority=kwargs.get("priority", "medium"),
            ticket_type=kwargs.get("ticket_type", "feature"),
            assignee=kwargs.get("assignee"),
            labels=kwargs.get("labels", []),
            story_id=story_id,
            created_at=datetime.now()
        )
        
        # Save to file
        task_file = self.tasks_dir / f"{task_id}.json"
        with open(task_file, 'w') as f:
            json.dump(self._ticket_to_dict(ticket), f, indent=2, default=str)
        
        return ticket
    
    def update_ticket(self, ticket_id: str, **kwargs) -> Ticket:
        """Update ticket fields."""
        ticket = self.fetch_ticket(ticket_id)
        if not ticket:
            raise ValueError(f"Ticket {ticket_id} not found")
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(ticket, key):
                setattr(ticket, key, value)
        
        ticket.updated_at = datetime.now()
        
        # Save updated ticket
        task_file = self.tasks_dir / f"{ticket_id}.json"
        with open(task_file, 'w') as f:
            json.dump(self._ticket_to_dict(ticket), f, indent=2, default=str)
        
        return ticket
    
    def list_tickets(self, status: Optional[str] = None, epic_id: Optional[str] = None,
                     **filters) -> List[Ticket]:
        """List all tickets with filters."""
        tickets = []
        
        for ticket_file in self.tasks_dir.glob("*.json"):
            try:
                with open(ticket_file, 'r') as f:
                    data = json.load(f)
                
                ticket = self._dict_to_ticket(data)
                if not ticket:
                    continue
                
                # Apply filters
                if status and ticket.status != status:
                    continue
                
                if epic_id and ticket.epic_id != epic_id:
                    continue
                
                tickets.append(ticket)
            
            except (json.JSONDecodeError, OSError):
                continue
        
        return tickets
    
    def add_comment(self, ticket_id: str, comment: str, author: str = "") -> bool:
        """Add comment to ticket metadata."""
        ticket = self.fetch_ticket(ticket_id)
        if not ticket:
            return False
        
        if not ticket.metadata:
            ticket.metadata = {}
        
        if 'comments' not in ticket.metadata:
            ticket.metadata['comments'] = []
        
        ticket.metadata['comments'].append({
            'author': author or 'unknown',
            'text': comment,
            'timestamp': datetime.now().isoformat()
        })
        
        # Save updated ticket
        task_file = self.tasks_dir / f"{ticket_id}.json"
        with open(task_file, 'w') as f:
            json.dump(self._ticket_to_dict(ticket), f, indent=2, default=str)
        
        return True
    
    def attach_file(self, ticket_id: str, file_path: str) -> bool:
        """Attach file reference to ticket."""
        ticket = self.fetch_ticket(ticket_id)
        if not ticket:
            return False
        
        if file_path not in ticket.files:
            ticket.files.append(file_path)
        
        # Save updated ticket
        task_file = self.tasks_dir / f"{ticket_id}.json"
        with open(task_file, 'w') as f:
            json.dump(self._ticket_to_dict(ticket), f, indent=2, default=str)
        
        return True
    
    def _generate_id(self) -> str:
        """Generate unique ID."""
        return str(uuid.uuid4())[:8].upper()
    
    def _ticket_to_dict(self, ticket: Ticket) -> Dict[str, Any]:
        """Convert Ticket to dict for JSON serialization."""
        return {
            'id': ticket.id,
            'title': ticket.title,
            'description': ticket.description,
            'status': ticket.status,
            'priority': ticket.priority,
            'ticket_type': ticket.ticket_type,
            'assignee': ticket.assignee,
            'labels': ticket.labels,
            'epic_id': ticket.epic_id,
            'story_id': ticket.story_id,
            'parent_id': ticket.parent_id,
            'requirements': ticket.requirements,
            'acceptance_criteria': ticket.acceptance_criteria,
            'user_stories': ticket.user_stories,
            'files': ticket.files,
            'metadata': ticket.metadata,
            'created_at': ticket.created_at.isoformat() if ticket.created_at else None,
            'updated_at': ticket.updated_at.isoformat() if ticket.updated_at else None
        }
    
    def _dict_to_ticket(self, data: Dict[str, Any]) -> Optional[Ticket]:
        """Convert dict to Ticket object."""
        try:
            return Ticket(
                id=data['id'],
                title=data['title'],
                description=data.get('description', ''),
                status=data.get('status', 'open'),
                priority=data.get('priority', 'medium'),
                ticket_type=data.get('ticket_type', 'feature'),
                assignee=data.get('assignee'),
                labels=data.get('labels', []),
                epic_id=data.get('epic_id'),
                story_id=data.get('story_id'),
                parent_id=data.get('parent_id'),
                requirements=data.get('requirements', []),
                acceptance_criteria=data.get('acceptance_criteria', []),
                user_stories=data.get('user_stories', []),
                files=data.get('files', []),
                metadata=data.get('metadata', {}),
                created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
                updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
            )
        except (KeyError, ValueError):
            return None
    
    def _epic_to_dict(self, epic: Epic) -> Dict[str, Any]:
        """Convert Epic to dict."""
        return {
            'id': epic.id,
            'title': epic.title,
            'description': epic.description,
            'status': epic.status,
            'priority': epic.priority,
            'owner': epic.owner,
            'ticket_ids': epic.ticket_ids,
            'goals': epic.goals,
            'created_at': epic.created_at.isoformat() if epic.created_at else None
        }
    
    def _story_to_dict(self, story: Story) -> Dict[str, Any]:
        """Convert Story to dict."""
        return {
            'id': story.id,
            'title': story.title,
            'description': story.description,
            'epic_id': story.epic_id,
            'status': story.status,
            'priority': story.priority,
            'story_points': story.story_points,
            'acceptance_criteria': story.acceptance_criteria
        }
    
    def get_backend_name(self) -> str:
        """Return backend name."""
        return "markdown"
