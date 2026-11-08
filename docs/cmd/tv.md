# `fbx tv`: command reference

17 records, 23 operations.

## `fbx tv status`

TV enablement/status

- docs/api: `tv/status/`

### `fbx tv status`

`GET tv/status/`

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

## `fbx tv channels`

- docs/api: `tv/channels/`

### `fbx tv channels`

`GET tv/channels/`

Response:

```json
{
  "result": [
    {
      "available": "syn-available",
      "id": 1,
      "name": "device-a",
      "number": 1
    },
    {
      "available": "syn-available",
      "id": 2,
      "name": "device-b",
      "number": 2
    }
  ],
  "success": true
}
```

Terminal:

```text
             tv channels             
 number  name      id  available     
 1       device-a  1   syn-available 
 2       device-b  2   syn-available 
-- 2 entries
```

## `fbx tv bouquets`

- docs/api: `tv/bouquets/`

### `fbx tv bouquets`

`GET tv/bouquets/`

Response:

```json
{
  "result": [
    {
      "channel_count": "syn-channel-count",
      "id": 1,
      "name": "device-a",
      "state": "up"
    },
    {
      "channel_count": "syn-channel-count",
      "id": 2,
      "name": "device-b",
      "state": "up"
    }
  ],
  "success": true
}
```

Terminal:

```text
              tv bouquets               
 id  name      channel_count      state 
 1   device-a  syn-channel-count  up    
 2   device-b  syn-channel-count  up    
-- 2 entries
```

## `fbx tv bouquet-channels`

channels of one bouquet (default: freeboxtv)

- docs/api: `tv/bouquets/{bouquet_id}/channels/`

### `fbx tv bouquet-channels`

`GET tv/bouquets/{bouquet_id}/channels/`

Response:

```json
{
  "result": [
    {
      "available": "syn-available",
      "id": 1,
      "number": 1,
      "pub_service": "syn-pub-service"
    },
    {
      "available": "syn-available",
      "id": 2,
      "number": 2,
      "pub_service": "syn-pub-service"
    }
  ],
  "success": true
}
```

Terminal:

```text
            tv bouquet-channels             
 number  id  available      pub_service     
 1       1   syn-available  syn-pub-service 
 2       2   syn-available  syn-pub-service 
-- 2 entries
```

## `fbx tv epg-by-time`

programs by time bucket

- docs/api: `tv/epg/by_time/{time}/`

### `fbx tv epg-by-time <time>`

`GET tv/epg/by_time/{time}/`

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

## `fbx tv epg-by-channel`

programs for one channel at a timestamp

- docs/api: `tv/epg/by_channel/{channel}/{time}/`

### `fbx tv epg-by-channel <channel> <time>`

`GET tv/epg/by_channel/{channel}/{time}/`

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

## `fbx tv epg-program`

one program

- docs/api: `tv/epg/programs/{program_id}/`

### `fbx tv epg-program <program_id>`

`GET tv/epg/programs/{program_id}/`

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

## `fbx tv epg-highlights`

featured programs

- docs/api: `tv/epg/highlights/`

### `fbx tv epg-highlights`

`GET tv/epg/highlights/`

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

## `fbx tv pvr-config`

- docs/api: `pvr/config`

### `fbx tv pvr-config show`

`GET pvr/config`

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

### `fbx tv pvr-config set [key=value …]`

`PUT pvr/config`

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

## `fbx tv pvr-programmed`

scheduled recordings

- docs/api: `pvr/programmed/`

### `fbx tv pvr-programmed list`

`GET pvr/programmed/`

Response:

```json
{
  "result": [
    {
      "channel_uuid": "syn-channel-uuid",
      "conflict": "syn-conflict",
      "enabled": true,
      "end": 1762500000,
      "id": 1,
      "name": "device-a",
      "start": 1762500000,
      "state": "up"
    },
    {
      "channel_uuid": "syn-channel-uuid",
      "conflict": "syn-conflict",
      "enabled": true,
      "end": 1762500060,
      "id": 2,
      "name": "device-b",
      "start": 1762500060,
      "state": "up"
    }
  ],
  "success": true
}
```

Terminal:

```text
                                        tv pvr-programmed                                         
 id  name      state  start             end               channel_uuid      conflict      enabled 
 1   device-a  up     2025-11-07 07:20  2025-11-07 07:20  syn-channel-uuid  syn-conflict  yes     
 2   device-b  up     2025-11-07 07:21  2025-11-07 07:21  syn-channel-uuid  syn-conflict  yes     
-- 2 entries
```

### `fbx tv pvr-programmed add [key=value …]`

`POST pvr/programmed/`

Response:

```json
{
  "result": {
    "channel_uuid": "syn-channel-uuid",
    "conflict": "syn-conflict",
    "enabled": true,
    "end": 1762500000,
    "id": 1,
    "name": "device-a",
    "start": 1762500000,
    "state": "up"
  },
  "success": true
}
```

Terminal:

```text
  channel_uuid               syn-channel-uuid
  conflict                   syn-conflict
  enabled                    True
  end                        1762500000
  id                         1
  name                       device-a
  start                      1762500000
  state                      up
```

### `fbx tv pvr-programmed set <id> [key=value …]`

`PUT pvr/programmed/`

Response:

```json
{
  "result": {
    "channel_uuid": "syn-channel-uuid",
    "conflict": "syn-conflict",
    "enabled": true,
    "end": 1762500000,
    "id": 1,
    "name": "device-a",
    "start": 1762500000,
    "state": "up"
  },
  "success": true
}
```

