#!/bin/bash
#
# POWERFUL Bluetooth DOS - Chromebook Complete Setup Script
# Run this ONCE on your Chromebook to set up everything
#

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  POWERFUL Bluetooth DOS - Chromebook Setup              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "This script will:"
echo "  1. Install all required packages"
echo "  2. Configure Bluetooth adapter"
echo "  3. Test Bluetooth functionality"
echo "  4. Prepare system for attacks"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

# Update package lists
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[1/6] Updating package lists..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
sudo apt-get update

# Install Bluetooth tools
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[2/6] Installing Bluetooth tools..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
sudo apt-get install -y bluez bluetooth

# Install Python
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[3/6] Installing Python..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
sudo apt-get install -y python3 python3-pip

# Restart Bluetooth service
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[4/6] Configuring Bluetooth service..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
sudo systemctl enable bluetooth
sudo systemctl restart bluetooth
sleep 2

# Power on adapter
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[5/6] Powering on Bluetooth adapter..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
sudo hciconfig hci0 down
sleep 1
sudo hciconfig hci0 up
sudo bluetoothctl power on

# Test installation
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[6/6] Testing installation..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "Checking installed tools:"
echo -n "  ✓ bluetoothctl: "
which bluetoothctl
echo -n "  ✓ hcitool: "
which hcitool
echo -n "  ✓ l2ping: "
which l2ping
echo -n "  ✓ sdptool: "
which sdptool
echo -n "  ✓ python3: "
which python3

echo ""
echo "Bluetooth adapter status:"
hciconfig

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SETUP COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo ""
echo "  1. Put your Bluetooth speaker in PAIRING MODE"
echo "     (Hold Bluetooth button until light blinks)"
echo ""
echo "  2. Run the tool:"
echo "     sudo python3 bluetooth_dos_chromebook.py"
echo ""
echo "  3. Select option 1 to scan"
echo ""
echo "  4. Select option 3 to attack"
echo ""
echo "  5. Watch your speaker disconnect! 🔥"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "⚠️  IMPORTANT:"
echo "   - Only attack YOUR devices"
echo "   - Speaker MUST be in pairing mode (blinking light)"
echo "   - Keep speaker close (within 2 meters)"
echo ""
echo "Good luck! 🚀"
echo ""

