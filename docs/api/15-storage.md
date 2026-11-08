# Domain: storage (disks / partitions / RAID)

## `storage/config/`
- Form (`AjaxFormPanel`) GET/PUT. Field seen: `external_pm_enabled:bool`
  (SATA power management); more storage-pool fields on the same form
  `[inferred]`.

## `storage/disk/`
- rest proxy. `result` entries = `Fbx.os.app.settings.storage.DiskModel`:
  `id:int`, `connector:int`, `state:string`, `total_bytes:int`,
  `type:string`, `table_type:string`, `model:string`, `serial:string`,
  `firmware:string`, `spinning:bool`, `idle:bool`, `idle_duration:int`,
  `active_duration:int`, `time_before_spindown:int`, `temp:int`,
  `operation_pct:auto`, `read_requests:int`, `read_error_requests:int`,
  `write_requests:int`, `write_error_requests:int`, `title:string`,
  `disk_title:string`, `state_str:string` (computed).
- Disk state changes via record save (PUT): `state:"enabled"` mounts/enables;
  partition `state:"mounted"|"umounted"|"mounting"|"maintenance"` via
  partition save (see below).

## `storage/disk/<id>/format`
- Verb: PUT. Body: `jsonData:{table_type:"superfloppy", fs_type:"ext4",
  label:<string>}`. Used by the format dialog and the RAID wizard.

## `storage/partition/`
- rest proxy (4 call sites). `result` =
  `Fbx.os.app.settings.storage.PartitionModel`: `id:int`, `label:string`,
  `state:string`, `path:string`, `disk_id:int`, `total_bytes:int`,
  `used_bytes:int`, `free_bytes:int`, `fsck_result:string`,
  `fstype:string`, `operation_pct:auto`, `usage_pct:int`,
  `description:string`, `canFsck:bool` (computed). Belongs to a DiskModel.
- Partition state save (PUT record): `"umounted"→"mounted"` mounts.

## `storage/partition/<id>/check`
- Form URL for the fsck dialog; submit triggers the check
  `[inferred: verb via form submit, likely PUT]`.

## `storage/raid/`
- rest proxy + POST (create array) + DELETE (5 call sites).
  `result` = `Fbx.os.app.settings.storage.RaidModel`: `id:int`,
  `state:string`, `name:string`, `level:string` ("raid0|1|5|6|10"),
  `uuid:string`, `sync_action:string`, `sysfs_state:string`,
  `array_size:int`, `raid_disks:int`, `sync_speed:int`,
  `sync_completed_pos:int`, `sync_completed_end:int`,
  `sync_completed_percent:int`, `check_interval:int`, `last_check:int`,
  `next_check:int`, `degraded:bool`, `members:auto`, plus computed
  display fields. Members (`RaidMemberModel`): `id:int`, `array_id:int`,
  `role:string` ("faulty"/"missing"/"spare"/…), `set_name:string`,
  `set_uuid:string`, `dev_uuid:string`, `device_location:string`,
  `total_bytes:int`, `disk_serial:string`, `disk_model:string`,
  `disk_temp:string`.
- Record save (PUT) with `state:"stopped"` stops the array.

## `storage/raid/<id>/…` member operations
- `POST storage/raid/<id>/forcestart` — force-start a degraded array.
- `DELETE storage/raid/<id>/members/faulty` — remove faulty members.
- `PUT storage/raid/<id>/members` — body
  `jsonData:{members:[<disk ids>]}` (add members).
- `POST storage/raid/<id>/members/addspares` — add spares (no body).
  `[thin: spare-disk selection is client-side; body not captured]`

## `storage/internal_storage_state`
- Form URL, GET, polled every 1 s; shows internal SSD state summary.

## `/storage/reset_internal_storage` and `/storage/check_internal_storage`
- Verb: PUT, empty JSON body (`jsonData:{}`) — from the `ops` table of the
  internal-storage screen (`post_op` helper), then progress is tracked by
  polling `GET /storage/internal_storage_state` every 1 s
  (`monitor_op` reads `progress`/`success` fields `[inferred]`).
  Note these two are written with a leading slash in the bundle
  (`api_call:"/storage/…"`).

Observed quirk (2026-11-08): a box with no RAID array answers `storage/raid/`
with HTTP 500 "Erreur interne". `fbx storage overview` treats each sub-call as
optional and shows `raid: unavailable (box error: …)` instead of aborting.
