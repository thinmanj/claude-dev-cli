# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Claude Dev CLI is a Python-based command-line tool that provides AI-powered development assistance using Claude API. It supports multi-API key routing (personal vs client keys), usage tracking, test generation, code review, debugging, and optional TOON format for token reduction.

## Development Commands

### Installation & Setup
```bash
# Install in development mode with all dependencies
pip install -e ".[dev]"

# Install with optional TOON support
pip install -e ".[toon]"
```

### Testing
```bash
# Run tests (when test suite exists)
pytest

# Run specific test file
pytest tests/test_<module>.py
```

### Code Quality
```bash
# Format code
black src/

# Lint code
ruff check src/

# Type checking
mypy src/
```

### Building & Distribution
```bash
# Build distribution packages
python -m build

# Check dist directory for built packages
ls -l dist/
```

### Running the CLI during development
```bash
# Use the cdc command after installing in dev mode
cdc --help

# Or run directly via Python module
python -m claude_dev_cli.cli --help
```

## Architecture

### Core Components

**config.py** (`Config`, `APIConfig`, `ProjectProfile`)
- Manages global configuration in `~/.claude-dev-cli/config.json`
- Handles multiple API keys with routing logic (personal vs client)
- Supports project-specific config via `.claude-dev-cli` files in project roots
- Project profiles automatically select which API key to use based on current directory

**core.py** (`ClaudeClient`)
- Main Claude API client wrapper using the Anthropic SDK
- Handles both streaming and non-streaming responses
- Automatic usage logging to `~/.claude-dev-cli/usage.jsonl`
- API config resolution: checks for project profile → named config → default config

**cli.py** (Click-based CLI)
- Entry point with command groups: `ask`, `interactive`, `config`, `generate`, `review`, `debug`, `refactor`, `git`, `usage`, `toon`
- Uses Rich library for terminal formatting (tables, panels, markdown rendering)
- Supports piping input from stdin for `ask` and `debug` commands

**commands.py**
- Developer workflow commands: `generate_tests`, `code_review`, `debug_code`, `generate_docs`, `refactor_code`, `git_commit_message`
- Each command loads file content and formats prompts from templates
- Git integration uses subprocess to run `git --no-pager diff --cached`

**usage.py** (`UsageTracker`)
- Parses usage logs (JSONL format)
- Calculates costs based on MODEL_PRICING dictionary
- Aggregates statistics by API config, model, and date
- Displays usage with Rich tables

**templates.py**
- Contains prompt templates for various developer commands
- Templates use Python string formatting with placeholders

**toon_utils.py**
- Optional integration with TOON format (Token-Oriented Object Notation)
- Provides 30-60% token reduction for large data files
- Graceful fallback if toon-format package not installed

### Key Design Patterns

**API Routing Hierarchy**
1. Explicit `--api` flag in CLI command
2. Project-specific `.claude-dev-cli` file in current/parent directories  
3. Default API config marked in global configuration
4. First configured API if no default set

**Project Profile Resolution**
- Searches from current directory upward for `.claude-dev-cli` file
- Allows per-project API selection (e.g., use client API in client projects)
- Can override system prompts per project

**Usage Logging**
- Every API call logs to append-only JSONL file
- Captures: timestamp, api_config, model, tokens, duration, prompt preview
- Enables cost tracking and API usage attribution

### Configuration Files

**Global: `~/.claude-dev-cli/config.json`**
```json
{
  "api_configs": [
    {"name": "personal", "api_key": "sk-ant-...", "default": true},
    {"name": "client", "api_key": "sk-ant-...", "default": false}
  ],
  "default_model": "claude-3-5-sonnet-20241022",
  "max_tokens": 4096
}
```

**Project-specific: `.claude-dev-cli`**
```json
{
  "name": "Project Name",
  "api_config": "client",
  "system_prompt": "Optional custom system prompt",
  "allowed_commands": ["all"]
}
```

## Important Notes

- Use f-strings for string formatting (per user preference)
- Always use `--no-pager` flag with git commands in subprocess calls
- API keys can be provided via environment variables: `{NAME}_ANTHROPIC_API_KEY`
- The tool creates `~/.claude-dev-cli/` directory on first run
- Code follows type hints with mypy strict mode (`disallow_untyped_defs = true`)
- Line length set to 100 characters (black and ruff)
- Minimum Python version: 3.9

## Common Development Patterns

When extending the CLI:
1. Add new commands to `cli.py` using Click decorators
2. Implement core logic in `commands.py` if it's a developer workflow
3. Add prompt templates to `templates.py` for AI interactions
4. Update `ClaudeClient` in `core.py` only for API-level changes
5. New commands should support `-a/--api` flag for API routing

When modifying configuration:
- Always update both `Config` class methods and serialization logic
- Use Pydantic models for validation (`APIConfig`, `ProjectProfile`)
- Remember to call `_save_config()` after modifications
