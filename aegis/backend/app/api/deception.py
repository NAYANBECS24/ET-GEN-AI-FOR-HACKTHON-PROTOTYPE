from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.deception_gen import DeceptionGenerator

router = APIRouter(prefix="/deception", tags=["deception"])


class DeceptionDeployRequest(BaseModel):
    deployment_type: str
    target_environment: str
    specification: dict = {}


@router.post("/deploy")
def deploy_deception(payload: DeceptionDeployRequest, db: Session = Depends(get_db)):
    generator = DeceptionGenerator(db)
    decoy_spec = generator.generate_decoy(payload.deployment_type, payload.specification)
    deployment = generator.deploy_decoy(decoy_spec, payload.target_environment)
    return {
        "deployment_id": deployment.id,
        "status": deployment.status,
        "container_id": deployment.container_id,
        "decoy_spec": decoy_spec,
    }
