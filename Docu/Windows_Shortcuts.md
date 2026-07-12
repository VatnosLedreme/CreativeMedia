# Windows Master Shortcuts Guide

This guide contains the hidden GUID (Globally Unique Identifier) codes used to unlock master control panels and hidden directories in Microsoft Windows.

---

## How to Create These Master Folders

You can deploy any of these shortcuts using two different methods:

### Method 1: Desktop Folder (Permanent)
1. **Right-click** an empty space on your desktop.
2. Hover over **New** and select **Folder**.
3. Copy and paste any of the exact folder names from the list below.
4. Press **Enter**. The folder icon will change automatically.

### Method 2: The Run Box (Instant Access)
1. Press `Windows Key + R` to open the Run dialog.
2. Type `explorer shell:::` followed by the bracketed code.
   * *Example:* `explorer shell:::{ED7BA470-8E54-465E-825C-99712043E01C}`
3. Press **Enter**.

---

## Master Shortcuts Directory

### 1. Windows "God Mode" (All Tasks)
Puts over 200 scattered Windows settings, administrative tools, and configuration links into a single, easily searchable folder.
* **Folder Name:** `GodMode.{ED7BA470-8E54-465E-825C-99712043E01C}`

### 2. Network Connections Panel
Bypasses the modern settings menu to show all physical Wi-Fi, Ethernet, and virtual VPN adapters. Ideal for changing IP configurations or diagnosing connection drops.
* **Folder Name:** `Network.{7007ACC7-3202-11D1-AAD2-00805FC1270E}`

### 3. Applications Directory
A complete repository of every application installed on the PC. This combines classic desktop software and hidden Microsoft Store apps into one master folder, making it easy to create desktop shortcuts.
* **Folder Name:** `Apps.{148BD4BB-A2CD-4726-80A0-A97822651E21}`

### 4. Printers and Devices Dashboard
Opens the legacy hardware dashboard. Use this to quickly add, remove, or manage mice, keyboards, bluetooth accessories, and printers without modern interface lag.
* **Folder Name:** `Hardware.{A8A91A66-3A7D-4424-8D24-04E180695C7A}`

### 5. Programs and Features (Classic Uninstaller)
Takes you straight to the fast, lightweight legacy uninstaller tool. Bypasses the multi-layered modern Windows settings application.
* **Folder Name:** `Uninstall.{7B81BE6A-CE2B-4676-A29E-EB907A5126C5}`

### 6. Classic Advanced System Properties
Skips the generic "About this PC" screen and drops you into the properties menu. Useful for altering environmental variables, setting up virtual memory, and changing network domain/workgroup names.
* **Folder Name:** `System.{BB06C0E4-D293-4F75-8A90-CB05B6477EEE}`

---

## Customization Tip
You can change the text *before* the period in any folder name to whatever you want (e.g., changing `GodMode.` to `MyTools.`). However, you **must keep the period and the exact bracketed code** intact for the shortcut to work.


---
---


# Windows Master Shortcuts Guide (Shortcut Method)

This guide contains the foolproof "Shortcut Method" to unlock master control panels and hidden directories in Microsoft Windows. This method avoids the modern Windows bugs that cause renamed folders to break or become invisible.

---

## How to Create These Master Shortcuts

1. **Right-click** an empty space on your desktop.
2. Hover over **New** and select **Shortcut**.
3. Copy and paste the exact line from the **Target Location** field below.
4. Click **Next**.
5. Type any name you prefer for the shortcut (e.g., "God Mode").
6. Click **Finish**.

---

## Master Shortcuts Directory

### 1. Windows "God Mode" (All Tasks)
Puts over 200 scattered Windows settings, administrative tools, and configuration links into a single, easily searchable window.
* **Target Location:** `explorer shell:::{ED7BA470-8E54-465E-825C-99712043E01C}`

### 2. Network Connections Panel
Bypasses the modern settings menu to show all physical Wi-Fi, Ethernet, and virtual VPN adapters. Ideal for changing IP configurations or diagnosing connection drops.
* **Target Location:** `explorer shell:::{7007ACC7-3202-11D1-AAD2-00805FC1270E}`

