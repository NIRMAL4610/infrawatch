import psutil

from .config import load_config

def get_disk_info(path):
    disk = psutil.disk_usage(path)

    config = load_config()
    warning = config["thresholds"]["warning"]
    critical = config["thresholds"]["critical"] 

    if disk.percent < warning:
        status = "OK"
    elif disk.percent <= critical:
        status = "WARNING"
    else:
        status = "CRITICAL"

    return {
            "path": path,
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percentage": disk.percent,
            "status": status
        }
