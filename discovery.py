import socket
import threading
import time
from config import DISCOVERY_PORT

class Discovery:
    BROADCAST_ADDR = '<broadcast>'
    BROADCAST_INTERVAL = 1  

    @staticmethod
    def broadcast_presence(name, stop_event):
        """
        Receiver-side:
        Periodically broadcasts presence on the LAN with device name.
        Format: P2PDEVICE|<name>
        """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            message = f"P2PDEVICE|{name}"

            while not stop_event.is_set():
                s.sendto(message.encode(), (Discovery.BROADCAST_ADDR, DISCOVERY_PORT))
                time.sleep(Discovery.BROADCAST_INTERVAL)

    @staticmethod
    def scan_receivers(timeout=3):
        """
        Sender-side:
        Listens for UDP broadcast messages and returns discovered devices.
        Output: {ip: name}
        """
        found = {}
        start_time = time.time()

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', DISCOVERY_PORT))
            s.settimeout(0.5)

            while time.time() - start_time < timeout:
                try:
                    data, addr = s.recvfrom(1024)
                    decoded = data.decode()

                    if decoded.startswith("P2PDEVICE|"):
                        name = decoded.split("|", 1)[1]
                        ip = addr[0]
                        found[ip] = name
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"⚠️ Discovery error: {e}")
        return found
