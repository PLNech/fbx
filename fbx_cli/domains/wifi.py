# docs/api/05-wifi.md
from ..spec import Rec

_STATION_COLS = ["hostname", "mac", "state", "signal", "tx_rate", "rx_rate", "inactive"]
_STATION_UNITS = {"tx_rate": "rate", "rx_rate": "rate", "inactive": "dur"}

Rec("wifi", "state", "wifi/state", "R", alias="status",
    note="global wifi state (the quick-toggle one)")
Rec("wifi", "config", "wifi/config/", "RU", singleton=True,
    note="wifi config — set enabled=true|false turns wifi on/off")
Rec("wifi", "config-reset", "wifi/config/reset", "A", singleton=True, gate=True,
    note="reset wifi config to defaults — needs --yes")
Rec("wifi", "ap", "wifi/ap/", "L", cols=["id", "config", "status"],
    name_field="id", note="access points / phys")
Rec("wifi", "ap-survey", "wifi/ap/{apid}/channel_survey_history/{ts}/", "R",
    note="channel-survey history snapshot for one AP")
Rec("wifi", "ap-stations", "wifi/ap/{apid}/stations/", "L",
    cols=_STATION_COLS, units=_STATION_UNITS, name_field="hostname",
    note="stations of one AP (ap spelling of /stations/)")
Rec("wifi", "bss", "wifi/bss/", "L",
    cols=["id", "phy_id", "status", "config", "use_shared_params"], name_field="id")
Rec("wifi", "bss-config", "wifi/bss/{bssid}/", "RU", singleton=True,
    note="one BSS (GET) / update incl. mesh partners (PUT)")
Rec("wifi", "stations", "wifi/bss/{bssid}/stations/", "L",
    cols=_STATION_COLS, units=_STATION_UNITS, name_field="hostname",
    note="associated stations of one BSS (bss spelling of /stations/)")
Rec("wifi", "mlo-config", "wifi/bss/{bssid}/mlo/config/", "RU", singleton=True,
    note="Wi-Fi 7 MLO config")
Rec("wifi", "mlo-combos", "wifi/bss/{bssid}/mlo/allowed_comb/", "R",
    note="allowed MLO combinations")
Rec("wifi", "mac-filter", "wifi/mac_filter/", "LCUD",
    cols=["mac", "hostname", "comment", "type"], name_field="hostname",
    note="MAC filter entries (wifi/mac_filter/)")
Rec("wifi", "custom-key", "wifi/custom_key/", "LC",
    cols=["id", "description", "remaining", "expire_date"], name_field="description",
    note="guest custom keys — add: description=… key=… duration=… access_type=…")
Rec("wifi", "guest-config", "wifi/custom_keys/config/", "RU", singleton=True,
    note="guest-network global config")
Rec("wifi", "wps-candidates", "wifi/wps/candidates/", "L",
    cols=["bssid", "ssid", "state", "wps_enabled", "encryption", "band"],
    name_field="ssid")
Rec("wifi", "wps-start", "wifi/wps/start/", "A", singleton=True,
    note="start a WPS pairing: wps-start bssid=<bssid>")
Rec("wifi", "wps-stop", "wifi/wps/stop/", "A", singleton=True, note="stop WPS pairing")
Rec("wifi", "wps-session", "wifi/wps/sessions/", "LD",
    cols=["id", "ssid", "active", "result", "mac", "start_date", "end_date"],
    units={"start_date": "ts", "end_date": "ts"}, name_field="ssid",
    note="WPS sessions; rm cancels the session")
Rec("wifi", "steering", "wifi/steering/config/", "RU", singleton=True,
    note="band-steering config")
Rec("wifi", "wizard", "wifi/wizard/", "RU", singleton=True,
    note="first-run wifi wizard config")
