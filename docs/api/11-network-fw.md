# Domain: firewall / port forwarding / shares / network control

## `fw/incoming/`
- rest proxy. `result` = `Fbx.os.app.settings.ports.PortInModel`:
  `id:string`, `type:string`, `in_port:int`, `netns:string`,
  `enabled:bool`, `readonly:bool`, `active:bool`, `min_port:int`,
  `max_port:int`, `port_valid:bool`, `description:string`.

## `fw/redir/`
- rest proxy. `result` = `Fbx.os.app.settings.ports.PortRedirModel`:
  `id:int`, `enabled:bool`, `wan_port_start:int`, `wan_port_end:int`,
  `ip_proto:string`, `lan_ip:string`, `lan_port:int`, `hostname:string`,
  `host:object`, `src_ip:string`, `comment:string`, `valid:bool`.

## `fw/dmz/`
- DMZ config form GET/PUT `[inferred]`.

## `upnpigd/redir/`
- rest proxy. `result` = `Fbx.os.app.settings.UpnpIgdRedirModel`:
  `id:string`, `enabled:bool`, `ext_src_ip:string`, `ext_port:int`,
  `proto:string`, `int_ip:string`, `desc:string`, `int_port:int`,
  `remaining:int`, `host:object`. (UPnP-created forwardings; DELETE to
  remove `[inferred]`.)

## `upnpigd/config/` and `upnpav/config/`
- Config forms GET/PUT `[thin]`.

## `netshare/samba/` and `netshare/afp/`
- File-sharing config forms (Windows/Samba, Apple) GET/PUT `[thin]`.

## `ftp/config/`
- FTP config form GET/PUT `[thin]`.

## `tftp/config/`
- TFTP config form GET/PUT `[thin]`.

## `network_control/` (per-profile parental control)
- rest proxy (`startParam/limitParam/pageParam` disabled).
  `result` entries = `Fbx.os.app.profiles.NetworkControlModel`:
  `profile_id:int`, `profile_name:string`, `profile_icon:string`,
  `next_change:int`, `override_mode:string`, `current_mode:string`,
  `override_until:int`, `rule_mode:string`, `override:bool`, `macs:auto`.
- Rule modes include `denied` and legacy values (`isLegacy`: mode !=
  "denied"); holiday calendar keys `:fr_school_holidays_a/_b/_c/_corse` are
  used as schedule references.
- `network_control/<profile_id>/rules` — restforeign proxy on the profile id.
  Rule records (fields not captured) `[thin]`.
- `network_control/migrate` — GET
  (`result.default_mode_migrated:bool`) + POST (perform the "allow by
  default" migration; shown once in an evolution dialog).

## `settings/` and `settings/reset/`
- `settings/` — rest proxy over `Fbx.os.core.AppSettingsModel`:
  `id:int`, `name:string`, `data:auto` — the panel's own UI-state store
  (window positions etc., backed by `Fbx.ux.state.AjaxProvider`).
  Wait: this store is persisted server-side under `settings/`.
- `settings/reset/` — DELETE (reset stored UI prefs).
  (Note: also a `settings/` form-family in the settings screens; the
  AppSettings usage is the confirmed proxy consumer.)
