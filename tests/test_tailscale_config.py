import os
from importlib import reload

def test_tailscale_defaults(monkeypatch):
    # Clear env to get defaults
    for k in [
        "TAILSCALE_ENABLED",
        "TAILSCALE_AUTH_KEY",
        "TAILSCALE_AUTH_KEY_FILE",
        "TAILSCALE_HOSTNAME",
        "TAILSCALE_TAGS",
        "TAILSCALE_EXTRA_ARGS",
        "TAILSCALE_STATE_DIR",
        "TAILSCALE_TIMEOUT",
    ]:
        monkeypatch.delenv(k, raising=False)

    from app.core import config
    reload(config)

    assert config.settings.TAILSCALE_ENABLED is False
    assert config.settings.TAILSCALE_AUTH_KEY == ""
    assert config.settings.TAILSCALE_AUTH_KEY_FILE == ""
    assert isinstance(config.settings.TAILSCALE_HOSTNAME, str)
    assert isinstance(config.settings.TAILSCALE_TAGS, str)
    assert isinstance(config.settings.TAILSCALE_EXTRA_ARGS, str)
    assert config.settings.TAILSCALE_STATE_DIR == "/var/lib/tailscale"
    assert isinstance(config.settings.TAILSCALE_TIMEOUT, int)


def test_tailscale_enabled_with_timeout(monkeypatch):
    monkeypatch.setenv("TAILSCALE_ENABLED", "true")
    monkeypatch.setenv("TAILSCALE_TIMEOUT", "45")

    from app.core import config
    reload(config)

    assert config.settings.TAILSCALE_ENABLED is True
    assert config.settings.TAILSCALE_TIMEOUT == 45
