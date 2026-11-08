Provenance note: the command wiki under `docs/cmd/` is generated from the
endpoint records (which cite these documents) with synthetic fixtures; the
test suite renders every record/op through the real renderer offline.

## Login flow (from `login.min.js`)

1. `GET /api/latest/login/` (header `X-FBX-FREEBOX0S: 1`) →
   `result.logged_in` (bool), `result.challenge` (object of parts the page
   `eval`-concatenates into one string), `result.password_salt` (string).
   If already `logged_in`, the panel JS is loaded and the panel opens.
2. Password auth `POST /api/latest/login/` with form field
   `password = HmacSHA1(challenge, SHA1(password_salt + password)).toString()`
   (hex string). On success the server session starts (cookie `[inferred]`).
3. On failure (`success:false`, HTTP 403 handled as a JSON body): if the
   `challenge` changed since the attempt, the form is re-submitted after 2 s;
   otherwise `msg` is displayed.

Panel-side extras:

- `GET …/login/` at panel launch (same call) drives the environment.
- `POST …/login/quality/` with `params:{password:<plaintext>}`; password
  strength check from the settings password-change form `[inferred: response
  not read; only success/failure used]`.
- `GET …/login/perms/`: loads the logged-in app's permission set at startup.
- `POST …/login/logout`: ends the session (settings page "logout").

## API versioning

Only `apiBaseUrl` is used; the concrete version segment (`latest` vs `vN`)
lives in `FbxConf`, not the bundle. Trailing slashes are inconsistent
(`connection/full/` vs `wifi/state`); transcribe paths exactly as used.

## REST conventions (Ext JS proxies)

Most collections are Ext `rest`/`resttree`/`restforeign` proxies with
`sortParam/startParam/limitParam/filterParam/pageParam` all `undefined`,
so **no paging/sort/filter query params are sent**; a collection GET returns
everything. Proxy CRUD maps to:

- `GET <url>`: list (`root:"result"` or `root:"result.entries"`)
- `POST <url>`: create (record data as JSON body)
- `PUT <url><id>` (or `<url>` for singleton configs): update
- `DELETE <url><id>`: destroy

`restforeign` proxies substitute `{foreignId}` in the URL with a parent
record's key (`foreignProperty`, e.g. `profile_id`, `task_id`, `bssid`).

## Non-REST extras

- **WebSocket `…/event/`**: notification bus. Client sends
  `{"action":"register","events":["<source>_<event>", …]}`; server replies
  `{"success":true,"action":"register"}` then pushes
  `{"action":"notification","source":"…","event":"…","result":…}`. One
  shared socket in `Fbx.os.gui.Environment.registerNotif/unregisterNotif`.
- **WebSocket `…/upload`**: chunked file upload (see `06-fs.md`).
- **Multipart upload fallback**: `POST upload/` with `file`, `dirname`,
  `MAX_FILE_SIZE`, `csrf_token`, then `POST upload/<id>/send` (see `06-fs.md`).
- **Long-poll**: none found; the panel polls with `setInterval` (1 s form
  reloads, task monitors) instead.
