"""Auth flow, fully mocked: challenge eval stubbed, no node, no network."""
import stat

from fbx_cli import auth, config, http

# original (unpatched) login, saved before conftest goes hard-offline
_REAL_LOGIN = auth.login

LOGIN_STATE = {"success": True, "result": {
    "logged_in": False,
    "challenge": {"p0": "1+1", "p1": "'a'"},  # evaluated by the stub, not node
    "password_salt": "salty",
}}


def _patch(monkeypatch, calls):
    monkeypatch.setattr(http, "call", _fake_call(calls))
    monkeypatch.setattr(auth, "challenge_to_string", lambda table: "CHALLENGE")
    monkeypatch.setattr(auth, "login", _REAL_LOGIN)


def _fake_call(calls):
    def fake(path, data=None, headers=None, method=None, form=False, timeout=20):
        calls.append((method or ("POST" if data else "GET"), path, data))
        if path == "login/" and method != "POST":
            return LOGIN_STATE
        if path == "login/":  # password POST
            assert form and "password" in data
            http._cj.set_cookie(auth._mkcookie("FBXSID", "test-token"))
            return {"success": True}
        return {"success": True, "result": {}}
    return fake


def test_login_computes_panel_hash_and_stores_cookie(monkeypatch):
    calls = []
    _patch(monkeypatch, calls)
    import hashlib, hmac
    cookie = auth.login(force=True, password="hunter2")
    h_pass = hashlib.sha1(b"saltyhunter2").hexdigest()
    expected = hmac.new(h_pass.encode(), b"CHALLENGE", hashlib.sha1).hexdigest()
    posts = [c for c in calls if c[1] == "login/" and c[0] == "POST"]
    assert posts and posts[0][2]["password"] == expected
    assert cookie and "=" in cookie
    assert config.SESSION_FILE.exists()
    assert stat.S_IMODE(config.SESSION_FILE.stat().st_mode) == 0o600


def test_login_reuses_saved_cookie(monkeypatch):
    calls = []
    _patch(monkeypatch, calls)
    auth.login(force=True, password="hunter2")
    n = len(calls)
    auth.login()  # no force: file-backed session, no new login POST
    assert all(c[0] != "POST" for c in calls[n:])


def test_authed_retries_once_on_auth_error(monkeypatch):
    calls = []
    _patch(monkeypatch, calls)
    auth.login(force=True, password="hunter2")  # prime the session, no 1Password
    responses = [{"success": False, "error_code": "auth_required"},
                 {"success": True, "result": {"ok": 1}}]

    def flaky(path, data=None, headers=None, method=None, form=False, timeout=20):
        if path == "login/":
            http._cj.set_cookie(auth._mkcookie("FBXSID", "retry-token"))
            return {"success": True}
        return responses.pop(0)

    monkeypatch.setattr(http, "call", flaky)
    monkeypatch.setattr(auth, "load_password", lambda: "hunter2")  # force re-login path
    resp = auth.authed("connection")
    assert resp == {"success": True, "result": {"ok": 1}}


def test_password_never_hits_disk_or_argv(monkeypatch):
    calls = []
    _patch(monkeypatch, calls)
    auth.login(force=True, password="topsecret")
    blob = config.SESSION_FILE.read_text()
    assert "topsecret" not in blob and "hunter2" not in blob
