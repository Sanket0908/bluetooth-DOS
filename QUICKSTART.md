# 🚀 Quick Start Guide - Bluetooth DOS Tool (macOS)

## ✅ Setup Complete!

All dependencies are installed. You're ready to go!

---

## 🎯 How to Run (3 Simple Steps)

### Step 1: Open Terminal and Navigate
```bash
cd "/Users/sanket/bluetooth DOS"
```

### Step 2: Run the Tool
```bash
python3 bluetooth_dos_macos.py
```

### Step 3: Use the Menu
Follow the on-screen menu to:
1. Scan for devices
2. Select targets
3. Launch attack
4. Stop when done

---

## 📱 Quick Example Workflow

```
1. Type: 1 [Enter]          → Scan for devices (wait 8 seconds)
2. Type: 2 [Enter]          → View discovered devices
3. Type: 3 [Enter]          → Attack specific device
   Enter: 1 [Enter]         → Attack device #1
4. Wait... (device will disconnect and become non-connectable)
5. Type: 6 [Enter]          → Stop all attacks
   Type: yes [Enter]        → Confirm
   
✓ Device is now reconnectable!
```

---

## 🎮 Menu Options Explained

- **Option 1** - Scan for nearby Bluetooth/BLE devices
- **Option 2** - Display list of found devices
- **Option 3** - Attack selected devices (enter: 1,2,3)
- **Option 4** - Attack ALL devices at once
- **Option 5** - Stop attacking specific devices
- **Option 6** - Stop ALL attacks (makes devices reconnectable)
- **Option 7** - Check Bluetooth system status
- **Option 8** - Exit program

---

## 💡 Tips

### For Better Results:
1. **Turn on Bluetooth** on target devices first
2. **Make devices discoverable** (pairing mode)
3. **Stay close** to target devices (within 10 meters)
4. **Use option 6** to stop all attacks and restore connectivity

### For Classic Bluetooth Attacks:
Install `blueutil` for enhanced functionality:
```bash
brew install blueutil
```

---

## 🎯 What Each Attack Does:

### BLE (Bluetooth Low Energy) Attack:
- Floods device with rapid connection requests
- Reads GATT characteristics repeatedly
- Exhausts device's connection handling
- Makes device unable to accept new connections

### Classic Bluetooth Attack:
- Sends repeated disconnect commands
- Overwhelms Bluetooth stack
- Forces device to drop connections
- Prevents new pairing attempts

---

## ⚠️ Important Notes

1. **Legal**: Only use on YOUR devices in YOUR space
2. **Permissions**: macOS may ask for Bluetooth permissions - click "Allow"
3. **Range**: Bluetooth range is typically 10-30 meters
4. **Stopping**: Simply stop the attack to restore device connectivity
5. **Educational**: This is for learning about Bluetooth security

---

## 🔧 Troubleshooting

### "Permission denied" or "Bluetooth access required"
→ Go to System Preferences → Security & Privacy → Bluetooth → Allow Terminal

### "No devices found"
→ Make sure target devices have Bluetooth ON and are discoverable
→ Try increasing scan duration
→ Move closer to devices

### "Module not found"
→ Run: `pip3 install bleak`

### Attack not working on Classic Bluetooth
→ Install blueutil: `brew install blueutil`

---

## 🏆 Success!

You're all set! Use responsibly and ethically.

**Remember**: With great power comes great responsibility.

