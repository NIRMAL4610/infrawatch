import time

from .cpu import get_cpu_info
from .memory import get_memory_info
from .disk import get_disk_info
from .health import get_status, get_overall_status
from .database import save_metrics
from .config import load_config
from .alerts import handle_alert

def collect_and_save(disk_path):
    cpu_usage, _, _ = get_cpu_info()
    _, _, _, memory_percentage = get_memory_info()
    root_disk = get_disk_info(disk_path)

    cpu_status = get_status(cpu_usage)
    memory_status = get_status(memory_percentage)
    disk_status = root_disk["status"]

    overall_status = get_overall_status([
        cpu_status,
        memory_status,
        disk_status
    ])

    if overall_status == "CRITICAL":
        handle_alert(
            overall_status,
            f"InfraWatch CRITICAL: CPU={cpu_usage}%, "
            f"Memory={memory_percentage}%, "
            f"Disk={root_disk['percentage']}%"
        )
    else:
        handle_alert(overall_status, "")

    save_metrics(
        cpu_usage,
        memory_percentage,
        root_disk["percentage"],
        overall_status
    )

if __name__ == "__main__":
    config = load_config()
    interval = config["monitoring"]["interval"]
    disk_path = config["monitoring"]["disk_paths"][0]

    while True:
        collect_and_save(disk_path)
        time.sleep(300)
