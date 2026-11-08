"""Panel-dialect auth, transcribed from the panel's own login flow.

Login flow (extracted from the panel's login.min.js):
  GET login/  -> challenge (a TABLE of obfuscated JS snippets, one per char) +
                 password_salt
  h_pass = SHA1(salt + password); hash = HMAC-SHA1(key=challenge, msg=h_pass)
  POST login/ (form) -> session cookie, stored chmod 600, never printed.
"""
import getpass
import hashlib
import hmac
import json
import stat
import subprocess
import sys

from . import config, http


def load_password():
    """The password goes 1Password -> memory. Never argv, never stdout, never disk.

    The op:// reference comes from the config ladder: FREEBOX_OP_REF env, then
    the <CFG>/opref file, then the default item."""
    ref = config.load_op_ref()
    try:
        out = subprocess.run(
            ["op", "read", "--no-newline", ref],
            capture_output=True, text=True, timeout=60, check=True,
        )
        return out.stdout
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        sys.exit(f"could not fetch the Freebox password from 1Password ({ref}): {e}")


def challenge_to_string(table):
    """The challenge is a list of ~32 OBFUSCATED JS SNIPPETS the panel eval()s one
    by character (Free's anti-script layer): `s += '' + eval(table[i])`. Each snippet
    yields one character; concatenating the raw code instead of the evaluated result
    hashes garbage and the box answers "Identifiants invalides" forever.

    Evaluate with node (one subprocess, all snippets in one context). The snippets
    come from your own box; they are DATA and nothing else is ever eval'd.
    """
    parts = list(table.values()) if isinstance(table, dict) else list(table)
    script = (
        "const parts=JSON.parse(require('fs').readFileSync(0,'utf8'));"
        "let s='';for(const p of parts){s+=String(eval(p))}process.stdout.write(s)"
    )
    out = subprocess.run(
        ["node", "-e", script], input=json.dumps(parts),
        capture_output=True, text=True, timeout=30,
    )
    if out.returncode != 0 or not out.stdout:
        sys.exit(f"challenge evaluation failed (is node installed?): {out.stderr.strip()[:200]}")
    return out.stdout


def login(force=False, password=None):
    """Panel-style session; keeps the cookie jar + the 600 session file in sync."""
    if not force and config.SESSION_FILE.exists():
        saved = config.SESSION_FILE.read_text().strip()
        if saved and not http.cookie_header():
            for pair in saved.split("; "):
                name, _, value = pair.partition("=")
                http._cj.set_cookie(_mkcookie(name, value))
        if http.cookie_header():
            return http.cookie_header()
    if password is None:
        password = load_password()
    state = http.call("login/")
    if not state.get("success"):
        sys.exit(f"could not get login state: {state.get('msg') or state}")
    result = state.get("result", {})
    challenge = challenge_to_string(result.get("challenge", []))
    salt = result.get("password_salt", "")
    h_pass = hashlib.sha1((salt + password).encode()).hexdigest()
    pw_hash = hmac.new(h_pass.encode(), challenge.encode(), hashlib.sha1).hexdigest()
    resp = http.call("login/", data={"password": pw_hash}, form=True, method="POST")
    if not resp.get("success"):
        sys.exit(f"login failed: {resp.get('msg') or resp.get('error_code')}")
    cookie = http.cookie_header()
    if not cookie:
        sys.exit("login succeeded but no session cookie was set")
    config.CFG.mkdir(mode=0o700, parents=True, exist_ok=True)
    config.SESSION_FILE.write_text(cookie + "\n")
    config.SESSION_FILE.chmod(stat.S_IRUSR | stat.S_IWUSR)
    return cookie


def _mkcookie(name, value):
    import http.cookiejar as cj
    return cj.Cookie(0, name, value, None, False, config.BASE_HOST, False, False,
                     "/", False, True, False, None, False, None, None, {})


def authed(path, data=None, method=None, form=False):
    """Authed call with one auto re-login on an auth error (same rule as phase 1)."""
    cookie = login()
    resp = http.call(path, data, {"Cookie": cookie}, method, form)
    if not resp.get("success") and "auth" in str(resp.get("error_code", "")).lower():
        resp = http.call(path, data, {"Cookie": login(force=True)}, method, form)
    return resp


def prompt_password():
    return getpass.getpass("Freebox password: ")
