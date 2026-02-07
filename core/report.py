import json
from datetime import datetime

def generate_report(results):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"reports/report_{timestamp}.json"

    report = {
        "timestamp": timestamp,
        "summary": {
            "processes_scanned": results["processes"],
            "high_risk": results["high"],
            "medium_risk": results["medium"],
            "low_risk": results["low"]
        },
        "details": results["details"]
    }

    with open(filename, "w") as f:
        json.dump(report, f, indent=2)

    return filename
