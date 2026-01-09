from abc import ABC, abstractmethod
import random
import time
import os

class NetworkDevice(ABC):
    def __init__(self, ip_address, location):
        self.ip_address = ip_address
        self.location = location
        self.is_status = False

    def connect(self):
        if not self.is_status:
            self.is_status = True
            print(f"\nDevice {self.ip_address} is now connected.")
        else:
            print(f"\nDevice {self.ip_address} is already connected.")

    def disconnect(self):
        if self.is_status:
            self.is_status = False
            print(f"\nDevice {self.ip_address} has been disconnected.")
        else:
            print(f"\nDevice {self.ip_address} is already disconnected.")

    def get_device_type(self):
        return self.__class__.__name__

    def show_info(self):
        status_str = "Connected" if self.is_status else "Disconnected"
        print_divider()
        print(f" Device Type : {self.get_device_type():<10}")
        print(f" IP Address  : {self.ip_address:<15}")
        print(f" Status      : {status_str:<10}")
        print(f" Location    : {self.location:<20}")
        print_divider()

    @abstractmethod
    def operate(self):
        pass

class Router(NetworkDevice):
    def authenticate(self):
        for attempt in range(3):
            print("\nEnter the router's login credentials:")
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            if username and password:
                print("\nLogin successful.")
                return True
            else:
                print("\nInvalid credentials. Please try again.")
        print("\nAuthentication failed after 3 attempts.")
        return False

    def configure(self):
        while True:
            response = input("\nWould you like to configure your WiFi network? (yes/no): ").strip().lower()
            if response == "yes":
                ssid = input("Enter WiFi network name (SSID): ").strip()
                wifi_password = input("Enter WiFi password: ").strip()
                if ssid and wifi_password:
                    print(f"\nWiFi network '{ssid}' has been successfully configured.")
                    return
                else:
                    print("\nInvalid input. Both SSID and password must be provided.")
            elif response == "no":
                print("\nSkipping WiFi configuration.")
                return
            else:
                print("\nInvalid choice. Please enter 'yes' or 'no'.")

    def operate(self):
        if self.is_status:
            print("\nTo operate the router, connect it to a modem and Ethernet.")
            if self.authenticate():
                self.configure()
                print(f"\nRouter at {self.ip_address} is now managing network traffic.")
        else:
            print("\nRouter is offline. Connect it first.")

class Modem(NetworkDevice):
    def authenticate(self):
        for attempt in range(3):
            print("\nEnter your ISP credentials:")
            account_id = input("ISP Account ID: ").strip()
            password = input("ISP Password: ").strip()
            if account_id and password:
                print("\nAuthenticated with ISP successfully.")
                return True
            else:
                print("\nInvalid credentials. Please try again.")
        print("\nAuthentication failed after 3 attempts.")
        return False

    def configure(self):
        while True:
            response = input("\nWould you like to set a bandwidth limit? (yes/no): ").strip().lower()
            if response == "yes":
                try:
                    bandwidth = int(input("Enter bandwidth limit (in Mbps): ").strip())
                    if bandwidth > 0:
                        print(f"\nBandwidth limit set to {bandwidth} Mbps.")
                        return
                    else:
                        print("\nBandwidth must be a positive number.")
                except ValueError:
                    print("\nInvalid input. Please enter a numeric value for bandwidth.")
            elif response == "no":
                print("\nSkipping bandwidth configuration.")
                return
            else:
                print("\nInvalid choice. Please enter 'yes' or 'no'.")

    def monitor_network(self):
        print("\nChecking signal strength... Signal is stable.")

    def operate(self):
        if self.is_status:
            if self.authenticate():
                self.configure()
                self.monitor_network()
                print(f"\nModem at {self.ip_address} is now handling internet traffic.")
        else:
            print("\nModem is offline. Connect it first.")

class Hub(NetworkDevice):
    def monitor_network(self):
        while True:
            response = input("\nWould you like to enable network traffic monitoring? (yes/no): ").strip().lower()
            if response == "yes":
                print("Network traffic monitoring enabled.")
                return
            elif response == "no":
                print("\nSkipping network monitoring.")
                return
            else:
                print("\nInvalid choice. Please enter 'yes' or 'no'.")

    def operate(self):
        if self.is_status:
            print("\nChecking connected devices...")
            connected_devices = [dev.ip_address for dev in devices if dev.is_status]
            if connected_devices:
                print(f"Devices connected to the hub: {', '.join(connected_devices)}")
                print("Broadcasting data to all connected devices.")
            else:
                print("\nNo devices connected to the hub.")
            self.monitor_network()
        else:
            print("\nHub is offline. Connect it first.")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_and_clear():
    input("\nPress Enter to return to main menu...")
    clear_screen()

def print_divider():
    print("-" * 75)

def show_menu():
    print_divider()
    print("Menu:")
    print("[1] - Add a device to connect to the Network.")
    print("[2] - Show Information of all Devices.")
    print("[3] - Connect a Device.")
    print("[4] - Disconnect a Device.")
    print("[5] - Operate a Device.")
    print("[6] - Check Ping of the Device (Simulated).")
    print("[7] - Exit")
    print_divider()

def validate_ip(ip_address):
    parts = ip_address.split(".")
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False

