from core.pdf_report import generate_pdf
from core.os_detect import get_os
from core.state import load_state, save_state
from collector.process_monitor import get_process_data
from collector.network_monitor import get_network_activity
from ai_engine.baseline import load_baseline
from ai_engine.anomaly_model import train_model
from ai_engine.threat_score import calculate_risk
from core.report import generate_report

import sys
import os


# ---------------- PATH HANDLING (EXE SAFE) ---------------- #

def app_path(*paths):
    """Returns correct path for script or frozen EXE"""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, *paths)


DATA_DIR = app_path("data")
os.makedirs(DATA_DIR, exist_ok=True)


# ---------------- MODE HANDLING ---------------- #

mode = "detect"
if len(sys.argv) > 1:
    mode = sys.argv[1].lower()

os_name = get_os()
baseline_file = os.path.join(DATA_DIR, f"behavior_log_{os_name}.txt")

print(f"\nAI Security Tool – {mode.upper()} MODE ({os_name.upper()})\n")


# ---------------- LEARN MODE ---------------- #

if mode == "learn":
    with open(baseline_file, "a") as f:
        for p in get_process_data():
            f.write(f"{p['name']},{p['cpu']},{p['mem']}\n")

    print("Learning complete")
    sys.exit(0)


# ---------------- LOAD BASELINE ---------------- #

baseline = load_baseline(baseline_file)
if not baseline:
    print("No baseline found. Run learning mode first.")
    sys.exit(1)


# ---------------- TRAIN MODEL ---------------- #

model = train_model(baseline)


# ---------------- LOAD STATES ---------------- #

proc_state_file = os.path.join(DATA_DIR, "anomaly_state.json")
net_state_file = os.path.join(DATA_DIR, "network_state.json")

proc_state = load_state(proc_state_file)
net_state = load_state(net_state_file)


# ---------------- PROCESS SCAN ---------------- #

print("Process scan\n")

process_hits = {}

for p in get_process_data():
    if model.predict([[p["cpu"], p["mem"]]])[0] == -1:
        name = p["name"]
        process_hits[name] = process_hits.get(name, 0) + 1
        proc_state[name] = proc_state.get(name, 0) + 1


# ---------------- NETWORK SCAN ---------------- #

print("Network scan\n")

network_hits = {}

for n in get_network_activity():
    key = f"{n['process']}:{n['ip']}"
    network_hits[n["process"]] = network_hits.get(n["process"], 0) + 1
    net_state[key] = net_state.get(key, 0) + 1


# ---------------- RISK ANALYSIS ---------------- #

print("\nThreat Risk Summary\n")

results = {
    "processes": len(process_hits),
    "high": 0,
    "medium": 0,
    "low": 0,
    "details": []
}

all_processes = set(process_hits) | set(network_hits)

for process in all_processes:
    risk = calculate_risk(
        process_hits.get(process, 0),
        network_hits.get(process, 0)
    )

    if risk >= 70:
        level = "HIGH"
        results["high"] += 1
    elif risk >= 40:
        level = "MEDIUM"
        results["medium"] += 1
    else:
        level = "LOW"
        results["low"] += 1

    print(f"{process:25} | Risk: {risk:3} | {level}")

    results["details"].append({
        "process": process,
        "risk": risk,
        "level": level
    })


# ---------------- REPORTING ---------------- #

report_file = generate_report(results)
print(f"\nReport saved to: {report_file}")

pdf_file = generate_pdf(results["details"])
print(f"PDF report saved to: {pdf_file}")


# ---------------- SAVE STATE ---------------- #

save_state(proc_state_file, proc_state)
save_state(net_state_file, net_state)

print("\nScan completed successfully")
sys.exit(0)
