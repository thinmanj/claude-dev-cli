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

## Deployment & Release Process

### Pre-Release Checklist

1. **Ensure all tests pass**
   ```bash
   pytest --tb=short
   # Should show all tests passing (currently 163 tests)
   ```

2. **Run code quality checks**
   ```bash
   black src/
   ruff check src/
   mypy src/
   ```

3. **Verify CLI works**
   ```bash
   cdc --version
   cdc --help
   cdc ask "test"
   ```

### Version Bump

1. **Update version in two places:**
   
   **pyproject.toml:**
   ```toml
   [project]
   version = "0.X.0"  # Update this
   ```
   
   **src/claude_dev_cli/__init__.py:**
   ```python
   __version__ = "0.X.0"  # Update this
   ```

2. **Update CHANGELOG.md**
   
   Add new version section:
   ```markdown
   ## [Unreleased]
   
   ## [0.X.0] - YYYY-MM-DD
   
   ### Added
   - Feature descriptions
   
   ### Changed
   - Changes to existing features
   
   ### Fixed
   - Bug fixes
   ```

3. **Update ROADMAP.md**
   
   Mark completed features and update status:
   ```markdown
   ## Current: v0.X.0 - Feature Name (✅ COMPLETED)
   ```

### Build & Test Locally

1. **Clean previous builds**
   ```bash
   rm -rf dist/ build/ *.egg-info
   ```

2. **Build distribution packages**
   ```bash
   python3 -m build
   # Creates dist/claude_dev_cli-0.X.0.tar.gz and .whl
   ```

3. **Verify build artifacts**
   ```bash
   ls -lh dist/
   # Should show both .tar.gz and .whl files
   ```

4. **Test installation locally (optional)**
   ```bash
   python3 -m venv test_env
   source test_env/bin/activate
   pip install dist/claude_dev_cli-0.X.0-py3-none-any.whl
   cdc --version
   deactivate
   rm -rf test_env
   ```

### Commit & Tag

1. **Commit all changes**
   ```bash
   git add -A
   git commit -m "feat: release v0.X.0 - Feature Name
   
   Major changes:
   - Feature 1
   - Feature 2
   - Feature 3
   
   Statistics:
   - X tests passing
   - Y new features
   
   Co-Authored-By: Warp <agent@warp.dev>"
   ```

2. **Create git tag**
   ```bash
   git tag -a v0.X.0 -m "Release v0.X.0: Feature Name
   
   Summary of key features and changes.
   
   Full changelog: https://github.com/thinmanj/claude-dev-cli/blob/master/CHANGELOG.md"
   ```

### Publish to PyPI

1. **Ensure twine is installed**
   ```bash
   pip install twine
   ```

2. **Upload to PyPI**
   ```bash
   twine upload dist/claude_dev_cli-0.X.0*
   # Prompts for PyPI username and password/token
   ```

3. **Verify on PyPI**
   - Visit: https://pypi.org/project/claude-dev-cli/
   - Check that new version appears
   - Verify package metadata and description

### Push to GitHub

1. **Push commits**
   ```bash
   git push origin master
   ```

2. **Push tags**
   ```bash
   git push origin v0.X.0
   ```

3. **Verify on GitHub**
   - Check commits: https://github.com/thinmanj/claude-dev-cli/commits/master
   - Check tags: https://github.com/thinmanj/claude-dev-cli/tags
   - Check releases: https://github.com/thinmanj/claude-dev-cli/releases

### Publish to Homebrew (Optional)

1. **Update Homebrew formula**
   ```bash
   # Get new SHA256 from PyPI
   curl -sL https://pypi.org/pypi/claude-dev-cli/json | \
     python3 -c "import sys, json; data = json.load(sys.stdin); \
     [print(f'URL: {f[\"url\"]}\nSHA256: {f[\"digests\"][\"sha256\"]}') \
     for f in data['urls'] if f['packagetype'] == 'sdist']"
   ```

2. **Update formula file**
   ```bash
   # Edit /opt/homebrew/Library/Taps/thinmanj/homebrew-tap/Formula/claude-dev-cli.rb
   # Update url and sha256 fields
   ```

3. **Test and push**
   ```bash
   # Test installation
   brew uninstall claude-dev-cli 2>/dev/null || true
   brew install --build-from-source thinmanj/tap/claude-dev-cli
   cdc --version
   
   # Push to GitHub
   cd /opt/homebrew/Library/Taps/thinmanj/homebrew-tap
   git add Formula/claude-dev-cli.rb
   git commit -m "feat: update claude-dev-cli to v0.X.0
   
   Co-Authored-By: Warp <agent@warp.dev>"
   git push
   ```

   See HOMEBREW.md for detailed instructions and automation script.

### Post-Release

1. **Test installation from PyPI**
   ```bash
   pip install --upgrade claude-dev-cli
   cdc --version  # Should show new version
   ```

2. **Test installation from Homebrew**
   ```bash
   brew upgrade claude-dev-cli
   cdc --version  # Should show new version
   ```

3. **Update documentation**
   - Verify README.md is current on GitHub
   - Check that PyPI description renders correctly

4. **Announce release** (optional)
   - Create GitHub Release with changelog
   - Update project documentation
   - Notify users if breaking changes

### Quick Release Script

For convenience, here's a complete release workflow:

```bash
#!/bin/bash
# Release script for claude-dev-cli

VERSION="0.X.0"  # Update this

# 1. Run tests
echo "Running tests..."
pytest --tb=short || exit 1

# 2. Clean and build
echo "Building packages..."
rm -rf dist/ build/ *.egg-info
python3 -m build || exit 1

# 3. Commit and tag
echo "Committing and tagging..."
git add -A
git commit -m "feat: release v${VERSION}"
git tag -a "v${VERSION}" -m "Release v${VERSION}"

# 4. Publish to PyPI
echo "Publishing to PyPI..."
twine upload "dist/claude_dev_cli-${VERSION}"* || exit 1

# 5. Push to GitHub
echo "Pushing to GitHub..."
git push origin master
git push origin "v${VERSION}"

echo "✓ Release v${VERSION} complete!"
echo "Verify at: https://pypi.org/project/claude-dev-cli/${VERSION}/"
```

### Rollback Procedure

If a release has issues:

1. **Yank from PyPI** (if critical bug)
   ```bash
   # Cannot delete, but can yank (mark as bad)
   # This prevents new installs but doesn't break existing ones
   # Contact PyPI support or use web interface
   ```

2. **Release hotfix version**
   ```bash
   # Increment patch version
   # E.g., if 0.8.0 has issues, release 0.8.1
   ```

3. **Update documentation**
   - Add notice in README about known issues
   - Update CHANGELOG with hotfix details

### Version Numbering Guidelines

- **Major (X.0.0)**: Breaking changes, major rewrites
- **Minor (0.X.0)**: New features, significant additions
- **Patch (0.0.X)**: Bug fixes, minor improvements

Examples:
- New feature (context awareness): 0.8.0
- Bug fix: 0.8.1
- Multiple new features: 0.9.0
- Breaking API change: 1.0.0

### Release History Reference

- **v0.1.0**: Initial release
- **v0.2.0-v0.3.0**: Testing & documentation
- **v0.4.0**: Secure storage
- **v0.5.0**: Shell completion & conversation history
- **v0.6.0**: Custom templates
- **v0.7.0**: Workflows & Warp integration
- **v0.8.0**: Context intelligence
