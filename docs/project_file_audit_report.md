# 📂 Project File Integrity & Audit Report (v6.0.1)

**Date**: February 5, 2026
**Purpose**: Inventory of active v6.0.1 application files vs. legacy/obsolete artifacts.

---

## 🟢 1. Active Application Core (Production Critical)
*These files are essential for the Runtime, Logic, and UI of the application.*

### **Entry Points & Gateways**
*   `app.py`: **Main Application Entry**. Defines Flask routes and API endpoints.
*   `gateway.py`: **WSGI Gateway**. Headless entry point for Gunicorn/production servers.
*   `wsgi.py`: Standard WSGI exposure hook.

### **Logic Engines ("The Brain")**
*   `engines/`:
    *   `base.py`: Abstract base class for all calendar engines.
    *   `factory.py`: Logic to instantiate correct engine based on user selection.
    *   `panchanga/`: Core Hindu Panchanga calculations.
    *   `mayan/`: Core Mayan Chronology calculations.
*   `utils/`:
    *   `ai_engine.py`: **AI Maestro**. Handles OpenRouter/Gemini integration.
    *   `astronomy.py`: **NASA JPL Wrapper**. High-precision Skyfield logic.
    *   `location.py`: Geocoding and timezone utilities.
    *   `zodiac.py`: Calculation logic for Rashi/Nakshatra boundaries.
    *   `ical_gen.py`: iCalendar (.ics) generator.

### **Frontend & UI ("The Skin")**
*   `templates/`:
    *   `index.html`: Landing Page / Portal.
    *   `insights_panchanga.html`: **Core UI**. The "Panchanga Insights" dashboard (renamed from `insights.html`).
    *   `insights_mayan.html`: The "Mayan Insights" dashboard.
    *   `guide.html`: The "Student Guide" / Masterclass view.
    *   `portal.html`: Alternative landing view.
    *   `visuals/`: (Subfolder) Contains all 3D visualization iframes (zodiac, precession, etc.).
*   `static/`:
    *   `css/`: Core stylesheets (Glassmorphism design system).
    *   `js/`: Client-side interactivity.
    *   `images/`: Texture assets for 3D visualizations.

### **Data Assets**
*   `data/star_catalog.json`: **New in v6.0**. Normalized catalog of stars for Sky Map search.
*   `de421.bsp`: **Critical Binary**. NASA JPL planetary ephemeris data file (600MB+). Do not delete.

---

## 🟡 2. Deployment & Orchestration
*These files are actively used to install and run the application on servers.*

*   `setup_fresh.sh`: **Orchestrator**. The "One-Click" installer for Oracle Linux 9.
*   `deploy.sh`: **Worker Script**. Handles dependencies, SELinux, and filesystem setup.
*   `requirements.txt`: Python dependency manifest (pinned versions).
*   `ancient_calendars.nginx.template`: Nginx reverse proxy configuration.
*   `panchanga_gateway.service.template`: Systemd service definition for Gunicorn.
*   `docker-compose.yml` / `Dockerfile`: Containerization configs (Valid, but secondary to the Oracle Linux 9 script).

---

## 🔵 3. Reference Documentation
*These files define the project but are not executed.*

*   `docs/MASTER_ARCHITECTURE_V2.md`: **Source of Truth**. Current architecture spec.
*   `docs/Student_User_Guide.md`: **Manual**. The Functional Application Manual.
*   `docs/Cosmic_Explorer_Student_Guide.md`: **Textbook**. The Educational Content.
*   `README.md`: GitHub landing page.
*   `docs/`: (Various historical archives of previous version specs like v3.2, v4.1, etc.).

---

## 🔴 4. Inactive / Legacy / Test Artifacts (Cleanup Candidates)
*These files are NOT used by the live v6.0.1 application and can typically be archived or ignored.*

### **Test Harnesses & Verification**
*   `verify_parity.py`: Regression test suite (Keep for dev, remove from Prod).
*   `stress_test_parity.py`: Load tester (Keep for dev).
*   `debug_calculation.py`: Scratchpad for math debugging.
*   `verify_v2_api.py`: API contract tester.
*   `verify_mayan.py`: Mayan math tester.
*   `trace_tithi.py`: Specific debugging script for Tithi jumps.

### **Disposable Prototypes** (Safe to Archive)
*   `test_*.html` (ALL of them):
    *   `test_embed.html`
    *   `test_d3_simple.html`
    *   `test_d3_celestial.html` (Old embedded map POC)
    *   `test_aladin.html` / `test_wwt.html` (Abandoned sky map alternatives)
    *   `test_celestial_new.html`
*   `panchanga_converter.py`: **Legacy Entry**. Old monolithic CLI/Flask app (replaced by `app.py`).

### **Temporary / Local Configs**
*   `gregorian_to_ancient_calendars.code-workspace`: VS Code configuration.
*   `possibleImages/`: Unsorted asset folder.
*   `scripts/generate_star_catalog.py`: **Utility**. Run once to generate `data/star_catalog.json`, not needed at runtime.

---

## 📋 Recommended Action Plan

To "Slim Down" the production deployment, you can safely exclude the **Category 4 (Red)** files.
The `deploy.sh` script currently uses `rsync --exclude` to handle some of this (`.git`, `venv`), but adding the `test_*.html` files to the exclude list would further clean up the production server.
