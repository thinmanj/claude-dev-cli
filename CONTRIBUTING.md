# Contributing to Claude Dev CLI

Thank you for your interest in contributing to Claude Dev CLI! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- git

### Setting Up Your Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/thinmanj/claude-dev-cli
   cd claude-dev-cli
   ```

2. **Install in development mode**
   ```bash
   # Install base package in editable mode
   pip install -e .
   
   # Install with development dependencies
   pip install -e ".[dev]"
   
   # Optional: Install with TOON support
   pip install -e ".[toon]"
   ```

3. **Verify installation**
   ```bash
   cdc --version
   ```

## Running Tests

The project has 257 tests covering all functionality including conversation history, summarization, context intelligence, and core features.

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_config.py
```

### Run Tests with Coverage
```bash
pytest --cov=claude_dev_cli --cov-report=html
```

### Run Tests in Verbose Mode
```bash
pytest -v
```

## Code Quality

This project uses several tools to maintain code quality:

### Code Formatting with Black
```bash
# Format all code
black src/

# Check formatting without making changes
black src/ --check
```

### Linting with Ruff
```bash
# Check for linting issues
ruff check src/

# Auto-fix issues where possible
ruff check src/ --fix
```

### Type Checking with MyPy
```bash
# Run type checking
mypy src/
```

### Run All Quality Checks
```bash
# Format, lint, and type check
black src/ && ruff check src/ && mypy src/
```

## Code Style Guidelines

### General Principles
- Use type hints for all function parameters and return values
- Write docstrings for all public functions, classes, and modules
- Keep functions focused and single-purpose
- Follow PEP 8 guidelines (enforced by Black and Ruff)

### Specific Rules
- **Line length**: 100 characters (configured in pyproject.toml)
- **String formatting**: Use f-strings
- **Imports**: Organize imports with standard library first, then third-party, then local
- **Type hints**: Always use type hints (`disallow_untyped_defs = true` in mypy)

### Example Function
```python
def add_api_config(
    self,
    name: str,
    api_key: Optional[str] = None,
    description: Optional[str] = None,
    make_default: bool = False
) -> None:
    """Add a new API configuration.
    
    Args:
        name: Name of the API configuration
        api_key: API key (or set via environment variable)
        description: Optional description of the API
        make_default: Whether to set as default configuration
        
    Raises:
        ValueError: If API key not provided and not in environment
    """
    # Implementation...
```

## Making Changes

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes
- Write or update code
- Add or update tests
- Update documentation if needed
- Follow the code style guidelines

### 3. Test Your Changes
```bash
# Run tests
pytest

# Check code quality
black src/ --check
ruff check src/
mypy src/
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "feat: add new feature"
```

#### Commit Message Format
Use conventional commits format:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
- `feat: add shell completion support`
- `fix: handle missing config file gracefully`
- `docs: update CONTRIBUTING.md with testing guide`

Include co-author attribution:
```
feat: add new feature

Co-Authored-By: Warp <agent@warp.dev>
```

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Pull Request Guidelines

### Before Submitting
- [ ] All tests pass
- [ ] Code follows style guidelines (black, ruff, mypy pass)
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (for significant changes)

### PR Description Should Include
- Summary of changes
- Motivation and context
- Related issues (if any)
- Screenshots (if applicable)
- Testing notes

### Review Process
1. Automated checks must pass (tests, linting, type checking)
2. At least one maintainer review required
3. Address any feedback
4. Maintainer will merge once approved

## Adding New Features

### 1. Developer Commands
To add a new developer command (like `cdc generate tests`):

1. Add function to `commands.py`:
   ```python
   def new_command(file_path: str, api_config_name: Optional[str] = None) -> str:
       """New command description."""
       with open(file_path, 'r') as f:
           code = f.read()
       
       prompt = NEW_COMMAND_PROMPT.format(code=code)
       client = ClaudeClient(api_config_name=api_config_name)
       return client.call(prompt, system_prompt="Expert system prompt")
   ```

2. Add prompt template to `templates.py`:
   ```python
   NEW_COMMAND_PROMPT = """Your prompt template here..."""
   ```

3. Add CLI command to `cli.py`:
   ```python
   @main.command()
   @click.argument('file_path')
   @click.option('-a', '--api', help='API config to use')
   def new_cmd(file_path: str, api: Optional[str]) -> None:
       """New command help text."""
       result = new_command(file_path, api_config_name=api)
       console.print(result)
   ```

4. Add tests to `tests/test_commands.py` and `tests/test_cli.py`

### 2. Configuration Options
To add new configuration options:

1. Update models in `config.py`
2. Update default config in `_load_config()`
3. Add getters/setters as needed
4. Update tests in `tests/test_config.py`
5. Document in README.md

## Issue Reporting

### Bug Reports
Include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/stack traces
- Relevant configuration (sanitized)

### Feature Requests
Include:
- Use case description
- Proposed solution
- Alternatives considered
- Additional context

## Questions?

- Open an issue for questions
- Check existing issues and PRs
- Review documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
