from __future__ import annotations

import re
from typing import Optional

import redis
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.services.package_graph import PackageKnowledgeGraph

settings = get_settings()


class CodeIntentAnalyzer:
    PY_IMPORT_RE = re.compile(r"(?:import|from)\s+([a-zA-Z0-9_\-\.]+)")
    JS_IMPORT_RE = re.compile(r"(?:import\s+.*?from\s+|require\()\s*['\"]([@a-zA-Z0-9_\-/\.]+)")

    def __init__(self, db: Session):
        self.db = db
        self.pkg_graph = PackageKnowledgeGraph(db)
        try:
            self.cache = redis.from_url(settings.redis_url, decode_responses=True)
            self.cache.ping()
        except Exception:
            self.cache = None

    def extract_imports(self, code: str) -> list[str]:
        py = [m.lower().split(".")[0] for m in self.PY_IMPORT_RE.findall(code or "")]
        js = [m.lower().split("/")[0] for m in self.JS_IMPORT_RE.findall(code or "")]
        return sorted(set(py + js))

    def predict_intent(self, code: str, context: Optional[dict] = None) -> str:
        blob = (code or "").lower()
        if any(k in blob for k in ["encrypt", "hash", "jwt", "token"]):
            return "crypto"
        if any(k in blob for k in ["http", "request", "fetch", "axios", "socket"]):
            return "networking"
        if any(k in blob for k in ["sql", "database", "orm", "query", "postgres", "redis"]):
            return "database"
        if any(k in blob for k in ["auth", "login", "password", "oauth"]):
            return "identity"
        return (context or {}).get("intent", "general")

    def is_hallucination(self, package: str, intent: str) -> bool:
        key = f"hallucination:{package}:{intent}"
        if self.cache:
            cached = self.cache.get(key)
            if cached is not None:
                return cached == "1"

        risk = self.pkg_graph.assess_risk(package)
        is_bad = (not risk.exists) and risk.typosquat_risk >= 0.6
        if self.cache:
            self.cache.setex(key, 300, "1" if is_bad else "0")
        return is_bad

    def find_alternative(self, package: str, intent: str) -> Optional[str]:
        options = self.pkg_graph.similar_packages(package, intent)
        return options[0] if options else None

    def analyze_import(self, package_name: str, code: str, context: Optional[dict] = None) -> dict:
        intent = self.predict_intent(code, context)
        registry = (context or {}).get("ecosystem", "pypi")
        self.pkg_graph.upsert_from_registry(registry, package_name)
        risk = self.pkg_graph.assess_risk(package_name)
        hallucination = self.is_hallucination(package_name, intent)
        return {
            "package": package_name,
            "intent": intent,
            "hallucination": hallucination,
            "reputation": risk.reputation,
            "risk_reason": risk.reason,
            "typosquat_risk": risk.typosquat_risk,
            "alternative": self.find_alternative(package_name, intent) if hallucination else None,
            "imports": self.extract_imports(code),
        }
