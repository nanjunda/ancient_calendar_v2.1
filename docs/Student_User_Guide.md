# 🌌 Application User Manual (v6.0.1)

**Welcome to the Ancient Calendars Platform.**
This manual provides functional instructions for navigating and utilizing the application's features, including the Conversion Engine, Co-Pilot Sky Map, and the AI Maestro.

---

## 🛠️ Core Workflows

### 1. Generating a Calendar Conversion
The primary function is converting Gregorian dates to ancient timekeeping systems.
1.  **Select Civilization**: Choose between **Hindu Panchanga** or **Mayan Chronology** from the home screen.
2.  **Input Details**:
    *   **Date & Time**: Enter the exact historical or future moment.
    *   **Location**: Enter the city (calculation builds a geodetic vector).
3.  **Generate**: Click "Calculate". The system processes the orbital vectors and renders the **Panchanga Insights** dashboard.

### 2. The "Co-Pilot" Sky Map Integration
We use a professional-grade external visualizer (Stellarium Web) in a **Co-Pilot Mode**.

**How to Launch:**
1.  Look for buttons labeled `🔭 Open Sky Map: [Target Name]` (e.g., "Moon", "Jyeshtha").
2.  **Click the Button**:
    *   **Toast Notification**: A black popup appears at the bottom of the screen. Read it! It tells you exactly what to search for.
    *   **New Tab**: The application opens **Stellarium Web** in a new browser tab.
3.  **In the New Tab**:
    *   Click the **Spyglass Icon** (Search) at the top.
    *   Type the name shown in the Toast notification.
    *   Stellarium will fly to that object in the 3D sky.

> **Why this way?** This "Dual-Window" approach gives you the full power of a desktop planetarium without slowing down your insights report.

### 3. The Chat with Maestro (AI Assistant)
The **Lead Educator (Maestro)** is an AI companion available to explain the data.

**How to Use:**
1.  **Locate the Widget**: Look for the floating **✨ (Sparkle)** button in the bottom-right corner of the Insights page.
2.  **Toggle**: Click to open the chat window.
3.  **Ask Questions**:
    *   *Functional*: "What does 'Tithi' mean?"
    *   *Contextual*: "Why is the Moon in Jyeshtha today?"
4.  **Loading**: The AI will display "Consulting the Sages..." while it processes your query using the specific astronomical data of the current page.

---

## 🔬 Dashboard Features

### The Time Machine (Birthday Drift)
Located in the "Cosmic Identity Card" section.
*   **Slider**: Drag the slider from 1950 to 2100.
*   **Visual**: The bar shows the delta between the Solar Year and Lunar Year.
*   **Purpose**: Demonstrates why your "Star Birthday" (Nakshatra Birthday) drifts relative to your Gregorian Birthday until a Leap Month resets it.

### The Educational Modules (Student Guide)
Access the **Student Guide** from the top navigation bar.
*   **Interactive Visuals**: Click on terms like "Precession" to see 3D animations of the Earth's wobble.
*   **Audio Narration**: Click "Listen to Maestro" for a voice-over summary of the lesson.

---

## ⚙️ Troubleshooting

**"The Sky Map didn't open."**
*   Check your browser's **Pop-up Blocker**. You must allow pop-ups for this site to launch the Co-Pilot window.

**"The Chatbot isn't responding."**
*   Ensure you have an active internet connection. The AI requires a live link to the inference engine (OpenRouter/Gemini).

---
*Version 6.0.1 | Powered by NASA JPL Ephemerides*