### 3. Applications Directory
A complete repository of every application installed on the PC. This combines classic desktop software and hidden Microsoft Store apps into one master screen, making it easy to launch or manage tricky apps.
* **Target Location:** `explorer shell:::{148BD4BB-A2CD-4726-80A0-A97822651E21}`

### 4. Printers and Devices Dashboard
Opens the legacy hardware dashboard. Use this to quickly add, remove, or manage mice, keyboards, bluetooth accessories, and printers without modern interface lag.
* **Target Location:** `explorer shell:::{A8A91A66-3A7D-4424-8D24-04E180695C7A}`

### 5. Programs and Features (Classic Uninstaller)
Takes you straight to the fast, lightweight legacy uninstaller tool. Bypasses the multi-layered modern Windows settings application.
* **Target Location:** `explorer shell:::{7B81BE6A-CE2B-4676-A29E-EB907A5126C5}`

### 6. Classic Advanced System Properties
Skips the generic "About this PC" screen and drops you into the advanced system configuration window. Useful for altering environmental variables, setting up virtual memory, and changing network domain/workgroup names.
* **Target Location:** `explorer shell:::{BB06C0E4-D293-4F75-8A90-CB05B6477EEE}`

---

## Bonus: How to Use These Instantly (The Run Box)
If you do not want to create a permanent desktop icon, you can use these shortcuts temporarily:
1. Press `Windows Key + R` on your keyboard.
2. Paste any of the **Target Location** strings from above into the box.
3. Press **Enter**.



---
---



# Windows Shell Commands & Official Technical Names

The table below maps the hidden `explorer shell:::` shortcuts to their official internal Windows database names and common user nicknames. 

In technical terms, these strings are known as **CLSID (Class Identifier) codes**, which act as unique coordinates for virtual folders within the Windows operating system shell.

---

## Technical Names Reference Table

| Target Location Code | Official Windows Technical Name | Common / Friendly Nickname |
| :--- | :--- | :--- |
| `explorer shell:::{ED7BA470-8E54-465E-825C-99712043E01C}` | **All Tasks** | God Mode (Windows Master Control Panel) |
| `explorer shell:::{7007ACC7-3202-11D1-AAD2-00805FC1270E}` | **Network Connections** | Network Connections Adapter Settings |
| `explorer shell:::{148BD4BB-A2CD-4726-80A0-A97822651E21}` | **Applications** | The Apps Folder |
| `explorer shell:::{A8A91A66-3A7D-4424-8D24-04E180695C7A}` | **Devices and Printers** | Hardware and Devices Dashboard |
| `explorer shell:::{7B81BE6A-CE2B-4676-A29E-EB907A5126C5}` | **Programs and Features** | Add/Remove Programs (Classic Uninstaller) |
| `explorer shell:::{BB06C0E4-D293-4F75-8A90-CB05B6477EEE}` | **System** | Classic Advanced System Properties |

---

## Technical Notes
* **The Windows Registry:** The names in the **Official Windows Technical Name** column are the explicit identifiers hardcoded by Microsoft developers inside the Windows Registry database.
* **Origin of "God Mode":** The phrase "All Tasks" is the true backend name for God Mode. The "God Mode" title was completely invented by tech bloggers in 2007 during the Windows Vista era.


# Windows Master Configuration & Hidden Diagnostics Registry

This master document serves as a complete repository for hidden Windows configuration portals, advanced diagnostics, and system shortcuts. Using these commands bypasses modern menu restrictions and allows direct access to the legacy core of the operating system.

---

## 🛠️ Deployment Methods

You can deploy any tool in this document using one of two methods:

### Method 1: Desktop Shortcut (Permanent Icon)
1. **Right-click** an empty space on your desktop.
2. Hover over **New** and select **Shortcut**.
3. Paste the string from the **Command / Code** column into the location field.
4. Click **Next**, name the shortcut whatever you want, and click **Finish**.

### Method 2: The Run Box (Instant Execution)
1. Press **`Windows Key + R`** on your keyboard.
2. Paste the string from the **Command / Code** column directly into the box.
3. Press **Enter**.

