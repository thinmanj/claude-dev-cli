# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Interactive Mode for Generation Commands**: Add `--interactive` / `-i` flag to all generation commands
  - `cdc generate tests --interactive`: Iteratively refine generated tests
  - `cdc generate docs --interactive`: Iteratively refine documentation
  - `cdc review --interactive`: Ask follow-up questions about code review findings
  - `cdc refactor --interactive`: Iteratively improve refactoring suggestions
  - Commands: 'save' to save and exit, 'exit' to discard changes
  - Maintains conversation context for intelligent refinements

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
