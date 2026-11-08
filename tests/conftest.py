import pytest

from fbx_cli import auth, config, http


@pytest.fixture(autouse=True)
def _tmp_session(tmp_path, monkeypatch):
    """No test may touch the real session file or 1Password."""
    monkeypatch.setattr(config, "CFG", tmp_path / "cfg")
    monkeypatch.setattr(config, "SESSION_FILE", tmp_path / "cfg" / "session")


@pytest.fixture(autouse=True)
def _hard_offline(monkeypatch):
    """Kill switch: any un-mocked HTTP call (or 1Password read) fails loudly.
    Tests never touch the real box; individual tests override with fakes."""
    def _deny(*a, **k):
        raise AssertionError("tests never touch the network")
    monkeypatch.setattr(http, "call", _deny)
    monkeypatch.setattr(http, "call_raw", _deny)
    monkeypatch.setattr(http, "call_body", _deny)
    monkeypatch.setattr(auth, "login", _deny)
    monkeypatch.setattr(auth, "load_password", _deny)
    http._cj.clear()  # no cookie leakage between tests


@pytest.fixture(autouse=True)
def _reset_globals():
    """Global flags must not leak from one CliRunner invocation to the next."""
    from fbx_cli import engine
    yield
    http.JSON_MODE = False
    http.DEBUG = False
    engine.set_yes(False)
