# fbx — Le CLI freebox

[![CI (GitLab)](https://git.nech.pl/pln/fbx/badges/master/pipeline.svg)](https://git.nech.pl/pln/fbx/-/commits/master)
[![CI (GitHub)](https://github.com/plnech/fbx/actions/workflows/ci.yml/badge.svg)](https://github.com/plnech/fbx/actions/workflows/ci.yml)

An unofficial, full-coverage command line into a Freebox OS router's panel API.

The Freebox web panel is just a JavaScript client over a REST API. That API is
neither the well-known developer API nor documented anywhere official — the
panel speaks its own dialect (different paths, form posts, a challenge-based
login). `fbx` is the missing terminal client for that dialect: everything the
panel can see, so does your shell — **15 domains, 183 endpoint records, 292
operations**, driven by one generic engine.

## Install

With [poetry](https://python-poetry.org) (recommended):

```sh
git clone https://git.nech.pl/pln/fbx
cd fbx
poetry install        # installs into .venv, exposes the `fbx` entry point
```

Or [pipx](https://pipx.pypa.io):

```sh
pipx install fbx-cli          # from a future PyPI release
pipx install git+https://git.nech.pl/pln/fbx   # straight from the clone
```

No clone, no install? From the repo root both spellings work:

```sh
python -m fbx_cli.cli version          # module form
poetry run fbx version                 # console script (after poetry install)
```

## Quickstart

```sh
fbx version        # unauthenticated GET /api_version — the reachability check
fbx login          # panel-dialect auth (see below)
fbx wan            # WAN state, IPs, rates
fbx wifi status    # global wifi state
fbx fw samba       # Samba/netshare config
```

## Auth, in one paragraph

The panel's login is not the developer API's app-token dance. `fbx` mirrors the
panel exactly: `GET /api/latest/login/` returns a password salt and a *challenge*
— a table of ~32 obfuscated JavaScript snippets the panel `eval()`s one per
character and concatenates. `fbx` runs the same snippets through a one-shot
`node` subprocess (the only snippet that is ever evaluated is the box's own
challenge data), computes `HMAC-SHA1(key=SHA1(salt+password), msg=challenge)`,
and posts it form-encoded to `login/`. The session cookie is stored `chmod 600`
under `~/.config/freebox/session/`, never printed, and `fbx` re-authenticates
automatically once when the box reports an auth error. The password is read at
runtime from 1Password (`op read` of the item named by `FREEBOX_OP_REF`, by
default `op://Personal/Freebox/credential` — point it at your own item) or via
`fbx login --stdin`. It never touches argv, stdout, or disk. You need `node`
installed for the challenge evaluation.

The box address defaults to the stock Freebox ULA `fd0f:ee:b0::1`; override with
`FREEBOX_HOST` (or use `mafreebox.freebox.fr`).

## Domains

| Domain | Records | What's inside |
|---|---:|---|
| `wifi` | 20 | state/config, ap, bss, stations, mlo, mac-filter, guest keys, wps, steering |
| `downloads` | 18 | task queue, add, trackers, peers, files, blacklist, throttling, rss |
| `tv` | 17 | channels, bouquets, epg, pvr, dvb |
| `connection` | 16 | WAN state, xdsl/lte, ipv6, ddns, logs, rrd graphs |
| `storage` | 16 | disks, partitions, raid, fsck, internal storage |
| `fs` | 15 | ls, cp/mv/rm, extract/archive, tasks, share links, binary get/put |
| `fw` | 15 | incoming, port redir, dmz, upnp, netshare (samba/afp), ftp, tftp, parental |
| `lan` | 14 | config, devices, hosts, wol, routes, dhcp, dhcpv6, switch, freeplug |
| `contacts` | 13 | entries, numbers/emails/addresses, groups, vCard import/export |
| `system` | 10 | health, reboot/shutdown, standby, lcd, ledstrip, sfp, licenses |
| `vpn` | 10 | servers, ip pool, users, live connections, vpn client |
| `phone` | 9 | hardware, sip, dect, paging, call log |
| `accounts` | 4 | profiles, groups, notification targets |
| `auth` | 3 | sessions, permissions, app tokens |
| `airmedia` | 3 | config, receivers, cast |

## The grammar

- **Read everywhere**: `fbx <domain> <thing>` (or `… list` for collections).
- **CRUD** where documented: `add` (POST), `set` (PUT), `rm` (DELETE), plus
  `get` on composed resources.
- **Body fields** ride as `key=value` pairs, auto-typed
  (`enabled=true`, `progress=42`, `files='["a.iso"]'`).
- **Path slots** are positional: `fbx wifi stations <bssid>`.
- **Destructive ops** (storage format/fsck, raid member ops, fs rm/mv, system
  reboot/shutdown, token revocation, …) refuse to run without `--yes`.
- **Escape hatch**: `fbx api GET|POST <path> [JSON-or-form]` reaches anything
  the generated commands miss.

Global flags work anywhere on the line: `--json` (raw response envelope,
untouched), `--debug` (method + path + status of each call — never bodies),
`--yes` (confirm a destructive op).

## Scope & security notes

- `fbx` is meant to talk to **your own box**, over your own LAN. It ships no
  defaults that reach beyond that, and you are responsible for what you do to
  your network.
- Unofficial project — not affiliated with, nor endorsed by, Free SAS or
  Freebox. "Freebox" is a trademark of Free SAS; this project only
  interoperates with the product.
- Provided under GPL-3.0, **without any warranty** (see LICENSE).

## API notes

The endpoint surface is transcribed, clean-room style, from the panel's
publicly-served JavaScript into the markdown documents under
[`docs/api/`](docs/api/) — 16 files, one per panel area, no secrets, no
personal data. They are the single source of truth: each endpoint record in
`fbx_cli/domains/` cites them, and the fixture-based test suite is generated
from their response models.

## License

GPL-3.0 — see [LICENSE](LICENSE). Copyright (C) 2026 Paul-Louis NECH.
