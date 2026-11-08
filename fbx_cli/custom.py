"""Handwritten renderers, only where the generic table is genuinely worse:
connection summary, system health grid, download-task progress, call-log summary,
and the combined storage view (three endpoints in one screen)."""
from .fmt import console, hb, hr, hdur, hts, cut, cellstr
from .render import render_list


def fmt_connection(r):
    state = r.get("state", "?")
    console.print(f"wan: {state}  ({r.get('type', '?')} / {r.get('media', '?')} / mode {r.get('mode', '?')})")
    console.print(f"ipv4: {r.get('ipv4', '-')}    ipv6: {r.get('ipv6', '-')}")
    console.print(f"rate_down {hr(r.get('rate_down'))} / bw_down {hr(r.get('bw_down'))}")
    console.print(f"rate_up   {hr(r.get('rate_up'))} / bw_up   {hr(r.get('bw_up'))}")


def fmt_system(r):
    mi = r.get("model_info") or {}
    ident = " / ".join(str(x) for x in (mi.get("pretty_name") or mi.get("name")
                                        or r.get("box_model"),
                                        r.get("firmware_version")) if x)
    if ident:
        console.print(ident)
    up = r.get("uptime_val", r.get("uptime"))
    if up is not None:
        console.print(f"  {'uptime':18s} {hdur(up)}")
    for k in ("mac", "serial", "disk_status", "user_main_storage"):
        if r.get(k) is not None:
            console.print(f"  {k:18s} {r[k]}")
    # real shape: fans/sensors are arrays of {id,name,value};
    # legacy flat keys (fan_rpm, temp_*) still supported as a fallback.
    fans = [f"{f.get('name','fan')}={f.get('value')}rpm" for f in (r.get("fans") or [])
            if isinstance(f, dict)]
    if r.get("fan_rpm") is not None:
        fans.append(f"fan_rpm={r['fan_rpm']}")
    if fans:
        console.print("  fans:  " + "  ".join(fans))
    sensors = {s.get("name", f"sensor{s.get('id')}"): s.get("value")
               for s in (r.get("sensors") or []) if isinstance(s, dict)}
    temps = {k: v for k, v in r.items()
             if k.startswith("temp_") and isinstance(v, (int, float))}
    if sensors or temps:
        pairs = [f"{k}={v}" for k, v in sorted({**sensors, **temps}.items())]
        console.print("  sensors: " + "  ".join(pairs))


def fmt_tasks(tasks):
    if not tasks:
        console.print("no download tasks")
        return
    rows = []
    for t in tasks:
        pct = t.get("progress")
        pct = f"{pct:.0f}%" if isinstance(pct, (int, float)) else "-"
        rows.append([cellstr(t.get("id", "-")), cut(t.get("name") or "-", 44),
                     cellstr(t.get("status", "-")), pct, hr(t.get("rx_speed")),
                     hr(t.get("tx_speed")), hb(t.get("size"))])
    render_list(rows, cols=["id", "name", "status", "progress", "rx_speed", "tx_speed", "size"],
                title="downloads")


def fmt_calls(entries):
    if not entries:
        console.print("no calls in the log")
        return
    counts = {}
    for e in entries:
        counts[e.get("type", "?")] = counts.get(e.get("type", "?"), 0) + 1
    new = sum(1 for e in entries if e.get("new"))
    summary = "  ".join(f"{k}={v}" for k, v in sorted(counts.items()))
    console.print(f"call log: {len(entries)} entries ({summary}; new={new})")
    rows = []
    for e in sorted(entries, key=lambda x: x.get("datetime", 0), reverse=True)[:15]:
        rows.append([hts(e.get("datetime")), cellstr(e.get("type", "-")),
                     cellstr(e.get("number") or "-"), cut(e.get("name") or "-", 20),
                     hdur(e.get("duration", 0)), "new" if e.get("new") else ""])
    render_list(rows, cols=["datetime", "type", "number", "name", "duration", ""], title=None)
    console.print(f"-- last {min(15, len(entries))} shown")


CUSTOM = {"connection": fmt_connection, "system": fmt_system,
          "tasks": fmt_tasks, "calls": fmt_calls}
