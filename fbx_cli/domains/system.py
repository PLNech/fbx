# docs/api/01-login-auth.md + 02-system.md
# The session login itself is `fbx login` (auth core); these are the panel's
# account/session surface.
from ..spec import Rec

Rec("auth", "sessions", "sessions/", "L",
    cols=["id", "app_name", "device_name", "client_ip", "is_web_app", "start_time"],
    units={"start_time": "ts"}, name_field="app_name")
Rec("auth", "perms", "login/perms/", "R",
    note="permission names of the logged-in app (login/perms/)")
Rec("auth", "tokens", "authorization/", "LCUD",
    cols=["id", "app_name", "app_version", "app_id", "device_name", "token_validity"],
    name_field="app_name", gate="D",
    note="app pairings/tokens (authorization/): rm = revoke a pairing")

Rec("system", "health", "system/", "R", custom="system",
    note="firmware, uptime, temps, fan (system/), the box's health grid")
Rec("system", "reboot", "system/reboot/", "A", singleton=True, gate=True,
    note="reboot the box (system/reboot/): DESTRUCTIVE, needs --yes")
Rec("system", "shutdown", "system/shutdown", "A", singleton=True, gate=True,
    note="shut the box down (system/shutdown): DESTRUCTIVE, needs --yes")
Rec("system", "standby", "standby/config/", "RU", singleton=True,
    note="standby planning (mode: suspend | wifi_off)")
Rec("system", "lcd", "lcd/config/", "RU", singleton=True,
    note="front LCD: brightness, orientation, forced")
Rec("system", "ledstrip", "ledstrip/planning/", "RU", singleton=True,
    note="LED strip brightness/animation + planning")
Rec("system", "sfp-status", "sfp/status", "R",
    cols=["present", "link", "type", "used_type", "power_good", "vendor_name",
          "part_number", "serial_number"],
    name_field="part_number", note="SFP module status (sfp/status)")
Rec("system", "sfp-config", "sfp/config", "RU", singleton=True,
    note="SFP forced-type config (sfp/config)")
Rec("system", "licenses", "licenses/", "L",
    cols=["name", "version", "license"], name_field="name",
    note="open-source licenses of the firmware")
Rec("system", "license", "licenses/{name}/", "R",
    note="one license's full text (licenses/<name>/)")
