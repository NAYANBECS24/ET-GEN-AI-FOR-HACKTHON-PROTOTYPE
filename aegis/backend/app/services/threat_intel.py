from __future__ import annotations

from datetime import datetime


class ThreatIntelFeed:
    def __init__(self):
        self.events: list[dict] = []

    def ingest(self, event: dict) -> dict:
        normalized = {
            "event_type": event.get("type", "unknown"),
            "severity": event.get("severity", "medium"),
            "source": event.get("source", "ghostguard"),
            "payload": event,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.events.append(normalized)
        return {"status": "ingested", "event": normalized, "count": len(self.events)}
