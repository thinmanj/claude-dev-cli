# Multi-API Routing Examples

This directory shows how to manage multiple Claude API keys for different purposes (personal, client, enterprise).

## Scenario: Client Work with Enterprise API

You're working on a client project and need to use their Enterprise API key while keeping your personal API key for your own projects.

### Step 1: Set Up Multiple API Keys

```bash
# Add your personal API key
export PERSONAL_ANTHROPIC_API_KEY="sk-ant-personal-..."
cdc config add personal --default --description "My personal API key"

# Add client's API key
export CLIENT_ANTHROPIC_API_KEY="sk-ant-client-..."
cdc config add client --description "Client's Enterprise API"

# Verify both are configured
cdc config list
```

### Step 2: Create Project-Specific Configuration

```bash
# Navigate to client project
cd /path/to/client/project

# Create project config file
cat > .claude-dev-cli << 'EOF'
{
  "name": "Client Project Alpha",
  "api_config": "client",
  "system_prompt": "You are a senior Python developer working on financial systems. Always prioritize security and data integrity.",
  "allowed_commands": ["all"]
}
EOF
```

### Step 3: Use Commands Automatically

Now all commands in this directory automatically use the client's API:

```bash
# All these use client's API
cdc generate tests app.py
cdc review security.py
cdc debug -f payment_processor.py
```

### Step 4: Your Personal Projects

In your personal project directories without `.claude-dev-cli`:

```bash
cd ~/my-personal-project

# These use your personal API (the default)
cdc ask "help me with this code"
cdc generate tests my_module.py
```

### Step 5: Explicit Override

Override project settings with the `-a` flag:

```bash
# In client project, but use your personal API
cdc ask -a personal "quick question about Python syntax"
```

## Usage Tracking by API

Track usage separately for each API:

```bash
# View all usage
cdc usage

# View only client API usage
cdc usage --api client

# View only your personal usage
cdc usage --api personal

# Last 7 days of client usage
cdc usage --api client --days 7
```

## Example Project Structure

```
client-project/
├── .claude-dev-cli          # Routes to client API
├── src/
│   ├── main.py
│   └── utils.py
└── tests/

personal-project/
├── (no .claude-dev-cli)     # Uses default (personal) API
├── src/
│   └── app.py
└── README.md
```

## API Routing Priority

Claude Dev CLI uses this priority order:

1. **Explicit `-a` flag**: `cdc ask -a client "question"`
2. **Project config**: `.claude-dev-cli` file in current/parent directories
3. **Default API**: API marked as default in global config
4. **First configured**: First API in config if no default set

## What the Client Can See

When using a client's Enterprise API:

### ✅ They CAN see:
- Total API calls made with their key
- Token usage and costs
- Potentially conversation history (if enabled by admin)

### ❌ They CANNOT see:
- Your machine details or identity
- Your other API keys or projects
- Local file contents (unless you send them in prompts)
- Your personal API usage

## Best Practices

1. **Separate Work Clearly**: Use project configs for all client work
2. **Check Before Commands**: Run `cdc config list` to see active configuration
3. **Monitor Usage**: Regularly check `cdc usage --api client` to track costs
4. **Sanitize Prompts**: Don't include client-sensitive data in prompts
5. **Document Configuration**: Add `.claude-dev-cli` to version control (without sensitive data)

## Troubleshooting

### Wrong API Being Used

```bash
# Check which API will be used
cd /path/to/project
cdc config list  # Look for (default) marker

# Check for project config
ls -la .claude-dev-cli

# Force specific API
cdc ask -a personal "test question"
```

### API Key Not Found

```bash
# Check environment variables
echo $PERSONAL_ANTHROPIC_API_KEY
echo $CLIENT_ANTHROPIC_API_KEY

# Re-add API config
cdc config add personal --api-key "sk-ant-..."
```

### Project Config Not Working

```bash
# Verify JSON syntax
cat .claude-dev-cli | python -m json.tool

# Check file is in project root
pwd
ls .claude-dev-cli
```

## Sample .claude-dev-cli Files

### For Client Project
```json
{
  "name": "Client Project",
  "api_config": "client",
  "system_prompt": "You are a senior developer specializing in fintech.",
  "allowed_commands": ["all"]
}
```

### For Personal Side Project
```json
{
  "name": "My Experimental Project",
  "api_config": "personal",
  "system_prompt": "You are a creative coding assistant who encourages experimentation.",
  "allowed_commands": ["all"]
}
```

### For Team Project (Shared Config)
```json
{
  "name": "Team Project - Marketing Platform",
  "api_config": "team",
  "system_prompt": "You are a full-stack developer working on a Django/React application. Follow PEP 8 and Airbnb JavaScript style guides.",
  "allowed_commands": ["generate", "review", "refactor"]
}
```
