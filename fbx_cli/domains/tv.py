# docs/api/08-tv-pvr.md
from ..spec import Rec

Rec("tv", "status", "tv/status/", "R", note="TV enablement/status")
Rec("tv", "channels", "tv/channels/", "L",
    cols=["number", "name", "id", "available"], name_field="name")
Rec("tv", "bouquets", "tv/bouquets/", "L",
    cols=["id", "name", "channel_count", "state"], name_field="name")
Rec("tv", "bouquet-channels", "tv/bouquets/{bouquet_id}/channels/", "L",
    cols=["number", "id", "available", "pub_service"], name_field="id",
    defaults={"bouquet_id": "freeboxtv"},
    note="channels of one bouquet (default: freeboxtv)")
Rec("tv", "epg-by-time", "tv/epg/by_time/{time}/", "R", note="programs by time bucket")
Rec("tv", "epg-by-channel", "tv/epg/by_channel/{channel}/{time}/", "R",
    note="programs for one channel at a timestamp")
Rec("tv", "epg-program", "tv/epg/programs/{program_id}/", "R", note="one program")
Rec("tv", "epg-highlights", "tv/epg/highlights/", "R", note="featured programs")
Rec("tv", "pvr-config", "pvr/config", "RU", singleton=True)
Rec("tv", "pvr-programmed", "pvr/programmed/", "LCUD",
    cols=["id", "name", "state", "start", "end", "channel_uuid", "conflict", "enabled"],
    units={"start": "ts", "end": "ts"}, name_field="name",
    note="scheduled recordings")
Rec("tv", "pvr-finished", "pvr/finished/", "L",
    cols=["id", "name", "state", "channel_name", "start", "end", "byte_size"],
    units={"start": "ts", "end": "ts", "byte_size": "bytes"}, name_field="name",
    note="finished recordings")
Rec("tv", "pvr-generator", "pvr/generator/", "L",
    cols=["id", "type", "name", "media", "path"], name_field="name",
    note="recurring recording rules")
Rec("tv", "pvr-media", "pvr/media/", "R", note="recording storage space")
Rec("tv", "dvb", "dvb/", "LC", cols=["id", "type", "name", "last_successful_scan"],
    units={"last_successful_scan": "ts"}, name_field="name",
    note="TNT/DVB frontends")
Rec("tv", "dvb-frontend", "dvb/{frontend_id}/", "RU", singleton=True)
Rec("tv", "dvb-scan", "dvb/{frontend_id}/scan_start", "A", singleton=True,
    note="launch a channel scan on one frontend")
Rec("tv", "dvb-services", "dvb/{frontend_id}/services/", "L",
    cols=["lcn", "name", "scrambled"], name_field="name")
