# Linux Bluetooth Scanning Troubleshooting Guide

## 🔴 Problem: Not Finding Devices on Linux

If the Linux version isn't finding devices but macOS is, here are the solutions:

---

## ✅ Quick Fix Commands (Run These First!)

Copy and paste these commands on your Chromebook/Linux:

```bash
# 1. Restart Bluetooth service
sudo systemctl restart bluetooth

# 2. Power on the Bluetooth adapter
sudo hciconfig hci0 up

# 3. Enable scanning
sudo hciconfig hci0 piscan

# 4. Test with bluetoothctl
bluetoothctl power on
bluetoothctl scan on
# Wait 10 seconds, then:
bluetoothctl devices
bluetoothctl scan off
```

**Then try running the tool again:**
```bash
sudo python3 bluetooth_dos_linux.py
```

---

## 🔍 Why This Happens

### macOS vs Linux Difference:

| Feature | macOS (Bleak) | Linux (hcitool) |
|---------|---------------|-----------------|
| BLE Advertising | ✅ Finds devices | ❌ Limited |
| Discoverable mode | Not required | **REQUIRED** |
| Scan method | High-level API | Raw HCI |
| Permissions | User-level | Needs root |

**Key Issue:** `hcitool` only finds devices in **discoverable/pairing mode**, while macOS/Bleak finds devices that are just advertising (like your CMF Buds when not in pairing mode).

---

## 🎯 Solution: Put Devices in Discoverable Mode

### For Bluetooth Speakers:
1. **Turn on the speaker**
2. **Press and HOLD the Bluetooth button** (usually 3-5 seconds)
3. **Wait for blinking light** (indicates pairing/discoverable mode)
4. **NOW scan** with the tool

### For CMF Buds/Earbuds:
1. **Put buds in charging case**
2. **Press and hold the button on case** (5 seconds)
3. **Light should blink** (pairing mode)
4. **NOW scan** with the tool

### For Phones:
1. **Go to Settings → Bluetooth**
2. **Make sure Bluetooth is ON**
3. **Stay on the Bluetooth settings page** (makes it discoverable)
4. **NOW scan** with the tool

---

## 🛠️ Step-by-Step Troubleshooting

### Step 1: Check Bluetooth Adapter

```bash
# Check if adapter exists
hciconfig

# Expected output:
# hci0:	Type: Primary  Bus: USB
# 	BD Address: XX:XX:XX:XX:XX:XX  ACL MTU: 1021:8  SCO MTU: 64:1
# 	UP RUNNING
```

**If you see "DOWN":**
```bash
sudo hciconfig hci0 up
```

**If "hci0" doesn't exist:**
```bash
# Check USB Bluetooth
lsusb | grep -i bluetooth

# Check Bluetooth service
sudo systemctl status bluetooth
```

---

### Step 2: Test Bluetooth Service

```bash
# Check service status
sudo systemctl status bluetooth

# If not running:
sudo systemctl start bluetooth

# Enable on boot
sudo systemctl enable bluetooth
```

---

### Step 3: Manual Scan Test

Try manual scanning to see if it's a tool issue or system issue:

```bash
# Test 1: bluetoothctl (modern, works best)
bluetoothctl
# Inside bluetoothctl:
power on
scan on
# Wait 10 seconds
devices
scan off
exit

# Test 2: hcitool classic scan
sudo hcitool scan

# Test 3: BLE scan (deprecated but sometimes works)
sudo timeout 8 hcitool lescan
```

**If these don't find devices either:**
- Your devices aren't in discoverable mode
- Bluetooth adapter issue
- Interference/range issue

**If these DO find devices:**
- The tool has a bug (use improved version)

---

### Step 4: Check Permissions

```bash
# Make sure you're running with sudo
sudo python3 bluetooth_dos_linux.py

# Check your user is in bluetooth group
groups | grep bluetooth

# If not, add yourself:
sudo usermod -a -G bluetooth $USER
# Then log out and log back in
```

---

## 🚀 Updated Tool (Better Scanning)

I've updated `bluetooth_dos_linux.py` with improved scanning that:
- ✅ Uses `bluetoothctl` (more reliable)
- ✅ Automatically powers on adapter
- ✅ Falls back to `hcitool` if needed
- ✅ Shows troubleshooting tips if no devices found

**Transfer the updated file to your Chromebook and try again!**

---

## 📊 Comparison: What Each Method Finds

### bluetoothctl (BEST):
```bash
bluetoothctl scan on
```
✅ Finds BLE devices advertising  
✅ Finds Classic Bluetooth in discoverable mode  
✅ Modern and maintained  
✅ Works on most Linux systems  

### hcitool scan (LIMITED):
```bash
sudo hcitool scan
```
✅ Finds Classic Bluetooth in discoverable mode  
❌ Doesn't find BLE devices  
❌ Deprecated  
⚠️ Only works if device is actively discoverable  

