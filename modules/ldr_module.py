import socket
from PySide6.QtWidgets import QLabel, QMainWindow
from PySide6.QtCore import QSize, QThread, Signal, Slot
from PySide6.QtGui import QPixmap
from utils.static_engine_render import (
    load_evening_icon,
    load_morning_icon,
    load_afternoon_icon,
    load_offline_icon
)


class ServerThread(QThread):
    update_icon = Signal(QPixmap)

    def __init__(self, host="0.0.0.0", port=555):
        super().__init__()
        self.host = host
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"Server listening on {self.host}:{self.port}...")

            while True:
                client_socket, client_address = server_socket.accept()
                print(f"Connected to {client_address}")
                with client_socket:
                    while True:
                        try:
                            data = client_socket.recv(1024)
                            if not data:
                                break
                            received_message = int(data.decode('utf-8').strip())

                            if 1000 <= received_message < 2000:
                                self.update_icon.emit(QPixmap(load_afternoon_icon()).scaled(100, 100))

                            elif received_message >= 2000:
                                self.update_icon.emit(QPixmap(load_morning_icon()).scaled(100, 100))

                            elif 0 <= received_message <= 200:
                                self.update_icon.emit(QPixmap(load_evening_icon()).scaled(100, 100))

                        except socket.error as e:
                            print(f"Socket error: {e}")
                            break


class LDRModuleWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(300, 200))
        self.setObjectName("LDR")

        self.label_icon = QLabel(self)
        self.label_icon.setPixmap(
            QPixmap(load_offline_icon()).scaled(100, 100)
        )
        self.label_icon.setFixedSize(QSize(100, 100))
        self.label_icon.move(100, 40)

        self.worker = ServerThread()
        self.worker.update_icon.connect(self.update_icon_label)
        self.worker.start()

    @Slot(QPixmap)
    def update_icon_label(self, pixmap):
        self.label_icon.setPixmap(pixmap)
