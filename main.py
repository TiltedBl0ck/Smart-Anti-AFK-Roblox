import time
import threading
import tkinter as tk
from core import execute_action

is_running = False

ACTIONS = [
    "Jump (Spacebar)",
    "Walk Forward (W)",
    "Walk Backward (S)"
]

INTERVALS = [
    "5 Minutes",
    "10 Minutes",
    "15 Minutes",
    "20 Minutes"
]

def afk_loop():
    global is_running
    while True:
        if is_running:
            for _ in range(5):
                if not is_running:
                    break
                time.sleep(1)

            while is_running:
                current_action = action_var.get()
                current_interval_str = interval_var.get()

                minutes = int(current_interval_str.split()[0])
                wait_seconds = minutes * 60

                execute_action(current_action, "Normal")

                log_text.config(state="normal")
                log_text.insert(tk.END, f"Executed: {current_action}. Waiting {minutes} min...\n")
                log_text.see(tk.END)
                log_text.config(state="disabled")

                for _ in range(wait_seconds):
                    if not is_running:
                        break
                    time.sleep(1)
        else:
            time.sleep(1)

def toggle_script():
    global is_running
    is_running = not is_running

    if is_running:
        status_label.config(text="Status: ENABLED", fg="green")
        toggle_btn.config(text="Stop Anti-AFK", bg="#ffcccc")
        action_menu.config(state="disabled")
        interval_menu.config(state="disabled")
        log_text.config(state="normal")
        log_text.insert(tk.END, f"Enabled! Getting ready to {action_var.get()} in 5 seconds...\n")
        log_text.see(tk.END)
        log_text.config(state="disabled")
        root.iconify()
    else:
        status_label.config(text="Status: DISABLED", fg="red")
        toggle_btn.config(text="Start Anti-AFK", bg="#ccffcc")
        action_menu.config(state="normal")
        interval_menu.config(state="normal")
        log_text.config(state="normal")
        log_text.insert(tk.END, "Disabled.\n")
        log_text.see(tk.END)
        log_text.config(state="disabled")

if __name__ == "__main__":
    # GUI Setup
    root = tk.Tk()
    root.title("Smart Anti-AFK")
    root.geometry("280x300")
    root.attributes('-topmost', True)
    root.resizable(False, False)

    status_label = tk.Label(root, text="Status: DISABLED", fg="red", font=("Helvetica", 12, "bold"))
    status_label.pack(pady=5)

    action_label = tk.Label(root, text="Action to Perform:", font=("Helvetica", 9))
    action_label.pack()
    action_var = tk.StringVar(value=ACTIONS[0])
    action_menu = tk.OptionMenu(root, action_var, *ACTIONS)
    action_menu.config(font=("Helvetica", 10))
    action_menu.pack(pady=3)

    interval_label = tk.Label(root, text="Trigger Interval:", font=("Helvetica", 9))
    interval_label.pack()
    interval_var = tk.StringVar(value=INTERVALS[1])
    interval_menu = tk.OptionMenu(root, interval_var, *INTERVALS)
    interval_menu.config(font=("Helvetica", 10))
    interval_menu.pack(pady=3)

    toggle_btn = tk.Button(root, text="Start Anti-AFK", font=("Helvetica", 11, "bold"), bg="#ccffcc", command=toggle_script)
    toggle_btn.pack(pady=10)

    log_text = tk.Text(root, height=5, width=34, state="disabled", font=("Courier", 8))
    log_text.pack(pady=3)

    # Thread starts AFTER widgets exist
    thread = threading.Thread(target=afk_loop, daemon=True)
    thread.start()

    root.mainloop()