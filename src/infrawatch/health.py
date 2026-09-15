from .services import monitor_services
from .config import load_config


def get_status(percentage):
    config = load_config()

    warning = config["thresholds"]["warning"]
    critical = config["thresholds"]["critical"]

    if percentage < warning:
        return "OK"
    elif percentage <= critical:
        return "WARNING"
    else:
        return "CRITICAL"

def get_overall_status(statuses):
    if "CRITICAL" in statuses:
        return "CRITICAL"
    elif "WARNING" in statuses:
        return "WARNING"
    else:
        return "HEALTHY"

def get_current_health():
    from .cpu import get_cpu_info
    from .memory import get_memory_info
    from .disk import get_disk_info
    from .services import monitor_services

    cpu_usage, _, _ = get_cpu_info()
    _, _, _, memory_percentage = get_memory_info()

    root_disk = get_disk_info("/")
    home_disk = get_disk_info("/home")

    services = []
    service_results = monitor_services(services)

    cpu_status = get_status(cpu_usage)
    memory_status = get_status(memory_percentage)

    service_statuses = []

    for status in service_results.values():
        if status == "RUNNING":
            service_statuses.append("OK")
        else:
            service_statuses.append("CRITICAL")

    overall_status = get_overall_status([
        cpu_status,
        memory_status,
        root_disk["status"],
        home_disk["status"],
        *service_statuses
    ])

    return overall_status
