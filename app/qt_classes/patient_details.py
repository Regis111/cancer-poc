import logging

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QPushButton,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
)

from qt_classes.measurements_tab import MeasurementsTab
from qt_classes.predictions_tab import PredictionsTab

logging.basicConfig(level=logging.DEBUG)


class PatientDetailsView(QWidget):
    def __init__(self, patient):
        QWidget.__init__(self)
        self.setWindowFlags(Qt.Window)

        tab_widget = QTabWidget()
        tab_widget.addTab(DetailsTab(patient), "Szczegóły pacjenta")
        tab_widget.addTab(MeasurementsTab(patient, ("MTD", "mm")), "Pomiary MTD")
        tab_widget.addTab(PredictionsTab(patient), "Predykcje MTD")

        self.back_button = QPushButton("Wróć")

        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        main_layout.addWidget(self.back_button)
        self.setLayout(main_layout)

        self.setWindowTitle(f"Pacjent {patient.name} {patient.surname}")


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
