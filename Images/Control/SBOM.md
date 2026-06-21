# Software Bill of Materials (SBOM)

**Product Name:** HWA-Launcher  
**Version:** 2.00.00  
**Author:** Serge-EMR  
**License:** Provided "As-Is"  

## Overview
This application requires **Zero (0)** external dependencies. It is built entirely on the Python Standard Library to ensure maximum portability, future-proof stability, and minimal supply-chain risk. No third-party packages (e.g., from PyPI) are downloaded, installed, or required at runtime.

## Component List

| Component / Module | Version | Origin | Purpose |
| :--- | :--- | :--- | :--- |
| `os` | Standard Library | Python Core | Path routing, system environment interactions. |
| `sys` | Standard Library | Python Core | Frozen EXE detection, platform identification. |
| `socket` | Standard Library | Python Core | Single-instance enforcement via loopback binding. |
| `tkinter` | Standard Library | Python Core | Core Graphical User Interface (GUI) framework. |
| `messagebox` | Standard Library | Python Core (`tkinter`) | Displaying system error dialogues and warnings. |
| `webbrowser` | Standard Library | Python Core | Securely routing safe URLs to the default browser. |
| `subprocess` | Standard Library | Python Core | Executing cross-platform binaries/scripts. |
| `urllib.parse` | Standard Library | Python Core | Safe parsing of URLs to extract domain names. |
| `ctypes` | Standard Library | Python Core | Interfacing with Windows API for UI styling exclusions. |