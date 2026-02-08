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

process_hits = {}

for p in get_process_data():
    if model.predict([[p['cpu'], p['mem']]])[0] == -1:
        name = p['name']
        process_hits[name] = process_hits.get(name, 0) + 1
        proc_state[name] = proc_state.get(name, 0) + 1
print("\nNetwork scan")

network_hits = {}

for n in get_network_activity():
    key = f"{n['process']}:{n['ip']}"
    network_hits[n['process']] = network_hits.get(n['process'], 0) + 1
    net_state[key] = net_state.get(key, 0) + 1


print("\nThreat Risk Summary\n")

for process in set(list(process_hits.keys()) + list(network_hits.keys())):
    risk = calculate_risk(
        process_hits.get(process, 0),
        network_hits.get(process, 0)
    )

    if risk >= 70:
        level = "HIGH"
    elif risk >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    print(f"{process:25} | Risk: {risk:3} | {level}")

results = {
    "processes": len(process_hits),
    "high": 0,
    "medium": 0,
    "low": 0,
    "details": []
}

for process in set(list(process_hits.keys()) + list(network_hits.keys())):
    risk = calculate_risk(
        process_hits.get(process, 0),
        network_hits.get(process, 0)
    )

    if risk >= 70:
        results["high"] += 1
    elif risk >= 40:
        results["medium"] += 1
    else:
        results["low"] += 1

    results["details"].append({
        "process": process,
        "risk": risk
    })

report_file = generate_report(results)
print(f"\nReport saved to: {report_file}")
pdf = generate_pdf(results["details"])
print(f"PDF report saved to: {pdf}")


save_state("data/anomaly_state.json", proc_state)
save_state("data/network_state.json", net_state)

input("\nPress Enter to exit...")

