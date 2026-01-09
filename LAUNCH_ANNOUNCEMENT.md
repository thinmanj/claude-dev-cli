# Launch Announcement Templates

Use these templates to announce claude-dev-cli on various platforms.

---

## Twitter/X

```
🎉 claude-dev-cli v0.8.3 - AI dev assistant with Claude API

✨ Multi-API routing for teams/clients
✨ Auto code review & test generation
✨ Context intelligence
✨ Conversation summarization (30-50% cost savings)
✨ 257 tests passing

🍺 brew install thinmanj/tap/claude-dev-cli

https://github.com/thinmanj/claude-dev-cli

#AI #DevTools #CLI #Claude
```

---

## LinkedIn

```
🚀 Launching claude-dev-cli: AI-Powered Development Assistant

I'm excited to share claude-dev-cli v0.8.3, a professional CLI tool for developers using Claude AI.

🔑 Key Features:
• Multi-API Key Management: Route tasks between personal, client, and enterprise API keys
• Developer Workflows: Code review, test generation, debugging, refactoring
• Context Intelligence: Automatically gathers git history, dependencies, and related files
• Conversation Summarization: 30-50% cost reduction in long conversations
• Multi-Language Support: Parse errors in Python, JavaScript, Go, Rust, and Java
• Cost Control: Track usage and costs per API key

📦 Easy Installation:
brew install thinmanj/tap/claude-dev-cli
pip install claude-dev-cli

🧪 Battle-Tested:
257 tests passing, fully documented, MIT licensed

Perfect for:
✓ Freelancers managing multiple client projects
✓ Teams wanting AI-powered code reviews
✓ Developers seeking intelligent debugging assistance
✓ Anyone wanting to track AI API costs

Check it out: https://github.com/thinmanj/claude-dev-cli

#SoftwareDevelopment #AI #DeveloperTools #Python #Claude #OpenSource
```

---

## Hacker News (Show HN)

**Title:**
```
Show HN: claude-dev-cli – AI-powered CLI for code review, testing, and debugging
```

**Post:**
```
Hi HN!

I built claude-dev-cli, a CLI tool for developers using Claude AI with some unique features I haven't seen elsewhere.

What makes it different:

1. Multi-API routing: Manage multiple Claude API keys (personal/client/enterprise) and automatically route commands to the right one based on project config. Great for freelancers/agencies.

2. Context intelligence: Automatically gathers relevant context (git history, dependencies, related files) before sending to the API. Uses configurable size limits to avoid token waste.

3. Multi-language error parsing: Parses stack traces from Python, JavaScript, Go, Rust, and Java to extract precise file locations and context.

4. Developer workflows: Built-in commands for code review, test generation, debugging, refactoring, and git commit messages.

5. Cost tracking: Every API call is logged with token usage and cost estimates, filterable by API key and date.

Technical details:
- Python 3.9+, fully typed with mypy
- 257 tests passing
- Secure key storage (system keyring)
- Conversation summarization (30-50% cost reduction)
- MIT licensed

Installation:
  brew install thinmanj/tap/claude-dev-cli
  pip install claude-dev-cli

The market research showed most Claude CLI tools are basic wrappers, while this is focused on real developer workflows with professional features like multi-API routing and usage tracking.

Would love feedback from the community!

GitHub: https://github.com/thinmanj/claude-dev-cli
PyPI: https://pypi.org/project/claude-dev-cli/
```

---

## Reddit - r/Python

**Title:**
```
[P] claude-dev-cli: AI-powered CLI for code review, testing, and debugging with Claude API
```

**Post:**
```
Hey r/Python!

I've been working on `claude-dev-cli`, a CLI tool for developers using Claude AI. It's designed for real development workflows rather than just being a chat wrapper.

**Key Features:**

🔑 **Multi-API Key Management**
- Route tasks to different Claude API keys (personal/client/enterprise)
- Automatic API selection based on project config
- Secure storage in system keyring
- Perfect for freelancers managing multiple clients

🧪 **Developer Commands**
- `cdc review` - Code reviews with security/performance checks
- `cdc generate tests` - Automatic pytest test generation
- `cdc debug` - Error analysis with multi-language parsing
- `cdc refactor` - Refactoring suggestions
- `cdc git commit` - Generate conventional commit messages

🧠 **Context Intelligence**
- `--auto-context` flag automatically gathers:
  - Git history and modified files
  - Dependencies from requirements.txt
  - Related files through import analysis
- Smart truncation to avoid token limits
- Preview context with `cdc context summary`

📊 **Usage Tracking**
- Every API call logged with tokens and cost
- Filter by date range and API key
- Track spending across projects

🔧 **Multi-Language Support**
- Parse errors from Python, JavaScript/TypeScript, Go, Rust, Java
- Extract precise file locations and stack traces
- Language auto-detection

**Installation:**
```bash
# Via Homebrew
brew install thinmanj/tap/claude-dev-cli

# Via pip
pip install claude-dev-cli

# Via pipx (recommended)
pipx install claude-dev-cli
```

**Example Usage:**
```bash
# Code review with context
cdc review mymodule.py --auto-context

# Debug with error parsing
python broken.py 2>&1 | cdc debug --auto-context

