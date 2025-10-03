#!/bin/bash
# Bluetooth Troubleshooting Script for Linux/Chromebook

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     Bluetooth Troubleshooting & Test Script              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

echo "[1/6] Checking Bluetooth service status..."
sudo systemctl status bluetooth | head -5

echo ""
echo "[2/6] Checking Bluetooth adapter status..."
hciconfig -a

echo ""
echo "[3/6] Powering on Bluetooth adapter..."
sudo hciconfig hci0 up
sudo hciconfig hci0 piscan

echo ""
echo "[4/6] Testing with bluetoothctl scan..."
echo "Scanning for 5 seconds..."
timeout 5 bluetoothctl scan on &
sleep 6
bluetoothctl devices

echo ""
echo "[5/6] Testing with hcitool..."
timeout 8 sudo hcitool scan

echo ""
echo "[6/6] Testing BLE scan..."
timeout 5 sudo hcitool lescan

echo ""
echo "✅ Troubleshooting complete!"
