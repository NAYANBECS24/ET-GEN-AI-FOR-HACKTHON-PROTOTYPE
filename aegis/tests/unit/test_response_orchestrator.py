from app.services.deception_gen import DeceptionGenerator
from app.services.response_orchestrator import AutonomousResponseCoordinator
from app.services.threat_intel import ThreatIntelFeed


class DummyDB:
    def add(self, _):
        pass

    def commit(self):
        pass

    def refresh(self, item):
        item.id = 1


def test_orchestrator_requires_approval_for_production():
    coordinator = AutonomousResponseCoordinator(DeceptionGenerator(DummyDB()), ThreatIntelFeed())
    result = coordinator.handle_alert(
        {
            "type": "package_hallucination",
            "severity": "critical",
            "impact": "production",
            "alternative": "requests",
        }
    )
    assert result["approval_required"] is True
    assert "deploy_decoy" in result["actions"]
