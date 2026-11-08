# Domain: phone / calls

## `phone/`
- rest proxy (phone hardware list). `result` =
  `Fbx.os.app.settings.PhoneModel`: `id:int`, `type_id:int`, `type:string`,
  `gain_rx:int`, `gain_tx:int`, `default_gain_rx:int`,
  `default_gain_tx:int`, `on_hook:bool`, `vendor:string`,
  `hardware_defect:bool`, `is_ringing:bool`.

## `phone/config/`
- GET (3+ call sites; form reload timer every 1 s) + PUT (save gains etc).

## `phone/sip`
- GET + POST (no trailing slash). POST body seen:
  `jsonData:{enabled:<bool>}` (SIP (ALG?) toggle) `[thin: only `enabled`
  visible]`.

## `phone/dect_vendors/`
- rest proxy GET. `result` = `DectVendorModel`: `id:string`, `name:string`.

## DECT handset paging
- `phone/dect_page_start/` — POST (ring DECT handsets).
- `phone/dect_page_stop/` — POST (stop paging).

## FXS line ring
- `phone/fxs_ring_start/` — POST.
- `phone/fxs_ring_stop/` — POST.

## `call/log/`
- rest proxy. `result` entries = `Fbx.os.app.calls.CallModel`: `id:int`,
  `duration:int`, `datetime:date`, `line_id:int`, `contact_id:int`,
  `number:string`, `type:string` (call type: incoming/outgoing/missed
  `[inferred from outgoing flag + type column]`), `name:string`,
  `new:bool`, `outgoing:bool`, `niceCallDate:string` (client-computed).
- The calls screen also links entries to contacts via `contact_id`.
