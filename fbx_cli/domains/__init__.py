# Importing the package registers every documented endpoint record.
from . import (  # noqa: F401
    system, connection, lan, wifi, fs, downloads, tv, phone, fw, vpn, storage,
)

# phone.py registers both the phone and the contacts domains.
