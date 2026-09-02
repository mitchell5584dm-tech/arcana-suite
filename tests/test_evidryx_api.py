from fastapi.testclient import TestClient

import evidryx.api as api
from evidryx.service import EvidenceService


def test_health_and_evidence_workflow(tmp_path, monkeypatch):
    monkeypatch.setattr(api, "service", EvidenceService(tmp_path / "evidryx.db", [tmp_path]))
    client = TestClient(api.app)
    source = tmp_path / "event.log"
    source.write_text("authentication failure\n", encoding="utf-8")

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["vendor"] == "Arcana Forensics"

    created = client.post("/api/v1/cases", json={"case_id": "IR-1", "name": "Incident"})
    assert created.status_code == 201
    evidence = client.post("/api/v1/evidence", json={
        "case_id": "IR-1", "source_path": str(source), "platform": "windows",
        "examiner": "Analyst", "acquisition_method": "exported event log",
    })
    assert evidence.status_code == 201
    evidence_id = evidence.json()["evidence_id"]
    assert client.post(f"/api/v1/evidence/{evidence_id}/verify").json()["verified"] is True
    assert client.get("/api/v1/audit/integrity").json() == {"valid": True, "events": 3}


def test_api_returns_actionable_client_errors(tmp_path, monkeypatch):
    monkeypatch.setattr(api, "service", EvidenceService(tmp_path / "evidryx.db", [tmp_path]))
    client = TestClient(api.app)
    response = client.post("/api/v1/cases", json={"case_id": "../bad", "name": "Bad"})
    assert response.status_code == 400
    assert "case_id" in response.json()["detail"]
