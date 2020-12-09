from PySide2.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import (
    FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure

from db.prediction import get_predictions_for_patient_id, create_predictions_for_patient
from reservoir.engine import generate_prediction
from util import unzip


class PredictionView(QWidget):
    def __init__(self, patient):
        QWidget.__init__(self)
        self.patient = patient

        self.static_canvas = FigureCanvas(Figure(figsize=(5, 3)))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.static_canvas)
        self.layout.addWidget(NavigationToolbar(self.static_canvas, self))
        self._static_ax = self.static_canvas.figure.subplots()
        m_dates, measurements = self.loadMeasurements()
        p_dates, predictions = self.loadPredictions()
        self._static_ax.plot(m_dates, measurements, ".", color="blue")
        self._static_ax.plot(p_dates, predictions, ".", color="red")
        self.setLayout(self.layout)

    def loadPredictions(self):
        predictions = get_predictions_for_patient_id(self.patient.db_id)
        if not predictions:
            dates_values = generate_prediction(self.patient.measurements)
            predictions = create_predictions_for_patient(self.patient, dates_values)
        return unzip([(p.date, p.value) for p in predictions])

    def loadMeasurements(self):
        return unzip([(m.date, m.value) for m in self.patient.measurements])