import tkinter as tk
import sys
import subprocess
import threading

def run_scan():
    output.delete(1.0, tk.END)
    output.insert(tk.END, "🔍 Running security scan...\n\n")

    def task():
        process = subprocess.Popen(
            [sys.executable, "main.py", "detect"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in process.stdout:
            output.insert(tk.END, line)
            output.see(tk.END)

        for err in process.stderr:
            output.insert(tk.END, err)
            output.see(tk.END)

        output.insert(tk.END, "\n✅ Scan finished\n")

    threading.Thread(target=task).start()

root = tk.Tk()
root.title("AI Security Monitor")
root.geometry("750x520")

title = tk.Label(root, text="AI Security Monitor", font=("Arial", 16, "bold"))
title.pack(pady=10)

scan_btn = tk.Button(root, text="Run Security Scan", command=run_scan)
scan_btn.pack(pady=10)

output = tk.Text(root, wrap="word")
output.pack(expand=True, fill="both", padx=10, pady=10)

root.mainloop()

