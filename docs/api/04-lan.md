# Domain: lan / dhcp / dhcpv6 / switch / freeplug

## `lan/config/`
- GET/PUT (form + explicit GET). Bridge/Router mode, IP settings
  `[inferred from i18n keys]`.

## `lan/browser/`
- rest proxy. `result` entries = `Fbx.os.app.lanbrowser.HostModel`:
  `id:string`, `vendor_name:string`, `host_type:string`,
  `primary_name:string`, `interface:string`, `reachable:bool`,
  `primary_name_manual:bool`, `active:bool`, `persistent:bool`,
  `last_time_reachable:int`, `first_activity:int`, `last_activity:int`,
  `l2ident:object`, `network_control:object`, `mac:string`, `is_laa:bool`,
  `is_crappy_name:bool`, `icon_name:string`, `primary_name_fallback:string`,
  `info:object`, `domain_name:string`, `local_domain:string`,
  `domain_name_short:string`.
- Host update: PUT on `lan/browser/<id>` via record save `[inferred]`.

## `lan/browser/pub/`
- Same model, "public/API-visible" subset of hosts `[inferred from name]`.

## `lan/wol/pub/`
- Verb: POST. Body: `jsonData:{mac:<string>, password:<string>}` (Wake-on-LAN).

## `lan/routes/` (bundle shows `"/lan/routes/"` with a leading slash)
- rest proxy + explicit GET and PUT. `result` entries =
  `Fbx.os.app.settings.RouteModel`: `prefix:string`, `gateway:string`,
  `enabled:bool`, `description:string`. (Static IPv6/IPv4 routes.)

## `dhcp/config/`
- Form GET/PUT `[inferred]`.

## `dhcp/static_lease/`
- rest proxy. `result` = `Fbx.os.app.settings.DhcpStaticLeaseModel`:
  `id:string`, `mac:string`, `hostname:string`, `host:object`, `ip:string`,
  `comment:string`, `options:object`.

## `dhcp/dynamic_lease/`
- rest proxy (read-only list). `result` =
  `Fbx.os.app.settings.DhcpDynamicLeaseModel`: `mac:string`, `ip:string`,
  `hostname:string`, `host:object`, `is_static:bool`, `assign_time:int`,
  `refresh_time:int`, `lease_remaining:int`.

## `dhcpv6/config/`
- Form GET/PUT (2 call sites).

## `switch/status/`
- rest proxy GET. Port list `[thin]`.

## `switch/port/` and `switch/port/<id>` (bundle also shows literal `switch/port/1`)
- rest proxy. `result` = `Fbx.os.app.settings.SwitchPortModel`: `id:int`,
  `name:string`, `rrd_id:string`, `duplex:string`, `mode:string`,
  `speed:string`, `link:string`, `mac_list:auto`, `str:string`.

## `freeplug/`
- rest proxy (list of CPL/freeplug networks).
- Networks: `Fbx.os.app.settings.FreeplugNetworkModel` = `id:string`.
- Members: `Fbx.os.app.settings.FreeplugModel`: `id:string`,
  `net_role:string`, `net_id:string`, `model:string`,
  `eth_port_status:string`, `eth_speed:int`, `inactive:int`, `local:bool`,
  `has_network:bool`, `eth_full_duplex:bool`, `rx_rate:int`, `tx_rate:int`.

## `freeplug/<id>/reset/`
- Verb: POST (no body). From `FreeplugModel.reboot()`.
