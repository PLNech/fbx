"""Where things live: the box address, the session cookie, the 1Password ref."""
import os
import stat
import sys
from pathlib import Path

# The Freebox answers on its ULA (fd0f:ee:b0::/48 is the stock Freebox prefix);
# mafreebox.freebox.fr also resolves on the LAN. Override with FREEBOX_HOST.
BASE_HOST = os.environ.get("FREEBOX_HOST", "fd0f:ee:b0::1")
BASE = f"http://[{BASE_HOST}]/api/latest"

CFG = Path(os.environ.get("FREEBOX_CONFIG_DIR", str(Path.home() / ".config" / "freebox")))
SESSION_FILE = CFG / "session"

# The password lives in 1Password and is read at runtime into memory only.
# The op:// reference resolves by ladder:
#   1. FREEBOX_OP_REF env (shell-level override)
#   2. a one-line file at <CFG>/opref (machine-level, shell-independent; the
#      whole line is the op:// reference; keep it chmod 600)
#   3. this generic default
DEFAULT_OP_REF = "op://Personal/Freebox/credential"


def _warn(msg):
    print(f"fbx: {msg}", file=sys.stderr)


def load_op_ref():
    ref = os.environ.get("FREEBOX_OP_REF")
    if ref:
        return ref
    f = CFG / "opref"
    try:
        if f.is_file():
            mode = f.stat().st_mode & 0o777
            if mode & 0o077:
                _warn(f"{f} is readable by group/others ({stat.filemode(mode)}); "
                      f"tighten it to 600")
            text = f.read_text().strip()
            line = text.splitlines()[0] if text else ""
            if line:
                return line
            _warn(f"{f} is empty; using the default 1Password item")
    except OSError:
        pass
    return DEFAULT_OP_REF


# Snapshot at import (compat); auth reads the ladder fresh via load_op_ref().
OP_REF = load_op_ref()


def op_item():
    """(item name, vault or None) parsed out of the op:// reference."""
    parts = OP_REF.split("/")
    vault = parts[2] if len(parts) > 4 and parts[2] not in ("v", "i", "o") else None
    return parts[3], vault

PANEL_HEADER = {"X-FBX-FREEBOX0S": "1"}
