"""Where things live: the box address, the session cookie, the 1Password ref."""
import os
from pathlib import Path

# The Freebox answers on its ULA (fd0f:ee:b0::/48 is the stock Freebox prefix);
# mafreebox.freebox.fr also resolves on the LAN. Override with FREEBOX_HOST.
BASE_HOST = os.environ.get("FREEBOX_HOST", "fd0f:ee:b0::1")
BASE = f"http://[{BASE_HOST}]/api/latest"

CFG = Path(os.environ.get("FREEBOX_CONFIG_DIR", str(Path.home() / ".config" / "freebox")))
SESSION_FILE = CFG / "session"

# The password lives in 1Password and is read at runtime into memory only.
# Point FREEBOX_OP_REF at your own item if it lives elsewhere.
OP_REF = os.environ.get("FREEBOX_OP_REF", "op://Personal/Freebox/credential")


def op_item():
    """(item name, vault or None) parsed out of the op:// reference."""
    parts = OP_REF.split("/")
    vault = parts[2] if len(parts) > 4 and parts[2] not in ("v", "i", "o") else None
    return parts[3], vault

PANEL_HEADER = {"X-FBX-FREEBOX0S": "1"}
