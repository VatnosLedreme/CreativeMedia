# HWA-Launcher (v2.00.00)

A lightweight, highly optimized, standalone desktop launcher designed for rapid access to local HTML files, executable applications, and web links. Built entirely on Python's standard library with a custom-engineered UI that integrates deeply with the Windows Desktop Window Manager (DWM).

---

## 📖 Table of Contents
1. [Features](#-features)
2. [Installation & Setup](#-installation--setup)
3. [Usage & Configuration](#-usage--configuration)
4. [Security Documentation](#-security-documentation)
5. [Software Bill of Materials (SBOM)](#-software-bill-of-materials-sbom)

---

## ✨ Features

* **Zero Dependencies:** Runs on pure Python. No `pip install` required.
* **Deep Windows OS Integration:** Utilizes `ctypes` and layered window hacks to create borderless, transparent UI elements while preventing the infamous "Ghost Window" (Alt+Tab orphaned handles) bug.
* **Procedural Asset Generation:** Generates its own 32x32 PPM application icon dynamically in memory. No external `.ico` or image files required to run.
* **Smart Parsing:** Automatically extracts readable display names from URLs (e.g., formats `https://github.com` into "GITHUB Com").
* **Dynamic Theming:** Built-in Light and Dark modes with isolated opacity controls.
* **Single-Instance Lock:** Prevents multiple instances of the launcher from running simultaneously via a system-wide localhost socket lock.

---

## 🚀 Installation & Setup

Because this application relies exclusively on the Python Standard Library, deployment is trivial.

### Prerequisites
* Python 3.8 or higher.
* Windows 10/11 (Recommended for full transparency/UI features), macOS, or Linux (Fallback UI applies).

### Running from Source
1. Clone or download the repository.
2. Run the script:
   ```bash
   python hwa_launcher.py