"""Synthetic payloads built from the docs/api/ response models.

ALL names are obviously fake (device-*, person-*, host-*): real LAN names are
private and must never appear in fixtures, docs or commits.
"""

CONNECTION = {"state": "up", "type": "ftth", "media": "ftth", "mode": "router",
              "ipv4": "82.64.1.2", "ipv6": "2a01:e0a:0:1::1",
              "rate_down": 1048576, "bw_down": 1000000000,
              "rate_up": 4096, "bw_up": 500000000}

SYSTEM = {"box_model": "Freebox Server", "firmware_version": "4.8.6",
          "version": "48.6", "cpu_model": "ARMv7", "board_name": "v7",
          "uptime": 90061, "fan_rpm": 1800, "fan_mode": "auto",
          "temp_sw": 52, "temp_cpuc": 61, "temp_cpub": 58, "temp_ntc1": 44,
          "mac": "aa:bb:cc:00:00:01", "serial": "FREEBOX-0000"}

HOST = {"id": "eth0:aa:bb:cc:00:00:02", "vendor_name": "ACME", "host_type": "desktop",
        "primary_name": "device-alpha", "interface": "eth0", "reachable": True,
        "primary_name_manual": False, "active": True, "persistent": False,
        "last_time_reachable": 1762500000, "l2ident": {"id": "aa:bb:cc:00:00:02"},
        "l3connectivities": [{"af": "ipv4", "addr": "192.168.1.50"},
                             {"af": "ipv6", "addr": "fd0f:ee:b0::50"}]}

STATION = {"id": "s1", "bssid": "aa:bb:cc:11:22:33", "mac": "aa:bb:cc:00:00:03",
           "hostname": "device-beta", "access_type": "wpa", "inactive": 0,
           "state": "associated", "tx_bytes": 1000, "rx_bytes": 2000,
           "tx_rate": 866700, "rx_rate": 650000, "signal": -52,
           "conn_duration": 3600, "host": {"primary_name": "device-beta"}}

TASK = {"id": 3, "name": "synthetic.iso", "status": "downloading",
        "progress": 42.0, "rx_speed": 5242880, "tx_speed": 0,
        "size": 3900700160, "uploaded": 0, "type": "bt"}

CALL = {"id": 1, "duration": 0, "datetime": 1762500000, "line_id": 0,
        "contact_id": 0, "number": "0600000001", "type": "missed",
        "name": "", "new": True, "outgoing": False}

DISK = {"id": 1, "connector": 0, "state": "enabled", "total_bytes": 4000787030016,
        "type": "hdd", "model": "SYN-WD40", "spinning": True, "temp": 34}
PARTITION = {"id": 1, "label": "syn-data", "state": "mounted", "path": "/disks/1/part1",
             "disk_id": 1, "total_bytes": 4000000000000, "used_bytes": 2000000000000,
             "free_bytes": 2000000000000, "fstype": "ext4"}
RAID = {"id": 1, "state": "in_sync", "name": "raid0", "level": "raid1",
        "array_size": 4000000000000, "raid_disks": 2, "degraded": False,
        "members": [{"id": 1, "role": "active", "disk_model": "SYN-WD40"}]}

# Real shape of the box payload (structure-only capture): nested
# fans/sensors arrays; the docs' flat field list was [inferred].
SYSTEM_NESTED = {"model_info": {"name": "fbxgw8-r1", "pretty_name": "Freebox Server",
                                "has_dsl": False},
                 "firmware_version": "4.8.6", "uptime_val": 90061,
                 "disk_status": "ok", "mac": "aa:bb:cc:00:00:01",
                 "serial": "FREEBOX-0000",
                 "fans": [{"id": 0, "name": "fan0", "value": 1800}],
                 "sensors": [{"id": 0, "name": "temp_sw", "value": 52},
                             {"id": 1, "name": "temp_cpuc", "value": 61},
                             {"id": 2, "name": "temp_ntc1", "value": 44}]}
