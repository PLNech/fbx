# `fbx auth`: command reference

3 records, 6 operations.

## `fbx auth sessions`

- docs/api: `sessions/`

### `fbx auth sessions`

`GET sessions/`

Response:

```json
{
  "result": [
    {
      "app_name": "syn-app-name",
      "client_ip": "192.168.1.50",
      "device_name": "syn-device-name",
      "id": 1,
      "is_web_app": "syn-is-web-app",
      "start_time": 1762500000
    },
    {
      "app_name": "syn-app-name",
      "client_ip": "192.168.1.51",
      "device_name": "syn-device-name",
      "id": 2,
      "is_web_app": "syn-is-web-app",
      "start_time": 1762500060
    }
  ],
  "success": true
}
```

Terminal:

```text
                                   auth sessions                                   
 id  app_name      device_name      client_ip     is_web_app      start_time       
 1   syn-app-name  syn-device-name  192.168.1.50  syn-is-web-app  2025-11-07 07:20 
 2   syn-app-name  syn-device-name  192.168.1.51  syn-is-web-app  2025-11-07 07:21 
-- 2 entries
```

## `fbx auth perms`

permission names of the logged-in app (login/perms/)

- docs/api: `login/perms/`

### `fbx auth perms`

`GET login/perms/`

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

## `fbx auth tokens`

app pairings/tokens (authorization/): rm = revoke a pairing

- docs/api: `authorization/`

### `fbx auth tokens list`

`GET authorization/`

Response:

```json
{
  "result": [
    {
      "app_id": "syn-app-id",
      "app_name": "syn-app-name",
      "app_version": "syn-app-version",
      "device_name": "syn-device-name",
      "id": 1,
      "token_validity": "syn-token-validity"
    },
    {
      "app_id": "syn-app-id",
      "app_name": "syn-app-name",
      "app_version": "syn-app-version",
      "device_name": "syn-device-name",
      "id": 2,
      "token_validity": "syn-token-validity"
    }
  ],
  "success": true
}
```

Terminal:

```text
                                    auth tokens                                     
 id  app_name      app_version      app_id      device_name      token_validity     
 1   syn-app-name  syn-app-version  syn-app-id  syn-device-name  syn-token-validity 
 2   syn-app-name  syn-app-version  syn-app-id  syn-device-name  syn-token-validity 
-- 2 entries
```

### `fbx auth tokens add [key=value …]`

`POST authorization/`

Response:

```json
{
  "result": {
    "app_id": "syn-app-id",
    "app_name": "syn-app-name",
    "app_version": "syn-app-version",
    "device_name": "syn-device-name",
    "id": 1,
    "token_validity": "syn-token-validity"
  },
  "success": true
}
```

Terminal:

```text
  app_id                     syn-app-id
  app_name                   syn-app-name
  app_version                syn-app-version
  device_name                syn-device-name
  id                         1
  token_validity             syn-token-validity
```

### `fbx auth tokens set <id> [key=value …]`

`PUT authorization/`

Response:

```json
{
  "result": {
    "app_id": "syn-app-id",
    "app_name": "syn-app-name",
    "app_version": "syn-app-version",
    "device_name": "syn-device-name",
    "id": 1,
    "token_validity": "syn-token-validity"
  },
  "success": true
}
```

Terminal:

```text
  app_id                     syn-app-id
  app_name                   syn-app-name
  app_version                syn-app-version
  device_name                syn-device-name
  id                         1
  token_validity             syn-token-validity
```

### `fbx auth tokens rm <id> --yes` *(gated: add `--yes`)*

`DELETE authorization/`

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

Examples on `fbx auth sessions`; the error
envelope is exactly what the box answers; the CLI prints
`<domain> <record> <op> failed: <msg>` and exits non-zero.

**invalid session**

```text
auth sessions list failed: Invalid session
```

The session cookie expired. `fbx` re-authenticates once automatically (fresh challenge + login) before surfacing this; if it persists, run `fbx login`.

**box unreachable**

```text
auth sessions list failed: unreachable: [Errno 65] no route to host
```

The box did not answer. Check the address (`FREEBOX_HOST`, default `fd0f:ee:b0::1`) and that you are on the box's LAN.

**validation error**

```text
auth sessions list failed: unknown or invalid field
```

A body field the box does not accept. Field names come straight from docs/api/; `fbx api` is the escape hatch for anything undocumented.

