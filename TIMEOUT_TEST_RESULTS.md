# Timeout Configuration Test Results

## Problem
Previously, Ollama requests would timeout at 120 seconds when:
- Using complex prompts
- Processing large documents
- Running on resource-constrained servers
- Using larger models like qwen2.5-coder

## Solution
Added configurable timeout parameter with increased default:
- **New default**: 300 seconds (5 minutes) - up from 120s
- **Configurable**: Can be set per provider config
- **Flexible**: Different timeouts for different use cases

## Test Results

### Before Fix (120s timeout)
```bash
# Calculator spec with qwen2.5-coder
cat test_calculator.md | cdc ask -a local -m qwen2.5-coder:latest "..."
❌ Error: HTTPConnectionPool(host='192.168.88.219', port=11434): Read timed out. (read timeout=120)

# Inventory spec with qwen2.5-coder  
cat test_inventory_system.md | cdc ask -a local -m qwen2.5-coder:latest "..."
❌ Error: HTTPConnectionPool(host='192.168.88.219', port=11434): Read timed out. (read timeout=120)
```

### After Fix (300s default, 600s configured)

#### Test 1: Calculator Spec with qwen2.5-coder
```bash
cat test_calculator.md | cdc ask -a local -m qwen2.5-coder:latest \
  "Read this specification and generate the calculator.py file with all four functions and proper error handling."
```

✅ **Success** - Generated complete calculator.py with:
- `add(a, b) -> float`
- `subtract(a, b) -> float`
- `multiply(a, b) -> float`
- `divide(a, b) -> float` with ValueError for division by zero
- Proper type hints and error handling

#### Test 2: Inventory System Spec with qwen2.5-coder
```bash
cat test_inventory_system.md | cdc ask -a local -m qwen2.5-coder:latest \
  "Read this project specification and create the Product class from the models.py file with all fields and validation mentioned in the spec."
```

✅ **Success** - Generated complete Product dataclass with:
- All fields (sku, name, category, price, quantity, min_quantity, created_at, updated_at)
- @dataclass decorator with frozen=True
- Validation in __post_init__ method
- from_dict() and to_dict() methods
- update_product() method
- is_below_min_quantity property
- Comprehensive error handling

Response time: ~2-3 minutes (well within 300s default timeout)

## Configuration Methods

### Method 1: CLI (Recommended)
```bash
# Add new config with custom timeout
cdc config add ollama local --base-url http://192.168.88.219:11434 --timeout 600

# For extremely slow servers or large models
cdc config add ollama slow-server --base-url http://server:11434 --timeout 900
```

### Method 2: Manual Config Edit
Edit `~/.claude-dev-cli/config.json`:
```json
{
  "api_configs": [
    {
      "name": "local",
      "provider": "ollama",
      "base_url": "http://192.168.88.219:11434",
      "timeout": 600
    }
  ]
}
```

## Timeout Recommendations

### By Model Size
- **Small models** (1-7B): 120-180 seconds
- **Medium models** (7-13B): 180-300 seconds
- **Large models** (13-30B): 300-600 seconds
- **Very large models** (70B+): 600-900 seconds

### By Use Case
- **Simple queries**: 120-180 seconds
- **Code generation**: 180-300 seconds
- **Large documents**: 300-600 seconds
- **Complex analysis**: 600-900 seconds

### By Server Resources
- **High-end workstation**: Use defaults
- **Mid-range server**: Add 50-100%
- **Low-resource server**: Add 100-200%
- **Shared/busy server**: Add 200-300%

## Summary

✅ **Problem Solved**: Timeouts no longer occur with default settings
✅ **Configurable**: Can adjust per server/model needs
✅ **Tested**: Both simple and complex prompts work
✅ **Documented**: Clear guidance on when to increase timeout
✅ **Backward Compatible**: Existing configs work, defaults improved

## Implementation Details

**Files Modified:**
- `src/claude_dev_cli/config.py` - Added timeout field to APIConfig/ProviderConfig
- `src/claude_dev_cli/providers/ollama.py` - Use config timeout (default 300s)
- `src/claude_dev_cli/cli.py` - Added --timeout option to config add

**Commit:** 736f594
**Tests:** All 337 tests passing
**Version:** 0.19.0+
