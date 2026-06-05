import time
import sys
import subprocess
import shutil

try:
    from evdev import UInput, ecodes as e
    ui = UInput()
except Exception as err:
    print("Linux Setup Error: Failed to open uinput.")
    print("Did you run: sudo chmod 666 /dev/uinput ?")
    ui = None

def get_key_map():
    if not ui:
        return {}
    return {
        "Jump (Spacebar)": e.KEY_SPACE,
        "Walk Forward (W)": e.KEY_W,
        "Walk Backward (S)": e.KEY_S
    }

def get_delay(base_time, profile):
    """ Scales delays based on selected system performance profile. """
    multipliers = {
        "Fast (Gaming PC)": 0.7,
        "Normal": 1.0,
        "Slower (Budget PC)": 1.6
    }
    return base_time * multipliers.get(profile, 1.0)

def tap_key(key, hold_time=0.1):
    if not ui: return
    ui.write(e.EV_KEY, key, 1) # Key down
    ui.syn()
    time.sleep(hold_time)
    ui.write(e.EV_KEY, key, 0) # Key up
    ui.syn()

def get_active_window_id():
    """ Returns the active window ID using xdotool if available. """
    if shutil.which("xdotool"):
        try:
            # Capture the current active window ID
            window_id = subprocess.check_output(["xdotool", "getactivewindow"], stderr=subprocess.DEVNULL).decode().strip()
            if window_id.isdigit():
                return window_id
        except Exception:
            pass
    return None

def minimize_window_id(window_id):
    """ Minimizes a window by its ID using xdotool (keeps it running but hides it). """
    if window_id and shutil.which("xdotool"):
        try:
            subprocess.call(["xdotool", "windowminimize", window_id], stderr=subprocess.DEVNULL)
            return True
        except Exception:
            pass
    return False

def focus_window_id(window_id):
    """ Activates a window by its ID using xdotool. """
    if window_id and shutil.which("xdotool"):
        try:
            subprocess.call(["xdotool", "windowactivate", window_id], stderr=subprocess.DEVNULL)
            return True
        except Exception:
            pass
    return False

def act(action_name, speed_profile="Normal"):
    if not ui:
        print("Cannot act: uinput not initialized.")
        return
        
    key_map = get_key_map()
    
    prev_window_id = get_active_window_id()
    if prev_window_id:
        print(f"[Linux] Captured active background window ID: {prev_window_id}")
    else:
        print("[Linux] xdotool not detected or inactive. Will use fallback Alt+Esc to restore focus.")
        print("[Linux] Tip: Run 'sudo apt install xdotool' to enable smart background window restoration!")

    # 1. Open GNOME Activities Overview
    tap_key(e.KEY_LEFTMETA, 0.1)
    time.sleep(get_delay(0.8, speed_profile))
    
    # 2. Type "sober"
    for key in [e.KEY_S, e.KEY_O, e.KEY_B, e.KEY_E, e.KEY_R]:
        tap_key(key, 0.05)
    time.sleep(get_delay(0.6, speed_profile))
    
    # 3. Press Enter to select the Sober window
    tap_key(e.KEY_ENTER, 0.1)
    time.sleep(get_delay(1.2, speed_profile))
    
    # Capture the Sober game window ID now that it is fully focused and active
    sober_window_id = get_active_window_id()
    
    # 4. Perform Action inside Sober
    target_key = key_map.get(action_name, e.KEY_SPACE)
    hold_time = 0.5 if target_key in [e.KEY_W, e.KEY_S] else 0.2
    tap_key(target_key, hold_time)
    time.sleep(get_delay(0.5, speed_profile))
    
    # 5. Smart Minimize / Focus Restoration
    if sober_window_id and sober_window_id != prev_window_id:
        print(f"[Linux] Minimizing game window (ID: {sober_window_id}) to return to work...")
        if minimize_window_id(sober_window_id):
            time.sleep(get_delay(0.6, speed_profile))
            return

    if prev_window_id:
        print(f"[Linux] Fallback: Directly restoring focus to window ID: {prev_window_id}")
        if focus_window_id(prev_window_id):
            time.sleep(get_delay(0.6, speed_profile))
            return

    print("[Linux] Performing fallback Alt+Esc direct window cycle...")
    ui.write(e.EV_KEY, e.KEY_LEFTALT, 1)
    ui.syn()
    time.sleep(get_delay(0.15, speed_profile))
    
    ui.write(e.EV_KEY, e.KEY_ESC, 1)
    ui.syn()
    time.sleep(get_delay(0.15, speed_profile))
    
    ui.write(e.EV_KEY, e.KEY_ESC, 0)
    ui.syn()
    time.sleep(get_delay(0.15, speed_profile))
    
    ui.write(e.EV_KEY, e.KEY_LEFTALT, 0)
    ui.syn()
    
    for modifier in [e.KEY_LEFTALT, e.KEY_TAB, e.KEY_ESC, e.KEY_LEFTMETA]:
        ui.write(e.EV_KEY, modifier, 0)
    ui.syn()
    
    time.sleep(get_delay(0.6, speed_profile))