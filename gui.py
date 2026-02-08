import tkinter as tk
import threading
from engine import run_detect, run_learn


def append(text, tag=None):
    output.after(0, lambda: (output.insert(tk.END, text, tag), output.see(tk.END)))


def set_status(text, color):
    status.after(0, lambda: status.config(text=text, fg=color))


def start_scan():
    output.delete(1.0, tk.END)
    set_status("Scanning system...", "orange")

    threading.Thread(
        target=lambda: (
            run_detect(append),
            set_status("Idle", "green")
        ),
        daemon=True
    ).start()


def start_learn():
    output.delete(1.0, tk.END)
    set_status("Learning mode...", "blue")

    threading.Thread(
        target=lambda: (
            run_learn(append),
            set_status("Idle", "green")
        ),
        daemon=True
    ).start()


# ---------- GUI ---------- #

root = tk.Tk()
root.title("AI Security Monitor")
root.geometry("780x560")
root.resizable(False, False)

tk.Label(root, text="AI Security Monitor", font=("Arial", 18, "bold")).pack(pady=10)

btns = tk.Frame(root)
btns.pack()

tk.Button(btns, text="Run Security Scan", width=18, command=start_scan).grid(row=0, column=0, padx=10)
tk.Button(btns, text="Run Learning Mode", width=18, command=start_learn).grid(row=0, column=1, padx=10)

status = tk.Label(root, text="Idle", font=("Arial", 10, "bold"))
status.pack(pady=5)

output = tk.Text(root, wrap="word", font=("Consolas", 10))
output.pack(expand=True, fill="both", padx=10, pady=10)

output.tag_config("LOW", foreground="green")
output.tag_config("MEDIUM", foreground="orange")
output.tag_config("HIGH", foreground="red")

root.mainloop()
