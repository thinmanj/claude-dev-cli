# Claude Dev CLI - Fast Track Guide

Get up and running with claude-dev-cli in minutes! This guide takes you from installation to advanced workflows.

## 📦 Installation (30 seconds)

```bash
# Basic installation
pip install claude-dev-cli

# Or with all features (recommended)
pip install claude-dev-cli[toon]
```

## 🔑 Setup (1 minute)

```bash
# Set your API key
export PERSONAL_ANTHROPIC_API_KEY="sk-ant-..."

# Add to config
cdc config add personal --default

# Verify it works
cdc ask "hello"
```

## 🎯 Level 1: Basic Usage (5 minutes)

### Quick Questions

```bash
# Simple question
cdc ask "explain Python decorators"

# With file context
cdc ask -f mycode.py "what does this do?"

# From clipboard/pipe
pbpaste | cdc ask "review this code"
```

### Interactive Chat

```bash
# Start chat mode
cdc interactive

# In the chat:
You: explain asyncio
Claude: [detailed explanation]
You: show me an example
Claude: [example code]
You: exit
```

## 🛠️ Level 2: Developer Tools (10 minutes)

### Code Review

```bash
# Basic review
cdc review src/api.py

# With follow-up questions
cdc review src/api.py --interactive
You: are there any security issues?
You: how can I optimize this?
You: exit
```

### Test Generation

```bash
# Generate tests
cdc generate tests src/calculator.py -o tests/test_calculator.py

# Refine interactively
cdc generate tests src/calculator.py --interactive
You: add edge cases for division by zero
You: add fixtures for test data
You: save
```

### Debug Errors

```bash
# Analyze error from output
python buggy.py 2>&1 | cdc debug

# Debug specific file with error
cdc debug -f buggy.py -e "NameError: name 'x' is not defined"
```

### Refactoring

```bash
# Get refactoring suggestions
cdc refactor legacy_code.py

# Interactive refactoring
cdc refactor legacy_code.py --interactive
You: focus on performance
You: apply SOLID principles
You: save
```

### Git Commit Messages

```bash
# Stage your changes
git add .

# Generate commit message
cdc git commit

# Copy and use the suggested message
git commit -m "..."
```

## 🧠 Level 3: Context-Aware Intelligence (15 minutes)

### Smart Code Review

```bash
# Review with full context
cdc review src/api.py --auto-context

# Automatically includes:
# ✓ Git context (branch, recent commits, modified files)
# ✓ Dependencies (requirements.txt, package.json)
# ✓ Related files (through imports)
# ✓ Test files (if they exist)
```

### Intelligent Debugging

```bash
# Debug with context
python broken.py 2>&1 | cdc debug -f broken.py --auto-context

# Automatically includes:
# ✓ Parsed error traceback (file, line, function)
# ✓ Git context (recent changes)
# ✓ Related code files
```

### Context-Aware Questions

```bash
# Ask with full project context
cdc ask -f src/api.py --auto-context "how can I improve error handling?"

# Gets context about:
# ✓ Imported modules
# ✓ Project dependencies
# ✓ Git history
```

## 📝 Level 4: Templates (20 minutes)

### Use Built-in Templates

```bash
# List available templates
cdc template list

# Use a template
cdc template use debug-error
error: [paste your error]
code: [paste your code]
```

### Create Custom Templates

```bash
# Create a template for API design
cdc template add api-review \
  -c "Review this {{framework}} API for:
- RESTful design
- Error handling
- Security best practices
- Performance

API Code:
{{code}}" \
  -d "API review template" \
  --category review

# Use your template
cdc template use api-review
framework: FastAPI
code: [paste your API code]
```

### Template Categories

```bash
# List by category
cdc template list --category review
cdc template list --category testing
cdc template list --category debugging

# Filter user templates
cdc template list --user
```

## 🔄 Level 5: Workflows (30 minutes)

### Create a Workflow

```bash
# Create workflow file: ~/.claude-dev-cli/workflows/review-and-test.yaml
```

