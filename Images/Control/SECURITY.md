# 🛡️ SECURITY

## Security Policies & Architecture

The HWA-Launcher is designed with a minimal attack surface and strict internal guardrails to prevent common desktop application vulnerabilities.

### Supported Versions
Only the latest version is actively supported for security updates.
| Version | Supported |
| :--- | :--- |
| **v1.12.0** | ✅ Yes |
| < v1.11.0 | ❌ No |

### Built-in Security Mechanisms

#### 1. Arbitrary Execution Mitigation (Strict Filtering)
The application does not blindly execute paths provided in the `paths.txt` file. During the read phase, the application verifies the file extension. **Only `.html`, `.exe`, and `.bat` files, alongside standard web protocols (`http://`, `https://`), are permitted.** Any other extension (e.g., `.ps1`, `.vbs`, `.js`) is silently dropped and ignored, preventing accidental execution of malicious scripts.

#### 2. Local Directory Context Locking
When launching `.exe` or `.bat` files, the application uses Python's `os.startfile` (Windows) or `subprocess.Popen` (Mac/Linux) while explicitly setting the Current Working Directory (`cwd`) to the exact folder where the executable resides. This ensures the target application loads its own local assets and mitigates certain types of DLL hijacking that occur when applications are launched from an untrusted working directory.

#### 3. Path Traversal Prevention
All local paths are passed through `os.path.abspath()`. This sanitizes user input and resolves any relative pathing tricks (e.g., `../../Windows/System32/`) before checking if the file actually exists on the disk.

#### 4. Memory Exhaustion Protection
To prevent Denial of Service (DoS) via memory exhaustion (e.g., a user pasting 100,000 lines into `paths.txt`), the file reader includes a strict break condition. The app stops parsing memory once it hits **20 valid items**, ensuring UI rendering and memory utilization remain flat and instantaneous.

#### 5. Race Condition Prevention (Instance Lock)