# Domain: login / sessions / authorization / app tokens

All paths relative to `FbxConf.apiBaseUrl`. Call-site provenance = the
minified class/function that issues the request.

## `login/` — session state
- Verb: GET. Used by `Ext.application.launch` (panel bootstrap) and the whole
  login page.
- Response `result` (login page): `logged_in:bool`, `challenge:object`
  ( concatenated into a string by `getchallenge()` via `eval` of its parts),
  `password_salt:string`.
- Panel launch reads `res.` further fields `[not visible in captured slice —
  thin]`.

## `login/` — password auth
- Verb: POST. Body (form-encoded): `password:<hex HmacSHA1>`. See overview.
- Failure HTTP 403 with JSON body `{success:false, result:{challenge:…}}`.

## `login/logout`
- Verb: POST. No body observed. Call sites: settings "logout" button (2 sites).

## `login/perms/`
- Verb: GET. Loaded once by `Fbx.os.app.accounts.AuthorizationModel
  .loadPermissions`, cached in `AuthorizationModel.permissionsName`.
- Response: permission name list `[inferred: consumed as a boolean set of
  permission names]`.

## `login/quality/`
- Verb: POST. Body: `params:{password:<plaintext password>}` — sent by the
  settings password field to score password quality. Failure = weak password
  `[inferred]`.

## `sessions/` — active sessions
- Proxy: `Fbx.os.app.accounts.SessionsModel` (rest proxy, full collection).
- `result` entries (model fields): `id:int`, `app_name:string`,
  `device_name:string`, `client_ip:string`, `start_time:int`,
  `is_web_app:bool`.

## `authorization/` — app tokens / pairings
- Proxy: `Fbx.os.app.accounts.AuthorizationModel` (rest). CRUD implied:
  GET list, PUT `<id>` update, DELETE `<id>` revoke `[inferred from proxy]`.
- `result` entries: `id:int`, `app_name:string`, `app_version:string`,
  `app_id:string`, `device_name:string`, `last_session:int`,
  `req_ip:string`, `req_date:int`, `token_validity:string`,
  `permissions:object`, `permissions_str:string`.
