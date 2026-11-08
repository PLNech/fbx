# `fbx airmedia`: command reference

3 records, 4 operations.

## `fbx airmedia config`

airmedia: enabled=true|false password=…

- docs/api: `airmedia/config/`

### `fbx airmedia config show`

`GET airmedia/config/`

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

### `fbx airmedia config set [key=value …]`

`PUT airmedia/config/`

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

## `fbx airmedia receivers`

- docs/api: `airmedia/receivers/`

### `fbx airmedia receivers`

`GET airmedia/receivers/`

Response:

```json
{
  "result": [
    {
      "name": "device-a",
      "password_protected": "syn-password-protected"
    },
    {
      "name": "device-b",
      "password_protected": "syn-password-protected"
    }
  ],
  "success": true
}
```

Terminal:

```text
        airmedia receivers        
 name      password_protected     
 device-a  syn-password-protected 
 device-b  syn-password-protected 
-- 2 entries
```

## `fbx airmedia cast`

cast/stop on one receiver: cast action=start media_type=video media=… [password=…]

- docs/api: `airmedia/receivers/{receiver_name}/`

### `fbx airmedia cast <receiver_name>`

`POST airmedia/receivers/{receiver_name}/`

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

Examples on `fbx airmedia config` show; the error
envelope is exactly what the box answers; the CLI prints
`<domain> <record> <op> failed: <msg>` and exits non-zero.

**invalid session**

```text
airmedia config show failed: Invalid session
```

The session cookie expired. `fbx` re-authenticates once automatically (fresh challenge + login) before surfacing this; if it persists, run `fbx login`.

**box unreachable**

```text
airmedia config show failed: unreachable: [Errno 65] no route to host
```

The box did not answer. Check the address (`FREEBOX_HOST`, default `fd0f:ee:b0::1`) and that you are on the box's LAN.

**validation error**

```text
airmedia config show failed: unknown or invalid field
```

A body field the box does not accept. Field names come straight from docs/api/; `fbx api` is the escape hatch for anything undocumented.

