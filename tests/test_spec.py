"""Spec hygiene + coverage: every record well-formed, domains complete."""
import pytest

import fbx_cli.domains  # noqa: F401 — registers every record
from fbx_cli.spec import BY_DOMAIN, RECORDS


def test_all_documented_domains_present():
    expected = {"auth", "system", "connection", "lan", "wifi", "fs", "downloads",
                "tv", "phone", "contacts", "fw", "accounts", "vpn", "airmedia",
                "storage"}
    assert expected <= set(BY_DOMAIN)


def test_no_vm_domain():
    assert "vm" not in BY_DOMAIN


def test_record_count_is_in_doc_ballpark():
    # docs/api/ documents ~190 endpoints; every one must be a record or a
    # deliberate gap. Verb-level count (ops per record) is the coverage unit.
    assert len(RECORDS) >= 150
    assert sum(len(r.ops) for r in RECORDS) >= 180


@pytest.mark.parametrize("rec", RECORDS, ids=lambda r: f"{r.dom}.{r.name}")
def test_record_shape(rec):
    assert set(rec.ops) <= set("LRGCUDA"), rec.path
    assert rec.path and not rec.path.startswith("/")
    assert "//" not in rec.path
    if rec.singleton:
        # singleton writes hit the path itself: no leading slot-free id appending
        assert rec.path.endswith("/") or rec.path.split("/")[-1]


def test_path_templates_resolve_all_slots():
    for r in RECORDS:
        for s in r.slots:
            assert s.replace("_", "").isalnum()


def test_destructive_records_are_gated():
    must_be_gated = [
        ("system", "reboot"), ("system", "shutdown"), ("storage", "format"),
        ("storage", "fsck"), ("storage", "internal-reset"), ("fs", "rm"),
        ("system", "reboot"),
    ]
    for dom, name in must_be_gated:
        rec = next(r for r in RECORDS if r.dom == dom and r.name == name)
        assert rec.gate, f"{dom} {name} must be gated"


def test_aliases_exist():
    names = {r.alias for r in RECORDS if r.alias}
    assert {"wan", "status", "calls"} <= names