# Generate tests
cdc generate tests mymodule.py -o tests/test_mymodule.py
```

**Technical Details:**
- Python 3.9+
- Fully typed with mypy
- 257 tests passing
- Conversation summarization (30-50% cost reduction)
- MIT licensed
- Docs: [QUICKSTART.md](https://github.com/thinmanj/claude-dev-cli/blob/master/QUICKSTART.md)

GitHub: https://github.com/thinmanj/claude-dev-cli
PyPI: https://pypi.org/project/claude-dev-cli/

Happy to answer any questions!
```

---

## Reddit - r/commandline

**Title:**
```
claude-dev-cli: AI-powered development assistant with multi-API routing and context intelligence
```

**Post:**
```
Hey r/commandline!

Built a CLI tool for developers using Claude AI. Unlike basic chat wrappers, this focuses on developer workflows.

**Unique Features:**

🔑 Multi-API routing
- Manage multiple Claude API keys
- Auto-route based on project
- Great for consultants

🧠 Smart context
- `--auto-context` auto-gathers git/deps/files
- Preview with `cdc context summary`
- Configurable size limits

📊 Cost tracking
- Log every API call
- Track tokens & costs
- Filter by key/date

**Commands:**
- `cdc review` - Code review
- `cdc debug` - Error analysis (multi-language)
- `cdc generate tests` - Test generation
- `cdc git commit` - Commit messages
- `cdc ask` - Quick questions

**Install:**
```bash
brew install thinmanj/tap/claude-dev-cli
pip install claude-dev-cli
```

257 tests | MIT | Docs: https://github.com/thinmanj/claude-dev-cli

Feedback welcome!
```

---

## Dev.to Article

**Title:**
```
Building an AI-Powered CLI for Developers: claude-dev-cli
```

**Opening:**
```markdown
# Building an AI-Powered CLI for Developers: claude-dev-cli

After using various Claude API wrappers and finding them too basic, I built `claude-dev-cli` - a professional CLI tool focused on real developer workflows.

## The Problem

Most AI CLI tools are just chat wrappers. As a developer working with multiple clients, I needed:
- Multi-API key management (personal vs client keys)
- Context-aware operations (git, dependencies, related files)
- Cost tracking per project
- Developer-specific commands (review, test, debug)

## The Solution

`claude-dev-cli` is a Python CLI that addresses these needs:

### 1. Multi-API Key Management

```bash
# Add personal and client keys
cdc config add personal --default
cdc config add client

# Projects automatically use the right key
cd ~/client-project  # Uses client key
cd ~/personal-project  # Uses personal key
```

[Continue with examples, architecture, implementation details...]

## Try It Out

```bash
brew install thinmanj/tap/claude-dev-cli
pip install claude-dev-cli
```

GitHub: https://github.com/thinmanj/claude-dev-cli

## Discussion

What features would you find useful in an AI-powered CLI? Let me know in the comments!
```

---

## Product Hunt

**Tagline:**
```
AI-powered CLI for code review, testing, and debugging with multi-API routing
```

**Description:**
```
claude-dev-cli is a professional CLI tool for developers using Claude AI, designed for real development workflows.

🔑 Multi-API Key Management
Route tasks to different API keys (personal/client/enterprise) with automatic project-based selection.

🧪 Developer Workflows
Built-in commands for code review, test generation, debugging, refactoring, and git commit messages.

🧠 Context Intelligence
Automatically gathers git history, dependencies, and related files with smart truncation.

📊 Cost Tracking
Track API usage and costs per project with detailed breakdowns.

🌐 Multi-Language Support
Parse errors from Python, JavaScript, Go, Rust, and Java with precise stack trace extraction.

Perfect for freelancers, agencies, and development teams who want professional AI tooling.

257 tests passing | MIT License | Available via Homebrew and pip
```

**First Comment:**
```
👋 Maker here!

I built claude-dev-cli because existing Claude CLI tools were too basic. As a developer managing multiple client projects, I needed:
- Multi-API routing (don't mix personal and client usage)
- Context intelligence (auto-gather relevant files)
- Cost tracking (know what you're spending)
- Real dev commands (not just chat)

The tool has 257 tests and is battle-tested across multiple projects.

Would love your feedback! What features would make this more useful for your workflow?

Install: brew install thinmanj/tap/claude-dev-cli
```

---

## Discord/Slack Communities

```
🎉 New Tool: claude-dev-cli

AI-powered CLI for developers with some unique features:

✨ Multi-API routing (personal/client keys)
✨ Context intelligence (auto-gathers git/deps/files)  
✨ Conversation summarization (30-50% cost savings)
✨ Multi-language error parsing
✨ Usage & cost tracking
✨ 257 tests passing

Install: `brew install thinmanj/tap/claude-dev-cli`

GitHub: https://github.com/thinmanj/claude-dev-cli

Happy to answer questions!
```

---

## Tips for Posting

1. **Timing:** Post on weekdays, mid-morning (10am-12pm) in target timezone
2. **Hacker News:** Tuesday-Thursday are best days
3. **Reddit:** Check each subreddit's rules about self-promotion
4. **Engage:** Respond to all comments within first few hours
5. **Cross-post:** Wait 24-48 hours between platforms
6. **Track:** Use GitHub traffic stats to see what works

Good luck with the launch! 🚀
