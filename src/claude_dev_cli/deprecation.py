"""Deprecation notices for project rename.

This module handles showing deprecation warnings about the upcoming
rename from claude-dev-cli to devflow.
"""

import os
import sys
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel


# Deprecation message
DEPRECATION_MESSAGE = """[bold yellow]⚠️  DEPRECATION NOTICE[/bold yellow]

[bold]claude-dev-cli is being renamed to devflow![/bold]

Starting with v0.20.0, this project will be available as [cyan]devflow[/cyan].
The [dim]claude-dev-cli[/dim] package will become a compatibility wrapper.

[bold]What this means for you:[/bold]
• The [cyan]cdc[/cyan] command will continue to work
• New command will be [cyan]devflow[/cyan] (or [cyan]df[/cyan] for short)
• All features and functionality remain the same
• Migration is automatic - no action required now

[bold]Why the rename?[/bold]
This tool has evolved beyond Claude AI to support multiple AI providers
(Anthropic, OpenAI, Ollama) and comprehensive project automation.
The new name better reflects these capabilities.

[bold]Timeline:[/bold]
• [yellow]v0.19.x[/yellow] - Current (with deprecation warnings)
• [cyan]v0.20.0[/cyan] - Dual publishing (both names work)
• [green]v1.0.0[/green] - Official rename to devflow

[dim]To suppress this warning, set: CLAUDE_DEV_CLI_NO_DEPRECATION=1[/dim]
[dim]Learn more: https://github.com/thinmanj/claude-dev-cli/blob/master/RENAME.md[/dim]
"""


def should_show_deprecation_warning() -> bool:
    """Check if deprecation warning should be shown.
    
    Returns False if:
    - Environment variable CLAUDE_DEV_CLI_NO_DEPRECATION is set
    - User has acknowledged the warning before
    """
    # Check environment variable
    if os.environ.get("CLAUDE_DEV_CLI_NO_DEPRECATION"):
        return False
    
    # Check if user has acknowledged (by creating a marker file)
    marker_file = Path.home() / ".claude-dev-cli" / ".deprecation-acknowledged"
    if marker_file.exists():
        return False
    
    return True


def show_deprecation_warning(console: Optional[Console] = None) -> None:
    """Show deprecation warning about project rename.
    
    Args:
        console: Rich console to use (creates new one if None)
    """
    if not should_show_deprecation_warning():
        return
    
    if console is None:
        console = Console(stderr=True)
    
    # Show the warning
    console.print()
    console.print(Panel(
        DEPRECATION_MESSAGE,
        title="[bold red]Important Notice[/bold red]",
        border_style="yellow",
        padding=(1, 2)
    ))
    console.print()
    
    # Offer to suppress future warnings
    try:
        # Only in interactive mode
        if sys.stdin.isatty():
            response = input("Acknowledge and hide this warning? [y/N]: ").strip().lower()
            if response in ('y', 'yes'):
                marker_file = Path.home() / ".claude-dev-cli" / ".deprecation-acknowledged"
                marker_file.parent.mkdir(parents=True, exist_ok=True)
                marker_file.touch()
                console.print("[dim]✓ Warning acknowledged. It won't be shown again.[/dim]\n")
    except (EOFError, KeyboardInterrupt):
        console.print()


def show_inline_deprecation_notice(console: Optional[Console] = None) -> None:
    """Show a brief inline deprecation notice (for command output).
    
    Args:
        console: Rich console to use (creates new one if None)
    """
    if not should_show_deprecation_warning():
        return
    
    if console is None:
        console = Console(stderr=True)
    
    console.print(
        "[yellow]⚠[/yellow]  [dim]Note: claude-dev-cli is being renamed to "
        "[cyan]devflow[/cyan] in v0.20.0. Run 'cdc --version' for details.[/dim]"
    )
