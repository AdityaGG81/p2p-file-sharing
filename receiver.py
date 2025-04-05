import socket
import threading
import os
from config import TRANSFER_PORT, BUFFER_SIZE
from discovery import Discovery

class Receiver:
    def __init__(self, name):
        self.name = name
        self.stop_discovery = threading.Event()

    def start(self):
        # Start broadcasting presence on LAN
        threading.Thread(
            target=Discovery.broadcast_presence,
            args=(self.name, self.stop_discovery),
            daemon=True
        ).start()

        print(f"Receiver '{self.name}' is ready to accept files.")
        self._listen_for_files()

    def _listen_for_files(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(('', TRANSFER_PORT))
            server.listen(5)
            print(f"Listening for file transfers on port {TRANSFER_PORT}...\n")

            while True:
                client_socket, addr = server.accept()
                threading.Thread(
                    target=self._handle_incoming_file,
                    args=(client_socket, addr),
                    daemon=True
                ).start()

    def _handle_incoming_file(self, client_socket, addr):
        with client_socket:
            try:
                metadata = client_socket.recv(BUFFER_SIZE).decode()
                sender_name, filename, filesize = metadata.split('|')
                filesize = int(filesize)

                print(f"\nFile transfer request from {sender_name} ({addr[0]}):")
                print(f"Filename: {filename} | Size: {filesize} bytes")
                choice = input("Accept file? (y/n): ").strip().lower()

                if choice != 'y':
                    client_socket.send(b'REJECT')
                    print("File rejected.")
                    return

                client_socket.send(b'ACCEPT')

                with open(filename, 'wb') as f:
                    received = 0
                    while received < filesize:
                        data = client_socket.recv(BUFFER_SIZE)
                        if not data:
                            break
                        f.write(data)
                        received += len(data)

                print(f"File '{filename}' received successfully.\n")

            except Exception as e:
                print(f"Error during file reception: {e}")

    def stop(self):
        self.stop_discovery.set()
