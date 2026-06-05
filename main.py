import time
import threading
import tkinter as tk
from main.core import execute_action

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
            
            # Main execution loop
            while is_running:
                current_action = action_var.get()
                current_interval_str = interval_var.get()
                
                minutes = int(current_interval_str.split()[0])
                wait_seconds = minutes * 60
                
                execute_action(current_action, "Normal")
                
                print(f"Executed: {current_action}. Waiting {minutes} minutes...")
                
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
        action_menu.config(state="disabled") # Lock configurations
        interval_menu.config(state="disabled")
        print(f"Enabled! Getting ready to {action_var.get()} in 5 seconds...")
        
        root.iconify()
    else:
        status_label.config(text="Status: DISABLED", fg="red")
        toggle_btn.config(text="Start Anti-AFK", bg="#ccffcc")
        action_menu.config(state="normal")
        interval_menu.config(state="normal")
        print("Disabled.")

# Start the background loop in a separate thread so the GUI doesn't freeze
thread = threading.Thread(target=afk_loop, daemon=True)
thread.start()

# GUI Setup
root = tk.Tk()
root.title("Smart Anti-AFK")
root.geometry("250x220")
root.attributes('-topmost', True) 
root.resizable(False, False)

status_label = tk.Label(root, text="Status: DISABLED", fg="red", font=("Helvetica", 12, "bold"))
status_label.pack(pady=5)

# Action Dropdown
action_label = tk.Label(root, text="Action to Perform:", font=("Helvetica", 9))
action_label.pack()
action_var = tk.StringVar(value=ACTIONS[0]) 
action_menu = tk.OptionMenu(root, action_var, *ACTIONS)
action_menu.config(font=("Helvetica", 10))
action_menu.pack(pady=3)

# Interval Dropdown
interval_label = tk.Label(root, text="Trigger Interval:", font=("Helvetica", 9))
interval_label.pack()
interval_var = tk.StringVar(value=INTERVALS[1]) # Defaults to index 1 ("10 Minutes")
interval_menu = tk.OptionMenu(root, interval_var, *INTERVALS)
interval_menu.config(font=("Helvetica", 10))
interval_menu.pack(pady=3)

# Toggle Control Button
toggle_btn = tk.Button(root, text="Start Anti-AFK", font=("Helvetica", 11, "bold"), bg="#ccffcc", command=toggle_script)
toggle_btn.pack(pady=10)

root.mainloop()