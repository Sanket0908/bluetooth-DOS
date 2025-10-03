#!/bin/bash
#
# Bluetooth DOS Tool - Chromebook Linux Setup Script
# Run this on your Chromebook to set up everything automatically
#

echo "╔══════════════════════════════════════════════════════════╗"
echo "║   Bluetooth DOS Tool - Chromebook Setup                 ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Update package lists
echo "[1/4] Updating package lists..."
sudo apt-get update

# Install Bluetooth tools and dependencies
echo "[2/4] Installing Bluetooth tools and Python dependencies..."
sudo apt-get install -y bluez bluetooth python3 python3-pip python3-dev libbluetooth-dev

# Check if Bluetooth is available
echo "[3/4] Checking Bluetooth adapter..."
if command -v hciconfig &> /dev/null; then
    echo "✅ Bluetooth tools installed successfully"
    hciconfig
else
    echo "⚠️  hciconfig not found, trying alternative..."
    sudo systemctl status bluetooth
fi

# Install Python dependencies (if requirements.txt exists)
if [ -f "requirements.txt" ]; then
    echo "[4/4] Installing Python packages..."
    pip3 install -r requirements.txt
else
    echo "[4/4] No requirements.txt found, skipping Python packages..."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the tool, use:"
echo "  sudo python3 bluetooth_dos_linux.py"
echo ""
echo "⚠️  Remember: Only test on YOUR OWN devices!"
echo ""

