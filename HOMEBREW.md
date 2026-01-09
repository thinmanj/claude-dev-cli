# Homebrew Distribution Guide

This guide explains how to set up and maintain the Homebrew tap for `claude-dev-cli`.

## What is a Homebrew Tap?

A Homebrew "tap" is a third-party repository of formula files. Users can add your tap to their Homebrew installation and install your formula like any official Homebrew package.

## Setup Instructions

### 1. Create GitHub Repository

Create a new GitHub repository named `homebrew-tap` under your account (thinmanj):
- Repository name: `homebrew-tap` (must start with "homebrew-")
- Description: "Homebrew formulae for claude-dev-cli"
- Public repository
- Initialize with README

### 2. Populate Repository

Copy the contents from the local tap:

```bash
# Navigate to local tap directory
cd /opt/homebrew/Library/Taps/thinmanj/homebrew-tap

# Add remote and push
git remote add origin https://github.com/thinmanj/homebrew-tap.git
git push -u origin main
```

### 3. Copy Formula File

Ensure the formula file is in the repository:

```bash
cp /Volumes/Projects/claude-dev-cli/Formula/claude-dev-cli.rb /opt/homebrew/Library/Taps/thinmanj/homebrew-tap/Formula/claude-dev-cli.rb
cd /opt/homebrew/Library/Taps/thinmanj/homebrew-tap
git add Formula/claude-dev-cli.rb
git commit -m "feat: add claude-dev-cli formula

Co-Authored-By: Warp <agent@warp.dev>"
git push
```

## User Installation

Once the tap is published on GitHub, users can install with:

```bash
# Add the tap
brew tap thinmanj/tap

# Install claude-dev-cli
brew install claude-dev-cli
```

Or in one command:

```bash
brew install thinmanj/tap/claude-dev-cli
```

## Updating the Formula

When you release a new version:

1. **Update pyproject.toml and __init__.py** with new version number

2. **Build and publish to PyPI**
   ```bash
   python3 -m build
   twine upload dist/claude_dev_cli-X.Y.Z*
   ```

3. **Get new SHA256**
   ```bash
   curl -sL https://pypi.org/pypi/claude-dev-cli/json | \
     python3 -c "import sys, json; data = json.load(sys.stdin); \
     [print(f'URL: {f[\"url\"]}\nSHA256: {f[\"digests\"][\"sha256\"]}') \
     for f in data['urls'] if f['packagetype'] == 'sdist']"
   ```

4. **Update Formula/claude-dev-cli.rb**
   - Update `url` with new PyPI URL
   - Update `sha256` with new hash
   - Remove `version` line (Homebrew will auto-detect from URL)

5. **Test locally**
   ```bash
   # If already installed, uninstall first
   brew uninstall claude-dev-cli
   
   # Test the updated formula
   brew install --build-from-source thinmanj/tap/claude-dev-cli
   
   # Verify it works
   cdc --version
   cdc --help
   ```

6. **Commit and push**
   ```bash
   cd /opt/homebrew/Library/Taps/thinmanj/homebrew-tap
   git add Formula/claude-dev-cli.rb
   git commit -m "feat: update claude-dev-cli to vX.Y.Z
   
   Co-Authored-By: Warp <agent@warp.dev>"
   git push
   ```

## Formula Template for New Versions

```ruby
class ClaudeDevCli < Formula
  include Language::Python::Virtualenv

  desc "AI-powered CLI tool for developers using Claude API with multi-API routing"
  homepage "https://github.com/thinmanj/claude-dev-cli"
  url "https://files.pythonhosted.org/packages/XX/YY/HASH/claude_dev_cli-X.Y.Z.tar.gz"
  sha256 "NEW_SHA256_HASH"
  license "MIT"

  depends_on "python@3.11"

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "Usage:", shell_output("#{bin}/cdc --help")
  end
end
```

## Automated Release Script

For convenience, here's a script to automate formula updates:

```bash
#!/bin/bash
# update-homebrew-formula.sh

VERSION="$1"

if [ -z "$VERSION" ]; then
    echo "Usage: ./update-homebrew-formula.sh X.Y.Z"
    exit 1
fi

# Get SHA256 from PyPI
echo "Fetching SHA256 for version ${VERSION}..."
SHA_INFO=$(curl -sL https://pypi.org/pypi/claude-dev-cli/json | \
  python3 -c "import sys, json; data = json.load(sys.stdin); \
  [print(f'{f[\"url\"]}|{f[\"digests\"][\"sha256\"]}') \
  for f in data['urls'] if f['packagetype'] == 'sdist']")

URL=$(echo "$SHA_INFO" | cut -d'|' -f1)
SHA256=$(echo "$SHA_INFO" | cut -d'|' -f2)

echo "URL: $URL"
echo "SHA256: $SHA256"

# Update formula
TAP_DIR="/opt/homebrew/Library/Taps/thinmanj/homebrew-tap"
FORMULA="$TAP_DIR/Formula/claude-dev-cli.rb"

# Create updated formula
cat > "$FORMULA" <<EOF
class ClaudeDevCli < Formula
  include Language::Python::Virtualenv

  desc "AI-powered CLI tool for developers using Claude API with multi-API routing"
  homepage "https://github.com/thinmanj/claude-dev-cli"
  url "$URL"
  sha256 "$SHA256"
  license "MIT"

  depends_on "python@3.11"

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "Usage:", shell_output("#{bin}/cdc --help")
  end
end
EOF

echo "✓ Formula updated"

# Test installation
echo "Testing installation..."
brew uninstall claude-dev-cli 2>/dev/null || true
brew install --build-from-source thinmanj/tap/claude-dev-cli

if [ $? -eq 0 ]; then
    echo "✓ Installation successful"
    cdc --version
    
    # Commit and push
    cd "$TAP_DIR"
    git add Formula/claude-dev-cli.rb
    git commit -m "feat: update claude-dev-cli to v${VERSION}

Co-Authored-By: Warp <agent@warp.dev>"
    git push
    
    echo "✓ Formula pushed to GitHub"
else
    echo "✗ Installation failed"
    exit 1
fi
```

Make it executable:
```bash
chmod +x update-homebrew-formula.sh
```

Use it:
```bash
./update-homebrew-formula.sh 0.8.3
```

## Troubleshooting

### Formula not found
```bash
brew untap thinmanj/tap
brew tap thinmanj/tap
```

### Installation fails
```bash
# Check formula syntax
brew audit --strict thinmanj/tap/claude-dev-cli

# Install with verbose output
brew install --build-from-source --verbose thinmanj/tap/claude-dev-cli
```

### Python dependency issues
The formula uses `python@3.11`. If users have issues, they can:
```bash
brew install python@3.11
```

## Best Practices

1. **Test before pushing**: Always test the formula locally before pushing to GitHub
2. **Version synchronization**: Keep formula version in sync with PyPI releases
3. **SHA256 verification**: Always verify SHA256 matches the PyPI package
4. **Semantic versioning**: Follow semver for version numbers
5. **Git co-authoring**: Include co-author line in commits

## References

- [Homebrew Formula Cookbook](https://docs.brew.sh/Formula-Cookbook)
- [Python for Formula Authors](https://docs.brew.sh/Python-for-Formula-Authors)
- [How to Create and Maintain a Tap](https://docs.brew.sh/How-to-Create-and-Maintain-a-Tap)