def ping_device():
    if not devices:
        clear_screen()
        print("\033[1mNo devices to ping.\033[0m")
        pause_and_clear()
        return
    ip = input("Enter the IP address to ping: ").strip()
    for device in devices:
        if device.ip_address == ip:
            if device.is_status:
                print("\nChecking Ping... please wait.")
                time.sleep(2)  
                time_ms = random.randint(1, 50)
                ttl = random.choice([32, 64, 128])
                print(f"\nReply from {ip}: bytes=32 time={time_ms}ms TTL={ttl}")
            else:
                print(f"\nDevice {ip} is offline. No response.")
            pause_and_clear()
            return
    print("\nNo device with that IP address.")
    pause_and_clear()

def get_device_type_input():
    device_types = {
        "1": Router,
        "2": Hub,
        "3": Modem
    }
    print("Select device type:")
    for number, device_class in device_types.items():
        print(f"[{number}] - {device_class.__name__}")
    choice = input("Enter the number corresponding to the device type: ").strip()
    clear_screen()
    return device_types.get(choice, None), device_types.get(choice, None).__name__ if choice in device_types else None

def operate_device():
    if not devices:
        clear_screen()
        print("\n\033[1mNo devices available to operate.\033[0m")
        pause_and_clear()
        return
    try:
        device_index = int(input("Select the device number to operate: ")) - 1
        if 0 <= device_index < len(devices):
            devices[device_index].operate()
        else:
            print("\nInvalid device number.")
    except ValueError:
        print("\nPlease enter a valid number.")

devices = []

clear_screen()
title = "WELCOME TO THE NETWORK ROOM"
print("-" * 75)
print(f"{title:^75}")

while True:
    show_menu()
    try:
        option = int(input("Select an option: "))
    except ValueError:
        clear_screen()
        print("\nInvalid input, please enter a number.")
        pause_and_clear()
        continue

    if option == 1:
        clear_screen()
        device_class, device_name = None, None
        while device_class is None:
            device_class, device_name = get_device_type_input()

        ip_address = input(f"Enter the IP address of the {device_name} [x.x.x.x]: ").strip()
        if not validate_ip(ip_address):
            clear_screen()
            print("\033[1mInvalid IP address format. Please enter a valid IPv4 address.\033[0m")
            pause_and_clear()
            continue

        location = ""
        while not location.strip():
            location = input(f"Enter the location of the {device_name}: ").strip()
            if not location:
                print("Location cannot be empty. Please enter a valid location.")

        clear_screen()

        device = device_class(ip_address, location)
        devices.append(device)
        print(f"\nDevice '{device_name}' added successfully:")
        device.show_info()
        pause_and_clear()

    elif option == 2:
        clear_screen()
        if not devices:
            print("\033[1mNo device(s) added yet.\033[0m")
        else:
            print("\nDevices Information:")
            for i, device in enumerate(devices, 1):
                print(f"\nDevice Number: [{i}]")
                device.show_info()
        pause_and_clear()

    elif option == 3:
        clear_screen()
        if not devices:
            print("\033[1mNo device(s) available to connect.\033[0m")
            pause_and_clear()
            continue
        try:
            for i, device in enumerate(devices, 1):
                print(f"| Device Number: [{i}] | Device Type: {device.get_device_type()} | IP Address: ({device.ip_address}) | Status: {'Connected' if device.is_status else 'Disconnected'} |")
            device_index = int(input("Select the device number to connect: ")) - 1
            if 0 <= device_index < len(devices):
                devices[device_index].connect()
            else:
                print("\nInvalid device number.")
        except ValueError:
            print("\nPlease enter a valid number.")
        pause_and_clear()

    elif option == 4:
        clear_screen()
        if not devices:
            print("\033[1mNo device(s) available to disconnect.\033[0m")
            pause_and_clear()
            continue
        try:
            for i, device in enumerate(devices, 1):
                print(f"| Device Number: [{i}] | Device Type: {device.get_device_type()} | IP Address: ({device.ip_address}) | Status: {'Connected' if device.is_status else 'Disconnected'} |")
            device_index = int(input("Select the device number to disconnect: ")) - 1
            if 0 <= device_index < len(devices):
                devices[device_index].disconnect()
            else:
                print("\nInvalid device number.")
        except ValueError:
            print("\nPlease enter a valid number.")
        pause_and_clear()

    elif option == 5:
        clear_screen()
        if not devices:
            print("\033[1mNo device(s) to Operate.\033[0m")
            pause_and_clear()
            continue
        print("\033[1mDevices Available:\033[0m")
        for i, device in enumerate(devices, 1):
            print(f"| Device Number: [{i}] | Device Type: {device.get_device_type()} | IP Address: ({device.ip_address}) | Status: {'Connected' if device.is_status else 'Disconnected'} |")
        operate_device()
        pause_and_clear()

    elif option == 6:
        clear_screen()
        if not devices:
            print("\033[1mNo device(s) to check the ping.\033[0m")
            pause_and_clear()
            continue
        print("\033[1mDevices Available:\033[0m")
        for i, device in enumerate(devices, 1):
            print(f"| Device Number: [{i}] | Device Type: {device.get_device_type()} | IP Address: ({device.ip_address}) | Status: {'Connected' if device.is_status else 'Disconnected'} |")
        ping_device()

    elif option == 7:
        print("\n\033[1mThe Program was Terminated.\033[0m")
        break

    else:
        clear_screen()
        print("\033[1mInvalid option. Please try again.\033[0m")
        pause_and_clear()

