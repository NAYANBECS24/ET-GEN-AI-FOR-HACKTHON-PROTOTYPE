from __future__ import annotations

from dataclasses import dataclass
from difflib import get_close_matches
from typing import Optional

import requests
from sqlalchemy.orm import Session

from app.core.models import Package


@dataclass
class PackageRisk:
    exists: bool
    reputation: float
    typosquat_risk: float
    reason: str


class PackageKnowledgeGraph:
    """SQLite-backed package catalog with lightweight reputation and similarity heuristics."""

    SAFE_BOOTSTRAP = {
        "requests": ("pypi", "HTTP for humans", 0.93),
        "fastapi": ("pypi", "FastAPI framework", 0.96),
        "sqlalchemy": ("pypi", "Database toolkit", 0.95),
        "numpy": ("pypi", "Numerical computing", 0.95),
        "pandas": ("pypi", "Data analysis", 0.92),
        "express": ("npm", "Node.js server framework", 0.91),
        "react": ("npm", "UI library", 0.94),
    }

    def __init__(self, db: Session):
        self.db = db
        self.bootstrap_catalog()

    def bootstrap_catalog(self) -> None:
        for name, (ecosystem, description, score) in self.SAFE_BOOTSTRAP.items():
            if self.db.query(Package).filter(Package.name == name).first():
                continue
            self.db.add(
                Package(
                    ecosystem=ecosystem,
                    name=name,
                    version="seed",
                    description=description,
                    security_score=score,
                    metadata_json={"source": "bootstrap"},
                )
            )
        self.db.commit()

    def exists(self, package_name: str) -> bool:
        return self.db.query(Package).filter(Package.name == package_name.lower()).first() is not None

    def get_reputation(self, package_name: str) -> float:
        pkg = self.db.query(Package).filter(Package.name == package_name.lower()).first()
        return pkg.security_score if pkg else 0.0

    def similar_packages(self, package_name: str, intent: str) -> list[str]:
        names = [row[0] for row in self.db.query(Package.name).all()]
        suggestions = get_close_matches(package_name, names, n=5, cutoff=0.6)
        if suggestions:
            return suggestions
        keyword_hits = self.db.query(Package.name).filter(Package.description.ilike(f"%{intent}%")).limit(5).all()
        return [row[0] for row in keyword_hits]

    def assess_risk(self, package_name: str) -> PackageRisk:
        exists = self.exists(package_name)
        reputation = self.get_reputation(package_name)
        if exists:
            return PackageRisk(True, reputation, 0.0, "Known package")

        near = self.similar_packages(package_name, "")
        if near:
            return PackageRisk(False, 0.0, 0.85, f"Potential typosquat of '{near[0]}'")
        return PackageRisk(False, 0.0, 0.6, "Unknown package not found in local graph")

    def upsert_from_registry(self, ecosystem: str, package_name: str) -> Optional[Package]:
        package_name = package_name.lower()
        pkg = self.db.query(Package).filter(Package.name == package_name).first()
        if pkg:
            return pkg

        if ecosystem == "npm":
            url = f"https://registry.npmjs.org/{package_name}"
        else:
            url = f"https://pypi.org/pypi/{package_name}/json"

        try:
            response = requests.get(url, timeout=4)
            if response.status_code != 200:
                return None
            data = response.json()
        except Exception:
            return None

        if ecosystem == "npm":
            latest = data.get("dist-tags", {}).get("latest", "unknown")
            description = data.get("description", "")
        else:
            latest = data.get("info", {}).get("version", "unknown")
            description = data.get("info", {}).get("summary", "")

        pkg = Package(
            ecosystem=ecosystem,
            name=package_name,
            version=latest,
            description=description,
            download_count=0,
            security_score=0.8,
            metadata_json={"source": "registry"},
        )
        self.db.add(pkg)
        self.db.commit()
        self.db.refresh(pkg)
        return pkg
