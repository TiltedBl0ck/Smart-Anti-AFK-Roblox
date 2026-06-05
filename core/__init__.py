import platform

# 1.Detect the operating system
OS_TYPE = platform.system()

# 2.Dynamically import only the module needed for the current OS
if OS_TYPE == "Linux":
    try:
        from . import linux_input as os_input
    except ImportError as err:
        os_input = None
        print(f"Linux Import Error: {err}")
elif OS_TYPE == "Windows":
    try:
        from . import windows_input as os_input
    except ImportError as err:
        os_input = None
        print(f"Windows Import Error: {err}")
else:
    os_input = None
    print(f"Warning: OS '{OS_TYPE}' is not supported yet.")

def execute_action(action_name, speed_profile="Normal"):
    """
    Exposes a unified interface to the main app.
    Routes the action and timing profile to the active platform's input engine.
    """
    if os_input is not None:
        os_input.act(action_name, speed_profile)
    else:
        print(f"Cannot execute '{action_name}': Platform engine is not loaded or unsupported.")