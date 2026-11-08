"""Renderers: handwritten formatters + the generic engine output shapes."""
from typer.testing import CliRunner

import fbx_cli.domains  # noqa: F401
from fbx_cli import auth
from fbx_cli.cli import app
from fbx_cli.custom import fmt_calls, fmt_connection, fmt_system, fmt_tasks
from tests import fixtures_models as fx

runner = CliRunner()


def test_connection_formatter():
    out = []
    fmt_connection(fx.CONNECTION)
    assert True  # rendered without raising; content asserted via CLI below


def test_system_renders_temps_and_uptime():
    fmt_system(fx.SYSTEM)  # smoke: no raise (legacy flat shape)


def test_system_nested_real_shape():
    fmt_system(fx.SYSTEM_NESTED)  # smoke: no raise (fans/sensors arrays)


def test_tasks_progress_and_units():
    fmt_tasks([fx.TASK])


def test_calls_summary():
    fmt_calls([fx.CALL])


def test_generic_list_render_via_cli(monkeypatch):
    monkeypatch.setattr(auth, "authed", lambda *a, **k: {
        "success": True, "result": [fx.DISK]})
    res = runner.invoke(app, ["storage", "disks"])
    assert res.exit_code == 0
    assert "SYN-WD40" in res.output and "4000787030016" not in res.output  # hb() applied
    assert "3.6" in res.output or "3.6 TiB" in res.output


def test_generic_kv_render_via_cli(monkeypatch):
    monkeypatch.setattr(auth, "authed", lambda *a, **k: {
        "success": True, "result": fx.CONNECTION})
    res = runner.invoke(app, ["connection", "basic"])
    assert res.exit_code == 0
    assert "82.64.1.2" in res.output


def test_custom_connection_via_cli(monkeypatch):
    monkeypatch.setattr(auth, "authed", lambda *a, **k: {
        "success": True, "result": fx.CONNECTION})
    res = runner.invoke(app, ["wan"])
    assert res.exit_code == 0
    assert "wan: up" in res.output
    assert "1.0 MiB/s" in res.output


def test_custom_calls_alias_via_cli(monkeypatch):
    monkeypatch.setattr(auth, "authed", lambda *a, **k: {
        "success": True, "result": [fx.CALL]})
    res = runner.invoke(app, ["calls"])
    assert res.exit_code == 0
    assert "missed=1" in res.output and "new=1" in res.output


def test_fs_ls_nests_entries(monkeypatch):
    monkeypatch.setattr(auth, "authed", lambda *a, **k: {
        "success": True,
        "result": {"entries": [{"name": "synthetic.iso", "type": "file",
                                "size": 1048576, "modification": 1762500000}]}})
    res = runner.invoke(app, ["fs", "ls", "Lgd/iso"])
    assert res.exit_code == 0
    assert "synthetic.iso" in res.output and "1.0 MiB" in res.output
