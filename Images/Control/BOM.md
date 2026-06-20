# Software Bill of Materials (BOM)

This document outlines the dependencies, libraries, and components utilized by the HTML Project Launcher.

## 1. Application Details
* **Name:** HTML Project Launcher
* **Version:** 1.4.0
* **Author:** Serge-EMR
* **License:** MIT

## 2. Core Language
* **Python:** Requires version 3.6 or higher.

## 3. Standard Library Dependencies
The runtime application relies strictly on Python's Standard Library. No external packages via `pip` are required for the source code to execute.
* `os`: Path resolution and file system interactions.
* `sys`: System-specific parameters and executable state detection.
* `tkinter`: Standard GUI framework for Python.
* `webbrowser`: High-level interface to display web-based documents.
* `subprocess`: Spawning processes to open the native text editor across different OS platforms.

## 4. Development & Build Tools (Optional)
Required only for compiling the application into a standalone executable.
* **PyInstaller:** Used via `pip install pyinstaller`.

## 5. Local File Generation
The application automatically generates and relies on the following local files during runtime:
* `paths.txt`: A plain text file used as the data source for generating launcher buttons. Created in the root directory of the application upon first run.