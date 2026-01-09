#!/bin/bash
# update-homebrew-formula.sh
# Automates updating the Homebrew formula for new releases

set -e  # Exit on error

VERSION="$1"

if [ -z "$VERSION" ]; then
    echo "Usage: ./update-homebrew-formula.sh X.Y.Z"
    echo "Example: ./update-homebrew-formula.sh 0.8.3"
    exit 1
fi

echo "🔄 Updating Homebrew formula to version ${VERSION}..."

# Get SHA256 from PyPI
echo "📦 Fetching SHA256 from PyPI..."
SHA_INFO=$(curl -sL https://pypi.org/pypi/claude-dev-cli/json | \
  python3 -c "import sys, json; data = json.load(sys.stdin); \
  [print(f'{f[\"url\"]}|{f[\"digests\"][\"sha256\"]}') \
  for f in data['urls'] if f['packagetype'] == 'sdist']")

if [ -z "$SHA_INFO" ]; then
    echo "❌ Error: Could not fetch package info from PyPI"
    echo "Make sure version ${VERSION} is published to PyPI"
    exit 1
fi

URL=$(echo "$SHA_INFO" | cut -d'|' -f1)
SHA256=$(echo "$SHA_INFO" | cut -d'|' -f2)

echo "✓ URL: $URL"
echo "✓ SHA256: $SHA256"

# Update formula
TAP_DIR="/opt/homebrew/Library/Taps/thinmanj/homebrew-tap"
FORMULA="$TAP_DIR/Formula/claude-dev-cli.rb"

if [ ! -d "$TAP_DIR" ]; then
    echo "❌ Error: Tap directory not found at $TAP_DIR"
    echo "Run: brew tap-new thinmanj/tap"
    exit 1
fi

echo "📝 Updating formula file..."

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
echo "🧪 Testing installation..."
brew uninstall claude-dev-cli 2>/dev/null || true
brew install --build-from-source thinmanj/tap/claude-dev-cli

if [ $? -ne 0 ]; then
    echo "❌ Installation failed"
    exit 1
fi

echo "✓ Installation successful"

# Verify version
INSTALLED_VERSION=$(cdc --version | awk '{print $3}')
if [ "$INSTALLED_VERSION" != "$VERSION" ]; then
    echo "⚠️  Warning: Installed version ($INSTALLED_VERSION) doesn't match expected ($VERSION)"
fi

echo "✓ Version check: $INSTALLED_VERSION"

# Commit and push
echo "🚀 Committing and pushing to GitHub..."
cd "$TAP_DIR"
git add Formula/claude-dev-cli.rb
git commit -m "feat: update claude-dev-cli to v${VERSION}

Co-Authored-By: Warp <agent@warp.dev>"

# Check if remote exists
if git remote get-url origin >/dev/null 2>&1; then
    git push
    echo "✓ Formula pushed to GitHub"
else
    echo "⚠️  No remote configured. Formula updated locally but not pushed."
    echo "To push manually:"
    echo "  cd $TAP_DIR"
    echo "  git remote add origin https://github.com/thinmanj/homebrew-tap.git"
    echo "  git push -u origin main"
fi

echo ""
echo "✅ Homebrew formula successfully updated to v${VERSION}!"
echo ""
echo "Users can now install/upgrade with:"
echo "  brew upgrade claude-dev-cli"
