from src.infrawatch.system_info import get_system_info


def test_get_system_info():
    info = get_system_info()

    assert "hostname" in info
    assert "os" in info
    assert "kernel" in info
    assert "uptime" in info
