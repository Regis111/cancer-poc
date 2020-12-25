import logging

from PySide2.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import (
    FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from util import unzip

from db.config import DATETIME_FORMAT
logging.getLogger("matplotlib").setLevel(logging.WARNING)
from matplotlib.figure import Figure


class PredictionsView(QWidget):
    """View for drawing chosen already generated predictions"""


    def __init__(self, measurements, predictions):
        QWidget.__init__(self)
        self.colors = ["yellow", "red", "cyan", "magenta", "green", "blue"]
        self.resize(1500, 800)

        self.measurements = measurements
        self.predictions = predictions

        logging.debug("Predictions number: %d", len(self.predictions))

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(NavigationToolbar(self.canvas, self))

        self.axes = self.canvas.figure.subplots()

        m_dates, measurements_values = unzip(
            [(m.date, m.value) for m in self.measurements]
        )
        self.axes.plot(
            m_dates,
            measurements_values,
            "-o",
            color="black",
            label="Pomiary",
        )
        for prediction in self.predictions:
            color = self.colors.pop()
            dates = [pv.date for pv in prediction.prediction_values]
            prediction_values = [pv.value for pv in prediction.prediction_values]
            self.axes.plot(
                dates,
                prediction_values,
                ".",
                color=color,
                label=f"{prediction.method} {prediction.datetime_created.strftime(DATETIME_FORMAT)}",
            )
        self.axes.legend()
