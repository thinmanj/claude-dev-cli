# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-12-28

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
