"""
Tests for authentication configuration validation.

Ensures that the server fails fast with clear error messages when
authentication is not properly configured.
"""

import os
import pytest


class TestAuthConfigValidation:
    """Test authentication configuration validation at startup"""

    def test_empty_token_fails_validation(self, monkeypatch):
        """Test that empty MCP_ACCESS_TOKEN fails validation"""
        monkeypatch.setenv("MCP_ACCESS_TOKEN", "")
        monkeypatch.setenv("TOKEN_SCOPES", "")
        
        # Force reload of settings
        import importlib
        import app.core.config
        
        with pytest.raises(ValueError) as exc_info:
            importlib.reload(app.core.config)
        
        error_msg = str(exc_info.value)
        assert "Security requires either MCP_ACCESS_TOKEN or TOKEN_SCOPES" in error_msg
        assert "HINT" in error_msg or "openssl rand -hex 32" in error_msg

    def test_whitespace_only_token_fails_validation(self, monkeypatch):
        """Test that whitespace-only MCP_ACCESS_TOKEN fails validation"""
        monkeypatch.setenv("MCP_ACCESS_TOKEN", "   ")
        monkeypatch.setenv("TOKEN_SCOPES", "")
        
        # Force reload of settings
        import importlib
        import app.core.config
        
        with pytest.raises(ValueError) as exc_info:
            importlib.reload(app.core.config)
        
        error_msg = str(exc_info.value)
        assert "Security requires either MCP_ACCESS_TOKEN or TOKEN_SCOPES" in error_msg

    def test_valid_token_passes_validation(self, monkeypatch):
        """Test that valid MCP_ACCESS_TOKEN passes validation"""
        monkeypatch.setenv("MCP_ACCESS_TOKEN", "valid-token-123")
        monkeypatch.setenv("TOKEN_SCOPES", "")
        
        # Force reload of settings
        import importlib
        import app.core.config
        
        # Should not raise
        importlib.reload(app.core.config)
        
        # Verify the token is set
        from app.core.config import settings
        assert settings.MCP_ACCESS_TOKEN == "valid-token-123"

    def test_valid_token_scopes_passes_validation(self, monkeypatch):
        """Test that valid TOKEN_SCOPES passes validation"""
        monkeypatch.setenv("MCP_ACCESS_TOKEN", "")
        monkeypatch.setenv("TOKEN_SCOPES", '{"token1": ["admin"]}')
        
        # Force reload of settings
        import importlib
        import app.core.config
        
        # Should not raise
        importlib.reload(app.core.config)
        
        # Verify the token scopes are set
        from app.core.config import settings
        assert settings.TOKEN_SCOPES == '{"token1": ["admin"]}'

    def test_both_empty_fails_validation(self, monkeypatch):
        """Test that both empty MCP_ACCESS_TOKEN and TOKEN_SCOPES fails validation"""
        monkeypatch.setenv("MCP_ACCESS_TOKEN", "")
        monkeypatch.setenv("TOKEN_SCOPES", "")
        
        # Force reload of settings
        import importlib
        import app.core.config
        
        with pytest.raises(ValueError) as exc_info:
            importlib.reload(app.core.config)
        
        error_msg = str(exc_info.value)
        assert "Security requires either MCP_ACCESS_TOKEN or TOKEN_SCOPES" in error_msg

    def test_helpful_error_message_includes_hints(self, monkeypatch):
        """Test that error message includes helpful hints for users"""
        monkeypatch.setenv("MCP_ACCESS_TOKEN", "")
        monkeypatch.setenv("TOKEN_SCOPES", "")
        
        # Force reload of settings
        import importlib
        import app.core.config
        
        with pytest.raises(ValueError) as exc_info:
            importlib.reload(app.core.config)
        
        error_msg = str(exc_info.value)
        # Check for helpful hints
        assert ".env" in error_msg or "environment variable" in error_msg
        assert "openssl rand -hex 32" in error_msg or "Generate" in error_msg

    def test_valid_token_from_file_passes_validation(self, monkeypatch, tmp_path):
        """Test that valid token from MCP_ACCESS_TOKEN_FILE passes validation"""
        # Create a token file
        token_file = tmp_path / "test_token.txt"
        token_file.write_text("valid-file-token-123")
        
        monkeypatch.setenv("MCP_ACCESS_TOKEN", "")
        monkeypatch.setenv("MCP_ACCESS_TOKEN_FILE", str(token_file))
        monkeypatch.setenv("TOKEN_SCOPES", "")
        
        # Force reload of settings
        import importlib
        import app.core.config
        
        # Should not raise
        importlib.reload(app.core.config)
        
        # Verify the token is set
        from app.core.config import settings
        assert settings.MCP_ACCESS_TOKEN == "valid-file-token-123"

    def test_empty_token_file_fails_validation(self, monkeypatch, tmp_path):
        """Test that empty token file fails validation"""
        # Create an empty token file
        token_file = tmp_path / "empty_token.txt"
        token_file.write_text("")
        
        monkeypatch.setenv("MCP_ACCESS_TOKEN", "")
        monkeypatch.setenv("MCP_ACCESS_TOKEN_FILE", str(token_file))
        monkeypatch.setenv("TOKEN_SCOPES", "")
        
        # Force reload of settings
        import importlib
        import app.core.config
        
        with pytest.raises(ValueError) as exc_info:
            importlib.reload(app.core.config)
        
        error_msg = str(exc_info.value)
        assert "empty" in error_msg.lower()

    def test_whitespace_only_token_file_fails_validation(self, monkeypatch, tmp_path):
        """Test that whitespace-only token file fails validation"""
        # Create a whitespace-only token file
        token_file = tmp_path / "whitespace_token.txt"
        token_file.write_text("   \n  \t  ")
        
        monkeypatch.setenv("MCP_ACCESS_TOKEN", "")
        monkeypatch.setenv("MCP_ACCESS_TOKEN_FILE", str(token_file))
        monkeypatch.setenv("TOKEN_SCOPES", "")
        
        # Force reload of settings
        import importlib
        import app.core.config
        
        with pytest.raises(ValueError) as exc_info:
            importlib.reload(app.core.config)
        
        error_msg = str(exc_info.value)
        # After stripping, the file is empty
        assert "empty" in error_msg.lower()
