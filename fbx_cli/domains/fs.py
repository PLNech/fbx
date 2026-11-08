# docs/api/06-fs.md — the explorer. fs get / fs put are handwritten (binary).
from ..spec import Rec

Rec("fs", "ls", "fs/ls/{path}", "R", root="result.entries",
    cols=["name", "type", "size", "modification", "mimetype"],
    units={"size": "bytes", "modification": "ts"}, name_field="name",
    note="list a directory (fs/ls/<escaped path>, tree proxy)")
Rec("fs", "cp", "fs/cp/", "A", note="copy files: cp dst=… mode=overwrite|both|recent files='[…]'")
Rec("fs", "mv", "fs/mv/", "A", gate=True, note="move files (same body as cp) — needs --yes")
Rec("fs", "rm", "fs/rm/", "A", gate=True, note="delete files: rm files='[…]' — needs --yes")
Rec("fs", "extract", "fs/extract/", "A",
    note="extract archive: extract src=… dst=… password=… delete_archive=false overwrite=false")
Rec("fs", "archive", "fs/archive/", "A", note="create archive: archive dst=… files='[…]'")
Rec("fs", "repair", "fs/repair/", "A", note="par2 repair: repair src=… delete_archive=false")
Rec("fs", "mkdir", "fs/mkdir/", "A", note="mkdir parent=… dirname=…")
Rec("fs", "mkpath", "fs/mkpath/", "A", note="create a full path: mkpath path=…")
Rec("fs", "rename", "fs/rename/", "A", gate=True, note="rename src=… dst=… — needs --yes")
Rec("fs", "tasks", "fs/tasks/", "L",
    cols=["id", "state", "error", "progress", "title"],
    note="background fs tasks (fields partial in docs/api/)")
Rec("fs", "task", "fs/tasks/{task_id}", "RU", singleton=True,
    note="one fs task; set state=paused|running pauses/resumes")
Rec("fs", "share-link", "share_link/", "LCUD",
    cols=["token", "path", "expire", "fullurl"], units={"expire": "ts"},
    name_field="token", note="file share links")
Rec("fs", "backup-export", "backup/config/export", "R",
    note="download the box config backup (see also: fbx fs get)")
Rec("fs", "backup-import", "backup/config/import", "A", gate=True,
    note="import a config backup — needs --yes")
