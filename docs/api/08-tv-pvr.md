# Domain: tv / epg / pvr / dvb

## `tv/status/`
- Verb: GET. TV enablement/status `[thin]`.

## `tv/channels/`
- rest proxy (channel list) `[thin]`.

## `tv/bouquets/`
- rest proxy. `result` = `Fbx.os.app.tv.BouquetModel`: `id:string`,
  `name:string`, `channel_count:int`, `state:string`.

## `tv/bouquets/freeboxtv/channels/`
- rest proxy (2 call sites). `result` = `Fbx.os.app.tv.BouquetChannelModel`:
  `id:string`, `uuid:string`, `number:int`, `sub_number:int`,
  `available:bool`, `pub_service:bool`, `streams:auto`.

## EPG
- `tv/epg/by_time/<time>/`: GET; programs by time bucket.
- `tv/epg/by_channel/<channel>/<time>/`: GET; channel + timestamp both
  URL-encoded.
- `tv/epg/programs/<id>/`: GET one program (`encodeURIComponent(prog.id)`).
- `tv/epg/highlights/`: GET (featured programs).
- Program fields consumed by the epg app `[inferred from viewer widgets]`:
  `id`, `title`, `subtitle`, `category`, `start`, `end`, `channel`,
  `summary`, `picture_url` … `[inferred]`.

## PVR
- `pvr/config` and `pvr/config/`: GET (config singleton);
  `[inferred]` PUT to save.
- `pvr/programmed/`: rest proxy + POST (schedule recording).
  `result` = `Fbx.os.app.pvr.PrecordModel`: `id:int`, `state:string`,
  `name:string`, `media:string`, `path:string`, `subname:string`,
  `has_record_gen:bool`, `record_gen_id:int`, `overlap_list:auto`,
  `start:int`, `end:int`, `broadcast_type:string`,
  `channel_quality:string`, `channel_uuid:string`, `channel_type:string`,
  `conflict:bool`, `error:string`, `enabled:bool`, `margin_after:int`,
  `margin_before:int`, `channel:auto`.
- `pvr/finished/`: rest proxy. `result` = `FrecordModel`: `id:int`,
  `byte_size:int`, `secure:bool`, `state:string`, `name:string`,
  `subname:string`, `channel_name:string`, `start:int`, `end:int`,
  `broadcast_type:string`, `channel_quality:string`,
  `channel_uuid:string`, `channel_type:string`, `error:string`,
  `enabled:bool`.
- `pvr/generator/`: rest proxy (recurring rules). `result` =
  `RecordGenModel`: `id:int`, `type:string`, `name:string`, `media:string`,
  `path:string`, `params:auto`.
- `pvr/media/`: rest proxy. `result` = `RecordMediaModel`: `media:string`,
  `free_bytes:string`, `total_bytes:string`, `record_time:auto`,
  `available_rec_time:-` (computed client-side).

## DVB (TNT tuner)
- `dvb/`: rest proxy + POST (2 call sites). `result` entries =
  `Fbx.os.app.settings.DvbFrontendModel`: `id:int`, `type:string`,
  `name:string`, `last_successful_scan:int`, `scan:object`.
- `dvb/<id>/`: GET/PUT single frontend.
- `dvb/<id>/scan_start`: POST (launch a channel scan).
- `dvb/<id>/services/`: rest proxy. `result` =
  `Fbx.os.app.settings.DvbServicesModel`: `lcn:int`, `name:string`,
  `scrambled:bool`.
