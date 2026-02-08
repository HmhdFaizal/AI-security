from core.os_detect import get_os
from core.state import load_state, save_state
from collector.process_monitor import get_process_data
from collector.network_monitor import get_network_activity
from ai_engine.baseline import load_baseline
from ai_engine.anomaly_model import train_model
from ai_engine.threat_score import calculate_risk
from core.report import generate_report
from core.pdf_report import generate_pdf

import os
import sys


def app_path(*paths):
    base = getattr(sys, "_MEIPASS", os.getcwd())
    return os.path.join(base, *paths)


def run_learn(callback):
    os_name = get_os()
    data_dir = app_path("data")
    os.makedirs(data_dir, exist_ok=True)

    baseline_file = os.path.join(data_dir, f"behavior_log_{os_name}.txt")

    callback(" Learning system behavior...\n")

    with open(baseline_file, "a") as f:
        for p in get_process_data():
            f.write(f"{p['name']},{p['cpu']},{p['mem']}\n")

    callback(" Learning complete\n")


def run_detect(callback):
    os_name = get_os()
    data_dir = app_path("data")

    baseline_file = os.path.join(data_dir, f"behavior_log_{os_name}.txt")

    baseline = load_baseline(baseline_file)
    if not baseline:
        callback(" No baseline found. Run learning mode first.\n")
        return

    model = train_model(baseline)

    proc_state = load_state(os.path.join(data_dir, "anomaly_state.json"))
    net_state = load_state(os.path.join(data_dir, "network_state.json"))

    callback("Scanning processes...\n")

    process_hits = {}
    for p in get_process_data():
        if model.predict([[p["cpu"], p["mem"]]])[0] == -1:
            process_hits[p["name"]] = process_hits.get(p["name"], 0) + 1

    callback(" Scanning network...\n")

    network_hits = {}
    for n in get_network_activity():
        network_hits[n["process"]] = network_hits.get(n["process"], 0) + 1

    callback("\nThreat Summary\n")

    results = {"details": []}

    for proc in set(process_hits) | set(network_hits):
        risk = calculate_risk(
            process_hits.get(proc, 0),
            network_hits.get(proc, 0)
        )

        level = "HIGH" if risk >= 70 else "MEDIUM" if risk >= 40 else "LOW"
        callback(f"{proc:25} | Risk: {risk} | {level}\n")

        results["details"].append({
            "process": proc,
            "risk": risk,
            "level": level
        })

    report = generate_report(results)
    pdf = generate_pdf(results["details"])

    callback(f"\n Report saved: {report}\n")
    callback(f" PDF saved: {pdf}\n")

    save_state(os.path.join(data_dir, "anomaly_state.json"), proc_state)
    save_state(os.path.join(data_dir, "network_state.json"), net_state)

    callback("\nScan completed\n")
