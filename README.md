# Bluetooth DOS Tool - Educational Project

⚠️ **WARNING: This tool is for EDUCATIONAL PURPOSES ONLY**

This Bluetooth DOS (Denial of Service) tool is designed for learning about Bluetooth security vulnerabilities and should **ONLY** be used on devices you own in a controlled environment.

## ⚖️ Legal Disclaimer

- **Unauthorized access** to Bluetooth devices is **ILLEGAL** in most countries
- This tool should only be used for:
  - Educational purposes
  - Security research on your own devices
  - Penetration testing with explicit written permission
- The author assumes **NO LIABILITY** for misuse of this tool
- You are **SOLELY RESPONSIBLE** for compliance with local laws

## Features

✅ Scan for nearby Bluetooth devices  
✅ Display discovered devices with MAC addresses and names  
✅ Multiple attack types:
  - L2CAP Flood (fast connection flooding)
  - RFCOMM Flood (comprehensive channel flooding)
  - Hybrid Attack (both methods simultaneously)  
✅ Select individual devices or attack all at once  
✅ Start and stop attacks on demand  
✅ Real-time attack status monitoring  

## Requirements

- Python 3.6+
- macOS, Linux, or Windows with Bluetooth adapter
- PyBluez library
- Root/Administrator privileges (may be required)

## Installation

### macOS

1. Install Xcode Command Line Tools:
```bash
xcode-select --install
```

2. Install PyBluez dependencies:
```bash
brew install python3
```

3. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

### Linux (Ubuntu/Debian)

1. Install system dependencies:
```bash
sudo apt-get update
sudo apt-get install python3-dev libbluetooth-dev
```

2. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

### Windows

1. Install Python 3 from [python.org](https://www.python.org)

2. Install Microsoft Visual C++ Build Tools

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the tool (may require sudo on Unix systems):

```bash
python3 bluetooth_dos.py
```

Or with elevated privileges:

```bash
sudo python3 bluetooth_dos.py
```

### Step-by-Step Guide

1. **Scan for devices:**
   - Select option `1` from the menu
   - Wait for scan to complete (default: 8 seconds)
   - Discovered devices will be stored

2. **View discovered devices:**
   - Select option `2` to display all found devices
   - Note the device numbers you want to target

3. **Start attack on specific devices:**
   - Select option `3`
   - Enter device numbers separated by commas (e.g., `1,3,5`)
   - Choose attack type:
     - `1` - L2CAP Flood (fast, less intensive)
     - `2` - RFCOMM Flood (comprehensive, more channels)
     - `3` - Hybrid (recommended, uses both methods)
   - Attack will start in background threads

4. **Attack all devices:**
   - Select option `4`
   - Confirm by typing `yes`
   - Choose attack type
   - All discovered devices will be attacked simultaneously

5. **Stop specific attacks:**
   - Select option `5`
   - Enter device numbers to stop attacking

6. **Stop all attacks:**
   - Select option `6`
   - Confirm by typing `yes`
   - All active attacks will be terminated

### Quick Commands

To **make devices reconnectable**, simply stop the attack:
- The devices will naturally return to normal connectable state once the DOS attack stops
- No special "restore" command needed - just stop the attack (option 5 or 6)

## How It Works

### Attack Mechanisms

1. **L2CAP Flood:**
   - Sends rapid connection requests on L2CAP protocol layer
   - Overwhelms device's connection handling capability
   - Uses multiple PSM (Protocol/Service Multiplexer) values
   - Fast and resource-efficient

2. **RFCOMM Flood:**
   - Floods RFCOMM (Bluetooth serial) channels
   - Attempts connections on channels 1-30
   - More comprehensive coverage
   - Targets application layer services

3. **Hybrid Attack:**
   - Combines both L2CAP and RFCOMM methods
   - Runs attacks in parallel threads
   - Most effective for maximum disruption
   - Recommended for best results

### Technical Details

- **Connection Flooding:** Creates numerous Bluetooth socket connections rapidly
- **Resource Exhaustion:** Overwhelms target device's Bluetooth stack
- **Timeout Management:** Uses short timeouts to maximize packet rate
- **Multi-threading:** Each device attack runs in separate thread for parallel execution

## Troubleshooting

### "Permission denied" errors
- Run with `sudo` on Unix systems
- Ensure Bluetooth adapter has proper permissions

### "PyBluez not installed"
```bash
pip3 install pybluez
```

### No devices found
- Ensure target devices have Bluetooth enabled and are discoverable
- Increase scan duration
- Move closer to target devices
- Check if your Bluetooth adapter is working: `hcitool dev` (Linux)

### macOS specific issues
If PyBluez installation fails on macOS:
```bash
brew install pkg-config
export PKG_CONFIG_PATH="/usr/local/opt/openssl/lib/pkgconfig"
pip3 install pybluez
```

### Attack not effective
- Try different attack types
- Ensure devices are in range
- Some devices have DOS protection mechanisms
- Modern devices may be more resilient

## Educational Value

This project demonstrates:
- Bluetooth protocol vulnerabilities
- Connection flooding attacks
- Security implications of wireless protocols
- Importance of Bluetooth security measures
- Need for proper authentication and rate limiting

## Ethical Guidelines

✅ **DO:**
- Use on your own devices only
- Use in controlled, isolated environments
- Document findings for educational purposes
- Understand the technology and implications

❌ **DON'T:**
- Target devices you don't own
- Use in public spaces
- Disrupt critical services
- Ignore local laws and regulations

## Prevention & Defense

To protect against such attacks:
- Keep Bluetooth disabled when not in use
- Use Bluetooth in "non-discoverable" mode
- Keep device firmware updated
- Implement connection rate limiting
- Use strong authentication mechanisms

## References

- [Bluetooth Core Specification](https://www.bluetooth.com/specifications/bluetooth-core-specification/)
- [PyBluez Documentation](https://github.com/pybluez/pybluez)
- [OWASP Bluetooth Security](https://owasp.org/www-community/vulnerabilities/Bluetooth_Vulnerabilities)

## License

This project is for educational purposes only. Use responsibly and ethically.

## Support

For educational inquiries or issues with the tool, please ensure you're using it in an appropriate context.

---

**Remember: With great power comes great responsibility. Use this knowledge to improve security, not to cause harm.**

