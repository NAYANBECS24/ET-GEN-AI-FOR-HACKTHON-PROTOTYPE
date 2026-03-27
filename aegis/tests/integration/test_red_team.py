from app.services.correlation import ThreatCorrelationEngine


def test_red_team_path_not_empty_for_multi_signal_attack():
    engine = ThreatCorrelationEngine()
    result = engine.correlate(
        [{"package": "malpkg", "hallucination": True}],
        [{"event_type": "ssh_bruteforce"}],
    )
    assert len(result["predicted_attack_path"]) >= 1
