# docs/api/04-lan.md
from ..spec import Rec

Rec("lan", "config", "lan/config/", "RU", singleton=True,
    note="LAN mode/IP settings (lan/config/)")
Rec("lan", "devices", "lan/browser/pub/", "L",
    cols=["primary_name", "vendor_name", "host_type", "interface", "reachable",
          "last_time_reachable"],
    units={"last_time_reachable": "ts"}, name_field="primary_name",
    note="the LAN table, API-visible subset (lan/browser/pub/)")
Rec("lan", "hosts-all", "lan/browser/", "L",
    cols=["primary_name", "vendor_name", "host_type", "interface", "reachable",
          "persistent", "last_time_reachable"],
    units={"last_time_reachable": "ts"}, name_field="primary_name",
    note="full host table incl. never-connected (lan/browser/)")
Rec("lan", "host", "lan/browser/", "U", name_field="primary_name",
    note="rename/configure one host record (PUT lan/browser/<id>)")
Rec("lan", "wol", "lan/wol/pub/", "A",
    note="wake-on-lan: wol mac=AA:BB:CC:DD:EE:FF [password=…]")
Rec("lan", "routes", "lan/routes/", "LCUD", gate="D",
    cols=["prefix", "gateway", "enabled", "description"], name_field="prefix",
    note="static routes (lan/routes/)")
Rec("lan", "dhcp-config", "dhcp/config/", "RU", singleton=True)
Rec("lan", "static-lease", "dhcp/static_lease/", "LCUD",
    cols=["hostname", "mac", "ip", "comment"], name_field="hostname",
    note="static DHCP leases (dhcp/static_lease/)")
Rec("lan", "leases", "dhcp/dynamic_lease/", "L",
    cols=["hostname", "mac", "ip", "is_static", "lease_remaining"],
    units={"lease_remaining": "dur"}, name_field="hostname",
    note="dynamic DHCP leases (read-only)")
Rec("lan", "dhcpv6", "dhcpv6/config/", "RU", singleton=True)
Rec("lan", "switch-status", "switch/status/", "L", note="switch port states")
Rec("lan", "switch-port", "switch/port/", "L",
    cols=["id", "name", "duplex", "mode", "speed", "link"],
    name_field="name", note="switch port details (switch/port/)")
Rec("lan", "freeplug", "freeplug/", "L", cols=["id"],
    note="CPL/freeplug networks (members via the escape hatch)")
Rec("lan", "freeplug-reset", "freeplug/{net_id}/reset/", "A", singleton=True, gate=True,
    note="reboot a freeplug member (freeplug/<id>/reset/); needs --yes")
