# Security Policy

## Supported Versions
Only the latest version of the HTML Project Launcher receives active security updates. 

| Version | Supported          |
| ------- | ------------------ |
| 1.4.x   | :white_check_mark: |
| < 1.3.x | :x:                |

## Reporting a Vulnerability
If you discover a security vulnerability within this project, please do not disclose it publicly. Instead, submit an issue tagged strictly as `[SECURITY]` or contact the maintainer directly. We will attempt to acknowledge your report within 48 hours.

## Security Architecture Notes
This application is designed with security and minimal permissions in mind:
1. **Zero Telemetry:** The application makes zero network requests. It does not track, log, or send data externally.
2. **Path Traversal Prevention:** The application strictly uses absolute path resolution (`os.path.abspath`) locally. It does not scan underlying directories recursively, preventing arbitrary directory traversal exposure.
3. **Safe Execution Execution:** The application does not execute arbitrary code. It utilizes `webbrowser.open()` specifically bound to `file://` URIs to safely hand off file paths to the user's default OS web browser.
4. **Command Injection Prevention:** Native OS calls (e.g., opening text editors via `subprocess.run()`) use hardcoded argument arrays with `shell=False` to prevent shell injection vectors.