Terminal:

```text
  channel_uuid               syn-channel-uuid
  conflict                   syn-conflict
  enabled                    True
  end                        1762500000
  id                         1
  name                       device-a
  start                      1762500000
  state                      up
```

### `fbx tv pvr-programmed rm <id>`

`DELETE pvr/programmed/`

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

## `fbx tv pvr-finished`

finished recordings

- docs/api: `pvr/finished/`

### `fbx tv pvr-finished`

`GET pvr/finished/`

Response:

```json
{
  "result": [
    {
      "byte_size": 2000000000000,
      "channel_name": "syn-channel-name",
      "end": 1762500000,
      "id": 1,
      "name": "device-a",
      "start": 1762500000,
      "state": "up"
    },
    {
      "byte_size": 1999999999999,
      "channel_name": "syn-channel-name",
      "end": 1762500060,
      "id": 2,
      "name": "device-b",
      "start": 1762500060,
      "state": "up"
    }
  ],
  "success": true
}
```

Terminal:

```text
                                   tv pvr-finished                                    
 id  name      state  channel_name      start             end               byte_size 
 1   device-a  up     syn-channel-name  2025-11-07 07:20  2025-11-07 07:20  1.8 TiB   
 2   device-b  up     syn-channel-name  2025-11-07 07:21  2025-11-07 07:21  1.8 TiB   
-- 2 entries
```

## `fbx tv pvr-generator`

recurring recording rules

- docs/api: `pvr/generator/`

### `fbx tv pvr-generator`

`GET pvr/generator/`

Response:

```json
{
  "result": [
    {
      "id": 1,
      "media": "auto",
      "name": "device-a",
      "path": "syn-path",
      "type": "auto"
    },
    {
      "id": 2,
      "media": "auto",
      "name": "device-b",
      "path": "syn-path",
      "type": "auto"
    }
  ],
  "success": true
}
```

Terminal:

```text
          tv pvr-generator           
 id  type  name      media  path     
 1   auto  device-a  auto   syn-path 
 2   auto  device-b  auto   syn-path 
-- 2 entries
```

## `fbx tv pvr-media`

recording storage space

- docs/api: `pvr/media/`

### `fbx tv pvr-media`

`GET pvr/media/`

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

## `fbx tv dvb`

TNT/DVB frontends

- docs/api: `dvb/`

### `fbx tv dvb list`

`GET dvb/`

Response:

```json
{
  "result": [
    {
      "id": 1,
      "last_successful_scan": 1762500000,
      "name": "device-a",
      "type": "auto"
    },
    {
      "id": 2,
      "last_successful_scan": 1762500060,
      "name": "device-b",
      "type": "auto"
    }
  ],
  "success": true
}
```

Terminal:

```text
                  tv dvb                  
 id  type  name      last_successful_scan 
 1   auto  device-a  2025-11-07 07:20     
 2   auto  device-b  2025-11-07 07:21     
-- 2 entries
```

### `fbx tv dvb add [key=value …]`

`POST dvb/`

Response:

```json
{
  "result": {
    "id": 1,
    "last_successful_scan": 1762500000,
    "name": "device-a",
    "type": "auto"
  },
  "success": true
}
```

Terminal:

```text
  id                         1
  last_successful_scan       1762500000
  name                       device-a
  type                       auto
```

## `fbx tv dvb-frontend`

- docs/api: `dvb/{frontend_id}/`

### `fbx tv dvb-frontend show <frontend_id>`

`GET dvb/{frontend_id}/`

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

### `fbx tv dvb-frontend set <frontend_id> [key=value …]`

`PUT dvb/{frontend_id}/`

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

## `fbx tv dvb-scan`

launch a channel scan on one frontend

- docs/api: `dvb/{frontend_id}/scan_start`

### `fbx tv dvb-scan <frontend_id>`

`POST dvb/{frontend_id}/scan_start`

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

## `fbx tv dvb-services`

- docs/api: `dvb/{frontend_id}/services/`

### `fbx tv dvb-services <frontend_id>`

`GET dvb/{frontend_id}/services/`

Response:

```json
{
  "result": [
    {
      "lcn": "syn-lcn",
      "name": "device-a",
      "scrambled": "syn-scrambled"
    },
    {
      "lcn": "syn-lcn",
      "name": "device-b",
      "scrambled": "syn-scrambled"
    }
  ],
  "success": true
}
```

Terminal:

```text
         tv dvb-services          
 lcn      name      scrambled     
 syn-lcn  device-a  syn-scrambled 
 syn-lcn  device-b  syn-scrambled 
-- 2 entries
```

## When it fails

Examples on `fbx tv status`; the error
envelope is exactly what the box answers; the CLI prints
`<domain> <record> <op> failed: <msg>` and exits non-zero.

**invalid session**

```text
tv status show failed: Invalid session
```

The session cookie expired. `fbx` re-authenticates once automatically (fresh challenge + login) before surfacing this; if it persists, run `fbx login`.

**box unreachable**

```text
tv status show failed: unreachable: [Errno 65] no route to host
```

The box did not answer. Check the address (`FREEBOX_HOST`, default `fd0f:ee:b0::1`) and that you are on the box's LAN.

**validation error**

```text
tv status show failed: unknown or invalid field
```

A body field the box does not accept. Field names come straight from docs/api/; `fbx api` is the escape hatch for anything undocumented.

