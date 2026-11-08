# `fbx system`: command reference

10 records, 14 operations.

## `fbx system health`

firmware, uptime, temps, fan (system/), the box's health grid

- docs/api: `system/`

### `fbx system health`

`GET system/`

Response:

```json
{
  "result": {
    "disk_status": "ok",
    "fans": [
      {
        "id": 0,
        "name": "fan0",
        "value": 1800
      }
    ],
    "firmware_version": "4.8.6",
    "mac": "aa:bb:cc:00:00:01",
    "model_info": {
      "has_dsl": false,
      "name": "fbxgw8-r1",
      "pretty_name": "Freebox Server"
    },
    "sensors": [
      {
        "id": 0,
        "name": "temp_sw",
        "value": 52
      },
      {
        "id": 1,
        "name": "temp_cpuc",
        "value": 61
      },
      {
        "id": 2,
        "name": "temp_ntc1",
        "value": 44
      }
    ],
    "serial": "FREEBOX-0000",
    "uptime_val": 90061
  },
  "success": true
}
```

Terminal:

```text
Freebox Server / 4.8.6
  uptime             1d 1h 1m
  mac                aa:bb:cc:00:00:01
  serial             FREEBOX-0000
  disk_status        ok
  fans:  fan0=1800rpm
  sensors: temp_cpuc=61  temp_ntc1=44  temp_sw=52
```

## `fbx system reboot`

reboot the box (system/reboot/): DESTRUCTIVE, needs --yes

- docs/api: `system/reboot/`

### `fbx system reboot --yes` *(gated: add `--yes`)*

`POST system/reboot/`

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

## `fbx system shutdown`

shut the box down (system/shutdown): DESTRUCTIVE, needs --yes

- docs/api: `system/shutdown`

### `fbx system shutdown --yes` *(gated: add `--yes`)*

`POST system/shutdown`

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

## `fbx system standby`

standby planning (mode: suspend | wifi_off)

- docs/api: `standby/config/`

### `fbx system standby show`

`GET standby/config/`

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

### `fbx system standby set [key=value …]`

`PUT standby/config/`

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

## `fbx system lcd`

front LCD: brightness, orientation, forced

- docs/api: `lcd/config/`

### `fbx system lcd show`

`GET lcd/config/`

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

### `fbx system lcd set [key=value …]`

`PUT lcd/config/`

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

## `fbx system ledstrip`

LED strip brightness/animation + planning

- docs/api: `ledstrip/planning/`

### `fbx system ledstrip show`

`GET ledstrip/planning/`

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

### `fbx system ledstrip set [key=value …]`

`PUT ledstrip/planning/`

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

## `fbx system sfp-status`

SFP module status (sfp/status)

- docs/api: `sfp/status`

### `fbx system sfp-status`

`GET sfp/status`

Response:

```json
{
  "result": {
    "link": "syn-link",
    "part_number": "syn-part-number",
    "power_good": "syn-power-good",
    "present": true,
    "serial_number": "syn-serial-number",
    "type": "auto",
    "used_type": "syn-used-type",
    "vendor_name": "syn-vendor-name"
  },
  "success": true
}
```

Terminal:

```text
  link                       syn-link
  part_number                syn-part-number
  power_good                 syn-power-good
  present                    True
  serial_number              syn-serial-number
  type                       auto
  used_type                  syn-used-type
  vendor_name                syn-vendor-name
```

## `fbx system sfp-config`

SFP forced-type config (sfp/config)

- docs/api: `sfp/config`

### `fbx system sfp-config show`

`GET sfp/config`

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

### `fbx system sfp-config set [key=value …]`

`PUT sfp/config`

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

## `fbx system licenses`

open-source licenses of the firmware

- docs/api: `licenses/`

### `fbx system licenses`

`GET licenses/`

Response:

```json
{
  "result": [
    {
      "license": "syn-license",
      "name": "device-a",
      "version": "syn-version"
    },
    {
      "license": "syn-license",
      "name": "device-b",
      "version": "syn-version"
    }
  ],
  "success": true
}
```

Terminal:

```text
          system licenses           
 name      version      license     
 device-a  syn-version  syn-license 
 device-b  syn-version  syn-license 
-- 2 entries
```

## `fbx system license`

one license's full text (licenses/<name>/)

- docs/api: `licenses/{name}/`

### `fbx system license <name>`

`GET licenses/{name}/`

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

## When it fails

Examples on `fbx system health`; the error
envelope is exactly what the box answers; the CLI prints
`<domain> <record> <op> failed: <msg>` and exits non-zero.

**invalid session**

```text
system health show failed: Invalid session
```

The session cookie expired. `fbx` re-authenticates once automatically (fresh challenge + login) before surfacing this; if it persists, run `fbx login`.

**box unreachable**

```text
system health show failed: unreachable: [Errno 65] no route to host
```

The box did not answer. Check the address (`FREEBOX_HOST`, default `fd0f:ee:b0::1`) and that you are on the box's LAN.

**validation error**

```text
system health show failed: unknown or invalid field
```

A body field the box does not accept. Field names come straight from docs/api/; `fbx api` is the escape hatch for anything undocumented.

