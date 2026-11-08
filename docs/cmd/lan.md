# `fbx lan`: command reference

14 records, 23 operations.

## `fbx lan config`

LAN mode/IP settings (lan/config/)

- docs/api: `lan/config/`

### `fbx lan config show`

`GET lan/config/`

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

### `fbx lan config set [key=value …]`

`PUT lan/config/`

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

## `fbx lan devices`

the LAN table, API-visible subset (lan/browser/pub/)

- docs/api: `lan/browser/pub/`

### `fbx lan devices`

`GET lan/browser/pub/`

Response:

```json
{
  "result": [
    {
      "host_type": "syn-host-type",
      "interface": "syn-interface",
      "last_time_reachable": 1762500000,
      "primary_name": "syn-primary-name",
      "reachable": true,
      "vendor_name": "syn-vendor-name"
    },
    {
      "host_type": "syn-host-type",
      "interface": "syn-interface",
      "last_time_reachable": 1762500060,
      "primary_name": "syn-primary-name",
      "reachable": true,
      "vendor_name": "syn-vendor-name"
    }
  ],
  "success": true
}
```

Terminal:

```text
                                           lan devices                                           
 primary_name      vendor_name      host_type      interface      reachable  last_time_reachable 
 syn-primary-name  syn-vendor-name  syn-host-type  syn-interface  yes        2025-11-07 07:20    
 syn-primary-name  syn-vendor-name  syn-host-type  syn-interface  yes        2025-11-07 07:21    
-- 2 entries
```

## `fbx lan hosts-all`

full host table incl. never-connected (lan/browser/)

- docs/api: `lan/browser/`

### `fbx lan hosts-all`

`GET lan/browser/`

Response:

```json
{
  "result": [
    {
      "host_type": "syn-host-type",
      "interface": "syn-interface",
      "last_time_reachable": 1762500000,
      "persistent": true,
      "primary_name": "syn-primary-name",
      "reachable": true,
      "vendor_name": "syn-vendor-name"
    },
    {
      "host_type": "syn-host-type",
      "interface": "syn-interface",
      "last_time_reachable": 1762500060,
      "persistent": true,
      "primary_name": "syn-primary-name",
      "reachable": true,
      "vendor_name": "syn-vendor-name"
    }
  ],
  "success": true
}
```

Terminal:

```text
                                           lan hosts-all                                            
                                                                                     last_time_reac 
 primary_name    vendor_name    host_type      interface      reachable  persistent  hable          
 syn-primary-na  syn-vendor-na  syn-host-type  syn-interface  yes        yes         2025-11-07     
 me              me                                                                  07:20          
 syn-primary-na  syn-vendor-na  syn-host-type  syn-interface  yes        yes         2025-11-07     
 me              me                                                                  07:21          
-- 2 entries
```

## `fbx lan host`

rename/configure one host record (PUT lan/browser/<id>)

- docs/api: `lan/browser/`

### `fbx lan host <id> [key=value …]`

`PUT lan/browser/`

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

## `fbx lan wol`

wake-on-lan: wol mac=AA:BB:CC:DD:EE:FF [password=…]

- docs/api: `lan/wol/pub/`

### `fbx lan wol`

`POST lan/wol/pub/`

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

## `fbx lan routes`

static routes (lan/routes/)

- docs/api: `lan/routes/`

### `fbx lan routes list`

`GET lan/routes/`

Response:

```json
{
  "result": [
    {
      "description": "192.168.1.50",
      "enabled": true,
      "gateway": "syn-gateway",
      "prefix": "syn-prefix"
    },
    {
      "description": "192.168.1.51",
      "enabled": true,
      "gateway": "syn-gateway",
      "prefix": "syn-prefix"
    }
  ],
  "success": true
}
```

Terminal:

```text
                   lan routes                   
 prefix      gateway      enabled  description  
 syn-prefix  syn-gateway  yes      192.168.1.50 
 syn-prefix  syn-gateway  yes      192.168.1.51 
-- 2 entries
```

### `fbx lan routes add [key=value …]`

`POST lan/routes/`

Response:

```json
{
  "result": {
    "description": "192.168.1.50",
    "enabled": true,
    "gateway": "syn-gateway",
    "prefix": "syn-prefix"
  },
  "success": true
}
```

Terminal:

```text
  description                192.168.1.50
  enabled                    True
  gateway                    syn-gateway
  prefix                     syn-prefix
```

### `fbx lan routes set <id> [key=value …]`

`PUT lan/routes/`

Response:

```json
{
  "result": {
    "description": "192.168.1.50",
    "enabled": true,
    "gateway": "syn-gateway",
    "prefix": "syn-prefix"
  },
  "success": true
}
```

Terminal:

```text
  description                192.168.1.50
  enabled                    True
  gateway                    syn-gateway
  prefix                     syn-prefix
```

### `fbx lan routes rm <id> --yes` *(gated: add `--yes`)*

`DELETE lan/routes/`

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

## `fbx lan dhcp-config`

- docs/api: `dhcp/config/`

### `fbx lan dhcp-config show`

`GET dhcp/config/`

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

### `fbx lan dhcp-config set [key=value …]`

`PUT dhcp/config/`

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

## `fbx lan static-lease`

static DHCP leases (dhcp/static_lease/)

- docs/api: `dhcp/static_lease/`

### `fbx lan static-lease list`

`GET dhcp/static_lease/`

Response:

