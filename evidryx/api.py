"""Authenticated FastAPI surface for local EVIDRYX deployments."""

import hmac
import json
import os
import sqlite3
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .service import EvidenceService

DATA_DIR = Path(os.getenv("EVIDRYX_DATA_DIR", "./data")).resolve()
roots = [item for item in os.getenv("EVIDRYX_EVIDENCE_ROOTS", str(Path.cwd())).split(os.pathsep) if item]
service = EvidenceService(DATA_DIR / "evidryx.db", roots)
app = FastAPI(title="EVIDRYX by Arcana Forensics", version="0.1.0")


class SecurityMiddleware:
    """Fail closed, authenticate API requests, and bound request bodies."""

    def __init__(self, asgi_app: Any) -> None:
        self.app = asgi_app

    @staticmethod
    async def _response(send: Any, status: int, detail: str) -> None:
        body = json.dumps({"detail": detail}, separators=(",", ":")).encode()
        await send({"type": "http.response.start", "status": status, "headers": [
            (b"content-type", b"application/json"),
            (b"content-length", str(len(body)).encode()),
            (b"cache-control", b"no-store"),
        ]})
        await send({"type": "http.response.body", "body": body})

    async def __call__(self, scope: dict, receive: Any, send: Any) -> None:
        if scope["type"] != "http" or scope.get("path") == "/health":
            await self.app(scope, receive, send)
            return

        configured_key = os.getenv("EVIDRYX_API_KEY", "")
        if not configured_key:
            await self._response(send, 503, "API access is disabled")
            return
        headers = {key.lower(): value for key, value in scope.get("headers", [])}
        supplied_key = headers.get(b"x-api-key", b"").decode("utf-8", errors="ignore")
        if not hmac.compare_digest(supplied_key.encode(), configured_key.encode()):
            await self._response(send, 401, "Authentication required")
            return

        try:
            maximum = int(os.getenv("EVIDRYX_MAX_REQUEST_BYTES", "1048576"))
        except ValueError:
            maximum = 1048576
        maximum = min(max(maximum, 1024), 10 * 1024 * 1024)
        content_length = headers.get(b"content-length", b"0")
        if content_length.isdigit() and int(content_length) > maximum:
            await self._response(send, 413, "Request body too large")
            return

        messages: list[dict] = []
        total = 0
        while True:
            message = await receive()
            messages.append(message)
            if message["type"] == "http.disconnect":
                return
            total += len(message.get("body", b""))
            if total > maximum:
                await self._response(send, 413, "Request body too large")
                return
            if not message.get("more_body", False):
                break

        async def replay() -> dict:
            return messages.pop(0) if messages else {"type": "http.request", "body": b"", "more_body": False}

        await self.app(scope, replay, send)


app.add_middleware(SecurityMiddleware)


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
    if isinstance(error, LookupError):
        status, detail = 404, "Requested record was not found"
    elif isinstance(error, PermissionError):
        status, detail = 403, "Evidence source is not permitted"
    elif isinstance(error, sqlite3.IntegrityError):
        status, detail = 409, "Record conflicts with existing data"
    elif isinstance(error, (ValueError, FileNotFoundError)):
        status, detail = 400, "Request data is invalid"
    else:
        status, detail = 500, "Internal server error"
    raise HTTPException(status_code=status, detail=detail) from error


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
