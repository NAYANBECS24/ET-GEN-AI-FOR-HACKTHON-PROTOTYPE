from __future__ import annotations

import random


class PPOAgent:
    def __init__(self):
        self.policies = ["aggressive_lure", "quiet_monitor", "credential_lure"]

    def choose_policy(self, state: dict) -> str:
        _ = state
        return random.choice(self.policies)
