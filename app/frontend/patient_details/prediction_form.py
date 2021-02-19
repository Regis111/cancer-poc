from data_model.Prediction import Prediction
from data_model.Treatment import Treatment
from datetime import datetime
from operator import attrgetter
from PySide2.QtWidgets import (
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QDoubleSpinBox,
    QDialog,
    QStyledItemDelegate,
    QFormLayout,
    QLabel,
    QToolButton,
    QDateEdit,
    QProgressDialog,
    QProgressBar,
)
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt, QThread, Signal

from db.prediction import create_prediction_for_patient
from prediction.reservoir import (
    generate_prediction_subreservoir,
    generate_prediction_deep_esn,
    generate_prediction_esn_base,
)
from prediction.abc_smc import generate_prediction_abc_smc
import logging


class PredictionForm(QDialog):
    base_esn_method = "ESN"
    deep_esn_method = "DeepESN"
    sub_reservoir_method = "SubReservoirESN"
    abc_smc_method = "ABC-SMC"
    name_to_impl = {
        base_esn_method: generate_prediction_esn_base,
        deep_esn_method: generate_prediction_deep_esn,
        sub_reservoir_method: generate_prediction_subreservoir,
        abc_smc_method: generate_prediction_abc_smc,
    }

    def __init__(self, parent, patient):
        QDialog.__init__(self)
        self.parent = parent
        self.patient = patient
        self.resize(480, 100)
        self.setWindowTitle("Stwórz predykcję")

        self.choose_method = QComboBox()
        self.choose_method.setItemDelegate(QStyledItemDelegate())
        self.choose_method.addItem(self.base_esn_method)
        self.choose_method.addItem(self.deep_esn_method)
        self.choose_method.addItem(self.sub_reservoir_method)
        self.choose_method.addItem(self.abc_smc_method)

        spin_box = QDoubleSpinBox()
        spin_box.setRange(0.0, 1000.0)
        spin_box.setSingleStep(0.1)
        self.choose_prediction_length = spin_box

        self.predict_button = QPushButton("Stwórz predykcję")
        self.predict_button.clicked.connect(self.generatePrediction)

        self.add_future_treatment_button = QPushButton("Dodaj podanie lekarstwa")
        self.add_future_treatment_button.clicked.connect(self.addFutureTreatment)

        self.form_layout = QFormLayout()
        self.form_layout.addRow("Wybierz metodę", self.choose_method)
        self.form_layout.addRow(
            "Długość predykcji (dni)", self.choose_prediction_length
        )

        self.treatments = []

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.add_future_treatment_button)
        buttons_layout.addWidget(self.predict_button)

        layout = QVBoxLayout(self)
        layout.addLayout(self.form_layout)
        layout.addLayout(buttons_layout)

    def addFutureTreatment(self):
        row = QHBoxLayout()
        row.addWidget(QLabel("Wybierz punkt podania lekarstwa"))
        treatment_date = QDateEdit()

        treatment_date.setMinimumDate(self.patient.measurements[-1].date)
        row.addWidget(treatment_date)

        remove_treatment_button = QToolButton()
        remove_treatment_button.setIcon(QIcon("resources/icon/minus.png"))
        remove_treatment_button.setStatusTip("Usuń")

        row.addWidget(remove_treatment_button)

        self.treatments.append(treatment_date)

        self.form_layout.addRow(row)

        def remove_treatment():
            self.form_layout.removeRow(row)
            self.treatments.remove(treatment_date)

        remove_treatment_button.clicked.connect(remove_treatment)

    def generatePrediction(self):
        self.method_name = self.choose_method.currentText()
        self.prediction_length = self.choose_prediction_length.value()
        form_treatments = sorted(
            [Treatment(0, t_date.date().toPython(), 1) for t_date in self.treatments],
            key=attrgetter("date"),
        )
        treatments = self.patient.treatments + form_treatments
        self.accept()

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_dialog = QProgressDialog(
            f"Generowanie predykcji za pomocą {self.method_name}", None, 0, 1
        )
        self.progress_dialog.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setBar(self.progress_bar)

        prediction_fun = self.name_to_impl[self.method_name]

        self.progress_dialog.show()
        self.runnable = PredictionRunnable(
            prediction_fun,
            self.patient.measurements,
            self.prediction_length,
            treatments,
        )
        self.runnable.result.connect(self.handlePrediction)
        self.runnable.start()

    def handlePrediction(self, predictions):
        self.progress_dialog.close()
        for date_values in predictions:
            prediction_obj: Prediction = create_prediction_for_patient(
                self.patient,
                self.method_name,
                datetime.now().replace(microsecond=0),
                date_values,
            )
            logging.debug("Generated prediction %s", prediction_obj)
            self.parent.addPrediction(prediction_obj)


class PredictionRunnable(QThread):
    result = Signal(list)

    def __init__(self, method, measurements, length, treatments):
        QThread.__init__(self)
        self.method = method
        self.measurements = measurements
        self.length = length
        self.treatments = treatments

    def run(self):
        predictions = self.method(self.measurements, self.length, self.treatments)
        self.result.emit(predictions)