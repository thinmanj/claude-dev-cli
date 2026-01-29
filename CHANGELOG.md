# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.13.3] - 2026-01-29

### Enhanced
- **Robust Diff Parsing**: Integrated `unidiff` library for production-grade diff handling
  - Replaced manual regex-based diff parsing with `unidiff.PatchSet`
  - More reliable hunk parsing with edge case handling (no newline, binary diffs, malformed diffs)
  - Simplified hunk application using unidiff's built-in line iteration
  - Better handling of complex diff scenarios
  - 435k weekly downloads, MIT licensed, well-maintained library

### Changed
- **Internal Refactoring**: Updated `multi_file_handler.py` to use unidiff
  - Created `HunkWrapper` class wrapping `unidiff.Hunk` with approval state
  - `parse_hunks()`: Now uses `PatchSet(StringIO(diff_text))` for parsing
  - `apply_approved_hunks()`: Uses unidiff's line access methods (`line.is_added`, `line.is_context`, `line.value`)
  - Cleaner code with better maintainability
  - Properties: `source_start`, `source_length`, `target_start`, `target_length`
  - Graceful fallback if unidiff not available

### Dependencies
- Added: `unidiff>=0.7.0` as core dependency

### Testing
- Updated tests to use `HunkWrapper` instead of direct `Hunk` class
- All 37 multi_file_handler tests passing
- All 95 core tests passing (config, core, commands, multi_file_handler)

### Technical Details
- unidiff provides `PatchSet`, `PatchedFile`, and `Hunk` classes
- Each line has properties: `is_added`, `is_removed`, `is_context`, `value`
- Hunk attributes: `source_start`, `source_length`, `target_start`, `target_length`
- Better error handling for edge cases like missing newlines
- Maintains backward compatibility with existing hunk approval flow

## [0.13.2] - 2026-01-29

