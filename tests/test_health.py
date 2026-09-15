from src.infrawatch.health import get_status, get_overall_status


def test_get_status():
    assert get_status(50) == "OK"
    assert get_status(85) == "WARNING"
    assert get_status(95) == "CRITICAL"


def test_get_overall_status():
    assert get_overall_status(["OK", "OK"]) == "HEALTHY"
    assert get_overall_status(["OK", "WARNING"]) == "WARNING"
    assert get_overall_status(["WARNING", "CRITICAL"]) == "CRITICAL"
