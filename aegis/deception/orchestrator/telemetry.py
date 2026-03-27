from __future__ import annotations

from datetime import datetime


class TelemetryCollector:
    def __init__(self):
        self.events: list[dict] = []

    def capture(self, event_type: str, payload: dict) -> dict:
        item = {"event_type": event_type, "payload": payload, "timestamp": datetime.utcnow().isoformat()}
        self.events.append(item)
        return item
