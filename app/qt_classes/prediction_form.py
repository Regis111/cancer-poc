from datetime import datetime

from PySide2.QtWidgets import QComboBox, QPushButton, QVBoxLayout, QDialog

from db.prediction import create_prediction_for_patient
from reservoir.engine import (
    generate_prediction_subreservoir,
    generate_prediction_deep_esn,
)


class PredictionForm(QDialog):
    deep_esn_method = "DeepESN"
    sub_reservoir_method = "SubReservoir"

    def __init__(self, patient):
        QDialog.__init__(self)
        self.patient = patient

        self.choose_method = QComboBox()
        self.choose_method.addItem(self.deep_esn_method)
        self.choose_method.addItem(self.sub_reservoir_method)

        self.predict_button = QPushButton("Stwórz predykcję")
        self.predict_button.clicked.connect(self.generatePrediction)

        layout = QVBoxLayout(self)
        layout.addWidget(self.choose_method)
        layout.addWidget(self.predict_button)

    def generatePrediction(self):
        method = self.choose_method.currentText()
        date_values = (
            generate_prediction_deep_esn(self.patient.measurements)
            if method == self.deep_esn_method
            else generate_prediction_subreservoir(self.patient.measurements)
        )
        create_prediction_for_patient(self.patient, datetime.now(), date_values)
        self.accept()
