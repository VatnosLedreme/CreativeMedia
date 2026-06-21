# Security Documentation: HWA-Launcher

HWA-Launcher is built with local execution safety and system stability in mind. Below are the implemented security constraints and threat mitigations for version 2.00.00.

## 1. Protocol & Execution Whitelisting
The application strictly validates all inputs parsed from `paths.txt` before passing them to the OS.
* **Web Protocols:** Only `http://`, `https://`, and `www.` prefixes are routed to the system's default browser.
* **Blocked Protocols:** Potentially dangerous URI schemes such as `javascript:`, `data:`, and `file:` are explicitly intercepted and blocked via a standard GUI error dialogue.
* **File Whitelisting:** Local file execution is strictly limited to `.html`, `.exe`, and `.bat` extensions. Attempting to pass `.ps1`, `.vbs`, or arbitrary binaries will trigger a security block.

## 2. Execution Context Isolation
When launching `.exe` or `.bat` files, the application explicitly locks the execution context (`cwd`) to the target application's native directory via `subprocess.Popen([abs_path], cwd=cwd)`. This prevents path-hijacking or unintended behavior from applications that rely on relative file paths to load dependencies.

## 3. Concurrency Protection (Socket Locking)
To prevent race conditions, memory leaks, or file-write collisions on `paths.txt`, the application enforces a single-instance lock. It binds a hidden socket to `127.0.0.1:54321`. If a user attempts to open a second instance of the launcher, the socket lock catches the `socket.error`, alerts the user, and terminates the duplicate process instantly.

## 4. Input Sanitization
The procedural file parser limits reading to 20 items at a time to prevent memory overflows from maliciously or accidentally bloated `.txt` files.

## Limitations & Acceptable Risk
* **File Write Access:** The application requires write permissions in its current working directory to generate and update `paths.txt`.
* **Trust Model:** The application assumes the user has control over the contents of `paths.txt`. It does not hash or verify the signatures of the `.exe` files listed in the document.