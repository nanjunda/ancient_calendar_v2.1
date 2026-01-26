#!/bin/bash

# =================================================================
# Ancient Calendars v2.0 Headless - Oracle Linux 9 Orchestrator
# =================================================================

# Exit on any error
set -e

REPO_URL="https://github.com/nanjunda/ancient_calendar_v2.1.git"
INSTALL_BASE="/tmp"
INSTALL_DIR="$INSTALL_BASE/ancient_calendars_v2.0"
APP_NAME="ancient_calendar_v2.1"
# Default to v2.0 main branch
BRANCH=${1:-"main"}

echo "🌌 Starting Fresh Installation of Hindu Panchanga..."
echo "🌿 Target Branch: $BRANCH"

# --- Bulletproof Environment Discovery ---
# 1. Capture from Shell (Priority)
# 2. Support for aliases
export GOOGLE_API_KEY="${GOOGLE_API_KEY:-$GOOGLE_GEMINI_API_KEY}"
export AI_PROVIDER="${AI_PROVIDER}"
export OPENROUTER_API_KEY="${OPENROUTER_API_KEY}"
export AI_MODEL_OVERRIDE="${AI_MODEL_OVERRIDE}"

echo "🤖 AI Engine Discovery Results:"
[ -n "$GOOGLE_API_KEY" ] && echo "   ✅ Google Gemini Key: DETECTED"    || echo "   ⚪ Google Gemini Key: MISSING"
[ -n "$OPENROUTER_API_KEY" ] && echo "   ✅ OpenRouter Key:    DETECTED" || echo "   ⚪ OpenRouter Key:    MISSING"
[ -n "$AI_PROVIDER" ] && echo "   🎯 AI Provider:       ${AI_PROVIDER:-'Auto-Detect'}"
[ -n "$AI_MODEL_OVERRIDE" ] && echo "   🚀 AI Model Override: ${AI_MODEL_OVERRIDE:-'Default'}"

if [ -z "$GOOGLE_API_KEY" ] && [ -z "$OPENROUTER_API_KEY" ]; then
    echo "💡 TIP: If keys are set in your shell but not detected here, run:"
    echo "   export OPENROUTER_API_KEY=\"your_key\"; bash <(curl -L [URL])"
fi

# 1. Clean up old installer traces
if [ -d "$INSTALL_DIR" ]; then
    echo "🧹 Removing previous installation traces..."
    sudo rm -rf "$INSTALL_DIR"
fi

# 2. Create and enter temporary staging dir
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"
echo "📂 Working in: $(pwd)"

# 3. Ensure Git is installed
echo "📦 Ensuring Git is present..."
if command -v dnf &> /dev/null; then
    sudo dnf install -y git-core
else
    sudo apt-get update && sudo apt-get install -y git
fi

# 4. Clone the specific branch
echo "🏎️  Cloning Codebase ($BRANCH)..."
git clone -b "$BRANCH" "$REPO_URL"

# 5. Execute the core deployment script
# Use absolute paths to avoid any "not found" ambiguities
DEPLOY_PATH="$INSTALL_DIR/$APP_NAME/deploy.sh"

if [ ! -f "$DEPLOY_PATH" ]; then
    echo "❌ Error: Could not find deploy.sh at $DEPLOY_PATH"
    exit 1
fi

echo "🚀 Launching Deployment Engine..."
echo "📍 Transitioning to: $INSTALL_DIR/$APP_NAME"
cd "$INSTALL_DIR/$APP_NAME"

# Ensure deploy script is executable
chmod +x deploy.sh

# Pass the current environment's GOOGLE_API_KEY if it exists
# 6. Handle AI Configuration (Pre-flight)
if [ -z "$GOOGLE_API_KEY" ] && [ -z "$OPENROUTER_API_KEY" ]; then
    echo "⚠️  No AI API keys found in environment."
    read -p "🔑 Please enter your Google Gemini API Key (or leave blank to configure later): " GOOGLE_API_KEY
    export GOOGLE_API_KEY="$GOOGLE_API_KEY"
    echo "✅ Key received."
fi

# Pass the key explicitly to the deployment script
echo "🚢 Handing off to deploy.sh..."
sudo GOOGLE_API_KEY="$GOOGLE_API_KEY" \
     AI_PROVIDER="$AI_PROVIDER" \
     AI_MODEL_OVERRIDE="$AI_MODEL_OVERRIDE" \
     OPENROUTER_API_KEY="$OPENROUTER_API_KEY" \
     bash ./deploy.sh


echo "================================================================="
echo "✅ SUCCESS! Ancient Calendars v2.0 (Headless Edition) is now installed."
echo "🌍 Access at: https://$PUBLIC_IP:58921"
echo "📘 The API v2 Contract is documented in the docs/ folder."
echo "================================================================="
