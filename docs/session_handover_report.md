# 🔄 AI Session Handover Report: Ancient Calendars v6.0.1

**Date**: February 5, 2026
**Version**: v6.0.1 (Oracle Linux 9 Ready)
**Git Branch**: `main` (Synced)

---

## 1. Executive Summary
The application has been successfully upgraded to **v6.0.1**. Critical features (Chatbox, Sky Map) have been restored and modernized. The deployment scripts are fully optimized for **Oracle Linux 9** on OCI. The codebase is stable, and the remote repository is verified to be in sync.

---

## 2. Key Achievements in This Session
1.  **Restored Chat Widget**:
    *   **Issue**: Code was missing in `insights_panchanga.html`.
    *   **Fix**: Re-implemented the floating widget and `toggleChat/sendMessage` JS logic.
2.  **Implemented "Co-Pilot" Sky Map**:
    *   **Change**: Removed embedded D3/Stellarium iframes to solve WASM memory errors.
    *   **New Flow**: "Open Sky Map" buttons now launch Stellarium Web in a **new tab** (`window.open`) and trigger a "Toast Notification" guiding the user on what to search for.
3.  **Oracle Linux 9 Deployment**:
    *   **Updates**: Enhanced `deploy.sh` to include `epel-release` and `tar`.
    *   **Fixes**: Included SELinux booleans (`httpd_can_network_connect`) to allow Nginx->Gunicorn communication.
4.  **Documentation Refresh**:
    *   Updated `MASTER_ARCHITECTURE_V2.md`, `Student_User_Guide.md`, and `Cosmic_Explorer_Student_Guide.md` to reflect the new architecture.

---

## 3. Active Architecture ("Headless v2.0")
*   **Split Architecture**: The frontend (`insights_panchanga.html`) is decoupled from the backend logic (`app.py`). It consumes data via JSON APIs (`/api/ai-chat`, `/api/ai-explain`).
*   **Gateway**: Production runs via `gateway.py` (Gunicorn) behind Nginx.
*   **AI Engine**: Uses a "Double-Spoke" prompt architecture (Foundation + Civilization Context).

---

## 4. Deployment Instructions (Oracle Cloud)
To deploy this exact state on a fresh Oracle Linux 9 VM:

```bash
# 1. Set Environment Keys (Optional but recommended)
export GOOGLE_API_KEY="your_api_key"

# 2. Run the Orchestrator
curl -L https://raw.githubusercontent.com/nanjunda/ancient_calendar_v2.1/main/setup_fresh.sh | bash
```
*Note: The script now defaults to the `main` branch.*

---

## 5. Critical Files & Integrity
*   **Audit Report**: Refer to `project_file_audit_report.md` for a detailed list of Active vs. Legacy files.
*   **Action Pended**: The user has the report but has *not yet approved* the deletion of legacy files (e.g., `panchanga_converter.py`, `test_*.html`). **Do not delete them without explicit approval.**

---

## 6. Next Recommended Actions
1.  **Cleanup**: Review `project_file_audit_report.md` and archive/delete the "Red" category files to slim down the repo.
2.  **Monitor**: Watch the application logs (`journalctl -u ancient_calendar_v2.1 -f`) on the VM after deployment to ensure the Chatbox/AI connection is stable.

---
*End of Handover Report*
