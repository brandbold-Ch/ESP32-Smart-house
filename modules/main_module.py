from PySide6.QtWidgets import QMainWindow, QWidget, QLabel
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap
from modules.led_module import LedModuleWidget
from modules.ldr_module import LDRModuleWidget
from modules.thermistor_module import ThermistorWindow
from modules.ultrasonic_module import SonicWindow
from utils.static_engine_render import load_logo_icon, load_styles


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(600, 480))
        self.setStyleSheet(load_styles())
        self.setWindowTitle("Mileróticos")
        self.leds = LedModuleWidget()
        self.ldr = LDRModuleWidget()
        self.thermistor = ThermistorWindow()
        self.sonic = SonicWindow()
        self.led_status = False

        self.project_description = QWidget(self)
        self.project_description.setFixedSize(QSize(600, 70))
        self.project_description.setObjectName("Description")

        self.label = QLabel(self)
        self.label.setPixmap(
            QPixmap(load_logo_icon()).scaled(180, 100)
        )
        self.label.setObjectName("Title")
        self.label.setFixedSize(QSize(250, 50))
        self.label.move(200, 10)

        self.leds.setParent(self)
        self.ldr.setParent(self)
        self.thermistor.setParent(self)
        self.sonic.setParent(self)

        self.leds.move(0, 75)
        self.ldr.move(300, 75)
        self.thermistor.move(0, 280)
        self.sonic.move(300, 280)

        self.leds.clicked.connect(lambda x: self.leds_event())

    def leds_event(self) -> None:
        if self.led_status is False:
            self.leds.status_light(1)
            self.led_status = True

        else:
            self.leds.status_light(0)
            self.led_status = False
