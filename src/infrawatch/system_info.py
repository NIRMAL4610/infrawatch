import socket
import platform
import time
import psutil

def get_hostname():
    return socket.gethostname()

def get_os():
    os_info = platform.freedesktop_os_release()
    return os_info["NAME"]

def get_kernel():
    return platform.release()

def get_uptime():
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    uptime_days = uptime_seconds / (24 * 60 * 60)
    return int(uptime_days)

def get_system_info():
    return {
        "hostname": get_hostname(),
        "os": get_os(),
        "kernel": get_kernel(),
        "uptime": get_uptime()
    }
