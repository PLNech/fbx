#!/usr/bin/env python3
"""Prepare and commit the GitHub wiki from docs/cmd/ (the command wiki).

Single source of truth: docs/cmd/ (generated from the endpoint records).
This script syncs a checkout of the PLNech/fbx.wiki repo:

  - copies each docs/cmd/X.md as X.md (pages are self-contained),
  - builds Home.md (tagline, pitch, quickstart, page index) and _Sidebar.md,
  - commits as "wiki: sync from <main-repo short sha>" ONLY when something
    actually changed (second run = no commit),
  - does NOT push: the caller pushes (dev: `git -C <checkout> push`;
    CI: enable the push line in the wiki-sync job, see CONTRIBUTING).

Safety rules:
  - Home.md is overwritten ONLY when it is missing or still holds GitHub's
    default empty stub; human-written wiki content is never clobbered.
  - WIKI_TOKEN is never printed and never lands in any file.

Usage (CI):   WIKI_TOKEN=... python tools/sync_gh_wiki.py
Usage (dev):  python tools/sync_gh_wiki.py --wiki-dir /path/to/fbx.wiki
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "cmd"
WIKI_URL = "https://github.com/PLNech/fbx.wiki.git"

TAGLINE = "fbx, une CLI pour ta Freebox"
PITCH = ("An unofficial, full-coverage command line into a Freebox OS router's "
         "panel API. The web panel is just a JavaScript client over a REST API, "
         "and `fbx` is the missing terminal client for that dialect.")

PAGE_BLURB = {
    "core": "version, login, logout, the `fbx api` escape hatch",
    "accounts": "profiles, groups, notification targets",
    "airmedia": "config, receivers, cast",
    "auth": "sessions, permissions, app tokens",
    "connection": "WAN state, xdsl/lte, ipv6, ddns, logs, rrd graphs",
    "contacts": "entries, numbers/emails/addresses, groups, vCard",
    "downloads": "task queue, trackers, peers, files, blacklist, rss",
    "fs": "ls, cp/mv/rm, extract/archive, share links, binary get/put",
    "fw": "incoming, port redir, dmz, upnp, netshare, ftp, tftp, parental",
    "lan": "config, devices, hosts, wol, routes, dhcp, switch, freeplug",
    "phone": "hardware, sip, dect, paging, call log",
    "storage": "disks, partitions, raid, fsck, internal storage",
    "system": "health, reboot/shutdown, standby, lcd, ledstrip, sfp",
    "tv": "channels, bouquets, epg, pvr, dvb",
    "vpn": "servers, ip pool, users, live connections, vpn client",
    "wifi": "state/config, ap, bss, stations, mlo, mac-filter, wps",
}


def pages():
    return sorted(p.stem for p in SRC.glob("*.md"))


def build_home():
    lines = [f"# {TAGLINE}", "", PITCH, "", "## Quickstart", "",
             "```sh",
             "fbx version        # reachability check, no login needed",
             "fbx login          # panel-dialect auth (1Password or --stdin)",
             "fbx wan            # live WAN state and rates",
             "fbx tldr           # ten more copy-pasteable examples",
             "```", "", "## Command pages", ""]
    for name in pages():
        blurb = PAGE_BLURB.get(name, "")
        lines.append(f"- [[{name}]]" + (f": {blurb}" if blurb else ""))
    lines += ["", "Synthetic examples only: every page is generated from the "
              "endpoint records and the response models in docs/api/, never "
              "from a live box."]
    return "\n".join(lines) + "\n"


def build_sidebar():
    lines = [f"**{TAGLINE}**", "", "- [[Home]]", ""]
    for name in pages():
        lines.append(f"- [[{name}]]")
    return "\n".join(lines) + "\n"


def is_stub(text):
    """GitHub's default empty Home page (or an empty file). Human content is
    never a stub, by construction."""
    t = text.strip().lower()
    if not t:
        return True
    return "welcome to the" in t[:200] and "wiki" in t[:200]


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} failed:\n{r.stdout}\n{r.stderr}")
    return r.stdout.strip()


def sync(wiki_dir):
    """Sync one wiki checkout. Returns True when a commit was made."""
    changed = []
    for name in pages():
        dst = Path(wiki_dir) / f"{name}.md"
        new = (SRC / f"{name}.md").read_text()
        if not dst.exists() or dst.read_text() != new:
            dst.write_text(new)
            changed.append(f"{name}.md")
    home = Path(wiki_dir) / "Home.md"
    if not home.exists() or is_stub(home.read_text()):
        new = build_home()
        if not home.exists() or home.read_text() != new:
            home.write_text(new)
            changed.append("Home.md")
    sidebar = Path(wiki_dir) / "_Sidebar.md"
    new = build_sidebar()
    if not sidebar.exists() or sidebar.read_text() != new:
        sidebar.write_text(new)
        changed.append("_Sidebar.md")
    if not changed:
        print("wiki-sync: wiki already up to date, nothing to commit")
        return False
    sha = run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT)
    run(["git", "add", "-A"], cwd=wiki_dir)
    run(["git", "commit", "-m", f"wiki: sync from {sha}"], cwd=wiki_dir)
    print(f"wiki-sync: committed {', '.join(sorted(changed))} "
          f"(wiki: sync from {sha}); push it from {wiki_dir}")
    return True


def main():
    wiki_dir = None
    for i, a in enumerate(sys.argv):
        if a == "--wiki-dir":
            wiki_dir = sys.argv[i + 1]
    if wiki_dir:
        sync(wiki_dir)
        return
    token = os.environ.get("WIKI_TOKEN", "")
    if not token:
        print("wiki-sync: WIKI_TOKEN is not set; skipping the GitHub wiki sync "
              "(add the Actions secret to enable it)")
        return
    url = f"https://x-access-token:{token}@github.com/PLNech/fbx.wiki.git"
    tmp = tempfile.mkdtemp(prefix="fbx-wiki-")
    try:
        run(["git", "clone", "--depth", "1", url, tmp])
        sync(tmp)
    finally:
        # the token can leak into the checkout's remote URL config: remove it
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
