Smart Anti-AFK (Windows & Linux)

A cross-platform, smart Anti-AFK tool designed for Roblox (and the Sober emulator on Linux).

Unlike basic auto-clickers that hijack your mouse and prevent you from using your computer, this tool intelligently targets the game window in the background, performs a movement action, and automatically restores focus directly to whatever app you were previously working in.

✨ Features

💻 Cross-Platform: Runs seamlessly on both Windows and Linux.

🧠 Smart Focus Restoration: Uses xdotool (Linux) and window activation (Windows) to instantly return you to your workspace after executing an action.

🛡️ Hardware-Level Input: Uses evdev on Linux and pynput on Windows to bypass standard input-blocking, ensuring the game always registers your movement.

🕒 Customizable Intervals: Choose exactly how often the script triggers (5, 10, 15, or 20 minutes).

👻 Unobtrusive GUI: The interface automatically minimizes to your taskbar/dock when enabled so it stays out of your way.

🚀 Download & Usage (For Regular Users)

You do not need to install Python to use this application!

Go to the Releases page on the right side of this repository.

For Windows: Download Smart-Anti-AFK-Windows.exe and double-click to run.

For Linux: Download the Smart-Anti-AFK-Linux executable, right-click to make it executable (or run chmod +x), and launch it.

🐧 Linux Specific Setup (Required)

To ensure the game detects the keystrokes, this app simulates hardware-level keyboards. You must grant permission to access the input system, and you need xdotool for the smart-window switching.

Run these commands in your terminal:

# 1. Install xdotool for smart window switching
sudo apt install xdotool

# 2. Grant virtual keyboard permissions (Run this once per reboot)
sudo chmod 666 /dev/uinput


🛠️ For Developers (Building from Source)

If you want to modify the code, build the project yourself, or contribute, follow these steps:

Prerequisites

Python 3.10+

Git

Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/Smart-Anti-AFK.git
cd Smart-Anti-AFK


Install OS-specific dependencies:
(This will automatically detect your OS and install either evdev or pynput/pygetwindow)

pip install -r requirements.txt


Run the script:

python main.py


🤝 Contributing

Pull requests are welcome! If you want to add MacOS support or improve the window management logic, feel free to fork the repository and submit a PR.

📄 License

This project is open-source and free to use.