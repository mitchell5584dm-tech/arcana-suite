import asyncio

import httpx

import evidryx.api as api
from evidryx.service import EvidenceService

API_KEY = "test-only-secret"


def request(method, path, *, headers=None, **kwargs):
    async def send():
        transport = httpx.ASGITransport(app=api.app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.request(method, path, headers=headers, **kwargs)
    return asyncio.run(send())


def authenticated_headers(monkeypatch):
    monkeypatch.setenv("EVIDRYX_API_KEY", API_KEY)
    return {"X-API-Key": API_KEY}


def test_health_and_evidence_workflow(tmp_path, monkeypatch):
    monkeypatch.setattr(api, "service", EvidenceService(tmp_path / "evidryx.db", [tmp_path]))
    headers = authenticated_headers(monkeypatch)
    source = tmp_path / "event.log"
    source.write_text("authentication failure\n", encoding="utf-8")

    health = request("GET", "/health")
    assert health.status_code == 200
    assert health.json()["vendor"] == "Arcana Forensics"

    created = request("POST", "/api/v1/cases", headers=headers, json={"case_id": "IR-1", "name": "Incident"})
    assert created.status_code == 201
    evidence = request("POST", "/api/v1/evidence", headers=headers, json={
        "case_id": "IR-1", "source_path": str(source), "platform": "windows",
        "examiner": "Analyst", "acquisition_method": "exported event log",
    })
    assert evidence.status_code == 201
    evidence_id = evidence.json()["evidence_id"]
    assert request("POST", f"/api/v1/evidence/{evidence_id}/verify", headers=headers).json()["verified"] is True
    assert request("GET", "/api/v1/audit/integrity", headers=headers).json() == {"valid": True, "events": 3}


def test_api_returns_actionable_client_errors(tmp_path, monkeypatch):
    monkeypatch.setattr(api, "service", EvidenceService(tmp_path / "evidryx.db", [tmp_path]))
    headers = authenticated_headers(monkeypatch)
    response = request("POST", "/api/v1/cases", headers=headers, json={"case_id": "../bad", "name": "Bad"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Request data is invalid"}
    assert "../bad" not in response.text


def test_only_health_is_available_without_configuration(monkeypatch):
    monkeypatch.delenv("EVIDRYX_API_KEY", raising=False)
    assert request("GET", "/health").status_code == 200
    for path in ("/api/v1/audit/integrity", "/docs", "/openapi.json"):
        response = request("GET", path)
        assert response.status_code == 503
        assert response.json() == {"detail": "API access is disabled"}


def test_rejects_missing_and_incorrect_api_keys(monkeypatch):
    monkeypatch.setenv("EVIDRYX_API_KEY", API_KEY)
    assert request("GET", "/api/v1/audit/integrity").status_code == 401
    assert request("GET", "/api/v1/audit/integrity", headers={"X-API-Key": "wrong"}).status_code == 401
    assert request("GET", "/api/v1/audit/integrity", headers={"X-API-Key": API_KEY}).status_code == 200


def test_rejects_oversized_requests(monkeypatch):
    monkeypatch.setenv("EVIDRYX_API_KEY", API_KEY)
    monkeypatch.setenv("EVIDRYX_MAX_REQUEST_BYTES", "1024")
    response = request("POST", "/api/v1/cases", content=b"x" * 1025,
                       headers={"X-API-Key": API_KEY, "Content-Type": "application/json"})
    assert response.status_code == 413
    assert response.json() == {"detail": "Request body too large"}
