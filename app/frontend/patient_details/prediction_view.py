import logging

from PySide2.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import (
    FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from util import unzip

logging.getLogger("matplotlib").setLevel(logging.WARNING)
from matplotlib.figure import Figure


class PredictionsView(QWidget):
    """View for drawing chosen already generated predictions"""

    def __init__(self, measurements, predictions):
        QWidget.__init__(self)
        self.colors = ["yellow", "red", "cyan", "magenta", "green", "blue"]
        self.resize(1500, 800)

        self.predictions = predictions
        self.measurements = measurements

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
            ".",
            color="black",
            label="Pomiary",
        )

        for prediction_datetime, prediction_value_list in self.predictions.items():
            color = self.colors.pop()
            dates, prediction_values = unzip(
                [(p.date, p.value) for p in prediction_value_list]
            )
            self.axes.plot(
                dates,
                prediction_values,
                ".",
                color=color,
                label=f"Predykcja z {prediction_datetime.isoformat()}",
            )
        self.axes.legend()