"""Project management and automation for claude-dev-cli.

Note: This project will be renamed in the future to reflect its broader
automation capabilities beyond Claude AI integration.
"""

from claude_dev_cli.project.executor import TicketExecutor
from claude_dev_cli.project.bug_tracker import BugTriageSystem, BugReport, BugSeverity, BugCategory

__all__ = ["TicketExecutor", "BugTriageSystem", "BugReport", "BugSeverity", "BugCategory"]
