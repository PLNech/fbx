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

HELP_SETTINGS = {"help_option_names": ["-h", "--help"]}


def parse_value(raw):
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        return raw


def parse_pairs(values, rec=None):
    """key=value argv pairs -> dict. `k=` -> empty string; a bare positional is
    a usage ERROR, never silently swallowed."""
    body = {}
    for v in values or []:
        k, sep, raw = v.partition("=")
        if not sep or not k:
            hint = ""
            if rec is not None:
                verb = "show" if "R" in rec.ops else ("get" if "G" in rec.ops else None)
                if verb:
                    addr = "" if rec.singleton else " <id>"
                    hint = f"; to address one record try `fbx {rec.dom} {rec.name} {verb}{addr}`"
            raise typer.BadParameter(
                f"unexpected argument {v!r} — body fields are key=value{hint}")
        body[k] = parse_value(raw)
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
    body = parse_pairs(values, rec=rec)
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
        status = getattr(http, "LAST_STATUS", None)
        suffix = f" (HTTP {status})" if status else ""
        hint = ""
        if method_for(op) == "GET" and str(resp.get("error_code", "")) in ("unknown", "notfound"):
            hint = "\n(endpoint not in docs; try `fbx api` as the escape hatch)"
        raise typer.Exit(f"{rec.dom} {rec.name} {OP_LEAF[op]} failed: {msg}{suffix}{hint}")
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


def _example(rec):
    """One usage example, generated from the record's REAL ops only (clean-room:
    never invent an endpoint or a flag)."""
    verb = "get" if "G" in rec.ops else ("show" if "R" in rec.ops else None)
    if verb is None:
        return None
    parts = ["fbx", rec.dom, rec.name]
    if len(rec.ops) > 1:
        parts.append(verb)
    if rec.slots or (verb == "get" and not rec.singleton):
        parts += [str(rec.defaults.get(s, 0)) for s in rec.slots]
        if verb == "get" and not rec.singleton:
            parts.append("0")
    return " ".join(parts)


def _domain_example(recs):
    """Prefer a record you can both list and address one of; else any read."""
    ranked = [r for r in recs if "L" in r.ops and set(r.ops) & set("RG")]
    for rec in ranked + [r for r in recs if r not in ranked]:
        ex = _example(rec)
        if ex:
            return f"e.g. {ex}"
    return None


def build(app):
    """Register every domain group and its generated commands; return the groups."""
    groups = {}
    for dom in sorted(BY_DOMAIN):
        recs = BY_DOMAIN[dom]
        g = typer.Typer(help=f"{dom} — documented endpoints: "
                             f"{len({r.path for r in recs})}",
                        epilog=_domain_example(recs), no_args_is_help=True,
                        context_settings=HELP_SETTINGS)
        app.add_typer(g, name=dom)
        groups[dom] = g
        for rec in recs:
            ex = _example(rec)
            if len(rec.ops) == 1:
                g.command(rec.name, help=rec.help(),
                          context_settings=HELP_SETTINGS)(_make_fn(rec, rec.ops))
                continue
            sub = typer.Typer(help=rec.help(),
                              epilog=f"e.g. {ex}" if ex else None,
                              no_args_is_help=True, context_settings=HELP_SETTINGS)
            g.add_typer(sub, name=rec.name)
            for op in rec.ops:
                sub.command(OP_LEAF[op], help=f"{method_for(op)} {rec.path}",
                            context_settings=HELP_SETTINGS)(_make_fn(rec, op))
        for rec in recs:
            if rec.alias:
                op = rec.ops
                app.command(rec.alias, help=f"(= fbx {dom} {rec.name}) "
                                            f"{rec.help()}",
                            context_settings=HELP_SETTINGS)(_make_fn(rec, op))
    return groups
