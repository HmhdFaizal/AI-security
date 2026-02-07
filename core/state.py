import json
import os

def load_state(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

def save_state(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

