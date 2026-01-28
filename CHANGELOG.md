# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.8.6] - 2026-01-28

### Fixed
- Fixed dependency resolution issue causing pip/pipx to install old version (0.1.0)
- Changed toon-format requirement from `>=0.9.0` to `>=0.1.0` (0.9.0 stable not available on PyPI)
- This was causing pip dependency resolver to backtrack to oldest compatible version

## [0.8.5] - 2026-01-28

### Fixed
- Comprehensive file/directory conflict validation across all config paths
- Fixed potential "Is a directory" errors for `usage.jsonl`, `.keyfile`, and `keys.enc`
- Added validation for history directory path conflicts
- Improved error messages with specific paths and clear resolution steps

### Added
- Additional validation in `SecureStorage` for encrypted file paths
- Directory validation in `ConversationHistory` initialization
- Test for usage.jsonl directory conflict (1 new test)
- Total: 260 tests (was 259)

## [0.8.4] - 2026-01-28

### Fixed
- Improved config file/directory error handling with clear error messages
- Fixed potential "Is a directory" error (Errno 21) when config path conflicts exist
- Added validation to detect if config files are accidentally created as directories

### Added
- Tests for config directory/file conflict scenarios (2 new tests)
- Total: 259 tests (was 257)

## [0.8.3] - 2025-01-09

### Added
- **Conversation Summarization**: Reduce token usage and costs in long conversations
  - `cdc history summarize <conversation_id>`: Manually summarize any conversation
  - `cdc history summarize --latest`: Summarize the most recent conversation
  - Automatic summarization in interactive mode when conversations exceed token threshold
  - Smart compression: keeps recent messages, summarizes older ones
  - Token and message count tracking with savings display
  - Configurable via `summarization` section in config.json
- **Summarization Configuration**: Fine-tune summarization behavior
  - `auto_summarize`: Enable/disable automatic summarization (default: true)
  - `threshold_tokens`: Token count threshold for auto-summarization (default: 8000)
  - `keep_recent_messages`: Number of recent message pairs to keep (default: 4)
  - `summary_max_words`: Maximum words in generated summary (default: 300)
- **History Management**: New delete command
  - `cdc history delete <conversation_id>`: Remove conversations you no longer need

### Enhanced
- `Conversation` class now tracks summaries and estimates token counts
- Interactive mode shows token savings when auto-summarization occurs
- Conversation summaries include context from previous summaries (rolling summaries)
- History export and listing show token estimates

### Changed
- Conversations can now have both a summary and recent messages
- `should_summarize()` method checks both token threshold and minimum message count
- Auto-save in interactive mode triggers after summarization
- Conversation IDs now include microseconds to prevent collisions

### Testing
- Added 39 new tests for conversation summarization
- Total: 257 tests (was 218)
- Test coverage for Message, Conversation, ConversationHistory classes
- Mock-based tests for API summarization calls
- Persistence and data integrity tests

## [0.8.2] - 2025-01-09

### Added
- **Multi-Language Error Parsing**: Debug command now supports 5 programming languages
  - JavaScript/TypeScript: Parse stack traces with `at func (file.js:line:col)` format
  - Go: Parse panic traces with goroutine information
  - Rust: Parse panic messages with precise file locations
  - Java: Parse exception stack traces with full class paths
  - Automatic language detection from error format
- **Context Summary Command**: Preview context before API calls
  - `cdc context summary <file>`: Show what context would be gathered
  - Rich table display with Type, Content, Size, Lines, Truncated columns
  - Estimated token count calculation (~chars / 4)
  - Total statistics across all context items
  - Truncation warnings when size limits are hit
  - Toggle options: `--include-git`, `--include-deps`, `--include-tests`
- **Enhanced Error Context**:
  - `detect_language()`: Auto-identify error language
  - Language-specific parsers for each supported language
  - Column numbers for JS, TypeScript, Rust errors
  - Improved error formatting with language identification

### Enhanced
- `format_for_ai()` now includes language identification in output
- Error parsing preserves original error text as fallback
- Frame structure adapted per language (column for JS/Rust, class for Java)
- Backward compatible with existing Python error parsing

### Testing
- Added 11 new tests for multi-language error parsing
- Language detection tests for all 5 languages  
- Parser validation with realistic error examples
- Auto-detection and formatting tests
- Total: 218 tests (was 207)

## [0.8.1] - 2024-12-29

### Added
- **Extended Context Support**: `--auto-context` flag now available on more commands
  - `cdc git commit --auto-context`: Include git history and branch context for better commit messages
  - `cdc generate tests --auto-context`: Include dependencies and related files for comprehensive tests
  - `cdc generate docs --auto-context`: Include dependencies and related files for better documentation
- **Smart Truncation System**: Prevent token limit issues with large files
  - `ContextItem.truncate()` method with configurable max_lines
  - Automatic truncation indicators showing "... (truncated X lines)"
  - Truncation metadata tracking for transparency
