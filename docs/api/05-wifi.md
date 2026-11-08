# Domain: wifi

## `wifi/config` and `wifi/config/`
- GET (form load), PUT (save). PUT body seen:
  `jsonData:{enabled:<bool>}` (global wifi toggle); full form fields
  `[inferred: ap config + channel + country etc]`.
- `wifi/config/reset`: POST, resets wifi config `[thin]`.

## `wifi/state`
- Verb: GET (2 call sites). Global wifi state for the tray/quick toggle
  `[thin]`.

## `wifi/ap/`
- rest proxy (list of access points / phys). 7 call sites.
- AP record fields `[inferred from bss/ap navigation code]`: `id`,
  `config`, `status`, `bss` list.
- Composed: `wifi/ap/<apid>/channel_survey_history/<ts>/`; GET survey
  history snapshot.

## `wifi/bss/`
- GET (list BSS), PUT (update; PUT body seen:
  `jsonData:{partners:<data>}`; mesh partners). 7 call sites.
- `result` = `Fbx.os.app.settings.wifi.WifiBssModel`: `id:string`,
  `phy_id:int`, `status:object`, `config:object`, `use_shared_params:bool`.
- Composed: `wifi/bss/<bssid>/`; GET/PUT single BSS;
  `wifi/bss/<bssid>/mlo/config/`: GET/PUT MLO (Wi-Fi 7) config;
  `wifi/bss/<bssid>/mlo/allowed_comb/`: GET allowed MLO combos.

## `wifi/stations/`?: actually stations come from `"/stations/"` literal
- `Fbx.os.app.settings.wifi.WifiStationModel` fields: `id:string`,
  `bssid:string`, `mac:string`, `hostname:string`, `custom_key_id:int`,
  `access_type:string`, `inactive:int`, `state:string`, `tx_bytes:int`,
  `rx_bytes:int`, `tx_rate:int`, `rx_rate:int`, `signal:int`,
  `conn_duration:int`, `host:object`, `flags:object`, `last_rx:object`,
  `last_tx:object`. URL composed as `<bss url>stations/` or similar
  `[inferred: the literal "/stations/" is appended to a bss base]`.
- `"/channel_survey_history/"` literal likewise appends to an ap/bss base.

## `wifi/mac_filter/`
- rest proxy. `result` = `Fbx.os.app.settings.WifiMacModel`: `id:string`,
  `mac:string`, `hostname:string`, `comment:string`, `type:string`,
  `host:object`.

## `wifi/custom_key/` and `wifi/custom_keys/config/`
- `wifi/custom_key/`: rest proxy + POST create. POST body:
  `jsonData:{description:<string>, key:<string>, max_use_count:<int>,
  duration:<int>, access_type:<string>}`.
- `result` = `Fbx.os.app.settings.wifi.WifiCustomKeyModel`: `id:int`,
  `remaining:int`, `expire_date:str`, `params:object`, `params_str:object`,
  `users:array`, `users_str:object`, `description:str`.
- `wifi/custom_keys/config/`: rest proxy (guest-network key global config).

## Guest network model (screen data)
- `Fbx.os.app.settings.wifi.WifiGuestModel`: `ssid:string`,
  `ssid_read_only:bool`, `hide_ssid:bool`, `encryption:string`.
- `Fbx.os.app.settings.wifi.WifiNeighborModel`: `bssid:string`,
  `channel_width:int`, `capabilities:object`, `ssid:string`, `channel:int`,
  `secondary_channel:int`, `band:string`, `signal:int`.

## WPS
- `wifi/wps/candidates/`: rest proxy GET. `result` =
  `WifiWpsCandidateModel`: `bss_uuid:string`, `ssid:string`,
  `bssid:string`, `state:string`, `wps_enabled:bool`, `encryption:string`,
  `band:string`, `display_ssid:string`.
- `wifi/wps/start/`: POST `jsonData:{bssid:<string>}`.
- `wifi/wps/sessions/`: GET (rest proxy) + DELETE (cancel). `result` =
  `WifiWpsSessionModel`: `id:int`, `bss_uuid:string`, `ssid:string`,
  `active:bool`, `result:string`, `mac:string`, `start_date:date`,
  `end_date:int`. Also composed `wifi/wps/sessions/<sessionId>` (poll).
- `wifi/wps/stop/`: POST `jsonData:{bssid:<string>}`.

## `wifi/steering/config/`
- Band-steering config form GET/PUT `[thin]`.

## `wifi/wizard/`
- GET + PUT: first-run wifi wizard config `[thin]`.
