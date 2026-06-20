# 📦 SBOM (Software Bill of Materials)

## Overview
HWA-Launcher (v1.12.0) is designed to be highly portable and secure by relying **exclusively on the Python Standard Library**. There are zero third-party dependencies required to run the source code, drastically reducing the risk of software supply chain attacks.

### Application Details
* **Application Name:** HWA-Launcher
* **Version:** 1.12.0
* **Primary Language:** Python 3.x
* **License:** Provided "As-is" (Vibe Coded)

### Component Inventory

Because the application uses no external `pip` packages (like `requests` or `Pillow`), the SBOM consists entirely of built-in Python modules.

| Component | Type | Version | License | Origin | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Python** | Runtime Engine | `3.6+` | Python Software Foundation License | built-in | Core execution engine. |
| **tkinter** | GUI Framework | Native | PSF | built-in | Renders the application windows, canvas, buttons, and procedurally generated icons. |
| **os** | System Module | Native | PSF | built-in | File path resolution (`abspath`), directory extraction, and file validation (`exists`). |
| **sys** | System Module | Native | PSF | built-in | Platform detection (`win32`, `darwin`) and executable environment checking (`sys.frozen`). |
| **socket** | Networking | Native | PSF | built-in | Localhost port binding to enforce the single-instance application lock. |
| **webbrowser** | Utility | Native | PSF | built-in | Safely hands off web links and `.html` files to the system's default browser. |
| **subprocess** | Utility | Native | PSF | built-in | Securely executes local applications and opens text editors on Mac/Linux environments. |
| **urllib.parse** | Utility | Native | PSF | built-in | Safely parses and sanitizes URLs to extract domain names for the fallback UI labels. |

### Build Considerations (If compiling to EXE)
If you choose to package this application into a standalone executable using a tool like **PyInstaller**, the resulting binary will contain the Python interpreter and the required compiled `.pyd`/`.dll` files for the above standard libraries. When scanning the compiled executable, security tools will detect standard Python C-binaries.