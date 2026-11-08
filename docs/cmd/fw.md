# `fbx fw`: command reference

15 records, 30 operations.

## `fbx fw incoming`

incoming port rules

- docs/api: `fw/incoming/`

### `fbx fw incoming list`

`GET fw/incoming/`

Response:

```json
{
  "result": [
    {
      "active": true,
      "description": "192.168.1.50",
      "enabled": true,
      "id": 1,
      "in_port": 8080,
      "type": "auto"
    },
    {
      "active": true,
      "description": "192.168.1.51",
      "enabled": true,
      "id": 2,
      "in_port": 8081,
      "type": "auto"
    }
  ],
  "success": true
}
```

Terminal:

```text
                   fw incoming                    
 id  type  in_port  enabled  active  description  
 1   auto  8080     yes      yes     192.168.1.50 
 2   auto  8081     yes      yes     192.168.1.51 
-- 2 entries
```

### `fbx fw incoming add [key=value …]`

`POST fw/incoming/`

Response:

```json
{
  "result": {
    "active": true,
    "description": "192.168.1.50",
    "enabled": true,
    "id": 1,
    "in_port": 8080,
    "type": "auto"
  },
  "success": true
}
```

Terminal:

```text
  active                     True
  description                192.168.1.50
  enabled                    True
  id                         1
  in_port                    8080
  type                       auto
```

### `fbx fw incoming set <id> [key=value …]`

`PUT fw/incoming/`

Response:

```json
{
  "result": {
    "active": true,
    "description": "192.168.1.50",
    "enabled": true,
    "id": 1,
    "in_port": 8080,
    "type": "auto"
  },
  "success": true
}
```

Terminal:

```text
  active                     True
  description                192.168.1.50
  enabled                    True
  id                         1
  in_port                    8080
  type                       auto
```

### `fbx fw incoming rm <id>`

`DELETE fw/incoming/`

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

## `fbx fw redir`

port forwards

- docs/api: `fw/redir/`

### `fbx fw redir list`

`GET fw/redir/`

Response:

```json
{
  "result": [
    {
      "comment": "synthetic entry 1",
      "enabled": true,
      "hostname": "device-a",
      "id": 1,
      "ip_proto": "192.168.1.50",
      "lan_ip": "192.168.1.50",
      "lan_port": 8080,
      "wan_port_end": 8080,
      "wan_port_start": 8080
    },
    {
      "comment": "synthetic entry 2",
      "enabled": true,
      "hostname": "device-b",
      "id": 2,
      "ip_proto": "192.168.1.51",
      "lan_ip": "192.168.1.51",
      "lan_port": 8081,
      "wan_port_end": 8081,
      "wan_port_start": 8081
    }
  ],
  "success": true
}
```

Terminal:

```text
                                              fw redir                                              
              wan_port_st                                                                           
 id  enabled  art          wan_port_end  ip_proto     lan_ip        lan_port  hostname  comment     
 1   yes      8080         8080          192.168.1.5  192.168.1.50  8080      device-a  synthetic   
                                         0                                              entry 1     
 2   yes      8081         8081          192.168.1.5  192.168.1.51  8081      device-b  synthetic   
                                         1                                              entry 2     
-- 2 entries
```

### `fbx fw redir add [key=value …]`

`POST fw/redir/`

Response:

```json
{
  "result": {
    "comment": "synthetic entry 1",
    "enabled": true,
    "hostname": "device-a",
    "id": 1,
    "ip_proto": "192.168.1.50",
    "lan_ip": "192.168.1.50",
    "lan_port": 8080,
    "wan_port_end": 8080,
    "wan_port_start": 8080
  },
  "success": true
}
```

Terminal:

```text
  comment                    synthetic entry 1
  enabled                    True
  hostname                   device-a
  id                         1
  ip_proto                   192.168.1.50
  lan_ip                     192.168.1.50
  lan_port                   8080
  wan_port_end               8080
  wan_port_start             8080
```

### `fbx fw redir set <id> [key=value …]`

`PUT fw/redir/`

Response:

```json
{
  "result": {
    "comment": "synthetic entry 1",
    "enabled": true,
    "hostname": "device-a",
    "id": 1,
    "ip_proto": "192.168.1.50",
    "lan_ip": "192.168.1.50",
    "lan_port": 8080,
    "wan_port_end": 8080,
    "wan_port_start": 8080
  },
  "success": true
}
```

Terminal:

```text
  comment                    synthetic entry 1
  enabled                    True
  hostname                   device-a
  id                         1
  ip_proto                   192.168.1.50
  lan_ip                     192.168.1.50
  lan_port                   8080
  wan_port_end               8080
  wan_port_start             8080
```

### `fbx fw redir rm <id>`

`DELETE fw/redir/`

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

## `fbx fw dmz`

DMZ config

- docs/api: `fw/dmz/`

### `fbx fw dmz show`

`GET fw/dmz/`

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

### `fbx fw dmz set [key=value …]`

`PUT fw/dmz/`

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

## `fbx fw upnp`

UPnP IGD forwardings; rm kicks one out

- docs/api: `upnpigd/redir/`

### `fbx fw upnp list`

`GET upnpigd/redir/`

Response:

```json
{
  "result": [
    {
      "desc": "synthetic entry 1",
      "enabled": true,
      "ext_port": 8080,
      "id": 1,
      "int_ip": "192.168.1.50",
      "int_port": 8080,
      "proto": "tcp",
      "remaining": 3600
    },
    {
      "desc": "synthetic entry 2",
      "enabled": true,
      "ext_port": 8081,
      "id": 2,
      "int_ip": "192.168.1.51",
      "int_port": 8081,
      "proto": "tcp",
      "remaining": 3660
    }
  ],
  "success": true
}
```

