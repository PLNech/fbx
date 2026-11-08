# docs/api/03-connection.md
from ..spec import Rec

Rec("connection", "basic", "connection", "R",
    note="bare connection status (connection) — rates and state")
Rec("connection", "full", "connection/full/", "R", custom="connection",
    alias="wan", cols=["state", "type", "mode", "media", "ipv4", "ipv6",
                              "rate_down", "rate_up", "bw_down", "bw_up"],
    units={"rate_down": "rate", "rate_up": "rate", "bw_down": "rate", "bw_up": "rate"},
    note="full WAN state incl. IPs and bandwidth (connection/full/)")
Rec("connection", "aggregation", "connection/aggregation", "R",
    note="bonding aggregation status")
Rec("connection", "lte-aggregation", "connection/lte/aggregation", "R",
    note="4G aggregation status")
Rec("connection", "lte-backup", "connection/lte/backup", "R", note="LTE backup status/config")
Rec("connection", "xdsl", "connection/xdsl/", "R", note="xDSL line stats")
Rec("connection", "config", "connection/config/", "RU", singleton=True,
    note="connection settings (ping, mtu, remote access fields ride here [inferred])")
Rec("connection", "ipv6-config", "connection/ipv6/config/", "RU", singleton=True)
Rec("connection", "ddns", "connection/ddns/all/", "R", note="DDNS providers list")
Rec("connection", "ddns-status", "connection/ddns/all/status/", "R",
    note="DDNS providers status")
Rec("connection", "logs", "connection/logs/", "LD", gate="D",
    cols=["id", "type", "state", "conn", "link", "date", "bw_down", "bw_up"],
    units={"date": "ts", "bw_down": "rate", "bw_up": "rate"},
    note="WAN connection history — rm CLEARS the log (needs --yes)")
Rec("connection", "rrd", "rrd/", "A",
    note="graphs time series: db=… precision=… date_start=… date_end=… fields=[…]")
Rec("connection", "domains", "domain/owned/", "LC", gate="C",
    cols=["id", "type", "owner", "default"], name_field="id",
    note="owned DNS domains — add registers one (domain/owned/)")
Rec("connection", "domain-config", "domain/config/", "RU", singleton=True,
    note="default remote-access domain (domain/config/)")
Rec("connection", "domain-availability", "domain/availability/", "R",
    note="check a domain's availability: domain-availability <name> [tld=…]")
Rec("connection", "domain-reserve", "domain/reserve/", "A", gate=True,
    note="reserve a box domain (domain/reserve/) — write, needs --yes")
