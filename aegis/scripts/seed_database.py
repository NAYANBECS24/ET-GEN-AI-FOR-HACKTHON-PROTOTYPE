from app.core.database import SessionLocal
from app.core.models import Package

SEED = [
    ("pypi", "requests", "2.32.3", "HTTP library", 0.93),
    ("pypi", "fastapi", "0.115.12", "FastAPI framework", 0.95),
    ("pypi", "sqlalchemy", "2.0.40", "Database toolkit", 0.91),
]


def main():
    db = SessionLocal()
    for ecosystem, name, version, description, score in SEED:
        if db.query(Package).filter(Package.name == name).first():
            continue
        db.add(Package(ecosystem=ecosystem, name=name, version=version, description=description, security_score=score, metadata_json={"seed": True}))
    db.commit()
    db.close()
    print("Seed complete")


if __name__ == "__main__":
    main()
