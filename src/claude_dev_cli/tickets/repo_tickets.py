"""repo-tickets backend implementation for claude-dev-cli.

Integrates with repo-tickets CLI to manage tickets in VCS repositories.
"""

import subprocess
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

from claude_dev_cli.tickets.backend import TicketBackend, Ticket, Epic, Story


class RepoTicketsBackend(TicketBackend):
    """Backend for repo-tickets integration.
    
    Uses subprocess to call 'tickets' CLI commands.
    Assumes repo-tickets is installed and initialized in current repository.
    """
    
    def __init__(self, repo_path: Optional[Path] = None):
        """Initialize repo-tickets backend.
        
        Args:
            repo_path: Path to repository (default: current directory)
        """
        self.repo_path = repo_path or Path.cwd()
        self._tickets_dir = self.repo_path / ".tickets"
    
    def connect(self) -> bool:
        """Verify repo-tickets is initialized and accessible."""
        try:
            # Check if .tickets directory exists
            if not self._tickets_dir.exists():
                return False
            
            # Try to list tickets (will fail if not properly initialized)
            result = subprocess.run(
                ["tickets", "list", "--format", "json"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def fetch_ticket(self, ticket_id: str) -> Optional[Ticket]:
        """Fetch a ticket from repo-tickets."""
        try:
            result = subprocess.run(
                ["tickets", "show", ticket_id, "--format", "json"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return None
            
            data = json.loads(result.stdout)
            return self._convert_to_ticket(data)
        
        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
            return None
    
    def create_epic(self, title: str, description: str = "", **kwargs) -> Epic:
        """Create an epic in repo-tickets."""
        cmd = ["tickets", "epic", "create", title]
        
        if description:
            cmd.extend(["--description", description])
        
        if "priority" in kwargs:
            cmd.extend(["--priority", kwargs["priority"]])
        
        if "owner" in kwargs:
            cmd.extend(["--owner", kwargs["owner"]])
        
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Failed to create epic: {result.stderr}")
        
        # Extract epic ID from output
        epic_id = self._extract_id_from_output(result.stdout)
        
        return Epic(
            id=epic_id,
            title=title,
            description=description,
            status=kwargs.get("status", "draft"),
            priority=kwargs.get("priority", "medium"),
            owner=kwargs.get("owner"),
            created_at=datetime.now()
        )
    
    def create_story(self, epic_id: str, title: str, description: str = "", **kwargs) -> Story:
        """Create a user story within an epic."""
        # repo-tickets uses backlog items for stories
        cmd = ["tickets", "backlog", "add", title]
        
        if description:
            cmd.extend(["--description", description])
        
        if "priority" in kwargs:
            cmd.extend(["--priority", kwargs["priority"]])
        
        if "story_points" in kwargs:
            cmd.extend(["--effort", str(kwargs["story_points"])])
        
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Failed to create story: {result.stderr}")
        
        story_id = self._extract_id_from_output(result.stdout)
        
        # Link story to epic
        subprocess.run(
            ["tickets", "epic", "add-ticket", epic_id, story_id],
            cwd=self.repo_path,
            timeout=10
        )
        
        return Story(
            id=story_id,
            title=title,
            description=description,
            epic_id=epic_id,
            status=kwargs.get("status", "draft"),
            priority=kwargs.get("priority", "medium"),
            story_points=kwargs.get("story_points")
        )
    
    def create_task(self, story_id: Optional[str], title: str, description: str = "", **kwargs) -> Ticket:
        """Create a task ticket."""
        cmd = ["tickets", "create", title]
        
        if description:
            cmd.extend(["--description", description])
        
        if "priority" in kwargs:
            cmd.extend(["--priority", kwargs["priority"]])
        
        if "assignee" in kwargs:
            cmd.extend(["--assignee", kwargs["assignee"]])
        
        if "labels" in kwargs and kwargs["labels"]:
            for label in kwargs["labels"]:
                cmd.extend(["--label", label])
        
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Failed to create task: {result.stderr}")
        
        task_id = self._extract_id_from_output(result.stdout)
        
        # Link to story if provided
        if story_id:
            # In repo-tickets, we add the task to the epic that contains the story
            # This is a simplification - could be enhanced
            pass
        
        return Ticket(
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
    
    def update_ticket(self, ticket_id: str, **kwargs) -> Ticket:
        """Update a ticket's fields."""
        cmd = ["tickets", "update", ticket_id]
        
        if "status" in kwargs:
            cmd.extend(["--status", kwargs["status"]])
        
        if "priority" in kwargs:
            cmd.extend(["--priority", kwargs["priority"]])
        
        if "assignee" in kwargs:
            cmd.extend(["--assignee", kwargs["assignee"]])
        
        if "description" in kwargs:
            cmd.extend(["--description", kwargs["description"]])
        
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Failed to update ticket: {result.stderr}")
        
        # Fetch updated ticket
        updated = self.fetch_ticket(ticket_id)
        if not updated:
            raise RuntimeError(f"Ticket {ticket_id} not found after update")
        
        return updated
    
    def list_tickets(self, status: Optional[str] = None, epic_id: Optional[str] = None,
                     **filters) -> List[Ticket]:
        """List tickets with filters."""
        cmd = ["tickets", "list", "--format", "json"]
        
        if status:
            cmd.extend(["--status", status])
        
        if epic_id:
            cmd.extend(["--epic", epic_id])
        
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode != 0:
            return []
        
        try:
            data = json.loads(result.stdout)
            tickets = []
            
            if isinstance(data, list):
                for item in data:
                    ticket = self._convert_to_ticket(item)
                    if ticket:
                        tickets.append(ticket)
            
            return tickets
        except json.JSONDecodeError:
            return []
    
    def add_comment(self, ticket_id: str, comment: str, author: str = "") -> bool:
        """Add a comment to a ticket."""
        try:
            cmd = ["tickets", "comment", ticket_id, comment]
            
            if author:
                cmd.extend(["--author", author])
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False
    
    def attach_file(self, ticket_id: str, file_path: str) -> bool:
        """Attach a file reference to a ticket.
        
        repo-tickets doesn't support file attachments directly,
        so we add a comment with the file path.
        """
        comment = f"📎 File attached: {file_path}"
        return self.add_comment(ticket_id, comment, "claude-dev-cli")
    
    def _extract_id_from_output(self, output: str) -> str:
        """Extract ticket/epic/story ID from command output.
        
        Looks for patterns like "TICKET-123" or "EPIC-1"
        """
        import re
        
        # Common patterns in repo-tickets
        patterns = [
            r'(TICKET-\d+)',
            r'(EPIC-\d+)',
            r'(BACKLOG-\d+)',
            r'(STORY-\d+)',
            r'(TASK-\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, output)
            if match:
                return match.group(1)
        
        raise ValueError(f"Could not extract ID from output: {output}")
    
    def _convert_to_ticket(self, data: Dict[str, Any]) -> Optional[Ticket]:
        """Convert repo-tickets JSON to unified Ticket object."""
        try:
            return Ticket(
                id=data.get("id", ""),
                title=data.get("title", ""),
                description=data.get("description", ""),
                status=data.get("status", "open"),
                priority=data.get("priority", "medium"),
                ticket_type=data.get("type", "feature"),
                assignee=data.get("assignee"),
                labels=data.get("labels", []),
                epic_id=data.get("epic_id"),
                story_id=data.get("story_id"),
                requirements=data.get("requirements", []),
                acceptance_criteria=data.get("acceptance_criteria", []),
                files=data.get("files", []),
                metadata=data.get("metadata", {}),
                created_at=self._parse_datetime(data.get("created_at")),
                updated_at=self._parse_datetime(data.get("updated_at"))
            )
        except (KeyError, ValueError):
            return None
    
    def _parse_datetime(self, value: Any) -> Optional[datetime]:
        """Parse datetime from various formats."""
        if not value:
            return None
        
        if isinstance(value, datetime):
            return value
        
        try:
            return datetime.fromisoformat(str(value))
        except (ValueError, AttributeError):
            return None
    
    def get_backend_name(self) -> str:
        """Return backend name."""
        return "repo-tickets"
