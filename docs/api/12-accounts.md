# Domain: accounts / profiles / groups / notifications

## `profile/`
- rest proxy + explicit DELETE. `result` entries (fields from profile form
  bindings) `[partial]`: `id`, `name`, `icon`, `allowed_permissions`,
  `cdayranges` (holiday calendar ranges, referenced by network_control),
  guest-related flags `[inferred]`.
- `profile/<profile_id>` — PUT (update) / DELETE `[inferred]`.

## `group/`
- rest proxy. Groups of permission profiles `[thin: only the URL visible;
  group records carry permission lists — inferred]`.

## `notif/targets/`
- rest proxy. Notification targets (webhooks). `result` =
  `Fbx.os.app.accounts.NotificationTargetModel`: `id:string`,
  `last_use:int`, `type:string`, `name:string`, `api_url:string`,
  `message_type:string`, `subscriptions:object`, `subscriptions_str:string`
  (computed), `last_use_str:string` (computed).
- The settings screen shows a "server-url" per target (`api_url`) — target
  receives push notifications of `message_type` for subscribed events.

## `taskcount/`
- rest proxy. `result` = `Fbx.os.core.TaskCountModel`: `name:string` —
  count of background tasks per name; drives the task-count badge
  `[inferred]`.

## AppSettings persistence
- Covered in `11-network-fw.md` under `settings/` —
  `Fbx.ux.state.AjaxProvider` saves UI state records
  (`{name, data}`) via record `save()`; disabled for mobile devices and
  when the box reports the settings DB is unavailable.

## Guest mode / remote access (accounts screen)
- Form fields on the accounts screen (saved via the main settings form):
  `disable_guest`, `remote_access` (bool), `remote_access_port`,
  `https_port`, `https_available`, `api_remote_access` (bool) — these ride
  on a settings endpoint `[inferred: the form's url field was not captured;
  likely `connection/config/` or a dedicated settings form]`.
