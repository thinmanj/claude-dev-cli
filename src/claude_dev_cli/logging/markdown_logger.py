"""Markdown-based progress logger."""

from pathlib import Path
from typing import Optional, List
from datetime import datetime

from claude_dev_cli.logging.logger import ProgressLogger, LogEntry


class MarkdownLogger(ProgressLogger):
    """Markdown file-based progress logger.
    
    Creates a progress.md file to track project execution.
    """
    
    def __init__(self, log_dir: Optional[Path] = None):
        """Initialize markdown logger.
        
        Args:
            log_dir: Directory for log files (default: .cdc-logs)
        """
        self.log_dir = log_dir or Path.cwd() / ".cdc-logs"
        self.log_file = self.log_dir / "progress.md"
        self.entries: List[LogEntry] = []
    
    def init(self, project_name: str) -> bool:
        """Initialize logging directory and file."""
        try:
            self.log_dir.mkdir(exist_ok=True)
            
            # Create initial progress.md with header
            with open(self.log_file, 'w') as f:
                f.write(f"# {project_name} - Progress Log\n\n")
                f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
            
            return True
        except OSError:
            return False
    
    def log(
        self,
        message: str,
        ticket_id: Optional[str] = None,
        level: str = "info",
        **metadata
    ) -> bool:
        """Log an entry to markdown file."""
        try:
            entry = LogEntry(
                timestamp=datetime.now(),
                message=message,
                ticket_id=ticket_id,
                level=level,
                metadata=metadata
            )
            self.entries.append(entry)
            
            # Append to file
            with open(self.log_file, 'a') as f:
                # Format entry
                icon = self._get_level_icon(level)
                timestamp_str = entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                
                f.write(f"## {icon} {timestamp_str}\n\n")
                
                if ticket_id:
                    f.write(f"**Ticket:** {ticket_id}\n\n")
                
                f.write(f"{message}\n\n")
                
                # Add metadata if present
                if metadata:
                    f.write("**Details:**\n")
                    for key, value in metadata.items():
                        f.write(f"- {key}: {value}\n")
                    f.write("\n")
                
                f.write("---\n\n")
            
            return True
        except OSError:
            return False
    
    def link_artifact(self, ticket_id: str, artifact_path: str) -> bool:
        """Link an artifact to a ticket in the log."""
        return self.log(
            f"📎 Generated artifact: `{artifact_path}`",
            ticket_id=ticket_id,
            level="info",
            artifact=artifact_path
        )
    
    def get_report(self) -> str:
        """Generate a summary report."""
        if not self.log_file.exists():
            return "No progress log found."
        
        with open(self.log_file, 'r') as f:
            content = f.read()
        
        # Add summary at top
        total_entries = len(self.entries)
        success_count = sum(1 for e in self.entries if e.level == "success")
        error_count = sum(1 for e in self.entries if e.level == "error")
        
        summary = f"""# Progress Summary

**Total Entries:** {total_entries}
**Successes:** ✅ {success_count}
**Errors:** ❌ {error_count}

---

{content}
"""
        return summary
    
    def _get_level_icon(self, level: str) -> str:
        """Get emoji icon for log level."""
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "error": "❌",
            "warning": "⚠️"
        }
        return icons.get(level, "📝")
    
    def get_logger_name(self) -> str:
        """Return logger name."""
        return "markdown"
