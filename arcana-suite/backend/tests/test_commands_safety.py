# backend/tests/test_commands_safety.py

from engine.pain_point_resolver import PainPointResolver

def test_command_autocorrect():
    resolver = PainPointResolver()

    raw = "instal arcana"
    result = resolver.validate_command(raw)

    assert result["status"] == "ok"
    assert result["normalized"] == "install arcana"

def test_safe_command_passes():
    resolver = PainPointResolver()

    raw = "update system"
    result = resolver.validate_command(raw)

    assert result["status"] == "ok"

