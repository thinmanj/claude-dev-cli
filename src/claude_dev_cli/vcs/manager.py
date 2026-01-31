"""Abstract VCS manager interface."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class CommitInfo:
    """Information about a VCS commit."""
    sha: str
    message: str
    author: str
    files: List[str]


class VCSManager(ABC):
    """Abstract base class for VCS operations."""
    
    @abstractmethod
    def is_repository(self) -> bool:
        """Check if current directory is a VCS repository."""
        pass
    
    @abstractmethod
    def commit(
        self,
        message: str,
        files: Optional[List[str]] = None,
        co_author: Optional[str] = None
    ) -> CommitInfo:
        """Create a commit.
        
        Args:
            message: Commit message
            files: Files to commit (None = all changed files)
            co_author: Co-author attribution (e.g., "Name <email>")
            
        Returns:
            CommitInfo object
        """
        pass
    
    @abstractmethod
    def create_branch(self, branch_name: str, from_branch: Optional[str] = None) -> bool:
        """Create a new branch.
        
        Args:
            branch_name: Name of new branch
            from_branch: Base branch (None = current branch)
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    def checkout(self, branch_name: str) -> bool:
        """Checkout a branch.
        
        Args:
            branch_name: Branch to checkout
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    def current_branch(self) -> str:
        """Get current branch name."""
        pass
    
    @abstractmethod
    def push(self, remote: str = "origin", branch: Optional[str] = None) -> bool:
        """Push changes to remote.
        
        Args:
            remote: Remote name
            branch: Branch to push (None = current branch)
            
        Returns:
            True if successful
        """
        pass
    
    def get_vcs_name(self) -> str:
        """Get VCS system name."""
        return self.__class__.__name__.replace('Manager', '').lower()
