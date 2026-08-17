# backend/tests/test_install_flow.py

from engine.pain_point_resolver import PainPointResolver

def test_install_missing_fields():
    resolver = PainPointResolver()

    config = {
        "path": "/usr/local/arcana"
        # missing permissions + network_mode
    }

    result = resolver.safe_install(config)

    assert result["status"] == "error"
    assert "missing" in result["reason"].lower()

def test_install_valid():
    resolver = PainPointResolver()

    config = {
        "path": "/usr/local/arcana",
        "permissions": "user",
        "network_mode": "offline"
    }

    result = resolver.safe_install(config)

    assert result["status"] == "ok"

