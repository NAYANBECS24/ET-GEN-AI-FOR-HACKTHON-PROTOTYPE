from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="organization")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="analyst")
    is_active = Column(Boolean, default=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization", back_populates="users")


class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True)
    ecosystem = Column(String(20), default="pypi")
    name = Column(String(255), unique=True, index=True, nullable=False)
    version = Column(String(50), nullable=True)
    description = Column(Text, default="")
    download_count = Column(Integer, default=0)
    security_score = Column(Float, default=0.5)
    metadata_json = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)


class DeceptionDeployment(Base):
    __tablename__ = "deception_deployments"

    id = Column(Integer, primary_key=True)
    deployment_type = Column(String(50), nullable=False)
    target_environment = Column(String(255), nullable=False)
    status = Column(String(30), default="created")
    container_id = Column(String(128), nullable=True)
    spec = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)


class ThreatEvent(Base):
    __tablename__ = "threat_events"

    id = Column(Integer, primary_key=True)
    event_type = Column(String(50), nullable=False)
    source = Column(String(50), default="unknown")
    severity = Column(String(20), default="medium")
    payload = Column(JSON, default={})
    correlation_id = Column(String(100), index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
