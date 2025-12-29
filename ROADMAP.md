# Roadmap

Future development plans for claude-dev-cli.

## Current Version: 0.6.0

**Completed Features:**
- ✅ Multi-API key management with secure storage
- ✅ Developer tools (test gen, review, debug, refactor)
- ✅ Usage tracking and cost monitoring
- ✅ Shell completion (bash/zsh/fish)
- ✅ Conversation history with export
- ✅ Custom prompt templates
- ✅ TOON format support
- ✅ Diff editor plugin

## Next: v0.7.0 - AI Workflow Integration

### 1. Interactive Mode for Generation Commands
**Status**: ✅ Completed (v0.6.1)

Add `--interactive` flag to all generation commands for iterative refinement:
- ✅ `cdc generate tests --interactive`: Review and refine tests before saving
- ✅ `cdc review --interactive`: Ask follow-up questions about findings
- ✅ `cdc refactor --interactive`: Iteratively improve suggestions
- ✅ `cdc generate docs --interactive`: Refine documentation interactively

### 2. Workflow Chains
**Status**: Planned

Chain multiple AI operations for complex workflows:
- YAML-based workflow definitions
- Step chaining with variable passing
- Conditional logic and approval gates
- Rollback support
- CLI: `cdc workflow run <name>`

**Example**:
```yaml
# review-fix-test.yaml
steps:
  - review: {file: "{{target}}"}
  - ask: "Fix issues: {{review.output}}"
  - generate tests: {file: "{{target}}"}
  - git commit: {if: "{{tests.passed}}"}
```

### 3. Warp Terminal Integration
**Status**: Planned

Deep integration with Warp features:
- Warp block formatting for outputs
- Warp workflow file generation
- Launch configuration templates
- Click-to-apply actions in Warp
- Warp Drive compatibility for team sharing

### 4. Context-Aware Operations
**Status**: Planned

Automatic context gathering:
- Auto-include relevant files
- Git context (commits, diffs, branches)
- Dependency context (package.json, requirements.txt)
- Error context capture
- Project memory

## Future: v0.8.0 - Team & Collaboration

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
