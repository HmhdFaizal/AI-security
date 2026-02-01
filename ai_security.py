import psutil
import time

print("\nAI Security Tool – Learning Mode\n")
print("Recording normal behavior...\n")

log_file = "behavior_log.txt"

with open(log_file, "a") as log:
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            name = process.info['name']
            cpu = process.cpu_percent(interval=0.1)
            mem = process.info['memory_percent']

            log.write(f"{name},{cpu},{mem}\n")

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

print("Behavior recorded successfully ✅")
print("This will be used as NORMAL baseline.")

input("\nPress Enter to exit...")

