# Context Intelligence

v0.18.0 introduces **intelligent context gathering** - a pre-processing system that analyzes your codebase before generating code for tickets. This dramatically improves code generation quality by providing the AI with relevant context about your project's structure, conventions, and existing code.

## Overview

When executing a ticket, the system automatically gathers:

### Project Structure
- **Language detection**: Identifies primary programming language
- **Framework detection**: Detects Django, Flask, FastAPI, React, Express, etc.
- **Directory structure**: Maps models/, views/, controllers/, tests/, etc.
- **Configuration files**: Locates config files, .env, docker-compose, etc.

### Dependencies
- **Project dependencies**: Parses requirements.txt, package.json, pyproject.toml, go.mod, etc.
- **Common imports**: Identifies most frequently used libraries/modules

### Code Patterns
- **Similar code**: Finds files with similar purpose based on ticket description
- **Similar functions**: Locates functions with related names
- **Naming conventions**: Detects snake_case, camelCase, PascalCase patterns
- **Related files**: Identifies relevant models, views, controllers, tests

## Usage

### Automatic Context Gathering (Default)

```bash
# Context gathering is enabled by default
cdc ticket execute TASK-123

# Explicitly with notifications and auto-commit
cdc ticket execute TASK-456 --notify --commit
```

### Disable Context Gathering

For faster execution when you don't need context:

```bash
# Skip context gathering
cdc ticket execute TASK-789 --no-context
```

## How It Works

### 1. Pre-Processing Phase

When you execute a ticket, the system:

1. Fetches the ticket from backend (repo-tickets, Jira, etc.)
2. **NEW**: Gathers codebase context by analyzing:
   - File extensions → Language detection
   - Config files → Framework detection
   - Dependency manifests → Dependencies list
   - Source code → Naming conventions & patterns
   - Ticket keywords → Similar existing code
3. Analyzes requirements and acceptance criteria
4. Generates implementation plan **with context**
5. Generates code **following existing patterns**
6. Generates tests
7. Commits changes (if `--commit`)

### 2. Context Integration

The gathered context is integrated into AI prompts:

```
**Implementation Plan:**
[ticket details]

==================================================
# CODEBASE CONTEXT
==================================================

## Project Context
**Language:** Python
**Framework:** FastAPI
**Root:** /path/to/project

## Dependencies (36)
- anthropic (unknown)
- click (unknown)
- rich (unknown)
...

## Project Structure
**tests:** tests/

## Naming Conventions
- functions: snake_case

## Common Imports
anthropic, click, rich, pathlib, typing, ...

==================================================

**IMPORTANT:** Follow the existing codebase patterns and conventions shown above.
```

### 3. Improved Code Generation

The AI uses this context to:

- Use the correct language and framework idioms
- Follow project naming conventions
- Import commonly used libraries
- Structure code similar to existing patterns
- Place files in appropriate directories

## Examples

### Example 1: Django Project

```bash
$ cdc ticket execute FEAT-100
```

**Context gathered:**
- Language: Python
- Framework: Django
- Dependencies: django, djangorestframework, celery, ...
- Structure: models/, views/, serializers/, urls/
- Conventions: snake_case functions, PascalCase classes

**Result:** Generated code follows Django patterns, uses DRF serializers, places files in correct apps/

### Example 2: React/TypeScript Project

```bash
$ cdc ticket execute UI-200
```

**Context gathered:**
- Language: TypeScript
- Framework: React
- Dependencies: react, @types/react, styled-components, ...
- Structure: components/, hooks/, utils/, __tests__/
- Conventions: PascalCase components, camelCase functions

**Result:** Generated code uses React hooks, TypeScript types, styled-components, follows project structure

### Example 3: Fast Execution (No Context)

```bash
$ cdc ticket execute HOTFIX-300 --no-context
```

Skips context gathering for immediate code generation (useful for simple fixes or when you want maximum speed).

## Architecture

### TicketContextGatherer

Main class that orchestrates context gathering:

```python
from claude_dev_cli.project.context_gatherer import TicketContextGatherer

gatherer = TicketContextGatherer(project_root=Path.cwd())
context = gatherer.gather_context(ticket, ai_client=None)
```

### CodeContext

Dataclass containing all gathered context:

```python
@dataclass
class CodeContext:
    # Project structure
    project_root: Path
    language: str
    framework: Optional[str]
    
    # Dependencies
    dependencies: List[str]
    installed_packages: Dict[str, str]
    
    # Similar code
    similar_files: List[Dict[str, Any]]
    similar_functions: List[Dict[str, Any]]
    
    # Conventions
    naming_conventions: Dict[str, str]
    directory_structure: Dict[str, List[str]]
    common_imports: List[str]
    
    # Related files
    related_models: List[str]
    related_views: List[str]
    related_controllers: List[str]
    related_tests: List[str]
    
    # Configuration
    config_files: List[str]
```

### Integration with TicketExecutor

```python
executor = TicketExecutor(
    ticket_backend=backend,
    gather_context=True,  # Enable context gathering
    project_root=Path.cwd()
)

# Context is automatically gathered and used during execution
executor.execute_ticket("TASK-123")
```

## Supported Languages & Frameworks

### Languages
- Python
- JavaScript
- TypeScript
- Go
- Rust
- Java
- Ruby
- PHP
- C#, C++, C

### Frameworks Detected
- **Python**: Django, Flask, FastAPI
- **JavaScript**: React, Vue, Express
- **TypeScript**: Next.js, NestJS
- **Go**: Gin, Echo
- **Ruby**: Rails

### Dependency Files
- Python: requirements.txt, pyproject.toml, setup.py, Pipfile
- JavaScript/TypeScript: package.json
- Go: go.mod
- Ruby: Gemfile
- PHP: composer.json
- Rust: Cargo.toml
- Java: pom.xml, build.gradle

## Performance

Context gathering typically adds **2-5 seconds** to ticket execution time, but results in:

- **Higher quality** code generation
- **Better consistency** with existing codebase
- **Fewer iterations** needed
- **Less manual cleanup** required

Use `--no-context` for time-critical situations.

## Future Enhancements

Planned improvements:

1. **Semantic code search**: Use AI to find semantically similar code (not just keyword matching)
2. **Database schema detection**: Auto-detect and include DB models
3. **API endpoint discovery**: Map existing REST/GraphQL endpoints
4. **Test pattern identification**: Detect and follow test organization patterns
5. **Caching**: Cache context between executions for faster repeated runs
6. **Enhanced package version detection**: Query actual environment for installed versions
7. **Cross-language imports**: Detect FFI patterns in polyglot projects

## See Also

- [README.md](README.md) - Main documentation
- [RENAME.md](RENAME.md) - Project rename plans
- [WARP.md](WARP.md) - WARP integration guide
