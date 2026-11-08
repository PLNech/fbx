# docs/api/15-storage.md — disks/partitions/RAID. The format/fsck/raid family is
# DESTRUCTIVE: every write there is gated behind --yes.
from ..spec import Rec

Rec("storage", "config", "storage/config/", "RU", singleton=True,
    note="storage config (external SATA power management etc.)")
Rec("storage", "disks", "storage/disk/", "L",
    cols=["id", "model", "state", "temp", "total_bytes", "spinning"],
    units={"total_bytes": "bytes"}, name_field="model")
Rec("storage", "disk", "storage/disk/{disk_id}", "RU", singleton=True,
    note="one disk; set state=enabled mounts/enables it")
Rec("storage", "format", "storage/disk/{disk_id}/format", "U", singleton=True, gate=True,
    note="FORMAT a disk: format table_type=superfloppy fs_type=ext4 label=… — "
         "DESTROYS DATA, needs --yes")
Rec("storage", "partitions", "storage/partition/", "L",
    cols=["id", "label", "state", "path", "fstype", "used_bytes", "total_bytes",
          "free_bytes", "fsck_result"],
    units={"used_bytes": "bytes", "total_bytes": "bytes", "free_bytes": "bytes"},
    name_field="label")
Rec("storage", "partition", "storage/partition/{partition_id}", "RU", singleton=True,
    note="one partition; set state=mounted|umounted")
Rec("storage", "fsck", "storage/partition/{partition_id}/check", "U", singleton=True,
    gate=True, note="run a filesystem check — needs --yes")
Rec("storage", "raid", "storage/raid/", "LCUD", gate="CD",
    cols=["id", "name", "level", "state", "degraded", "array_size", "sync_action"],
    units={"array_size": "bytes"}, name_field="name",
    note="RAID arrays — add/rm create/destroy arrays, needs --yes")
Rec("storage", "raid-array", "storage/raid/{raid_id}", "RU", singleton=True, gate="U",
    note="one array; set state=stopped stops it — needs --yes")
Rec("storage", "raid-forcestart", "storage/raid/{raid_id}/forcestart", "A",
    singleton=True, gate=True, note="force-start a degraded array — needs --yes")
Rec("storage", "raid-members", "storage/raid/{raid_id}/members", "U", singleton=True,
    gate=True, note="add members: raid-members members='[<disk ids>]' — needs --yes")
Rec("storage", "raid-rm-faulty", "storage/raid/{raid_id}/members/faulty", "D",
    singleton=True, gate=True, note="remove faulty members — needs --yes")
Rec("storage", "raid-addspares", "storage/raid/{raid_id}/members/addspares", "A",
    singleton=True, gate=True, note="add spares (body [thin in docs]) — needs --yes")
Rec("storage", "internal-state", "storage/internal_storage_state", "R",
    note="internal SSD state summary")
# The bundle writes these two with a leading slash; they are relative to
# apiBaseUrl like everything else (api_call joins), so stored here without it.
Rec("storage", "internal-reset", "storage/reset_internal_storage", "U", singleton=True,
    gate=True, note="reset internal storage — DESTROYS DATA, needs --yes")
Rec("storage", "internal-check", "storage/check_internal_storage", "U", singleton=True,
    gate=True, note="check internal storage — needs --yes")
