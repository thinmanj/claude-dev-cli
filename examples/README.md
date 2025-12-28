# Claude Dev CLI Examples

This directory contains practical examples and tutorials for using Claude Dev CLI effectively.

## Directory Structure

### [basic_usage/](basic_usage/)
Simple examples to get started:
- Single questions
- File context
- Piping input
- Interactive mode
- Custom system prompts
- Saving output

**Start here if you're new to Claude Dev CLI!**

### [multi_api_routing/](multi_api_routing/)
Managing multiple API keys:
- Personal vs client API keys
- Project-specific configurations
- API routing hierarchy
- Usage tracking by API
- Best practices for client work

**Essential for consultants and contractors!**

### [developer_workflows/](developer_workflows/)
Real-world development workflows:
- Test-driven development
- Code review workflows
- Debugging production errors
- Refactoring legacy code
- Documentation generation
- Security audits
- Performance optimization

**Power user techniques for daily development!**

### [toon_format/](toon_format/)
Reducing token usage by 30-60%:
- JSON to TOON conversion
- Cost savings examples
- Real-world scenarios
- Performance metrics
- Integration patterns

**Save money on API costs with large datasets!**

## Quick Start

1. **Install**
   ```bash
   pip install claude-dev-cli
   ```

2. **Configure**
   ```bash
   export PERSONAL_ANTHROPIC_API_KEY="sk-ant-..."
   cdc config add personal --default
   ```

3. **Try Basic Examples**
   ```bash
   cd basic_usage/
   # Follow the README
   ```

4. **Explore Workflows**
   ```bash
   cd developer_workflows/
   # Try the workflows relevant to your work
   ```

## Common Use Cases

### Quick Help
```bash
cdc ask "how do I parse JSON in Python?"
```

### Code Review
```bash
cdc review mycode.py
```

### Generate Tests
```bash
cdc generate tests mymodule.py -o test_mymodule.py
```

### Debug Errors
```bash
python buggy.py 2>&1 | cdc debug
```

### Git Commit Messages
```bash
git add .
cdc git commit
```

## Tips

1. **Start Simple**: Begin with [basic_usage/](basic_usage/) examples
2. **Use File Context**: Include relevant files with `-f` flag
3. **Save Costs**: Use [toon_format/](toon_format/) for large data
4. **Monitor Usage**: Run `cdc usage` to track API costs
5. **Be Specific**: More detailed prompts = better results

## Need Help?

- Check [CONTRIBUTING.md](../CONTRIBUTING.md) for development setup
- View [README.md](../README.md) for full documentation
- Open an issue on GitHub for questions

## Contributing Examples

Have a useful workflow? Submit a PR with:
1. Clear README with step-by-step instructions
2. Sample files (if needed)
3. Expected outputs
4. Tips and best practices

---

**Happy coding with Claude Dev CLI!** 🚀
