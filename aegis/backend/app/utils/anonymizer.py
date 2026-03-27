from __future__ import annotations

import re


EMAIL_RE = re.compile(r"[\w.-]+@[\w.-]+")
IP_RE = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")


def anonymize_text(text: str) -> str:
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    text = IP_RE.sub("[REDACTED_IP]", text)
    return text
