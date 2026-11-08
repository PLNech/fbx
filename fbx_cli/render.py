"""Generic renderers: one shape per documented response model, hints from the spec."""
import json

from rich.table import Table

from .fmt import console, fmt_cell, cellstr


def render_list(rows, cols=None, units=None, title=None):
    """A collection GET rendered as a rich table (no colors when not a TTY)."""
    t = Table(box=None, title=title, header_style=None)
    if not cols and rows and isinstance(rows[0], dict):
        seen = {}
        for r in rows:
            for k in r:
                seen.setdefault(k, 0)
                seen[k] += 1
        cols = [k for k, n in seen.items() if n == len(rows)] or list(rows[0])
    units = units or {}
    for c in cols:
        t.add_column(c, overflow="fold")
    for r in rows or []:
        t.add_row(*[cellstr(fmt_cell(r.get(c), units.get(c))) if isinstance(r, dict) else cellstr(r)
                    for c in cols])
    console.print(t)
    if rows is not None:
        console.print(f"-- {len(rows)} entries")


def render_kv(obj, title=None):
    """A singleton dict rendered as key: value lines."""
    if title:
        console.print(title)
    for k in sorted(obj):
        v = obj[k]
        if isinstance(v, (dict, list)):
            console.print(f"  {k:26s} [list:{len(v)}]" if isinstance(v, list) else f"  {k:26s} {{…}}")
        else:
            console.print(f"  {k:26s} {v}")


def render_result(resp, rec=None, op=None):
    """Route a documented response payload to the right renderer, hints from rec."""
    res = resp.get("result")
    if rec is not None and rec.root and rec.root != "result" and isinstance(res, dict):
        # e.g. root="result.entries": the fs/ls tree proxy nests the rows one down
        for part in rec.root.split(".")[1:]:
            res = (res or {}).get(part) if isinstance(res, dict) else None
    if res is None:
        console.print("(empty result)")
        return
    if isinstance(res, list):
        render_list(res, cols=rec.cols if rec else None,
                    units=rec.units if rec else None,
                    title=f"{rec.dom} {rec.name}" if rec else None)
    elif isinstance(res, dict):
        if op in ("L",) or all(isinstance(v, (list, dict)) for v in res.values()):
            entries = next((v for v in res.values() if isinstance(v, list)), None)
            if entries is not None and rec is not None:
                render_list(entries, cols=rec.cols, units=rec.units)
                return
        render_kv(res)
    else:
        console.print(res)


def dump_json(resp):
    console.print(json.dumps(resp, indent=2, ensure_ascii=False))
