from __future__ import annotations

from datetime import datetime
from random import choice
from typing import Any

from sqlalchemy.orm import Session

from app.core.models import DeceptionDeployment


class DeceptionGenerator:
    STRATEGIES = ["high-interaction", "low-interaction", "credential-lure"]

    def __init__(self, db: Session):
        self.db = db

    def generate_decoy(self, target_service: str, attack_context: dict[str, Any]) -> dict[str, Any]:
        strategy = attack_context.get("strategy") or choice(self.STRATEGIES)
        if target_service == "api":
            spec = {"image": "aegis-decoy-api", "endpoints": ["/api/payments", "/api/users"], "token": "fake-token-123"}
        elif target_service == "db":
            spec = {"image": "postgres:16", "database": "finance_shadow", "username": "readonly_audit", "password": "HoneyPass!"}
        else:
            spec = {"image": "aegis-decoy-ssh", "banner": "Ubuntu 22.04 LTS", "credentials": "ops_admin:Welcome123!"}
        return {
            "target_service": target_service,
            "strategy": strategy,
            "generated_at": datetime.utcnow().isoformat(),
            "specification": spec,
        }

    def deploy_decoy(self, decoy_spec: dict[str, Any], target_environment: str) -> DeceptionDeployment:
        deployment = DeceptionDeployment(
            deployment_type=decoy_spec.get("target_service", "unknown"),
            target_environment=target_environment,
            status="deployed",
            container_id=f"sim-{int(datetime.utcnow().timestamp())}",
            spec=decoy_spec,
        )
        self.db.add(deployment)
        self.db.commit()
        self.db.refresh(deployment)
        return deployment
