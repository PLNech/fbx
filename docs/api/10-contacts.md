# Domain: contacts

## `contact/`
- rest proxy + record CRUD. `result` entries =
  `Fbx.os.app.contacts.ContactModel`: `id:int`, `display_name:string`,
  `first_name:string`, `last_name:string`, `company:string`,
  `photo_url:string`, `birthday:date`, `notes:string`,
  `display_name_pretty:string`, `display_name_pretty_lower:string`
  (computed client-side `[inferred]`).

## `contact/<id>/update_photo/`
- POST multipart (photo upload): composed with `record.getId()`.
  (`"/update_photo/"` literal confirmed.)

## Sub-resources (Ext `restforeign`, `{foreignId}` = contact id)
- `contact/<id>/addresses/`: postal addresses.
- `contact/<id>/emails/`: email addresses.
- `contact/<id>/numbers/`: phone numbers.
- `contact/<id>/urls/`: web URLs.
- Field shapes of each sub-record are not captured in the bundle slice
  `[thin: only the URLs and the association pattern are visible]`.

## Group operations (all POST, no rest proxy)
- `contact/groups`: list groups. `result` =
  `Fbx.os.app.contacts.ContactGroup`: `id:int`, `name:string`,
  `nb_contact:int`.
- `contact/addtogroup`: POST `{contact:<id>, group:<id>}`
  `[inferred param names from action name]`.
- `contact/removefromgroup`: POST, same shape `[inferred]`.

## Import / export
- `contact/count`: GET (number of contacts, used before import).
- `contact/export/`: GET (vCard download) `[inferred]`.
- `contact/import/step1/`: POST (upload vCard file, multipart, like the
  explorer uploader) `[inferred]`.
- `contact/import/step2/`: POST
  `jsonData:{emptyBeforeAdding:<bool>, contacts:[<parsed contacts>]}`.

## Loose strings `address/`, `email/`, `url/`, `number/`
- These bare literals appear in the bundle next to the contact app; they are
  the *singular* lookup/creation endpoints used by the import step-2 parser
  `[inferred: used standalone, not under contact/<id>/]`. Their verbs are
  not visible.
