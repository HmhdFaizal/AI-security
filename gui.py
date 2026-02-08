import tkinter as tk
import sys
import subprocess
import threading

def run_learn():
    output.delete(1.0, tk.END)
    output.insert(tk.END, "Running learning mode...\n\n")

    def task():
        process = subprocess.Popen(
            [sys.executable, "main.py", "learn"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in process.stdout:
            output.insert(tk.END, line)
            output.see(tk.END)

        output.insert(tk.END, "\nLearning completed\n")

    threading.Thread(target=task).start()

def run_scan():
    output.delete(1.0, tk.END)
    output.insert(tk.END, "Running security scan...\n\n")

    def task():
        process = subprocess.Popen(
            [sys.executable, "main.py", "detect"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Read standard output
        for line in process.stdout:
            if "HIGH" in line:
                output.insert(tk.END, line, "HIGH")
            elif "MEDIUM" in line:
                output.insert(tk.END, line, "MEDIUM")
            elif "LOW" in line:
                output.insert(tk.END, line, "LOW")
            else:
                output.insert(tk.END, line)

            output.see(tk.END)

        # Read errors (if any)
        for err in process.stderr:
            output.insert(tk.END, err)
            output.see(tk.END)

        output.insert(tk.END, "\nScan finished\n")

    threading.Thread(target=task, daemon=True).start()

# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("AI Security Monitor")
root.geometry("750x520")

title = tk.Label(root, text="AI Security Monitor", font=("Arial", 16, "bold"))
title.pack(pady=10)

scan_btn = tk.Button(root, text="Run Security Scan", command=run_scan)
scan_btn.pack(pady=10)

learn_btn = tk.Button(root, text="Run Learning Mode", command=run_learn)
learn_btn.pack(pady=5)


output = tk.Text(root, wrap="word")
output.pack(expand=True, fill="both", padx=10, pady=10)

# Risk color tags
output.tag_config("LOW", foreground="green")
output.tag_config("MEDIUM", foreground="orange")
output.tag_config("HIGH", foreground="red")

root.mainloop()

