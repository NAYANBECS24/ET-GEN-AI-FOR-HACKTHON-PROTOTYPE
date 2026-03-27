from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.deception_gen import DeceptionGenerator
from app.services.response_orchestrator import AutonomousResponseCoordinator
from app.services.threat_intel import ThreatIntelFeed

router = APIRouter(prefix="/response", tags=["response"])


class AlertRequest(BaseModel):
    type: str
    severity: str = "medium"
    source: str = "ghostguard"
    impact: str = "development"
    target_service: str = "ssh"
    strategy: str = "credential-lure"
    alternative: str | None = None
    payload: dict = {}


@router.post("/alert")
def process_alert(payload: AlertRequest, db: Session = Depends(get_db)):
    coordinator = AutonomousResponseCoordinator(DeceptionGenerator(db), ThreatIntelFeed())
    return coordinator.handle_alert(payload.model_dump())
