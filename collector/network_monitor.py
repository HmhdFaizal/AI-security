import psutil

def get_network_activity():
    activity = []
    for conn in psutil.net_connections(kind='inet'):
        try:
            if conn.raddr and conn.pid:
                pname = psutil.Process(conn.pid).name()
                activity.append({
                    "process": pname,
                    "ip": conn.raddr.ip
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return activity

