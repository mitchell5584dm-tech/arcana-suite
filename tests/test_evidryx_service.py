import hashlib

import pytest

from evidryx.service import EvidenceService


@pytest.fixture()
def service(tmp_path):
    return EvidenceService(tmp_path / "state" / "evidryx.db", [tmp_path])


def test_registers_and_verifies_cross_platform_evidence(service, tmp_path):
    source = tmp_path / "memory.raw"
    source.write_bytes(b"defensive forensic image")
    service.create_case("IR-2026-001", "Endpoint incident")

    for platform in ("windows", "linux", "android"):
        record = service.register_evidence(
            case_id="IR-2026-001", source_path=source, platform=platform,
            examiner="Analyst", acquisition_method="validated logical acquisition",
        )
        assert record.platform == platform
        assert record.sha256 == hashlib.sha256(source.read_bytes()).hexdigest()
        assert service.verify_evidence(record.evidence_id)["verified"] is True

    assert service.verify_audit_chain() is True


def test_detects_changed_evidence(service, tmp_path):
    source = tmp_path / "device.img"
    source.write_bytes(b"original")
    service.create_case("CASE-2", "Integrity test")
    record = service.register_evidence(case_id="CASE-2", source_path=source,
        platform="android", examiner="A", acquisition_method="ADB backup")
    source.write_bytes(b"changed")
    assert service.verify_evidence(record.evidence_id)["verified"] is False


def test_rejects_sources_outside_allowed_roots(tmp_path):
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    outside = tmp_path / "outside.bin"
    outside.write_bytes(b"no")
    service = EvidenceService(tmp_path / "db.sqlite", [allowed])
    service.create_case("CASE-3", "Boundary test")
    with pytest.raises(PermissionError):
        service.register_evidence(case_id="CASE-3", source_path=outside,
            platform="linux", examiner="A", acquisition_method="copy")


def test_validates_case_and_platform(service, tmp_path):
    source = tmp_path / "file"
    source.write_bytes(b"x")
    with pytest.raises(ValueError):
        service.create_case("../escape", "bad")
    service.create_case("CASE-4", "Platform test")
    with pytest.raises(ValueError, match="windows, linux, or android"):
        service.register_evidence(case_id="CASE-4", source_path=source,
            platform="ios", examiner="A", acquisition_method="copy")
