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
    """Human rate (bytes/s assumed — units are not documented in docs/api/)."""
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


def fmt_cell(v, unit=None):
    if isinstance(v, (dict, list)):
        if unit == "count" or isinstance(v, list):
            return f"[{len(v)} items]" if v else "[]"
        return f"{{{len(v)} keys}}" if v else "{}"
    if isinstance(v, bool):
        return "yes" if v else "no"
    if unit in UNIT_FN:
        return UNIT_FN[unit](v)
    return cut(v)


def cellstr(s):
    return str(s) if s is not None else "-"