### hcitool lescan (DEPRECATED):
```bash
sudo hcitool lescan
```
✅ Finds some BLE devices  
❌ Deprecated, may not work  
❌ Requires root  
⚠️ Unreliable  

---

## 🎯 Recommended Workflow

### Before Running the Tool:

1. **Prepare your test device (speaker/earbuds):**
   - Turn it on
   - Put in **PAIRING MODE** (blinking light)
   - Keep it close (2-3 meters)

2. **Prepare Linux/Chromebook:**
   ```bash
   sudo systemctl restart bluetooth
   sudo hciconfig hci0 up
   ```

3. **Run the updated tool:**
   ```bash
   sudo python3 bluetooth_dos_linux.py
   ```

4. **Select option 1** (Scan)

5. **Wait for scan to complete**

6. **You should now see your device!**

---

## 🔧 Common Issues & Fixes

### Issue: "hci0: No such device"
```bash
# Check if Bluetooth hardware exists
lsusb | grep -i bluetooth
rfkill list bluetooth

# If blocked:
sudo rfkill unblock bluetooth
```

### Issue: "Operation not permitted"
```bash
# Always use sudo
sudo python3 bluetooth_dos_linux.py
```

### Issue: Finds devices but can't attack
```bash
# Some devices have DOS protection
# Try different devices
# Make sure device is close enough
```

### Issue: "bluetoothctl: command not found"
```bash
# Install BlueZ
sudo apt-get update
sudo apt-get install bluez bluetooth
```

---

## 🎓 For Chromebook Specifically

### Chromebook-Specific Issues:

1. **Linux container might not have Bluetooth access**
   
   Fix:
   ```bash
   # Check if Bluetooth is available in container
   ls /dev/hci*
   
   # If not, you may need to enable it in Chromebook settings
   # Settings → Linux → Develop Android apps → Enable Bluetooth
   ```

2. **Bluetooth might be controlled by Chrome OS**
   
   Workaround:
   - Make sure Chrome OS Bluetooth is ON
   - Disconnect any connected devices in Chrome OS
   - Then use Linux tools

3. **Permissions in container**
   
   ```bash
   # Run with sudo (always)
   sudo python3 bluetooth_dos_linux.py
   ```

---

## 🎬 Demo-Ready Checklist

To ensure devices are found during your presentation:

- [ ] Speaker is in **PAIRING MODE** (blinking light)
- [ ] Speaker is **CLOSE** (within 3 meters)
- [ ] Chrome OS Bluetooth is **ON**
- [ ] Linux Bluetooth service is **RUNNING**
- [ ] Adapter is **POWERED ON** (`hciconfig hci0 up`)
- [ ] Running tool with **SUDO**
- [ ] Using **UPDATED** version of the tool
- [ ] Tested before presentation!

---

## 💡 Pro Tips

1. **Test the night before your presentation**
   - Don't wait until the last minute
   - Make sure scanning works reliably

2. **Have a backup plan**
   - Record a video of it working
   - Show that as backup if live demo fails

3. **Use a cheap Bluetooth speaker**
   - More reliable than earbuds for demos
   - Bigger buttons, easier to put in pairing mode
   - Visual indicator (blinking light)

4. **Scan multiple times**
   - First scan might not find everything
   - Let it run for 15-20 seconds

5. **Keep device close**
   - 2-3 meters max during demo
   - Reduces interference issues

---

## 🔬 Debug Script

Run this to diagnose your setup:

```bash
# Save this as bluetooth_debug.sh
#!/bin/bash

echo "=== Bluetooth Diagnostic ==="
echo ""

echo "1. Bluetooth Service:"
sudo systemctl status bluetooth | grep Active

echo ""
echo "2. Bluetooth Adapter:"
hciconfig

echo ""
echo "3. RF Kill Status:"
rfkill list bluetooth

echo ""
echo "4. Bluetooth Tools:"
which bluetoothctl
which hcitool

echo ""
echo "5. Quick Scan Test:"
timeout 5 sudo hcitool scan

echo ""
echo "=== End Diagnostic ==="
```

---

## ✅ Final Checklist

If you've done all this and still no devices:

1. ✅ Bluetooth service running?
2. ✅ Adapter powered on?
3. ✅ Using sudo?
4. ✅ Target device in pairing mode?
5. ✅ Target device close enough?
6. ✅ Using updated scanning code?
7. ✅ Manual `bluetoothctl` scan works?

If all YES but still no devices in tool:
- Try the manual `bluetoothctl` commands
- Copy the MAC addresses manually
- Or use the improved version I created

---

**Bottom Line:** The main issue is devices need to be in **DISCOVERABLE/PAIRING MODE** on Linux, unlike macOS which can find devices just advertising. Put your speaker in pairing mode and it will work!

