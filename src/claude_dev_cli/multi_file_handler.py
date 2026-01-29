"""Multi-file handler for parsing and applying AI-generated file changes."""

import re
import difflib
from pathlib import Path
from typing import List, Tuple, Optional, Literal
from dataclasses import dataclass
from rich.console import Console
from rich.tree import Tree
from rich.panel import Panel


@dataclass
class FileChange:
    """Represents a single file change."""
    path: str
    content: str
    change_type: Literal["create", "modify", "delete"]
    original_content: Optional[str] = None
    
    @property
    def line_count(self) -> int:
        """Count lines in content."""
        return len(self.content.splitlines()) if self.content else 0
    
    @property
    def diff(self) -> Optional[str]:
        """Generate unified diff for modifications."""
        if self.change_type != "modify" or not self.original_content:
            return None
        
        original_lines = self.original_content.splitlines(keepends=True)
        new_lines = self.content.splitlines(keepends=True)
        
        diff_lines = list(difflib.unified_diff(
            original_lines,
            new_lines,
            fromfile=f"a/{self.path}",
            tofile=f"b/{self.path}",
            lineterm=''
        ))
        
        return ''.join(diff_lines) if diff_lines else None


class MultiFileResponse:
    """Parses and handles multi-file AI responses."""
    
    def __init__(self):
        self.files: List[FileChange] = []
    
    def parse_response(self, text: str, base_path: Optional[Path] = None) -> None:
        """Parse AI response to extract file changes.
        
        Supports formats:
        - ## File: path/to/file.ext
        - ## Create: path/to/file.ext
        - ## Modify: path/to/file.ext  
        - ## Delete: path/to/file.ext
        
        Args:
            text: AI response text
            base_path: Base directory to check for existing files (for modifications)
        """
        self.files = []
        
        # Pattern to match file markers and code blocks
        # Matches: ## File: path or ## Create: path or ## Modify: path or ## Delete: path
        file_pattern = r'^##\s+(File|Create|Modify|Delete):\s*(.+?)$'
        code_block_pattern = r'```(\w+)?\n(.*?)```'
        
        lines = text.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            match = re.match(file_pattern, line, re.IGNORECASE)
            
            if match:
                action = match.group(1).lower()
                file_path = match.group(2).strip()
                
                # Map actions to change types
                if action in ('file', 'create'):
                    change_type = 'create'
                elif action == 'modify':
                    change_type = 'modify'
                elif action == 'delete':
                    change_type = 'delete'
                else:
                    change_type = 'create'
                
                # For delete, no content needed
                if change_type == 'delete':
                    self.files.append(FileChange(
                        path=file_path,
                        content='',
                        change_type='delete'
                    ))
                    i += 1
                    continue
                
                # Extract code block following the file marker
                remaining_text = '\n'.join(lines[i+1:])
                code_match = re.search(code_block_pattern, remaining_text, re.DOTALL)
                
                if code_match:
                    content = code_match.group(2).strip()
                    
                    # Check if file exists for modifications
                    original_content = None
                    if change_type == 'modify' and base_path:
                        file_full_path = base_path / file_path
                        if file_full_path.exists():
                            original_content = file_full_path.read_text()
                            change_type = 'modify'
                        else:
                            # File doesn't exist, treat as create
                            change_type = 'create'
                    
                    self.files.append(FileChange(
                        path=file_path,
                        content=content,
                        change_type=change_type,
                        original_content=original_content
                    ))
                    
                    # Skip past the code block
                    lines_used = code_match.group(0).count('\n')
                    i += lines_used + 1
                else:
                    # No code block found, skip this line
                    i += 1
            else:
                i += 1
    
    def validate_paths(self, base_path: Path) -> List[str]:
        """Validate file paths for security.
        
        Returns list of validation errors, empty if all valid.
        """
        errors = []
        base_path = base_path.resolve()
        
        for file_change in self.files:
            # Check for absolute paths
            if Path(file_change.path).is_absolute():
                errors.append(f"Absolute path not allowed: {file_change.path}")
                continue
            
            # Resolve the path
            try:
                full_path = (base_path / file_change.path).resolve()
                
                # Check if resolved path is within base_path
                if not str(full_path).startswith(str(base_path)):
                    errors.append(f"Path traversal detected: {file_change.path}")
                    
            except Exception as e:
                errors.append(f"Invalid path {file_change.path}: {str(e)}")
        
        return errors
    
    def build_tree(self, base_path: Path) -> str:
        """Generate visual directory tree.
        
        Returns formatted tree string with colors and status indicators.
        """
        if not self.files:
            return "No files"
        
        # Build tree structure
        tree = Tree(f"[bold cyan]{base_path.name or base_path}/[/bold cyan]")
        
        # Group files by directory
        dirs = {}
        for file_change in self.files:
            parts = Path(file_change.path).parts
            current = dirs
            
            for i, part in enumerate(parts[:-1]):
                if part not in current:
                    current[part] = {}
                current = current[part]
            
            # Store file info at leaf
            filename = parts[-1]
            current[filename] = file_change
        
        def add_to_tree(node, items):
            """Recursively add items to tree."""
            for name, value in sorted(items.items()):
                if isinstance(value, dict):
                    # Directory
                    branch = node.add(f"[bold blue]{name}/[/bold blue]")
                    add_to_tree(branch, value)
                elif isinstance(value, FileChange):
                    # File
                    if value.change_type == 'create':
                        status = "[green](new)[/green]"
                    elif value.change_type == 'modify':
                        status = "[yellow](modified)[/yellow]"
                    elif value.change_type == 'delete':
                        status = "[red](deleted)[/red]"
                    else:
                        status = ""
                    
                    lines = f"{value.line_count} lines" if value.line_count > 0 else ""
                    node.add(f"{name} {status} [dim]{lines}[/dim]")
        
        add_to_tree(tree, dirs)
        
        return tree
    
    def preview(self, console: Console, base_path: Path) -> None:
        """Show formatted preview with tree and summary."""
        if not self.files:
            console.print("[yellow]No files to change[/yellow]")
            return
        
        # Show tree
        console.print("\n[bold]File Structure:[/bold]")
        console.print(self.build_tree(base_path))
        
        # Summary
        creates = sum(1 for f in self.files if f.change_type == 'create')
        modifies = sum(1 for f in self.files if f.change_type == 'modify')
        deletes = sum(1 for f in self.files if f.change_type == 'delete')
        total_lines = sum(f.line_count for f in self.files)
        
        summary_parts = []
        if creates:
            summary_parts.append(f"[green]{creates} created[/green]")
        if modifies:
            summary_parts.append(f"[yellow]{modifies} modified[/yellow]")
        if deletes:
            summary_parts.append(f"[red]{deletes} deleted[/red]")
        
        summary = ", ".join(summary_parts)
        console.print(f"\n[bold]Summary:[/bold] {summary} ({total_lines} total lines)\n")
    
    def write_all(self, base_path: Path, dry_run: bool = False, console: Optional[Console] = None) -> None:
        """Write all file changes to disk.
        
        Args:
            base_path: Base directory for file operations
            dry_run: If True, don't actually write files
            console: Rich console for output
        """
        if console is None:
            console = Console()
        
        base_path = base_path.resolve()
        base_path.mkdir(parents=True, exist_ok=True)
        
        for file_change in self.files:
            full_path = base_path / file_change.path
            
            if dry_run:
                if file_change.change_type == 'create':
                    console.print(f"[dim]Would create: {file_change.path}[/dim]")
                elif file_change.change_type == 'modify':
                    console.print(f"[dim]Would modify: {file_change.path}[/dim]")
                elif file_change.change_type == 'delete':
                    console.print(f"[dim]Would delete: {file_change.path}[/dim]")
                continue
            
            # Actual file operations
            if file_change.change_type == 'delete':
                if full_path.exists():
                    full_path.unlink()
                    console.print(f"[red]✗[/red] Deleted: {file_change.path}")
            else:
                # Create parent directories
                full_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Write file
                full_path.write_text(file_change.content)
                
                if file_change.change_type == 'create':
                    console.print(f"[green]✓[/green] Created: {file_change.path}")
                elif file_change.change_type == 'modify':
                    console.print(f"[yellow]✓[/yellow] Modified: {file_change.path}")
    
    def confirm(self, console: Console) -> bool:
        """Interactive confirmation prompt.
        
        Returns True if user confirms, False otherwise.
        """
        if not self.files:
            return False
        
        while True:
            response = console.input("\n[cyan]Continue?[/cyan] [dim](Y/n/preview/help)[/dim] ").strip().lower()
            
            if response in ('y', 'yes', ''):
                return True
            elif response in ('n', 'no'):
                return False
            elif response == 'preview':
                # Show individual file contents
                for i, file_change in enumerate(self.files, 1):
                    console.print(f"\n[bold]File {i}/{len(self.files)}:[/bold] {file_change.path}")
                    
                    if file_change.change_type == 'delete':
                        console.print("[red]This file will be deleted[/red]")
                    elif file_change.change_type == 'modify' and file_change.diff:
                        console.print("[yellow]Diff:[/yellow]")
                        console.print(Panel(file_change.diff, border_style="yellow"))
                    else:
                        preview = file_change.content[:500]
                        if len(file_change.content) > 500:
                            preview += "\n... (truncated)"
                        console.print(Panel(preview, border_style="green"))
            elif response == 'help':
                console.print("""
[bold]Options:[/bold]
  y, yes    - Proceed with changes
  n, no     - Cancel
  preview   - Show file contents/diffs
  help      - Show this help
""")
            else:
                console.print("[red]Invalid response. Type 'help' for options.[/red]")


def extract_code_blocks(text: str) -> List[Tuple[str, str, str]]:
    """Extract code blocks from markdown text.
    
    Returns list of (file_marker, language, code) tuples.
    """
    pattern = r'^##\s+(File|Create|Modify|Delete):\s*(.+?)$.*?```(\w+)?\n(.*?)```'
    matches = re.findall(pattern, text, re.MULTILINE | re.DOTALL)
    
    results = []
    for match in matches:
        action = match[0]
        path = match[1].strip()
        language = match[2] if match[2] else ''
        code = match[3].strip()
        results.append((f"{action}: {path}", language, code))
    
    return results


def count_lines(content: str) -> int:
    """Count non-empty lines in content."""
    return len([line for line in content.splitlines() if line.strip()])
