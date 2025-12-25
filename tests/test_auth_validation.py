"""
Tests for authentication configuration validation.

Ensures that the server fails fast with clear error messages when
authentication is not properly configured.
"""

import pytest
from unittest.mock import patch, MagicMock


class TestAuthConfigValidation:
    """Test authentication configuration validation at startup"""

    def test_validation_empty_both(self):
        """Test that validate() fails when both MCP_ACCESS_TOKEN and TOKEN_SCOPES are empty"""
        # Create a mock Settings object with empty auth config
        mock_settings = MagicMock()
        mock_settings.MCP_ACCESS_TOKEN = ""
        mock_settings.TOKEN_SCOPES = ""
        
        # Import and call the validate method directly
        from app.core.config import Settings
        with pytest.raises(ValueError) as exc_info:
            Settings.validate(mock_settings)
        
        error_msg = str(exc_info.value)
        assert "Security requires either MCP_ACCESS_TOKEN or TOKEN_SCOPES" in error_msg
        assert "HINT" in error_msg or "openssl rand -hex 32" in error_msg

    def test_validation_whitespace_only_token(self):
        """Test that validate() fails when MCP_ACCESS_TOKEN is whitespace only"""
        mock_settings = MagicMock()
        mock_settings.MCP_ACCESS_TOKEN = "   "
        mock_settings.TOKEN_SCOPES = ""
        
        from app.core.config import Settings
        with pytest.raises(ValueError) as exc_info:
            Settings.validate(mock_settings)
        
        error_msg = str(exc_info.value)
        assert "Security requires either MCP_ACCESS_TOKEN or TOKEN_SCOPES" in error_msg

    def test_validation_valid_token(self):
        """Test that validate() succeeds with valid MCP_ACCESS_TOKEN"""
        mock_settings = MagicMock()
        mock_settings.MCP_ACCESS_TOKEN = "valid-token-123"
        mock_settings.TOKEN_SCOPES = ""
        mock_settings.MCP_TRANSPORT = "http"
        mock_settings.INTENT_PRECEDENCE = "intent"
        
        from app.core.config import Settings
        # Should not raise
        Settings.validate(mock_settings)

    def test_validation_valid_token_scopes(self):
        """Test that validate() succeeds with valid TOKEN_SCOPES"""
        mock_settings = MagicMock()
        mock_settings.MCP_ACCESS_TOKEN = ""
        mock_settings.TOKEN_SCOPES = '{"token1": ["admin"]}'
        mock_settings.MCP_TRANSPORT = "http"
        mock_settings.INTENT_PRECEDENCE = "intent"
        
        from app.core.config import Settings
        # Should not raise
        Settings.validate(mock_settings)

    def test_validation_helpful_error_message(self):
        """Test that error message includes helpful hints"""
        mock_settings = MagicMock()
        mock_settings.MCP_ACCESS_TOKEN = ""
        mock_settings.TOKEN_SCOPES = ""
        
        from app.core.config import Settings
        with pytest.raises(ValueError) as exc_info:
            Settings.validate(mock_settings)
        
        error_msg = str(exc_info.value)
        # Check for helpful hints
        assert ".env" in error_msg or "environment variable" in error_msg
        assert "openssl rand -hex 32" in error_msg or "Generate" in error_msg

    def test_read_token_from_file(self, tmp_path):
        """Test reading token from file"""
        from app.core.config import read_token_from_file_or_env
        
        # Create a token file
        token_file = tmp_path / "test_token.txt"
        token_file.write_text("file-token-123")
        
        with patch.dict('os.environ', {
            'TEST_TOKEN': '',
            'TEST_TOKEN_FILE': str(token_file)
        }, clear=False):
            result = read_token_from_file_or_env('TEST_TOKEN', 'TEST_TOKEN_FILE')
            assert result == "file-token-123"

    def test_read_token_from_env(self):
        """Test reading token from environment variable"""
        from app.core.config import read_token_from_file_or_env
        
        with patch.dict('os.environ', {
            'TEST_TOKEN': 'env-token-123',
            'TEST_TOKEN_FILE': ''
        }, clear=False):
            result = read_token_from_file_or_env('TEST_TOKEN', 'TEST_TOKEN_FILE')
            assert result == "env-token-123"

    def test_read_token_file_takes_precedence(self, tmp_path):
        """Test that file takes precedence over env var"""
        from app.core.config import read_token_from_file_or_env
        
        token_file = tmp_path / "test_token.txt"
        token_file.write_text("file-token")
        
        with patch.dict('os.environ', {
            'TEST_TOKEN': 'env-token',
            'TEST_TOKEN_FILE': str(token_file)
        }, clear=False):
            result = read_token_from_file_or_env('TEST_TOKEN', 'TEST_TOKEN_FILE')
            assert result == "file-token"

    def test_read_token_empty_file_raises(self, tmp_path):
        """Test that empty token file raises error"""
        from app.core.config import read_token_from_file_or_env
        
        token_file = tmp_path / "empty.txt"
        token_file.write_text("")
        
        with patch.dict('os.environ', {
            'TEST_TOKEN': '',
            'TEST_TOKEN_FILE': str(token_file)
        }, clear=False):
            with pytest.raises(ValueError) as exc_info:
                read_token_from_file_or_env('TEST_TOKEN', 'TEST_TOKEN_FILE')
            
            assert "empty" in str(exc_info.value).lower()

    def test_read_token_whitespace_only_file_raises(self, tmp_path):
        """Test that whitespace-only token file raises error"""
        from app.core.config import read_token_from_file_or_env
        
        token_file = tmp_path / "whitespace.txt"
        token_file.write_text("   \n  \t  ")
        
        with patch.dict('os.environ', {
            'TEST_TOKEN': '',
            'TEST_TOKEN_FILE': str(token_file)
        }, clear=False):
            with pytest.raises(ValueError) as exc_info:
                read_token_from_file_or_env('TEST_TOKEN', 'TEST_TOKEN_FILE')
            
            # After stripping, the file is empty
            assert "empty" in str(exc_info.value).lower()

