import time

try:
    import pygetwindow as gw
    from pynput.keyboard import Controller, Key
    keyboard = Controller()
except ImportError:
    print("Windows dependencies missing!")
    print("Run: pip install pygetwindow pynput")
    gw = None
    keyboard = None

def get_delay(base_time, profile):
    """ Scales delays based on selected system performance profile. """
    multipliers = {
        "Fast (Gaming PC)": 0.7,
        "Normal": 1.0,
        "Slower (Budget PC)": 1.6
    }
    return base_time * multipliers.get(profile, 1.0)

def act(action_name, speed_profile="Normal"):
    if not gw or not keyboard:
        print("Cannot act: Windows dependencies not loaded.")
        return

    # Capture the window you are currently working in
    prev_window = None
    try:
        prev_window = gw.getActiveWindow()
        print(f"[Windows] Saved active background window: {prev_window.title if prev_window else 'None'}")
    except Exception as e:
        print(f"[Windows] Could not capture current window: {e}")

    # 1. Find Roblox Window
    windows = gw.getWindowsWithTitle('Roblox')
    if not windows:
        windows = gw.getWindowsWithTitle('RobloxPlayer')

    if windows:
        win = windows[0]
        try:
            if win.isMinimized:
                win.restore()
            win.activate() # Bring window to front
        except Exception as e:
            print(f"[Windows] Window activation failed: {e}")
        
        # Settle delay after focus change
        time.sleep(get_delay(0.8, speed_profile)) 
        
        # 2. Perform Action
        if action_name == "Jump (Spacebar)":
            keyboard.press(Key.space)
            time.sleep(0.2)
            keyboard.release(Key.space)
            
        elif action_name == "Walk Forward (W)":
            keyboard.press('w')
            time.sleep(0.5)
            keyboard.release('w')
            
        elif action_name == "Walk Backward (S)":
            keyboard.press('s')
            time.sleep(0.5)
            keyboard.release('s')

        time.sleep(get_delay(0.4, speed_profile))
        
        if prev_window:
            try:
                print(f"[Windows] Restoring focus to: {prev_window.title}")
                prev_window.activate()
                time.sleep(get_delay(0.5, speed_profile))
            except Exception:
                fallback_alt_tab(speed_profile)
        else:
            fallback_alt_tab(speed_profile)
        
    else:
        print("Error: Roblox window not found on Windows!")

def fallback_alt_tab(speed_profile):
    """ Manual Alt-Tab key simulation sequence """
    if not keyboard: return
    keyboard.press(Key.alt_l)
    time.sleep(get_delay(0.1, speed_profile))
    keyboard.press(Key.tab)
    time.sleep(get_delay(0.1, speed_profile))
    keyboard.release(Key.tab)
    time.sleep(get_delay(0.1, speed_profile))
    keyboard.release(Key.alt_l)
    time.sleep(get_delay(0.5, speed_profile))