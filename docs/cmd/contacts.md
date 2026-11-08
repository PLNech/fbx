# `fbx contacts`: command reference

13 records, 28 operations.

## `fbx contacts list`

contacts (contact/)

- docs/api: `contact/`

### `fbx contacts list list`

`GET contact/`

Response:

```json
{
  "result": [
    {
      "birthday": "syn-birthday",
      "company": "syn-company",
      "display_name": "syn-display-name",
      "first_name": "syn-first-name",
      "id": 1,
      "last_name": "syn-last-name"
    },
    {
      "birthday": "syn-birthday",
      "company": "syn-company",
      "display_name": "syn-display-name",
      "first_name": "syn-first-name",
      "id": 2,
      "last_name": "syn-last-name"
    }
  ],
  "success": true
}
```

Terminal:

```text
                                 contacts list                                  
 id  display_name      first_name      last_name      company      birthday     
 1   syn-display-name  syn-first-name  syn-last-name  syn-company  syn-birthday 
 2   syn-display-name  syn-first-name  syn-last-name  syn-company  syn-birthday 
-- 2 entries
```

### `fbx contacts list add [key=value …]`

`POST contact/`

Response:

```json
{
  "result": {
    "birthday": "syn-birthday",
    "company": "syn-company",
    "display_name": "syn-display-name",
    "first_name": "syn-first-name",
    "id": 1,
    "last_name": "syn-last-name"
  },
  "success": true
}
```

Terminal:

```text
  birthday                   syn-birthday
  company                    syn-company
  display_name               syn-display-name
  first_name                 syn-first-name
  id                         1
  last_name                  syn-last-name
```

### `fbx contacts list set <id> [key=value …]`

`PUT contact/`

Response:

```json
{
  "result": {
    "birthday": "syn-birthday",
    "company": "syn-company",
    "display_name": "syn-display-name",
    "first_name": "syn-first-name",
    "id": 1,
    "last_name": "syn-last-name"
  },
  "success": true
}
```

Terminal:

```text
  birthday                   syn-birthday
  company                    syn-company
  display_name               syn-display-name
  first_name                 syn-first-name
  id                         1
  last_name                  syn-last-name
```

### `fbx contacts list rm <id>`

`DELETE contact/`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## `fbx contacts photo`

upload a photo (multipart; prefer the escape hatch or the panel)

- docs/api: `contact/{contact_id}/update_photo/`

### `fbx contacts photo <contact_id>`

`POST contact/{contact_id}/update_photo/`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## `fbx contacts addresses`

postal addresses of one contact [field shapes thin in docs]

- docs/api: `contact/{contact_id}/addresses/`

### `fbx contacts addresses list <contact_id>`

`GET contact/{contact_id}/addresses/`

Response:

```json
{
  "result": [
    {
      "enabled": true,
      "state": "up"
    },
    {
      "enabled": true,
      "state": "up"
    }
  ],
  "success": true
}
```

Terminal:

```text
    contacts    
   addresses    
 enabled  state 
 yes      up    
 yes      up    
-- 2 entries
```

### `fbx contacts addresses add <contact_id> [key=value …]`

`POST contact/{contact_id}/addresses/`

Response:

```json
{
  "result": {
    "enabled": true,
    "state": "up"
  },
  "success": true
}
```

Terminal:

```text
  enabled                    True
  state                      up
```

### `fbx contacts addresses set <contact_id> <id> [key=value …]`

`PUT contact/{contact_id}/addresses/`

Response:

```json
{
  "result": {
    "enabled": true,
    "state": "up"
  },
  "success": true
}
```

Terminal:

```text
  enabled                    True
  state                      up
```

### `fbx contacts addresses rm <contact_id> <id>`

`DELETE contact/{contact_id}/addresses/`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## `fbx contacts emails`

emails of one contact [thin]

- docs/api: `contact/{contact_id}/emails/`

### `fbx contacts emails list <contact_id>`

`GET contact/{contact_id}/emails/`

Response:

```json
{
  "result": [
    {
      "enabled": true,
      "state": "up"
    },
    {
      "enabled": true,
      "state": "up"
    }
  ],
  "success": true
}
```

Terminal:

```text
contacts emails 
 enabled  state 
 yes      up    
 yes      up    
-- 2 entries
```

### `fbx contacts emails add <contact_id> [key=value …]`

`POST contact/{contact_id}/emails/`

Response:

```json
{
  "result": {
    "enabled": true,
    "state": "up"
  },
  "success": true
}
```

Terminal:

```text
  enabled                    True
  state                      up
```

### `fbx contacts emails set <contact_id> <id> [key=value …]`

`PUT contact/{contact_id}/emails/`

Response:

```json
{
  "result": {
    "enabled": true,
    "state": "up"
  },
  "success": true
}
```

Terminal:

```text
  enabled                    True
  state                      up
```

### `fbx contacts emails rm <contact_id> <id>`

`DELETE contact/{contact_id}/emails/`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## `fbx contacts numbers`

phone numbers of one contact [thin]

- docs/api: `contact/{contact_id}/numbers/`