---

## 📊 Master Shortcuts Directory (CLSID Virtual Folders)

These shortcuts leverage Class Identifier (CLSID) strings to open virtual folders managed directly by the Windows Shell interface.

| Command / Code | Official Windows Technical Name | Practical Function / Nickname |
| :--- | :--- | :--- |
| `explorer shell:::{ED7BA470-8E54-465E-825C-99712043E01C}` | **All Tasks** | **God Mode**: A searchable master list of over 200 system configurations on one screen. |
| `explorer shell:::{7007ACC7-3202-11D1-AAD2-00805FC1270E}` | **Network Connections** | **Network Adapters**: Instantly manage, disable, or assign static IPs to Wi-Fi and Ethernet hardware. |
| `explorer shell:::{148BD4BB-A2CD-4726-80A0-A97822651E21}` | **Applications** | **The Apps Folder**: Displays all classic software and hidden Microsoft Store apps in one place. |
| `explorer shell:::{A8A91A66-3A7D-4424-8D24-04E180695C7A}` | **Devices and Printers** | **Hardware Dashboard**: Manage external accessories and fix printer issues without interface lag. |
| `explorer shell:::{7B81BE6A-CE2B-4676-A29E-EB907A5126C5}` | **Programs and Features** | **Classic Uninstaller**: Lightweight and fast tool to uninstall software without modern settings lag. |
| `explorer shell:::{BB06C0E4-D293-4F75-8A90-CB05B6477EEE}` | **System** | **Advanced System Properties**: Instantly tweak virtual memory page files and environment variables. |
| `explorer shell:::{2559a1f3-21d7-11d4-bdaf-00c04f60b9f0}` | **Run Dialog Folder** | **Network Search Panel**: A unique directory built to browse all shared local network paths at once. |
| `explorer shell:::{05d7b0f4-2121-4eff-bf6b-ed3f69b894d9}` | **Notification Icons** | **Tray Icon Manager**: Control which icons stay permanently visible or hidden on the taskbar. |
| `explorer shell:::{d555645e-2b78-478a-9150-0dbca88a2c2d}` | **Network Sharing** | **Network Sharing Center**: Rapid access to classic profile sharing configurations and network visibility. |
| `explorer shell:startup` | **Startup Folder** | **Startup Direct Link**: Paste any normal program shortcut here to force it to run when Windows boots up. |

---

## ⚡ Power Diagnostics & Executables (Run Commands)

These commands bypass the Windows File Explorer entirely. They pull up high-level optimization, diagnostic, or security engines directly from the Windows system root directory.

| Command / Code | System Tool Name | Practical Function / Fix |
| :--- | :--- | :--- |
| `msinfo32` | **System Information** | **MSInfo**: Provides a complete diagnostic readout of every hardware component and system driver. |
| `resmon` | **Resource Monitor** | **Advanced Task Manager**: Track real-time charts showing precisely which processes hog disk IO or network bandwidth. |
| `mrt` | **Malware Removal Tool** | **Built-in Virus Scanner**: Forces a manual deep system scrub using Microsoft’s standalone security scanner. |
| `mdsched` | **Memory Diagnostic** | **RAM Tester**: Restarts your system to run deep binary hardware scans for malfunctioning RAM sticks. |
| `cleanmgr` | **Disk Cleanup** | **Legacy Storage Cleaner**: Rapid tool to safely purge gigabytes of cached Windows Update junk files. |
| `gpedit.msc` | **Local Group Policy Editor** | **OS Policy Master**: *(Pro/Enterprise Only)* Permanently disable telemetry, block forced restarts, or modify deep OS rules. |

---

## 🎹 Hidden Productivity Key Combos

Keep these built-in hotkey combinations memorized to navigate Windows significantly faster.

* **`Windows Key + V`** : Opens **Clipboard History**. Allows you to view and paste items from a history list of your last 25 copied texts, links, or screenshots.
* **`Windows Key + Period (.)`** : Opens the native **Glyph & Emoji Picker**. Gives you immediate access to standard emojis, animated GIFs, emoticons, and advanced math/language symbols in any text field.