- **Global Context Configuration**: New `context` section in `~/.claude-dev-cli/config.json`
  - `auto_context_default`: Default for --auto-context flag (default: false)
  - `max_file_lines`: Maximum lines per file (default: 1000)
  - `max_related_files`: Maximum related files to include (default: 5)
  - `max_diff_lines`: Maximum lines of diff (default: 200)
  - `include_git`, `include_dependencies`, `include_tests`: Toggle context types
- **ProjectProfile Context Settings**: Per-project context configuration in `.claude-dev-cli`
  - `max_context_files`: Limit related files
  - `max_diff_lines`: Limit diff size
  - `max_file_lines`: Limit lines per file
  - `include_tests_by_default`: Auto-include test files
  - `context_depth`: Control module search depth
- **Diff Size Limiting**: Intelligent truncation of large git diffs
  - `GitContext.gather()` accepts `max_diff_lines` parameter
  - Shows truncation indicators for visibility

### Enhanced
- `ContextGatherer` now accepts `max_file_lines` and `max_related_files` parameters
- All `gather_*` methods support optional `max_lines` parameter
- Git commit messages now benefit from full repository context
- Test and documentation generation improved with dependency awareness
- File context automatically truncated to prevent overwhelming AI

### Changed
- Context gathering respects size limits from config (global or per-project)
- Large files show truncation notices with original line count
- Diff output intelligently truncated with summary

## [0.8.0] - 2024-12-29

### Added
- **Context-Aware Operations**: Intelligent context gathering for smarter AI responses
  - `--auto-context` flag for ask, review, debug, refactor commands
  - Automatic inclusion of git context (branch, commits, modified files)
  - Dependency analysis and related file discovery
  - Python import parsing using AST
  - Multi-language dependency detection (Python, Node.js, Go, Rust)
  - Error context with structured traceback parsing
- **Context Module**: New `context.py` with 494 lines
  - GitContext: Git repository information gathering
  - DependencyAnalyzer: Import and dependency analysis
  - ErrorContext: Smart error parsing and formatting
  - ContextGatherer: Coordinator with specialized methods
- **Project Memory**: Enhanced ProjectProfile in config
  - `auto_context`: Default --auto-context behavior per project
  - `coding_style`: Remember preferred coding style
  - `test_framework`: Remember preferred test framework
  - `preferences`: Custom key-value preferences

### Enhanced
- Commands now support intelligent context gathering
- Review command includes test files automatically with --auto-context
- Debug command includes parsed error details with --auto-context
- Ask/refactor commands include dependencies and related files

## [0.7.0] - 2024-12-29

### Added
- **Workflow Chains**: YAML-based multi-step automation
  - `cdc workflow run <file>`: Execute workflow from YAML file
  - `cdc workflow list`: List available workflows
  - `cdc workflow show <file>`: Show workflow details
  - `cdc workflow validate <file>`: Validate workflow syntax
  - Variable interpolation with {{variable}} syntax
  - Conditional steps with `if` clauses
  - Approval gates for human-in-the-loop
  - Continue on error with `continue_on_error` flag
  - Three step types: command (cdc commands), shell (shell commands), set (variable assignment)
- **Warp Terminal Integration**: Enhanced output formatting and workflows
  - `cdc warp export-workflows`: Export Warp workflows for common tasks
  - `cdc warp export-launch-configs`: Export Warp launch configurations
  - Block formatting with click-to-run actions
  - 4 built-in Warp workflows (code review, test generation, refactor, debug)
- **Interactive Mode for Generation Commands**: Add `--interactive` / `-i` flag to all generation commands
  - `cdc generate tests --interactive`: Iteratively refine generated tests
  - `cdc generate docs --interactive`: Iteratively refine documentation
  - `cdc review --interactive`: Ask follow-up questions about code review findings
  - `cdc refactor --interactive`: Iteratively improve refactoring suggestions
  - Commands: 'save' to save and exit, 'exit' to discard changes
  - Maintains conversation context for intelligent refinements
- ROADMAP.md for future feature planning

### Dependencies
- Added PyYAML >= 6.0.0 for workflow support

## [0.6.0] - 2024-12-29

### Added
- **Custom Prompt Templates**: Reusable prompt templates with variable substitution
  - 8 built-in templates for common tasks (code review, testing, debugging, etc.)
  - `cdc template list` to view all templates with filtering
  - `cdc template show <name>` to view template details
  - `cdc template add <name>` to create custom templates
  - `cdc template delete <name>` to remove user templates
  - `cdc template use <name>` for interactive template execution
  - Variable substitution using {{variable}} syntax
  - Category organization (review, testing, debugging, optimization, etc.)
  - Protection against overriding/deleting built-in templates
