from PySide6.QtWidgets import QPushButton, QLabel
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap
from utils.static_engine_render import load_on_icon, load_off_icon
from repository.clients_tcp import TCPClient

client_leds = TCPClient("192.168.1.101", 444)


class LedModuleWidget(QPushButton):

    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(300, 200))
        self.setObjectName("Leds")

        self.label_icon = QLabel(self)
        self.label_icon.setPixmap(
            QPixmap(load_off_icon()).scaled(100, 100)
        )
        self.label_icon.move(100, 40)

    def status_light(self, state: int) -> None:
        match state:
            case 0:
                self.label_icon.setPixmap(
                    QPixmap(load_off_icon()).scaled(100, 100)
                )
                client_leds.engine("0")
                self.setStyleSheet("""
                    #Leds {
                        background-color: #181717;
                        border-radius: 10px;
                    }
                    #Leds:hover {
                        background-color: #383737;
                        border-radius: 10px;
                    }
                """)

            case 1:
                self.label_icon.setPixmap(
                    QPixmap(load_on_icon()).scaled(100, 100)
                )
                client_leds.engine("1")
                self.setStyleSheet("""
                    #Leds {
                        background-color: #f1f165;
                        border-radius: 10px;
                    }
                    #Leds:hover {
                        background-color: #e5e586;
                        border-radius: 10px;
                    }
                """)
