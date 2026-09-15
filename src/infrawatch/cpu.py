import psutil

def get_cpu_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_cores = psutil.cpu_count()
    load_average = psutil.getloadavg()[0]

    return cpu_usage, cpu_cores, load_average