- Template storage in `~/.claude-dev-cli/templates.json`
- Comprehensive test suite for templates (24 new tests, 163 total)

### Technical Details
- Template class with variable extraction and rendering
- TemplateManager for CRUD operations and persistence
- Built-in templates covering common developer workflows
- JSON-based storage for user templates

## [0.5.0] - 2024-12-28

### Added
- **Shell Completion**: Auto-complete for bash, zsh, and fish
  - `cdc completion install` with auto-detection
  - `cdc completion generate` for manual setup
  - Tab completion for commands and options
- **Conversation History**: Persistent chat history in interactive mode
  - Automatic saving of all conversations
  - `--continue` flag to resume last conversation
  - `--save/--no-save` flag to control history
  - `cdc history list` to view past conversations
  - `cdc history export` to export as markdown/json
  - Auto-save every 10 messages
  - Search through conversation history

### Changed
- Interactive mode now preserves conversation context
- Conversations stored in `~/.claude-dev-cli/history/`
- Clear command resets conversation without exiting

## [0.4.0] - 2024-12-28

### Added
- **Secure API Key Storage**: Cross-platform keyring support
  - macOS: Keychain integration
  - Linux: Secret Service API (GNOME Keyring, KWallet)
  - Windows: Windows Credential Locker
  - Automatic fallback to encrypted file storage
- `cdc config migrate-keys` command for manual migration
- Test environment detection to prevent system keyring prompts during tests
- Comprehensive test suite for secure storage (21 new tests)
- Storage method indicators in CLI output (🔐/🔒)

### Changed
- API keys now stored securely instead of plain text
- Automatic migration of existing plaintext keys on first run
- Config metadata and actual keys stored separately
- Enhanced `cdc config add` to show storage method
- Enhanced `cdc config list` to show storage method

### Security
- **BREAKING SECURITY IMPROVEMENT**: API keys no longer stored in plain text
- All keys automatically migrated to secure storage
- File permissions set to 0o600 for encrypted fallback files
- Zero plaintext key exposure

## [0.3.1] - 2024-12-28

### Added
- Syntax highlighting in diff editor using Pygments (auto-detects language)
- Undo support in diff editor with history stack
- Optional `plugins` dependency group for enhanced features

### Fixed
- All test failures resolved (98/98 tests passing)
- Config class now respects HOME environment variable for test isolation
- API routing hierarchy properly prioritizes explicit flags over project profiles

## [0.3.0] - 2024-12-28

### Added
- Plugin system architecture with base Plugin class and discovery mechanism
- Interactive diff editor plugin with dual keybinding support (Neovim and Fresh modes)
- `cdc diff` command for hunk-by-hunk code review
- `cdc apply-diff` command placeholder for AI workflow integration
- Auto-detection of keybinding preference from $EDITOR environment variable
- Comprehensive test suite with 98 tests across 7 test files
- CONTRIBUTING.md with developer guidelines
- WARP.md for AI assistant guidance
- Examples directory with usage guides for all major features

### Changed
- CLI now automatically discovers and loads plugins on startup
- Enhanced documentation with architecture details

### Added
- TOON format support for 30-60% token reduction
- `cdc toon encode` command to convert JSON to TOON format
- `cdc toon decode` command to convert TOON back to JSON
- `cdc toon info` command to check TOON installation status
- Optional `[toon]` installation extra for TOON format support
- `format_for_llm()` utility for automatic format selection
- `auto_detect_format()` utility for format detection
- Graceful fallback when TOON format package not installed

### Changed
- Updated pyproject.toml with toon-format optional dependency
- Enhanced README with TOON format documentation and examples

## [0.1.0] - 2024-12-27

### Added
- Initial release of claude-dev-cli
- Multi-API key management (personal/client routing)
- Interactive and single-shot modes
- Usage tracking with cost monitoring
- Context-aware routing by directory/project
- Test generation command (`cdc generate tests`)
- Code review command (`cdc review`)
- Debug assistant command (`cdc debug`)
- Documentation generation (`cdc generate docs`)
- Refactoring suggestions (`cdc refactor`)
- Git commit message generation (`cdc git commit`)
- Global configuration in `~/.claude-dev-cli/config.json`
- Project-specific configuration via `.claude-dev-cli` files
- Usage logging to `~/.claude-dev-cli/usage.jsonl`
- Cost estimation based on Claude API pricing
- Rich terminal UI with tables and panels
- Streaming and non-streaming response support
- Environment variable support for API keys
- Click-based CLI with command groups
- Comprehensive README with usage examples

### Technical Details
- Python 3.9+ support
- Type hints throughout codebase
- Pydantic models for configuration validation
- Black and Ruff for code quality
- MyPy for static type checking
- Line length: 100 characters

[0.2.0]: https://github.com/thinmanj/claude-dev-cli/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/thinmanj/claude-dev-cli/releases/tag/v0.1.0
