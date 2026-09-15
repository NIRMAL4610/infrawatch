import psutil

def get_memory_info():
    memory = psutil.virtual_memory()

    total = memory.total / (1024 ** 3)
    used = memory.used / (1024 ** 3)
    available = memory.available / (1024 ** 3)
    percentage = memory.percent

    return total, used, available, percentage
