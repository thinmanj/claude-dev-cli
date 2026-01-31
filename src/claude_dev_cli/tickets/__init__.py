"""Ticket management backend abstraction for claude-dev-cli."""

from claude_dev_cli.tickets.backend import TicketBackend
from claude_dev_cli.tickets.repo_tickets import RepoTicketsBackend
from claude_dev_cli.tickets.markdown import MarkdownBackend

__all__ = ["TicketBackend", "RepoTicketsBackend", "MarkdownBackend"]
