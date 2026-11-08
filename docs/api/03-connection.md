# Domain: connection / rrd / domain (DDNS + box domains)

## `connection`
- Verb: GET (bare, no trailing slash). Used by the connection status widget.
- `result` used for rx/tx rates and state `[inferred from widget bindings]`.

## `connection/full/`
- Verb: GET (3 call sites). Response `result` fields consumed in the bundle:
  `ipv4`, `ipv6` (used to prefill DDNS A/AAAA record fields),
  `rate_down`, `rate_up`, `bw_down`, `bw_up`, `state`, `type`, `mode`,
  `media`, `wan_ip` `[inferred: beyond ipv4/ipv6 these match the
  ConnHistoryModel shape below]`.

## `connection/aggregation` and `connection/lte/aggregation`
- Verb: GET. Bonding / 4G aggregation status `[thin: only the URL + GET are
  visible]`.

## `connection/lte/backup`
- Status/config of the LTE backup `[thin: only the URL is visible]`.

## `connection/xdsl/`
- Verb: GET. xDSL line stats `[thin]`.

## `connection/config/`
- Form panel (3 call sites): ping/mtu etc `[inferred from i18n keys
  settings.connection*]`. Verbs GET/PUT.

## `connection/ipv6/config/`
- IPv6 config form `[thin]`.

## `connection/ddns/all/` and `connection/ddns/all/status/`
- Verbs: GET (list of DDNS providers + their status); PUT/POST per-provider
  config `[inferred from the ddns settings form]`.

## `connection/logs/`
- rest proxy + explicit `DELETE` (clear logs).
- `result` entries = `ConnHistoryModel`: `id:int`, `type:string`,
  `state:string`, `conn:string`, `link:string`, `bw_down:int`, `bw_up:int`,
  `date:int`, `connection:string`.

## `rrd/`
- Verb: POST. Body: `jsonData:{db:<string>, precision:<int>,
  date_start:<int>, date_end:<int>, fields:<string[]>}`.
- Used by the graphs screen (`me.db`, `me.precision`, `loadStart`, `me.end`,
  `fieldsNames`).
- `result` = time series per requested field `[inferred]`.

## `domain/` — DNS domains / remote-access domain
- `domain/owned/` — rest proxy + POST (add a domain, body
  `jsonData:{id:<domain_name>}`); `result` entries =
  `Fbx.os.app.settings.domains.DomainModel`: `id:string`, `type:string`,
  `owner:string`, `certs:auto`, `default:bool`, `defaultStr:bool`.
- `domain/config/` — GET + PUT (rest proxy on same model; PUT body
  `jsonData:{default_domain:<domain_name>}`).
- `domain/availability/` — GET, checks a domain name's availability.
- `domain/reserve/` — POST, body `jsonData:{prefix:<string>,
  domain:<string>}`.
- The default remote URL is built from `domainsCfg.default_domain` else
  `domainsCfg.api_domain` + optional `:https_port`/`:port` (accounts screen).
