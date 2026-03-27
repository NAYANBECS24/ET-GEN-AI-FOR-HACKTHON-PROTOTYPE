from __future__ import annotations

from typing import Any


class ThreatCorrelationEngine:
    MITRE_HINTS = {
        "ssh_bruteforce": "T1110 - Brute Force",
        "credential_access": "T1555 - Credentials from Password Stores",
        "suspicious_package": "T1195 - Supply Chain Compromise",
    }

    def correlate(self, dev_events: list[dict[str, Any]], runtime_events: list[dict[str, Any]]) -> dict[str, Any]:
        score = 0.0
        attack_path: list[str] = []
        mitigations: list[str] = []
        techniques: list[str] = []

        suspicious_packages = {e.get("package") for e in dev_events if e.get("hallucination")}
        if suspicious_packages:
            score += 0.5
            attack_path.append("Developer imported suspicious package")
            mitigations.append("Block package in policy engine")
            techniques.append(self.MITRE_HINTS["suspicious_package"])

        brute_force_seen = any(e.get("event_type") == "ssh_bruteforce" for e in runtime_events)
        if brute_force_seen:
            score += 0.3
            attack_path.append("Attacker performed SSH brute force on decoy")
            mitigations.append("Rotate credentials and enable MFA")
            techniques.append(self.MITRE_HINTS["ssh_bruteforce"])

        credential_harvest = any(e.get("event_type") == "credential_access" for e in runtime_events)
        if credential_harvest:
            score += 0.2
            attack_path.append("Attacker attempted credential access")
            mitigations.append("Isolate host and invalidate secrets")
            techniques.append(self.MITRE_HINTS["credential_access"])

        confidence = "low"
        if score >= 0.8:
            confidence = "high"
        elif score >= 0.5:
            confidence = "medium"

        return {
            "correlation_score": round(min(score, 1.0), 2),
            "confidence": confidence,
            "predicted_attack_path": attack_path,
            "mitigations": mitigations,
            "mitre_techniques": sorted(set(techniques)),
        }
