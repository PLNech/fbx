"""Readability sweep (corpus + fuzz): every documented op renders a synthetic
response through the REAL renderer without shrug cells, and random hostile
structures never crash it. Zero-shrug is asserted; per-domain counts are the
generated report."""
import io
import random
import re
import sys
from pathlib import Path

import pytest
from rich.console import Console

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import fbx_cli.domains  # noqa: F401,E402
from fbx_cli import render  # noqa: E402
from fbx_cli.fmt import DETAIL_HINT, compact, fmt_cell  # noqa: E402
from fbx_cli.render import render_kv, render_list, render_result  # noqa: E402
from fbx_cli.spec import BY_DOMAIN  # noqa: E402
from tools.gen_wiki import envelope_for  # noqa: E402  (same synthesizer as the wiki)

SHRUG = re.compile(r"\{\d+ keys\}|\{…\}|\[list:\d+\]|\[\d+ items\]")


class Capture:
    """Patch the renderers' console into a StringIO and hand back the text."""

    def __init__(self):
        self.buf = io.StringIO()
        self.console = Console(file=self.buf, width=100, legacy_windows=False)

    def __enter__(self):
        self._old_fmt = render.console
        self._old_render = render.console
        render.console = self.console
        import fbx_cli.fmt as fmt_mod
        self._old = fmt_mod.console
        fmt_mod.console = self.console
        return self

    def __exit__(self, *a):
        render.console = self._old_render
        import fbx_cli.fmt as fmt_mod
        fmt_mod.console = self._old


def render_text(resp, rec=None, op=None):
    with Capture() as c:
        render_result(resp, rec, op)
        return c.buf.getvalue()


# --- 1. corpus: all 292 record/ops through the real renderer

def test_corpus_every_record_op_renders_without_shrugs():
    report, shrugs = [], []
    n = 0
    for dom in sorted(BY_DOMAIN):
        ops_rendered = hinted = 0
        for rec in BY_DOMAIN[dom]:
            for op in rec.ops:
                n += 1
                out = render_text(envelope_for(rec, op), rec, op)
                ops_rendered += 1
                hits = SHRUG.findall(out)
                if hits:
                    shrugs.append((dom, rec.name, op, hits))
                if DETAIL_HINT in out:
                    hinted += 1
        report.append((dom, ops_rendered, hinted))
    print("\nfbx render sweep — per domain: ops rendered, cells truncated-with-hint")
    for dom, ops, hinted in report:
        print(f"  {dom:12s} {ops:3d} ops  {hinted:3d} hinted cells")
    assert n >= 292
    assert not shrugs, f"shrug cells found: {shrugs[:5]}"


# --- 2. fuzz: hostile structures never crash, never shrug

LEAVES = [None, True, False, 0, 42, 2**63, -1, 3.14, "", "x" * 200,
          "café — ☔", "fd0f:ee:b0::50", "a" * 41, [], {}, [1, 2, 3]]


def _random_value(rng, depth):
    if depth <= 0 or rng.random() < 0.35:
        return rng.choice(LEAVES)
    if rng.random() < 0.5:
        return {f"k{i}": _random_value(rng, depth - 1) for i in range(rng.randint(0, 6))}
    return [_random_value(rng, depth - 1) for _ in range(rng.randint(0, 6))]


def test_fuzz_render_never_crashes_or_shrugs():
    rng = random.Random(42)  # deterministic fuzz
    for i in range(300):
        v = _random_value(rng, 4)
        if rng.random() < 0.5:
            out = fmt_cell(v)
        else:
            obj = v if isinstance(v, dict) and v else {"synthetic": v}
            with Capture() as c:
                render_kv(obj)
                if isinstance(v, list) and v:
                    render_list([v[:3]], cols=["c0", "c1", "c2"])
                out = c.buf.getvalue()
        assert not SHRUG.search(out), f"fuzz case {i} produced a shrug: {out[:200]}"


def test_fuzz_compact_always_hinted_when_nested():
    rng = random.Random(7)
    for _ in range(100):
        v = _random_value(rng, 3)
        if isinstance(v, (dict, list)):
            cell = fmt_cell(v)
            assert cell.endswith(DETAIL_HINT), cell[:120]
            assert "…" in cell or DETAIL_HINT in cell


def test_compact_depth_guard():
    deep = {"a": {"b": {"c": {"d": {"e": 1}}}}}
    cell = compact(deep)
    assert "a=" in cell and "…" in cell  # deep nesting collapses, hint carries the rest
    assert "{3 keys}" not in cell and "{…}" not in cell
