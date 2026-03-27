from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.deception import router as deception_router
from app.api.package_verify import router as package_router
from app.api.threat_correlate import router as correlate_router
from app.api.response import router as response_router
from app.api.websocket import router as websocket_router
from app.core.config import get_settings
from app.core.database import Base, engine
from app.core.security import get_current_user

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(package_router, prefix=settings.api_prefix)
app.include_router(deception_router, prefix=settings.api_prefix)
app.include_router(correlate_router, prefix=settings.api_prefix)
app.include_router(response_router, prefix=settings.api_prefix)
app.include_router(websocket_router)


@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "aegis-backend"}


@app.get("/whoami")
def whoami(user=Depends(get_current_user)):
    return user