### Added
- **Edit Option**: Open files in `$EDITOR` before applying changes
  - Interactive file editing at confirmation prompt
  - Type 'edit' to open each file in your editor (vi, nano, code, emacs, etc.)
  - Make manual adjustments, save and close
  - Changes merged back and applied
  - Respects `$EDITOR` environment variable (defaults to `vi`)
  - Skips delete operations (can't edit deleted files)
  - Each file edited individually in temp location
  - Temp files automatically cleaned up

- **Save Option**: Save to custom location interactively
  - Alternative to `-o` flag with more flexibility
  - Type 'save' at confirmation prompt
  - Single file: prompts for custom filename
  - Multiple files: prompts for output directory
  - Creates parent directories automatically
  - Relative paths resolved from base directory
  - Skips delete operations
  - Does not continue with original write (saves and exits)

### Enhanced
- **Confirmation Flow**: Updated prompt options
  - New prompt: `(Y/n/preview/patch/edit/save/help)`
  - Help text includes edit and save descriptions
  - All file generation commands support edit/save
  - Base path passed to confirmation for edit/save functionality

- **User Experience**:
  - Edit: Full control before applying changes
  - Save: Try changes elsewhere before committing
  - Edit + Preview workflow: review, edit, then apply
  - Save for later workflow: generate, save, review offline
  - Non-destructive operations

### Use Cases
```bash
# Edit generated files before applying
cdc generate feature -f spec.md
# Type 'edit' at prompt to open in $EDITOR

# Save to custom location
cdc generate code -d "REST API" -o project/
# Type 'save' at prompt, enter custom path

# Combined workflow
cdc refactor src/
# Type 'preview' to review, 'edit' to adjust, then 'y' to apply
```

### Technical Details
- `_edit_files()`: Subprocess integration with $EDITOR
- `_save_to_location()`: Interactive path prompts with validation
- Both methods handle single/multiple files
- Confirmation method signature updated: `confirm(console, base_path)`
- All command calls updated to pass base_path

## [0.13.1] - 2026-01-29

### Added
- **Hunk-by-Hunk Diff Approval**: Interactive patch mode for file modifications (like `git add -p`)
  - New `Hunk` dataclass to represent individual diff chunks
  - `parse_hunks()`: Parses unified diffs into individual reviewable hunks
  - `apply_approved_hunks()`: Applies only user-approved hunks to files
  - `confirm_with_hunks()`: Interactive hunk-by-hunk confirmation flow
  - New 'patch' option in confirmation prompt
  - Per-hunk options: `y` (yes), `n` (no), `s` (skip file), `q` (quit), `help`
  - Per-file options for create/delete: `y`, `n`, `s`, `q`
  - Syntax-highlighted diff display using Rich

### Enhanced
- **Fine-Grained Control**: Review and approve changes at the hunk level
  - Partial approval: Apply some hunks while keeping original code for others
  - Skip entire files or quit early with partial changes applied
  - Visual diff display with monokai theme and line numbers
  - Clear indicators showing hunk progress ("Hunk 2/5")

- **Safety Features**:
  - Files with no approved hunks remain unchanged
  - Dry-run shows hunk counts: "Would modify: file.py (2/3 hunks)"
  - Skip messages: "Skipped: file.py (no hunks approved)"
  - Only writes files when at least one hunk is approved

- **User Experience**:
  - Confirmation prompt updated: `(Y/n/preview/patch/help)`
  - Help command explains all options
  - Quit command (q) preserves already-approved changes
  - Skip command (s) moves to next file

### Testing
- Added 7 new tests for hunk functionality
- All 37 tests passing
- Tests cover: hunk dataclass, parsing, approval states, partial application, file writing
- Test scenarios: all approved, none approved, partial approval, skipped files

### Examples
```bash
# Generate feature with hunk-by-hunk approval
cdc generate feature -f spec.md
# At prompt: Continue? (Y/n/preview/patch/help) patch
# Review each hunk: Apply this hunk? (y/n/s/q/help)

# Refactor with granular control
cdc refactor src/
# Type 'patch' at confirmation to review each change
```

### Technical Details
- `Hunk` dataclass tracks: header, lines, old_start, old_count, new_start, new_count, approved
- Hunk parsing uses regex: `@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@`
- Bottom-up hunk application to maintain correct line numbers
- Partial hunk application rebuilds file from approved hunks only
- Empty hunks list results in full file replacement (backward compatible)

## [0.13.0] - 2026-01-29

### Added
- **Multi-File Output System**: Commands can now generate and apply changes to multiple files
  - New `multi_file_handler.py` module for parsing structured AI responses
  - Support for file markers: `## File:`, `## Create:`, `## Modify:`, `## Delete:`
  - Visual directory tree preview with Rich formatting
  - Interactive confirmation with file content preview
  - Path validation and security checks (no traversal, no absolute paths)
  - Dry-run mode to preview without writing files
  - `--dry-run` flag: Show what would change without writing
  - `--yes` flag: Apply changes without confirmation
  - `--preview` flag: Review changes before applying

- **Enhanced `generate code` Command**:
  - Detects directory output (path ends with `/` or is existing directory)
  - Multi-file mode: Generates complete project structures
  - Single-file mode: Maintains backward compatibility
  - Examples:
    - `cdc generate code -d "FastAPI app" -o my-api/` (generates multiple files)
    - `cdc generate code -f spec.md -o project/ --dry-run` (preview multi-file output)
    - `cdc generate code -f spec.md -o script.py` (single file, unchanged behavior)

- **Enhanced `generate feature` Command**:
  - Parses structured multi-file output from Claude
  - Shows interactive tree preview of changes
  - Applies changes to multiple files simultaneously
  - `--dry-run`: Preview feature implementation
  - `--yes`: Apply without confirmation
  - Falls back to markdown display if no structured output
  - Examples:
    - `cdc generate feature -d "add auth" src/ --dry-run`
    - `cdc generate feature -f spec.md --yes`

- **Enhanced `refactor` Command**:
  - Multi-file refactoring with structured output
  - Tree preview of refactored files
  - `--preview`, `--dry-run`, `--yes` flags
  - Maintains backward compatibility with `-o` flag for single file
  - Examples:
    - `cdc refactor src/ --dry-run`
    - `cdc refactor file.py --yes`

### Enhanced
- **Prompt Engineering**: Updated prompts request structured multi-file format
  - Clear instructions for file markers in AI responses
  - Language-aware code block formatting
  - Complete file content (not diffs) for easier parsing

- **Safety Features**:
  - Path validation prevents directory traversal attacks
  - Rejects absolute paths for security
  - Resolves paths safely before writing
  - Creates parent directories automatically

- **User Experience**:
  - Visual tree shows: `(new)`, `(modified)`, `(deleted)` status
  - Summary shows counts: "2 created, 1 modified, 0 deleted"
  - Line counts displayed for each file
  - Interactive preview with content display
  - Confirmation prompt with multiple options (y/n/preview/help)

### Testing
- Added 30 comprehensive tests for `multi_file_handler`
- Tests cover: parsing, validation, tree building, file operations, dry-run, confirmation
- All tests pass (333 total: 30 new + 303 existing)

### Technical Details
- `FileChange` dataclass: Tracks path, content, change_type, original_content, diff
- `MultiFileResponse` class methods:
  - `parse_response()`: Extracts file changes from AI output
  - `validate_paths()`: Security validation
  - `build_tree()`: Creates Rich tree visualization
  - `preview()`: Shows tree and summary
  - `write_all()`: Writes all changes with dry-run support
  - `confirm()`: Interactive confirmation prompt
- Supports multiple languages in code blocks
- Handles whitespace variations in markers
- Graceful fallback to single-file or markdown output

## [0.12.1] - 2026-01-29

### Fixed
- **CRITICAL**: Fixed `ClaudeClient` instantiation bug in `generate code` and `generate feature` commands
- Error: "ClaudeClient.__init__() got an unexpected keyword argument 'model'"
- Bug was passing `model` parameter to `__init__()` instead of `.call()` method
- Both commands now work correctly with model profiles (e.g., `-m fast`)

## [0.12.0] - 2026-01-29

### Added
- **`generate code` Command**: Generate new code from specifications
  - Supports multiple input sources: `--description`, `-f/--file`, `--pdf`, `--url`
  - Auto-detects target language from output file extension
  - Interactive refinement mode with `-i/--interactive`
  - Project context awareness with `--auto-context`
  - Examples:
    - `cdc generate code --description "REST API client" -o client.py`
    - `cdc generate code --file spec.md -o implementation.go`
    - `cdc generate code --pdf requirements.pdf -o app.js`
    - `cdc generate code --url https://example.com/spec -o service.py`

- **`generate feature` Command**: Add features to existing codebase
  - Analyzes existing code and generates implementation plan
  - Supports multiple input sources for feature specifications
  - Multi-file analysis with `--max-files` limit
  - Preview mode with `--preview` flag (no changes applied)
  - Auto-detection of project files
  - Interactive refinement with `-i/--interactive`
  - Examples:
    - `cdc generate feature --description "Add authentication" src/`
    - `cdc generate feature --file feature-spec.md`
    - `cdc generate feature --pdf requirements.pdf --preview`
    - `cdc generate feature --url https://example.com/spec`

- **Input Sources Module** (`input_sources.py`): Unified input handling
  - `read_text_input()`: Direct text descriptions
  - `read_file_input()`: Read from text files (.txt, .md, etc.)
  - `read_pdf_input()`: Extract text from PDF documents
  - `read_url_input()`: Fetch and parse content from URLs
  - `get_input_content()`: Unified interface with validation
  - Supports HTML, JSON, and plain text from URLs
  - Graceful fallback when optional dependencies not installed

- **Optional Dependencies Group**: `pip install 'claude-dev-cli[generation]'`
  - `pypdf>=3.0.0`: PDF text extraction
  - `requests>=2.28.0`: URL fetching
  - `beautifulsoup4>=4.0.0`: HTML parsing
  - Clear error messages when dependencies missing

### Enhanced
- Both commands organized under `generate` group for consistency
- Commands: `generate code`, `generate feature`, `generate tests`, `generate docs`
- Supports 13+ languages: Python, JavaScript, TypeScript, Go, Rust, Java, C++, C, C#, Ruby, PHP, Swift, Kotlin
- Language auto-detection from file extensions
- Smart HTML parsing (removes scripts, nav, footer, header)
- JSON pretty-printing from URLs
- Interactive refinement with streaming responses
- Full integration with model profiles and API routing

### Testing
- Added 18 tests for input_sources module
- Tests cover all input types, error handling, graceful fallbacks
- Mock testing for PDF and URL functionality
- Tests work with/without optional dependencies
- Total: 303 tests (18 new, 285 existing)

## [0.11.0] - 2026-01-28

### Added
- **Multi-File Support**: All major commands now support multiple files, directories, and auto-detection
  - Commands affected: `review`, `refactor`, `generate tests`, `generate docs`
  - Can now process multiple files: `cdc review file1.py file2.py file3.py`
  - Can process entire directories: `cdc review src/`
  - Auto-detects git changes when no paths specified: `cdc review` (uses staged → modified → current dir)
  - `--max-files N` option to limit number of files processed
- **New Command**: `cdc git review` - Review git changes
  - `--staged`: Review only staged changes
  - `--branch <range>`: Review branch changes (e.g., `main..HEAD`)
  - `-i/--interactive`: Interactive follow-up questions
  - Default behavior: Reviews all modified files
- **Path Utilities Module**: `path_utils.py`
  - `expand_paths()`: Expands directories/globs to code files (25+ extensions)
  - `get_git_changes()`: Gets staged/modified/branch files from git
  - `auto_detect_files()`: Auto-detects files based on git status
  - `is_code_file()`: Filters by file extension
  - Supports: `.py`, `.js`, `.ts`, `.go`, `.rs`, `.java`, `.cpp`, `.cs`, `.rb`, `.php`, and more

### Changed
- **Review command**: Now accepts `[PATHS]...` instead of single `file_path`
- **Refactor command**: Now accepts `[PATHS]...` with auto-detection
- **Generate tests command**: Now accepts `[PATHS]...`, max-files default: 10
- **Generate docs command**: Now accepts `[PATHS]...`, max-files default: 10
- All multi-file commands combine files into single prompt for batch processing
- Output option (`-o`) only works with single file (warnings shown for multiple files)

### Enhanced
- Smart file list display: Shows first 5-10 files, then "... and N more"
- Consistent UX across all commands
- Auto-detection hierarchy: Staged files → Modified files → Current directory files
- Respects `.gitignore` through git commands

### Testing
- Added 25 new tests for path_utils module
- Total: 285 tests (25 new, 260 existing)
- Tests cover: file expansion, git integration, auto-detection, edge cases
- Note: 2 legacy CLI tests need updating for new multi-file signatures

### Examples
```bash
# Review multiple files
cdc review file1.py file2.py file3.py

# Review directory
cdc review src/

# Auto-detect (reviews git changes)
cdc review

# Review git changes
cdc git review --staged
cdc git review --branch main..HEAD

# Generate tests for directory
cdc generate tests src/ --max-files 10

# Refactor with auto-detection
cdc refactor
```

## [0.10.1] - 2026-01-28

### Fixed
- **CRITICAL**: Fixed 400 error "model: Input should be a valid string"
- Bug in `ClaudeClient.call()` was passing unresolved `model` parameter instead of `resolved_model`
- This broke all commands after v0.10.0 release (generate docs, ask, review, etc.)
- Model profile resolution now works correctly

## [0.10.0] - 2026-01-28

### Added
- **Model Profile System**: Create named model profiles with custom pricing
  - `ModelProfile` class with pricing per Mtok (input/output)
  - Support for global and API-specific profiles
  - Project-level model profile preferences
  - Profile name resolution to model IDs (use `fast`, `smart`, `powerful` instead of full model IDs)
- **CLI Commands**: `cdc model` command group
  - `cdc model add <name> <model_id>`: Create model profile with custom pricing
  - `cdc model list [--api <name>]`: View all profiles with pricing table
  - `cdc model show <name>`: Detailed profile information
  - `cdc model remove <name>`: Delete profile
  - `cdc model set-default <name> [--api <name>]`: Set default (global or per-API)
- **Default Profiles**: 3 built-in profiles
  - `fast`: Claude 3.5 Haiku ($0.80/$4.00 per Mtok)
  - `smart`: Claude Sonnet 4 ($3.00/$15.00 per Mtok) - default
  - `powerful`: Claude Opus 4 ($15.00/$75.00 per Mtok)
- **Dynamic Pricing**: Usage tracking now uses model profile pricing
  - Calculates costs from profile definitions instead of hardcoded values
  - Supports per-API pricing differences
  - Automatic fallback to Sonnet pricing for unknown models
- **Model Resolution Hierarchy**:
  1. Explicit `-m/--model` flag (profile name or model ID)
  2. Project-specific model profile (`.claude-dev-cli`)
  3. API-specific default model profile
  4. Global default model profile
  5. Legacy default model setting
- **Multi-API Architecture**: Each API config can have its own default model profile
- **Config Schema**: Added `model_profiles`, `default_model_profile` to config.json

### Changed
- `APIConfig` now has `default_model_profile` field for per-API defaults
- `ProjectProfile` now has `model_profile` field for per-project defaults
- `ClaudeClient._resolve_model()` converts profile names to model IDs automatically
- Usage tracking `_calculate_cost()` looks up pricing dynamically from profiles
- Removed hardcoded `MODEL_PRICING` dictionary from usage.py

### Enhanced
- You can now use profile names anywhere a model ID is accepted
  - `cdc ask -m fast "question"` uses Haiku automatically
  - `cdc ask -m smart "question"` uses Sonnet 4 automatically
  - `cdc ask -m powerful "question"` uses Opus 4 automatically
- Supports custom profiles with different pricing per API config
- Profile-based pricing enables accurate cost tracking for custom models

### Testing
- All 260 tests passing
- Updated tests to work with new model profile system
- Tests validate dynamic pricing and model resolution

## [0.9.0] - 2026-01-28

### Added
- **Model Configuration**: `cdc config set-model <model>` command to change default model
- Display default model in `cdc config list`

### Changed
- Updated default model from `claude-3-5-sonnet-20241022` to `claude-sonnet-4-5-20250929`
- This fixes 404 errors with deprecated model versions

## [0.8.8] - 2026-01-28

### Fixed
- **CRITICAL**: Fixed "Is a directory" error when ~/.claude-dev-cli exists as directory in $HOME
- `get_project_profile()` now checks if .claude-dev-cli is a file before trying to open it
- Added error handling to skip invalid project config files
- This was the root cause of Errno 21 errors on Linux installations

## [0.8.7] - 2026-01-28

### Fixed
- Added directory validation to TemplateManager initialization
- Fixed potential "Is a directory" errors for templates.json and templates directory
- Completes comprehensive file/directory validation across all config paths

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
