# Basic Usage Examples

This directory contains simple examples to get you started with Claude Dev CLI.

## Prerequisites

```bash
# Install claude-dev-cli
pip install claude-dev-cli

# Set up your API key
export PERSONAL_ANTHROPIC_API_KEY="sk-ant-..."
cdc config add personal --default
```

## Example 1: Simple Question

Ask Claude a quick question:

```bash
cdc ask "explain Python decorators in simple terms"
```

## Example 2: Question with File Context

Get help with a specific file:

```bash
# Create a sample file
cat > calculator.py << 'EOF'
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
EOF

# Ask about the file
cdc ask -f calculator.py "How can I improve this code?"
```

## Example 3: Piping Input

Analyze error output directly:

```bash
# Run a script and pipe errors to Claude
python buggy_script.py 2>&1 | cdc ask "what's causing this error?"

# Or analyze command output
git --no-pager log --oneline -10 | cdc ask "summarize these commits"
```

## Example 4: Interactive Mode

Have a conversation with Claude:

```bash
cdc interactive
```

In interactive mode:
- Type your questions naturally
- Type `exit` or `quit` to end
- Conversation history is maintained during the session

## Example 5: Using Different Models

```bash
# Use a faster, cheaper model
cdc ask -m claude-3-haiku-20240307 "quick question: what is 2+2?"

# Use the most powerful model
cdc ask -m claude-3-opus-20240229 "complex architectural question..."
```

## Example 6: Custom System Prompts

```bash
# Act as a specific expert
cdc ask -s "You are a security expert" "review this authentication code"

# Act as a teacher
cdc ask -s "You are a patient teacher for beginners" -f code.py "explain this code"
```

## Example 7: Saving Output

```bash
# Save response to file
cdc ask "write a Python quicksort implementation" > quicksort.py

# Or use the -o flag (for supported commands)
cdc generate docs mymodule.py -o docs.md
```

## Tips

1. **Be Specific**: More detailed questions get better answers
2. **Provide Context**: Use `-f` to include relevant files
3. **Use Streaming**: Default streaming shows responses in real-time
4. **Check Usage**: Run `cdc usage` to monitor your API costs

## Next Steps

- Check out [Multi-API Routing](../multi_api_routing/) for managing multiple API keys
- See [Developer Workflows](../developer_workflows/) for advanced development tasks
- Learn about [TOON Format](../toon_format/) for reducing token usage
