from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QPushButton,
    QTabWidget,
    QWidget,
    QVBoxLayout,
)

from frontend.patient_details.details_tab import DetailsTab
from frontend.patient_details.measurements_tab import MeasurementsTab
from frontend.patient_details.predictions_tab import PredictionsTab


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
