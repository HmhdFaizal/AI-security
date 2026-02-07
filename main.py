from core.os_detect import get_os
from core.state import load_state, save_state
from collector.process_monitor import get_process_data
from collector.network_monitor import get_network_activity
from ai_engine.baseline import load_baseline
from ai_engine.anomaly_model import train_model
import sys
import os

os_name = get_os()
baseline_file = f"data/behavior_log_{os_name}.txt"

mode = "detect"
if len(sys.argv) > 1:
    mode = sys.argv[1]

print(f"\nAI Security Tool – {mode.upper()} MODE ({os_name.upper()})\n")

if mode == "learn":
    os.makedirs("data", exist_ok=True)
    with open(baseline_file, "a") as f:
        for p in get_process_data():
            f.write(f"{p['name']},{p['cpu']},{p['mem']}\n")
    print(" Learning complete")
    exit()

baseline = load_baseline(baseline_file)
if not baseline:
    print("No baseline found. Run learning mode.")
    exit()

model = train_model(baseline)

proc_state = load_state("data/anomaly_state.json")
net_state = load_state("data/network_state.json")

print("Process scan")
for p in get_process_data():
    if model.predict([[p['cpu'], p['mem']]])[0] == -1:
        proc_state[p['name']] = proc_state.get(p['name'], 0) + 1
        if proc_state[p['name']] >= 3:
            print(f"[PROCESS] {p['name']}")

print("\n Network scan")
for n in get_network_activity():
    key = f"{n['process']}:{n['ip']}"
    net_state[key] = net_state.get(key, 0) + 1
    if net_state[key] >= 5:
        print(f"[NETWORK] {key}")

save_state("data/anomaly_state.json", proc_state)
save_state("data/network_state.json", net_state)

input("\nPress Enter to exit...")

