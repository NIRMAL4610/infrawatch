from .config import load_config
import subprocess


def check_service(service):
    result = subprocess.run(
        ["systemctl", "is-active", "--quiet", service]
    )

    if result.returncode == 0:
        return "RUNNING"
    else:
        return "NOT RUNNING"

def monitor_services(services):
    results = {}

    for service in services:
        results[service] = check_service(service)

    return results

def get_configured_services():
    config = load_config()
    return config["services"]
