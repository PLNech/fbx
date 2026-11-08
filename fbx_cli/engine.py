"""The generic engine: Rec -> typer commands -> one HTTP call -> rendered result.

Command naming: a single-op record is one leaf command (`fbx wifi state`);
a multi-op record is a sub-group with leaves named by op
(list/show/get/add/set/rm/run). Body fields arrive as key=value pairs and are
auto-typed (int, float, bool, null, JSON); on GETs they become query params.
"""
import json
import re
from typing import List, Optional

import typer

from . import auth, http
from .custom import CUSTOM
from .fmt import cellstr
from .render import dump_json, render_result
from .spec import BY_DOMAIN

OP_LEAF = {"L": "list", "R": "show", "G": "get", "C": "add", "U": "set",
           "D": "rm", "A": "run"}


def parse_value(raw):
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        return raw


def parse_pairs(values):
    """key=value argv pairs -> dict. `k=` -> empty string, bare `k` -> None."""
    body = {}
    for v in values or []:
        k, sep, raw = v.partition("=")
        body[k] = parse_value(raw) if sep else None
    return body


def resolve_path(rec, op, slots, item_id):
    path = rec.path
    for k, v in slots.items():
        path = path.replace("{" + k + "}", str(v))
    if "{" in path:
        raise typer.BadParameter(f"missing value for path slot in {path!r}")
    if op in "GUD" and not rec.singleton:
        path = path.rstrip("/") + "/" + str(item_id)
    return path


def method_for(op):
    return {"L": "GET", "R": "GET", "G": "GET", "C": "POST",
            "U": "PUT", "D": "DELETE", "A": "POST"}[op]


def run(rec, op, values=None, item_id=None, yes=False, **slots):
    body = parse_pairs(values)
    path = resolve_path(rec, op, slots, item_id)
    data = None if method_for(op) == "GET" else (body or None)
    if method_for(op) == "GET" and body:
        qs = "&".join(f"{k}={v}" for k, v in body.items())
        path = f"{path}{'&' if '?' in path else '?'}{qs}"
    if rec.gate and op in rec.gate and not (yes or _yes_flag()):
        raise typer.Exit(f"refusing a destructive op without --yes "
                         f"({method_for(op)} {path})")
    resp = auth.authed(path, data, method_for(op), form=rec.form)
    if http.JSON_MODE:
        dump_json(resp)
        return
    if not resp.get("success"):
        msg = resp.get("msg") or resp.get("error_code") or resp
        hint = ""
        if method_for(op) == "GET" and str(resp.get("error_code", "")) in ("unknown", "notfound"):
            hint = "\n(endpoint not in docs; try `fbx api` as the escape hatch)"
        raise typer.Exit(f"{rec.dom} {rec.name} {OP_LEAF[op]} failed: {msg}{hint}")
    if rec.custom and rec.custom in CUSTOM:
        CUSTOM[rec.custom](resp.get("result"))
    else:
        render_result(resp, rec, op)


_yes = False


def set_yes(flag):
    global _yes
    _yes = flag


def _yes_flag():
    return _yes


# ---------------------------------------------------- typer command factory

def _make_fn(rec, op):
    """Build a typed typer command function for (rec, op) via exec: path slots
    become positional args, an id arg joins for get/set/rm on collections, and
    `values` takes the key=value body pairs."""
    slots = rec.slots
    need_id = op in "GUD" and not rec.singleton
    params, names = [], []
    for s in slots:
        default = rec.defaults.get(s)
        arg = f"typer.Argument({default!r})" if default is not None else "typer.Argument(...)"
        params.append(f"{s}: str = {arg}")
        names.append(f'"{s}": {s}')
    if need_id:
        params.append("item_id: str = typer.Argument(..., help='record id')")
        names.append('"item_id": item_id')
    params.append("values: Optional[List[str]] = typer.Argument(None, "
                  "help='body fields as key=value (auto-typed)')")
    names.append('"values": values')
    if op in rec.gate:
        params.append("yes: bool = typer.Option(False, '--yes', "
                      "help='confirm the destructive op')")
        names.append('"yes": yes')
    ns = {"typer": typer, "List": List, "Optional": Optional, "_rec": rec, "_op": op,
          "_run": run}
    src = (f"def _fn({', '.join(params)}) -> None:\n"
           f"    _run(_rec, _op, **{{{', '.join(names)}}})")
    exec(src, ns)
    return ns["_fn"]


def build(app):
    """Register every domain group and its generated commands; return the groups."""
    groups = {}
    for dom in sorted(BY_DOMAIN):
        recs = BY_DOMAIN[dom]
        g = typer.Typer(help=f"{dom} — documented endpoints: "
                             f"{len({r.path for r in recs})}", no_args_is_help=True)
        app.add_typer(g, name=dom)
        groups[dom] = g
        for rec in recs:
            if len(rec.ops) == 1:
                g.command(rec.name, help=rec.help())(_make_fn(rec, rec.ops))
                continue
            sub = typer.Typer(help=rec.help(), no_args_is_help=True)
            g.add_typer(sub, name=rec.name)
            for op in rec.ops:
                sub.command(OP_LEAF[op], help=f"{method_for(op)} {rec.path}")(
                    _make_fn(rec, op))
        for rec in recs:
            if rec.alias:
                op = rec.ops
                app.command(rec.alias, help=f"(= fbx {dom} {rec.name}) "
                                            f"{rec.help()}")(_make_fn(rec, op))
    return groups
