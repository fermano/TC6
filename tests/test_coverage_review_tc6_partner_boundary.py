from src.coverage_review_tc6_partner_boundary import resolve_partner_value

def test_internal_zero_is_preserved():
    assert resolve_partner_value({"grace_seconds": 0}) == 0

def test_absent_value_uses_default():
    assert resolve_partner_value({}) == 45
