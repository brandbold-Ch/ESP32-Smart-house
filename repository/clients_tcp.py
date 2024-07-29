import socket


class TCPClient:
    def __init__(self, ip, port):
        self.server_ip = ip
        self.server_port = port

    def send_data(self, sock, command: str):
        try:
            sock.sendall(command.encode('utf-8'))
            print("Message sent.")
        except socket.error as e:
            print(f"Error sending data: {e}")

    def engine(self, command: str):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                print(f"Connecting to {self.server_ip}:{self.server_port}...")
                sock.connect((self.server_ip, self.server_port))
                print(f"Server connected: {self.server_ip}")

                self.send_data(sock, command)
        except (ConnectionError, OSError) as e:
            print(f"Error in connection: {e}")
