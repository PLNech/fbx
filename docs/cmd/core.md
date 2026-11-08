# Core commands

## `fbx version`

Unauthenticated `GET /api_version`: the reachability check, no login.

```text
  api_version        12.0
  device_name        Freebox Server
  box_model          fbxgw8-r1
  firmware_version   4.8.6
  api_base_url       /api/
```

## `fbx login`

Reads the password from 1Password (`op read`, item from `FREEBOX_OP_REF`) or
`--stdin`, evaluates the box's challenge via a one-shot `node` subprocess and
stores the session cookie `chmod 600` under `~/.config/freebox/session/`.
Nothing is printed but a confirmation; the password never touches argv or disk.

```text
$ fbx login
session stored (chmod 600, cookie never displayed)
```

## `fbx logout`

Ends the panel session (`POST login/logout`) and drops the local cookie file.

## `fbx api METHOD PATH [JSON-or-form]`

Generic authenticated escape hatch: anything the generated commands miss.

```sh
fbx api GET connection/xdsl/
fbx api POST system/reboot/          # gated surfaces still need --yes
```
