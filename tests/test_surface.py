"""Surface test: the installed CLI must expose the whole documented spec.

If a domain module stops being imported, a record loses its path/verbs, or the
op count silently shrinks, CI fails here: the test suite always covers every
command the docs promise.
"""
from typer.main import get_command

from fbx_cli import spec
from fbx_cli.cli import app

# The 15 domains the docs/api/ files describe (auth and contacts are registered
# from system.py and phone.py respectively).
DOMAINS = {
    "auth", "system", "connection", "lan", "wifi", "fs", "downloads",
    "tv", "phone", "contacts", "fw", "accounts", "vpn", "airmedia", "storage",
}

OP_LETTERS = set("LRGCUDA")  # list, read, get-one, create, update, delete, action


def _click_app():
    return get_command(app)


def test_root_commands_exist():
    root = _click_app()
    for name in ("version", "login", "logout", "api"):
        assert name in root.commands, f"missing root command: {name}"


def test_every_domain_registered():
    root = _click_app()
    missing = DOMAINS - set(root.commands)
    assert not missing, f"domain groups missing from the CLI: {sorted(missing)}"


def test_records_cover_every_domain():
    assert {r.dom for r in spec.RECORDS} == DOMAINS


def test_records_have_path_and_verbs():
    assert len(spec.RECORDS) > 0
    for rec in spec.RECORDS:
        where = f"{rec.dom}/{rec.name}"
        assert rec.path and isinstance(rec.path, str), f"{where}: empty path template"
        assert rec.ops, f"{where}: no verbs"
        assert set(rec.ops) <= OP_LETTERS, f"{where}: unknown op letters {rec.ops}"


def test_total_op_count_at_least_280():
    total = sum(len(r.ops) for r in spec.RECORDS)
    assert total >= 280, f"spec shrank: {total} ops across {len(spec.RECORDS)} records"
