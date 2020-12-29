import logging

from PySide2.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
)


class DetailsTab(QWidget):
    def __init__(self, patient):
        QWidget.__init__(self)
        name_label = QLabel("Name:")

        name_label_value = QLabel(patient.name)
        name_label_value.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        surname_label = QLabel("Surname:")

        surname_label_value = QLabel(patient.surname)
        surname_label_value.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(name_label)
        main_layout.addWidget(name_label_value)
        main_layout.addWidget(surname_label)
        main_layout.addWidget(surname_label_value)
