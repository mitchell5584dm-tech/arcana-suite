# backend/tests/test_opsec.py

from engine.pain_point_resolver import PainPointResolver

def test_block_dangerous_commands():
    resolver = PainPointResolver()

    dangerous = "rm -rf /"
    result = resolver.validate_command(dangerous)

    assert result["status"] == "blocked"
    assert "unsafe" in result["reason"].lower()