### `fbx contacts numbers list <contact_id>`

`GET contact/{contact_id}/numbers/`

Response:

```json
{
  "result": [
    {
      "enabled": true,
      "state": "up"
    },
    {
      "enabled": true,
      "state": "up"
    }
  ],
  "success": true
}
```

Terminal:

```text
contacts numbers
 enabled  state 
 yes      up    
 yes      up    
-- 2 entries
```

### `fbx contacts numbers add <contact_id> [key=value …]`

`POST contact/{contact_id}/numbers/`

Response:

```json
{
  "result": {
    "enabled": true,
    "state": "up"
  },
  "success": true
}
```

Terminal:

```text
  enabled                    True
  state                      up
```

### `fbx contacts numbers set <contact_id> <id> [key=value …]`

`PUT contact/{contact_id}/numbers/`

Response:

```json
{
  "result": {
    "enabled": true,
    "state": "up"
  },
  "success": true
}
```

Terminal:

```text
  enabled                    True
  state                      up
```

### `fbx contacts numbers rm <contact_id> <id>`

`DELETE contact/{contact_id}/numbers/`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## `fbx contacts urls`

web urls of one contact [thin]

- docs/api: `contact/{contact_id}/urls/`

### `fbx contacts urls list <contact_id>`

`GET contact/{contact_id}/urls/`

Response:

```json
{
  "result": [
    {
      "enabled": true,
      "state": "up"
    },
    {
      "enabled": true,
      "state": "up"
    }
  ],
  "success": true
}
```

Terminal:

```text
 contacts urls  
 enabled  state 
 yes      up    
 yes      up    
-- 2 entries
```

### `fbx contacts urls add <contact_id> [key=value …]`

`POST contact/{contact_id}/urls/`

Response:

```json
{
  "result": {
    "enabled": true,
    "state": "up"
  },
  "success": true
}
```

Terminal:

```text
  enabled                    True
  state                      up
```

### `fbx contacts urls set <contact_id> <id> [key=value …]`

`PUT contact/{contact_id}/urls/`

Response:

```json
{
  "result": {
    "enabled": true,
    "state": "up"
  },
  "success": true
}
```

Terminal:

```text
  enabled                    True
  state                      up
```

### `fbx contacts urls rm <contact_id> <id>`

`DELETE contact/{contact_id}/urls/`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## `fbx contacts groups`

- docs/api: `contact/groups`

### `fbx contacts groups`

`GET contact/groups`

Response:

```json
{
  "result": {
    "id": 1,
    "name": "device-a",
    "nb_contact": "syn-nb-contact"
  },
  "success": true
}
```

Terminal:

```text
  id                         1
  name                       device-a
  nb_contact                 syn-nb-contact
```

## `fbx contacts addtogroup`

addtogroup contact=<id> group=<id>

- docs/api: `contact/addtogroup`

### `fbx contacts addtogroup`

`POST contact/addtogroup`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## `fbx contacts removefromgroup`

removefromgroup contact=<id> group=<id>

- docs/api: `contact/removefromgroup`

### `fbx contacts removefromgroup`

`POST contact/removefromgroup`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## `fbx contacts count`

number of contacts

- docs/api: `contact/count`

### `fbx contacts count`

`GET contact/count`

Response:

```json
{
  "result": {
    "enabled": true,
    "state": "up"
  },
  "success": true
}
```

Terminal:

```text
  enabled                    True
  state                      up
```

## `fbx contacts export`

vCard export (binary)

- docs/api: `contact/export/`

### `fbx contacts export`

`GET contact/export/`

Response:

```json
{
  "result": {
    "enabled": true,
    "state": "up"
  },
  "success": true
}
```

Terminal:

```text
  enabled                    True
  state                      up
```

## `fbx contacts import-step1`

upload a vCard file (multipart)

- docs/api: `contact/import/step1/`

### `fbx contacts import-step1`

`POST contact/import/step1/`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## `fbx contacts import-step2`

commit parsed contacts: import-step2 emptyBeforeAdding=false contacts='[…]'

- docs/api: `contact/import/step2/`

### `fbx contacts import-step2`

`POST contact/import/step2/`

Response:

```json
{
  "result": null,
  "success": true
}
```

Terminal:

```text
(empty result)
```

## When it fails

Examples on `fbx contacts list` list; the error
envelope is exactly what the box answers; the CLI prints
`<domain> <record> <op> failed: <msg>` and exits non-zero.

**invalid session**

```text
contacts list list failed: Invalid session
```

The session cookie expired. `fbx` re-authenticates once automatically (fresh challenge + login) before surfacing this; if it persists, run `fbx login`.

**box unreachable**

```text
contacts list list failed: unreachable: [Errno 65] no route to host
```

The box did not answer. Check the address (`FREEBOX_HOST`, default `fd0f:ee:b0::1`) and that you are on the box's LAN.

**validation error**

```text
contacts list list failed: unknown or invalid field
```

A body field the box does not accept. Field names come straight from docs/api/; `fbx api` is the escape hatch for anything undocumented.

