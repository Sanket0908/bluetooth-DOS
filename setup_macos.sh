#!/bin/bash

# Setup script for macOS
# This script installs dependencies for the Bluetooth DOS tool

echo "=========================================="
echo "Bluetooth DOS Tool - macOS Setup"
echo "=========================================="
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "[!] Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "[+] Homebrew is already installed"
fi

# Check if Xcode Command Line Tools are installed
if ! xcode-select -p &> /dev/null; then
    echo "[!] Installing Xcode Command Line Tools..."
    xcode-select --install
    echo "[*] Please complete the Xcode installation and run this script again"
    exit 1
else
    echo "[+] Xcode Command Line Tools are installed"
fi

# Install Python3 if not present
if ! command -v python3 &> /dev/null; then
    echo "[!] Installing Python 3..."
    brew install python3
else
    echo "[+] Python 3 is already installed"
fi

# Install pkg-config (needed for PyBluez)
echo "[*] Installing pkg-config..."
brew install pkg-config

# Set PKG_CONFIG_PATH for OpenSSL
export PKG_CONFIG_PATH="/usr/local/opt/openssl/lib/pkgconfig"

# Install Python dependencies
echo "[*] Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if installation was successful
if python3 -c "import bluetooth" 2>/dev/null; then
    echo ""
    echo "=========================================="
    echo "[+] Setup completed successfully!"
    echo "=========================================="
    echo ""
    echo "To run the tool:"
    echo "  python3 bluetooth_dos.py"
    echo ""
    echo "Or with elevated privileges:"
    echo "  sudo python3 bluetooth_dos.py"
    echo ""
else
    echo ""
    echo "[!] Setup completed with warnings"
    echo "[!] PyBluez may not be properly installed"
    echo "[!] Try running: pip3 install pybluez"
fi

