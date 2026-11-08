"""One HTTP layer: cookie jar, panel header, JSON/form bodies, raw streams.

Small, dependency-free HTTP layer over urllib with a cookie jar.
A path starting with '/' is absolute against the box root (e.g. /api_version,
which lives OUTSIDE /api/latest unlike every documented panel endpoint).
"""
import http.cookiejar
import json
import urllib.error
import urllib.parse
import urllib.request

from . import config

JSON_MODE = False   # --json: pass the raw response envelope through untouched
DEBUG = False       # --debug: print method + path + status only (never bodies)
LAST_STATUS = None  # HTTP status of the last real call (None when mocked)

_cj = http.cookiejar.CookieJar()
_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_cj))


def call(path, data=None, headers=None, method=None, form=False, timeout=20):
    """One call against the box. Returns parsed JSON (HTTP errors included)."""
    if path.startswith("/"):
        url = f"http://[{config.BASE_HOST}]{path}"
    else:
        url = f"{config.BASE}/{path.lstrip('/')}"
    if form and data is not None:
        body = urllib.parse.urlencode(data).encode()
        ctype = "application/x-www-form-urlencoded"
    else:
        body = json.dumps(data).encode() if data is not None else None
        ctype = "application/json"
    req = urllib.request.Request(url, data=body, method=method or ("POST" if body else "GET"))
    req.add_header("Content-Type", ctype)
    req.add_header("X-FBX-FREEBOX0S", "1")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    if DEBUG:
        print(f"[fbx] {req.method} {url}")
    try:
        with _opener.open(req, timeout=timeout) as r:
            if DEBUG:
                print(f"[fbx] -> {r.status}")
            globals()["LAST_STATUS"] = r.status
            return json.load(r)
    except urllib.error.HTTPError as e:
        if DEBUG:
            print(f"[fbx] -> HTTP {e.code}")
        globals()["LAST_STATUS"] = e.code
        try:
            return json.load(e)
        except Exception:
            return {"success": False, "msg": f"HTTP {e.code}"}
    except (urllib.error.URLError, OSError) as e:
        globals()["LAST_STATUS"] = None
        return {"success": False, "msg": f"unreachable: {e}"}


def call_raw(path, headers=None, timeout=60):
    """GET that returns the raw bytes (file downloads: dl/<path>, contact/export/)."""
    url = f"{config.BASE}/{path.lstrip('/')}"
    req = urllib.request.Request(url)
    req.add_header("X-FBX-FREEBOX0S", "1")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    if DEBUG:
        print(f"[fbx] GET {url}")
    with _opener.open(req, timeout=timeout) as r:
        return r.read()


def call_body(path, body, headers=None, method="POST", timeout=60):
    """One call with a pre-encoded body (multipart uploads), no JSON wrapping."""
    url = f"{config.BASE}/{path.lstrip('/')}"
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("X-FBX-FREEBOX0S", "1")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    if DEBUG:
        print(f"[fbx] {method} {url} ({len(body)} bytes)")
    try:
        with _opener.open(req, timeout=timeout) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            return json.load(e)
        except Exception:
            return {"success": False, "msg": f"HTTP {e.code}"}
    except (urllib.error.URLError, OSError) as e:
        return {"success": False, "msg": f"unreachable: {e}"}


def cookie_header():
    return "; ".join(f"{c.name}={c.value}" for c in _cj)
