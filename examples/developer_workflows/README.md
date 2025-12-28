# Developer Workflow Examples

Common development workflows using Claude Dev CLI.

## Workflow 1: Test-Driven Development

```bash
# 1. Write your function
cat > math_utils.py << 'EOF'
def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
EOF

# 2. Generate comprehensive tests
cdc generate tests math_utils.py -o test_math_utils.py

# 3. Run tests to verify they work
pytest test_math_utils.py

# 4. If tests fail, debug
pytest test_math_utils.py 2>&1 | cdc debug
```

## Workflow 2: Code Review Before Commit

```bash
# 1. Make your changes
# ... edit files ...

# 2. Review your code
cdc review app.py

# 3. Make improvements based on feedback
# ... fix issues ...

# 4. Stage changes
git add app.py

# 5. Generate commit message
cdc git commit

# 6. Use the suggested message
git commit -m "feat: add user authentication

Implemented JWT-based authentication with password hashing.
Added login and logout endpoints with proper error handling.
Includes comprehensive input validation.

Co-Authored-By: Warp <agent@warp.dev>"
```

## Workflow 3: Debugging Production Errors

```bash
# 1. Capture error from logs
tail -50 /var/log/app/error.log > recent_errors.txt

# 2. Debug with Claude
cdc debug -f app.py < recent_errors.txt

# 3. Get specific analysis
cat recent_errors.txt | cdc ask "What's the root cause of this error and how can I fix it?"

# 4. Test the fix
cdc ask -f app.py "review this fix for the database connection error"
```

## Workflow 4: Refactoring Legacy Code

```bash
# 1. Review legacy code
cdc review legacy_module.py

# 2. Get refactoring suggestions
cdc refactor legacy_module.py -o refactored_module.py

# 3. Review changes
diff legacy_module.py refactored_module.py

# 4. Generate tests for refactored code
cdc generate tests refactored_module.py -o test_refactored.py

# 5. Run tests to ensure behavior unchanged
pytest test_refactored.py
```

## Workflow 5: Documentation Generation

```bash
# 1. Generate docstrings and module docs
cdc generate docs my_module.py -o docs/my_module.md

# 2. Generate README for whole project
cdc ask "Generate a README.md for this project" \
  -f src/main.py \
  -f src/utils.py \
  -f setup.py > README.md

# 3. Generate API documentation
find src/ -name "*.py" -exec cdc generate docs {} \; > docs/API.md
```

## Workflow 6: Feature Development

```bash
# 1. Plan the feature
cdc ask -f requirements.txt "I need to add user authentication. What's the best approach?"

# 2. Generate boilerplate
cdc ask "Generate a Flask authentication blueprint with JWT support" > auth.py

# 3. Review generated code
cdc review auth.py

# 4. Generate tests
cdc generate tests auth.py -o test_auth.py

# 5. Review everything before committing
git add auth.py test_auth.py
cdc git commit
```

## Workflow 7: Learning New Codebase

```bash
# 1. Get overview of main module
cdc ask -f src/main.py "Explain what this module does and its key components"

# 2. Understand complex function
cdc ask -f src/algorithm.py "Explain this algorithm step by step"

# 3. Identify dependencies
cdc ask -f requirements.txt "What are these dependencies used for?"

# 4. Generate architecture documentation
cdc ask "Create an architecture diagram in mermaid format" \
  -f src/main.py \
  -f src/models.py \
  -f src/api.py > architecture.md
```

## Workflow 8: Security Audit

```bash
# 1. Review for security issues
cdc ask -s "You are a security expert" -f auth.py \
  "Audit this code for security vulnerabilities"

# 2. Check for common vulnerabilities
cdc ask -f app.py "Check for SQL injection, XSS, and CSRF vulnerabilities"

# 3. Review dependencies
cdc ask -f requirements.txt "Are there any known vulnerabilities in these packages?"

# 4. Get security recommendations
cdc ask "What security best practices should I implement for this Flask app?" \
  -f app.py
```

## Workflow 9: Performance Optimization

```bash
# 1. Identify bottlenecks
cdc ask -f slow_function.py "What are the performance bottlenecks in this code?"

# 2. Get optimization suggestions
cdc refactor slow_function.py

# 3. Compare approaches
cdc ask "Compare these two implementations for performance" \
  -f approach1.py \
  -f approach2.py

# 4. Generate benchmarks
cdc ask -f optimized.py "Generate pytest benchmarks to test performance"
```

## Workflow 10: Error Recovery

```bash
# 1. Run failing test and capture output
pytest test_feature.py -v 2>&1 | tee test_output.txt

# 2. Get Claude's analysis
cdc debug < test_output.txt

# 3. Get specific fix
cdc ask -f src/feature.py \
  -e "$(cat test_output.txt)" \
  "Provide the exact code fix for this test failure"

# 4. Verify fix
pytest test_feature.py -v
```

## Tips for Effective Workflows

### 1. Use Specific System Prompts
```bash
# For testing
cdc generate tests app.py -s "You are a testing expert focused on edge cases and error handling"

# For security
cdc review auth.py -s "You are a security auditor looking for vulnerabilities"

# For performance
cdc refactor slow.py -s "You are a performance optimization expert"
```

### 2. Chain Commands
```bash
# Review, then generate tests if approved
cdc review new_feature.py && cdc generate tests new_feature.py -o test_new_feature.py
```

### 3. Save Common Prompts
```bash
# Create alias for common workflow
alias review-and-commit='cdc review $1 && git add $1 && cdc git commit'

# Use it
review-and-commit app.py
```

### 4. Monitor API Usage
```bash
# Check usage before expensive operations
cdc usage --days 1

# Use cheaper model for simple tasks
cdc ask -m claude-3-haiku-20240307 "simple question"
```

## Integration with Other Tools

### With Pre-commit Hooks
```bash
# .git/hooks/pre-commit
#!/bin/bash
# Review staged Python files
git diff --cached --name-only --diff-filter=ACM | grep ".py$" | while read file; do
  echo "Reviewing $file..."
  cdc review "$file"
done
```

### With CI/CD
```bash
# In your CI pipeline
cdc review src/**/*.py > review_report.txt
# Fail if critical issues found
grep -i "critical\|security" review_report.txt && exit 1
```

### With Git Hooks
```bash
# Generate commit message automatically
git add .
GIT_MESSAGE=$(cdc git commit)
git commit -m "$GIT_MESSAGE"
```

## Next Steps

- Explore [TOON Format](../toon_format/) to reduce API costs
- Check [Basic Usage](../basic_usage/) for fundamental commands
- Review [Multi-API Routing](../multi_api_routing/) for managing multiple keys
