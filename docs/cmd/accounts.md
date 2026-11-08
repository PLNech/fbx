# `fbx accounts`: command reference

4 records, 10 operations.

## `fbx accounts profiles`

profiles (family): rm needs --yes

- docs/api: `profile/`

### `fbx accounts profiles list`

`GET profile/`

Response:

```json
{
  "result": [
    {
      "icon": "syn-icon",
      "id": 1,
      "name": "device-a"
    },
    {
      "icon": "syn-icon",
      "id": 2,
      "name": "device-b"
    }
  ],
  "success": true
}
```

Terminal:

```text
   accounts profiles    
 id  name      icon     
 1   device-a  syn-icon 
 2   device-b  syn-icon 
-- 2 entries
```

### `fbx accounts profiles add [key=value …]`

`POST profile/`

Response:

```json
{
  "result": {
    "icon": "syn-icon",
    "id": 1,
    "name": "device-a"
  },
  "success": true
}
```

Terminal:

```text
  icon                       syn-icon
  id                         1
  name                       device-a
```

### `fbx accounts profiles set <id> [key=value …]`

`PUT profile/`

Response:

```json
{
  "result": {
    "icon": "syn-icon",
    "id": 1,
    "name": "device-a"
  },
  "success": true
}
```

Terminal:

```text
  icon                       syn-icon
  id                         1
  name                       device-a
```

### `fbx accounts profiles rm <id> --yes` *(gated: add `--yes`)*

`DELETE profile/`

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

## `fbx accounts groups`

permission groups [thin in docs]

- docs/api: `group/`

### `fbx accounts groups`

`GET group/`

Response:

```json
{
  "result": [
    {
      "enabled": true,
      "state": "up"
    },
    {
      "enabled": true,
      "state": "up"
    }
  ],
  "success": true
}
```

Terminal:

```text
accounts groups 
 enabled  state 
 yes      up    
 yes      up    
-- 2 entries
```

## `fbx accounts notif-targets`

notification webhook targets

- docs/api: `notif/targets/`

### `fbx accounts notif-targets list`

`GET notif/targets/`

Response:

```json
{
  "result": [
    {
      "api_url": "syn-api-url",
      "id": 1,
      "last_use": 1762500000,
      "message_type": "syn-message-type",
      "name": "device-a",
      "type": "auto"
    },
    {
      "api_url": "syn-api-url",
      "id": 2,
      "last_use": 1762500060,
      "message_type": "syn-message-type",
      "name": "device-b",
      "type": "auto"
    }
  ],
  "success": true
}
```

Terminal:

```text
                       accounts notif-targets                        
 id  name      type  api_url      message_type      last_use         
 1   device-a  auto  syn-api-url  syn-message-type  2025-11-07 07:20 
 2   device-b  auto  syn-api-url  syn-message-type  2025-11-07 07:21 
-- 2 entries
```

### `fbx accounts notif-targets add [key=value …]`

`POST notif/targets/`

Response:

```json
{
  "result": {
    "api_url": "syn-api-url",
    "id": 1,
    "last_use": 1762500000,
    "message_type": "syn-message-type",
    "name": "device-a",
    "type": "auto"
  },
  "success": true
}
```

Terminal:

```text
  api_url                    syn-api-url
  id                         1
  last_use                   1762500000
  message_type               syn-message-type
  name                       device-a
  type                       auto
```

### `fbx accounts notif-targets set <id> [key=value …]`

`PUT notif/targets/`

Response:

```json
{
  "result": {
    "api_url": "syn-api-url",
    "id": 1,
    "last_use": 1762500000,
    "message_type": "syn-message-type",
    "name": "device-a",
    "type": "auto"
  },
  "success": true
}
```

Terminal:

```text
  api_url                    syn-api-url
  id                         1
  last_use                   1762500000
  message_type               syn-message-type
  name                       device-a
  type                       auto
```

### `fbx accounts notif-targets rm <id>`

`DELETE notif/targets/`

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

## `fbx accounts taskcount`

background task counts per name

- docs/api: `taskcount/`

### `fbx accounts taskcount`

`GET taskcount/`

Response:

```json
{
  "result": [
    {
      "name": "device-a"
    },
    {
      "name": "device-b"
    }
  ],
  "success": true
}
```

Terminal:

```text
 accounts 
taskcount 
 name     
 device-a 
 device-b 
-- 2 entries
```

## When it fails

Examples on `fbx accounts profiles` list; the error
envelope is exactly what the box answers; the CLI prints
`<domain> <record> <op> failed: <msg>` and exits non-zero.

**invalid session**

```text
accounts profiles list failed: Invalid session
```

The session cookie expired. `fbx` re-authenticates once automatically (fresh challenge + login) before surfacing this; if it persists, run `fbx login`.

**box unreachable**

```text
accounts profiles list failed: unreachable: [Errno 65] no route to host
```

The box did not answer. Check the address (`FREEBOX_HOST`, default `fd0f:ee:b0::1`) and that you are on the box's LAN.

**validation error**

```text
accounts profiles list failed: unknown or invalid field
```

A body field the box does not accept. Field names come straight from docs/api/; `fbx api` is the escape hatch for anything undocumented.

