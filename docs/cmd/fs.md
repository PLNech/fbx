# `fbx fs`: command reference

15 records, 19 operations.

## `fbx fs ls`

list a directory (fs/ls/<escaped path>, tree proxy)

- docs/api: `fs/ls/{path}`

### `fbx fs ls <path>`

`GET fs/ls/{path}`

Response:

```json
{
  "result": {
    "entries": {
      "mimetype": "syn-mimetype",
      "modification": 1762500000,
      "name": "device-a",
      "size": 2000000000000,
      "type": "auto"
    }
  },
  "success": true
}
```

Terminal:

```text
  mimetype                   syn-mimetype
  modification               1762500000
  name                       device-a
  size                       2000000000000
  type                       auto
```

## `fbx fs cp`

copy files: cp dst=… mode=overwrite|both|recent files='[…]'

- docs/api: `fs/cp/`

### `fbx fs cp`

`POST fs/cp/`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## `fbx fs mv`

move files (same body as cp); needs --yes

- docs/api: `fs/mv/`

### `fbx fs mv --yes` *(gated: add `--yes`)*

`POST fs/mv/`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## `fbx fs rm`

delete files: rm files='[…]'; needs --yes

- docs/api: `fs/rm/`

### `fbx fs rm --yes` *(gated: add `--yes`)*

`POST fs/rm/`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## `fbx fs extract`

extract archive: extract src=… dst=… password=… delete_archive=false overwrite=false

- docs/api: `fs/extract/`

### `fbx fs extract`

`POST fs/extract/`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## `fbx fs archive`

create archive: archive dst=… files='[…]'

- docs/api: `fs/archive/`

### `fbx fs archive`

`POST fs/archive/`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## `fbx fs repair`

par2 repair: repair src=… delete_archive=false

- docs/api: `fs/repair/`

### `fbx fs repair`

`POST fs/repair/`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## `fbx fs mkdir`

mkdir parent=… dirname=…

- docs/api: `fs/mkdir/`

### `fbx fs mkdir`

`POST fs/mkdir/`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## `fbx fs mkpath`

create a full path: mkpath path=…

- docs/api: `fs/mkpath/`

### `fbx fs mkpath`

`POST fs/mkpath/`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## `fbx fs rename`

rename src=… dst=…; needs --yes

- docs/api: `fs/rename/`

### `fbx fs rename --yes` *(gated: add `--yes`)*

`POST fs/rename/`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## `fbx fs tasks`

background fs tasks (fields partial in docs/api/)

- docs/api: `fs/tasks/`

### `fbx fs tasks`

`GET fs/tasks/`

Response:

```json
{
  "result": [
    {
      "error": "syn-error",
      "id": 1,
      "progress": "syn-progress",
      "state": "up",
      "title": "device-a"
    },
    {
      "error": "syn-error",
      "id": 2,
      "progress": "syn-progress",
      "state": "up",
      "title": "device-b"
    }
  ],
  "success": true
}
```

Terminal:

```text
                   fs tasks                   
 id  state  error      progress      title    
 1   up     syn-error  syn-progress  device-a 
 2   up     syn-error  syn-progress  device-b 
-- 2 entries
```

## `fbx fs task`

one fs task; set state=paused|running pauses/resumes

- docs/api: `fs/tasks/{task_id}`

### `fbx fs task show <task_id>`

`GET fs/tasks/{task_id}`

Response:

```json
{
  "result": {
    "enabled": true,
    "state": "up"
  },
  "success": true
}
```

Terminal:

```text
  enabled                    True
  state                      up
```

### `fbx fs task set <task_id> [key=value …]`

`PUT fs/tasks/{task_id}`

Response:

```json
{
  "result": {
    "enabled": true,
    "state": "up"
  },
  "success": true
}
```

Terminal:

```text
  enabled                    True
  state                      up
```

## `fbx fs share-link`

file share links

- docs/api: `share_link/`

### `fbx fs share-link list`

`GET share_link/`

Response:

```json
{
  "result": [
    {
      "expire": 1762500000,
      "fullurl": "syn-fullurl",
      "path": "syn-path",
      "token": "syn-token"
    },
    {
      "expire": 1762500060,
      "fullurl": "syn-fullurl",
      "path": "syn-path",
      "token": "syn-token"
    }
  ],
  "success": true
}
```

Terminal:

```text
                   fs share-link                    
 token      path      expire            fullurl     
 syn-token  syn-path  2025-11-07 07:20  syn-fullurl 
 syn-token  syn-path  2025-11-07 07:21  syn-fullurl 
-- 2 entries
```

### `fbx fs share-link add [key=value …]`

`POST share_link/`

Response:

```json
{
  "result": {
    "expire": 1762500000,
    "fullurl": "syn-fullurl",
    "path": "syn-path",
    "token": "syn-token"
  },
  "success": true
}
```

Terminal:

```text
  expire                     1762500000
  fullurl                    syn-fullurl
  path                       syn-path
  token                      syn-token
```

### `fbx fs share-link set <id> [key=value …]`

`PUT share_link/`

Response:

```json
{
  "result": {
    "expire": 1762500000,
    "fullurl": "syn-fullurl",
    "path": "syn-path",
    "token": "syn-token"
  },
  "success": true
}
```

Terminal:

```text
  expire                     1762500000
  fullurl                    syn-fullurl
  path                       syn-path
  token                      syn-token
```

### `fbx fs share-link rm <id>`

`DELETE share_link/`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## `fbx fs backup-export`

download the box config backup (see also: fbx fs get)

- docs/api: `backup/config/export`

### `fbx fs backup-export`

`GET backup/config/export`

Response:

```json
{
  "result": {
    "enabled": true,
    "state": "up"
  },
  "success": true
}
```

Terminal:

```text
  enabled                    True
  state                      up
```

## `fbx fs backup-import`

import a config backup; needs --yes

- docs/api: `backup/config/import`

### `fbx fs backup-import --yes` *(gated: add `--yes`)*

`POST backup/config/import`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## When it fails

Examples on `fbx fs ls`; the error
envelope is exactly what the box answers; the CLI prints
`<domain> <record> <op> failed: <msg>` and exits non-zero.

**invalid session**

```text
fs ls show failed: Invalid session
```

The session cookie expired. `fbx` re-authenticates once automatically (fresh challenge + login) before surfacing this; if it persists, run `fbx login`.

**box unreachable**

```text
fs ls show failed: unreachable: [Errno 65] no route to host
```

The box did not answer. Check the address (`FREEBOX_HOST`, default `fd0f:ee:b0::1`) and that you are on the box's LAN.

**validation error**

```text
fs ls show failed: unknown or invalid field
```

A body field the box does not accept. Field names come straight from docs/api/; `fbx api` is the escape hatch for anything undocumented.

## Binary transfer

`fbx fs get <path> [-o out]` and `fbx fs put <file> [dirname]` move
file bytes, not JSON; no rendered example here. See `docs/api/06-fs.md`.

