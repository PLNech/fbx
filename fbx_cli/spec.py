"""Spec-driven endpoints: every documented panel endpoint as one compact record.

One Rec per (path, verb-set), transcribed verbatim from docs/api/ (the
clean-room source of truth). The generic engine (engine.py) turns each Rec
into typer commands; handwritten renderers only where the generic one is
genuinely worse (custom key).

Record fields:
  dom         domain group (fbx <dom> ...)
  name        command slug inside the domain
  path        URL template, relative to /api/latest, exactly as documented
              (trailing slashes are inconsistent upstream — transcribed as-is);
              "{slot}" = path param (the docs' {foreignId} pattern)
  ops         letters: L=list GET, R=read GET, G=get-one GET, C=create POST,
              U=update PUT, D=delete DELETE, A=action POST
  singleton   write ops hit the path itself, no trailing <id>
  cols/units  render hints (units: bytes|rate|dur|ts|pct)
  name_field  the row's human label
  gate        destructive: these ops require --yes (default "DA")
  form        POST body is form-encoded, not JSON
  root        result root ("result.entries" for the fs tree proxy)
  custom      handwritten renderer key (custom.py)
  defaults    path-param defaults (e.g. the default TV bouquet)
  alias       extra root-level command name (fbx connection, fbx calls ...)
  note        provenance/gap note surfaced in the command help
"""
import re

RECORDS = []
BY_DOMAIN = {}


class Rec:
    def __init__(self, dom, name, path, ops, *, singleton=False, cols=None,
                 units=None, name_field=None, gate=False, form=False,
                 root="result", custom=None, defaults=None, alias=None,
                 note=None):
        self.dom, self.name, self.path, self.ops = dom, name, path, ops
        self.singleton, self.cols, self.units = singleton, cols, units or {}
        self.name_field, self.gate, self.form = name_field, ("DA" if gate is True else (gate or "")), form
        self.root, self.custom, self.defaults = root, custom, defaults or {}
        self.alias, self.note = alias, note
        RECORDS.append(self)
        BY_DOMAIN.setdefault(dom, []).append(self)

    @property
    def slots(self):
        return re.findall(r"{(\w+)}", self.path)

    def help(self):
        return self.note or self.path


def add(*recs):
    for r in recs:
        RECORDS.append(r)
        BY_DOMAIN.setdefault(r.dom, []).append(r)
