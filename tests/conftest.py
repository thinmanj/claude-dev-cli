"""Shared pytest fixtures for claude-dev-cli tests."""

import json
import tempfile
from pathlib import Path
from typing import Any, Dict, Generator
from unittest.mock import Mock, MagicMock

import pytest
from click.testing import CliRunner


@pytest.fixture
def temp_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create a temporary home directory for config isolation."""
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    return home


@pytest.fixture
def temp_config_dir(temp_home: Path) -> Path:
    """Create a temporary .claude-dev-cli config directory."""
    config_dir = temp_home / ".claude-dev-cli"
    config_dir.mkdir(parents=True)
    return config_dir


@pytest.fixture
def sample_config() -> Dict[str, Any]:
    """Sample configuration data."""
    return {
        "api_configs": [
            {
                "name": "personal",
                "api_key": "sk-ant-personal-key",
                "description": "Personal API key",
                "default": True,
            },
            {
                "name": "client",
                "api_key": "sk-ant-client-key",
                "description": "Client API key",
                "default": False,
            },
        ],
        "default_model": "claude-3-5-sonnet-20241022",
        "max_tokens": 4096,
    }


@pytest.fixture
def config_file(temp_config_dir: Path, sample_config: Dict[str, Any]) -> Path:
    """Create a sample config file."""
    config_path = temp_config_dir / "config.json"
    with open(config_path, "w") as f:
        json.dump(sample_config, f, indent=2)
    return config_path


@pytest.fixture
def usage_log_file(temp_config_dir: Path) -> Path:
    """Create a sample usage log file."""
    log_path = temp_config_dir / "usage.jsonl"
    sample_logs = [
        {
            "timestamp": "2024-12-27T10:00:00.000000",
            "api_config": "personal",
            "model": "claude-3-5-sonnet-20241022",
            "prompt_preview": "Test prompt 1",
            "input_tokens": 100,
            "output_tokens": 200,
            "duration_ms": 1500,
        },
        {
            "timestamp": "2024-12-27T11:00:00.000000",
            "api_config": "client",
            "model": "claude-3-5-sonnet-20241022",
            "prompt_preview": "Test prompt 2",
            "input_tokens": 150,
            "output_tokens": 250,
            "duration_ms": 1800,
        },
    ]
    
    with open(log_path, "w") as f:
        for log in sample_logs:
            f.write(json.dumps(log) + "\n")
    
    return log_path


@pytest.fixture
def sample_project_profile() -> Dict[str, Any]:
    """Sample project profile configuration."""
    return {
        "name": "Test Project",
        "api_config": "client",
        "system_prompt": "You are a Python expert.",
        "allowed_commands": ["all"],
    }


@pytest.fixture
def project_dir(tmp_path: Path, sample_project_profile: Dict[str, Any]) -> Path:
    """Create a temporary project directory with .claude-dev-cli config."""
    project = tmp_path / "project"
    project.mkdir()
    
    config_file = project / ".claude-dev-cli"
    with open(config_file, "w") as f:
        json.dump(sample_project_profile, f, indent=2)
    
    return project


@pytest.fixture
def mock_anthropic_client() -> Mock:
    """Mock Anthropic client for testing."""
    mock_client = Mock()
    
    # Mock non-streaming response
    mock_response = Mock()
    mock_response.content = [Mock(text="Test response")]
    mock_response.usage = Mock(input_tokens=100, output_tokens=200)
    mock_client.messages.create.return_value = mock_response
    
    # Mock streaming response
    mock_stream = MagicMock()
    mock_stream.__enter__.return_value = mock_stream
    mock_stream.__exit__.return_value = None
    mock_stream.text_stream = ["Test ", "streaming ", "response"]
    mock_client.messages.stream.return_value = mock_stream
    
    return mock_client


@pytest.fixture
def sample_python_code() -> str:
    """Sample Python code for testing."""
    return '''"""Sample module for testing."""

def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
'''


@pytest.fixture
def sample_git_diff() -> str:
    """Sample git diff for testing."""
    return '''diff --git a/sample.py b/sample.py
index 1234567..abcdefg 100644
--- a/sample.py
+++ b/sample.py
@@ -1,5 +1,8 @@
 def hello():
-    print("Hello")
+    print("Hello, World!")
+
+def goodbye():
+    print("Goodbye!")
'''


@pytest.fixture
def cli_runner() -> CliRunner:
    """Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def isolated_cli_runner() -> Generator[CliRunner, None, None]:
    """Click CLI test runner with isolated filesystem."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        yield runner
