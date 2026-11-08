"""Formatting: human units, rich tables (style-free when not a TTY), generic renderers."""
import time

from rich.console import Console
from rich.table import Table

console = Console()


def hb(n):
    """Human bytes."""
    if n is None:
        return "-"
    n = float(n)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if abs(n) < 1024 or unit == "TiB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024


def hr(n):
    """Human rate (bytes/s assumed; units are not documented in docs/api/)."""
    if n is None:
        return "-"
    return f"{hb(n)}/s"


def hdur(s):
    """Human duration."""
    if s is None:
        return "-"
    s = int(s)
    d, s = divmod(s, 86400)
    h, s = divmod(s, 3600)
    m, _ = divmod(s, 60)
    parts = []
    if d:
        parts.append(f"{d}d")
    if h or d:
        parts.append(f"{h}h")
    parts.append(f"{m}m")
    return " ".join(parts)


def hts(epoch):
    """Epoch -> local time, or '-'."""
    if not epoch:
        return "-"
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(int(epoch)))


def hpct(v):
    if v is None:
        return "-"
    return f"{float(v):g}%"


UNIT_FN = {"bytes": hb, "rate": hr, "dur": hdur, "ts": hts, "pct": hpct}


def cut(s, n=40):
    s = str(s if s is not None else "")
    return s[: n - 1] + "…" if len(s) > n else s


DETAIL_HINT = " (--json for full detail)"


def compact(v, depth=0):
    """Nested dict/list as one compact line: `k=v, k=v, k=v … +N more`.
    The `{N keys}`-style shrug cell is banned; callers append DETAIL_HINT so
    nothing truncated or nested disappears silently."""
    if isinstance(v, dict):
        if depth >= 2:
            return "…"
        items = [f"{k}={compact(x, depth + 1)}" for k, x in v.items()]
        body = ", ".join(items[:3])
        more = len(items) - 3
        return body + (f" … +{more} more" if more > 0 else "")
    if isinstance(v, (list, tuple)):
        if depth >= 2:
            return "…"
        items = [compact(x, depth + 1) for x in v[:3]]
        body = ", ".join(items)
        more = len(v) - 3
        return body + (f" … +{more} more" if more > 0 else "")
    if isinstance(v, bool):
        return "yes" if v else "no"
    if v is None:
        return "-"
    return cut(v, 24)


def fmt_cell(v, unit=None):
    if isinstance(v, (dict, list)):
        return compact(v) + DETAIL_HINT
    if isinstance(v, bool):
        return "yes" if v else "no"
    if unit in UNIT_FN:
        return UNIT_FN[unit](v)
    out = cut(v)
    if out != str(v if v is not None else ""):
        return out + DETAIL_HINT  # long strings truncate explicitly, never silently
    return out


def cellstr(s):
    return str(s) if s is not None else "-"
