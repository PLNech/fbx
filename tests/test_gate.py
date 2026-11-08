"""Gate integrity: gate=True must cover EVERY mutating op, and every gated op
must refuse without --yes before any HTTP call happens."""
import pytest
import typer

from fbx_cli import auth, http
from fbx_cli import spec
import fbx_cli.domains  # noqa: F401 (populates spec.RECORDS)
from fbx_cli.engine import run, method_for

MUTATING = set("CUDA")
READS = set("LRG")


def test_gate_true_covers_all_mutating_ops():
    offenders = []
    for rec in spec.RECORDS:
        if rec.gate_all:
            missing = (set(rec.ops) & MUTATING) - set(rec.gate)
            if missing:
                offenders.append((rec.dom, rec.name, sorted(missing)))
    assert not offenders, f"gate=True records with ungated mutating ops: {offenders}"


def test_gate_never_covers_reads():
    for rec in spec.RECORDS:
        gated_reads = set(rec.gate) & READS
        assert not gated_reads, \
            f"{rec.dom}/{rec.name} gates read ops: {sorted(gated_reads)}"


NOTE_OP_WORDS = {"rm": "D", "delete": "D", "destroy": "D", "erase": "D",
                 "add": "C", "create": "C", "set": "U", "write": "U",
                 "format": "U", "reboot": "A", "shutdown": "A", "reset": "A"}


def test_destructive_notes_are_gated():
    """Notes that say DESTROYS gate every write; notes that scope --yes to
    named ops (rm/add/create/...) must have those ops gated."""
    offenders = []
    for rec in spec.RECORDS:
        note = (rec.note or "")
        if "DESTROYS" in note:
            missing = (set(rec.ops) & MUTATING) - set(rec.gate)
            if missing:
                offenders.append((rec.dom, rec.name, sorted(missing)))
        elif "needs --yes" in note:
            words = {w.strip(".,()") for w in note.split()}
            promised = {NOTE_OP_WORDS[w] for w in words if w in NOTE_OP_WORDS}
            missing = (promised & set(rec.ops)) - set(rec.gate)
            if missing:
                offenders.append((rec.dom, rec.name, sorted(missing)))
    assert not offenders, f"notes promise --yes but gate misses ops: {offenders}"


def _deny_http(*a, **k):
    raise AssertionError(f"HTTP call attempted on a gated op without --yes: {a}")


@pytest.mark.parametrize("rec", [r for r in spec.RECORDS if r.gate_all],
                         ids=lambda r: f"{r.dom}-{r.name}")
def test_gate_true_refuses_without_yes_before_any_http(rec, monkeypatch):
    """Every mutating op on a gate=True record refuses with no HTTP, no --yes."""
    monkeypatch.setattr(http, "call", _deny_http)
    monkeypatch.setattr(http, "call_raw", _deny_http)
    monkeypatch.setattr(http, "call_body", _deny_http)
    monkeypatch.setattr(auth, "authed", _deny_http)
    monkeypatch.setattr(auth, "login", _deny_http)
    for op in rec.ops:
        if op not in rec.gate:
            continue
        kwargs = {s: "0" for s in rec.slots}
        if op in "GUD" and not rec.singleton:
            kwargs["item_id"] = "0"
        with pytest.raises(typer.Exit, match="refusing a destructive op"):
            run(rec, op, **kwargs)


def test_failure_line_carries_http_status(monkeypatch):
    rec = next(r for r in spec.RECORDS if r.name == "disks")
    monkeypatch.setattr(auth, "authed",
                        lambda *a, **k: {"success": False, "msg": "Erreur interne"})
    monkeypatch.setattr(http, "LAST_STATUS", 500, raising=False)
    with pytest.raises(typer.Exit, match=r"Erreur interne \(HTTP 500\)"):
        run(rec, "L")
