import socket
from PySide6.QtWidgets import QLabel, QMainWindow
from PySide6.QtCore import QSize, QThread, Signal, Slot
from PySide6.QtGui import QPixmap, QFont
from json import loads
from json.decoder import JSONDecodeError
from utils.static_engine_render import (
    load_hot_icon,
    load_cold_icon,
    load_warm_icon,
    load_offline_icon
)


class ServerThread(QThread):
    update_icon = Signal(QPixmap, float)

    def __init__(self, host="0.0.0.0", port=666):
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
                            received_message = data.decode('utf-8').strip()
                            tmp = loads(received_message)["temperature"]

                            if tmp <= 22:
                                self.update_icon.emit(QPixmap(load_cold_icon()).scaled(100, 100), tmp)

                            elif tmp <= 30:
                                self.update_icon.emit(QPixmap(load_warm_icon()).scaled(100, 100), tmp)

                            elif tmp <= 38:
                                self.update_icon.emit(QPixmap(load_hot_icon()).scaled(100, 100), tmp)

                        except socket.error as e:
                            print(f"Socket error: {e}")
                            continue

                        except JSONDecodeError as e:
                            print(f"Json error: {e}")
                            continue


class ThermistorWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(300, 200))
        self.setObjectName("Thermistor")

        self.label_icon = QLabel(self)
        self.label_icon.setFixedSize(QSize(100, 100))
        self.label_icon.setPixmap(
            QPixmap(load_offline_icon()).scaled(100, 100)
        )
        self.label_icon.move(100, 30)

        self.label_text = QLabel(self)
        self.label_text.setFont(QFont("Arial", 20))
        self.label_text.move(100, 140)

        self.worker = ServerThread()
        self.worker.update_icon.connect(self.update_icon_label)
        self.worker.start()

    @Slot(QPixmap, str)
    def update_icon_label(self, pixmap, tmp):
        self.label_icon.setPixmap(pixmap)
        self.label_text.setText(f"{tmp} °C")
