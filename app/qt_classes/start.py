from PySide2.QtWidgets import (
    QPushButton,
    QWidget,
)
import logging

logging.basicConfig(level=logging.DEBUG)


class StartView(QWidget):
    def __init__(self, width, height):
        QWidget.__init__(self)

        self.width = width
        self.height = height

        self.button_size = (150, 50)

        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(
            (self.width / 2) - (self.button_size[0] / 2) - 125,
            (self.height / 2) - (self.button_size[1] / 2),
            self.button_size[0],
            self.button_size[1],
        )

        self.help_button = QPushButton("Help", self)
        self.help_button.setGeometry(
            (self.width / 2) - (self.button_size[0] / 2) + 125,
            (self.height / 2) - (self.button_size[1] / 2),
            self.button_size[0],
            self.button_size[1],
        )
