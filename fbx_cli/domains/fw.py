# docs/api/11-network-fw.md + 12-accounts.md
from ..spec import Rec

Rec("fw", "incoming", "fw/incoming/", "LCUD",
    cols=["id", "type", "in_port", "enabled", "active", "description"],
    name_field="description", note="incoming port rules")
Rec("fw", "redir", "fw/redir/", "LCUD",
    cols=["id", "enabled", "wan_port_start", "wan_port_end", "ip_proto", "lan_ip",
          "lan_port", "hostname", "comment"],
    name_field="hostname", note="port forwards")
Rec("fw", "dmz", "fw/dmz/", "RU", singleton=True, note="DMZ config")
Rec("fw", "upnp", "upnpigd/redir/", "LD", gate="D",
    cols=["id", "enabled", "ext_port", "proto", "int_ip", "int_port", "desc", "remaining"],
    units={"remaining": "dur"}, name_field="desc",
    note="UPnP IGD forwardings; rm kicks one out")
Rec("fw", "upnp-config", "upnpigd/config/", "RU", singleton=True)
Rec("fw", "upnpav-config", "upnpav/config/", "RU", singleton=True)
Rec("fw", "samba", "netshare/samba/", "RU", singleton=True,
    note="Windows/Samba file sharing config")
Rec("fw", "afp", "netshare/afp/", "RU", singleton=True, note="Apple file sharing config")
Rec("fw", "ftp", "ftp/config/", "RU", singleton=True)
Rec("fw", "tftp", "tftp/config/", "RU", singleton=True)
Rec("fw", "network-control", "network_control/", "L",
    cols=["profile_id", "profile_name", "current_mode", "override_mode", "rule_mode",
          "next_change", "override"],
    units={"next_change": "ts"}, name_field="profile_name",
    note="per-profile network control (parental) status")
Rec("fw", "nc-rules", "network_control/{profile_id}/rules", "L",
    note="one profile's network-control rules [fields thin in docs]")
Rec("fw", "nc-migrate", "network_control/migrate", "RA",
    note="GET migration state / POST perform the allow-by-default migration (run needs --yes)",
    gate="A")
Rec("fw", "ui-settings", "settings/", "L", cols=["id", "name"], name_field="name",
    note="panel UI-state store (AppSettings)")
Rec("fw", "ui-settings-reset", "settings/reset/", "D", singleton=True, gate=True,
    note="reset stored panel UI prefs; needs --yes")

Rec("accounts", "profiles", "profile/", "LCUD",
    cols=["id", "name", "icon"], name_field="name", gate="D",
    note="profiles (family): rm needs --yes")
Rec("accounts", "groups", "group/", "L", note="permission groups [thin in docs]")
Rec("accounts", "notif-targets", "notif/targets/", "LCUD",
    cols=["id", "name", "type", "api_url", "message_type", "last_use"],
    units={"last_use": "ts"}, name_field="name",
    note="notification webhook targets")
Rec("accounts", "taskcount", "taskcount/", "L", cols=["name"],
    note="background task counts per name")
# Guest mode / remote access fields ride on an [inferred] settings endpoint
# (connection/config/ is the likely host), covered by `fbx connection config`.
