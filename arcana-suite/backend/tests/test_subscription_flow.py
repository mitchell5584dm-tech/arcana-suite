# backend/tests/test_subscription_flow.py

from engine.pain_point_resolver import PainPointResolver

def test_subscription_unknown_plan():
    resolver = PainPointResolver()

    result = resolver.subscription_clarity("unknown")

    assert result["status"] == "error"
    assert "unknown" in result["reason"].lower()

def test_subscription_basic_plan():
    resolver = PainPointResolver()

    result = resolver.subscription_clarity("basic")

    assert result["status"] == "ok"
    assert result["plan"] == "basic"
    assert "price" in result["details"]

