import psutil
import platform
import os
import json
import sys
from sklearn.ensemble import IsolationForest

# -------------------------
# Config
# -------------------------
os_name = platform.system().lower()
baseline_file = f"behavior_log_{os_name}.txt"
proc_state_file = "anomaly_state.json"
net_state_file = "network_state.json"

mode = "detect"
if len(sys.argv) > 1:
    mode = sys.argv[1]

print(f"\nAI Security Tool ({mode.upper()} MODE) – {os_name.upper()}\n")

# -------------------------
# LEARNING MODE
# -------------------------
if mode == "learn":
    print("Recording normal behavior...\n")

    with open(baseline_file, "a") as log:
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                name = proc.info['name']
                cpu = proc.cpu_percent(interval=0.1)
                mem = proc.info['memory_percent']
                log.write(f"{name},{cpu},{mem}\n")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    print("Baseline data recorded successfully")
    print(f"Saved to: {baseline_file}")
    sys.exit()

# -------------------------
# DETECTION MODE
# -------------------------
if not os.path.exists(baseline_file):
    print("No baseline data found.")
    print("Run: python ai_security.py learn")
    sys.exit()

# Load baseline
cpu_data, mem_data = [], []
with open(baseline_file, "r") as f:
    for line in f:
        try:
            _, cpu, mem = line.strip().split(",")
            cpu_data.append(float(cpu))
            mem_data.append(float(mem))
        except:
            pass

if len(cpu_data) < 10:
    print("Not enough baseline data. Run learning mode more times.")
    sys.exit()

X_train = list(zip(cpu_data, mem_data))

# Train AI model
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X_train)

print("AI model trained on baseline\n")

# Load states
proc_state = {}
net_state = {}

if os.path.exists(proc_state_file):
    proc_state = json.load(open(proc_state_file))

if os.path.exists(net_state_file):
    net_state = json.load(open(net_state_file))

# -------------------------
# Process Scan
# -------------------------
print("🔍 Scanning process behavior...\n")

for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
    try:
        name = proc.info['name'] or "unknown"
        cpu = proc.cpu_percent(interval=0.1)
        mem = proc.info['memory_percent']

        if model.predict([[cpu, mem]])[0] == -1:
            proc_state[name] = proc_state.get(name, 0) + 1
            if proc_state[name] >= 3:
                print(f"[PROCESS] {name} | repeated anomaly")

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

# -------------------------
# Network Scan
# -------------------------
print("\nScanning network behavior...\n")

for conn in psutil.net_connections(kind='inet'):
    try:
        if conn.raddr and conn.pid:
            pname = psutil.Process(conn.pid).name()
            key = f"{pname}:{conn.raddr.ip}"
            net_state[key] = net_state.get(key, 0) + 1

            if net_state[key] >= 5:
                print(f"[NETWORK] {pname} → {conn.raddr.ip}")

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

# Save state
json.dump(proc_state, open(proc_state_file, "w"), indent=2)
json.dump(net_state, open(net_state_file, "w"), indent=2)

input("\nPress Enter to exit...")

