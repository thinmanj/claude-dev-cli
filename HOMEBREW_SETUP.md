# Homebrew Tap Setup - Next Steps

The Homebrew formula has been created and tested successfully! Here's what you need to do to publish it.

## ✅ Completed

- [x] Created Homebrew formula (`Formula/claude-dev-cli.rb`)
- [x] Tested formula locally (installs successfully)
- [x] Created local tap (`thinmanj/tap`)
- [x] Updated documentation (README.md, QUICKSTART.md, WARP.md)
- [x] Created HOMEBREW.md guide with maintenance instructions

## 📋 Next Steps to Publish

### 1. Create GitHub Repository

Go to GitHub and create a new public repository:

- **Repository name**: `homebrew-tap` (must start with "homebrew-")
- **Owner**: thinmanj
- **Description**: "Homebrew formulae for claude-dev-cli"
- **Visibility**: Public
- **Initialize**: Yes (with README)

URL will be: `https://github.com/thinmanj/homebrew-tap`

### 2. Push Local Tap to GitHub

```bash
# Navigate to local tap directory
cd /opt/homebrew/Library/Taps/thinmanj/homebrew-tap

# Check current state
git status
git log --oneline

# Add remote
git remote add origin https://github.com/thinmanj/homebrew-tap.git

# Push to GitHub (might need to force if repo was initialized with README)
git pull origin main --rebase  # If repo has README
git push -u origin main
```

### 3. Verify Installation Works from GitHub

Once pushed, test that users can install:

```bash
# Remove local tap (to simulate fresh install)
brew untap thinmanj/tap

# Add tap from GitHub
brew tap thinmanj/tap

# Install
brew install claude-dev-cli

# Verify
cdc --version  # Should show 0.8.3
```

### 4. Update README in Tap Repository

Edit the README.md in the homebrew-tap repository to include:

```markdown
# Homebrew Tap for claude-dev-cli

Official Homebrew tap for [claude-dev-cli](https://github.com/thinmanj/claude-dev-cli).

## Installation

```bash
brew install thinmanj/tap/claude-dev-cli
```

## What is claude-dev-cli?

A powerful AI-powered CLI tool for developers using Claude API with:
- Multi-API routing
- Code review, testing, debugging
- Context intelligence
- Usage tracking

See the [main repository](https://github.com/thinmanj/claude-dev-cli) for full documentation.

## Updating

```bash
brew upgrade claude-dev-cli
```

## Uninstalling

```bash
brew uninstall claude-dev-cli
```
```

## 🎯 Current Status

**Formula Location**: `/Volumes/Projects/claude-dev-cli/Formula/claude-dev-cli.rb`

**Formula Details**:
- Version: 0.8.3
- Python: 3.11
- Source: PyPI tarball
- SHA256: b47a8aa09714d088d653518e851b24f588ced88713457ca789b4e48b5838c297

**Local Testing**: ✅ PASSED
- Installation works
- `cdc --version` returns correct version
- `cdc --help` displays commands

## 📚 Documentation Updates

All documentation has been updated:

1. **README.md**: Added Homebrew installation as first option
2. **QUICKSTART.md**: Added Homebrew to installation section
3. **WARP.md**: Added Homebrew deployment steps to release process
4. **HOMEBREW.md**: Complete guide for maintaining the tap

## 🔄 Future Updates

When releasing new versions (e.g., v0.8.3):

1. Follow standard PyPI release process
2. Run the update script: `./update-homebrew-formula.sh 0.8.3`
3. Or manually update formula following HOMEBREW.md guide

See `HOMEBREW.md` for the complete update process and automation script.

## 🐛 Troubleshooting

If you encounter issues:

1. **Formula not found**: 
   ```bash
   brew untap thinmanj/tap
   brew tap thinmanj/tap
   ```

2. **Installation fails**:
   ```bash
   brew audit --strict thinmanj/tap/claude-dev-cli
   ```

3. **Test verbose installation**:
   ```bash
   brew install --build-from-source --verbose thinmanj/tap/claude-dev-cli
   ```

## 📞 Support

- Main repo: https://github.com/thinmanj/claude-dev-cli
- PyPI: https://pypi.org/project/claude-dev-cli/
- Issues: https://github.com/thinmanj/claude-dev-cli/issues
