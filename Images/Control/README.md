# HTML Project Launcher 🚀

A lightweight, portable desktop application built in Python and Tkinter. This app serves as a centralized hub to easily manage and launch local HTML files and web projects directly in your default web browser.

## ✨ Features
* **Zero Dependencies:** Built entirely with standard Python libraries. No external packages required to run the source code.
* **Auto-Adjusting UI:** The window automatically resizes to perfectly wrap around your project list, introducing a scrollbar only when necessary.
* **Always-on-Top Toggle:** Pin the launcher above all other windows for quick access while developing.
* **Procedural Icon:** Generates a dynamic, memory-safe app icon on the fly if a physical `.ico` file is missing.
* **Simple Configuration:** Add or edit projects by simply pasting their absolute paths into a local text file (`paths.txt`).
* **Cross-Platform:** Works natively on Windows, macOS, and Linux.

## 🛠️ Getting Started

### Prerequisites
* Python 3.x installed on your system.

### Running from Source
1. Clone or download this repository.
2. Open a terminal or command prompt in the project folder.
3. Run the script:
   ```bash
   python launcher.py