"""Engine: path resolution ({foreignId} slots), pair parsing, gating."""
import pytest
from typer.testing import CliRunner

import fbx_cli.domains  # noqa: F401
from fbx_cli import auth, engine
from fbx_cli.cli import app

runner = CliRunner()


def test_parse_pairs_autotypes():
    b = engine.parse_pairs(["enabled=true", "progress=42.5", "label=x",
                            "files=[\"a.iso\"]", "empty=", "bare"])
    assert b == {"enabled": True, "progress": 42.5, "label": "x",
                 "files": ["a.iso"], "empty": "", "bare": None}


def test_resolve_path_foreign_slots():
    rec = next(r for r in __import__("fbx_cli.spec", fromlist=["RECORDS"]).RECORDS
               if r.path == "downloads/{task_id}/trackers")
    assert engine.resolve_path(rec, "L", {"task_id": 7}, None) == "downloads/7/trackers"


def test_resolve_path_id_ops():
    spec = __import__("fbx_cli.spec", fromlist=["RECORDS"])
    rec = next(r for r in spec.RECORDS if r.path == "fw/redir/")
    assert engine.resolve_path(rec, "U", {}, "3") == "fw/redir/3"
    assert engine.resolve_path(rec, "L", {}, None) == "fw/redir/"


def test_singleton_put_has_no_id():
    spec = __import__("fbx_cli.spec", fromlist=["RECORDS"])
    rec = next(r for r in spec.RECORDS if r.path == "wifi/config/")
    assert engine.resolve_path(rec, "U", {}, "999") == "wifi/config/"


@pytest.fixture()
def fake_api(monkeypatch):
    seen = {}

    def fake_authed(path, data=None, method=None, form=False):
        seen.update(path=path, data=data, method=method)
        if path == "fw/redir/" and method == "GET":
            return {"success": True, "result": [{"id": 1, "enabled": True,
                                                 "ip_proto": "tcp"}]}
        return {"success": True, "result": {}}

    monkeypatch.setattr(auth, "authed", fake_authed)
    return seen


def test_list_via_cli(fake_api):
    res = runner.invoke(app, ["fw", "redir", "list"])
    assert res.exit_code == 0
    assert "tcp" in res.output
    assert fake_api["method"] == "GET" and fake_api["path"] == "fw/redir/"


def test_add_via_cli(fake_api):
    res = runner.invoke(app, ["fw", "redir", "add", "lan_ip=192.168.1.9",
                              "wan_port_start=22", "enabled=true"])
    assert res.exit_code == 0
    assert fake_api["method"] == "POST"
    assert fake_api["data"]["enabled"] is True
    assert fake_api["data"]["wan_port_start"] == 22


def test_destructive_refuses_without_yes(fake_api):
    res = runner.invoke(app, ["system", "reboot"])
    assert res.exit_code != 0
    assert "--yes" in res.output


def test_destructive_runs_with_yes(fake_api):
    res = runner.invoke(app, ["system", "reboot", "--yes"])
    assert res.exit_code == 0
    assert fake_api["method"] == "POST"
    assert fake_api["path"] == "system/reboot/"


def test_json_mode_passthrough(fake_api):
    res = runner.invoke(app, ["--json", "fw", "redir", "list"])
    assert res.exit_code == 0
    assert '"success": true' in res.output
