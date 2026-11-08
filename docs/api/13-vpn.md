# Domain: vpn (server) / vpn_client

## `vpn/`
- rest proxy. `result` entries = `Fbx.os.app.settings.VpnServerModel`:
  `name:string`, `type:string`, `state:string`, `connection_count:int`,
  `auth_connection_count:int`.
- `vpn/<vpnid>/config/` — GET/PUT (per-server config, composed with `id`).

## `vpn/ip_pool/`
- Verb: GET (2 call sites). Address pools for VPN users `[thin]`.

## `vpn/user/`
- rest proxy + explicit PUT. `result` =
  `Fbx.os.app.settings.VpnServerUserModel`: `id:string`, `login:string`,
  `type:string`, `password:string` (write-only on create/update
  `[inferred]`), `password_set:bool`, `ip_reservation:string`,
  `conf_wireguard:object`.

## `vpn/connection/`
- rest proxy (live VPN server connections). `result` =
  `Fbx.os.app.settings.VpnServerConnModel`: `id:string`, `rx_bytes:int`,
  `tx_bytes:int`, `authenticated:bool`, `user:string`, `vpn:string`,
  `src_ip:string`, `src_port:int`, `local_ip:string`, `auth_time:string`.

## `vpn/<vpnid>/config/`
- GET/PUT — per-server-type config (server list lives under `vpn/`
  `[inferred]`). The bare `vpn/` rest proxy entries =
  `Fbx.os.app.settings.VpnServerModel`: `name:string`, `type:string`,
  `state:string`, `connection_count:int`, `auth_connection_count:int`.

## `vpn/download_config/`
- GET. Composed: `vpn/download_config/<vpnid>/<login>/json` — download a
  client config (OpenVPN/WireGuard profile) for user `<login>` as JSON.
  (Bundle shows both a trailing-`/json` composed form and the plain
  `vpn/download_config/` literal.)

## `vpn_client/*` (outbound VPN client)
- `vpn_client/config/` — rest proxy. `result` =
  `Fbx.os.app.settings.VpnClientConfigModel`: `id:string`,
  `description:string`, `type:string` (pptp/openvpn/wireguard),
  `active:bool`, `conf_pptp:object`, `conf_openvpn:object`,
  `conf_wireguard:object`.
- `vpn_client/status/` — GET. Client connection status `[thin]`.
- `vpn_client/log/` — GET. Client log lines `[thin]`.
- `vpn_client/apps/` — GET. Per-app routing list (which apps use the
  client VPN) `[inferred from name]`.

## `vpn_client/` server upload of .ovpn/conf files
- Not captured; the client config screen likely posts the config file to a
  sub-path of `vpn_client/config/` `[inferred — no call site found]`.
