"""fbx, the command line into your Freebox OS. Everything the web panel can see,
so does `fbx` (spec-driven off docs/api/, ~190 endpoints)."""
import json
import sys
from pathlib import Path
from typing import Optional

import typer

from . import __version__, auth, config, engine, http
from .fmt import console, hb, cut, cellstr
from .render import dump_json, render_list

app = typer.Typer(no_args_is_help=True,
                  context_settings={"help_option_names": ["-h", "--help"]},
                  help="Full-coverage CLI into your own Freebox OS box. "
                       "Global flags: --json (raw envelope), --debug (method+path+status), "
                       "--yes (gate destructive ops). Domains below; `fbx api` is the escape "
                       "hatch; `fbx tldr` for ten starter examples.")


@app.callback()
def _root(json_mode: bool = typer.Option(False, "--json", help="pass the raw response envelope through"),
          debug: bool = typer.Option(False, "--debug", help="print method+path+status of each call (never bodies)"),
          yes: bool = typer.Option(False, "--yes", help="confirm a destructive op (storage/raid/fs rm/reboot...)")):
    http.JSON_MODE = json_mode or http.JSON_MODE
    http.DEBUG = debug or http.DEBUG
    engine.set_yes(yes or engine._yes_flag())


@app.command()
def version():
    """Unauthenticated GET /api_version, the reachability check (no login)."""
    resp = http.call("/api_version")
    if http.JSON_MODE:
        dump_json(resp)
        return
    if isinstance(resp, dict) and "success" not in resp and "api_version" in resp:
        r = resp
    elif resp.get("success"):
        r = resp.get("result", {})
    else:
        raise typer.Exit(f"version check failed: {resp.get('msg') or resp}")
    for k in ("api_version", "device_name", "box_model", "firmware_version", "api_base_url"):
        if k in r:
            console.print(f"  {k:18s} {r[k]}")


@app.command()
def login(stdin: bool = typer.Option(False, "--stdin", help="read the password from stdin instead of 1Password")):
    """Panel-dialect session login (cookie stored chmod 600, never printed)."""
    pw = sys.stdin.readline().rstrip("\n") if stdin else auth.load_password()
    auth.login(force=True, password=pw)
    if not http.JSON_MODE:
        console.print("session stored (chmod 600, cookie never displayed)")


@app.command()
def logout():
    """POST login/logout: end the panel session and drop the local cookie file."""
    resp = http.call("login/logout", method="POST", headers={"Cookie": auth.login()})
    if config.SESSION_FILE.exists():
        config.SESSION_FILE.unlink()
    console.print("logged out" if resp.get("success") else
                  f"logout answered: {resp.get('msg') or resp} (local cookie dropped anyway)")


# tldr: ten starter examples. Every line is verified against the spec records
# (tests/test_ux.py executes each one against fixtures, so tldr cannot rot).
TLDR = [
    ("check the box is reachable (no login needed)", "fbx version"),
    ("authenticate: password from --stdin or 1Password, never argv",
     "fbx login --stdin"),
    ("WAN state, IPs, live rates", "fbx wan"),
    ("global wifi state (the quick-toggle)", "fbx status"),
    ("wifi access points / phys", "fbx wifi ap"),
    ("port forwards", "fbx fw redir list"),
    ("Samba / Windows file-sharing config", "fbx fw samba show"),
    ("box health: temps, fans, uptime", "fbx system health"),
    ("disks + partitions + raid in one screen", "fbx storage overview"),
    ("escape hatch: any documented endpoint, raw",
     "fbx api GET connection/xdsl/"),
]


@app.command()
def tldr():
    """Ten copy-pasteable examples to start with."""
    for note, cmd in TLDR:
        console.print(f"[dim]# {note}[/dim]")
        console.print(cmd)
        console.print()


@app.command()
def api(method: str = typer.Argument(..., help="GET|POST|PUT|DELETE"),
        path: str = typer.Argument(..., help="path under /api/latest (or /absolute)"),
        body: Optional[str] = typer.Argument(None, help="JSON body (or key=value pairs for form posts)")):
    """Generic authenticated escape hatch: anything the generated commands miss."""
    data = json.loads(body) if body and body.strip().startswith(("{", "[")) else body
    form = isinstance(data, str) and data and "=" in data and not data.strip().startswith(("{", "["))
    if form:
        data = dict(p.split("=", 1) for p in data.split("&"))
    print(json.dumps(auth.authed(path, data, method.upper(), form=form),
                     indent=2, ensure_ascii=False))


def _soft(resp, what):
    """Sub-call of a multi-endpoint custom command: optional, degrades loudly
    but locally. One dead endpoint yields a dim warn line, the rest renders."""
    if resp.get("success"):
        return resp.get("result")
    why = resp.get("msg") or resp.get("error_code") or resp
    status = getattr(http, "LAST_STATUS", None)
    if status:
        why = f"{why} (HTTP {status})"
    if not http.JSON_MODE:  # in JSON mode errors ride the "errors" dict instead
        console.print(f"[dim]{what}: unavailable (box error: {why})[/dim]")
    return None


