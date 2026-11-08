#!/usr/bin/env python3
"""Regenerate docs/cmd/ — the per-domain command wiki.

Single source of truth: the endpoint records in fbx_cli/domains/ (themselves
transcribed from docs/api/). Every example is a SYNTHETIC fixture built by the
same machinery as the test suite (tests/fixtures_models.py + a type-driven
synthesizer for the rest) — no live box is ever contacted, no credentials are
involved. Terminal output is captured with typer's CliRunner against a mocked
transport, so each page shows exactly what rich prints.

Deterministic and idempotent: stable key order, fixed console width, no
timestamps — CI diffs the result (`git diff --exit-code docs/cmd`).

Usage:
    python tools/gen_wiki.py            # regenerate docs/cmd/
    python tools/gen_wiki.py --demo     # print the three README demo blocks
"""
import copy
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

os.environ["COLUMNS"] = "100"  # fixed rich width -> byte-stable output

from typer.testing import CliRunner  # noqa: E402

from fbx_cli import auth, http  # noqa: E402
from fbx_cli.cli import app  # noqa: E402
from fbx_cli.engine import OP_LEAF, method_for  # noqa: E402
from fbx_cli.spec import BY_DOMAIN  # noqa: E402
from tests import fixtures_models as fx  # noqa: E402

OUT = ROOT / "docs" / "cmd"

# --- synthetic payloads for the four custom renderers + the storage overview

TASK_B = {**fx.TASK, "id": 7, "name": "synthetic-backup.tar", "status": "queued",
          "progress": 0.0, "rx_speed": 0, "size": 1024**3}
CALL_B = {**fx.CALL, "id": 2, "number": "0600000002", "type": "outgoing",
          "new": False, "outgoing": True, "duration": 125}

CUSTOM_SAMPLES = {
    ("connection", "full", "R"): lambda: dict(fx.CONNECTION),
    ("system", "health", "R"): lambda: copy.deepcopy(fx.SYSTEM_NESTED),
    ("downloads", "tasks", "L"): lambda: [dict(fx.TASK), dict(TASK_B)],
    ("phone", "calls", "L"): lambda: [dict(fx.CALL), dict(CALL_B)],
}

# Paths that serve several endpoints in one invocation (fbx storage overview).
PATH_SAMPLES = {
    "storage/disk/": [dict(fx.DISK)],
    "storage/partition/": [dict(fx.PARTITION)],
    "storage/raid/": [dict(fx.RAID)],
    "/api_version": {"success": True,
                     "result": {"api_version": "12.0", "device_name": "Freebox Server",
                                "box_model": "fbxgw8-r1", "firmware_version": "4.8.6",
                                "api_base_url": "/api/"}},
}

SLOT_VALS = {"bssid": "aa:bb:cc:11:22:33", "apid": "1", "ts": "1762500000",
             "task_id": "3", "name": "syn-license", "contact_id": "1",
             "server_id": "1", "user_id": "1", "feed_id": "1", "group_id": "1"}

ERROR_CASES = [
    ("invalid session",
     {"success": False, "error_code": "auth", "msg": "Invalid session"},
     "The session cookie expired. `fbx` re-authenticates once automatically "
     "(fresh challenge + login) before surfacing this; if it persists, run "
     "`fbx login`."),
    ("box unreachable",
     {"success": False, "msg": "unreachable: [Errno 65] no route to host"},
     "The box did not answer. Check the address (`FREEBOX_HOST`, default "
     "`fd0f:ee:b0::1`) and that you are on the box's LAN."),
    ("validation error",
     {"success": False, "error_code": "invalid", "msg": "unknown or invalid field"},
     "A body field the box does not accept. Field names come straight from "
     "docs/api/ — `fbx api` is the escape hatch for anything undocumented."),
]


# --- the mocked transport

_CURRENT = {"envelope": {"success": True, "result": None}}


def _fake_call(path, data=None, headers=None, method=None, form=False, timeout=20):
    for prefix, sample in PATH_SAMPLES.items():
        if path.startswith(prefix):
            return {"success": True, "result": sample}
    return dict(_CURRENT["envelope"])


def _deny(*a, **k):
    raise AssertionError(f"wiki generation never touches the network ({a})")


def install_mock():
    http.call = _fake_call
    http.call_raw = _deny
    http.call_body = _deny
    auth.login = lambda force=False, password=None: "FBXSID=synthetic-session"
    auth.load_password = _deny


# --- sample synthesis (type-driven; obviously fake values)

