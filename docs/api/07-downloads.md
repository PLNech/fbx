# Domain: downloads (downloader app)

## `downloads/`
- rest proxy (task list) + explicit DELETE (5 call sites).
- Task model fields (from grid bindings) `[partial]`: `id`, `name`, `status`,
  `size`, `uploaded`, `rx`/`rx_speed`, `tx`/`tx_speed`, `progress`,
  `eta` (client-computed from speed), `type` `[inferred from columns]`.

## `downloads/add`
- Verb: POST. Body (form params): `download_url:<string>` — either a plain
  URL or `"file://"+base64_decode(path)` for a local file from the explorer
  (4 call sites). Optional `username`, `password`, `archive_password`
  `[inferred from the add-dialog fields]`.

## Per-task sub-resources (Ext `restforeign`, `{foreignId}` = task id)
- `downloads/<id>/trackers` — GET/POST/PUT/DELETE.
  `result` = `BtTrackerModel`: `task_id:int`, `announce:string`,
  `is_backup:bool`, `status:string`, `interval:int`, `min_interval:int`,
  `reannounce_in:int`, `nseeders:int`, `nleechers:int`, `is_enabled:bool`.
- `downloads/<id>/peers` — GET. `result` = `BtPeerModel`: `host:string`,
  `state:string`, `origin:string`, `protocol:string`, `client:string`,
  `country_code:string`, `port:int`, `tx:float`, `rx:float`,
  `tx_rate:float`, `rx_rate:float`, `progress:int`, `score:int`.
- `downloads/<id>/files` — GET + PUT (priority change).
  `result` = `TaskFileModel`: `id:string`, `task_id:int`, `name:string`,
  `filepath:string`, `status:string`, `priority:string`, `error:string`,
  `rx:int`, `size:int`, `preview_url:string`, `progress:float`,
  `running:bool`, `todownload:bool`.
- `downloads/<id>/blacklist` — GET (rest proxy).
  `result` = `BtBlacklistModel`: `id:string`, `task_id:string`,
  `host:string`, `expire:int`, `global:bool`, `reason:string`.
- `downloads/<id>/log/` — GET (log lines) `[thin]`.
- `downloads/<id>/pieces/` — GET (piece map for the pieces view) `[thin]`.
- `downloads/<id>/erase` — DELETE (erase task data).
- `downloads/<id>/blacklist/empty` — POST/DELETE (empty a task's blocklist)
  `[inferred from name; exact verb not captured]`.

## `downloads/blacklist/`
- Global blocklist (rest proxy) — same `BtBlacklistModel` shape `[inferred]`.

## `downloads/config/`
- Download settings form GET/PUT `[thin]`.

## `downloads/stats`
- Verb: GET. Global rx/tx counters `[thin]`.

## `downloads/throttling`
- Verb: PUT. Body: `jsonData:{throttling:<mode>}` — schedule mode string
  `[inferred: modes like "none"/"auto"/schedule names]`.

## RSS feeds
- `downloads/feeds/` — rest proxy + POST (add feed).
  `result` = `RssFeedModel`: `id:int`, `status:string`, `url:string`,
  `title:string`, `desc:string`, `image_url:string`, `nb_read:int`,
  `nb_unread:int`, `auto_download:bool`, `fetch_ts:date`, `pub_ts:date`,
  `error:string`, `pretty_name:string`.
- `downloads/feeds/<id>/items` — rest proxy GET/PUT (mark read).
  `result` = `RssFeedItemModel`: `id:int`, `feed_id:int`, `title:string`,
  `desc:string`, `author:string`, `link:string`, `is_read:bool`,
  `is_downloaded:bool`, `fetch_ts:date`, `pub_ts:date`,
  `pretty_name:string`, `enclosure_url:string`, `enclosure_type:string`,
  `enclosure_length:int`.
- `downloads/feeds/fetch` — POST (refresh feeds now).
