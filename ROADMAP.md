# Roadmap

Future development plans for claude-dev-cli.

## Current Version: 0.8.3

**Completed Features:**
- ✅ Multi-API key management with secure storage
- ✅ Developer tools (test gen, review, debug, refactor)
- ✅ Usage tracking and cost monitoring
- ✅ Shell completion (bash/zsh/fish)
- ✅ Conversation history with export and summarization
- ✅ Custom prompt templates
- ✅ TOON format support (30-60% token reduction)
- ✅ Diff editor plugin
- ✅ Workflow chains (YAML-based automation)
- ✅ Warp terminal integration
- ✅ Context intelligence with auto-gathering
- ✅ Multi-language error parsing (Python/JS/Go/Rust/Java)
- ✅ Conversation summarization (30-50% cost reduction)

## Recent: v0.7.0 - AI Workflow Integration (✅ COMPLETED)

### 1. Interactive Mode for Generation Commands
**Status**: ✅ Completed (v0.7.0)

Add `--interactive` flag to all generation commands for iterative refinement:
- ✅ `cdc generate tests --interactive`: Review and refine tests before saving
- ✅ `cdc review --interactive`: Ask follow-up questions about findings
- ✅ `cdc refactor --interactive`: Iteratively improve suggestions
- ✅ `cdc generate docs --interactive`: Refine documentation interactively

### 2. Workflow Chains
**Status**: ✅ Completed (v0.7.0)

Chain multiple AI operations for complex workflows:
- ✅ YAML-based workflow definitions
- ✅ Step chaining with variable passing
- ✅ Conditional logic and approval gates
- ✅ Three step types: command, shell, set
- ✅ CLI: `cdc workflow run/list/show/validate`

**Example**:
```yaml
name: "Review and Refactor"
steps:
  - name: review
    command: review
    args: {file: "{{target}}"}
  - name: refactor
    command: refactor
    args: {file: "{{target}}"}
    approval_required: true
  - name: commit
    command: git commit
    if: "{{refactor.success}}"
```

### 3. Warp Terminal Integration
**Status**: ✅ Completed (v0.7.0)

Deep integration with Warp features:
- ✅ Warp block formatting for outputs
- ✅ Warp workflow file generation
- ✅ Launch configuration templates
- ✅ Click-to-apply actions in Warp
- ✅ CLI: `cdc warp export-workflows/export-launch-configs`
- ✅ 4 built-in workflows (review, test, refactor, debug)

### 4. Context-Aware Operations
**Status**: ✅ Completed (v0.8.0-0.8.2)

Automatic context gathering:
- ✅ Auto-include relevant files with `--auto-context`
- ✅ Git context (commits, diffs, branches)
- ✅ Dependency context (package.json, requirements.txt, go.mod, Cargo.toml)
- ✅ Error context capture with multi-language parsing
- ✅ Project memory and preferences
- ✅ Context preview with `cdc context summary`
- ✅ Smart truncation with configurable limits

## Recent: v0.8.0 - Context Intelligence (✅ COMPLETED)

**Features**:
- ✅ `--auto-context` flag for 7 commands
- ✅ Git, dependency, and file relationship analysis
- ✅ Error traceback parsing (Python/JS/Go/Rust/Java)
- ✅ Context preview and token estimation
- ✅ Global and per-project configuration

## Recent: v0.8.3 - Conversation Summarization (✅ COMPLETED)

**Features**:
- ✅ Manual summarization: `cdc history summarize`
- ✅ Automatic summarization in interactive mode
- ✅ 30-50% token reduction in long conversations
- ✅ Smart compression with rolling summaries
- ✅ Configurable thresholds and behavior
- ✅ Token savings display
- ✅ 257 tests passing (39 new)

## Next: v0.9.0 - Team & Collaboration

## Future: Team & Collaboration Features

### Team Features
- Shared templates via Git
- Team usage analytics
- Centralized configuration
- Audit logging

### IDE Integration
- VSCode extension
- JetBrains plugin
- Sublime Text plugin

## Future: v0.9.0 - Advanced Features

### Multi-file Operations
- Batch operations across files
- Project-wide refactoring
- Dependency analysis

### Advanced Templates
- Template import/export
- Template versioning
- Template marketplace

### Performance
- Response caching
- Parallel API calls
- Streaming optimizations

## Contributing

See CONTRIBUTING.md for guidelines on implementing roadmap features.