def _scalar(col, i):
    c = col.lower()
    if c in ("mac", "bssid") or c.endswith("_mac"):
        return f"aa:bb:cc:00:00:{0x40 + i:02x}"
    if "ip" in c or "addr" in c:
        return f"192.168.1.{50 + i}"
    if c in ("state", "status"):
        return "up"
    if c in ("enabled", "active", "reachable", "present", "spinning", "allowed",
             "persistent", "degraded", "forced"):
        return True
    if "port" in c:
        return 8080 + i
    if "rate" in c:
        return 5_242_880 * (i + 1)
    if "temp" in c:
        return 50 + i
    if c in ("proto", "ip_proto", "protocol"):
        return "tcp"
    if c in ("type", "media", "mode"):
        return "auto"
    if c in ("model", "vendor"):
        return "ACME"
    if c in ("hostname", "name", "label", "title"):
        return f"device-{chr(97 + i)}"
    if c in ("description", "comment", "desc", "note"):
        return f"synthetic entry {i + 1}"
    if c in ("id", "uid", "number"):
        return i + 1
    if "bytes" in c or "size" in c:
        return 2_000_000_000_000 - i
    if "duration" in c:
        return 3600 + i
    return f"syn-{col.replace('_', '-')}"


def synth_row(rec, i):
    if rec.custom == "connection":
        return dict(fx.CONNECTION)
    if rec.custom == "system":
        return copy.deepcopy(fx.SYSTEM_NESTED)
    if rec.cols:
        return {c: rec.units.get(c) and {  # units are applied by the renderer
                   "bytes": 2_000_000_000_000 - i,
                   "rate": 5_242_880 * (i + 1),
                   "dur": 3600 + i * 60,
                   "ts": 1_762_500_000 + i * 60,
                   "pct": 42,
               }.get(rec.units[c]) or _scalar(c, i)
                for c in rec.cols}
    return {"enabled": True, "state": "up"}


def sample_for(rec, op):
    key = (rec.dom, rec.name, op)
    if key in CUSTOM_SAMPLES:
        return CUSTOM_SAMPLES[key]()
    if op == "L":
        return [synth_row(rec, 0), synth_row(rec, 1)]
    if op in "RGCU":
        return synth_row(rec, 0)
    return None  # D / A: the box answers {"success": true}


def envelope_for(rec, op):
    res = sample_for(rec, op)
    if rec.root and rec.root != "result" and res is not None:
        parts = rec.root.split(".")[1:]
        node = {}
        res_wrapped = node
        for p in parts[:-1]:
            node[p] = {}
            node = node[p]
        node[parts[-1]] = res
        res = res_wrapped
    return {"success": True, "result": res}


# --- CLI invocation per (record, op)

def cli_args(rec, op):
    args = [rec.dom]
    if len(rec.ops) > 1:
        args += [rec.name, OP_LEAF[op]]
    else:
        args += [rec.name]
    for s in rec.slots:
        if s not in rec.defaults:
            args.append(SLOT_VALS.get(s, f"{s}-1"))
    if op in "GUD" and not rec.singleton:
        args.append("1")
    if op in "CU":
        cols = [c for c in (rec.cols or []) if c != "id"][:2]
        for c in cols:
            v = synth_row(rec, 0)[c]
            v = ("true" if v is True else "false" if v is False else str(v))
            args.append(f"{c}={v}")
    if rec.gate and op in rec.gate:
        args.append("--yes")
    return args


def usage_line(rec, op):
    a = ["fbx", rec.dom]
    if len(rec.ops) > 1:
        a += [rec.name, OP_LEAF[op]]
    else:
        a += [rec.name]
    for s in rec.slots:
        if s in rec.defaults:
            continue
        a.append(f"<{s}>")
    if op in "GUD" and not rec.singleton:
        a.append("<id>")
    if op in "CU":
        a.append("[key=value …]")
    if rec.gate and op in rec.gate:
        a.append("--yes")
    return " ".join(a)


def run_cli(args, expect_fail=False):
    r = CliRunner().invoke(app, args)
    if expect_fail:
        if r.exit_code == 0:
            raise RuntimeError(f"fbx {' '.join(args)} was expected to fail")
        return r.output.rstrip("\n")
    if r.exit_code != 0:
        raise RuntimeError(f"fbx {' '.join(args)} exited {r.exit_code}:\n"
                           f"{type(r.exception).__name__ if r.exception else ''} {r.output}")
    return r.output.rstrip("\n")


# --- page rendering

