import psutil

def get_process_data():
    data = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            data.append({
                "name": proc.info['name'] or "unknown",
                "cpu": proc.cpu_percent(interval=0.1),
                "mem": proc.info['memory_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return data

