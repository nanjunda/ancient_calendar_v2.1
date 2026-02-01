# Implementation Plan - Mayan Student Guide Upgrade

## Goal
Transform the "Mayan Masterclass" in `guide.html` into a fully interactive, scientifically rich experience with custom 3D visuals and engaging content, fixing reported bugs and addressing user feedback.

## User Review Required
> [!IMPORTANT]
> **Visual "Not Found" Fix**: The existing "Solar System" visual failed to load. I will replace it with a dedicated **Venus Synodic Simulator**.

## Deployment Strategy: Oracle Cloud (Oracle Linux 9)

We will utilize the **Two-Script Orchestration Technique** proven in the 'Cosmic Explorer' project.

### 1. The Bootstrapper (`setup_fresh.sh`)
- **Role**: Remote orchestrator.
- **Actions**:
  - Cleans previous installs.
  - Installs `git`.
  - Clones the target branch (default: `main`, but we will test with `backup/v2.1`).
  - Discovers AI Keys from environment.
  - Handoffs execution to the internal deploy script.

### 2. The Engine (`deploy.sh`)
- **Role**: System configurator (run as sudo).
- **Oracle 9 Specifics**:
  - **PackageManager**: Detects `dnf`.
  - **Security**: Disables `fapolicyd` (to allow custom venv binaries), configures `firewalld` for port **58921**.
  - **SELinux**: Whitelists Nginx relay and port 8000.
  - **SSL**: Auto-generates self-signed certs.
  - **AI**: Injects API keys into the Systemd service unit.

### 3. AI Environment Configuration
The scripts automatically detect and propagate the following variables from your shell to the system service:

| Variable | Description | Default / Source |
| :--- | :--- | :--- |
| **`GOOGLE_API_KEY`** | Primary key for Gemini Engine. | $GOOGLE_API_KEY or $GOOGLE_GEMINI_API_KEY |
| **`AI_PROVIDER`** | Override the default provider (e.g., `openai`, `openrouter`). | $AI_PROVIDER |
| **`OPENROUTER_API_KEY`** | Key for OpenRouter if using `AI_PROVIDER=openrouter`. | $OPENROUTER_API_KEY |
| **`AI_MODEL_OVERRIDE`** | Force a specific model ID (e.g., `gpt-4`). | $AI_MODEL_OVERRIDE |

> [!NOTE]
> The orchestrator (`setup_fresh.sh`) will discover these from your current shell session and pass them securely to the `deploy.sh` script, which then bakes them into `/etc/systemd/system/panchanga.service`.

### 4. Execution Standard
```bash
# 1. Export Keys in your shell (or .bashrc)
export GOOGLE_API_KEY="AIzaSy..."
# Optional:
export AI_PROVIDER="gemini"

# 2. Run the Bootstrapper
curl -O [URL_TO_SETUP_SCRIPT]
chmod +x setup_fresh.sh
./setup_fresh.sh backup/v2.1
```

## Proposed Changes


### 1. New Interactive 3D Visuals
We will create two new dedicated 3D visualization routes:

#### A. `/visuals/mayan-gears` (The Odometer)
- **Concept**: A 3D "Cryptex" style set of rotating stone rings using Three.js.
- **Interactivity**: Students can click/drag to rotate rings. A "Play" button speeds up time to show how the `Kin` (Day) ring drives the `Uinal` (Month) ring, demonstrating the Base-20 rollover (0-19).
- **Style**: Stone texture, glowing glyphs.

#### B. `/visuals/venus-cycle` (Path of Kukulkan)
- **Concept**: A Heliocentric 3D view focusing *only* on Earth and Venus.
- **Scientific Feature**: Visualizing the **Synodic Period**.
    - Show line connecting Earth and Venus.
    - Trace the "Pentagram of Venus" pattern formed every 8 years.
- **Interactivity**: Slider to scrub through the 584-day synodic cycle.

### 2. Content & Terminology Overhaul
- **Terminology**: Global find/replace "Maya" -> "Mayans" (e.g., "The Mayans calculated...").
- **Section 1 (Math)**: Add explanation of *why* Base-20 (fingers/toes). Add "Dot & Bar" notation chart.
- **Section 2 (Venus)**:
    - Define **"Synodic Period"**: *The time it takes for a planet to return to the same position relative to the Sun as seen from Earth.*
    - Explain "Morning Star" (Heliacal Rise) significance for Mayan warfare ("Star Wars").
    - **Fix Visual Bug**: Ensure the iframe points to the new `/visuals/venus-cycle` route, not the broken/generic one.

### 3. "The Time-Keeper's Challenge" Module
- **Action**: Replace the static text with a live **interactive quiz widget**.
- **Mechanic**: "Verify the Date".
    - The Guide shows a random Long Count (e.g., `13.0.12.0.0`).
    - Student must use a "Glyph Calculator" or choose the correct interpretation.
    - *Simpler MVP*: A **"Date Decoder"**. User enters their birthdate, and the module actively calculating their Long Count and Tzolkin sign with a breakdown of the math.
- **Success Criteria**: Correct calculation of Julian Day Number correlation (GMT 584283).

## Execution Steps

1.  **Scaffold Routes**: Add `/visuals/mayan-gears` and `/visuals/venus-cycle` to `app.py`.
2.  **Create Visual Templates**:
    - `templates/visuals/mayan_gears.html` (Three.js implementation).
    - `templates/visuals/venus_cycle.html` (Three.js implementation).
3.  **Update `guide.html`**:
    - Rewrite text content.
    - Embed new iframes.
    - Implement the "Time-Keeper's Challenge" container using JavaScript.
4.  **Verify**: Ensure no "Not Found" errors and visuals are responsive.
