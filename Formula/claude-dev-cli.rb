class ClaudeDevCli < Formula
  include Language::Python::Virtualenv

  desc "AI-powered CLI tool for developers using Claude API with multi-API routing"
  homepage "https://github.com/thinmanj/claude-dev-cli"
  url "https://files.pythonhosted.org/packages/9a/72/94b1820e227ed266bde090c2647f706f61436e682d9a918e354771ea7309/claude_dev_cli-0.8.2.tar.gz"
  sha256 "c324a9bac6ba4bd43aaff9fa7e8260bfebaf0a3d0ca5b5485597018cd893be61"
  license "MIT"

  depends_on "python@3.11"

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "Usage:", shell_output("#{bin}/cdc --help")
  end
end