```json
{
  "result": [
    {
      "comment": "synthetic entry 1",
      "hostname": "device-a",
      "ip": "192.168.1.50",
      "mac": "aa:bb:cc:00:00:40"
    },
    {
      "comment": "synthetic entry 2",
      "hostname": "device-b",
      "ip": "192.168.1.51",
      "mac": "aa:bb:cc:00:00:41"
    }
  ],
  "success": true
}
```

Terminal:

```text
                       lan static-lease                       
 hostname  mac                ip            comment           
 device-a  aa:bb:cc:00:00:40  192.168.1.50  synthetic entry 1 
 device-b  aa:bb:cc:00:00:41  192.168.1.51  synthetic entry 2 
-- 2 entries
```

### `fbx lan static-lease add [key=value …]`

`POST dhcp/static_lease/`

Response:

```json
{
  "result": {
    "comment": "synthetic entry 1",
    "hostname": "device-a",
    "ip": "192.168.1.50",
    "mac": "aa:bb:cc:00:00:40"
  },
  "success": true
}
```

Terminal:

```text
  comment                    synthetic entry 1
  hostname                   device-a
  ip                         192.168.1.50
  mac                        aa:bb:cc:00:00:40
```

### `fbx lan static-lease set <id> [key=value …]`

`PUT dhcp/static_lease/`

Response:

```json
{
  "result": {
    "comment": "synthetic entry 1",
    "hostname": "device-a",
    "ip": "192.168.1.50",
    "mac": "aa:bb:cc:00:00:40"
  },
  "success": true
}
```

Terminal:

```text
  comment                    synthetic entry 1
  hostname                   device-a
  ip                         192.168.1.50
  mac                        aa:bb:cc:00:00:40
```

### `fbx lan static-lease rm <id>`

`DELETE dhcp/static_lease/`

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

## `fbx lan leases`

dynamic DHCP leases (read-only)

- docs/api: `dhcp/dynamic_lease/`

### `fbx lan leases`

`GET dhcp/dynamic_lease/`

Response:

```json
{
  "result": [
    {
      "hostname": "device-a",
      "ip": "192.168.1.50",
      "is_static": "syn-is-static",
      "lease_remaining": 3600,
      "mac": "aa:bb:cc:00:00:40"
    },
    {
      "hostname": "device-b",
      "ip": "192.168.1.51",
      "is_static": "syn-is-static",
      "lease_remaining": 3660,
      "mac": "aa:bb:cc:00:00:41"
    }
  ],
  "success": true
}
```

Terminal:

```text
                                lan leases                                 
 hostname  mac                ip            is_static      lease_remaining 
 device-a  aa:bb:cc:00:00:40  192.168.1.50  syn-is-static  1h 0m           
 device-b  aa:bb:cc:00:00:41  192.168.1.51  syn-is-static  1h 1m           
-- 2 entries
```

## `fbx lan dhcpv6`

- docs/api: `dhcpv6/config/`

### `fbx lan dhcpv6 show`

`GET dhcpv6/config/`

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

### `fbx lan dhcpv6 set [key=value …]`

`PUT dhcpv6/config/`

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

## `fbx lan switch-status`

switch port states

- docs/api: `switch/status/`

### `fbx lan switch-status`

`GET switch/status/`

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
      lan       
 switch-status  
 enabled  state 
 yes      up    
 yes      up    
-- 2 entries
```

## `fbx lan switch-port`

switch port details (switch/port/)

- docs/api: `switch/port/`

### `fbx lan switch-port`

`GET switch/port/`

Response:

```json
{
  "result": [
    {
      "duplex": "syn-duplex",
      "id": 1,
      "link": "syn-link",
      "mode": "auto",
      "name": "device-a",
      "speed": "syn-speed"
    },
    {
      "duplex": "syn-duplex",
      "id": 2,
      "link": "syn-link",
      "mode": "auto",
      "name": "device-b",
      "speed": "syn-speed"
    }
  ],
  "success": true
}
```

Terminal:

```text
                   lan switch-port                   
 id  name      duplex      mode  speed      link     
 1   device-a  syn-duplex  auto  syn-speed  syn-link 
 2   device-b  syn-duplex  auto  syn-speed  syn-link 
-- 2 entries
```

## `fbx lan freeplug`

CPL/freeplug networks (members via the escape hatch)

- docs/api: `freeplug/`

### `fbx lan freeplug`

`GET freeplug/`

Response:

```json
{
  "result": [
    {
      "id": 1
    },
    {
      "id": 2
    }
  ],
  "success": true
}
```

Terminal:

```text
lan 
free
plug
 id 
 1  
 2  
-- 2 entries
```

## `fbx lan freeplug-reset`

reboot a freeplug member (freeplug/<id>/reset/); needs --yes

- docs/api: `freeplug/{net_id}/reset/`

### `fbx lan freeplug-reset <net_id> --yes` *(gated: add `--yes`)*

`POST freeplug/{net_id}/reset/`

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

Examples on `fbx lan config` show; the error
envelope is exactly what the box answers; the CLI prints
`<domain> <record> <op> failed: <msg>` and exits non-zero.

**invalid session**

```text
lan config show failed: Invalid session
```

The session cookie expired. `fbx` re-authenticates once automatically (fresh challenge + login) before surfacing this; if it persists, run `fbx login`.

**box unreachable**

```text
lan config show failed: unreachable: [Errno 65] no route to host
```

The box did not answer. Check the address (`FREEBOX_HOST`, default `fd0f:ee:b0::1`) and that you are on the box's LAN.

**validation error**

```text
lan config show failed: unknown or invalid field
```

A body field the box does not accept. Field names come straight from docs/api/; `fbx api` is the escape hatch for anything undocumented.

