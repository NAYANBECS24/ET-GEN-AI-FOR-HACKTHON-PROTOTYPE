from __future__ import annotations

import random


def generate_fake_logs(count: int = 10) -> list[str]:
    actions = ["LOGIN_SUCCESS", "LOGIN_FAILURE", "PASSWORD_RESET", "EXPORT_REPORT"]
    return [f"2026-03-27T00:00:{i:02d}Z user=svc_finance action={random.choice(actions)}" for i in range(count)]
