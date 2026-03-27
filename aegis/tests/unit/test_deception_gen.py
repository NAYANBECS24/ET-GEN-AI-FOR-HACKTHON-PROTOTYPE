from app.services.deception_gen import DeceptionGenerator


class DummyDB:
    def add(self, _):
        pass

    def commit(self):
        pass

    def refresh(self, item):
        item.id = 1


def test_generate_decoy_contains_specification():
    gen = DeceptionGenerator(DummyDB())
    decoy = gen.generate_decoy("api", {})
    assert decoy["target_service"] == "api"
    assert "specification" in decoy
