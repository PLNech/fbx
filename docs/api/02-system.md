# Domain: system / standby / lcd / ledstrip / sfp / licenses

## `system/`
- Proxy: rest (5+ call sites; the "fan / temp / disks" dashboard grid and the
  general system form reload it every second).
- `result` (singleton object) fields used by views `[inferred from widget
  bindings]`: `fan_rpm`, `temp_sw`, `temp_sw1`.., `temp_cpuc', `temp_cpub`,
  `temp_ntc1..3`, `fan_mode`, `fan_pwm`, `uptime`, `version`, `cpu_model`,
  `board_name`, `mac`, `serial`, `box_model`, `firmware_version`,
  `reboot_requested` …: names not all verbatim in captured slices; the
  confirmed literal in the bundle is none beyond the URL, so treat the whole
  field list as `[inferred from typical Freebox system info]`.
- `system/reboot/`: POST, no body. From `Fbx.os.gui.Environment.__doReboot`
  (reboot confirm dialog).
- `system/shutdown`: POST, no body. Same dialog ("shutdown").

## `standby/config/`
- Used by the shared planning widget (`Fbx.os.app.settings.Planning`,
  `config.url`) and standby form.
- Fields (form): planning schedule grid; mode select values `suspend`
  (full standby) or `wifi_off` `[transcribed from the combo store]`.
- Verbs: GET/PUT `[inferred from AjaxFormPanel load/submit]`.

## `lcd/config/`
- Form panel (`Fbx.os.app.settings.Lcd`), rest proxy, 3 call sites.
- Fields (form items): brightness slider, orientation combo, forced
  `[inferred from i18n keys settings.misc-lcd*]`.

## `ledstrip/planning/`
- URL of the planning widget on the LED-strip settings screen; form fields
  `led_strip_brightness:int`, `led_strip_animation:string`,
  `available_led_strip_animations:object` (from
  `Fbx.os.app.settings.LedStripConfigModel`), plus planning schedule and a
  mode value `ledstrip_off`.

## `sfp/config` and `sfp/status`
- `sfp/status`: rest proxy GET; `result` = `Fbx.os.app.settings.SfpModel`:
  `present:bool`, `eeprom_valid:bool`, `supported:bool`, `type:string`,
  `used_type:string`, `power_good:bool`, `link:bool`, `vendor_name:string`,
  `part_number:string`, `hardware_rev:string`, `serial_number:string`.
- `sfp/config`: rest proxy; `result` =
  `Fbx.os.app.settings.SfpConfigModel`: `sfp_type_forced:bool`,
  `sfp_type_forced_value:string`, `available_sfp_types:object`.
  (Both spellings `sfp/config` and `sfp/config/` appear.)

## `licenses/`
- rest proxy, GET. `result` entries = `Fbx.os.app.settings.LicenseModel`:
  `url:string`, `name:string`, `version:string`, `license:string`.
- Composed: `licenses/<name>/` (name URL-encoded); open-source license text
  fetch `[inferred from encodeURIComponent(me.get("name")) call site]`.
