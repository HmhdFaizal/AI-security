import os

def load_baseline(file):
    cpu, mem = [], []
    if not os.path.exists(file):
        return None

    with open(file, "r") as f:
        for line in f:
            try:
                _, c, m = line.strip().split(",")
                cpu.append(float(c))
                mem.append(float(m))
            except:
                pass

    if len(cpu) < 10:
        return None

    return list(zip(cpu, mem))

