from __future__ import annotations

from deception.orchestrator.config import DecoyConfig


class DeploymentManager:
    def deploy(self, config: DecoyConfig) -> dict:
        return {
            "status": "deployed",
            "environment": config.environment,
            "image": config.image,
            "port": config.port,
            "container_id": f"mock-{config.environment}-{config.port}",
        }
