import socket
import os
from config import TRANSFER_PORT, BUFFER_SIZE
from discovery import Discovery

class Sender:
    def __init__(self, sender_name):
        self.sender_name = sender_name

    def start(self):
        print("Scanning for available devices...")
        devices = Discovery.scan_receivers(timeout=5)

        if not devices:
            print("No devices found on the network.")
            return

        print("\nDevices found:")
        device_list = list(devices.items())
        for idx, (ip, name) in enumerate(device_list):
            print(f"{idx + 1}. {name} ({ip})")

        try:
            choice = int(input("Select a device to send file to (number): ")) - 1
            target_ip, target_name = device_list[choice]
        except (IndexError, ValueError):
            print("Invalid selection.")
            return

        filepath = input("Enter full path to the file to send: ").strip()
        if not os.path.isfile(filepath):
            print("File not found.")
            return

        filename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                print(f"Connecting to {target_name} at {target_ip}:{TRANSFER_PORT}...")
                sock.connect((target_ip, TRANSFER_PORT))

                metadata = f"{self.sender_name}|{filename}|{filesize}"
                sock.send(metadata.encode())

                response = sock.recv(BUFFER_SIZE).decode()
                if response != "ACCEPT":
                    print("Transfer rejected by receiver.")
                    return

                print("Sending file...")
                with open(filepath, 'rb') as f:
                    while chunk := f.read(BUFFER_SIZE):
                        sock.sendall(chunk)

                print("File sent successfully.")
        except Exception as e:
            print(f"Error sending file: {e}")