def storage_overview():
    """Combined storage view: disks + partitions + RAID (three endpoints, one screen).
    Registered inside the storage group as `fbx storage overview`. Each sub-call
    is optional: a failing one degrades to a warn line (e.g. raid/ answering
    HTTP 500 on a box with no array), a total failure fails loudly."""
    disk_resp = auth.authed("storage/disk/")
    disks = _soft(disk_resp, "disks") or []
    part_resp = auth.authed("storage/partition/")
    parts = _soft(part_resp, "partitions") or []
    raid_resp = auth.authed("storage/raid/")
    raids = _soft(raid_resp, "raid") or []
    if http.JSON_MODE:
        dump_json({"disks": disks, "partitions": parts, "raids": raids,
                   "errors": {w: (r.get("msg") or r.get("error_code"))
                              for w, r in (("disks", disk_resp), ("partitions", part_resp),
                                           ("raid", raid_resp)) if not r.get("success")}})
        return
    if disks:
        render_list([[cellstr(d.get("id")), cut(d.get("model") or d.get("title") or "-", 24),
                      cellstr(d.get("state")), cellstr(d.get("temp")), hb(d.get("total_bytes"))]
                     for d in disks],
                    cols=["id", "model", "state", "temp", "total"], title="disks")
    if parts:
        render_list([[cellstr(p.get("id")), cut(p.get("label") or "-", 16),
                      cellstr(p.get("state")), cut(p.get("path") or "-", 24),
                      cellstr(p.get("fstype")), hb(p.get("free_bytes"))]
                     for p in parts],
                    cols=["id", "label", "state", "path", "fs", "free"], title="partitions")
    if raids:
        render_list([[cellstr(r.get("id")), cellstr(r.get("name")), cellstr(r.get("level")),
                      cellstr(r.get("state")), cellstr(r.get("degraded")), hb(r.get("array_size"))]
                     for r in raids],
                    cols=["id", "name", "level", "state", "degraded", "size"], title="raid")
    if not (disks or parts or raids):
        raise typer.Exit("storage overview failed: the box answered none of "
                         "disk/, partition/ or raid/ (see the warn lines above)")


def _ok(resp, what):
    if not resp.get("success"):
        raise typer.Exit(f"{what} failed: {resp.get('msg') or resp.get('error_code') or resp}")
    return resp.get("result")


# --- binary file helpers, appended into the spec-driven `fs` domain group ---

def fs_get(path: str = typer.Argument(..., help="box path, e.g. Lgd/iso/debian.iso"),
           out: Path = typer.Option(None, "-o", "--out", help="output file (default: basename)"),
           inline: bool = typer.Option(False, "--inline", help="ask the box to serve inline")):
    """Download a file from the box (GET dl/<path>?inline=…)."""
    cookie = auth.login()
    data = http.call_raw(f"dl/{path}?inline={1 if inline else 0}", headers={"Cookie": cookie})
    dest = out or Path(path).name
    dest.write_bytes(data)
    console.print(f"wrote {len(data)} bytes -> {dest}")


def _multipart(fields, boundary):
    import mimetypes
    body = b""
    for name, fname, data in fields:
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\""
                 + (f"; filename=\"{fname}\"" if fname else "") + "\r\n"
                 + f"Content-Type: {mimetypes.guess_type(fname or name)[0] or 'text/plain'}\r\n\r\n"
                 ).encode() + data + b"\r\n"
    return body + f"--{boundary}--\r\n".encode()


def fs_put(file: Path = typer.Argument(..., exists=True, dir_okay=False),
           dirname: str = typer.Argument("/", help="destination dir on the box"),
           force: str = typer.Option(None, "--force", help="overwrite|resume on conflict")):
    """Upload a file (documented multipart fallback: POST upload/ -> upload/<id>/send)."""
    import uuid
    cookie = auth.login()
    boundary = uuid.uuid4().hex
    fields = [("file", file.name, file.read_bytes()),
              ("dirname", "", dirname.encode()),
              ("MAX_FILE_SIZE", "", b"4194304000"),
              ("csrf_token", "", b"")]
    body = _multipart(fields, boundary)
    headers = {"Cookie": cookie, "Content-Type": f"multipart/form-data; boundary={boundary}"}
    resp = http.call_body("upload/", body, headers, method="POST", timeout=600)
    if not resp.get("success"):
        raise typer.Exit(f"upload failed: {resp.get('msg') or resp.get('error_code') or resp}")
    up_id = (resp.get("result") or {}).get("id")
    if force and up_id is not None:
        fields.append(("force", "", force.encode()))
        resp = http.call_body(f"upload/{up_id}/send", _multipart(fields, boundary),
                              headers, method="POST", timeout=600)
        if not resp.get("success"):
            raise typer.Exit(f"upload send failed: {resp.get('msg') or resp}")
    console.print(f"uploaded -> upload id {up_id}")


def build():
    """Import the spec (registers every record), generate the domain commands,
    then hang the handwritten helpers into their groups."""
    from . import domains  # noqa: F401 (the record registrations)
    groups = engine.build(app)
    fs_group = groups.get("fs")
    if fs_group is not None:
        fs_group.command("get", help="GET dl/<path>: download a file")(fs_get)
        fs_group.command("put", help="multipart upload (POST upload/)")(fs_put)
    st_group = groups.get("storage")
    if st_group is not None:
        st_group.command("overview",
                         help="disks + partitions + raid in one screen")(storage_overview)
    return app


def main():
    # Global flags work anywhere on the line: pre-strip them
    # before typer sees argv; the root callback handles group position too.
    argv = sys.argv[1:]
    http.JSON_MODE = "--json" in argv or http.JSON_MODE
    http.DEBUG = "--debug" in argv or http.DEBUG
    engine.set_yes("--yes" in argv or engine._yes_flag())
    sys.argv = [sys.argv[0]] + [a for a in argv if a not in ("--json", "--debug", "--yes")]
    app()


# Build the command tree once at import so tests (CliRunner on `app`) and the
# console entry point see the same fully-registered tree.
app = build()


if __name__ == "__main__":
    main()



