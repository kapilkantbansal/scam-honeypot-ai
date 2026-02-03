

import re

# UPI ID pattern (example: ram@ybl, abc.ok@oksbi)
UPI_REGEX = re.compile(r"[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}")

# Bank account numbers (9 to 18 digits)
ACCOUNT_REGEX = re.compile(r"\b\d{9,18}\b")

# IFSC code (example: SBIN0001234)
IFSC_REGEX = re.compile(r"\b[A-Z]{4}0[A-Z0-9]{6}\b")

# Indian phone numbers (+91XXXXXXXXXX or 10 digits)
PHONE_REGEX = re.compile(r"(?:\+91[\s-]?)?[6-9]\d{9}")


# URLs / phishing links
URL_REGEX = re.compile(r"https?:\/\/\S+")

# Bare domains (no http)
DOMAIN_REGEX = re.compile(r"\b[a-zA-Z0-9\-]+\.(in|com|net|org|co)(\/\S*)?\b")
MASKED_ACCOUNT_REGEX = re.compile(r"[Xx]{2,}\d{4,}")
IFSC_REGEX = re.compile(r"\b[A-Z]{4}0[A-Z0-9]{6}\b", re.IGNORECASE)
