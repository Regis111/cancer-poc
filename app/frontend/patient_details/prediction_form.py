from datetime import datetime

from PySide2.QtWidgets import QComboBox, QPushButton, QVBoxLayout, QDialog

from db.prediction import create_prediction_for_patient
from reservoir.engine import (
    generate_prediction_subreservoir,
    generate_prediction_deep_esn,
    generate_prediction_esn_base,
)

import logging


class PredictionForm(QDialog):
    base_esn_method = "ESN"
    deep_esn_method = "DeepESN"
    sub_reservoir_method = "SubReservoirESN"
    name_to_impl = {
        base_esn_method: generate_prediction_esn_base,
        deep_esn_method: generate_prediction_deep_esn,
        sub_reservoir_method: generate_prediction_subreservoir,
    }

    def __init__(self, parent, patient):
        QDialog.__init__(self)
        self.parent = parent
        self.patient = patient

        self.choose_method = QComboBox()
        self.choose_method.addItem(self.base_esn_method)
        self.choose_method.addItem(self.deep_esn_method)
        self.choose_method.addItem(self.sub_reservoir_method)

        self.predict_button = QPushButton("Stwórz predykcję")
        self.predict_button.clicked.connect(self.generatePrediction)

        layout = QVBoxLayout(self)
        layout.addWidget(self.choose_method)
        layout.addWidget(self.predict_button)

    def generatePrediction(self):
        method_name = self.choose_method.currentText()
        prediction_fun = self.name_to_impl[method_name]
        date_values = prediction_fun(self.patient.measurements)
        p = create_prediction_for_patient(
            self.patient,
            method_name,
            datetime.now().replace(microsecond=0),
            date_values,
        )
        logging.debug("Generated prediction %s", p)
        self.parent.addPrediction(p)
        self.accept()
