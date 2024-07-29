import socket
from PySide6.QtWidgets import QLabel, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, \
    QGraphicsTextItem
from PySide6.QtCore import QSize, QThread, Signal, Slot, Qt
from PySide6.QtGui import QPixmap, QFont, QColor, QBrush, QPen
from utils.static_engine_render import (
    load_hot_icon,
    load_cold_icon,
    load_warm_icon,
    load_offline_icon
)


class ServerThread(QThread):
    update_icon = Signal(QPixmap, float)
    update_distance = Signal(float)

    def __init__(self, host="0.0.0.0", port=777):
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
                            received_message = float(data.decode('utf-8').strip())

                            if received_message <= 22:
                                self.update_icon.emit(QPixmap(load_cold_icon()).scaled(100, 100), received_message)

                            elif received_message <= 30:
                                self.update_icon.emit(QPixmap(load_warm_icon()).scaled(100, 100), received_message)

                            elif received_message <= 38:
                                self.update_icon.emit(QPixmap(load_hot_icon()).scaled(100, 100), received_message)

                            self.update_distance.emit(received_message)

                        except socket.error as e:
                            print(f"Socket error: {e}")
                            continue

                        except ValueError as e:
                            print(f"Value error: {e}")
                            continue


class SonicWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(300, 200))
        self.setObjectName("Sonic")

        self.label_icon = QLabel(self)
        self.label_icon.setFixedSize(QSize(110, 100))
        self.label_icon.setPixmap(
            QPixmap(load_offline_icon()).scaled(100, 100)
        )
        self.label_icon.move(100, 30)

        self.label_text = QLabel(self)
        self.label_text.setFont(QFont("Arial", 20))
        self.label_text.setFixedSize(QSize(110, 40))
        self.label_text.move(100, 140)

        self.graphics_view = QGraphicsView(self)
        self.graphics_view.setGeometry(10, 10, 280, 180)
        self.scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.scene)

        self.circle_item = QGraphicsEllipseItem()
        self.scene.addItem(self.circle_item)

        self.distance_text_item = QGraphicsTextItem()
        self.distance_text_item.setFont(QFont("Arial", 12))
        self.distance_text_item.setDefaultTextColor(Qt.black)
        self.scene.addItem(self.distance_text_item)

        self.update_circle_size(0)

        self.worker = ServerThread()
        self.worker.update_icon.connect(self.update_icon_label)
        self.worker.update_distance.connect(self.update_circle_size)
        self.worker.start()

    @Slot(QPixmap, float)
    def update_icon_label(self, pixmap, distance):
        self.label_icon.setPixmap(pixmap)
        self.label_text.setText(f"{distance:.2f} cm")

    @Slot(float)
    def update_circle_size(self, distance):
        max_radius = 80
        min_radius = 10

        max_distance = 100
        radius = max(min_radius, min(max_radius, max_distance - distance))

        self.circle_item.setRect(-radius, -radius, 2 * radius, 2 * radius)
        self.circle_item.setPos(self.graphics_view.width() / 2 - radius, self.graphics_view.height() / 2 - radius)
        self.circle_item.setBrush(QBrush(QColor(0, 0, 255, 100)))
        self.circle_item.setPen(Qt.NoPen)

        self.distance_text_item.setPlainText(f"{distance:.2f} cm")
        self.distance_text_item.setPos(
            self.graphics_view.width() / 2 - self.distance_text_item.boundingRect().width() / 2,
            self.graphics_view.height() / 2 - self.distance_text_item.boundingRect().height() / 2)
