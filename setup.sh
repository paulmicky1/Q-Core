#!/bin/bash

echo "================================================="
echo "      INSTALLING Q-CORE AI - PLEASE WAIT"
echo "================================================="

# 1. Ask for Sudo (Admin) password immediately to handle installs
sudo -v

# 2. Install System Audio Drivers (Required for Voice)
echo "[*] Installing Audio Drivers (Microphone + Speaker)..."
sudo apt update -y
sudo apt install -y espeak-ng portaudio19-dev python3-pyaudio curl

# 3. Install Ollama (The AI Engine) if not present
if ! command -v ollama &> /dev/null
then
    echo "[*] Installing Ollama AI Engine..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "[*] Ollama is already installed."
fi

# 4. Download the Brain (Phi-3)
echo "[*] Downloading Neural Network Model (Phi-3)..."
echo "    (This may take a few minutes based on internet speed)"
ollama pull phi3

# 5. Set Permissions for Q-Core
echo "[*] Setting up executable permissions..."
chmod +x Q-Core

# 6. Create Desktop Shortcut
USER_HOME=$(eval echo ~$SUDO_USER)
ICON_PATH="$PWD/q_icon.png"
EXEC_PATH="$PWD/Q-Core"

echo "[Desktop Entry]
Version=1.0
Name=Q-Core AI
Comment=Quantum Enhanced Assistant
Exec=$EXEC_PATH
Icon=$ICON_PATH
Terminal=true
Type=Application
Categories=Utility;AI;" > "$USER_HOME/.local/share/applications/q-core.desktop"

echo "================================================="
echo "      INSTALLATION COMPLETE!"
echo "      Search for 'Q-Core' in your app menu."
echo "================================================="