def page_for(dom):
    recs = BY_DOMAIN[dom]
    n_ops = sum(len(r.ops) for r in recs)
    lines = [
        f"<!-- synthetic fixture, regenerated by tools/gen_wiki.py — do not edit -->",
        "",
        f"# `fbx {dom}` — command reference",
        "",
        "> All examples below are **synthetic fixtures** regenerated from the",
        "> endpoint records (`fbx_cli/domains/`) and the response models in",
        "> `docs/api/`. No live box data, ever. Regenerate with",
        "> `python tools/gen_wiki.py`.",
        "",
        f"{len(recs)} records, {n_ops} operations.",
        "",
    ]
    for rec in recs:
        head = f"`fbx {dom} {rec.name}`" if len(rec.ops) > 1 else f"`fbx {dom} {rec.name}`"
        lines += [f"## {head}", ""]
        if rec.note:
            lines += [rec.note, ""]
        lines += [f"- docs/api: `{rec.path}`", ""]
        for op in rec.ops:
            env = envelope_for(rec, op)
            _CURRENT["envelope"] = env
            out = run_cli(cli_args(rec, op))
            gated = " *(gated: add `--yes`)*" if rec.gate and op in rec.gate else ""
            lines += [
                f"### `{usage_line(rec, op)}`{gated}",
                "",
                f"`{method_for(op)} {rec.path}`",
                "",
                "Response (synthetic):",
                "",
                "```json",
                json.dumps(env, sort_keys=True, indent=2, ensure_ascii=False),
                "```",
                "",
                "Terminal:",
                "",
                "```text",
                out,
                "```",
                "",
            ]
        if rec.alias:
            lines += [f"Alias: `fbx {rec.alias}` (root-level shorthand).", ""]
    # error examples, once per page, on the page's first read op
    demo = next((r for r in recs if set(r.ops) & set("RL")), recs[0])
    op = demo.ops[0]
    lines += ["## When it fails", "",
              f"Examples on `fbx {dom} {demo.name}`"
              + (f" {OP_LEAF[op]}" if len(demo.ops) > 1 else "") + " — the error",
              "envelope is exactly what the box answers; the CLI prints",
              "`<domain> <record> <op> failed: <msg>` and exits non-zero.", ""]
    for title, resp, note in ERROR_CASES:
        _CURRENT["envelope"] = resp
        args = cli_args(demo, op)
        if demo.gate and op in demo.gate and "--yes" not in args:
            args.append("--yes")
        out = run_cli(args, expect_fail=True)
        lines += [f"**{title}**", "", "```text", out, "```", "", note, ""]
    if dom == "storage":
        _CURRENT["envelope"] = {"success": True, "result": None}
        out = run_cli(["storage", "overview"])
        lines += ["## `fbx storage overview`", "",
                  "Handwritten combined view — disks, partitions and raid in one screen.",
                  "", "```text", out, "```", ""]
    if dom == "fs":
        lines += ["## Binary transfer", "",
                  "`fbx fs get <path> [-o out]` and `fbx fs put <file> [dirname]` move",
                  "file bytes, not JSON — no rendered example here. See `docs/api/06-fs.md`.",
                  ""]
    return lines


CORE_PAGE = """<!-- synthetic fixture, regenerated by tools/gen_wiki.py — do not edit -->

# Core commands

> Synthetic fixtures only — regenerated alongside the domain pages.

## `fbx version`

Unauthenticated `GET /api_version` — the reachability check, no login.

```text
{version_out}
```

## `fbx login`

Reads the password from 1Password (`op read`, item from `FREEBOX_OP_REF`) or
`--stdin`, evaluates the box's challenge via a one-shot `node` subprocess and
stores the session cookie `chmod 600` under `~/.config/freebox/session/`.
Nothing is printed but a confirmation; the password never touches argv or disk.

```text
$ fbx login
session stored (chmod 600, cookie never displayed)
```

## `fbx logout`

Ends the panel session (`POST login/logout`) and drops the local cookie file.

## `fbx api METHOD PATH [JSON-or-form]`

Generic authenticated escape hatch — anything the generated commands miss.

```sh
fbx api GET connection/xdsl/
fbx api POST system/reboot/          # gated surfaces still need --yes
```
"""


def demo_blocks():
    """The three README demo sessions (synthetic, deterministic)."""
    _CURRENT["envelope"] = {"success": True,
                            "result": dict(PATH_SAMPLES["/api_version"]["result"])}
    v = run_cli(["version"])
    _CURRENT["envelope"] = envelope_for(BY_DOMAIN["wifi"][0], "R")  # wifi state
    w = run_cli(["wifi", "status"])
    samba = next(r for r in BY_DOMAIN["fw"] if r.name == "samba")
    _CURRENT["envelope"] = envelope_for(samba, "R")
    s = run_cli(["fw", "samba", "show"])
    return v, w, s


def main():
    install_mock()
    if "--demo" in sys.argv:
        v, w, s = demo_blocks()
        print("===VERSION===")
        print(v)
        print("===WIFI===")
        print(w)
        print("===SAMBA===")
        print(s)
        return
    OUT.mkdir(parents=True, exist_ok=True)
    for stale in OUT.glob("*.md"):
        stale.unlink()
    for dom in sorted(BY_DOMAIN):
        (OUT / f"{dom}.md").write_text("\n".join(page_for(dom)) + "\n")
    version_out = run_cli(["version"])
    (OUT / "core.md").write_text(CORE_PAGE.format(version_out=version_out))
    print(f"wrote {len(list(OUT.glob('*.md')))} pages to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
