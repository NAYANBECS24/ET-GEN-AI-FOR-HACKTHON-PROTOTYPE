from fastapi import APIRouter
from pydantic import BaseModel

from app.services.correlation import ThreatCorrelationEngine

router = APIRouter(prefix="/threat", tags=["threat"])


class ThreatCorrelateRequest(BaseModel):
    development_events: list[dict]
    runtime_events: list[dict]


@router.post("/correlate")
def correlate_threats(payload: ThreatCorrelateRequest):
    engine = ThreatCorrelationEngine()
    return engine.correlate(payload.development_events, payload.runtime_events)
