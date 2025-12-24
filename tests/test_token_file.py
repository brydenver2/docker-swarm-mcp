"""
Tests for MCP_ACCESS_TOKEN_FILE functionality
"""

from importlib import reload

import pytest


@pytest.fixture(autouse=True)
def restore_config_after_test(monkeypatch):
    """Ensure config is restored after each test that reloads it"""
    # Yield to run the test
    yield
    # After test, reload config to restore default settings
    from app.core import config
    # Restore the default test token
    monkeypatch.setenv("MCP_ACCESS_TOKEN", "test-token-123")
    monkeypatch.delenv("MCP_ACCESS_TOKEN_FILE", raising=False)
    reload(config)


def test_token_from_file(monkeypatch, tmp_path):
    """Test reading token from MCP_ACCESS_TOKEN_FILE"""
    # Create a temporary token file
    token_file = tmp_path / "token.txt"
    test_token = "file-based-token-12345"
    token_file.write_text(test_token)

    # Clear any existing token env vars
    monkeypatch.delenv("MCP_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("MCP_ACCESS_TOKEN_FILE", raising=False)

    # Set MCP_ACCESS_TOKEN_FILE
    monkeypatch.setenv("MCP_ACCESS_TOKEN_FILE", str(token_file))

    # Reload config to pick up new env vars
    from app.core import config
    reload(config)

    # Verify token was read from file
    assert config.settings.MCP_ACCESS_TOKEN == test_token


def test_token_from_env_var(monkeypatch):
    """Test reading token from MCP_ACCESS_TOKEN environment variable"""
    test_token = "env-var-token-67890"

    # Clear file-based token
    monkeypatch.delenv("MCP_ACCESS_TOKEN_FILE", raising=False)

    # Set MCP_ACCESS_TOKEN
    monkeypatch.setenv("MCP_ACCESS_TOKEN", test_token)

    # Reload config
    from app.core import config
    reload(config)

    # Verify token was read from env var
    assert config.settings.MCP_ACCESS_TOKEN == test_token


def test_token_file_takes_precedence(monkeypatch, tmp_path):
    """Test that MCP_ACCESS_TOKEN_FILE takes precedence over MCP_ACCESS_TOKEN"""
    # Create a temporary token file
    token_file = tmp_path / "token.txt"
    file_token = "file-token-priority"
    env_token = "env-token-secondary"
    token_file.write_text(file_token)

    # Set both env vars
    monkeypatch.setenv("MCP_ACCESS_TOKEN", env_token)
    monkeypatch.setenv("MCP_ACCESS_TOKEN_FILE", str(token_file))

    # Reload config
    from app.core import config
    reload(config)

    # File token should take precedence
    assert config.settings.MCP_ACCESS_TOKEN == file_token
    assert config.settings.MCP_ACCESS_TOKEN != env_token


def test_token_file_not_found(monkeypatch):
    """Test error handling when token file doesn't exist"""
    # Set a non-existent file path
    monkeypatch.delenv("MCP_ACCESS_TOKEN", raising=False)
    monkeypatch.setenv("MCP_ACCESS_TOKEN_FILE", "/nonexistent/path/token.txt")

    # Should raise ValueError when loading config
    from app.core import config
    with pytest.raises(ValueError, match="Token file not found"):
        reload(config)


def test_token_file_empty(monkeypatch, tmp_path):
    """Test error handling when token file is empty"""
    # Create an empty token file
    token_file = tmp_path / "empty_token.txt"
    token_file.write_text("")

    monkeypatch.delenv("MCP_ACCESS_TOKEN", raising=False)
    monkeypatch.setenv("MCP_ACCESS_TOKEN_FILE", str(token_file))

    # Should raise ValueError for empty token
    from app.core import config
    with pytest.raises(ValueError, match="Token file .* is empty"):
        reload(config)


def test_token_file_whitespace_stripped(monkeypatch, tmp_path):
    """Test that whitespace is stripped from token file content"""
    # Create a token file with leading/trailing whitespace
    token_file = tmp_path / "token_with_whitespace.txt"
    test_token = "token-with-spaces"
    token_file.write_text(f"\n  {test_token}  \n")

    monkeypatch.delenv("MCP_ACCESS_TOKEN", raising=False)
    monkeypatch.setenv("MCP_ACCESS_TOKEN_FILE", str(token_file))

    # Reload config
    from app.core import config
    reload(config)

    # Token should be stripped of whitespace
    assert config.settings.MCP_ACCESS_TOKEN == test_token


def test_token_file_permission_error(monkeypatch, tmp_path):
    """Test error handling when token file cannot be read due to permissions"""
    # Create a token file
    token_file = tmp_path / "protected_token.txt"
    token_file.write_text("secret-token")

    # Make it unreadable (this might not work on all systems)
    try:
        token_file.chmod(0o000)

        monkeypatch.delenv("MCP_ACCESS_TOKEN", raising=False)
        monkeypatch.setenv("MCP_ACCESS_TOKEN_FILE", str(token_file))

        # Should raise ValueError for permission error
        from app.core import config
        with pytest.raises(ValueError, match="Permission denied reading token file"):
            reload(config)
    finally:
        # Restore permissions for cleanup
        token_file.chmod(0o644)


def test_read_token_from_file_or_env_function(tmp_path, monkeypatch):
    """Test the read_token_from_file_or_env helper function directly"""
    from app.core.config import read_token_from_file_or_env

    # Test 1: File path specified and exists
    token_file = tmp_path / "test_token.txt"
    test_token = "test-token-123"
    token_file.write_text(test_token)

    monkeypatch.setenv("TEST_TOKEN_FILE", str(token_file))
    result = read_token_from_file_or_env("TEST_TOKEN", "TEST_TOKEN_FILE")
    assert result == test_token

    # Test 2: No file path, use env var
    monkeypatch.delenv("TEST_TOKEN_FILE", raising=False)
    monkeypatch.setenv("TEST_TOKEN", "env-token")
    result = read_token_from_file_or_env("TEST_TOKEN", "TEST_TOKEN_FILE")
    assert result == "env-token"

    # Test 3: Neither set
    monkeypatch.delenv("TEST_TOKEN", raising=False)
    monkeypatch.delenv("TEST_TOKEN_FILE", raising=False)
    result = read_token_from_file_or_env("TEST_TOKEN", "TEST_TOKEN_FILE")
    assert result == ""


def test_docker_secrets_scenario(monkeypatch, tmp_path):
    """Test realistic Docker secrets scenario with /run/secrets mount"""
    # Simulate Docker secrets directory structure
    secrets_dir = tmp_path / "run" / "secrets"
    secrets_dir.mkdir(parents=True)

    token_file = secrets_dir / "mcp_token"
    secret_token = "docker-secret-token-abc123"
    token_file.write_text(secret_token)

    # Set up environment as Docker would
    monkeypatch.delenv("MCP_ACCESS_TOKEN", raising=False)
    monkeypatch.setenv("MCP_ACCESS_TOKEN_FILE", str(token_file))

    # Reload config
    from app.core import config
    reload(config)

    # Verify token was read from secrets file
    assert config.settings.MCP_ACCESS_TOKEN == secret_token
