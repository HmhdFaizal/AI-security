import time
import subprocess
import sys

INTERVAL = 3600  # 1 hour

while True:
    print("⏱️ Scheduled security scan running...")
    subprocess.run([sys.executable, "main.py", "detect"])
    time.sleep(INTERVAL)