```yaml
name: "Review, Test, and Commit"
description: "Complete code review and testing workflow"

steps:
  - name: review-code
    command: review
    args:
      file: "{{target_file}}"
    output_var: review_result

  - name: ask-user-approval
    shell: echo "Review complete. Press enter to continue..."

  - name: generate-tests
    command: generate tests
    args:
      file: "{{target_file}}"
    approval_required: true
    output_var: tests

  - name: run-tests
    shell: "pytest tests/test_{{target_file}}"
    continue_on_error: true
    output_var: test_results

  - name: commit-if-passed
    command: git commit
    if: "{{test_results.success}}"
    approval_required: true
```

### Run Workflows

```bash
# Run the workflow
cdc workflow run ~/.claude-dev-cli/workflows/review-and-test.yaml \
  -v target_file=src/api.py

# List available workflows
cdc workflow list

# Validate workflow syntax
cdc workflow validate ~/.claude-dev-cli/workflows/review-and-test.yaml
```

### Complex Workflow Example

```yaml
name: "Complete Feature Development"
description: "Review, refactor, test, document, and commit"

steps:
  - name: initial-review
    command: review
    args:
      file: "{{feature_file}}"
    output_var: review

  - name: refactor
    command: refactor
    args:
      file: "{{feature_file}}"
    approval_required: true

  - name: generate-tests
    command: generate tests
    args:
      file: "{{feature_file}}"
    output_var: tests

  - name: save-tests
    shell: "echo '{{tests}}' > tests/test_{{feature_file}}"

  - name: run-tests
    shell: "pytest tests/test_{{feature_file}}"
    output_var: test_results

  - name: generate-docs
    command: generate docs
    args:
      file: "{{feature_file}}"
    if: "{{test_results.success}}"

  - name: commit-all
    command: git commit
    if: "{{test_results.success}}"
    approval_required: true
```

## 🎨 Level 6: Warp Terminal Integration (35 minutes)

### Export Warp Workflows

```bash
# Export built-in workflows
cdc warp export-workflows

# Creates 4 Warp workflows:
# - code-review-workflow.yaml
# - test-generation-workflow.yaml
# - refactor-workflow.yaml
# - debug-workflow.yaml

# Use in Warp with click-to-run actions
```

### Export Launch Configs

```bash
# Export Warp launch configurations
cdc warp export-launch-configs

# Creates launch configs for:
# - Claude Dev CLI - Interactive
# - Claude Dev CLI - Review Mode
# - Claude Dev CLI - Test Generation
```

## 💾 Level 7: Multi-Project Setup (40 minutes)

### Project-Specific Configuration

```bash
# In your client project
cd /path/to/client-project

# Create project config
cat > .claude-dev-cli << 'EOF'
{
  "name": "Client Project",
  "api_config": "client",
  "auto_context": true,
  "coding_style": "PEP 8 strict",
  "test_framework": "pytest",
  "preferences": {
    "max_line_length": "100",
    "docstring_style": "Google"
  }
}
EOF

# All commands in this directory now use:
# - Client's API key
# - Auto-context by default
# - Remembered preferences
```

### Multi-API Setup

```bash
# Add client API
export CLIENT_ANTHROPIC_API_KEY="sk-ant-..."
cdc config add client --description "Client Enterprise API"

# Personal projects use personal API
cd ~/my-project
cdc review code.py  # Uses personal API

# Client projects use client API
cd /path/to/client-project
cdc review code.py  # Uses client API (from .claude-dev-cli)
```

## 📊 Level 8: Usage Tracking (45 minutes)

### Monitor Usage

```bash
# View all usage
cdc usage

# Last 7 days
cdc usage --days 7

# By API
cdc usage --api personal
cdc usage --api client

# Shows:
# - Total tokens used
# - Cost estimates
# - Breakdown by model
# - Usage by date
```

## 🔁 Level 9: Conversation History (50 minutes)

### Save and Resume Conversations

