# docs/api/07-downloads.md, the downloader
from ..spec import Rec

_TASK_COLS = ["id", "name", "status", "progress", "rx_speed", "tx_speed", "size"]
_TASK_UNITS = {"rx_speed": "rate", "tx_speed": "rate", "size": "bytes"}

Rec("downloads", "tasks", "downloads/", "LD", custom="tasks",
    cols=_TASK_COLS, units=_TASK_UNITS, name_field="name",
    note="downloader tasks; pause/resume via `downloads task set` status=…")
Rec("downloads", "add", "downloads/add", "A", form=True,
    note="enqueue a URL (form-encoded): downloads add download_url=https://… "
         "[username=… password=… archive_password=…]")
Rec("downloads", "task", "downloads/{task_id}", "RU", singleton=True,
    note="one task; set status=paused|downloading")
Rec("downloads", "trackers", "downloads/{task_id}/trackers", "LCUD",
    cols=["announce", "is_backup", "status", "nseeders", "nleechers", "is_enabled"],
    name_field="announce", note="per-task tracker list")
Rec("downloads", "peers", "downloads/{task_id}/peers", "L",
    cols=["host", "state", "client", "country_code", "tx_rate", "rx_rate", "progress"],
    units={"tx_rate": "rate", "rx_rate": "rate"}, name_field="host")
Rec("downloads", "files", "downloads/{task_id}/files", "LGU",
    cols=["name", "filepath", "status", "priority", "size", "progress", "todownload"],
    units={"size": "bytes", "progress": "pct"}, name_field="name",
    note="task files; get/set one file's priority")
Rec("downloads", "task-blacklist", "downloads/{task_id}/blacklist", "L",
    cols=["host", "expire", "reason"], name_field="host")
Rec("downloads", "log", "downloads/{task_id}/log/", "L", note="task log lines")
Rec("downloads", "pieces", "downloads/{task_id}/pieces/", "L", note="piece map")
Rec("downloads", "erase", "downloads/{task_id}/erase", "D", singleton=True, gate=True,
    note="erase a task AND its downloaded data; needs --yes")
Rec("downloads", "task-blacklist-empty", "downloads/{task_id}/blacklist/empty", "A",
    singleton=True, note="empty a task's blocklist [verb inferred]")
Rec("downloads", "blocklist", "downloads/blacklist/", "LCUD",
    cols=["host", "expire", "reason"], name_field="host",
    note="global blocklist")
Rec("downloads", "config", "downloads/config/", "RU", singleton=True)
Rec("downloads", "stats", "downloads/stats", "R", note="global rx/tx counters")
Rec("downloads", "throttling", "downloads/throttling", "A", singleton=True,
    note="schedule mode: throttling throttling=none|auto|<schedule>")
Rec("downloads", "feeds", "downloads/feeds/", "LC",
    cols=["id", "title", "url", "nb_read", "nb_unread", "auto_download"],
    name_field="title", note="RSS feeds; add: url=… [auto_download=true]")
Rec("downloads", "feed-items", "downloads/feeds/{feed_id}/items", "LGU",
    cols=["id", "title", "is_read", "is_downloaded", "pub_ts", "link"],
    units={"pub_ts": "ts"}, name_field="title",
    note="feed items; set one item is_read=true")
Rec("downloads", "feeds-fetch", "downloads/feeds/fetch", "A", singleton=True,
    note="refresh all feeds now")
