# docs/api/13-vpn.md + 14-airmedia.md + 15-storage.md
from ..spec import Rec

Rec("vpn", "servers", "vpn/", "L",
    cols=["name", "type", "state", "connection_count", "auth_connection_count"],
    name_field="name")
Rec("vpn", "server-config", "vpn/{vpn_id}/config/", "RU", singleton=True,
    note="per-server config (composed with the server id)")
Rec("vpn", "ip-pool", "vpn/ip_pool/", "R", note="VPN address pools")
Rec("vpn", "users", "vpn/user/", "LCUD",
    cols=["id", "login", "type", "password_set", "ip_reservation"], name_field="login",
    note="VPN users — password is write-only: users add login=… password=…")
Rec("vpn", "connections", "vpn/connection/", "L",
    cols=["user", "vpn", "src_ip", "rx_bytes", "tx_bytes", "auth_time"],
    units={"rx_bytes": "bytes", "tx_bytes": "bytes", "auth_time": "ts"},
    name_field="user", note="live VPN server connections")
Rec("vpn", "client-config-dl", "vpn/download_config/{vpn_id}/{login}/json", "R",
    note="download a client VPN profile as JSON")
Rec("vpn", "client-config", "vpn_client/config/", "LCUD",
    cols=["id", "description", "type", "active"], name_field="description",
    note="outbound VPN client configs (pptp/openvpn/wireguard)")
Rec("vpn", "client-status", "vpn_client/status/", "R")
Rec("vpn", "client-log", "vpn_client/log/", "L")
Rec("vpn", "client-apps", "vpn_client/apps/", "R",
    note="per-app routing through the client VPN")

Rec("airmedia", "config", "airmedia/config/", "RU", singleton=True,
    note="airmedia: enabled=true|false password=…")
Rec("airmedia", "receivers", "airmedia/receivers/", "L",
    cols=["name", "password_protected"], name_field="name")
Rec("airmedia", "cast", "airmedia/receivers/{receiver_name}/", "A", singleton=True,
    note="cast/stop on one receiver: cast action=start media_type=video media=… [password=…]")
