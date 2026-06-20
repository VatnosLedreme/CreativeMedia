# 📄 README

## HWA-Launcher (v1.12.0)
**A lightweight, safe, and customizable launcher for your local projects, web applications, and executables.**

HWA-Launcher (formerly HTML-WEB-Launcher) is a Python-based desktop utility that gives you a clean, unified interface to launch web links, local `.html` files, and local executables (`.exe`, `.bat`). It features a smart window that auto-adjusts to your content, procedural UI elements, and a memory-safe architecture.

### ✨ Key Features
* **Unified Dashboard:** Access web links, local web pages, and native apps from one clean interface.
* **Custom Labels:** Rename your launcher buttons using a simple pipe (`|`) syntax without changing the actual file names.
* **Smart Color Coding:** Visual cues to identify your targets instantly:
    * **Blue:** Web Links (http/https/www)
    * **Green:** Local HTML files (.html)
    * **Red:** Local Executables (.exe, .bat)
* **Strict Security Filtering:** Automatically rejects unsupported or potentially dangerous file types.
* **Resource Friendly:** Procedurally generated graphics (no external image assets required) and a hard cap of 20 items to guarantee zero memory lag.
* **Single-Instance Lock:** Prevents accidentally opening multiple copies of the launcher.
* **Always-on-Top Toggle:** Pin the launcher over other windows for rapid access.

---

### 🚀 Step-by-Step Usage Guide

**Step 1: First Launch**
Run the `main.py` script (or the compiled `.exe` if you used PyInstaller). The app will generate a safe `paths.txt` file in its root directory if one doesn't exist.

**Step 2: Edit Your Paths**
Click the **"📝 Edit Paths"** button in the app header. This will open `paths.txt` in your system's default text editor.

**Step 3: Add Your Links and Files**
Add your absolute paths or web links, one per line. You can optionally add a custom label by using the `|` character. 
*Note: The app accepts a maximum of 20 valid items.*

**Formatting Examples:**
```text
# Example 1: Standard Web Link
[https://github.com](https://github.com) | My Code Repository

# Example 2: Local HTML File
C:\Users\Name\Documents\Projects\Portfolio\index.html | My Portfolio Website

# Example 3: Local Executable
C:\Tools\Development\server.exe | Local Development Server

# Example 4: No custom label (App will auto-format the name)
[https://google.com](https://google.com)