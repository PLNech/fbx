"""Wiki-sync contract: builders are deterministic, stub-safe and deslopped."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import tools.sync_gh_wiki as ws


def test_home_and_sidebar_structure():
    home = ws.build_home()
    assert home.startswith("# fbx, une CLI pour ta Freebox")
    assert "## Quickstart" in home and "fbx version" in home
    assert home.count("[[") == len(ws.pages())
    side = ws.build_sidebar()
    assert side.count("[[") == len(ws.pages()) + 1  # Home + pages


def test_no_em_dashes_in_generated_copy():
    for text in (ws.build_home(), ws.build_sidebar()):
        assert "—" not in text


def test_stub_detection_never_eats_human_content():
    assert ws.is_stub("")
    assert ws.is_stub("Welcome to the fbx wiki! Click the Edit button...")
    assert ws.is_stub("# welcome to the fbx wiki\n\nsome instructions")
    assert not ws.is_stub("# My custom Home\n\nReal content about fbx.")
    assert not ws.is_stub(ws.build_home())


def test_sync_is_idempotent(tmp_path):
    (tmp_path / "Home.md").write_text(ws.build_home())
    for name in ws.pages():
        (tmp_path / f"{name}.md").write_text((ws.SRC / f"{name}.md").read_text())
    (tmp_path / "_Sidebar.md").write_text(ws.build_sidebar())
    # no git repo here: sync must decide there is nothing to do BEFORE git
    assert ws.sync(tmp_path) is False
