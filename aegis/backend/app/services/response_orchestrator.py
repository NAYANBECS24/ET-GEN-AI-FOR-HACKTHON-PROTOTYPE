from __future__ import annotations

from app.services.deception_gen import DeceptionGenerator
from app.services.threat_intel import ThreatIntelFeed


class AutonomousResponseCoordinator:
    def __init__(self, deception_generator: DeceptionGenerator, intel_feed: ThreatIntelFeed):
        self.deception_generator = deception_generator
        self.intel_feed = intel_feed

    def handle_alert(self, alert: dict) -> dict:
        response = {"actions": [], "approval_required": False}
        if alert.get("type") == "package_hallucination":
            response["actions"].append("block_import")
            if alert.get("alternative"):
                response["actions"].append("suggest_alternative")

        if alert.get("severity") in {"high", "critical"}:
            decoy = self.deception_generator.generate_decoy(
                alert.get("target_service", "ssh"),
                {"strategy": alert.get("strategy", "credential-lure")},
            )
            response["actions"].append("deploy_decoy")
            response["decoy"] = decoy

        if alert.get("impact") == "production":
            response["approval_required"] = True

        response["intel"] = self.intel_feed.ingest(alert)
        return response