Terminal:

```text
                                      fw upnp                                       
 id  enabled  ext_port  proto  int_ip        int_port  desc               remaining 
 1   yes      8080      tcp    192.168.1.50  8080      synthetic entry 1  1h 0m     
 2   yes      8081      tcp    192.168.1.51  8081      synthetic entry 2  1h 1m     
-- 2 entries
```

### `fbx fw upnp rm <id> --yes` *(gated: add `--yes`)*

`DELETE upnpigd/redir/`

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

## `fbx fw upnp-config`

- docs/api: `upnpigd/config/`

### `fbx fw upnp-config show`

`GET upnpigd/config/`

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

### `fbx fw upnp-config set [key=value …]`

`PUT upnpigd/config/`

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

## `fbx fw upnpav-config`

- docs/api: `upnpav/config/`

### `fbx fw upnpav-config show`

`GET upnpav/config/`

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

### `fbx fw upnpav-config set [key=value …]`

`PUT upnpav/config/`

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

## `fbx fw samba`

Windows/Samba file sharing config

- docs/api: `netshare/samba/`

### `fbx fw samba show`

`GET netshare/samba/`

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

### `fbx fw samba set [key=value …]`

`PUT netshare/samba/`

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

## `fbx fw afp`

Apple file sharing config

- docs/api: `netshare/afp/`

### `fbx fw afp show`

`GET netshare/afp/`

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

### `fbx fw afp set [key=value …]`

`PUT netshare/afp/`

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

## `fbx fw ftp`

- docs/api: `ftp/config/`

### `fbx fw ftp show`

`GET ftp/config/`

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

### `fbx fw ftp set [key=value …]`

`PUT ftp/config/`

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

## `fbx fw tftp`

- docs/api: `tftp/config/`

### `fbx fw tftp show`

`GET tftp/config/`

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

### `fbx fw tftp set [key=value …]`

`PUT tftp/config/`

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

## `fbx fw network-control`

per-profile network control (parental) status

- docs/api: `network_control/`

### `fbx fw network-control`

`GET network_control/`

Response:

```json
{
  "result": [
    {
      "current_mode": "syn-current-mode",
      "next_change": 1762500000,
      "override": "syn-override",
      "override_mode": "syn-override-mode",
      "profile_id": "syn-profile-id",
      "profile_name": "syn-profile-name",
      "rule_mode": "syn-rule-mode"
    },
    {
      "current_mode": "syn-current-mode",
      "next_change": 1762500060,
      "override": "syn-override",
      "override_mode": "syn-override-mode",
      "profile_id": "syn-profile-id",
      "profile_name": "syn-profile-name",
      "rule_mode": "syn-rule-mode"
    }
  ],
  "success": true
}
```

Terminal:

```text
                                         fw network-control                                         
                                            override_mod                                            
 profile_id    profile_name  current_mode   e             rule_mode      next_change   override     
 syn-profile-  syn-profile-  syn-current-m  syn-override  syn-rule-mode  2025-11-07    syn-override 
 id            name          ode            -mode                        07:20                      
 syn-profile-  syn-profile-  syn-current-m  syn-override  syn-rule-mode  2025-11-07    syn-override 
 id            name          ode            -mode                        07:21                      
-- 2 entries
```

## `fbx fw nc-rules`

one profile's network-control rules [fields thin in docs]

- docs/api: `network_control/{profile_id}/rules`

### `fbx fw nc-rules <profile_id>`

`GET network_control/{profile_id}/rules`

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
  fw nc-rules   
 enabled  state 
 yes      up    
 yes      up    
-- 2 entries
```

## `fbx fw nc-migrate`

GET migration state / POST perform the allow-by-default migration (run needs --yes)

- docs/api: `network_control/migrate`

### `fbx fw nc-migrate show`

`GET network_control/migrate`

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

### `fbx fw nc-migrate run --yes` *(gated: add `--yes`)*

`POST network_control/migrate`

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

## `fbx fw ui-settings`

panel UI-state store (AppSettings)

- docs/api: `settings/`

### `fbx fw ui-settings`

`GET settings/`

Response:

```json
{
  "result": [
    {
      "id": 1,
      "name": "device-a"
    },
    {
      "id": 2,
      "name": "device-b"
    }
  ],
  "success": true
}
```

Terminal:

```text
fw ui-settings
 id  name     
 1   device-a 
 2   device-b 
-- 2 entries
```

## `fbx fw ui-settings-reset`

reset stored panel UI prefs; needs --yes

- docs/api: `settings/reset/`

### `fbx fw ui-settings-reset --yes` *(gated: add `--yes`)*

`DELETE settings/reset/`

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

Examples on `fbx fw incoming` list; the error
envelope is exactly what the box answers; the CLI prints
`<domain> <record> <op> failed: <msg>` and exits non-zero.

**invalid session**

```text
fw incoming list failed: Invalid session
```

The session cookie expired. `fbx` re-authenticates once automatically (fresh challenge + login) before surfacing this; if it persists, run `fbx login`.

**box unreachable**

```text
fw incoming list failed: unreachable: [Errno 65] no route to host
```

The box did not answer. Check the address (`FREEBOX_HOST`, default `fd0f:ee:b0::1`) and that you are on the box's LAN.

**validation error**

```text
fw incoming list failed: unknown or invalid field
```

A body field the box does not accept. Field names come straight from docs/api/; `fbx api` is the escape hatch for anything undocumented.

