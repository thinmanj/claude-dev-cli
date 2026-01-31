"""Git VCS manager implementation."""

import subprocess
from pathlib import Path
from typing import Optional, List

from claude_dev_cli.vcs.manager import VCSManager, CommitInfo


class GitManager(VCSManager):
    """Git version control manager.
    
    Supports conventional commits and co-author attribution.
    """
    
    def __init__(self, repo_path: Optional[Path] = None):
        """Initialize Git manager.
        
        Args:
            repo_path: Path to repository (default: current directory)
        """
        self.repo_path = repo_path or Path.cwd()
    
    def is_repository(self) -> bool:
        """Check if current directory is a Git repository."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_path,
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def commit(
        self,
        message: str,
        files: Optional[List[str]] = None,
        co_author: Optional[str] = None
    ) -> CommitInfo:
        """Create a Git commit with optional co-author."""
        # Add files
        if files:
            for file_path in files:
                subprocess.run(
                    ["git", "add", file_path],
                    cwd=self.repo_path,
                    timeout=10
                )
        else:
            # Add all changes
            subprocess.run(
                ["git", "add", "-A"],
                cwd=self.repo_path,
                timeout=10
            )
        
        # Build commit message with co-author
        full_message = message
        if co_author:
            full_message = f"{message}\n\nCo-Authored-By: {co_author}"
        
        # Create commit
        result = subprocess.run(
            ["git", "commit", "-m", full_message],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Commit failed: {result.stderr}")
        
        # Get commit SHA
        sha_result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            timeout=5
        )
        sha = sha_result.stdout.strip()
        
        # Get author
        author_result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%an <%ae>"],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            timeout=5
        )
        author = author_result.stdout.strip()
        
        return CommitInfo(
            sha=sha,
            message=message,
            author=author,
            files=files or []
        )
    
    def create_branch(self, branch_name: str, from_branch: Optional[str] = None) -> bool:
        """Create a new Git branch."""
        try:
            cmd = ["git", "checkout", "-b", branch_name]
            
            if from_branch:
                cmd.append(from_branch)
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                timeout=10
            )
            
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False
    
    def checkout(self, branch_name: str) -> bool:
        """Checkout a Git branch."""
        try:
            result = subprocess.run(
                ["git", "checkout", branch_name],
                cwd=self.repo_path,
                capture_output=True,
                timeout=10
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False
    
    def current_branch(self) -> str:
        """Get current Git branch name."""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            
            return "unknown"
        except subprocess.TimeoutExpired:
            return "unknown"
    
    def push(self, remote: str = "origin", branch: Optional[str] = None) -> bool:
        """Push changes to remote."""
        try:
            branch_name = branch or self.current_branch()
            
            result = subprocess.run(
                ["git", "push", remote, branch_name],
                cwd=self.repo_path,
                capture_output=True,
                timeout=30
            )
            
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False
    
    def get_vcs_name(self) -> str:
        """Return VCS name."""
        return "git"
