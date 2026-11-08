"""The 1Password reference ladder: env wins, then the opref file, then the
default. A too-open opref file warns on stderr but still works."""
import os
import stat

import pytest

from fbx_cli import config


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "CFG", tmp_path)
    monkeypatch.delenv("FREEBOX_OP_REF", raising=False)
    return tmp_path


def test_env_wins(cfg):
    assert config.load_op_ref() == config.DEFAULT_OP_REF  # no env, no file
    monkey = pytest.MonkeyPatch()
    monkey.setenv("FREEBOX_OP_REF", "op://Vault/EnvItem/credential")
    try:
        assert config.load_op_ref() == "op://Vault/EnvItem/credential"
    finally:
        monkey.undo()


def test_file_wins_over_default(cfg):
    f = cfg / "opref"
    f.write_text("op://Vault/FileItem/credential\n")
    f.chmod(0o600)
    assert config.load_op_ref() == "op://Vault/FileItem/credential"


def test_env_wins_over_file(cfg):
    f = cfg / "opref"
    f.write_text("op://Vault/FileItem/credential\n")
    f.chmod(0o600)
    os.environ["FREEBOX_OP_REF"] = "op://Vault/EnvItem/credential"
    try:
        assert config.load_op_ref() == "op://Vault/EnvItem/credential"
    finally:
        del os.environ["FREEBOX_OP_REF"]


def test_missing_file_yields_default(cfg):
    assert config.load_op_ref() == config.DEFAULT_OP_REF


def test_bad_perms_warn_but_still_work(cfg, capsys):
    f = cfg / "opref"
    f.write_text("op://Vault/FileItem/credential\n")
    f.chmod(0o666)
    assert config.load_op_ref() == "op://Vault/FileItem/credential"
    err = capsys.readouterr().err
    assert "tighten it to 600" in err and "opref" in err


def test_empty_file_warns_and_falls_back(cfg, capsys):
    f = cfg / "opref"
    f.write_text("\n")
    f.chmod(0o600)
    assert config.load_op_ref() == config.DEFAULT_OP_REF
    assert "is empty" in capsys.readouterr().err


def test_only_first_line_used(cfg):
    f = cfg / "opref"
    f.write_text("op://Vault/First/credential\nop://Vault/Second/credential\n")
    f.chmod(0o600)
    assert config.load_op_ref() == "op://Vault/First/credential"


def test_perm_bits_detected():
    # mechanical guard: 0o666 carries group/other bits, 0o600 does not
    assert 0o666 & 0o077
    assert not (0o600 & 0o077)
    assert stat.filemode(0o600).endswith("------")
