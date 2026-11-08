# Domain: airmedia (AirPlay / DLNA cast)

## `airmedia/config/`
- Form panel (`AjaxFormPanel`) GET/PUT.
- Form fields: `enabled:bool` (checkbox), `password:string` (textfield,
  disabled when airmedia off) `[transcribed from field names]`.

## `airmedia/receivers/`
- rest proxy GET (list of receivers on the network). `result` =
  `Fbx.os.lib.AirMediaReceiverModel`: `name:string`, `capabilities:raw`,
  `password_protected:bool`.

## `airmedia/receivers/<name>/`
- Verb: POST (`encodeURIComponent(target)`). Body:
  `jsonData:{action:"start"|"stop", media_type:<string>, media:<string>,
  password:<string, optional>}`.
- Call site: `Fbx.os.lib.AirMedia` (cast dialog); on 401-type failure it
  prompts for the receiver password and caches it client-side in
  `me.knownPasswords`.
- `media_type` values: `"video"` / `"photo"` `[inferred from the cast
  dialog's media kinds]`; `media` is a `dl/…`-style path or URL
  `[inferred]`.
