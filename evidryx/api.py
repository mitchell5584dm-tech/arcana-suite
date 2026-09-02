"""FastAPI surface for local EVIDRYX deployments."""

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .service import EvidenceService

DATA_DIR = Path(os.getenv("EVIDRYX_DATA_DIR", "./data")).resolve()
roots = [item for item in os.getenv("EVIDRYX_EVIDENCE_ROOTS", str(Path.cwd())).split(os.pathsep) if item]
service = EvidenceService(DATA_DIR / "evidryx.db", roots)
app = FastAPI(title="EVIDRYX by Arcana Forensics", version="0.1.0")


class CaseInput(BaseModel):
    case_id: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=4000)


class EvidenceInput(BaseModel):
    case_id: str
    source_path: str
    platform: str
    examiner: str = Field(min_length=1, max_length=200)
    acquisition_method: str = Field(min_length=1, max_length=200)


def _raise_api_error(error: Exception) -> None:
    status = 404 if isinstance(error, LookupError) else 403 if isinstance(error, PermissionError) else 409 if "UNIQUE" in str(error) else 400
    raise HTTPException(status_code=status, detail=str(error)) from error


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "product": "EVIDRYX", "vendor": "Arcana Forensics", "offline_first": True}


@app.post("/api/v1/cases", status_code=201)
def create_case(payload: CaseInput) -> dict:
    try:
        return service.create_case(**payload.model_dump())
    except Exception as error:
        _raise_api_error(error)


@app.post("/api/v1/evidence", status_code=201)
def register_evidence(payload: EvidenceInput) -> dict:
    try:
        return service.register_evidence(**payload.model_dump()).to_dict()
    except Exception as error:
        _raise_api_error(error)


@app.post("/api/v1/evidence/{evidence_id}/verify")
def verify_evidence(evidence_id: str) -> dict:
    try:
        return service.verify_evidence(evidence_id)
    except Exception as error:
        _raise_api_error(error)


@app.get("/api/v1/audit/integrity")
def audit_integrity() -> dict:
    return {"valid": service.verify_audit_chain(), "events": len(service.audit_log())}