```bash
# Interactive mode with history
cdc interactive

# Continue previous conversation
cdc interactive --continue

# Don't save history (private session)
cdc interactive --no-save
```

### Manage History

```bash
# List conversations
cdc history list

# Search conversations
cdc history list -s "python decorators"

# Export conversation
cdc history export <conversation-id> -o conversation.md
cdc history export <conversation-id> -o conversation.json
```

## 🚀 Level 10: Advanced Patterns (60+ minutes)

### Combine Everything

```bash
# Context-aware interactive review with template
cdc template use code-review
# Then provide context-rich input

# Workflow with auto-context steps
cdc workflow run smart-review.yaml -v file=app.py -v use_context=true

# Multi-step development workflow
cdc workflow run feature-development.yaml \
  -v feature=authentication \
  -v test_framework=pytest \
  -v api=client
```

### Shell Completion

```bash
# Install completion
cdc completion install

# Now use tab completion
cdc revi<TAB>  # completes to 'review'
cdc template li<TAB>  # completes to 'list'
```

### TOON Format (Token Optimization)

```bash
# Check if installed
cdc toon info

# Convert large JSON files
cat data.json | cdc toon encode | cdc ask "analyze this data"

# Saves 30-60% on tokens = lower costs
```

## 📚 Example Workflows for Common Tasks

### 1. Code Review Workflow

```bash
# Quick review
cdc review src/api.py

# Thorough review with context
cdc review src/api.py --auto-context --interactive

# Follow-up questions:
# - "Are there security issues?"
# - "How's the performance?"
# - "What about error handling?"
```

### 2. Bug Fix Workflow

```bash
# Run and capture error
python app.py 2>&1 | cdc debug --auto-context

# Get fix suggestions with full context
# Apply fixes

# Generate tests for the fix
cdc generate tests app.py --interactive

# Commit
git add .
cdc git commit
```

### 3. Feature Development Workflow

```bash
# Write initial code
vim src/new_feature.py

# Review
cdc review src/new_feature.py --auto-context

# Refactor based on suggestions
cdc refactor src/new_feature.py --interactive

# Generate tests
cdc generate tests src/new_feature.py -o tests/test_new_feature.py

# Generate docs
cdc generate docs src/new_feature.py

# Commit
git add .
cdc git commit
```

### 4. Refactoring Legacy Code

```bash
# Initial review
cdc review legacy/old_code.py --auto-context

# Get refactoring plan
cdc ask -f legacy/old_code.py --auto-context \
  "create a refactoring plan with steps"

# Refactor interactively
cdc refactor legacy/old_code.py --interactive

# Generate tests for refactored code
cdc generate tests legacy/old_code.py --interactive

# Verify with workflow
cdc workflow run refactor-and-verify.yaml -v file=legacy/old_code.py
```

## 🎓 Pro Tips

1. **Use `--auto-context` for complex questions** - It provides much better answers
2. **Create project-specific `.claude-dev-cli` configs** - Saves time and uses correct APIs
3. **Use templates for repetitive tasks** - Consistency and speed
4. **Leverage workflows for multi-step processes** - Automation and reliability
5. **Enable shell completion** - Faster command entry
6. **Use interactive mode for exploration** - Great for learning new concepts
7. **Monitor usage per API** - Track costs per project/client
8. **Export conversations** - Documentation and knowledge sharing

## 📖 Next Steps

- Read `CONTRIBUTING.md` for development guidelines
- Check `examples/` directory for more workflow examples
- Review `ROADMAP.md` for upcoming features
- Visit https://pypi.org/project/claude-dev-cli/ for latest version

## 🆘 Getting Help

```bash
# Command help
cdc --help
cdc review --help
cdc workflow --help

# Check version
cdc --version

# View usage
cdc usage
```

## 🔗 Resources

- **PyPI**: https://pypi.org/project/claude-dev-cli/
- **GitHub**: https://github.com/thinmanj/claude-dev-cli
- **Issues**: https://github.com/thinmanj/claude-dev-cli/issues
