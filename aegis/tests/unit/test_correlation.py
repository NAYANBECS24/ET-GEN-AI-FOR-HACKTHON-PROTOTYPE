from app.services.correlation import ThreatCorrelationEngine


def test_correlation_score_increases_with_events():
    engine = ThreatCorrelationEngine()
    result = engine.correlate(
        [{"package": "foo", "hallucination": True}],
        [{"event_type": "ssh_bruteforce"}, {"event_type": "credential_access"}],
    )
    assert result["correlation_score"] == 1.0
    assert result["confidence"] == "high"
    assert len(result["mitre_techniques"]) >= 2
