"""
Unit tests for Docker client with different connection modes

Tests verify DOCKER_HOST, DOCKER_TLS_VERIFY, and DOCKER_CERT_PATH handling
for Unix socket, TCP, TCP+TLS, and SSH modes.
"""

from unittest.mock import Mock, patch

import pytest

from app.docker_client import DockerClient


class TestDockerClientModes:
    """Test Docker client initialization with different connection modes"""

    @patch("app.docker_client.docker")
    @patch("app.docker_client.settings")
    def test_unix_socket_mode(self, mock_settings, mock_docker):
        """Test Docker client with Unix socket (default)"""
        mock_settings.DOCKER_HOST = "unix:///var/run/docker.sock"
        mock_settings.DOCKER_TLS_VERIFY = False
        mock_settings.DOCKER_CERT_PATH = ""

        mock_client = Mock()
        mock_client.ping.return_value = True
        mock_docker.from_env.return_value = mock_client

        client = DockerClient()

        mock_docker.from_env.assert_called_once()
        mock_client.ping.assert_called_once()
        assert client.client == mock_client

    @patch("app.docker_client.docker")
    @patch("app.docker_client.settings")
    def test_tcp_mode_without_tls(self, mock_settings, mock_docker):
        """Test Docker client with TCP without TLS"""
        mock_settings.DOCKER_HOST = "tcp://192.168.1.100:2375"
        mock_settings.DOCKER_TLS_VERIFY = False
        mock_settings.DOCKER_CERT_PATH = ""

        mock_client = Mock()
        mock_client.ping.return_value = True
        mock_docker.DockerClient.return_value = mock_client

        client = DockerClient()

        mock_docker.DockerClient.assert_called_once_with(
            base_url="tcp://192.168.1.100:2375"
        )
        mock_client.ping.assert_called_once()
        assert client.client == mock_client

    @patch("app.docker_client.docker")
    @patch("app.docker_client.settings")
    def test_tcp_mode_with_tls(self, mock_settings, mock_docker):
        """Test Docker client with TCP+TLS"""
        mock_settings.DOCKER_HOST = "tcp://192.168.1.100:2376"
        mock_settings.DOCKER_TLS_VERIFY = True
        mock_settings.DOCKER_CERT_PATH = "/path/to/certs"

        mock_client = Mock()
        mock_client.ping.return_value = True
        mock_docker.DockerClient.return_value = mock_client

        mock_tls_config = Mock()
        mock_docker.tls.TLSConfig.return_value = mock_tls_config

        client = DockerClient()

        mock_docker.tls.TLSConfig.assert_called_once_with(
            client_cert=(
                "/path/to/certs/cert.pem",
                "/path/to/certs/key.pem"
            ),
            ca_cert="/path/to/certs/ca.pem",
            verify=True
        )
        mock_docker.DockerClient.assert_called_once_with(
            base_url="tcp://192.168.1.100:2376",
            tls=mock_tls_config
        )
        mock_client.ping.assert_called_once()

    @patch("app.docker_client.docker")
    @patch("app.docker_client.settings")
    def test_ssh_mode(self, mock_settings, mock_docker):
        """Test Docker client with SSH"""
        mock_settings.DOCKER_HOST = "ssh://user@remote-host"
        mock_settings.DOCKER_TLS_VERIFY = False
        mock_settings.DOCKER_CERT_PATH = ""

        mock_client = Mock()
        mock_client.ping.return_value = True
        mock_docker.DockerClient.return_value = mock_client

        client = DockerClient()

        mock_docker.DockerClient.assert_called_once_with(
            base_url="ssh://user@remote-host"
        )
        mock_client.ping.assert_called_once()

    @patch("app.docker_client.docker")
    @patch("app.docker_client.settings")
    def test_connection_failure(self, mock_settings, mock_docker):
        """Test Docker client initialization failure"""
        mock_settings.DOCKER_HOST = "unix:///var/run/docker.sock"
        mock_settings.DOCKER_TLS_VERIFY = False
        mock_settings.DOCKER_CERT_PATH = ""

        mock_docker.from_env.side_effect = Exception("Connection refused")

        with pytest.raises(RuntimeError, match="Docker engine unreachable"):
            DockerClient()

    @patch("app.docker_client.docker")
    @patch("app.docker_client.settings")
    def test_tls_without_cert_path_warning(self, mock_settings, mock_docker, caplog):
        """Test warning when DOCKER_TLS_VERIFY=1 but no DOCKER_CERT_PATH"""
        mock_settings.DOCKER_HOST = "tcp://192.168.1.100:2376"
        mock_settings.DOCKER_TLS_VERIFY = True
        mock_settings.DOCKER_CERT_PATH = ""

        mock_client = Mock()
        mock_client.ping.return_value = True
        mock_docker.DockerClient.return_value = mock_client

        client = DockerClient()

        # Should log warning about missing cert path
        assert "DOCKER_CERT_PATH not set" in caplog.text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
