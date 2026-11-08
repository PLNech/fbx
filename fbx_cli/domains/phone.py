# docs/api/09-phone-calls.md + 10-contacts.md
from ..spec import Rec

Rec("phone", "hardware", "phone/", "L",
    cols=["id", "type", "vendor", "on_hook", "is_ringing", "gain_rx", "gain_tx"],
    name_field="type", note="phone hardware (FXS/DECT)")
Rec("phone", "config", "phone/config/", "RU", singleton=True, note="gains etc.")
Rec("phone", "sip", "phone/sip", "RU", singleton=True, note="SIP toggle (phone/sip)")
Rec("phone", "dect-vendors", "phone/dect_vendors/", "L", cols=["id", "name"],
    name_field="name")
Rec("phone", "dect-page-start", "phone/dect_page_start/", "A", singleton=True,
    note="ring the DECT handsets")
Rec("phone", "dect-page-stop", "phone/dect_page_stop/", "A", singleton=True)
Rec("phone", "fxs-ring-start", "phone/fxs_ring_start/", "A", singleton=True,
    note="ring the FXS line")
Rec("phone", "fxs-ring-stop", "phone/fxs_ring_stop/", "A", singleton=True)
Rec("phone", "calls", "call/log/", "L", custom="calls",
    cols=["datetime", "type", "number", "name", "duration", "new"],
    units={"datetime": "ts", "duration": "dur"},
    alias="calls", name_field="number", note="call log (call/log/)")

Rec("contacts", "list", "contact/", "LCUD",
    cols=["id", "display_name", "first_name", "last_name", "company", "birthday"],
    name_field="display_name", note="contacts (contact/)")
Rec("contacts", "photo", "contact/{contact_id}/update_photo/", "A", singleton=True,
    note="upload a photo (multipart — prefer the escape hatch or the panel)")
Rec("contacts", "addresses", "contact/{contact_id}/addresses/", "LCUD",
    note="postal addresses of one contact [field shapes thin in docs]")
Rec("contacts", "emails", "contact/{contact_id}/emails/", "LCUD",
    note="emails of one contact [thin]")
Rec("contacts", "numbers", "contact/{contact_id}/numbers/", "LCUD",
    note="phone numbers of one contact [thin]")
Rec("contacts", "urls", "contact/{contact_id}/urls/", "LCUD",
    note="web urls of one contact [thin]")
Rec("contacts", "groups", "contact/groups", "R",
    cols=["id", "name", "nb_contact"], name_field="name")
Rec("contacts", "addtogroup", "contact/addtogroup", "A", singleton=True,
    note="addtogroup contact=<id> group=<id>")
Rec("contacts", "removefromgroup", "contact/removefromgroup", "A", singleton=True,
    note="removefromgroup contact=<id> group=<id>")
Rec("contacts", "count", "contact/count", "R", note="number of contacts")
Rec("contacts", "export", "contact/export/", "R", note="vCard export (binary)")
Rec("contacts", "import-step1", "contact/import/step1/", "A", form=True,
    note="upload a vCard file (multipart)")
Rec("contacts", "import-step2", "contact/import/step2/", "A", singleton=True,
    note="commit parsed contacts: import-step2 emptyBeforeAdding=false contacts='[…]'")
