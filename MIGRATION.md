# Migration Guide: claude-dev-cli → devflow

This guide helps you transition from `claude-dev-cli` to `devflow`.

## Overview

Starting with v0.20.0, this project will be published under a new name: **devflow**.
The rename reflects the tool's evolution from a Claude-specific CLI to a comprehensive
AI-powered development automation platform supporting multiple providers.

## Timeline

### v0.19.0 (Current) - Deprecation Warnings
- ✅ All existing functionality works
- ⚠️ Deprecation warnings displayed
- 📦 Published as `claude-dev-cli`
- 🔧 Command: `cdc`

### v0.20.0 - Dual Publishing
- ✅ Published under both names
- 📦 PyPI packages: `claude-dev-cli` and `devflow`
- 🔧 Commands: `cdc` (legacy) and `devflow`/`df` (new)
- 🔄 `claude-dev-cli` becomes a wrapper around `devflow`

### v1.0.0 - Official Rename
- 📦 Primary package: `devflow`
- 🔧 Primary command: `devflow` (alias: `df`)
- ⚠️ `claude-dev-cli` deprecated but still functional
- 📝 All documentation uses new name

## What Changes

### Package Name
```bash
# Old
pip install claude-dev-cli

# New (v0.20.0+)
pip install devflow

# Both work in v0.20.0
pip install claude-dev-cli  # Still works, installs devflow
```

### Command Name
```bash
# Old
cdc ask "question"
cdc ticket execute TASK-123

# New (v0.20.0+)
devflow ask "question"
devflow ticket execute TASK-123

# Short alias
df ask "question"
df ticket execute TASK-123

# Legacy command still works
cdc ask "question"  # Redirects to devflow
```

### Configuration Directory
Both names will use the same configuration:
- `~/.claude-dev-cli/` - Existing configs continue to work
- `~/.devflow/` - New installations (v1.0.0+)
- Migration is automatic

## What Stays the Same

✅ **All features** - No functionality changes  
✅ **All commands** - Same command structure  
✅ **Configuration** - Your settings are preserved  
✅ **API keys** - No need to reconfigure  
✅ **Workflows** - All workflows continue to work  
✅ **Plugins** - Compatible plugins work unchanged  

## Migration Steps

### Option 1: Do Nothing (Recommended)
The migration is automatic. Your existing installation will continue to work.

### Option 2: Early Adoption (v0.20.0+)
```bash
# Uninstall old package
pip uninstall claude-dev-cli

# Install new package
pip install devflow

# Your config automatically migrates
```

### Option 3: Side-by-Side (v0.20.0 only)
```bash
# Keep both installed during transition
pip install devflow

# Both commands work
cdc --version   # Shows 0.20.0
devflow --version  # Shows 0.20.0
```

## Suppressing Deprecation Warnings

If you want to suppress the deprecation warnings in v0.19.x:

### Temporarily
```bash
export CLAUDE_DEV_CLI_NO_DEPRECATION=1
cdc ask "question"
```

### Permanently
Add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):
```bash
export CLAUDE_DEV_CLI_NO_DEPRECATION=1
```

### Acknowledge Once
When the warning appears, respond `y` to acknowledge it and hide future warnings.

## For CI/CD and Scripts

### Current (v0.19.0)
```bash
# Suppress warnings in automated environments
export CLAUDE_DEV_CLI_NO_DEPRECATION=1
cdc ticket execute TASK-123
```

### Future (v0.20.0+)
```bash
# Update to new command name
devflow ticket execute TASK-123

# Or use legacy command (still works)
cdc ticket execute TASK-123
```

## For Tool Integrations

If you've integrated claude-dev-cli into other tools:

### Python
```python
# Old (still works)
from claude_dev_cli import ClaudeClient

# New (v0.20.0+)
from devflow import ClaudeClient

# Both work during transition
```

### Shell Scripts
```bash
# Update command name when ready
# Old: cdc
# New: devflow or df
```

## Breaking Changes

**None!** This is a rename only. All functionality remains identical.

The only "breaking" change is the deprecation warnings in v0.19.0, which can be suppressed.

## FAQ

### Will my existing config work?
Yes, all configuration is automatically migrated.

### Do I need to reconfigure API keys?
No, all API keys and settings are preserved.

### When should I switch?
You can switch anytime after v0.20.0 is released. There's no urgency.

### Will `cdc` command stop working?
No, the `cdc` command will continue to work indefinitely as a compatibility alias.

### What about my workflows?
All workflows, templates, and customizations continue to work unchanged.

### Can I use both names?
Yes, during the transition period (v0.20.0), both package names and commands work.

### Why the rename?
The project has evolved beyond Claude AI to support multiple providers (Anthropic, 
OpenAI, Ollama) and comprehensive project automation. The new name better reflects 
these capabilities and isn't tied to a specific AI provider.

## Need Help?

- 📖 [README](README.md) - Updated documentation
- 🔄 [RENAME.md](RENAME.md) - Detailed rename plan
- 🐛 [Issues](https://github.com/thinmanj/claude-dev-cli/issues) - Report problems
- 💬 [Discussions](https://github.com/thinmanj/claude-dev-cli/discussions) - Ask questions

## Support Schedule

- **v0.19.x**: Full support, bug fixes
- **v0.20.x**: Dual publishing, both names supported
- **v1.0.x+**: Primary support for `devflow`, legacy support for `cdc` command
- **v2.0.0**: `claude-dev-cli` package fully deprecated (legacy command still works)

The `cdc` command will be supported for the foreseeable future to ensure backward compatibility.
