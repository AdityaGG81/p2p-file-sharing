import os
import socket
from config import BUFFER_SIZE

class FileTransfer:
    @staticmethod
    def send_file(conn, file_path):
        filesize = os.path.getsize(file_path)
        with open(file_path, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                conn.sendall(bytes_read)
                

    @staticmethod
    def recieve_file(conn, filesize, save_path):
        with open(save_path, "wb") as f:
            bytes_received = 0
            while bytes_received < filesize:
                chunk = conn.recv(BUFFER_SIZE)
                if not chunk:
                    break
                f.write(chunk)
                bytes_recieved += len(chunk)