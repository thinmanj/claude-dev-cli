# Project Rename Plan

## Current Name
`claude-dev-cli` - Claude Development CLI

## Reasoning for Rename
The project has evolved beyond being just a Claude AI CLI tool. It now includes:
- Multi-provider AI support (Anthropic, OpenAI, Ollama, and more)
- Complete project management automation
- Ticket management across multiple systems (repo-tickets, Jira, Linear, etc.)
- Bug triage and tracking
- VCS integration
- Workflow automation
- Progress logging and notifications

## Potential New Names

### Option 1: `devflow`
**Pros:**
- Short and memorable
- Describes the automated development workflow
- Not tied to any specific AI provider
- `.dev` domain available

**Cons:**
- Generic term, might conflict with other tools

### Option 2: `auto-dev-cli` / `adc`
**Pros:**
- Clearly indicates automation
- Short abbreviation (adc)
- Descriptive of core purpose

**Cons:**
- Less catchy than devflow

### Option 3: `codegen-pm`
**Pros:**
- Combines code generation + project management
- Clear purpose

**Cons:**
- Longer name
- Less professional sounding

### Option 4: `ticketflow`
**Pros:**
- Emphasizes ticket-based workflow
- Professional sounding

**Cons:**
- Might sound too focused on tickets only

## Recommended: `devflow`

**Full Name:** DevFlow - AI-Powered Development Automation
**CLI Command:** `devflow` or `df`

## Migration Plan

1. **Version 0.17.x - 0.19.x**: Keep current name, add deprecation warnings
2. **Version 0.20.0**: Publish under both names (`claude-dev-cli` and `devflow`)
3. **Version 1.0.0**: Official rename to `devflow`

## Package Structure After Rename

```
devflow/
├── ai/           # AI provider integrations
├── tickets/      # Ticket management
├── project/      # Project automation
├── vcs/          # Version control
├── logging/      # Progress tracking
├── notifications/# Notification systems
└── cli.py        # Main CLI
```

## CLI Command Changes

```bash
# Old
cdc ask "question"
cdc ticket execute TASK-123

# New  
devflow ask "question"
devflow ticket execute TASK-123

# Or with short alias
df ask "question"
df ticket execute TASK-123
```

## Notes
- All existing functionality will be maintained
- Backward compatibility shims for old command names
- PyPI package will redirect claude-dev-cli → devflow
- Documentation will be updated gradually
