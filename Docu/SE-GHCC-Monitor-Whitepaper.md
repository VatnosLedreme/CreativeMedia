# SE-GHCC-Monitor: Architectural, Security, and UX Whitepaper
**Application Name:** GitHub Copilot Model Advisor / Credit Monitor (SE-GHCC-Monitor)  
**Version:** 1.4.0  
**Author:** Serge-EMR  
**Document Type:** Technical Master Whitepaper & Security Architecture Guide  

---

## 1. Executive Summary
The **GitHub Copilot Credit Monitor v1.4.0 (SE-GHCC-Monitor)** is an offline, zero-dependency client-side web application designed to help individual engineers, consultants, and FinOps managers forecast daily AI consumption. In an era where AI assistants bill via variable token pools or dynamic credit allotments, SE-GHCC-Monitor provides an ultra-secure, instantaneous planning tool that completely isolates budgeting logic from corporate cloud infrastructure.

## 2. Architectural Philosophy & Core Differentiators
Unlike traditional Software-as-a-Service (SaaS) financial trackers or heavy Electron-based desktop utilities, SE-GHCC-Monitor adheres to a strict "Zero-Footprint" philosophy:

* **Vs. Web-Based SaaS Trackers:** Requires no account creation, no database storage, and zero network transmission. It renders instantly from a local `file://` path, executing entirely inside the browser's JavaScript V8/SpiderMonkey engine.
* **Vs. Cloud Billing Portals (Azure/GitHub):** Eliminates complex identity management, slow page rendering, and rigid calendar definitions. Users can dynamically exclude specific days (PTO, holidays) with a single click to instantly calculate real-time daily burn rates.
* **Vs. Spreadsheet Templates (Excel/Sheets):** Replaces easily corrupted macro scripts and complex formula linkages with a purpose-built, responsive user interface supporting mobile, desktop, and landscape orientations.

## 3. Human-Computer Interaction (HCI) Design UX Drivers
The user interface is structured around established ergonomic and psychological principles:

* **Extraneous Load Mitigation (Sweller, 1988):** Complex budget calculations are automated. By providing two raw inputs (Monthly Cap and Consumed Spend), the application computes outstanding daily allowances against dynamically active calendar days in real time.
* **Visual Search & Preattentive Processing (Treisman, 1985):** Key metrics are presented using distinct visual hierarchies. Swatches differentiate counted workdays from weekends and user-toggled leave days. The overarching health of the account is displayed via high-contrast status pills (`Enough credits`, `Almost out of credits`, `No more credits`), allowing instant status comprehension.
* **Frictionless Onboarding:** All interactive controls are paired with an explicit, collapsible `<details>` instruction manual directly within the single-page layout.

## 4. Advanced Security Architecture & Data Sovereignty
SE-GHCC-Monitor v1.4.0 is engineered for highly regulated enterprise environments (e.g., defense, banking, healthcare) where financial data and usage metrics are strictly confidential.

### 4.1. Absolute Client-Side Sandboxing
The application operates entirely within an air-gapped browser execution context. It enforces a rigorous, self-contained Content-Security-Policy (CSP) defined in the document `<head>`:
```html
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data:; font-src 'self'; base-uri 'none'; form-action 'none'; connect-src 'none';">
```
- `connect-src` 'none': Explicitly blocks the XHR/Fetch API, WebSockets, and EventSource. The application is cryptographically forbidden from making outbound network calls or exfiltrating data.

- `form-action` 'none' & `base-uri` 'none': Prevents HTML form hijacking or document base-injection attacks.

- img-src data:: Restricts imagery entirely to secure, hardcoded Base64 inline SVG assets.

### 4.2. Local Storage Sovereignty & File Backup
- Browser Persistence: State is cached exclusively in the user's local browser via `localStorage` under the namespaced key `se-ghcc-monitor-state-v1`.

- Zero-Network JSON Serialization: Clicking "Save .json" generates a fully serialized string in memory and triggers a native HTML5 download via a dynamically constructed `data:application/json` anchor tag. No server backend is involved in formatting or providing the backup file.

### 4.3. Cosmetic Data Masking (Privacy Mode)
To protect confidential corporate spending caps during remote engineering standups or screen sharing, version 1.4.0 implements a multi-tier CSS and JS masking layer triggered by the eye button (`#privacyToggle`):

- Numerical Field Blurring: Applies `filter: blur(5px); opacity: 0.6;` to input boxes.

- String Obfuscation: JavaScript overrides high-contrast summary outputs with non-numeric bullet strings (`••••••, ••%`).

- Data Integrity: This masking is strictly cosmetic; it does not overwrite the raw integer values stored in memory or exported via JSON backups.

## 5. Technical Footprint & Asset Self-Containment
* **Single-File Portability:** The entire application—including layout, CSS themes (Dark, Light, Stealth), state management logic, and vector graphics—is bundled inside a single `.html` file under 25KB in size.

* **Procedural SVG Favicon:** Bypasses external asset requests by embedding its own Base64-encoded SVG vector icon directly into the `<link rel="icon">` tag.

* **Resource Economy:** Consumes virtually zero memory when idle and requires zero background daemons.

## 6. Software Bill of Materials (SBOM) & Dependencies
Product Name: GitHub Copilot Credit Monitor (SE-GHCC-Monitor)
Version: 1.4.0
License: MIT License

Dependency Assessment

This application strictly requires Zero (0) external frameworks, libraries, or network fonts.

Component / APIVersionSourcePurposeRisk ProfileHTML5 / CSS3Native OS BrowserW3C StandardPage structure, responsive grid, dynamic theming.Absolute ZeroVanilla JS (ES6+)Native EngineECMA StandardCalculation engine, date parsing, local serialization.Absolute ZeroWeb Storage APINative BrowserW3C StandardPersistent local client caching (localStorage).Absolute ZeroHTML5 File APINative BrowserW3C StandardParsing and generating offline .json backup payloads.Absolute Zero