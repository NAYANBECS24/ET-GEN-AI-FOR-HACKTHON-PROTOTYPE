from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.code_intent import CodeIntentAnalyzer

router = APIRouter(prefix="/package", tags=["package"])


class PackageVerifyRequest(BaseModel):
    package_name: str = Field(..., examples=["requests"])
    context_code: str = ""
    development_context: dict = {}


@router.post("/verify")
def verify_package(payload: PackageVerifyRequest, db: Session = Depends(get_db)):
    analyzer = CodeIntentAnalyzer(db)
    return analyzer.analyze_import(payload.package_name, payload.context_code, payload.development_context)
