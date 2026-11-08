"""UX contract: -h works everywhere, bare args are usage errors, no shrug
cells, discoverability epilogs, graceful degradation, and a tldr that cannot
rot (every example is executed against fixtures)."""
import fbx_cli.domains  # noqa: F401
from fbx_cli import auth, http
from fbx_cli.cli import app, TLDR
from fbx_cli.fmt import compact, fmt_cell
from tests import fixtures_models as fx
from tests.test_engine import runner  # noqa: F401  (shared CliRunner)


# --- 1. -h alias everywhere

def test_dash_h_root():
    for args in (["-h"], ["--help"]):
        res = runner.invoke(app, args)
        assert res.exit_code == 0 and "Full-coverage CLI" in res.output


def test_dash_h_domain_group():
    res = runner.invoke(app, ["wifi", "-h"])
    assert res.exit_code == 0 and "documented endpoints" in res.output


def test_dash_h_record_subgroup_and_leaf():
    res = runner.invoke(app, ["fw", "samba", "-h"])
    assert res.exit_code == 0 and "samba" in res.output.lower()
    res = runner.invoke(app, ["fw", "samba", "show", "-h"])
    assert res.exit_code == 0 and "netshare/samba" in res.output
    res = runner.invoke(app, ["version", "-h"])
    assert res.exit_code == 0


# --- 2. bare args are usage errors, never swallowed

def test_bare_arg_is_usage_error_with_hint():
    res = runner.invoke(app, ["wifi", "bss-config", "set", "aa:bb:cc:00:00:02", "foo"])
    assert res.exit_code != 0
    assert "body fields are key=value" in res.output
    assert "fbx wifi bss-config show" in res.output  # R op exists -> teach show


def test_bare_arg_no_hint_without_read_ops():
    # mac-filter is LCUD — no show/get, so the error must not invent one
    res = runner.invoke(app, ["wifi", "mac-filter", "add", "mac=aa:bb:cc:00:00:01", "oops"])
    assert res.exit_code != 0
    assert "body fields are key=value" in res.output
    assert "show" not in res.output.split("key=value")[-1]


# --- 3. no {N keys} shrug cells

def test_compact_dict_cell():
    cell = fmt_cell({"alpha": True, "beta": "x", "gamma": 1, "delta": [1, 2]})
    assert "{4 keys}" not in cell and "{…}" not in cell
    assert "alpha=yes" in cell and "+1 more" in cell
    assert cell.endswith("(--json for full detail)")


def test_compact_long_list_cell():
    cell = fmt_cell([f"device-{i}" for i in range(9)])
    assert "device-0" in cell and "device-2" in cell and "+6 more" in cell
    assert "device-8" not in cell


def test_no_shrug_cells_in_kv_render(monkeypatch):
    monkeypatch.setattr(auth, "authed", lambda *a, **k: {
        "success": True,
        "result": {"name": "syn-perm", "flags": {"a": 1, "b": 2, "c": 3, "d": 4}}})
    res = runner.invoke(app, ["auth", "perms"])
    assert res.exit_code == 0
    assert "{…}" not in res.output and "{4 keys}" not in res.output
    assert "[list:" not in res.output
    assert "a=1" in res.output and "(--json for full detail)" in res.output


# --- 4. discoverability epilog

def test_domain_help_shows_real_example():
    res = runner.invoke(app, ["wifi", "-h"])
    assert res.exit_code == 0
    assert "e.g. fbx wifi" in res.output


def test_record_help_shows_real_example():
    res = runner.invoke(app, ["fw", "dmz", "-h"])
    assert res.exit_code == 0
    assert "e.g. fbx fw dmz show" in res.output


# --- 5. graceful degradation for multi-call customs

def _overview_mock(raid_resp):
    def fake_authed(path, *a, **k):
        if path.startswith("storage/disk/"):
            return {"success": True, "result": [fx.DISK]}
        if path.startswith("storage/partition/"):
            return {"success": True, "result": [fx.PARTITION]}
        if path.startswith("storage/raid/"):
            return raid_resp
        raise AssertionError(f"unexpected path {path}")
    return fake_authed


def test_storage_overview_degrades_when_raid_500s(monkeypatch):
    monkeypatch.setattr(auth, "authed", _overview_mock(
        {"success": False, "msg": "Erreur interne"}))
    monkeypatch.setattr(http, "LAST_STATUS", 500, raising=False)
    res = runner.invoke(app, ["storage", "overview"])
    assert res.exit_code == 0, res.output
    assert "raid: unavailable (box error: Erreur interne (HTTP 500))" in res.output
    assert "SYN-WD40" in res.output  # the disks table still renders


def test_storage_overview_total_failure_fails_loudly(monkeypatch):
    monkeypatch.setattr(auth, "authed",
                        lambda *a, **k: {"success": False, "msg": "Erreur interne"})
    res = runner.invoke(app, ["storage", "overview"])
    assert res.exit_code != 0
    assert "answered none" in res.output


# --- 6. tldr: every example must actually run against fixtures

def _install_fixture_transport(monkeypatch):
    def fake_call(path, *a, **k):
        if path.startswith("/api_version"):
            return {"success": True, "result": {"api_version": "12.0"}}
        if path.startswith("storage/"):
            return {"success": True, "result": [fx.DISK if "disk" in path else fx.PARTITION]}
        return {"success": True, "result": fx.CONNECTION}
    monkeypatch.setattr(http, "call", fake_call)
    monkeypatch.setattr(auth, "login", lambda *a, **k: "FBXSID=synthetic")
    monkeypatch.setattr(auth, "authed", lambda path, *a, **k: fake_call(path))


def test_tldr_lists_ten_examples():
    res = runner.invoke(app, ["tldr"])
    assert res.exit_code == 0
    cmds = [c for _, c in TLDR]
    assert len(cmds) == 10
    assert "fbx version" in res.output and "fbx api GET" in res.output
    assert not any(c.startswith("fbx wifi status") for c in cmds)  # not a real command


def test_tldr_examples_execute(monkeypatch):
    """tldr can never rot: each example's command path runs here, fixture-backed."""
    _install_fixture_transport(monkeypatch)
    for _, cmd in TLDR:
        argv = cmd.split()[1:]
        res = runner.invoke(app, argv)
        assert res.exit_code == 0, f"{cmd} failed:\n{res.output}"
