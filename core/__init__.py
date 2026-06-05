import platform

OS_TYPE = platform.system()

if OS_TYPE == "Linux":
    try:
        from core import linux_input as os_input
    except ImportError as err:
        os_input = None
        print(f"Linux Import Error: {err}")
elif OS_TYPE == "Windows":
    try:
        from core import windows_input as os_input
    except ImportError as err:
        os_input = None
        print(f"Windows Import Error: {err}")
else:
    os_input = None
    print(f"Warning: OS '{OS_TYPE}' is not supported yet.")

def execute_action(action_name, speed_profile="Normal"):
    if os_input is not None:
        os_input.act(action_name, speed_profile)
    else:
        print(f"Cannot execute '{action_name}': Platform engine is not loaded or unsupported.")