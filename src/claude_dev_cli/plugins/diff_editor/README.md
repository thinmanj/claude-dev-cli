# Diff Editor Plugin

Interactive diff viewer for reviewing code changes with support for multiple keybinding modes.

## Features

- **Hunk-by-hunk review**: Navigate through changes and accept/reject each one
- **Dual keybinding modes**:
  - **Neovim mode**: Familiar vim-style keybindings (j/k, y/n, etc.)
  - **Fresh mode**: Modern editor keybindings (arrows, Enter, etc.)
  - **Auto mode**: Detects preference from `$EDITOR` or `$VISUAL`
- **Syntax highlighting**: Color-coded diff display using Rich
- **Smart context**: Shows relevant code context for each change

## Usage

### Basic Diff Review

Compare two files interactively:

```bash
# Auto-detect keybindings
cdc diff original.py proposed.py

# Use Neovim keybindings
cdc diff original.py proposed.py --keybindings nvim

# Use Fresh keybindings
cdc diff original.py proposed.py --keybindings fresh

# Save to custom output file
cdc diff original.py proposed.py -o final.py
```

### Keybinding Modes

#### Neovim Mode

| Action | Keys |
|--------|------|
| Accept hunk | `y`, `a` |
| Reject hunk | `n`, `d` |
| Next hunk | `j`, `n` |
| Previous hunk | `k`, `p` |
| Accept all remaining | `A` |
| Reject all remaining | `D` |
| Quit | `q`, `ZZ` |
| Help | `?`, `h` |

#### Fresh Mode

| Action | Keys |
|--------|------|
| Accept hunk | `y`, `Enter` |
| Reject hunk | `n`, `Backspace` |
| Next hunk | `↓`, `j` |
| Previous hunk | `↑`, `k` |
| Accept all remaining | `Ctrl-A` |
| Reject all remaining | `Ctrl-R` |
| Quit | `q`, `Esc` |
| Help | `F1`, `?` |

## Architecture

### Components

- **`viewer.py`**: Main `DiffViewer` class with interactive UI
- **`plugin.py`**: Plugin registration and CLI command integration
- **`__init__.py`**: Package exports

### How It Works

1. **Diff Generation**: Uses Python's `difflib.Differ` to compare files line-by-line
2. **Hunk Creation**: Groups consecutive changes into logical hunks
3. **Interactive Review**: Displays each hunk with original/proposed views
4. **Change Application**: Applies only accepted hunks to produce final output

### Integration with Main CLI

The plugin uses the `register_commands()` hook to add commands to the main CLI:

```python
def register_commands(self, cli: click.Group) -> None:
    @cli.command("diff")
    def diff_command(...): ...
    
    @cli.command("apply-diff")
    def apply_diff_command(...): ...
```

## Future Enhancements

- **Edit mode**: Inline editing of hunks before accepting
- **Split mode**: Split large hunks into smaller pieces
- **Undo support**: Undo accept/reject decisions
- **Side-by-side view**: Full TUI with split panes using `prompt_toolkit`
- **Integration with AI workflows**: Auto-apply Claude suggestions with review
- **Syntax-aware hunks**: Smart hunk boundaries based on code structure
