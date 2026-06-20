# Architectural Decision Record: Automatic GitHub Copilot Credit Syncing

## Overview
This document outlines the technical and security evaluation regarding the proposal to add automatic synchronization of GitHub Copilot credit data (maximum credits and outstanding usage) to the **GitHub Copilot Credit Monitor** standalone HTML application.

**Decision:** The feature cannot be implemented. The application will remain a manual, strictly offline planning aid.

---

## Technical Constraints

### 1. Absence of a Public Individual-User API
Currently, GitHub does not offer a public, CORS-enabled API endpoint for individual users to securely query their real-time Copilot credit consumption. 
*   **Existing APIs:** While GitHub provides billing APIs for Enterprise and Organization administrators to track seat usage, these do not extend to individual user autocomplete credit limits or current balances.
*   **Current Access:** The only method to retrieve this specific data is by manually authenticating into the GitHub web interface and navigating to the billing dashboard.

### 2. Destruction of the Zero-Trust Security Model
The fundamental value proposition of this application is its strict, offline security model, enforced by a rigorous Content Security Policy (CSP).
*   **The Air-Gap Guarantee:** The application utilizes the directive `connect-src 'none';` within its CSP. This guarantees that the file cannot send or receive data over the internet.
*   **Impact of Syncing:** To fetch data from GitHub, this CSP directive would need to be relaxed or removed entirely. Doing so would fundamentally break the zero-telemetry, 100% offline privacy guarantee that makes this client-side tool safe to use on any device.

### 3. Authentication Vulnerabilities (OAuth & PATs)
Even in a hypothetical scenario where an appropriate GitHub API existed, authenticating a standalone HTML file introduces severe security risks.
*   **OAuth Limitations:** A standard GitHub OAuth flow requires a secure backend server to hold a "Client Secret" and securely process the callback URL. A standalone, client-side HTML file cannot perform this flow securely without exposing credentials.
*   **Personal Access Token (PAT) Risks:** The alternative authentication method requires the user to generate a PAT with billing-level permissions and paste it directly into the application. Storing a highly sensitive, high-privilege token in a local webpage exposes the user to massive security risks. If a malicious browser extension were running on the user's machine, it could steal the token from local storage and compromise the user's entire GitHub account.

---

## Conclusion
Due to the lack of supporting APIs from GitHub, the technical limitations of client-side OAuth, and the unacceptable security risks associated with modifying the application's Content Security Policy and handling Personal Access Tokens, automatic syncing is not feasible. 

The current architecture, a completely offline, manual budgeting tool remains the safest, most private, and most reliable method for local credit monitoring.
